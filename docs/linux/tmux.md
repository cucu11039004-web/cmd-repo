# tmux

终端复用：SSH 断线后训练任务继续运行，一个窗口里分多个窗格。键位写法：`ctrl + b → d` 表示先按 ctrl + b，松开后再按 d（`ctrl + b` 是默认前缀键）。

基础条目参考：[tmux 官方入门](https://github.com/tmux/tmux/wiki/Getting-Started)。

## 会话

新建、脱离、重新连接和列出会话。

### 新建一个有名字的会话 { #tmux-new-session }

```bash
tmux new -s train
```

- 助记：`tmux` ← terminal multiplexer（终端复用器）；new 是新建，`-s` 指 session name（会话名）。

### 列出已有会话 { #tmux-list-sessions }

```bash
tmux ls
```

- 助记：`ls` 是 list-sessions 的别名，列出会话；这里不是文件目录的 ls。

### 重新连接会话 { #tmux-attach-session }

```bash
tmux attach -t train
```

- 助记：`attach` = 连接回已有会话；`-t` = target（目标），后面指定会话名。

### 脱离会话并保持任务运行 { #tmux-detach-session }

```text
ctrl + b → d
```

- 助记：前缀 `ctrl + b` 后，`d` = detach（脱离）；脱离显示连接而不结束会话内任务。

## 窗口

在一个会话里新建、切换和重命名窗口。

### 新建窗口 { #tmux-new-window }

```text
ctrl + b → c
```

- 助记：前缀键松开后按 `c` 可联想 create（创建）；创建的是会话内的 window（窗口）。

### 切换到下一个窗口 { #tmux-next-window }

```text
ctrl + b → n
```

- 助记：前缀键松开后按 `n` = next（下一个）；对应 `p` = previous（上一个）。

## 窗格

分屏、在窗格间移动、调整大小。

### 左右分屏 { #tmux-split-horizontal }

```text
ctrl + b → shift + 5
```

- 助记：常见英文键盘上 `shift + 5` 输入 `%`，这是左右分屏的默认键位。

### 上下分屏 { #tmux-split-vertical }

```text
ctrl + b → shift + '
```

- 助记：常见英文键盘上 `shift + '` 输入双引号，这是上下分屏的默认键位；与 `%` 的左右分屏成对记忆。

### 切换到下一个窗格 { #tmux-next-pane }

```text
ctrl + b → o
```

- 助记：`pane` 是一个窗口里的窗格；前缀键松开后按 `o` 切换到下一个窗格。

## 复制模式与滚动

向上翻看输出、选择并复制文本。

### 进入滚动查看模式 { #tmux-copy-mode }

```text
ctrl + b → [
```

- 助记：`copy mode` 是复制／滚动模式；`[` 是进入该模式的默认键位。
- 作用：进入复制模式后用方向键或 page up 查看历史；默认 Emacs 键位下按 q 退出。

## 配置

`~/.tmux.conf` 常用设置，比如鼠标支持和改前缀键。

### 在当前会话启用鼠标 { #tmux-enable-mouse }

```bash
tmux set -g mouse on
```

- 助记：`set` = 设置，`-g` = global（全局），`mouse on` = 开启鼠标支持。
- 作用：长期启用可将 set -g mouse on 写入 ~/.tmux.conf。
