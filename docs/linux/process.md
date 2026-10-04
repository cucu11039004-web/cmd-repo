# 进程与资源

没有注明 Linux 的条目可用于 macOS；`pgrep` 的参数差异和 `free` 的平台限制见条目说明，部分 Linux 系统需先安装 `lsof`。

基础条目参考：[procps-ng：ps 手册](https://man7.org/linux/man-pages/man1/ps.1.html)、[Linux：kill 手册](https://man7.org/linux/man-pages/man1/kill.1.html)。

## 查看进程

列出正在运行的程序，找到它们的 PID。

### 查看正在运行的进程 { #ps-all }

```bash
ps aux
```

- 助记：`ps` 可按 process status（进程状态）记；BSD 风格的 `a` 扩大用户范围，`u` 显示用户格式，`x` 包含无终端进程。
- 作用：列出当前可见的进程及其 PID、CPU 和内存使用情况。
- 遇到场景：程序运行异常，想确认进程是否还在运行，或查找占用资源的程序。
- 来源：[procps-ng：ps 手册](https://man7.org/linux/man-pages/man1/ps.1.html)。

### 查找指定程序的 PID 和命令行 { #process-pgrep }

```bash
pgrep -af 'train.py'
```

- 助记：`pgrep` 可按 process + grep（搜索进程）记；Linux 的 `-a` 显示完整命令，`-f` 按完整命令行匹配。
- 作用：Linux procps 写法；macOS 可用 pgrep -fl。

## 结束进程

`kill`、`pkill`，结束卡住的程序或残留的训练进程。

### 请求进程正常退出 { #process-kill-term }

```bash
kill -TERM 12345
```

- 助记：`kill` 的实际作用是发送信号；`TERM` ← termination（终止），PID 是 process ID（进程编号）。
- 作用：先确认 PID 并替换示例编号；TERM 允许程序处理退出，程序是否响应取决于实现。

## 后台运行

`nohup`、`&`、`jobs`，让任务在后台或退出终端后继续运行。

### 退出终端后仍让任务继续运行 { #process-nohup }

```bash
nohup python train.py > train.log 2>&1 < /dev/null &
```

- 助记：`nohup` ← no hangup（忽略挂断）；结尾 `&` 才是让任务在后台运行，两者作用不同。
- 作用：忽略挂断信号并重定向输入输出；重启或进程报错仍会停止。

### 查看并切回终端后台任务 { #process-jobs }

```bash
jobs
fg %1
```

- 助记：`jobs` = 作业列表；`fg` ← foreground（前台），`%1` 是 shell 作业号，不是进程 PID。
- 作用：两步在启动任务的同一个 shell 中执行，%1 换成 jobs 显示的作业号。

## 端口占用

查看哪个进程占用了端口。

### 查看谁占用了某个端口 { #port-owner }

```bash
lsof -i :8000
```

- 助记：`lsof` ← list open files（列出打开的文件）；网络连接也按打开对象查看，`-i :8000` 筛选网络端口。
- 作用：列出使用 8000 端口的网络连接和进程，PID 是进程编号；没有输出可能是没有匹配结果或权限不足。
- 遇到场景：本地启动服务时报 `address already in use`，需要先确认占用者。
- 来源：命令速查表建站示例。

### 只查看某端口的 TCP 监听进程 { #process-listening-port }

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

- 助记：`lsof` ← list open files；`-n` 不解析主机名，`-P` 保留数字端口，`LISTEN` = 监听状态。

## 资源监控

`top`、`htop`、`free`，查看 CPU 和内存占用。显卡见 [GPU 与 CUDA](gpu.md)。

### 交互查看 CPU 和内存占用 { #process-top }

```bash
top
```

- 助记：`top` 是动态进程查看器；可按“最上方列出资源使用突出的进程”记用途，不当作缩写。
- 作用：按 q 退出。

### 查看 Linux 内存总量与可用量 { #process-free }

```bash
free -h
```

- 助记：`free` = 空闲；`-h` = human readable（易读单位），available 表示估算的可用内存。
- 作用：Linux 命令；判断剩余可用内存主要看 available 列。
