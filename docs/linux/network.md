# 网络

本页以 macOS / Linux 的常见工具为例；`ss` 和 `ip` 仅适用于 Linux，部分系统需先安装相应工具。

基础条目参考：[curl 官方手册](https://curl.se/docs/manpage.html)、[curl 名称说明](https://curl.se/docs/faq.html)、[iproute2：ip 手册](https://man7.org/linux/man-pages/man8/ip.8.html)、[ISC：dig 名称说明](https://www.isc.org/docs/2020webinar-dig.pdf)。

## HTTP 请求

用 `curl`、`wget` 发请求、下载文件或调试接口。

### 查看网站的响应头 { #http-headers }

```bash
curl -I https://example.com
```

- 助记：`curl` 的名称来自 client for URLs（处理 URL 的客户端）的文字组合；大写 `-I` 请求 HEAD，只看响应头，小写 `-i` 则把响应头和正文一起显示。
- 作用：发送 HEAD 请求，查看 HTTP 状态码和响应头，不下载完整页面正文。
- 遇到场景：检查网站是否响应，或查看它是否返回重定向；部分网站不支持 HEAD 请求。
- 来源：命令速查表建站示例，`example.com` 是演示用域名。

### 跟随重定向下载到指定文件 { #network-curl-download }

```bash
curl -fL https://example.com/ -o example.html
```

- 助记：`curl` 用 URL 请求资源；`-f` = fail（HTTP 错误时失败），`-L` = location（跟随跳转），`-o` = output（输出文件）。
- 作用：-f 在 HTTP 错误时返回失败，-L 跟随重定向，-o 指定输出路径。

### 向本地接口发送 JSON { #network-curl-json }

```bash
curl -X POST http://127.0.0.1:8000/echo \
  -H 'Content-Type: application/json' \
  -d '{"message":"hello"}'
```

- 助记：`-X` 指定请求方法，POST 表示提交；`-H` = header（请求头），`-d` = data（请求体数据）。
- 作用：需要本地服务已启动且提供 /echo 接口；地址和字段按实际接口替换。

## 连通性

检查能否到达某台主机。

### 测试网络连通性 { #ping-host }

```bash
ping -c 4 example.com
```

- 助记：`ping` 联想声呐探测的回声；`-c` = count（次数）。这里测的是 ICMP 连通性，不是 HTTP 服务是否正常。
- 作用：发送 4 次 ICMP 探测，查看响应延迟和丢包情况。
- 遇到场景：初步检查能否到达某台主机；主机可能禁用 ICMP，没有响应不一定代表网站无法访问。
- 来源：[iputils：ping 手册](https://man7.org/linux/man-pages/man8/ping.8.html)。

### 查询域名的 DNS 记录 { #network-dig }

```bash
dig example.com
```

- 助记：`dig` ← domain information groper（域名信息探测器），用于查询 DNS，而不是传输网页内容。
- 作用：需要安装 dig；常由 dnsutils 或 bind-utils 包提供。

## 端口与连接

`ss`、`nc`，查看监听端口、测试某个端口能否连通。

### 查看 Linux TCP 监听端口 { #network-ss-listen }

```bash
ss -ltnp
```

- 助记：`ss` 可按 socket statistics（套接字统计）记；`l` = listening，`t` = TCP，`n` = numeric，`p` = processes。
- 作用：Linux 命令；完整进程信息可能需要 sudo。

### 测试 TCP 端口是否可连接 { #network-nc-port }

```bash
nc -vz -w 3 example.com 443
```

- 助记：`nc` 是 netcat（网络连接工具）的命令名；`-z` 只探测端口，`-v` = verbose（详细输出），`-w` 指超时。
- 作用：适用于常见 OpenBSD nc 实现，其他实现参数可能不同。

## 网卡与 IP

`ip addr`、`ifconfig`，查看本机 IP 和网卡状态。

### 查看 Linux 网卡地址与路由 { #network-ip-address-route }

```bash
ip -br addr
ip route
```

- 助记：`IP` ← Internet Protocol（互联网协议）；`addr` = address（地址），`route` = 路由，`-br` = brief（简要）。
- 作用：Linux iproute2 命令；macOS 可用 ifconfig 查看网卡地址。

## 代理

`http_proxy`、`https_proxy` 等环境变量，让终端和下载工具走代理。

### 只让一次请求使用代理 { #network-curl-proxy }

```bash
curl -x http://127.0.0.1:7890 -I https://example.com
```

- 助记：`proxy` = 代理；`-x` 是 curl 指定代理的短选项，这次请求经过给定代理地址。
- 作用：7890 为示例端口，需按已运行的本地代理替换。
