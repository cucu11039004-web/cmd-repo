# PyTorch

深度学习训练中的常用写法。示例默认已执行 `import torch`。

## 张量创建与转换

创建张量，与 NumPy 数组、Python 数值互相转换，修改数据类型。

## 形状操作

`view`、`reshape`、`permute`、`unsqueeze`、`cat`、`stack`，以及 `einsum`。

## 设备与显存

把张量和模型放到 GPU，查看和释放显存。

## 自动求导

`requires_grad`、`backward`、`torch.no_grad()`、`detach()`。

## 模型与层

定义 `nn.Module`，统计参数量，冻结部分参数。

## 数据加载

`Dataset` 和 `DataLoader`，`batch_size`、`num_workers` 等常用参数。

## 训练循环

优化器、`zero_grad`、学习率调度器和梯度裁剪。

## 保存与加载

`state_dict` 保存和加载模型，断点续训的 checkpoint。

## 混合精度与分布式

`torch.autocast` 混合精度训练，`torchrun` 启动多卡训练。

## 调试与复现

固定随机种子，检查张量形状，定位 NaN。
