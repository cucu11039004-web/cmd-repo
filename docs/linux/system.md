# 系统与软件

查看系统信息、管理软件和服务。Linux 发行版以 Ubuntu 为例，macOS 用 Homebrew。

## 系统信息

`uname`、`lsb_release`、`lscpu`，查看系统版本和硬件。

## 磁盘与挂载

`df`、`du`、`lsblk`、`mount`，查看磁盘空间、找出占空间的目录、挂载硬盘。

## 软件包

`apt`、`brew` 安装、升级和卸载软件。

## 服务与日志

`systemctl`、`journalctl`，管理后台服务并查看日志。

## 用户与权限

`sudo`、`groups`、`usermod`，把用户加入组，比如串口用的 `dialout` 组。

## 定时任务

`crontab` 定时执行脚本。
