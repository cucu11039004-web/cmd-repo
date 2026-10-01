# Git

在 Git 仓库目录内执行这些命令。

### 查看当前有哪些改动 { #git-status }

<!-- common -->

```bash
git status
```

- 作用：查看当前分支，以及尚未提交、已暂存和未跟踪的文件。
- 遇到场景：准备提交笔记前，先确认这次会涉及哪些文件。
- 来源：命令速查表建站示例。

### 查看尚未暂存的修改 { #git-diff }

<!-- common -->

```bash
git diff
```

- 作用：显示已跟踪文件中尚未暂存的修改；查看已暂存的修改用 `git diff --staged`。
- 遇到场景：提交前检查具体改了哪些内容；新建且未跟踪的文件不会出现在这里。
- 来源：[Git 官方文档：git diff](https://git-scm.com/docs/git-diff)。

### 快速回看最近的提交 { #git-log }

<!-- common -->

```bash
git log --oneline -10
```

- 作用：每行显示一条提交的简短编号和说明，最多显示最近 10 条。
- 遇到场景：想知道最近更新过哪些笔记，或寻找某次修改对应的提交。
- 来源：命令速查表建站示例。

### 创建并切换到新分支 { #git-switch }

```bash
git switch -c feature/demo
```

- 作用：从当前提交创建新分支并切换过去；把 `feature/demo` 换成需要的分支名。
- 遇到场景：开始一项独立修改，希望在新分支上保存和检查。
- 来源：[Git 官方文档：git switch](https://git-scm.com/docs/git-switch)。

### 暂存指定文件 { #git-add }

```bash
git add docs/git.md
```

- 作用：将指定文件当前的修改放入暂存区；把路径换成实际需要提交的文件。
- 遇到场景：只想提交部分文件，先逐个选择，再用 `git diff --staged` 检查。
- 来源：[Git 官方文档：git add](https://git-scm.com/docs/git-add)。

### 提交已经暂存的改动 { #git-commit }

```bash
git commit -m "docs: update commands"
```

- 作用：为暂存区里的修改创建一次提交；把说明替换成这次改动的实际内容。
- 遇到场景：完成一组修改并检查后，保存一个可以回看的版本。
- 来源：[Git 官方文档：git commit](https://git-scm.com/docs/git-commit)。

### 获取远端更新并快进当前分支 { #git-pull }

```bash
git pull --ff-only
```

- 作用：获取上游分支的更新，只在可以快进时更新当前分支；历史分叉时停止。
- 遇到场景：当前分支已设置上游，准备同步其他设备上的提交；历史分叉时先检查提交记录，再处理合并或变基。
- 来源：[Git 官方文档：git pull](https://git-scm.com/docs/git-pull)。

### 推送当前分支的提交 { #git-push }

<!-- common -->

```bash
git push
```

- 作用：按仓库的推送配置将本地提交发送到远端；首次推送新分支可用 `git push -u origin 分支名` 设置上游。
- 遇到场景：当前分支已有上游，完成提交后同步到远端；本仓库推送 `main` 会触发网站发布。
- 来源：[Git 官方文档：git push](https://git-scm.com/docs/git-push)。
