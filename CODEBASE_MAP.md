# 代码库地图

给人和 AI 助手看的项目结构说明。动手改东西之前先读这一页，能少走很多弯路。

最后核对：2026-10-01。结构变化后请同步更新本页。

## 一句话概括

这是一个用 Markdown 写的个人命令速查表。用 MkDocs（把 Markdown 转成网站的工具）加 Material 主题生成网页，由 GitHub Actions 自动发布到 GitHub Pages。线上地址：<https://cucu11039004-web.github.io/cmd-repo/>。

没有后端、没有数据库、没有业务代码。内容就是 `docs/` 里的 Markdown，其余文件都在服务于“把它变成网站”。

## 目录结构

```text
my-cmd-repo/
├── CODEBASE_MAP.md            本页（放在根目录，不会被构建成网页）
├── docs/                      内容层：所有笔记，纯 Markdown
│   ├── index.md               首页：场景导航表、条目格式、AI 整理提示词
│   ├── inbox.md               收集箱：note 命令的写入目标
│   ├── linux-files.md         Linux 文件操作
│   ├── linux-process-network.md   Linux 进程与网络
│   ├── git.md                 Git
│   ├── docker.md              Docker
│   └── python-env.md          Python 环境
├── mkdocs.yml                 构建配置：站点名、主题、功能开关、左侧菜单
├── requirements.txt           固定版本的 Python 依赖（本地和线上共用）
├── scripts/notes.sh           终端函数 note、notepush
├── .github/workflows/deploy.yml   线上自动发布流程
├── README.md                  使用说明和阶段验收记录
├── cheatsheet-plan.md         最初的搭建计划书（已确认的决策来源）
├── .gitignore                 忽略 .venv/、site/ 等
├── .venv/                     本机虚拟环境（不提交）
└── site/                      本地构建产物（不提交）
```

## 各部分职责

| 部分 | 职责 | 什么时候会改它 |
| --- | --- | --- |
| `docs/*.md` | 存放内容，是唯一的数据源 | 日常记笔记、每周整理 |
| `mkdocs.yml` | 决定网站外观、功能和菜单 | 新增分类页、换功能、绑定域名 |
| `requirements.txt` | 决定装哪些依赖及版本 | 升级 MkDocs 或主题 |
| `scripts/notes.sh` | 提供 `note`（一行记录）和 `notepush`（检查后推送） | 调整记录或推送流程 |
| `deploy.yml` | 推送到 `main` 后，在线上构建并发布 | 调整构建环境或发布方式 |

## 发布流程

```text
note '...'        往 docs/inbox.md 追加一行（只写本地，不联网）
   │
notepush          检查 → 试构建 → 只提交 docs/ → 推送 main
   │
GitHub Actions    deploy.yml：装依赖，mkdocs gh-deploy 把网页推到 gh-pages 分支
   │
GitHub Pages      内置的 pages build and deployment 发布 gh-pages
   │
网站更新          搜索索引同步更新
```

要点：

- 脚本只负责到 `git push`。后两步由 GitHub 接力，整体约一分钟。
- `notepush` 的检查顺序：必须在 `main` 分支；必须有 `origin`；暂存区不能有 `docs/` 以外的文件；`mkdocs build --strict` 能通过；然后才提交推送。
- `notepush` 用 `git add -A -- docs`，会提交 `docs/` 里的**全部**改动，包括没写完的笔记。
- `gh-pages` 是生成物，由流程强制覆盖，不要手动改。`main` 禁止强制推送。

## 文件之间的依赖关系

- `note` 写入 `docs/inbox.md`；`notepush` 读取 `mkdocs.yml` 做试构建，路径写死为 `.venv/bin/python`，所以必须先建好虚拟环境。
- `mkdocs.yml` 的 `nav` 列出的每个文件名必须真实存在于 `docs/`。
- `mkdocs.yml` 里的 `theme.name: material` 依赖 `requirements.txt` 中的 `mkdocs-material`。
- `deploy.yml` 用 `requirements.txt` 装依赖，再读取 `mkdocs.yml` 和 `docs/` 构建。
- `site_url` 目前是 GitHub 默认地址；第二阶段绑定自定义域名时要改这一行。

## 约定

**笔记条目格式**（每条固定五项，“遇到场景”最重要）：

````markdown
### 标题

```bash
命令
```

- 作用：……
- 遇到场景：……
- 来源：……
````

**其他规则**：

- 说明文字用中文，命令保持英文原样。
- 文档内部链接只用相对路径。
- 仓库是公开的：不记录密钥、Token、内网地址和私有项目细节。`note` 不会自动检查这些。
- 来源只写真实出现过且可公开的内容，不确定就先问，不要编造。

## 常见任务怎么做

**新增一个分类页**

1. 在 `docs/` 新建 `xxx.md`，按条目格式写内容。
2. 在 `mkdocs.yml` 的 `nav` 里加一行 `- 显示名称: xxx.md`。
3. 在 [首页](docs/index.md) 的“从场景开始查”表里加一行入口。
4. 运行 `.venv/bin/python -m mkdocs build --strict` 确认能通过。

只做第 1 步页面也会被生成，但菜单里没有入口。**这种情况 `--strict` 不会报错**，只在日志里给一条 INFO，所以第 2 步容易漏。

**整理收集箱**：把 [收集箱](docs/inbox.md) 的记录补全成标准条目，移到对应分类页，再删除已归档的条目，保留收集箱的标题和说明。

**本地预览**：激活 `.venv` 后运行 `python -m mkdocs serve`，打开输出里的本地地址。

**只检查能否构建**：`.venv/bin/python -m mkdocs build --strict`。

## 给 AI 助手的注意事项

- 内容改动只动 `docs/`；配置、脚本、工作流的改动要单独处理，不要和笔记混在同一次提交里。
- 不要重命名或删除 `docs/` 下的文件而不同步修改 `mkdocs.yml` 的 `nav` 和首页入口表。
- 不要对 `main` 强制推送；不要手动改 `gh-pages`。
- 不要提交 `site/` 和 `.venv/`。
- 没有现成测试。验证改动的方式是 `mkdocs build --strict`，必要时用 `mkdocs serve` 看页面。
- 不要擅自创建 `docs/CNAME`，自定义域名属于第二阶段，要等用户确认 DNS 服务商。
- 新增条目前先检查是否已存在，避免重复；跳过琐碎的一次性命令。

## 已知情况

- 线上构建用 Python 3.13，本机 `.venv` 是 Python 3.9.6。目前两边都能构建成功，但并不能保证完全一致。
- 构建时终端会出现一大段红色提示，是 Material 主题对 MkDocs 2.0 的兼容性警告，不是配置错误。
- 本页放在仓库根目录而不是 `docs/`：`docs/` 里的文件都会变成公开网页，并被 `notepush` 一起提交。根目录的文件不会，所以结构说明、给 AI 的约定适合放在这里。
