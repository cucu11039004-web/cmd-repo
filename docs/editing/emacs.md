# Emacs 键位

HHKB 上 control 在 a 键左边，Emacs 键位按起来很顺手。`+` 表示同时按下，`→` 表示松开前一组后再按下一组，例如 `ctrl + x → ctrl + s`。空格键直接写作 `space`。

本页以 macOS 键盘为例，`option` 需要映射为 Emacs 的 meta 修饰键；Linux 通常使用 `alt`。也可以先按 `escape`，松开后再按对应字符。

基础条目参考：[GNU Emacs 手册](https://www.gnu.org/software/emacs/manual/html_node/emacs/Key-Index.html)。

## 终端与 macOS 通用键位

在 zsh、bash 命令行和 macOS 的大多数输入框里也能用的 Emacs 键位。

### 移到行首 { #emacs-beginning-of-line }

```text
ctrl + a
```

- 助记：`ctrl` 是 control（控制键）；这是 `beginning-of-line`（行的开头）命令。`a` 可联想字母表的起点，属于记忆联想。
- 作用：在 Emacs 和启用 Emacs 键位的终端里移到行首；输入框是否支持取决于应用。

### 移到行尾 { #emacs-end-of-line }

```text
ctrl + e
```

- 助记：`e` 对应 `end`（末尾）；命令名是 `end-of-line`。

### 删除光标到行尾的内容 { #emacs-kill-line }

```text
ctrl + k
```

- 助记：`k` 对应 `kill`；Emacs 的 kill 是剪切到剪切历史，不是结束进程。

## 光标移动

按字符、单词、行首行尾、整屏移动光标。

### 光标移动到下一行 { #emacs-ctrl-n }

```text
ctrl + n
```

- 助记：`n` 对应 `next`（下一步）；Emacs 命令名是 `next-line`（下一行）。终端单行编辑中常用于下一条历史命令。
- 作用：光标移到下一行
- 遇到场景：在 Emacs 中移动光标；终端单行编辑中通常用于下一条历史命令。
- 来源：[GNU Emacs 键位索引](https://www.gnu.org/software/emacs/manual/html_node/emacs/Key-Index.html)。

### 移到上一行 { #emacs-previous-line }

```text
ctrl + p
```

- 助记：`p` 对应 `previous`（前一个）；命令名是 `previous-line`。

### 向前或向后移动一个字符 { #emacs-char-motion }

```text
ctrl + f
ctrl + b
```

- 助记：`f` 对应 `forward`（向前），`b` 对应 `backward`（向后）。
- 作用：两行分别为向前、向后，按需使用。

## 编辑与删除

删除字符、单词和整行，交换字符，改变大小写。

### 删除光标后的一个字符 { #emacs-delete-char }

```text
ctrl + d
```

- 助记：`d` 对应 `delete`（删除）；命令名是 `delete-char`（删除字符）。

### 删除光标后的一个单词 { #emacs-kill-word }

```text
option + d
```

- 助记：`option` 在本页对应 Emacs 的 meta 修饰键；`d` 沿用删除的联想，Meta 组合把操作单位从字符扩展到单词。
- 作用：Meta 在终端和 macOS 输入框中的映射可能不同。

## 选区、剪切与粘贴

设置标记、剪切（kill）、粘贴（yank）和循环粘贴历史。

### 设置选区起点 { #emacs-set-mark }

```text
ctrl + space
```

- 助记：`mark` 是标记：先标记起点，再移动光标形成 region（选区）。空格键直接写为 `space`。
- 作用：在 Emacs 中设置标记，再移动光标选中文本；若被系统输入法快捷键拦截，需先调整系统键位映射。

### 剪切选区 { #emacs-kill-region }

```text
ctrl + w
```

- 助记：命令名 `kill-region` 表示剪切选区；`w` 不作强行词源展开。

### 粘贴最近剪切的内容 { #emacs-yank }

```text
ctrl + y
```

- 助记：`y` 对应 `yank`（拉回）：把之前 kill 的文字拉回来，也就是粘贴。

## 搜索与替换

增量搜索、反向搜索、交互式替换。

### 向前增量搜索 { #emacs-isearch }

```text
ctrl + s
```

- 助记：命令名 `isearch-forward`；`isearch` 是 `incremental search`（增量搜索），`s` 对应 search。
- 作用：在 Emacs 中输入关键词，继续按 ctrl + s 找下一个；终端中 ctrl + s 可能被流控拦截。

### 交互式替换 { #emacs-query-replace }

```text
option + shift + 5
```

- 助记：`query` 是逐项询问，`replace` 是替换；记住“每处都问是否替换”，不用硬记 `%` 的词源。
- 作用：以常见英文键盘布局为例，`shift + 5` 输入 `%`；依次输入旧文本、新文本并按 `enter`，再用 y / n 决定是否替换。

## 文件与缓冲区

打开、保存文件，在缓冲区之间切换。

### 打开文件 { #emacs-find-file }

```text
ctrl + x → ctrl + f
```

- 助记：在 `ctrl + x` 前缀下，`f` 对应 `find file`（查找／打开文件）；与单独 `ctrl + f` 的 forward 不同。

### 保存当前文件 { #emacs-save-buffer }

```text
ctrl + x → ctrl + s
```

- 助记：`s` 对应 `save`（保存）；`buffer` 是编辑中的内存文本，保存才写入文件。

### 切换缓冲区 { #emacs-switch-buffer }

```text
ctrl + x → b
```

- 助记：`b` 对应 `buffer`（缓冲区）；不是打开新文件，而是切换已有编辑内容。

## 窗口

分割窗口、在窗口间切换、关闭窗口。

### 上下分割窗口 { #emacs-split-window }

```text
ctrl + x → 2
```

- 助记：数字 `2` 表示把显示区域分成两个窗口；Emacs 的 window 是缓冲区的显示区域。

### 切换到另一个窗口 { #emacs-other-window }

```text
ctrl + x → o
```

- 助记：`o` 对应 `other`（另一个）；命令名是 `other-window`。

### 只保留当前窗口 { #emacs-one-window }

```text
ctrl + x → 1
```

- 助记：数字 `1` 表示只保留一个显示窗口。
- 作用：只调整显示窗口，不关闭文件缓冲区。

## 撤销、取消与帮助

撤销、取消当前命令，查看某个键位或函数的帮助。

### 撤销修改 { #emacs-undo }

```text
ctrl + /
```

- 助记：`undo` 是撤销；`ctrl + /` 是默认的撤销键位之一，不把 `/` 解释成缩写。

### 取消当前命令 { #emacs-keyboard-quit }

```text
ctrl + g
```

- 助记：命令名 `keyboard-quit` 表示取消当前键盘命令；不是关闭 Emacs。

### 查看一个键位的作用 { #emacs-describe-key }

```text
ctrl + h → k
```

- 助记：`h` 联想 `help`（帮助），`k` 对应 `key`（按键）：查询一个按键的说明。
- 作用：接着按要查询的键位。
