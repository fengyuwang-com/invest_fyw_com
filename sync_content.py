#!/usr/bin/env python3
"""从 FengInvest 私有仓按发布白名单同步 content/。

只读源仓、只写本项目 content/。清单之外的文件一律不碰。

用法：
    python sync_content.py --source C:/FengProj/FengInvest
    python sync_content.py --source ../FengInvest --check   # 只看会复制什么
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTENT = HERE / "content"
MANIFEST = json.loads((HERE / "publish_manifest.json").read_text(encoding="utf-8"))


def source_rel(rel: str) -> str:
    """清单里的路径（content/ 前缀）→ 源仓相对路径。"""
    rel = rel.replace("\\", "/")
    for public, private in (("content/060-companies/", "research/060-companies/"),
                            ("content/040-people/", "research/040-people/")):
        if rel.startswith(public):
            return private + rel[len(public):]
    return rel[len("content/"):] if rel.startswith("content/") else rel


def map_target(rel: str) -> str:
    """源仓相对路径 → content/ 下的相对路径。"""
    rel = rel.replace("\\", "/")
    for prefix in ("research/060-companies/", "research/040-people/"):
        if rel.startswith(prefix):
            return "content/" + rel[len("research/"):]
    return "content/" + rel


def collect_files(source: Path) -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []

    def add(rel: str) -> None:
        src_rel = source_rel(rel)
        src = source / src_rel
        if not src.exists():
            print(f"[缺文件] {src_rel}", file=sys.stderr)
            return
        pairs.append((src, HERE / map_target(src_rel)))

    for pattern in MANIFEST["reports"]["include"]:
        for path in sorted(source.glob(source_rel(pattern))):
            rel = str(path.relative_to(source)).replace("\\", "/")
            if map_target(rel) in MANIFEST["reports"].get("exclude", []):
                continue
            add(rel)

    for group in MANIFEST["knowledge"]:
        for item in group["items"]:
            add(item["path"])

    for item in MANIFEST["thoughts"]["items"]:
        add(item["path"])

    for pattern in MANIFEST["discussions"]["include"]:
        for path in sorted(source.glob(source_rel(pattern))):
            rel = str(path.relative_to(source)).replace("\\", "/")
            if map_target(rel) in MANIFEST["discussions"].get("exclude", []):
                continue
            add(rel)

    for pattern in MANIFEST["masters"]["include"]:
        for path in sorted(source.glob(source_rel(pattern))):
            add(str(path.relative_to(source)).replace("\\", "/"))

    return pairs


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=str(Path("C:/FengProj/FengInvest")), help="FengInvest 仓根目录")
    ap.add_argument("--check", action="store_true", help="只报告变更，不写文件")
    args = ap.parse_args()

    source = Path(args.source)
    if not (source / "knowledge").is_dir():
        raise SystemExit(f"[源仓不对] {source} 下找不到 knowledge/")

    pairs = collect_files(source)
    changed, same = [], 0
    for src, dst in pairs:
        if dst.exists() and digest(src) == digest(dst):
            same += 1
            continue
        changed.append((src, dst))

    print(f"清单内文件 {len(pairs)} · 无变化 {same} · 需更新 {len(changed)}")
    for src, dst in changed:
        print("  ", dst.relative_to(HERE))

    if args.check:
        return

    for src, dst in changed:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    print("同步完成。下一步：python build.py --check && python build.py")


if __name__ == "__main__":
    main()
