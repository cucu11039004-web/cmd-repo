# Shell 与终端

zsh 和 bash 的通用用法。命令行里的光标移动、删除等键位见 [Emacs 键位](../editing/emacs.md)。

基础条目参考：[Bash 官方手册](https://www.gnu.org/s/bash/manual/bash.html)。

## 重定向与管道

`>`、`>>`、`2>&1`、`|`，把输出写进文件或交给下一条命令。

### 把标准输出和错误保存到日志 { #shell-redirect-log }

```bash
python train.py > train.log 2>&1
```

- 助记：`>` 把标准输出写文件；`2` 是标准错误，`&1` 指标准输出的位置，所以 `2>&1` 合并两路输出。
- 作用：> 覆盖文件，>> 追加；2>&1 必须放在输出重定向之后。脚本名按实际替换。

### 筛选命令输出 { #shell-pipe-filter }

```bash
ps aux | grep '[p]ython'
```

- 助记：`|` 是 pipe（管道）；`grep` 可记成搜索匹配行，名称源于编辑器命令 `g/re/p`（全局／正则／打印）。
- 作用：管道把左侧输出交给右侧；[p]ython 避免匹配 grep 自身。

## 历史与补全

搜索和复用历史命令，善用 Tab 补全。

### 查看历史命令 { #shell-history }

```bash
history
```

- 助记：`history` = 历史；终端保存执行过的命令，可查看后再复用。
- 作用：交互式终端用上箭头取回历史；Tab 补全路径或命令。

## 别名与函数

`alias` 和 shell 函数，把常用的长命令缩短。

### 给长命令起别名 { #shell-alias }

```bash
alias ll='ls -lah'
```

- 助记：`alias` = 别名；`ll` 是自己选的名字，不是系统规定的命令缩写。
- 作用：当前终端生效，长期使用可写入对应 shell 配置文件。

### 创建并进入目录 { #shell-mkcd }

```bash
mkcd() {
    mkdir -p -- "$1" && cd -- "$1"
}
```

- 助记：`mkcd` 是这里自定义的名字，组合了 make directory + change directory；`&&` 表示前一步成功才继续。
- 作用：先定义函数，再运行 mkcd 目录名。

## 环境变量与配置文件

`export`、`PATH`、`~/.zshrc`、`~/.bashrc`，以及让修改生效的方法。

### 设置环境变量 { #shell-export }

```bash
export DEMO_DATA_DIR="$HOME/datasets"
```

- 助记：`export` = 导出；把 shell 变量导出给子进程，双引号保留路径为一个参数。
- 作用：只影响当前终端及其后启动的子进程；程序需主动读取该变量。

### 重新加载 zsh 配置 { #shell-source-zshrc }

```bash
source ~/.zshrc
```

- 助记：`source` = 在当前 shell 读取执行；`rc` 常指 run commands（启动配置），不是启动另一个 shell。
- 作用：在 zsh 中执行；bash 对应 source ~/.bashrc。

### 确认命令来自哪里 { #shell-command-path }

```bash
command -v python
```

- 助记：`command -v` 用于查询命令如何被当前 shell 解析，重点看它指向哪个环境的可执行文件。

## 引号与通配符

单引号、双引号、`*`、`?` 的区别，避免变量和通配符被意外展开。

### 区分字面文本和变量展开 { #shell-quotes }

```bash
printf '%s\n' '$HOME'
printf '%s\n' "$HOME"
```

- 助记：单引号保留原文；双引号允许变量展开，同时把结果保留为一个参数。
- 作用：单引号保留 $HOME 字面值，双引号展开变量并保留为一个参数。

## 脚本基础

写 shell 脚本：参数、条件、循环和 `set -euo pipefail`。

### 遍历匹配文件并保留空格 { #shell-file-loop }

```bash
for file in ./*.txt; do
    [ -f "$file" ] || continue
    printf "%s\n" "$file"
done
```

- 助记：`for ... in ...` = 对列表中的每一项循环；`-f` 判断是否为普通文件，`continue` 跳过当前项。
- 作用：文件变量总是加引号；zsh 无匹配时可能在进入循环前报错，可在脚本中使用 bash。
