# 网络

以下命令也适用于 macOS 的 zsh / bash；部分 Linux 系统需要先安装 `curl` 或 `ping`。

## HTTP 请求

用 `curl`、`wget` 发请求、下载文件或调试接口。

### 查看网站的响应头 { #http-headers }

```bash
curl -I https://example.com
```

- 作用：发送 HEAD 请求，查看 HTTP 状态码和响应头，不下载完整页面正文。
- 遇到场景：检查网站是否响应，或查看它是否返回重定向；部分网站不支持 HEAD 请求。
- 来源：命令速查表建站示例，`example.com` 是演示用域名。

## 连通性

检查能否到达某台主机。

### 测试网络连通性 { #ping-host }

```bash
ping -c 4 example.com
```

- 作用：发送 4 次 ICMP 探测，查看响应延迟和丢包情况。
- 遇到场景：初步检查能否到达某台主机；主机可能禁用 ICMP，没有响应不一定代表网站无法访问。
- 来源：[iputils：ping 手册](https://man7.org/linux/man-pages/man8/ping.8.html)。

## 端口与连接

`ss`、`nc`，查看监听端口、测试某个端口能否连通。

## 网卡与 IP

`ip addr`、`ifconfig`，查看本机 IP 和网卡状态。

## 代理

`http_proxy`、`https_proxy` 等环境变量，让终端和下载工具走代理。
