# Linux

以下命令也适用于 macOS 的 zsh / bash。`rg` 需要安装 ripgrep；部分 Linux 系统需要先安装 `lsof`、`curl` 或 `ping`。既有示例的来源表示建站演示，不代表你的学习经历。

## 文件与目录

### 查看当前所在目录 { #pwd }

```bash
pwd
```

- 作用：显示当前工作目录的完整路径。
- 遇到场景：运行项目命令前，确认终端所在的目录。
- 来源：[GNU Coreutils：pwd](https://www.gnu.org/s/coreutils/manual/html_node/pwd-invocation.html)。

### 查看目录里的全部文件 { #ls-all }

<!-- common -->

```bash
ls -la
```

- 作用：以详细列表显示当前目录内容，包括以点开头的隐藏文件。
- 遇到场景：想确认项目里有没有 `.gitignore`，或查看文件权限。
- 来源：命令速查表建站示例。

### 按名称查找 Markdown 文件 { #find-markdown }

<!-- common -->

```bash
find . -type f -name '*.md'
```

- 作用：从当前目录向下查找所有以 `.md` 结尾的文件；引号让通配符交给 `find` 处理。
- 遇到场景：文档分散在多个子目录，不知道某篇笔记放在哪里。
- 来源：命令速查表建站示例。

### 搜索项目里的文本 { #rg-text }

```bash
rg '关键词' .
```

- 作用：递归搜索当前目录中的文本，显示匹配的文件和内容；默认跳过隐藏文件和被忽略的文件。
- 遇到场景：查找某个配置项或报错信息出现在哪个文件中；把 `关键词` 换成要搜索的文本，搜索纯文本时可加 `-F`。
- 来源：[ripgrep 官方指南](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md)。

## 进程

### 查看正在运行的进程 { #ps-all }

```bash
ps aux
```

- 作用：列出当前可见的进程及其 PID、CPU 和内存使用情况。
- 遇到场景：程序运行异常，想确认进程是否还在运行，或查找占用资源的程序。
- 来源：[procps-ng：ps 手册](https://man7.org/linux/man-pages/man1/ps.1.html)。

### 查看谁占用了某个端口 { #port-owner }

<!-- common -->

```bash
lsof -i :8000
```

- 作用：列出使用 8000 端口的网络连接和进程，PID 是进程编号；没有输出可能是没有匹配结果或权限不足。
- 遇到场景：本地启动服务时报 `address already in use`，需要先确认占用者。
- 来源：命令速查表建站示例。

## 网络

### 查看网站的响应头 { #http-headers }

<!-- common -->

```bash
curl -I https://example.com
```

- 作用：发送 HEAD 请求，查看 HTTP 状态码和响应头，不下载完整页面正文。
- 遇到场景：检查网站是否响应，或查看它是否返回重定向；部分网站不支持 HEAD 请求。
- 来源：命令速查表建站示例，`example.com` 是演示用域名。

### 测试网络连通性 { #ping-host }

```bash
ping -c 4 example.com
```

- 作用：发送 4 次 ICMP 探测，查看响应延迟和丢包情况。
- 遇到场景：初步检查能否到达某台主机；主机可能禁用 ICMP，没有响应不一定代表网站无法访问。
- 来源：[iputils：ping 手册](https://man7.org/linux/man-pages/man8/ping.8.html)。
