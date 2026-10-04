# VS Code

macOS 下的 VS Code 快捷键。键位写法：`command + shift + p` 表示同时按下这几个键，`command + k → command + s` 表示依次按两组组合键。

基础条目参考：[macOS 官方快捷键表](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-macos.pdf)、[Remote-SSH 文档](https://code.visualstudio.com/docs/remote/ssh)。

## 命令面板与文件跳转

打开命令面板，按文件名、符号快速跳转。

### 打开命令面板 { #vscode-command-palette }

```text
command + shift + p
```

- 助记：`command palette` 是命令面板；与 `command + p` 的文件快速打开组成一对，Shift 切换到命令入口。

### 按文件名快速打开 { #vscode-quick-open }

```text
command + p
```

- 助记：命令名 `Quick Open`（快速打开）；先输入文件名，不需要在目录树里逐层找。

### 在整个项目中搜索 { #vscode-search-project }

```text
command + shift + f
```

- 助记：`F` 可联想 find（查找）；`command + f` 查当前文件，加入 Shift 后查整个项目。

## 编辑与多光标

多光标、整行移动和复制、批量修改同名变量。

### 选中下一个相同文本 { #vscode-next-match }

```text
command + d
```

- 助记：命令名 `Add Selection to Next Find Match`：把下一个匹配加入选区；字母 D 不作词源展开。
- 作用：先选中文本，重复按键可增加多处选区。

### 切换行注释 { #vscode-line-comment }

```text
command + /
```

- 助记：`/` 常见于 `//` 注释，可用这个符号联想“切换注释”。

### 格式化当前文档 { #vscode-format-document }

```text
shift + option + f
```

- 助记：`F` 联想 format（格式化）；该键位调用当前语言的格式化工具。
- 作用：需要当前语言已配置格式化工具。

## 代码导航与重构

跳转定义、查找引用、重命名符号、返回上一个位置。

### 跳转到定义 { #vscode-go-definition }

```text
F12
```

- 助记：`definition` 是定义；F12 是默认功能键绑定，不是英文缩写。
- 作用：部分 Mac 键盘需要同时按 Fn。

### 重命名符号 { #vscode-rename-symbol }

```text
F2
```

- 助记：`rename` = 重新命名，`symbol` = 代码符号；语言服务会一并处理引用位置。
- 作用：由语言服务更新引用；执行前可检查修改预览。

## 终端与面板

打开集成终端，切换侧边栏和底部面板。

### 显示或隐藏集成终端 { #vscode-toggle-terminal }

```text
ctrl + `
```

- 助记：`toggle` 是在显示／隐藏之间切换；反引号键位是默认绑定，没有可靠的缩写展开。

### 显示或隐藏侧边栏 { #vscode-toggle-sidebar }

```text
command + b
```

- 助记：`sidebar` 是侧边栏；`command + b` 是默认绑定，B 可作 bar 的个人联想。

## Remote-SSH 远程开发

连接远程服务器开发，转发端口，在远程打开文件夹。

### 连接 SSH 主机 { #vscode-remote-ssh-connect }

```text
command + shift + p
Remote-SSH: Connect to Host...
```

- 助记：`remote` = 远程，`SSH` = Secure Shell（安全远程终端）；`connect to host` = 连接主机。
- 作用：先安装 Remote - SSH 扩展，再在命令面板选择该命令并填写 SSH 主机。
