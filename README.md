# cmd-repo · 命令速查表

用 Markdown 记录命令，用 MkDocs Material 查阅和复习。按场景分类，临时内容先放进收集箱。

- 网站地址：<https://cucu11039004-web.github.io/cmd-repo/>（首次开启 Pages 后生效）
- 内容入口：[首页](docs/index.md) · [收集箱](docs/inbox.md)
- 第一阶段使用 GitHub 默认地址；绑定自定义域名留到第一阶段验收后。

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

## 首次开启 GitHub Pages（用户操作）

推送 `main` 后，工作流会构建并把网页发布到 `gh-pages` 分支。

1. 打开仓库的 [Actions](https://github.com/cucu11039004-web/cmd-repo/actions)，等待“发布命令速查表”变成绿色对勾。
2. 打开 [Settings → Pages](https://github.com/cucu11039004-web/cmd-repo/settings/pages)。
3. 在 **Build and deployment → Source** 选择 **Deploy from a branch**。
4. 在 **Branch** 选择 **gh-pages**，目录选择 **/ (root)**，点击 **Save**。如果没有分支选项，等待第一步完成后刷新。
5. 等待 Pages 发布完成，访问网站并搜索 `lsof` 和“端口”。

以后每次推送到 `main` 都会自动更新。手机上也可以直接编辑仓库里的 Markdown 并提交。

## 复习和公开范围

每周把收集箱内容补成“标题、命令、作用、遇到场景、来源”，移到对应分类，然后删除已归档的临时记录。AI 整理提示词和格式模板见 [首页](docs/index.md)。

本仓库公开，不记录密钥、Token、内网地址和私有项目细节。`note` 不会自动识别或清除敏感内容，推送前请检查记录。

## 第二阶段

第一阶段全部验收后，再确认域名服务商并绑定 `cmd.yongtonglab.com`：添加 DNS CNAME、创建 `docs/CNAME`、更新 `mkdocs.yml` 的 `site_url`，最后在 Pages 设置自定义域名及 HTTPS。目前不创建 CNAME 文件。

## 实现依据

- [Material 官方部署方式](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)
- [Material 安装与依赖固定](https://squidfunk.github.io/mkdocs-material/getting-started/)
- [GitHub Pages 发布来源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [actions/checkout](https://github.com/actions/checkout) · [actions/setup-python](https://github.com/actions/setup-python)
