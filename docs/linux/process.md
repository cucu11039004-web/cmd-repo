# 进程与资源

以下命令也适用于 macOS 的 zsh / bash；部分 Linux 系统需要先安装 `lsof`。

## 查看进程

列出正在运行的程序，找到它们的 PID。

### 查看正在运行的进程 { #ps-all }

```bash
ps aux
```

- 作用：列出当前可见的进程及其 PID、CPU 和内存使用情况。
- 遇到场景：程序运行异常，想确认进程是否还在运行，或查找占用资源的程序。
- 来源：[procps-ng：ps 手册](https://man7.org/linux/man-pages/man1/ps.1.html)。

## 结束进程

`kill`、`pkill`，结束卡住的程序或残留的训练进程。

## 后台运行

`nohup`、`&`、`jobs`，让任务在后台或退出终端后继续运行。

## 端口占用

查看哪个进程占用了端口。

### 查看谁占用了某个端口 { #port-owner }

```bash
lsof -i :8000
```

- 作用：列出使用 8000 端口的网络连接和进程，PID 是进程编号；没有输出可能是没有匹配结果或权限不足。
- 遇到场景：本地启动服务时报 `address already in use`，需要先确认占用者。
- 来源：命令速查表建站示例。

## 资源监控

`top`、`htop`、`free`，查看 CPU 和内存占用。显卡见 [GPU 与 CUDA](gpu.md)。
