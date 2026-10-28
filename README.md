# invest_fyw_com — 公开研究站

一个纯静态的公开研究站，内容只有五类：

- 公司报告（七层分析产出的 `07-report.md`）
- 知识库（纪律 / 方法 / 原则 / 策略）
- 思想（奇衡思想总纲、关注领域）
- 讨论（完整保留反方的讨论档案）
- 投资家列传（49 位投资人的方法提炼）

没有行情看板，没有持仓，没有成本，没有实时报价。这不是缺功能，是站点的立场：**买公司，不看报价**。

---

## 零依赖

- **构建**：只需要 Python 3.9+，全部用标准库（`html` / `json` / `re` / `pathlib` / `hashlib` / `xml.sax.saxutils` / `datetime`）。没有 npm、Node、Express、EJS、marked、sanitize-html，也没有任何 pip 包。
- **运行**：产物就是 `dist/` 里的 HTML/CSS/JS，没有后端、没有数据库、没有追踪脚本。托管在任何静态服务器上都能跑。

```bash
python build.py --check     # 只做白名单装载 + 泄漏扫描，不写文件
python build.py             # 生成 dist/
python -m http.server 8002 --directory dist
# 打开 http://127.0.0.1:8002/
```

`build.py --check` 是发布前的闸门：任何一篇内容命中泄漏规则都会 `exit 1`，不会带着问题生成。

---

## 目录

```
invest_fyw_com/
├── build.py                 # 零依赖静态生成器（唯一构建入口）
├── sync_content.py          # 从 FengInvest 私有仓按白名单同步 content/
├── publish_manifest.json    # 发布白名单（默认拒绝）
├── templates/base.html      # 公共页面骨架
├── content/                 # 唯一的内容来源（构建时只读这里）
│   ├── 060-companies/       # 公司报告
│   ├── knowledge/           # 知识库 + 思想
│   ├── Discussion/          # 讨论档案
│   └── 040-people/named/    # 投资家列传
├── assets/
│   ├── css/tokens.css       # 设计令牌（来自 fengweb）
│   ├── css/style.css        # 基础样式（来自 fengweb）
│   ├── img/logo.svg         # 站点 logo
│   ├── site.css             # 本项目的增量样式
│   └── reader.js            # 原生 JS：目录 / 主题 / 字号 / 进度 / 搜索 / 筛选
└── dist/                    # 构建产物（gitignored，部署时上传）
```

复用的 UI：`tokens.css`、`style.css` 与 logo 已随仓库固化，视觉语言与主 Web UI 保持一致；`site.css` 只加公共站独有的版块和阅读器控件。手机端、暗色模式、打印样式都在同一套令牌上工作。**构建不再依赖 fengweb 仓**。

---

## 内容从哪来

内容源在私有的 FengInvest 仓。本仓只存**已经允许公开**的副本，因此可以独立构建、独立发布。

```bash
python sync_content.py --source C:/FengProj/FengInvest          # 同步
python sync_content.py --source C:/FengProj/FengInvest --check  # 只看会更新哪些
python build.py
```

同步脚本只认 `publish_manifest.json` 里的白名单：清单之外的文件不会出现在 `content/`，更不会被发布。

---

## 发布规则：白名单，默认拒绝

`publish_manifest.json` 是唯一的发布范围定义。**没有写进清单的内容不会被发布**，即使它躺在 `content/` 里。

当前口径：

| 栏目 | 来源（`content/` 内） |
|:--|:--|
| 公司报告 | `060-companies/*/*/07-report.md` |
| 知识库 | `knowledge/` 下逐篇登记（纪律 7 / 方法 6 / 原则 4 / 策略 5） |
| 思想 | `knowledge/` 下两篇长文（内部合规清单《基准参考》不对外） |
| 讨论 | `Discussion/*.md`（排除 README） |
| 投资家列传 | `040-people/named/*.md` |
| 个人知识 | **空清单**——见下方隐私边界 |

新增一篇知识文档：先在私有仓写好，再在 `publish_manifest.json` 里给它一个英文 slug，然后跑同步 + 构建。
新增一份公司报告：在私有仓按 `research/060-companies/<TICKER>-<名称>/<日期>/07-report.md` 落盘，同步即可；本仓不需要改清单。

---

## 脱敏与泄漏闸门

`build.py` 在生成前会对每篇内容做清洗，并在写盘前做硬扫描。命中下列任一项直接失败：

- 持仓文件名 / 持仓目录 / 个人知识目录 / 《投资血泪史》
- 决策日志、组合文件、状态文件、绝对路径
- API Key、Bearer Token、邮箱地址

同时会替换：

- 内部路径 → `内部数据`（例如 `tools/fengcollision.py`、`sources/xxx.json`）
- 报告里的仓位与建仓比例 → `已隐去`（含表格里的 `position_pct` 整列）
- 标题里的 `@ 0%`、尾部的 `目标价：…` → 删除

知识库、思想、讨论、列传里的通用仓位管理知识（如大师的单笔 3% 规则）会保留；只有「我的仓位 / 当前仓位 / 持仓比例」这类个人持仓表述才抹掉。

这份站点**不发布**：持仓、成本、组合、交易记录、行情、个人血泪史。个人知识默认也不发布；将来若要发某篇个人笔记，逐篇加进 `personal.include`，不要放开目录。

---

## 搜索 / RSS / 部署

- 搜索索引在构建时生成 `dist/search-index.js`（`window.FENG_SEARCH_INDEX = [...]`），搜索页按需加载，不依赖后端和 fetch。
- 同时生成 `feed.xml`、`sitemap.xml`、`_headers` 和 `404.html`。
- 部署：把 `dist/` 原样上传到任意静态托管（Cloudflare Pages / GitHub Pages / Nginx / 对象存储）。
- 线上目标：Cloudflare Pages 项目 `invest-fyw-com`，域名 `invest.fengyuwang.com`。两种接法见 [DEPLOY.md](DEPLOY.md)。

---

## 仓库名

GitHub 允许仓库名包含字母、数字、连字符、下划线和点，所以 `invest_fyw_com` 可以直接用；如果更想要 URL 友好的形式，`invest-fyw-com` 等价。

---

## 边界

- 本站是个人研究记录，仅供学习与讨论，不构成任何投资建议。
- 报告里出现的历史价格、估值、目标价，都是撰写时点的分析材料，不是实时行情。
- 页面上的“上一份 / 下一份”按报告日期排序；同一家公司有多份报告时，旧报告保留为历史判断，不覆盖。
