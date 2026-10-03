# 代码库地图

给人和 AI 助手看的项目结构说明。动手改东西之前先读这一页，能少走很多弯路。

最后核对：2026-10-03。结构变化后请同步更新本页。

## 一句话概括

这是一个用 Markdown 写的个人命令速查表。用 MkDocs（把 Markdown 转成网站的工具）加 Material 主题生成网页，由 GitHub Actions 自动发布到 GitHub Pages。线上地址：<https://cucu11039004-web.github.io/cmd-repo/>。

没有后端、没有数据库。内容保存在 `docs/` 的 Markdown 中。首页显示哪些命令由 `docs/pins.yml` 决定：本地预览时在网页上点选写入，构建钩子按它生成首页。收集箱的记录也可以在本地预览的网页上归档到分类。其余文件服务于“把它变成网站”。

## 目录结构

```text
my-cmd-repo/
├── CODEBASE_MAP.md            本页（放在根目录，不会被构建成网页）
├── docs/                      内容层：所有笔记，纯 Markdown
│   ├── index.md               首页：标题与自动生成占位符
│   ├── inbox.md               收集箱：note 的写入目标，本地预览时可在网页上归档
│   ├── pins.yml               首页命令清单：条目锚点 + 加入时间
│   ├── editing/               编辑与写作：emacs、vim、vscode、markdown、regex
│   ├── linux/                 Linux 与服务器：shell、files、text、process、system、
│   │                          network、remote、tmux、gpu、docker
│   ├── python/                Python 与 AI：env、basics、numpy、data、pytorch、llm
│   ├── robotics/              机器人：serial、can、ros2、grpc、devices
│   ├── javascripts/pins.js    本地预览的点选与归档界面；首页复制按钮
│   └── stylesheets/home.css   首页四列命令板、分类页 ☆/★、收集箱归档卡片样式
├── mkdocs.yml                 构建配置：站点名、主题、功能开关、导航
├── requirements.txt           固定版本的 Python 依赖（本地和线上共用）
├── scripts/notes.sh           终端函数 note、notepush、cmdserve
├── scripts/common_commands.py MkDocs 构建钩子：校验条目、生成首页、本地点选与归档接口
├── .github/workflows/deploy.yml   线上自动发布流程
├── README.md                  使用说明、条目模板、AI 整理提示词和阶段验收记录
├── cheatsheet-plan.md         最初的搭建计划书（历史记录；现行结构以本页为准）
├── .gitignore                 忽略 .venv/、site/ 等
├── .venv/                     本机虚拟环境（不提交）
└── site/                      本地构建产物（不提交）
```

## 各部分职责

| 部分 | 职责 | 什么时候会改它 |
| --- | --- | --- |
| `docs/<大类>/*.md` | 存放命令条目，是唯一的内容来源 | 日常记笔记、每周整理 |
| `docs/pins.yml` | 记录首页显示哪些条目、何时加入 | 本地预览点选时自动改写，也可手动编辑 |
| `mkdocs.yml` | 决定网站外观、功能和导航 | 新增子页或大类、换功能、绑定域名 |
| `requirements.txt` | 决定装哪些依赖及版本 | 升级 MkDocs 或主题 |
| `scripts/notes.sh` | 提供 `note`（一行记录）、`notepush`（检查后推送）、`cmdserve`（本地预览） | 调整记录、预览或推送流程 |
| `scripts/common_commands.py` | 校验全部条目，按 `pins.yml` 生成首页，标记分类页已选条目，本地预览时提供点选和收集箱归档接口 | 调整首页、校验规则或本地接口 |
| `docs/javascripts/pins.js` | 本地预览时显示 ☆、✕ 和收集箱归档表单并调用接口；首页复制按钮 | 调整点选或归档交互 |
| `deploy.yml` | 推送到 `main` 后，在线上构建并发布 | 调整构建环境或发布方式 |

## 发布流程

```text
note '...'        往 docs/inbox.md 追加一行（只写本地，不联网）
   │
cmdserve          本地预览：在收集箱页只选分类即可归档，可批量（默认同时加入首页）；
                  在分类页点 ☆ 加入首页、在首页点 ✕ 移出，写入 docs/pins.yml
   │
notepush          检查 → 试构建 → 只提交 docs/（含 pins.yml）→ 推送 main
   │
GitHub Actions    deploy.yml：装依赖，构建时按 pins.yml 生成首页，gh-deploy 推到 gh-pages 分支
   │
GitHub Pages      内置的 pages build and deployment 发布 gh-pages
   │
网站更新          首页与本地一致；线上只读，不显示 ☆ 和 ✕
```

要点：

- 脚本只负责到 `git push`。后两步由 GitHub 接力，整体约一分钟。
- `notepush` 的检查顺序：必须在 `main` 分支；必须有 `origin`；暂存区不能有 `docs/` 以外的文件；`mkdocs build --strict` 能通过；然后才提交推送。
- `notepush` 用 `git add -A -- docs`，会提交 `docs/` 里的**全部**改动，包括没写完的笔记和 `pins.yml`。
- `gh-pages` 是生成物，由流程强制覆盖，不要手动改。`main` 禁止强制推送。

## 本地点选与归档的工作方式

- 线上网站是静态文件，没有地方保存点击，所以只读。
- `mkdocs serve` 时，构建钩子的 `on_serve` 包装预览服务器，接管路径以 `/__pins__`、`/__inbox__` 结尾的请求，其余交给 MkDocs。MkDocs 发现 `docs/` 变化后自动重建并刷新页面。
- `/__pins__`：`GET` 用于探测，`POST {"id", "pinned"}` 改写 `docs/pins.yml`。
- `/__inbox__`：`GET` 返回收集箱记录（按「命令；作用；来源」预拆分，带 `作用：`、`场景：`、`来源：` 前缀的段落按前缀归位）、各子页的二级小节、已用锚点，以及已有命令（用于提醒重复）。
- `POST {"action": "file", "items": [...]}` 一次归档一条或多条：全部检查通过才写入，任何一条有问题都不改文件。每条只有分类（子页）必填；作用作为标题；锚点留空时由 `make_anchor` 按命令生成（取前 4 个英文单词，键位类页面加页面名前缀，重复时加 `-2`）；小节留空时放进页面末尾的「未分小节」（没有就新建）。`{"action": "delete", "raw": ...}` 只删除记录。记录按整行文本定位，找不到时返回错误。
- 归档时依次写分类页、`pins.yml`、`inbox.md`，每一步之后的中间状态都能正常构建。来源、场景只在填写时写入条目。代码语言默认：编辑与写作用 `text`，Python 与 AI（环境页除外）用 `python`，其余用 `bash`。
- 接口只接受 `Content-Type: application/json`，且 `Origin` 必须与 `Host` 一致；预览服务器默认只监听本机。
- `pins.js` 只在 `localhost`、`127.0.0.1` 下探测接口，探测成功才显示 ☆、✕ 和收集箱归档表单。
- 首页每个大类一列，列内按 `added` 倒序，同一时间按文件顺序；新加入的条目写在文件最前面。
- 写入时会顺便清除指向已删除条目的记录。构建时 `pins.yml` 里有找不到的锚点会报错。

## 文件之间的依赖关系

- `note` 写入 `docs/inbox.md`；`notepush`、`cmdserve` 的路径写死为 `.venv/bin/python`，所以必须先建好虚拟环境。
- `mkdocs.yml` 的 `nav` 列出的每个文件名必须真实存在于 `docs/`。顶部标签（`navigation.tabs`）对应大类，左侧栏列出该类子页。
- 当前导航顺序为：首页 → 编辑与写作 → Linux 与服务器 → Python 与 AI → 机器人 → 收集箱。子页内的小类用二级标题组织。
- `mkdocs.yml` 的 `hooks` 加载 `scripts/common_commands.py`；首页的 `<!-- common-commands -->` 必须恰好出现一次。
- 构建钩子按导航顺序读取全部分类页（首页、收集箱除外），校验每个三级标题条目；再读取 `docs/pins.yml`，生成首页列表。源 Markdown 不会被构建改写。
- 首页按大类分四列，每条只显示小类标签和命令，不显示标题，方便自测记忆。点命令跳到分类页锚点，右侧图标复制；标题、作用、场景和来源只显示在分类页。
- 首页隐藏左侧导航和右侧目录，并通过 `search.exclude` 排除在搜索之外，避免与分类页重复。
- `extra_css` 加载 `docs/stylesheets/home.css`，`extra_javascript` 加载 `docs/javascripts/pins.js`。
- `attr_list` 提供标题固定锚点；锚点同时是 `pins.yml` 里的 ID。
- `pins.yml` 由 PyYAML 读写，PyYAML 是 MkDocs 的依赖，已在 `requirements.txt` 中。
- `mkdocs.yml` 里的 `theme.name: material` 依赖 `requirements.txt` 中的 `mkdocs-material`。
- `deploy.yml` 用 `requirements.txt` 装依赖，再读取 `mkdocs.yml` 和 `docs/` 构建。
- `site_url` 目前是 GitHub 默认地址；第二阶段绑定自定义域名时要改这一行。

## 约定

**笔记条目格式**（标题写作用；作用、遇到场景、来源三行都可选）：

````markdown
### 作用 { #tool-action }

```bash
命令
```

- 作用：需要比标题更长的解释时再写
- 遇到场景：……
- 来源：单词出处或助记（如 ls ← list），或学习出处、官方文档
````

- **每个三级标题都是条目**，必须有固定锚点和完整非空的代码块，否则构建报错。
- **锚点全站唯一**：以小写英文字母开头，只含小写英文字母、数字和连字符。新锚点以工具或主题作前缀，如 `emacs-next-line`、`tmux-detach`、`torch-no-grad`。修改中文标题时保留锚点；改锚点前先确认它不在 `pins.yml` 中。
- **时间顺序**：新条目追加到所属二级小节的末尾，文件顺序就是添加顺序。归档时没选小节的条目在页面末尾的「未分小节」里。
- **键位类条目**：代码块语言用 `text`。Emacs 写法为 `C-x C-s`（C 为 Control，M 为 Meta），Vim 普通模式直接写按键，VS Code 写法为 `Cmd+Shift+P`。
- 首页由 `pins.yml` 决定，不再使用 `<!-- common -->` 标记；遗留标记会导致构建报错。
- 收集箱每条记录是一行 `- 日期 内容`，内容按「命令；作用；来源」分隔，来源可省略。优先按中文分号拆分，整条没有中文分号时才按英文分号拆分。

**其他规则**：

- 说明文字用中文，命令保持英文原样。
- 文档内部链接只用相对路径。
- 仓库是公开的：不记录密钥、Token、内网地址和私有项目细节。`note` 不会自动检查这些。
- 来源只写真实出现过且可公开的内容（单词出处、助记、学习出处或官方文档），不确定就先问，不要编造。

## 常见任务怎么做

**新增一个子页**

1. 在对应大类目录新建 `docs/<大类>/xxx.md`，写页面说明和二级小节。
2. 在 `mkdocs.yml` 的 `nav` 对应大类下加一行 `- 显示名称: <大类>/xxx.md`。
3. 同步更新本页的目录说明。
4. 运行 `.venv/bin/python -m mkdocs build --strict` 确认能通过。

只做第 1 步页面也会被生成，但菜单里没有入口。**这种情况 `--strict` 不会报错**，只在日志里给一条 INFO，所以第 2 步容易漏。

**新增一个大类**：新建 `docs/<目录>/`，在 `nav` 加一个带子页列表的分组，其余同上。首页标签配色按大类在导航中的顺序循环使用四种颜色。

**整理收集箱**：本地预览时在收集箱页给每条选分类（小节可选），逐条点「归档」或点「全部归档」。也可以手动或请 AI 整理：把记录补全成标准条目，追加到对应分类小节的末尾，再删除已归档的条目，保留收集箱的标题和说明。

**本地预览与点选**：`source scripts/notes.sh` 后运行 `cmdserve`（等同于在仓库根目录运行 `.venv/bin/python -m mkdocs serve --open`）。在分类页点条目标题旁的 ☆ 加入首页，在首页点 ✕ 移出。

**只检查能否构建**：`.venv/bin/python -m mkdocs build --strict`。

修改分类 Markdown 或 `pins.yml` 后预览自动刷新；修改构建钩子后要重启 `mkdocs serve`，并用 `.venv/bin/python -m mkdocs build --strict` 检查。

## 给 AI 助手的注意事项

- 内容改动只动 `docs/`；配置、脚本、工作流的改动要单独处理，不要和笔记混在同一次提交里。
- 不要重命名或删除 `docs/` 下的文件而不同步修改 `mkdocs.yml` 的 `nav` 和文档内部链接。
- 删除或改名条目锚点时，同步检查 `docs/pins.yml`。
- 不要对 `main` 强制推送；不要手动改 `gh-pages`。
- 不要提交 `site/` 和 `.venv/`。
- 内容、配置或构建钩子改动用 `mkdocs build --strict` 验证，必要时用 `mkdocs serve` 看页面。
- 不要擅自创建 `docs/CNAME`，自定义域名属于第二阶段，要等用户确认 DNS 服务商。
- 新增条目前先检查是否已存在，避免重复；跳过琐碎的一次性命令。

## 已知情况

- 线上构建用 Python 3.13，本机 `.venv` 是 Python 3.9.6。目前两边都能构建成功，但并不能保证完全一致。
- 构建时终端会出现一大段红色提示，是 Material 主题对 MkDocs 2.0 的兼容性警告，不是配置错误。
- 本页放在仓库根目录而不是 `docs/`：`docs/` 里的文件都会变成公开网页，并被 `notepush` 一起提交。根目录的文件不会，所以结构说明、给 AI 的约定适合放在这里。
- `pins.yml` 也会作为静态文件出现在网站上，内容只有锚点和时间，可以公开。
- 本地点选接口依赖 MkDocs 1.6 预览服务器的 `get_app/set_app`（标准 WSGI 服务器方法）；升级 MkDocs 后要重新验证点选。
- 本地预览和线上网站的首页只在 `notepush` 后一致；本地点选后未推送时，线上仍是旧的首页。
