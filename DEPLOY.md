# 部署到 Cloudflare Pages

目标：`https://invest.fengyuwang.com`，静态只读，无后端、无数据库、无运行时。

站内产物是纯静态文件，Cloudflare Pages 只是托管它。两条路，选一条。

---

## 方式 A：GitHub 自动构建（推荐，一次配好不再管）

仓库：<https://github.com/fengyuwang-com/invest_fyw_com>（public，`main`）

1. Cloudflare Dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**。
2. 选 `invest_fyw_com`。
3. 构建设置：
   - Framework preset：`None`
   - Build command：`python build.py`
   - Build output directory：`dist`
   - 环境变量：不需要
4. Save and Deploy。首次构建约 1 分钟。
5. 项目 → **Custom domains** → `invest.fengyuwang.com` → Activate。
   因为 `fengyuwang.com` 的 zone 就在 Cloudflare，CNAME 与 TLS 证书会自动建好，不用手改 DNS。
6. 之后每次 push `main` 自动重新构建发布。

Pages 构建镜像自带 Python 3.11，`build.py` 只用标准库，不需要 `requirements.txt`。

---

## 方式 B：本机直接上传（已有 Cloudflare 登录态时最快）

```bash
cd C:/Projects/invest_fyw_com
python build.py
npx wrangler pages deploy dist --project-name invest-fyw-com
```

首次执行前需要在本机登录一次 Cloudflare（浏览器点一次 Allow）：

```bash
npx wrangler login
npx wrangler whoami      # 确认账号与权限
```

自定义域同样在 Dashboard → 项目 → Custom domains 里加。用命令行加域需要一个带 `zone:edit` 权限的 API Token，OAuth 登录的默认权限不含这一项，所以域名这一步走 Dashboard 更省事。

---

## 验证清单

发布后逐项确认：

- `https://invest.fengyuwang.com/` 返回首页，`/assets/reader.js?v=...` 返回 200
- 点左上角 ☰ 侧栏能展开，✕ / Esc / 点内容区能收起
- `/search.html` 搜一个词有结果
- `/feed.xml`、`/sitemap.xml` 能打开
- 随便开一份报告，页面里不出现任何仓位数字（`仓位…%` / `position_pct`）
- `http://` 自动跳 `https://`，证书有效

## 缓存

资源 URL 带内容指纹（`?v=<css+js 哈希>`），改样式或脚本后旧缓存自动失效；HTML 每次重新验证。`_headers` 已由构建生成，附带 `nosniff` / `Referrer-Policy` / `X-Frame-Options`。
