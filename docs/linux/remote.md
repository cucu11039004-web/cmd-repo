# 远程连接与传输

连接训练服务器和机器人主机，在本机和远程之间传文件。

基础条目参考：[OpenSSH 手册](https://man.openbsd.org/ssh)。

## SSH 登录与配置

`ssh` 登录，用 `~/.ssh/config` 给主机起别名。

### 登录远程主机 { #remote-ssh-login }

```bash
ssh user@server.example.com
```

- 助记：`SSH` ← Secure Shell（安全远程终端）；`user@host` 分别指定以谁的身份、登录哪台主机。
- 作用：替换用户名和主机；首次连接时核对主机指纹。

### 指定 SSH 端口 { #remote-ssh-port }

```bash
ssh -p 2222 user@server.example.com
```

- 助记：`-p` = port（端口）；ssh 使用小写 p 指定连接端口。

## 密钥

`ssh-keygen`、`ssh-copy-id`，配置免密登录。

### 创建 Ed25519 SSH 密钥 { #remote-ssh-keygen }

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_demo -C "demo"
```

- 助记：`keygen` = key generation（密钥生成）；`-t` = type（类型），`-f` = file（文件），`-C` = comment（备注）。
- 作用：示例使用独立文件名；设置口令，若已有同名文件不要覆盖。只把 .pub 公钥提供给服务端。

## 端口转发

`ssh -L` 把远程的 Jupyter、TensorBoard 映射到本机浏览器。

### 把远程服务转发到本机 { #remote-ssh-forward }

```bash
ssh -N -L 127.0.0.1:8888:127.0.0.1:8888 user@server.example.com
```

- 助记：`-L` = local forwarding（本地转发），`-N` 不执行远程命令；两个地址分别是本机监听位置与远端连接目标。
- 作用：远程服务需监听远端 8888；保持此连接，浏览器访问本机 8888。

## 文件传输

`scp`、`rsync`，上传代码、下载模型和实验结果。

### 把文件上传到远程主机 { #remote-scp-upload }

```bash
scp results.csv user@server.example.com:~/results/
```

- 助记：`scp` ← secure copy（安全复制）；冒号前是远程主机，冒号后是远程路径。

### 增量同步目录并显示进度 { #remote-rsync }

```bash
rsync -av --progress ./results/ user@server.example.com:~/results/
```

- 助记：`rsync` 可按 remote synchronization（远程同步）记；`-a` = archive（保留属性等），`-v` = verbose（详细），progress 是进度。
- 作用：源目录末尾的 / 表示同步目录内容；两端都需 rsync，这里不删除远端额外文件。

## 远程挂载

`sshfs` 把远程目录挂载到本机。

### 挂载远程目录到本机 { #remote-sshfs }

```bash
mkdir -p ~/remote-data
sshfs user@server.example.com:/home/user/data ~/remote-data
```

- 助记：`SSHFS` = SSH filesystem（通过 SSH 访问的文件系统）；把远程目录映射成本机目录。
- 作用：需要 SSHFS 与 FUSE；Linux 卸载可用 fusermount -u ~/remote-data，macOS 通常用 umount。
