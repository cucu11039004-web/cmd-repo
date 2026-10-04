# GPU 与 CUDA

在 Linux 服务器上查看和使用 NVIDIA 显卡。

基础条目参考：[NVIDIA nvidia-smi 文档](https://docs.nvidia.com/deploy/nvidia-smi/index.html)、[PyTorch CUDA 文档](https://docs.pytorch.org/docs/stable/cuda.html)。

## 查看显卡状态

`nvidia-smi`、`nvtop`，查看显存、利用率和占用显卡的进程。

### 查看 NVIDIA 显卡状态 { #gpu-nvidia-smi }

```bash
nvidia-smi
```

- 助记：`SMI` ← System Management Interface（系统管理接口）；工具显示显卡状态及进程信息。

### 每秒刷新一次显卡状态 { #gpu-nvidia-smi-loop }

```bash
nvidia-smi -l 1
```

- 助记：`-l` = loop（循环）；后面的 1 是刷新间隔秒数。
- 作用：ctrl + c 结束；无需额外依赖 watch。

## 指定显卡

`CUDA_VISIBLE_DEVICES`，让程序只用指定的显卡。

### 只让一次训练使用物理 GPU 1 { #gpu-visible-device }

```bash
CUDA_VISIBLE_DEVICES=1 python train.py
```

- 助记：`visible devices` = 可见设备；CUDA 是 Compute Unified Device Architecture，变量限制程序能看到哪些 CUDA 卡。
- 作用：程序内该卡通常重新编号为 cuda:0；示例脚本和物理编号按实际替换。

## 驱动与 CUDA 版本

查看驱动、CUDA 工具包和 PyTorch 对应的 CUDA 版本，排查版本不匹配。

### 查看 CUDA 编译工具包版本 { #gpu-nvcc-version }

```bash
nvcc --version
```

- 助记：`nvcc` 是 NVIDIA CUDA compiler（CUDA 编译器驱动）；它的版本属于工具包，不等于显卡驱动版本。
- 作用：nvcc 属于 CUDA 工具包；nvidia-smi 显示的 CUDA Version 表示驱动支持的版本上限。

### 查看 PyTorch 的 CUDA 支持 { #gpu-torch-cuda-check }

```bash
python -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available())"
```

- 助记：`is_available` = 是否可用；`torch.version.cuda` 是 PyTorch 构建所用 CUDA 版本，两者回答不同的问题。

## 显存排查

显存没有释放、残留进程占用显卡时的处理。

### 列出占用显卡的计算进程 { #gpu-memory-processes }

```bash
nvidia-smi --query-compute-apps=pid,process_name,used_gpu_memory --format=csv
```

- 助记：`query` = 查询；compute apps 是计算进程，`pid` 是进程编号，`used_gpu_memory` 是已用显存。
- 作用：先查 PID 对应的任务归属；多进程服务或部分平台可能无法报告完整显存信息。
