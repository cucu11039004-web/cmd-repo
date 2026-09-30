# 命令速查表网站：搭建计划书

> 这份文档是写给执行者（ChatGPT）的。你没有之前的对话背景，请把本文当作完整需求。
> 用户的编程背景较窄，所以每一步都要说明"为什么这样做"，并给出可以直接复制的命令。

---

## 1. 目标

用户想要一个**属于自己、放在网上、随时能查阅**的命令速查表：

- 用户在系统学习 Linux 等命令，也会在"用 AI 辅助做新项目"时遇到大量新命令，希望**干中学**，遇到就记。
- 记录要**摩擦极低**（尽量在终端里一行完成），否则坚持不下来。
- 网站的作用是**查阅和复习**；真正的练习在终端里发生。
- 内容必须是**纯 Markdown**，不被任何平台锁定，以后可以迁移。

## 2. 已确认的决定（不要擅自更改）

| 项目 | 决定 |
|---|---|
| 托管 | GitHub **公开**仓库 + GitHub Pages |
| 站点工具 | **MkDocs + Material 主题**（自带搜索） |
| 域名 | **第一阶段用 GitHub 默认地址**，跑通后再绑定 `cmd.yongtonglab.com`（第二阶段） |
| 内容组织 | 按场景分文件，固定条目格式（含作用、场景、来源），另设 `inbox.md` 临时收集 |
| 录入方式 | 终端 `note` 函数；AI 会话结束后整理追加；每周清理 inbox |
| 语言 | 说明文字用中文，命令本身保持英文原样 |
| 第一版范围 | 只做搭建 + 约 5 个初始文件 + 一个 inbox，只跑通"记录、推送、在线查看" |
| 公开注意 | 不记密钥、Token、内网地址、私有项目细节 |

**明确不要做的事**：不租服务器；不写自定义主题；不装一堆插件；不做评论、统计等花哨功能；不要把站点和用户的博客（另一个项目，用 Hugo）合并。

## 3. 执行原则

1. **标记为 🧑 的步骤只能用户自己做**（需要登录账号或点网页按钮）。请把这些步骤写成"照着点就行"的逐步说明，不要假装你能代做。
2. 如果你无法直接操作用户电脑，就把每个文件的完整内容和每条命令写出来，让用户复制执行。
3. 涉及版本、配置写法的地方（MkDocs Material、GitHub Actions、GitHub Pages 设置），**请以官方文档为准核对**，这些内容可能有更新。
4. 每完成一个阶段，给用户一个"怎么验证成功了"的检查方法。
5. 遇到需要用户提供的信息（GitHub 用户名、操作系统、终端类型），先问，不要猜。

## 4. 开始前需要向用户确认的信息

- GitHub 用户名（用来生成默认网址 `https://<用户名>.github.io/<仓库名>/`）
- 操作系统（macOS / Linux / Windows）以及使用的终端和 shell（zsh / bash / PowerShell 等）
- 电脑上是否已装 `git` 和 `python3`（如果没有，先指导安装）
- 仓库名：默认建议 `cheatsheet`，用户没有异议就用它

---

## 5. 第一阶段：搭建并跑通（使用 GitHub 默认地址）

### 步骤 1 🧑 创建 GitHub 仓库

让用户在 GitHub 网页上新建一个**公开**仓库 `cheatsheet`，勾选添加 README，其余默认。

### 步骤 2 克隆仓库并搭建 MkDocs 项目

```bash
git clone https://github.com/<用户名>/cheatsheet.git ~/cheatsheet
cd ~/cheatsheet
python3 -m venv .venv
source .venv/bin/activate
pip install mkdocs-material
```

**为什么用虚拟环境**：把这个项目需要的包隔离起来，不污染系统 Python，也避免和别的项目冲突。

在仓库根目录创建 `.gitignore`：

```
.venv/
site/
.DS_Store
```

**为什么**：`site/` 是 MkDocs 生成的网页，属于构建产物，不需要进版本库；`.venv/` 体积大且因机器而异。

### 步骤 3 写配置文件 `mkdocs.yml`

```yaml
site_name: 命令速查表
site_url: https://<用户名>.github.io/cheatsheet/
theme:
  name: material
  language: zh
  features:
    - search.highlight
    - content.code.copy
    - navigation.top
markdown_extensions:
  - admonition
  - pymdownx.highlight
  - pymdownx.superfences
plugins:
  - search
nav:
  - 首页: index.md
  - 收集箱: inbox.md
  - Linux 文件操作: linux-files.md
  - Linux 进程与网络: linux-process-network.md
  - Git: git.md
  - Docker: docker.md
  - Python 环境: python-env.md
```

说明给用户听：`content.code.copy` 让每个代码块右上角出现复制按钮；`search` 是速查表最关键的功能。

### 步骤 4 创建内容文件（放在 `docs/` 目录下）

需要创建：`index.md`、`inbox.md`、`linux-files.md`、`linux-process-network.md`、`git.md`、`docker.md`、`python-env.md`。

**硬性约束**：文档之间的链接**只用相对路径**（例如 `[Git](git.md)`），不要写死完整网址。这样以后换域名，内部链接不会失效。

**每条记录的固定格式**（所有分类文件都用它）：

````markdown
### 查看谁占用了某个端口

```bash
lsof -i :8000
```

- 作用：列出占用 8000 端口的进程，拿到 PID 后可以 `kill`
- 遇到场景：本地起服务时提示 "address already in use"
- 来源：（写明在哪个项目或哪次学习中遇到）
````

说明给用户听：**"遇到场景"最重要**。只记命令很容易忘，记住"什么时候用"才能记牢。

**初始内容**：每个分类文件放 1 到 2 条真实、常用的示例条目，用来演示格式（例如：`linux-files.md` 放 `ls -la`、`find`；`git.md` 放 `git status`、`git log --oneline`；`docker.md` 放 `docker ps`；`python-env.md` 放 `python3 -m venv`）。`inbox.md` 顶部写一句说明：这里是临时收集区，每周清理归类。`index.md` 写简短的使用说明和条目格式模板。

### 步骤 5 本地预览

```bash
mkdocs serve
```

让用户在浏览器打开命令输出里给出的本地地址，确认页面、导航、搜索都正常。

### 步骤 6 配置自动部署（GitHub Actions）

创建 `.github/workflows/deploy.yml`，实现：每次 push 到 `main` 分支，自动构建并发布。推荐使用 MkDocs Material 官方文档中的部署方式（`mkdocs gh-deploy --force`，需要给 workflow 设置 `contents: write` 权限）。请对照官方文档核对最新写法。

**为什么要自动部署**：这样用户只需要 `git push`，网站就会更新，录入链路最短。

### 步骤 7 首次推送

```bash
git add .
git commit -m "init: cheatsheet site"
git push
```

### 步骤 8 🧑 开启 GitHub Pages

让用户在仓库页面操作：**Settings → Pages**，把发布来源设为 `gh-pages` 分支（根目录）。首次推送后 Actions 会自动创建这个分支；如果选项里暂时没有，等 Actions 跑完再刷新。

### 步骤 9 验证

- 仓库 **Actions** 页面显示部署成功（绿色对勾）。
- 浏览器访问 `https://<用户名>.github.io/cheatsheet/` 能看到网站。
- 在网站搜索框搜 `lsof`，能搜到示例条目。

---

## 6. 降低录入摩擦

### 6.1 终端快速记录函数

先检测用户的 shell，再写入对应配置文件（zsh 用 `~/.zshrc`，bash 用 `~/.bashrc`；Windows PowerShell 请改写成对应的 `$PROFILE` 函数）。

```bash
# 追加一行到收集箱
note() {
  echo "- $(date +%F) $*" >> ~/cheatsheet/docs/inbox.md
  echo "已记录到 inbox"
}

# 提交并推送（网站会自动更新）
notepush() {
  cd ~/cheatsheet && git add -A && git commit -m "notes: $(date +%F)" && git push
  cd - > /dev/null
}
```

用法示例：`note "lsof -i :8000 查端口占用"`，然后需要时执行 `notepush`。

**为什么拆成两个函数**：记录要快，不应该每次都等网络推送；想发布时再 `notepush`。

提醒用户：修改配置文件后要 `source ~/.zshrc`（或重开终端）才会生效。

### 6.2 AI 会话结束后的整理提示词

给用户一段可以复制的提示词：

```
把这次会话里出现的新命令整理出来，按下面的格式追加到 ~/cheatsheet/docs/ 里对应的分类文件：
- 标题：一句话说明用途
- 代码块：命令
- 作用 / 遇到场景 / 来源（来源写本次项目名）
只整理我可能会再次用到的命令，琐碎的一次性命令不要。不要记录任何密钥、Token、内网地址。
```

### 6.3 每周清理

每周一次：把 `inbox.md` 里的条目补全格式，归到对应分类文件，清空 inbox。这一步本身就是复习。

### 6.4 手机应急

GitHub 网页和 App 都可以直接编辑 Markdown，临时想记一条时可用。

---

## 7. 第二阶段：绑定子域名 `cmd.yongtonglab.com`

**前提**：第一阶段全部验证通过后再做。用户已拥有域名 `yongtonglab.com`。

1. 🧑 **在域名服务商后台添加 DNS 记录**：类型 `CNAME`，主机记录 `cmd`，记录值 `<用户名>.github.io`。请先询问用户的域名服务商是谁，再给出对应后台的点击路径。DNS 生效可能需要几分钟到几小时。
2. 在仓库的 `docs/` 目录下创建 `CNAME` 文件，内容只有一行：`cmd.yongtonglab.com`。**为什么放 `docs/`**：MkDocs 会把它原样复制到发布目录，避免每次部署时 GitHub 的自定义域名设置被覆盖。
3. 把 `mkdocs.yml` 里的 `site_url` 改成 `https://cmd.yongtonglab.com/`，提交并推送。
4. 🧑 **在 GitHub 设置自定义域名**：Settings → Pages → Custom domain 填 `cmd.yongtonglab.com` 并保存，等 DNS 检查通过后勾选 **Enforce HTTPS**。
5. 验证：访问 `https://cmd.yongtonglab.com` 能打开网站，浏览器显示安全锁；旧的 `github.io` 地址会自动跳转到新域名。

---

## 8. 总验收清单

- [x] 本地 `mkdocs serve` 正常，搜索可用
- [x] 推送后 GitHub Actions 自动部署成功
- [x] 在线网站可访问，搜索可用
- [x] `note "..."` 能写入 inbox，`notepush` 能推送并使网站更新
- [x] 所有文档内部链接均为相对路径
- [x] 仓库中不含任何密钥、Token、内网地址
- [ ]（第二阶段）`cmd.yongtonglab.com` 可访问且有 HTTPS

## 9. 用户做的 🧑 步骤汇总

1. 在 GitHub 新建公开仓库
2. 在 GitHub Settings → Pages 选择 `gh-pages` 分支
3. 在域名服务商后台添加 `cmd` 的 CNAME 记录（第二阶段）
4. 在 GitHub Settings → Pages 填自定义域名并开启 HTTPS（第二阶段）
