# cmd-repo · 命令速查表

用 Markdown 记录命令，用 MkDocs Material 查阅和复习。按场景分类，临时内容先放进收集箱。

网站顶部是四个大类：编辑与写作（Emacs、Vim、VS Code、Markdown、正则）、Linux 与服务器、Python 与 AI、机器人，另有首页和收集箱。每个大类下分子页，子页内按二级小节组织。

首页是每日记忆板：按四个大类分成四列，每条只显示小类和命令，想不起作用时点命令进入详情，右侧图标复制。在本地预览中到分类页点 ☆ 把命令加入首页，在首页点 ✕ 移出；每列最新加入的在前，数量不限。

- 网站地址：<https://cucu11039004-web.github.io/cmd-repo/>
- 内容入口：[首页](docs/index.md) · [收集箱](docs/inbox.md)
- 第一阶段使用 GitHub 默认地址；绑定自定义域名留到第一阶段验收后。

第一阶段已于 2026-09-30 验收：本地构建、线上 HTTPS 访问、中英文搜索、搜索结果跳转、命令复制，以及 `note` → `notepush` → 在线收集箱均已验证通过。第二阶段等待确认 DNS 管理平台。

## 本地预览

在项目根目录运行。虚拟环境把依赖限制在这个项目中，不影响系统 Python。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m mkdocs serve
```

打开命令输出中的本地地址。检查导航，搜索 `lsof` 和“端口”，点击搜索结果，并试用代码复制按钮。按 `Ctrl+C` 停止预览。

只检查能否构建：

```bash
.venv/bin/python -m mkdocs build --strict
```

`site/` 是生成的网页，`.venv/` 是本机依赖，二者都不会提交。`requirements.txt` 固定依赖版本，供本地和线上安装使用。

## 一行记录，按需推送

本机项目位于 `$HOME/Workspace/my-cmd-repo`。当前终端先加载一次：

```bash
source "$HOME/Workspace/my-cmd-repo/scripts/notes.sh"
```

如需每次打开终端都可用，把上面这行加入 `~/.zshrc`；bash 用户加入 `~/.bashrc`。若移动项目，请更新加载路径；函数会根据脚本位置自动定位笔记目录。

```bash
note 'ls -la；列出全部文件（含隐藏文件）；list'
cmdserve
notepush
```

`note` 的格式是「命令；作用；来源」，来源可以省略，比如写单词出处帮助记忆（`ls` ← list）。优先用中文分号；整条都没有中文分号时，才按英文分号拆分。

`cmdserve` 启动本地预览并打开浏览器，期间可以归档收集箱、点选首页命令，按 `Ctrl+C` 结束。

用单引号包住记录内容，防止 `$` 或反引号被 shell 执行。`note` 立即写入 `docs/inbox.md`，不依赖网络。`notepush` 先检查站点能否构建，再提交 `docs/` 的改动并推送到 `main`；不会改变当前终端的目录。网络失败后再次执行即可重试，即使没有新改动也可以推送。请先解决远端冲突，不要强制推送 `main`。

配置和脚本的改动需要单独提交；`notepush` 只负责笔记。如果暂存区已有非笔记文件，它会提醒先处理。

验证记录成功：

```bash
tail -n 5 "$HOME/Workspace/my-cmd-repo/docs/inbox.md"
```

## 日常使用

### 添加一条命令

1. 快速记：`note '命令；作用；来源'`，写入收集箱。命令和作用必写，来源可以省略。
2. 运行 `cmdserve`，打开「收集箱」页。每条记录是一张卡片，命令、作用、来源已经按分号填好。
3. 每张卡片**只需选分类**（下拉框按大类分组，选子页即同时选了大类）。小节可选：选了就追加到该小节末尾；不选就放进该页末尾的「未分小节」，有空再挪。
4. 作用直接作为条目标题；锚点按命令自动生成，例如 `ls -la` → `ls-la`，键位类页面加页面名前缀，如 `C-n` → `emacs-c-n`。想自己定锚点或代码语言，点卡片右侧的「更多」。
5. 「⭐ 加入首页」默认勾选，不想上首页就取消。命令和已有条目相同时，卡片上会提醒；不需要的记录点「删除」。
6. 逐条点「归档」，或者各条都选好分类后点顶部的「全部归档」，一次处理完。
7. 按 `Ctrl+C` 结束预览，运行 `notepush`，约一分钟后网站更新。

也可以直接编辑 `docs/` 下的子页，按下面的[条目格式](#条目格式)追加条目。

### 每天点选首页命令

1. 运行 `cmdserve`，浏览器会打开本地预览。
2. 在分类页点条目标题旁的 ☆ 加入首页，再点一次（★）取消；在首页点 ✕ 移出。每次点击会改写 `docs/pins.yml`，页面随即自动刷新。
3. 按 `Ctrl+C` 结束预览，运行 `notepush`，线上首页约一分钟后与本地一致。

线上网站只读：已加入首页的条目在分类页标题旁显示 ★，但没有 ☆ 和 ✕。点选结果保存在仓库文件里，清浏览器缓存不影响。

`docs/pins.yml` 也可以手动编辑：每项是条目锚点 `id` 和加入时间 `added`，首页每列按时间倒序显示。锚点找不到对应条目时构建会报错，删掉那一项即可。

### 新加一个子页或大类

要同时改文件和导航配置，所以**不要用 `notepush`**，用普通 git：

1. 在对应大类目录新建 `docs/<大类>/xxx.md`，写页面说明和二级小节。新大类就新建一个目录。
2. 在 `mkdocs.yml` 的 `nav` 对应大类下加一行 `- 显示名称: <大类>/xxx.md`；新大类要加一个带子页列表的分组。
3. 同步更新 `CODEBASE_MAP.md` 的目录与导航说明。
4. 检查：`.venv/bin/python -m mkdocs build --strict`。
5. 提交并推送：

   ```bash
   git add docs mkdocs.yml CODEBASE_MAP.md
   git commit -m "docs: add xxx page"
   git push
   ```

只加 `xxx.md` 不加 `nav`，页面会生成，但菜单里没有入口，而且 `--strict` 不会报错，容易漏。

改 `mkdocs.yml`、`scripts/`、`deploy.yml` 等配置同理，走普通 git。项目结构和约定见 [CODEBASE_MAP.md](CODEBASE_MAP.md)。

### 条目格式

收集箱归档生成的条目是最简形式：标题就是作用，来源只在填写时出现。

````markdown
### 列出全部文件（含隐藏文件） { #ls-la }

```bash
ls -la
```

- 来源：list
````

手写时也可以加「- 作用：」写更长的解释，加「- 遇到场景：」记录什么时候用。来源可以是单词出处、助记，或者学习出处、官方文档链接。

每个三级标题都是一个条目，必须有固定锚点和完整非空的代码块，否则构建会报错并给出文件、行号和标题。

锚点是条目在网址里的门牌号（`…/linux/files/#ls-la` 中 `#` 后面那段）。首页的链接和 `pins.yml` 都靠它找到条目，所以要**全站唯一**，并且不随标题变化。只用小写英文字母、数字和连字符，以字母开头。收集箱归档会自动生成；手写时以工具或主题作前缀，如 `tmux-detach`、`torch-no-grad`。

键位类条目的代码块语言用 `text`，写法见各页开头的说明，例如 Emacs 的 `C-x C-s`、VS Code 的 `Cmd+Shift+P`。

### 请 AI 帮忙整理

在这个仓库里进行的 AI 会话结束后，可以复制下面的提示词：

```text
把这次会话里我可能再次用到的新命令，整理到当前命令速查表仓库 docs/<大类>/<子页>.md 中对应的二级小节，追加到小节末尾。
大类目录：editing（编辑与写作）、linux（Linux 与服务器）、python（Python 与 AI）、robotics（机器人）；子页和小节以 mkdocs.yml 的 nav 和页面内的二级标题为准。
每条至少有：标题（写作用）、全站唯一的固定英文锚点（以工具或主题作前缀）、命令代码块；需要时加「- 遇到场景：」和「- 来源：」。
来源写单词出处或助记，或本次会话中确实出现且可以公开的学习出处、实际核对的官方文档；不清楚时先问我，不要编造。
跳过琐碎的一次性命令，不重复已有条目，保留已有内容；不要添加 <!-- common --> 标记，也不要改 docs/pins.yml，首页由我自己点选。
不要记录密钥、Token、内网地址和私有项目细节，文档内部链接只使用相对路径。
从收集箱归类的条目，确认归档完成后再删除临时记录，保留收集箱标题和说明。
```

手机临时记录时，也可以在 GitHub 网页或 App 打开 `docs/inbox.md` 编辑。

## 首次开启 GitHub Pages（用户操作）

推送 `main` 后，工作流会构建并把网页发布到 `gh-pages` 分支。

1. 打开仓库的 [Actions](https://github.com/cucu11039004-web/cmd-repo/actions)，等待“发布命令速查表”变成绿色对勾。
2. 打开 [Settings → Pages](https://github.com/cucu11039004-web/cmd-repo/settings/pages)。
3. 在 **Build and deployment → Source** 选择 **Deploy from a branch**。
4. 在 **Branch** 选择 **gh-pages**，目录选择 **/ (root)**，点击 **Save**。如果没有分支选项，等待第一步完成后刷新。
5. 等待 Pages 发布完成，访问网站并搜索 `lsof` 和“端口”。

以后每次推送到 `main` 都会自动更新。手机上也可以直接编辑仓库里的 Markdown 并提交。

## 复习和公开范围

定期在本地预览的收集箱页把记录归档到分类，归档后记录会自动从收集箱删除。AI 整理提示词和格式模板见上面的「日常使用」。

本仓库公开，不记录密钥、Token、内网地址和私有项目细节。`note` 不会自动识别或清除敏感内容，推送前请检查记录。

## 第二阶段

第一阶段全部验收后，再确认域名服务商并绑定 `cmd.yongtonglab.com`：添加 DNS CNAME、创建 `docs/CNAME`、更新 `mkdocs.yml` 的 `site_url`，最后在 Pages 设置自定义域名及 HTTPS。目前不创建 CNAME 文件。

## 实现依据

- [MkDocs 构建钩子](https://www.mkdocs.org/user-guide/configuration/#hooks)
- [Material 官方部署方式](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)
- [Material 安装与依赖固定](https://squidfunk.github.io/mkdocs-material/getting-started/)
- [GitHub Pages 发布来源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [actions/checkout](https://github.com/actions/checkout) · [actions/setup-python](https://github.com/actions/setup-python)
