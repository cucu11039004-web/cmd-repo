# cmd-repo · 命令速查表

用 Markdown 记录命令，用 MkDocs Material 查阅和复习。按场景分类，临时内容先放进收集箱。

网站导航为：首页、Linux、Python 环境、收集箱。首页只展示每类最多 4 条常用命令，点击命令查看分类条目，代码块右上角可以复制；Linux 页内分文件与目录、进程、网络，Python 环境页内分 `.venv`、Conda、uv。

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
note 'lsof -i :8000 查端口占用；场景：服务启动失败；来源：本次学习'
notepush
```

用单引号包住记录内容，防止 `$` 或反引号被 shell 执行。`note` 立即写入 `docs/inbox.md`，不依赖网络。`notepush` 先检查站点能否构建，再提交 `docs/` 的改动并推送到 `main`；不会改变当前终端的目录。网络失败后再次执行即可重试，即使没有新改动也可以推送。请先解决远端冲突，不要强制推送 `main`。

配置和脚本的改动需要单独提交；`notepush` 只负责笔记。如果暂存区已有非笔记文件，它会提醒先处理。

验证记录成功：

```bash
tail -n 5 "$HOME/Workspace/my-cmd-repo/docs/inbox.md"
```

## 日常使用

### 添加一条命令

1. 快速记：`note '命令；作用；场景；来源'`，写入收集箱。
2. 或直接编辑 `docs/` 下对应分类页，按下面的[固定条目格式](#固定条目格式)追加条目。
3. 运行 `notepush`，约一分钟后网站更新。

### 新加一个分类

要同时改文件和菜单配置，所以**不要用 `notepush`**，用普通 git：

1. 在 `docs/` 新建 `xxx.md`，写入内容。
2. 在 `mkdocs.yml` 的 `nav` 里加一行 `- 显示名称: xxx.md`。
3. 按下面的格式标记希望展示在首页的常用条目；首页会在构建时按导航顺序自动汇总。
4. 同步更新 `CODEBASE_MAP.md` 的目录与导航说明。
5. 检查：`.venv/bin/python -m mkdocs build --strict`。
6. 提交并推送：

   ```bash
   git add docs/xxx.md mkdocs.yml CODEBASE_MAP.md
   git commit -m "docs: add xxx category"
   git push
   ```

只加 `xxx.md` 不加 `nav`，页面会生成，但菜单里没有入口，而且 `--strict` 不会报错，容易漏。

改 `mkdocs.yml`、`scripts/notes.sh`、`deploy.yml` 等配置同理，走普通 git。项目结构和约定见 [CODEBASE_MAP.md](CODEBASE_MAP.md)。

### 固定条目格式

“遇到场景”最重要：记住什么时候用，比只记命令更容易复习。下面的来源是填写示例，请替换成真实学习经历或实际核对的官方文档。

````markdown
### 查看谁占用了某个端口 { #port-owner }

<!-- common -->

```bash
lsof -i :8000
```

- 作用：查看使用 8000 端口的进程及 PID。
- 遇到场景：本地服务启动时报 address already in use。
- 来源：填写本次学习、可公开的项目名或官方文档链接。
````

固定锚点只用小写英文字母、数字和连字符，以字母开头，在同一页内保持唯一；修改中文标题时保留锚点，已有详情链接就仍然可用。常用条目在标题下加 `<!-- common -->`；其他条目去掉这行即可。

### 维护首页常用命令

分类页是唯一内容来源。构建钩子 `scripts/common_commands.py` 读取 `mkdocs.yml` 导航里的分类页（首页和收集箱除外），按导航顺序分组，再按文件顺序取每类前 4 条标记为常用的条目。不足 4 条时全部显示；没有常用条目的分类不会出现在首页。

首页只显示分组和命令代码块，点击命令文本跳到对应条目，点击复制按钮则复制命令；标题、作用、场景和来源保留在分类页。构建钩子在 Markdown 渲染后将详情链接放到命令文本上，保留主题原生的复制功能。

首页采用紧凑的分类网格，按可用宽度自动分栏；窄屏纵向排列，长命令可以换行，复制的文本不受换行影响。首页隐藏右侧目录，样式位于 `docs/stylesheets/home.css`，不影响分类详情页。

修改分类里的命令、作用或常用标记后，首页在下次构建和发布时自动更新。把常用条目在分类页内前移，可以调整精选顺序。`docs/index.md` 只保留标题和 `<!-- common-commands -->` 占位符，不需要复制命令进去。

常用条目缺少固定英文锚点、完整非空代码块或作用说明，以及同页固定锚点重复时，构建会报错并给出文件、行号和标题。构建钩子自身修改后，请重启 `mkdocs serve`；分类 Markdown 的修改可以自动刷新。

### 请 AI 帮忙整理

在这个仓库里进行的 AI 会话结束后，可以复制下面的提示词：

```text
把这次会话里我可能再次用到的新命令，整理到当前命令速查表仓库 docs/ 下对应的分类 Markdown 文件。
Linux 统一放在 linux.md，按文件与目录、进程、网络归类；Python 环境按 .venv、Conda、uv 归类。
每条保留：标题、命令代码块、作用、遇到场景、来源；标题配置同页唯一的固定英文锚点。
来源使用本次会话中确实出现且可以公开的学习或项目名称，或实际核对的官方文档；不清楚时先问我，不要编造。
跳过琐碎的一次性命令，不重复已有条目，保留已有内容；只按我的选择为常用条目添加 <!-- common -->，首页自动汇总每类前 4 条。
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

每周把收集箱内容补成“标题、命令、作用、遇到场景、来源”，移到对应分类，然后删除已归档的临时记录，保留收集箱标题和说明。AI 整理提示词和格式模板见上面的「日常使用」。

本仓库公开，不记录密钥、Token、内网地址和私有项目细节。`note` 不会自动识别或清除敏感内容，推送前请检查记录。

## 第二阶段

第一阶段全部验收后，再确认域名服务商并绑定 `cmd.yongtonglab.com`：添加 DNS CNAME、创建 `docs/CNAME`、更新 `mkdocs.yml` 的 `site_url`，最后在 Pages 设置自定义域名及 HTTPS。目前不创建 CNAME 文件。

## 实现依据

- [MkDocs 构建钩子](https://www.mkdocs.org/user-guide/configuration/#hooks)
- [Material 官方部署方式](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)
- [Material 安装与依赖固定](https://squidfunk.github.io/mkdocs-material/getting-started/)
- [GitHub Pages 发布来源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [actions/checkout](https://github.com/actions/checkout) · [actions/setup-python](https://github.com/actions/setup-python)
