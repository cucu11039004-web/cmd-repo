# 远程连接与传输

连接训练服务器和机器人主机，在本机和远程之间传文件。

## SSH 登录与配置

`ssh` 登录，用 `~/.ssh/config` 给主机起别名。

## 密钥

`ssh-keygen`、`ssh-copy-id`，配置免密登录。

## 端口转发

`ssh -L` 把远程的 Jupyter、TensorBoard 映射到本机浏览器。

## 文件传输

`scp`、`rsync`，上传代码、下载模型和实验结果。

## 远程挂载

`sshfs` 把远程目录挂载到本机。
