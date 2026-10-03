# GPU 与 CUDA

在 Linux 服务器上查看和使用 NVIDIA 显卡。

## 查看显卡状态

`nvidia-smi`、`nvtop`，查看显存、利用率和占用显卡的进程。

## 指定显卡

`CUDA_VISIBLE_DEVICES`，让程序只用指定的显卡。

## 驱动与 CUDA 版本

查看驱动、CUDA 工具包和 PyTorch 对应的 CUDA 版本，排查版本不匹配。

## 显存排查

显存没有释放、残留进程占用显卡时的处理。
