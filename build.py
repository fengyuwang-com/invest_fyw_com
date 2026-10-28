#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FengInvest 研究库 — 零依赖静态站生成器

设计约束：
  * 只用 Python 标准库（无 pip、无 npm、无 Node、无第三方包）。
  * 内容白名单：只生成 publish_manifest.json 明确列出的文件。
  * 默认拒绝：清单之外的文件永远不会进入 dist/。
  * 生成前逐篇脱敏 + 泄漏硬扫描，命中即终止，不出包。

用法：
  python build.py                 # 生成到 invest/dist/
  python build.py --check         # 只做清单/脱敏/泄漏检查，不写文件
  python -m http.server 8002 --directory dist   # 本地预览
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

HERE = Path(__file__).resolve().parent
ROOT = HERE
DIST = HERE / "dist"
TPL_DIR = HERE / "templates"
ASSET_DIR = HERE / "assets"
ASSETS_SRC = HERE / "assets"

CHECK_ONLY = "--check" in sys.argv

# 源文件名 → 站内地址，用于把文档里的相对 .md 互链改写成发布页
LINK_MAP: dict[str, str] = {}

# ---------------------------------------------------------------------------
# 基础工具
# ---------------------------------------------------------------------------


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ascii_slug(value: str) -> str:
    s = value.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or hashlib.sha1(value.encode("utf-8")).hexdigest()[:10]


def split_front_matter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, text[m.end():]


def take_first_h1(body: str) -> tuple[str | None, str]:
    m = re.search(r"^#\s+(.+?)\s*$", body, re.M)
    if not m:
        return None, body
    return m.group(1).strip(), (body[: m.start()] + body[m.end():]).lstrip("\n")


def plain_text(value: str) -> str:
    value = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = value.replace("**", "").replace("__", "").replace("`", "")
    value = re.sub(r"[*_~]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def excerpt_from(body: str, limit: int = 180) -> str:
    lines = body.splitlines()
    for i, line in enumerate(lines):
        s = line.strip()
        if not s or s.startswith(("#", "|", "---", "```")):
            continue
        if s.startswith(">"):
            buf = []
            j = i
            while j < len(lines) and lines[j].strip().startswith(">"):
                buf.append(lines[j].strip().lstrip(">").strip())
                j += 1
            s = " ".join(buf)
        elif re.match(r"^([-*+]|\d+\.)\s+", s):
            s = re.sub(r"^([-*+]|\d+\.)\s+", "", s)
        s = plain_text(s)
        if s:
            return s if len(s) <= limit else s[:limit].rstrip() + "…"
    return ""


def headings_from(body: str) -> list[str]:
    return [plain_text(h) for h in re.findall(r"^#{2,3}\s+(.+?)\s*$", body, re.M)]


# ---------------------------------------------------------------------------
# 脱敏 + 泄漏硬扫描
# ---------------------------------------------------------------------------

INTERNAL_PATH_RE = re.compile(
    r"`(?:tools|sources|research|data|fengweb|docs|logs|holdings|portfolio|Temp|\.zcode|\.agents)/[^`\n]*`"
)
# 正文里不带反引号的本地私有目录，按语义替换成中性词，避免暴露目录结构
BARE_PRIVATE_PATHS = [
    (re.compile(r"holdings/SCHEMA\.md"), "持仓登记结构"),
    (re.compile(r"holdings/"), "持仓模块"),
    (re.compile(r"portfolio/"), "组合模块"),
    (re.compile(r"(?<![\w/])logs/"), "日志目录"),
    (re.compile(r"(?<![\w/])alerts/"), "提醒目录"),
    (re.compile(r"(?<![\w/])reviews/"), "复盘目录"),
    (re.compile(r"research/state"), "状态目录"),
    (re.compile(r"research/speculative"), "投机研究目录"),
    (re.compile(r"knowledge/personal"), "个人笔记"),
    (re.compile(r"data/config/llm_config\.json"), "本地配置"),
    (re.compile(r"(?<![\w/])(?:Temp|\.zcode|\.agents)/"), "本地目录"),
]
WIN_PATH_RE = re.compile(r"(?<![\w])[A-Za-z]:\\[^\s`，。；、）)\]]+")
POSIX_PATH_RE = re.compile(r"(?<![\w])[A-Za-z]:/[^\s`，。；、）)\]]+")
MSYS_PATH_RE = re.compile(r"(?<![\w])/c/[^\s`，。；、）)\]]+", re.I)
POSITION_RE = re.compile(
    r"((?:建议|目标|当前|计划)?仓位(?:目标|建议|上限|下限)?)"
    r"([^\d\n，。；（）()]{0,12}?)"
    r"(\d+(?:\.\d+)?(?:\s*[-~—]\s*\d+(?:\.\d+)?)?\s*%)"
)
BUILD_POSITION_RE = re.compile(
    r"((?:首次|建议|计划|目标|开始)?建仓(?:目标|建议|比例|上限)?)"
    r"([^\d\n，。；（）()]{0,10}?)"
    r"(\d+(?:\.\d+)?(?:\s*[-~—]\s*\d+(?:\.\d+)?)?\s*%)"
)
POSITION_KEY_RE = re.compile(r"position_pct\s*[:=]\s*[^\s`,，。;；、）)\]]+")
REVERSED_POSITION_RE = re.compile(r"\d+(?:\.\d+)?\s*%\s*(?:的)?(仓位|建仓|持仓)")
POSITION_ROW_RE = re.compile(r"^(\|[^|\n]*仓位[^|\n]*\|)([^|\n]*)(\|.*)$", re.M)
TITLE_POSITION_RE = re.compile(r"\s*@\s*\d+(?:\.\d+)?\s*%")
TRAILING_TARGET_RE = re.compile(r"\s*[|｜]\s*目标价[:：][^\n]*$")

FORBIDDEN = [
    (r"hold_\d", "持仓文件名"),
    (r"holdings/", "持仓目录"),
    (r"knowledge/personal", "个人知识目录"),
    (r"投资血泪史", "个人血泪史"),
    (r"logs/journal", "决策日志"),
    (r"portfolio/current", "组合文件"),
    (r"temp_state_", "状态文件"),
    (r"api_key", "API Key 字段"),
    (r"sk-[A-Za-z0-9]{12,}", "API Key"),
    (r"Bearer\s+[A-Za-z0-9._-]{8,}", "Bearer Token"),
    (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "邮箱地址"),
    (r"(?<![\w])[A-Za-z]:[\\/]", "绝对路径"),
]


POSITION_HEADER_RE = re.compile(r"position_pct|仓位")


def redact_position_tables(text: str) -> tuple[str, int]:
    """把带仓位列的 Markdown 表格里的数值整列抹掉。"""
    lines = text.split("\n")
    hits = 0
    i = 0
    while i < len(lines):
        if not lines[i].strip().startswith("|"):
            i += 1
            continue
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        cols = [j for j, c in enumerate(cells) if POSITION_HEADER_RE.search(c)]
        if not cols:
            i += 1
            continue
        col = cols[0]
        i += 1
        if i < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i]):
            i += 1
        while i < len(lines) and lines[i].strip().startswith("|"):
            parts = lines[i].strip().split("|")
            # parts[0] 是行首竖线前的空串，第 col 列对应 parts[col + 1]
            if len(parts) > col + 1 and re.search(r"\d", parts[col + 1]):
                parts[col + 1] = " 已隐去 "
                lines[i] = "|".join(parts)
                hits += 1
            i += 1
    return "\n".join(lines), hits


PERSONAL_POSITION_RE = re.compile(
    r"((?:我的|本人|实际|当前)?(?:仓位|持仓)(?:建议|比例|占比)?)(\s*(?:为|[:：])?\s*)"
    r"(?:\*\*|__|`)?\s*\d+(?:\.\d+)?\s*%(?:\*\*|__|`)?"
)


def sanitize_text(text: str, strict_position: bool = False) -> tuple[str, int]:
    """返回 (脱敏后文本, 命中条数)。

    strict_position 用于公司报告：报告里的仓位/目标价一律隐去；
    知识/思想/讨论/列传里只抹「我的仓位」这类个人持仓表述，保留通用的
    仓位管理知识（如大师的 3% 单笔规则），否则会把公开内容阉割掉。
    """
    hits = 0

    def internal_path(_m):
        nonlocal hits
        hits += 1
        return "内部数据"

    text = INTERNAL_PATH_RE.sub(internal_path, text)

    for pattern, replacement in BARE_PRIVATE_PATHS:
        text, n = pattern.subn(replacement, text)
        hits += n

    for pattern in (WIN_PATH_RE, POSIX_PATH_RE, MSYS_PATH_RE):
        text, n = pattern.subn("", text)
        hits += n

    if strict_position:
        text, n = redact_position_tables(text)
        hits += n
        text, n = POSITION_ROW_RE.subn(lambda m: m.group(1) + " 已隐去 " + m.group(3), text)
        hits += n
        text, n = POSITION_KEY_RE.subn("", text)
        hits += n
    if strict_position:
        def _position_repl(m):
            # 保留原样的 Markdown 强调符/分隔符，只把数字替换掉，避免破坏加粗
            return m.group(1) + m.group(2) + "已隐去"

        text, n = POSITION_RE.subn(_position_repl, text)
        hits += n
        text, n = BUILD_POSITION_RE.subn(_position_repl, text)
        hits += n
        text, n = REVERSED_POSITION_RE.subn(lambda m: "已隐去" + m.group(1), text)
        hits += n
        text, n = TITLE_POSITION_RE.subn("", text)
        hits += n
        # 剥掉 `@ 30%` 后可能留下空的行内代码标记，会破坏后续解析
        text = re.sub(r"`\s*`", "", text)
        # 抹掉字段后可能留下悬空标点
        text = re.sub(r"[：:]\s*([，。；、])", r"\1", text)
        text = re.sub(r"[ \t]+([，。；、])", r"\1", text)
        text, n = TRAILING_TARGET_RE.subn("", text)
        hits += n
    else:
        text, n = PERSONAL_POSITION_RE.subn(lambda m: m.group(1) + "已隐去", text)
        hits += n

    return text, hits


def assert_clean(text: str, rel: str) -> None:
    for pattern, label in FORBIDDEN:
        m = re.search(pattern, text)
        if m:
            raise SystemExit(
                f"\n[泄漏扫描失败] {rel}\n"
                f"  命中：{label}\n"
                f"  片段：{m.group(0)[:120]}\n"
                f"  处理：把该内容从源文件移除，或在 publish_manifest.json 中排除该文件。\n"
            )


# ---------------------------------------------------------------------------
# Markdown → HTML（标准库实现，覆盖本仓实际用到的语法）
# ---------------------------------------------------------------------------

LIST_ITEM_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
HR_RE = re.compile(r"^\s*([-*_])\s*(?:\1\s*){2,}$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")


def _indent_of(s: str) -> int:
    return len(s) - len(s.lstrip(" "))


def _is_list_item(s: str) -> bool:
    return bool(LIST_ITEM_RE.match(s))


def _split_row(s: str) -> list[str]:
    s = s.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells = re.split(r"(?<!\\)\|", s)
    return [c.strip().replace(r"\|", "|") for c in cells]


def _starts_block(lines: list[str], i: int) -> bool:
    s = lines[i]
    if not s.strip():
        return True
    if HEADING_RE.match(s) or HR_RE.match(s) or s.lstrip().startswith("```"):
        return True
    if s.lstrip().startswith(">"):
        return True
    if _is_list_item(s):
        return True
    if "|" in s and i + 1 < len(lines) and TABLE_SEP_RE.match(lines[i + 1]):
        return True
    return False


def inline_md(text: str) -> str:
    held: list[str] = []

    def hold(fragment: str) -> str:
        held.append(fragment)
        return f"\x00{len(held) - 1}\x00"

    def code(m):
        return hold("<code>" + html.escape(m.group(1), quote=False) + "</code>")

    def image(m):
        alt = html.escape(m.group(1), quote=True)
        src = html.escape(m.group(2), quote=True)
        return hold(f'<img src="{src}" alt="{alt}" loading="lazy">')

    def link(m):
        label = inline_md(m.group(1))
        href = m.group(2).strip()
        # 仓内 .md 互链：能映射到发布页就改成站内地址，映射不到就降级成纯文本
        if ".md" in href and not href.startswith(("http://", "https://")):
            base, _, frag = href.partition("#")
            if base.endswith(".md"):
                public = LINK_MAP.get(base.rsplit("/", 1)[-1])
                if public:
                    if frag:
                        public += "#" + frag
                    return hold(f'<a href="{html.escape(public, quote=True)}">{label}</a>')
                return hold(label)
        target = "" if href.startswith("#") else ' target="_blank" rel="noopener"'
        return hold(f'<a href="{html.escape(href, quote=True)}"{target}>{label}</a>')

    text = re.sub(r"`([^`\n]+)`", code, text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", image, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    text = html.escape(text, quote=False)

    def bare_url(m):
        url = m.group(1).rstrip(".,;:!?)]}")
        tail = m.group(1)[len(url):]
        return hold(
            f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">'
            f'{html.escape(url, quote=False)}</a>{html.escape(tail, quote=False)}'
        )

    # 中文标点常常紧跟 URL，不能吞进链接
    text = re.sub(r"(?<![\"=>])(https?://[^\s<，。；：、（）【】「」『』《》]+)", bare_url, text)
    text = re.sub(r"\*\*([^\n]+?)\*\*", r"<strong>\1</strong>", text)
    # 下划线强调要求词边界，避免把 snake_case 标识符（position_pct）拆成斜体
    text = re.sub(r"(?<![\w])__(?!\s)([^\n]+?)(?<!\s)__(?![\w])", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"(?<![\w])_(?!\s)([^_\n]+?)(?<!\s)_(?![\w])", r"<em>\1</em>", text)
    text = re.sub(r"~~([^\n]+?)~~", r"<del>\1</del>", text)
    text = re.sub(r" {2,}\n", "<br>\n", text)

    for i, fragment in enumerate(held):
        text = text.replace(f"\x00{i}\x00", fragment)
    return text


def _render_table(header: list[str], rows: list[list[str]], aligns: list[str]) -> str:
    def cell(tag: str, value: str, idx: int) -> str:
        style = ""
        if idx < len(aligns) and aligns[idx]:
            style = f' style="text-align:{aligns[idx]}"'
        return f"<{tag}{style}>{inline_md(value)}</{tag}>"

    parts = ["<table><thead><tr>"]
    parts.extend(cell("th", h, i) for i, h in enumerate(header))
    parts.append("</tr></thead><tbody>")
    for row in rows:
        parts.append("<tr>")
        for i in range(len(header)):
            parts.append(cell("td", row[i] if i < len(row) else "", i))
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)


def _render_list(lines: list[str], start: int) -> tuple[str, int]:
    base = _indent_of(lines[start])
    ordered = bool(re.match(r"^\s*\d+[.)]\s+", lines[start]))
    items: list[dict] = []
    i = start

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and _is_list_item(lines[j]) and _indent_of(lines[j]) >= base:
                i = j
                continue
            break
        if not _is_list_item(line):
            break
        ind = _indent_of(line)
        if ind < base:
            break
        if ind > base:
            nested, i = _render_list(lines, i)
            if items:
                items[-1]["children"].append(nested)
            else:
                items.append({"text": "", "children": [nested]})
            continue
        m = LIST_ITEM_RE.match(line)
        item = {"text": m.group(3).strip(), "children": []}
        i += 1
        while (
            i < len(lines)
            and lines[i].strip()
            and not _is_list_item(lines[i])
            and not _starts_block(lines, i)
            and _indent_of(lines[i]) > base
        ):
            item["text"] += " " + lines[i].strip()
            i += 1
        items.append(item)

    tag = "ol" if ordered else "ul"
    out = [f"<{tag}>"]
    for item in items:
        value = item["text"]
        value = re.sub(r"^\[ \]\s*", "☐ ", value)
        value = re.sub(r"^\[[xX]\]\s*", "☑ ", value)
        out.append("<li>" + inline_md(value) + "".join(item["children"]) + "</li>")
    out.append(f"</{tag}>")
    return "".join(out), i


def render_markdown(body: str) -> tuple[str, list[dict]]:
    lines = body.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    toc: list[dict] = []
    counter = [0]
    out: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        if line.lstrip().startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].lstrip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>" + html.escape("\n".join(buf), quote=False) + "</code></pre>")
            continue

        m = HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            counter[0] += 1
            hid = f"h-{counter[0]}"
            out.append(f'<h{level} id="{hid}">{inline_md(text)}</h{level}>')
            if level in (2, 3):
                toc.append({"level": level, "text": plain_text(text), "id": hid})
            i += 1
            continue

        if HR_RE.match(line):
            out.append("<hr>")
            i += 1
            continue

        if "|" in line and i + 1 < len(lines) and TABLE_SEP_RE.match(lines[i + 1]):
            header = _split_row(line)
            aligns = []
            for spec in _split_row(lines[i + 1]):
                spec = spec.strip()
                if spec.startswith(":") and spec.endswith(":"):
                    aligns.append("center")
                elif spec.endswith(":"):
                    aligns.append("right")
                elif spec.startswith(":"):
                    aligns.append("left")
                else:
                    aligns.append("")
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip() and "|" in lines[i]:
                rows.append(_split_row(lines[i]))
                i += 1
            out.append(_render_table(header, rows, aligns))
            continue

        if line.lstrip().startswith(">"):
            buf = []
            while i < len(lines):
                if lines[i].lstrip().startswith(">"):
                    buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                    i += 1
                elif not lines[i].strip() and i + 1 < len(lines) and lines[i + 1].lstrip().startswith(">"):
                    buf.append("")
                    i += 1
                else:
                    break
            inner, _ = render_markdown("\n".join(buf))
            out.append("<blockquote>" + inner + "</blockquote>")
            continue

        if _is_list_item(line):
            rendered, i = _render_list(lines, i)
            out.append(rendered)
            continue

        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not _starts_block(lines, i):
            buf.append(lines[i])
            i += 1
        out.append("<p>" + inline_md("\n".join(buf)) + "</p>")

    return "\n".join(out), toc


# ---------------------------------------------------------------------------
# 内容装载
# ---------------------------------------------------------------------------


def decision_of(text: str) -> str | None:
    m = re.search(r"\b(BUY|WAIT|PASS)\b", text)
    return m.group(1) if m else None


def market_of(ticker: str, name: str) -> str:
    if "ETF" in name.upper() or ticker.upper() in {"LVHI", "159766.SZ"}:
        return "ETF"
    if ticker.endswith((".SZ", ".SS", ".SH")):
        return "A股"
    if ticker.endswith(".HK"):
        return "港股"
    if ticker.endswith((".KS", ".KQ")):
        return "韩股"
    return "美股"


def load_report(path: Path) -> dict:
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    raw = read_text(path)
    _fm, body = split_front_matter(raw)
    raw_title, body = take_first_h1(body)
    parts = path.relative_to(ROOT).parts
    # research/060-companies/<ticker>-<name>/<date>/07-report.md
    company_dir, date = parts[2], parts[3]
    ticker, company_name = company_dir.split("-", 1)
    fallback_title = f"{company_name} — {date}"
    title_raw = raw_title or fallback_title
    decision = decision_of(title_raw) or decision_of(body[:2000])
    title, _ = sanitize_text(title_raw, strict_position=True)
    body, _ = sanitize_text(body, strict_position=True)
    title = re.sub(r"\s{2,}", " ", title).strip(" —-|")
    assert_clean(title + "\n" + body, rel)
    summary = excerpt_from(body)
    company_slug = ascii_slug(ticker)
    return {
        "kind": "report",
        "path": rel,
        "ticker": ticker,
        "company": company_name,
        "company_slug": company_slug,
        "date": date,
        "title": title,
        "raw_title": title_raw,
        "decision": decision,
        "market": market_of(ticker, company_name),
        "summary": summary,
        "body": body,
        "headings": headings_from(body),
        "url": f"/reports/{ascii_slug(ticker)}-{date}.html",
        "company_url": f"/companies/{company_slug}.html",
    }


def load_markdown_doc(path: Path, url: str, category: str, fallback_title: str) -> dict:
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    raw = read_text(path)
    fm, body = split_front_matter(raw)
    h1, body = take_first_h1(body)
    title = fm.get("name") or h1 or fallback_title
    body, _ = sanitize_text(body)
    title, _ = sanitize_text(title)
    assert_clean(title + "\n" + body, rel)
    return {
        "kind": "doc",
        "path": rel,
        "category": category,
        "title": title,
        "summary": excerpt_from(body),
        "body": body,
        "headings": headings_from(body),
        "url": url,
        "meta": fm,
    }


# ---------------------------------------------------------------------------
# 页面片段
# ---------------------------------------------------------------------------

NAV_ITEMS = [
    ("/", "首页", "home"),
    ("/reports/", "公司报告", "reports"),
    ("/companies/", "公司索引", "companies"),
    ("/knowledge/", "知识库", "knowledge"),
    ("/thoughts/", "思想", "thoughts"),
    ("/discussions/", "讨论", "discussions"),
    ("/masters/", "投资家列传", "masters"),
    ("/search.html", "搜索", "search"),
    ("/about.html", "关于", "about"),
]

BOTTOM_ITEMS = [
    ("/", "首页", "home"),
    ("/reports/", "报告", "reports"),
    ("/knowledge/", "知识", "knowledge"),
    ("/search.html", "搜索", "search"),
    ("/about.html", "关于", "about"),
]

DECISION_LABEL = {"BUY": "买入", "WAIT": "等待", "PASS": "回避"}
DECISION_CLASS = {"BUY": "badge-green", "WAIT": "badge-yellow", "PASS": "badge-red"}


def nav_html(active: str) -> str:
    out = []
    for href, label, key in NAV_ITEMS:
        cls = "nav-item active" if key == active else "nav-item"
        out.append(f'<li><a href="{href}" class="{cls}">{label}</a></li>')
    return "".join(out)


def bottom_nav_html(active: str) -> str:
    out = []
    for href, label, key in BOTTOM_ITEMS:
        cls = "bn-item active" if key == active else "bn-item"
        out.append(f'<a href="{href}" class="{cls}">{label}</a>')
    return "".join(out)


def badge(decision: str | None) -> str:
    if not decision:
        return '<span class="badge badge-neutral">未结论</span>'
    return f'<span class="badge {DECISION_CLASS[decision]}">{decision} · {DECISION_LABEL[decision]}</span>'


def report_row(r: dict) -> str:
    return (
        f'<a class="report-row" href="{r["url"]}" data-market="{r["market"]}" data-decision="{r["decision"] or ""}">'
        f'<div class="rr-main">'
        f'<div class="rr-title">{html.escape(r["company"])} <span class="rr-ticker">{html.escape(r["ticker"])}</span></div>'
        f'<div class="rr-summary">{html.escape(r["summary"])}</div>'
        f"</div>"
        f'<div class="rr-meta">{badge(r["decision"])}'
        f'<span class="rr-date">{r["date"]}</span><span class="rr-market">{r["market"]}</span></div>'
        f"</a>"
    )


def entry_card(url: str, title: str, summary: str, meta: str = "") -> str:
    meta_html = f'<div class="entry-meta">{html.escape(meta)}</div>' if meta else ""
    return (
        f'<a class="entry-item" href="{url}">'
        f'<div class="entry-title">{html.escape(title)}</div>'
        f'<div class="entry-preview">{html.escape(summary)}</div>'
        f"{meta_html}</a>"
    )


def page(title: str, desc: str, section: str, body: str, active: str, canonical: str) -> str:
    template = (TPL_DIR / "base.html").read_text(encoding="utf-8")
    values = {
        "TITLE": title,
        "DESC": desc,
        "SECTION": section,
        "BODY": body,
        "NAV": nav_html(active),
        "BOTTOMNAV": bottom_nav_html(active),
        "SITE_NAME": SITE["name"],
        "DISCLAIMER": SITE["disclaimer"],
        "CANONICAL": SITE["base_url"] + canonical,
    }
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def write(rel: str, content: str) -> None:
    target = DIST / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# 页面生成
# ---------------------------------------------------------------------------


def render_doc_page(doc: dict, section: str, active: str, crumb: str) -> str:
    content_html, toc = render_markdown(doc["body"])
    toc_html = ""
    if len(toc) > 2:
        items = []
        for t in toc:
            cls = "toc-l3" if t["level"] == 3 else "toc-l2"
            items.append(f'<a class="{cls}" href="#{t["id"]}">{html.escape(t["text"])}</a>')
        toc_html = (
            f'<details class="card toc-card"><summary>目录（{len(toc)} 节）</summary>'
            f'<div class="toc-list">{"".join(items)}</div></details>'
        )
    meta_rows = []
    fm = doc.get("meta", {})
    for key, label in (("representative", "代表"), ("school", "流派"), ("when_to_use", "何时启用")):
        if fm.get(key):
            meta_rows.append(f'<div><span class="meta-label">{label}</span>{html.escape(fm[key])}</div>')
    meta_html = f'<div class="doc-meta">{"".join(meta_rows)}</div>' if meta_rows else ""
    body = (
        f'<div class="page-header">'
        f'<div class="breadcrumb">{crumb}</div>'
        f'<h1 class="page-title">{html.escape(doc["title"])}</h1>'
        f"{meta_html}"
        f'<div class="reader-tools">字号 '
        f'<button type="button" data-fs-set="s">A-</button>'
        f'<button type="button" data-fs-set="m">A</button>'
        f'<button type="button" data-fs-set="l">A+</button>'
        f"</div></div>"
        f"{toc_html}"
        f'<article class="card report-reader"><div class="md-content">{content_html}</div></article>'
    )
    return page(f'{doc["title"]} · {SITE["name"]}', doc["summary"], section, body, active, doc["url"])


def build_home(reports: list[dict], knowledge: list[dict], thoughts: list[dict], discussions: list[dict], masters: list[dict]) -> None:
    latest = sorted(reports, key=lambda r: r["date"], reverse=True)[:6]
    cards = [
        ("/reports/", "公司报告", f"{len(reports)} 份", "一份份把判断写下来，连同当时的证据与反方。"),
        ("/knowledge/", "知识库", f"{len(knowledge)} 篇", "纪律、方法、原则、策略。"),
        ("/thoughts/", "思想", f"{len(thoughts)} 篇", "整套系统背后的底层逻辑。"),
        ("/discussions/", "讨论", f"{len(discussions)} 篇", "有反方的观点交锋，才值得存档。"),
        ("/masters/", "投资家列传", f"{len(masters)} 位", "别人的方法，自己的判断。"),
    ]
    cards_html = "".join(
        f'<a class="entry-card" href="{url}"><div class="ec-label">{label}</div>'
        f'<div class="ec-count">{count}</div><div class="ec-desc">{desc}</div></a>'
        for url, label, count, desc in cards
    )
    picks = "".join(entry_card(d["url"], d["title"], d["summary"], d.get("category_label", "")) for d in knowledge[:3])
    body = (
        '<section class="hero">'
        '<p class="hero-kicker">FENGINVEST RESEARCH LIBRARY</p>'
        "<h1>买公司，不看报价</h1>"
        "<p>这里没有行情看板，没有涨跌提醒。只有生意、护城河、纪律，"
        "和一份份把判断写下来的报告。</p>"
        '<div class="hero-actions"><a class="btn btn-primary" href="/reports/">读报告</a>'
        '<a class="btn btn-outline" href="/knowledge/">翻知识库</a></div>'
        "</section>"
        f'<section class="entry-grid">{cards_html}</section>'
        '<section class="section-block"><div class="section-title">最新报告</div>'
        f'<div class="report-list">{"".join(report_row(r) for r in latest)}</div></section>'
        '<section class="section-block"><div class="section-title">从这三篇开始</div>'
        f'<div class="entry-list">{picks}</div></section>'
        '<section class="card philosophy-card">'
        '<div class="section-title">为什么没有行情</div>'
        "<p>价格是别人愿意交易的价格，价值是生意自己创造的东西。"
        "本站关心后者：这家公司十年后还在不在、护城河是变宽还是变窄、现金流是不是真的。</p>"
        "<p>没有实时报价，不是缺功能，是刻意去掉的。看价格的时间越多，看生意的时间就越少。</p>"
        '<p class="philosophy-links"><a href="/knowledge/discipline/annual-line.html">年线法则</a>'
        '<a href="/thoughts/focus-domains.html">关注领域</a></p>'
        "</section>"
    )
    write("index.html", page(SITE["name"], SITE["description"], "研究库", body, "home", "/"))


def build_reports(reports: list[dict]) -> None:
    ordered = sorted(reports, key=lambda r: r["date"], reverse=True)
    chips = ['<button class="chip active" type="button" data-filter="all">全部</button>']
    for market in ("A股", "港股", "美股", "韩股", "ETF"):
        chips.append(f'<button class="chip" type="button" data-filter="market:{market}">{market}</button>')
    for decision in ("BUY", "WAIT", "PASS"):
        chips.append(
            f'<button class="chip" type="button" data-filter="decision:{decision}">{decision} · {DECISION_LABEL[decision]}</button>'
        )
    body = (
        '<div class="page-header"><div class="breadcrumb">研究库</div>'
        '<h1 class="page-title">公司报告</h1>'
        f'<p class="page-sub">共 {len(ordered)} 份。按日期倒序；同一家公司有多份报告时，旧报告保留为历史判断。</p></div>'
        f'<div class="chip-row">{"".join(chips)}</div>'
        f'<div class="report-list" id="reportList">{"".join(report_row(r) for r in ordered)}</div>'
    )
    write("reports/index.html", page(f"公司报告 · {SITE['name']}", "公司研究报告总览", "公司报告", body, "reports", "/reports/"))


def build_companies(reports: list[dict]) -> None:
    groups: dict[str, list[dict]] = {}
    for r in reports:
        groups.setdefault(r["company_slug"], []).append(r)
    rows = []
    for slug, items in sorted(groups.items(), key=lambda kv: max(i["date"] for i in kv[1]), reverse=True):
        items.sort(key=lambda r: r["date"], reverse=True)
        latest = items[0]
        rows.append(
            f'<a class="report-row" href="{latest["company_url"]}">'
            f'<div class="rr-main"><div class="rr-title">{html.escape(latest["company"])} '
            f'<span class="rr-ticker">{html.escape(latest["ticker"])}</span></div>'
            f'<div class="rr-summary">{len(items)} 份报告 · 最近 {latest["date"]} · {html.escape(latest["market"])}</div></div>'
            f'<div class="rr-meta">{badge(latest["decision"])}<span class="rr-date">{latest["date"]}</span></div>'
            f"</a>"
        )
        page_body = (
            f'<div class="page-header"><div class="breadcrumb"><a href="/companies/">公司索引</a></div>'
            f'<h1 class="page-title">{html.escape(latest["company"])}</h1>'
            f'<p class="page-sub">{html.escape(latest["ticker"])} · {html.escape(latest["market"])} · 共 {len(items)} 份报告</p></div>'
            f'<div class="report-list">{"".join(report_row(r) for r in items)}</div>'
        )
        write(
            f"companies/{slug}.html",
            page(f'{latest["company"]} · {SITE["name"]}', latest["summary"], "公司索引", page_body, "companies", latest["company_url"]),
        )
    body = (
        '<div class="page-header"><div class="breadcrumb">研究库</div>'
        '<h1 class="page-title">公司索引</h1>'
        f'<p class="page-sub">共 {len(groups)} 家公司。点进去看这家公司的全部报告。</p></div>'
        f'<div class="report-list">{"".join(rows)}</div>'
    )
    write("companies/index.html", page(f"公司索引 · {SITE['name']}", "已研究公司索引", "公司索引", body, "companies", "/companies/"))


def build_report_pages(reports: list[dict]) -> None:
    ordered = sorted(reports, key=lambda r: (r["date"], r["ticker"]))
    index = {id(r): i for i, r in enumerate(ordered)}
    for r in reports:
        content_html, toc = render_markdown(r["body"])
        toc_html = ""
        if len(toc) > 2:
            items = []
            for t in toc:
                cls = "toc-l3" if t["level"] == 3 else "toc-l2"
                items.append(f'<a class="{cls}" href="#{t["id"]}">{html.escape(t["text"])}</a>')
            toc_html = (
                f'<details class="card toc-card"><summary>目录（{len(toc)} 节）</summary>'
                f'<div class="toc-list">{"".join(items)}</div></details>'
            )
        i = index[id(r)]
        older = ordered[i - 1] if i > 0 else None
        newer = ordered[i + 1] if i + 1 < len(ordered) else None
        nav = ['<div class="prev-next">']
        if older:
            nav.append(f'<a href="{older["url"]}"><span>上一份</span>{html.escape(older["company"])} · {older["date"]}</a>')
        if newer:
            nav.append(f'<a class="pn-right" href="{newer["url"]}"><span>下一份</span>{html.escape(newer["company"])} · {newer["date"]}</a>')
        nav.append("</div>")
        body = (
            f'<div class="page-header">'
            f'<div class="breadcrumb"><a href="/reports/">公司报告</a> / '
            f'<a href="{r["company_url"]}">{html.escape(r["company"])}</a></div>'
            f'<h1 class="page-title">{html.escape(r["company"])} '
            f'<span class="page-ticker">{html.escape(r["ticker"])}</span></h1>'
            f'<div class="report-meta">{badge(r["decision"])}'
            f'<span>{r["date"]}</span><span>{html.escape(r["market"])}</span></div>'
            f'<div class="reader-tools">字号 '
            f'<button type="button" data-fs-set="s">A-</button>'
            f'<button type="button" data-fs-set="m">A</button>'
            f'<button type="button" data-fs-set="l">A+</button></div></div>'
            f"{toc_html}"
            f'<article class="card report-reader"><div class="md-content">{content_html}</div></article>'
            f"{''.join(nav)}"
        )
        write(
            r["url"].lstrip("/"),
            page(f'{r["company"]} {r["date"]} · {SITE["name"]}', r["summary"], "公司报告", body, "reports", r["url"]),
        )


def build_knowledge(knowledge: list[dict], groups: list[dict]) -> None:
    sections = []
    for group in groups:
        items = [d for d in knowledge if d["category"] == group["category"]]
        cards = "".join(entry_card(d["url"], d["title"], d["summary"], d["category_label"]) for d in items)
        sections.append(
            f'<section class="section-block"><div class="section-title">{html.escape(group["label"])}'
            f'<span class="section-count">{len(items)}</span></div>'
            f'<p class="section-desc">{html.escape(group["desc"])}</p>'
            f'<div class="entry-list">{cards}</div></section>'
        )
        cat_body = (
            f'<div class="page-header"><div class="breadcrumb"><a href="/knowledge/">知识库</a></div>'
            f'<h1 class="page-title">{html.escape(group["label"])}</h1>'
            f'<p class="page-sub">{html.escape(group["desc"])}</p></div>'
            f'<div class="entry-list">{cards}</div>'
        )
        write(
            f"knowledge/{group['category']}/index.html",
            page(f'{group["label"]} · {SITE["name"]}', group["desc"], "知识库", cat_body, "knowledge", f"/knowledge/{group['category']}/"),
        )
    body = (
        '<div class="page-header"><div class="breadcrumb">研究库</div>'
        '<h1 class="page-title">知识库</h1>'
        f'<p class="page-sub">共 {len(knowledge)} 篇。不是名言摘抄，是可以拿去约束自己动作的规则。</p></div>'
        f'{"".join(sections)}'
    )
    write("knowledge/index.html", page(f"知识库 · {SITE['name']}", "纪律、方法、原则、策略", "知识库", body, "knowledge", "/knowledge/"))


def build_thoughts(thoughts: list[dict]) -> None:
    cards = "".join(entry_card(d["url"], d["title"], d["summary"], "思想") for d in thoughts)
    body = (
        '<div class="page-header"><div class="breadcrumb">研究库</div>'
        '<h1 class="page-title">思想</h1>'
        '<p class="page-sub">整套系统背后的底层逻辑：怎么看世界，怎么定坐标，怎么取舍。</p></div>'
        f'<div class="entry-list">{cards}</div>'
    )
    write("thoughts/index.html", page(f"思想 · {SITE['name']}", "系统背后的底层逻辑", "思想", body, "thoughts", "/thoughts/"))


def build_discussions(discussions: list[dict]) -> None:
    ordered = sorted(discussions, key=lambda d: d.get("date", ""), reverse=True)
    rows = []
    for d in ordered:
        rows.append(
            f'<a class="entry-item" href="{d["url"]}">'
            f'<div class="entry-title">{html.escape(d["title"])}</div>'
            f'<div class="entry-preview">{html.escape(d["summary"])}</div>'
            f'<div class="entry-meta">{html.escape(d.get("date", ""))}</div></a>'
        )
    body = (
        '<div class="page-header"><div class="breadcrumb">研究库</div>'
        '<h1 class="page-title">讨论</h1>'
        f'<p class="page-sub">共 {len(ordered)} 篇。每条结论背后，必须站着一个没被安抚的反方。</p></div>'
        f'<div class="entry-list">{"".join(rows)}</div>'
    )
    write("discussions/index.html", page(f"讨论 · {SITE['name']}", "观点交锋档案", "讨论", body, "discussions", "/discussions/"))


def build_masters(masters: list[dict]) -> None:
    cards = []
    for m in masters:
        fm = m["meta"]
        sub = fm.get("representative") or fm.get("when_to_use") or ""
        cards.append(entry_card(m["url"], m["title"], m["summary"], sub))
    body = (
        '<div class="page-header"><div class="breadcrumb">研究库</div>'
        '<h1 class="page-title">投资家列传</h1>'
        f'<p class="page-sub">共 {len(masters)} 位。第三方风格提炼，只用于研究与教育，不代表本人观点。</p></div>'
        f'<div class="entry-list">{"".join(cards)}</div>'
    )
    write("masters/index.html", page(f"投资家列传 · {SITE['name']}", "49 位投资人的方法提炼", "投资家列传", body, "masters", "/masters/"))


def build_static_pages(reports: list[dict], knowledge: list[dict]) -> None:
    body = (
        '<div class="page-header"><div class="breadcrumb">研究库</div>'
        '<h1 class="page-title">关于本站</h1></div>'
        '<article class="card report-reader"><div class="md-content">'
        "<h2>这是什么</h2>"
        "<p>这是 FengInvest 的公开研究库：公司报告、知识库、思想、讨论档案、投资家列传。"
        "它只放研究，不放持仓、成本、仓位、组合和实时行情。</p>"
        "<h2>为什么没有行情</h2>"
        "<p>这套系统买的是公司，不是报价。价格只在两个时刻有用：决定要不要买，和决定要不要卖。"
        "其余时间，看价格只会干扰对生意的判断。</p>"
        "<h2>内容边界</h2>"
        "<ul><li>公司报告：每份都标注日期，旧报告保留为历史判断，不代表当前观点。</li>"
        "<li>知识库：纪律、方法、原则、策略，是约束动作的规则，不是名言。</li>"
        "<li>讨论：保留完整反方，结论可以被新证据推翻。</li>"
        "<li>投资家列传：第三方风格提炼，仅用于研究与教育。</li></ul>"
        "<h2>免责声明</h2>"
        f"<p>{html.escape(SITE['disclaimer'])}</p>"
        "<h2>技术</h2>"
        "<p>纯静态站点，零运行时依赖。没有后端、没有数据库、没有追踪脚本。"
        "内容由本地研究系统按白名单导出，逐篇脱敏后生成。</p>"
        "</div></article>"
    )
    write("about.html", page(f"关于 · {SITE['name']}", "关于本站与免责声明", "关于", body, "about", "/about.html"))

    body404 = (
        '<div class="page-header"><h1 class="page-title">404</h1></div>'
        '<div class="card"><p>这一页不存在。可以回<a href="/">首页</a>，或者去<a href="/reports/">报告库</a>看看。</p></div>'
    )
    write("404.html", page(f"404 · {SITE['name']}", "页面不存在", "404", body404, "", "/404.html"))

    search_body = (
        '<div class="page-header"><div class="breadcrumb">研究库</div>'
        '<h1 class="page-title">搜索</h1>'
        '<p class="page-sub">搜公司、代码、概念、报告标题。</p></div>'
        '<input id="searchInput" class="search-input" type="search" placeholder="例如：格力、护城河、年线、腾讯…" autocomplete="off">'
        '<div id="searchResults" class="search-results"><p class="search-hint">输入关键词开始搜索。</p></div>'
    )
    write("search.html", page(f"搜索 · {SITE['name']}", "站内搜索", "搜索", search_body, "search", "/search.html"))


def build_search_index(reports: list[dict], docs: list[dict]) -> None:
    entries = []
    for r in reports:
        entries.append(
            {
                "title": f'{r["company"]} {r["ticker"]} {r["date"]}',
                "url": r["url"],
                "cat": "公司报告",
                "excerpt": r["summary"],
                "text": " ".join([r["company"], r["ticker"], r["date"], r["market"], r["summary"]] + r["headings"]),
            }
        )
    for d in docs:
        entries.append(
            {
                "title": d["title"],
                "url": d["url"],
                "cat": d.get("category_label", d["category"]),
                "excerpt": d["summary"],
                "text": " ".join([d["title"], d["summary"]] + d["headings"]),
            }
        )
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":"))
    write("search-index.js", "window.FENG_SEARCH_INDEX = " + payload + ";\n")


def build_feed(reports: list[dict], discussions: list[dict]) -> None:
    items = []
    for r in sorted(reports, key=lambda x: x["date"], reverse=True)[:20]:
        items.append(
            {
                "title": f'{r["company"]} {r["date"]}',
                "url": SITE["base_url"] + r["url"],
                "date": r["date"],
                "desc": r["summary"],
            }
        )
    for d in sorted(discussions, key=lambda x: x.get("date", ""), reverse=True)[:10]:
        if d.get("date"):
            items.append(
                {
                    "title": d["title"],
                    "url": SITE["base_url"] + d["url"],
                    "date": d["date"],
                    "desc": d["summary"],
                }
            )
    items.sort(key=lambda x: x["date"], reverse=True)
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0"><channel>',
        f"<title>{xml_escape(SITE['name'])}</title>",
        f"<link>{xml_escape(SITE['base_url'])}</link>",
        f"<description>{xml_escape(SITE['description'])}</description>",
        f"<lastBuildDate>{now}</lastBuildDate>",
    ]
    for item in items:
        parts.append(
            "<item>"
            f"<title>{xml_escape(item['title'])}</title>"
            f"<link>{xml_escape(item['url'])}</link>"
            f"<guid>{xml_escape(item['url'])}</guid>"
            f"<description>{xml_escape(item['desc'])}</description>"
            f"<pubDate>{item['date']}T00:00:00+08:00</pubDate>"
            "</item>"
        )
    parts.append("</channel></rss>")
    write("feed.xml", "\n".join(parts))


def build_sitemap(urls: list[str]) -> None:
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        parts.append(f"<url><loc>{xml_escape(SITE['base_url'] + url)}</loc></url>")
    parts.append("</urlset>")
    write("sitemap.xml", "\n".join(parts))


def copy_assets() -> None:
    pairs = [
        (ASSETS_SRC / "css" / "tokens.css", DIST / "assets" / "css" / "tokens.css"),
        (ASSETS_SRC / "css" / "style.css", DIST / "assets" / "css" / "style.css"),
        (ASSETS_SRC / "img" / "logo.svg", DIST / "assets" / "img" / "logo.svg"),
        (ASSET_DIR / "site.css", DIST / "assets" / "site.css"),
        (ASSET_DIR / "reader.js", DIST / "assets" / "reader.js"),
    ]
    for src, dst in pairs:
        if not src.exists():
            raise SystemExit(f"[缺少资源] {src}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    headers = (
        "/*\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  X-Frame-Options: SAMEORIGIN\n"
    )
    (DIST / "_headers").write_text(headers, encoding="utf-8")


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

MANIFEST = json.loads((HERE / "publish_manifest.json").read_text(encoding="utf-8"))
SITE = MANIFEST["site"]


def main() -> None:
    reports = []
    for pattern in MANIFEST["reports"]["include"]:
        for path in sorted(ROOT.glob(pattern)):
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            if rel in MANIFEST["reports"].get("exclude", []):
                continue
            reports.append(load_report(path))

    knowledge = []
    groups = []
    for group in MANIFEST["knowledge"]:
        groups.append(group)
        for item in group["items"]:
            path = ROOT / item["path"]
            if not path.exists():
                raise SystemExit(f"[清单缺文件] {item['path']}")
            doc = load_markdown_doc(
                path,
                f"/knowledge/{group['category']}/{item['slug']}.html",
                group["category"],
                path.stem,
            )
            doc["category_label"] = group["label"]
            knowledge.append(doc)

    thoughts = []
    for item in MANIFEST["thoughts"]["items"]:
        path = ROOT / item["path"]
        if not path.exists():
            raise SystemExit(f"[清单缺文件] {item['path']}")
        doc = load_markdown_doc(path, f"/thoughts/{item['slug']}.html", "thoughts", item.get("title") or path.stem)
        doc["category_label"] = "思想"
        thoughts.append(doc)

    discussions = []
    for pattern in MANIFEST["discussions"]["include"]:
        for path in sorted(ROOT.glob(pattern)):
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            if rel in MANIFEST["discussions"].get("exclude", []):
                continue
            m = re.match(r"(\d{4}-\d{2}-\d{2})", path.stem)
            doc = load_markdown_doc(path, f"/discussions/{ascii_slug(path.stem)}.html", "discussions", path.stem)
            doc["date"] = m.group(1) if m else ""
            doc["category_label"] = "讨论"
            discussions.append(doc)

    masters = []
    for pattern in MANIFEST["masters"]["include"]:
        for path in sorted(ROOT.glob(pattern)):
            doc = load_markdown_doc(path, f"/masters/{ascii_slug(path.stem)}.html", "masters", path.stem)
            doc["category_label"] = "投资家列传"
            masters.append(doc)
    masters.sort(key=lambda d: d["meta"].get("name", d["title"]))

    LINK_MAP.clear()
    for doc in knowledge + thoughts + discussions + masters:
        LINK_MAP[Path(doc["path"]).name] = doc["url"]

    # 一致性检查
    if not reports:
        raise SystemExit("[空内容] 没有匹配到任何报告")
    for r in reports:
        if not r["date"]:
            raise SystemExit(f"[报告缺日期] {r['path']}")

    print(f"清单装载：报告 {len(reports)} · 知识 {len(knowledge)} · 思想 {len(thoughts)} · 讨论 {len(discussions)} · 列传 {len(masters)}")

    if CHECK_ONLY:
        print("检查通过（未写文件）。")
        return

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True, exist_ok=True)

    build_home(reports, knowledge, thoughts, discussions, masters)
    build_reports(reports)
    build_companies(reports)
    build_report_pages(reports)
    build_knowledge(knowledge, groups)
    build_thoughts(thoughts)
    build_discussions(discussions)
    build_masters(masters)
    for doc in knowledge + thoughts + discussions + masters:
        section = {
            "discipline": "知识库",
            "methodology": "知识库",
            "principles": "知识库",
            "strategy": "知识库",
            "thoughts": "思想",
            "discussions": "讨论",
            "masters": "投资家列传",
        }[doc["category"]]
        active = {"discipline": "knowledge", "methodology": "knowledge", "principles": "knowledge", "strategy": "knowledge",
                  "thoughts": "thoughts", "discussions": "discussions", "masters": "masters"}[doc["category"]]
        if doc["category"] == "discipline":
            crumb = f'<a href="/knowledge/">知识库</a> / <a href="/knowledge/discipline/">纪律</a>'
        elif doc["category"] == "methodology":
            crumb = f'<a href="/knowledge/">知识库</a> / <a href="/knowledge/methodology/">方法</a>'
        elif doc["category"] == "principles":
            crumb = f'<a href="/knowledge/">知识库</a> / <a href="/knowledge/principles/">原则</a>'
        elif doc["category"] == "strategy":
            crumb = f'<a href="/knowledge/">知识库</a> / <a href="/knowledge/strategy/">策略</a>'
        elif doc["category"] == "thoughts":
            crumb = '<a href="/thoughts/">思想</a>'
        elif doc["category"] == "discussions":
            crumb = '<a href="/discussions/">讨论</a>'
        else:
            crumb = '<a href="/masters/">投资家列传</a>'
        write(doc["url"].lstrip("/"), render_doc_page(doc, section, active, crumb))

    build_static_pages(reports, knowledge)
    build_search_index(reports, knowledge + thoughts + discussions + masters)
    build_feed(reports, discussions)

    urls = ["/", "/reports/", "/companies/", "/knowledge/", "/thoughts/", "/discussions/", "/masters/", "/search.html", "/about.html"]
    urls += [r["url"] for r in reports]
    urls += [d["company_url"] for d in reports]
    urls += [d["url"] for d in knowledge + thoughts + discussions + masters]
    build_sitemap(sorted(set(urls)))

    copy_assets()

    total = sum(1 for _ in DIST.rglob("*") if _.is_file())
    size = sum(p.stat().st_size for p in DIST.rglob("*") if p.is_file())
    print(f"生成完成：{total} 个文件，{size / 1024:.1f} KB → {DIST}")
    print("预览：python -m http.server 8002 --directory dist")


if __name__ == "__main__":
    main()
