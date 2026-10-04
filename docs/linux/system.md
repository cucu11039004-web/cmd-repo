# 系统与软件

查看系统信息、管理软件和服务。Linux 发行版以 Ubuntu 为例，macOS 用 Homebrew。

基础条目参考：[GNU Coreutils 手册](https://www.gnu.org/software/coreutils/manual/coreutils.html)、[systemctl 官方手册源码](https://raw.githubusercontent.com/systemd/systemd/main/man/systemctl.xml)。

## 系统信息

`uname`、`lsb_release`、`lscpu`，查看系统版本和硬件。

### 查看系统和内核信息 { #system-uname }

```bash
uname -a
```

- 助记：`uname` 可按 Unix name（系统名）记；`-a` = all（全部可用的系统信息）。

## 磁盘与挂载

`df`、`du`、`lsblk`、`mount`，查看磁盘空间、找出占空间的目录、挂载硬盘。

### 查看文件系统剩余空间 { #system-df }

```bash
df -h
```

- 助记：`df` ← disk free（磁盘可用空间）；`-h` = human readable（易读单位）。

### 查看一个目录的总大小 { #system-du }

```bash
du -sh ./data
```

- 助记：`du` ← disk usage（磁盘占用）；`-s` = summarize（只给汇总），`-h` = human readable。

### 列出 Linux 磁盘与分区 { #system-lsblk }

```bash
lsblk -f
```

- 助记：`lsblk` ← list block devices（列出块设备）；`blk` 指 block，`-f` 显示 filesystem（文件系统）信息。
- 作用：Linux 命令，显示文件系统、UUID 与挂载点。

## 软件包

`apt`、`brew` 安装、升级和卸载软件。

### 在 Ubuntu 安装软件包 { #system-apt-install }

```bash
sudo apt update
sudo apt install ripgrep
```

- 助记：`APT` ← Advanced Package Tool（高级软件包工具）；update 更新索引，install 安装指定包，作用不同。
- 作用：apt update 更新软件索引，不等于升级所有已安装软件。

### 在 macOS 安装软件包 { #system-brew-install }

```bash
brew install ripgrep
```

- 助记：`brew` = 酿造，是 Homebrew 的命令名；`install` 直接表示安装，不必把 brew 当缩写。
- 作用：需要先安装 Homebrew。

## 服务与日志

`systemctl`、`journalctl`，管理后台服务并查看日志。

### 查看 Linux 服务状态 { #system-service-status }

```bash
systemctl status ssh
```

- 助记：`ctl` 常见于 control（控制）的简写；systemctl 操作系统服务，`status` 是查看状态。
- 作用：使用 systemd 的系统适用；服务名按系统替换，如 sshd。

### 查看指定服务最近的日志 { #system-service-log }

```bash
journalctl -u ssh -n 50 --no-pager
```

- 助记：`journal` = 日志，`ctl` = control；`-u` 指 unit（服务单元），`-n` 指最近记录的数量。
- 作用：Linux systemd 命令；日志读取可能需要 sudo。

## 用户与权限

`sudo`、`groups`、`usermod`，把用户加入组，比如串口用的 `dialout` 组。

### 查看当前用户及所属组 { #system-user-groups }

```bash
id
```

- 助记：`id` = identity（身份）；UID 是 user ID（用户编号），GID 是 group ID（组编号）。
- 作用：串口访问所需的 dialout 组操作见 [串口](../robotics/serial.md)。

## 定时任务

`crontab` 定时执行脚本。

### 查看当前用户的定时任务 { #system-crontab-list }

```bash
crontab -l
```

- 助记：`crontab` 可拆成 cron + table（定时任务表）；`-l` = list（列出），`-e` = edit（编辑）。
- 作用：没有任务时可能提示 no crontab；编辑使用 crontab -e。
