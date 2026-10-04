# PyTorch

深度学习训练中的常用写法。示例默认已执行 `import torch`。

基础条目参考：[PyTorch 官方入门](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html)、[PyTorch AMP 文档](https://docs.pytorch.org/docs/stable/amp.html)、[torchrun 文档](https://docs.pytorch.org/docs/stable/elastic/run.html)。

## 张量创建与转换

创建张量，与 NumPy 数组、Python 数值互相转换，修改数据类型。

### 创建张量并转成 Python 列表 { #torch-tensor-create }

```python
x = torch.tensor([1, 2, 3], dtype=torch.float32)
x.tolist()
```

- 助记：`tensor` = 张量，可理解成支持求导等操作的多维数组；`tolist` = 转为 Python 列表。
- 使用前提：本页默认已 import torch；两条分别创建张量和转换为列表。

**解释性示例：**

```python
x = torch.tensor([1, 2, 3], dtype=torch.float32)
print(x.tolist())
```

## 形状操作

`view`、`reshape`、`permute`、`unsqueeze`、`cat`、`stack`，以及 `einsum`。

### 改变形状并交换维度 { #torch-reshape-permute }

```python
x.reshape(2, 3).permute(1, 0)
```

- 助记：`reshape` = 改形状，`permute` = 重排维度；前者重排形状，后者交换轴的位置。
- 使用前提：x 含 6 个元素；改变形状后交换两个轴，结果形状为 (3, 2)。

**解释性示例：**

```python
x = torch.arange(6).reshape(2, 3)
print(x.shape)
print(x.permute(1, 0).shape)
```

## 设备与显存

把张量和模型放到 GPU，查看和释放显存。

### 把张量移动到指定设备 { #torch-select-device }

```python
x = x.to(device)
```

- 助记：`device` = 运算设备；`to(device)` 把张量搬到目标设备，后续计算的模型和输入也应位于兼容设备。
- 作用：这个示例只在 CUDA 与 CPU 之间选择；Mac 的 MPS 设备需单独判断。
- 使用前提：x 是已有张量，device 是目标设备；自动选择 CUDA / CPU 的写法见下方示例。

**解释性示例：**

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
x = torch.ones(2, 3).to(device)
print(x.device)
```

## 自动求导

`requires_grad`、`backward`、`torch.no_grad()`、`detach()`。

### 计算一个标量的梯度 { #torch-backward }

```python
y.backward()
```

- 助记：`requires_grad` = 需要梯度；`backward` = 反向传播，结果累积到叶子张量的 grad（梯度）中。
- 使用前提：y 是参与梯度计算的标量结果；输入张量需开启 requires_grad。

**解释性示例：**

```python
x = torch.tensor(3.0, requires_grad=True)
y = x ** 2
y.backward()
print(x.grad)  # tensor(6.)
```

### 推理时关闭梯度记录 { #torch-inference-mode }

```python
with torch.inference_mode():
    output = model(x)
```

- 助记：`inference` = 推理，`eval` = evaluation（评估）；前者关梯度记录，后者切换模型层的运行行为。
- 作用：eval 调整 Dropout / BatchNorm 等层行为，inference_mode 关闭梯度记录；两者用途不同。
- 使用前提：model 与 x 已准备好；还应调用 model.eval() 切换模型层的行为。

**解释性示例：**

```python
model = torch.nn.Linear(3, 1)
model.eval()
with torch.inference_mode():
    output = model(torch.ones(2, 3))
print(output)
```

## 模型与层

定义 `nn.Module`，统计参数量，冻结部分参数。

### 构建一个简单的前馈网络 { #torch-sequential-model }

```python
model = torch.nn.Sequential(torch.nn.Linear(3, 8), torch.nn.ReLU(), torch.nn.Linear(8, 1))
```

- 助记：`nn` = neural network（神经网络），`Sequential` = 顺序连接，`Linear` = 线性层，ReLU = rectified linear unit。
- 使用前提：三个层按顺序连接；统计参数量的写法放在下方示例。

**解释性示例：**

```python
model = torch.nn.Sequential(
    torch.nn.Linear(3, 8),
    torch.nn.ReLU(),
    torch.nn.Linear(8, 1),
)
print(sum(p.numel() for p in model.parameters()))
```

## 数据加载

`Dataset` 和 `DataLoader`，`batch_size`、`num_workers` 等常用参数。

### 按批次读取张量数据 { #torch-data-loader }

```python
loader = DataLoader(dataset, batch_size=4, shuffle=True)
```

- 助记：`TensorDataset` 把对应张量组成样本，`DataLoader` 按批加载；batch size = 每批数量，shuffle = 打乱顺序。
- 使用前提：先从 torch.utils.data 导入 DataLoader，并准备 dataset；构造数据与遍历批次见下方。

**解释性示例：**

```python
from torch.utils.data import DataLoader, TensorDataset

x = torch.randn(8, 3)
y = torch.randn(8, 1)
loader = DataLoader(TensorDataset(x, y), batch_size=4, shuffle=True)
for batch_x, batch_y in loader:
    print(batch_x.shape, batch_y.shape)
```

## 训练循环

优化器、`zero_grad`、学习率调度器和梯度裁剪。

### 根据梯度更新模型参数 { #torch-training-step }

```python
optimizer.step()
```

- 助记：zero_grad 清掉旧梯度，backward 求新梯度，step 更新参数；lr = learning rate（学习率），MSE = mean squared error（均方误差）。
- 使用前提：先创建 optimizer、清除旧梯度并执行 loss.backward()；step 只负责根据已有梯度更新参数。

**解释性示例：**

```python
model = torch.nn.Linear(3, 1)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
x, y = torch.randn(4, 3), torch.randn(4, 1)
model.train()
optimizer.zero_grad(set_to_none=True)
loss = torch.nn.functional.mse_loss(model(x), y)
loss.backward()
optimizer.step()
print(loss.item())
```

## 保存与加载

`state_dict` 保存和加载模型，断点续训的 checkpoint。

### 保存并加载模型参数 { #torch-state-dict }

```python
torch.save(model.state_dict(), "weights-demo.pt")
state = torch.load("weights-demo.pt", map_location="cpu", weights_only=True)
```

- 助记：`state_dict` = 状态字典，存参数和缓冲区；map_location 指加载位置，weights_only 限制加载的对象类型。
- 作用：需较新的 PyTorch 支持 weights_only；模型结构必须一致，只加载可信来源的权重文件。
- 使用前提：model 是已有模型；读取的 state 是参数字典，还需用同结构模型的 load_state_dict(state) 装入参数。

**解释性示例：**

```python
model = torch.nn.Linear(3, 1)
torch.save(model.state_dict(), "weights-demo.pt")
restored = torch.nn.Linear(3, 1)
state = torch.load("weights-demo.pt", map_location="cpu", weights_only=True)
restored.load_state_dict(state)
restored.eval()
```

## 混合精度与分布式

`torch.autocast` 混合精度训练，`torchrun` 启动多卡训练。

### 在支持 BF16 的 CUDA 设备上进行混合精度推理 { #torch-autocast }

```python
with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
    output = model(x)
```

- 助记：`auto` = 自动，`cast` = 类型转换；autocast 在上下文中为算子选择精度，BF16 指 bfloat16。
- 作用：需要 CUDA 和支持 BF16 的设备；这是推理示例，训练还需处理优化器和精度策略。
- 使用前提：model 与 x 需位于支持 BF16 的 CUDA 设备；完整推理示例还使用 inference_mode 关闭梯度记录。

**解释性示例：**

```python
model = torch.nn.Linear(3, 1).cuda().eval()
x = torch.randn(2, 3, device="cuda")
with torch.inference_mode(), torch.autocast(device_type="cuda", dtype=torch.bfloat16):
    output = model(x)
print(output.dtype)
```

### 在单机启动两个训练进程 { #torch-distributed-launch }

```bash
torchrun --standalone --nnodes=1 --nproc-per-node=2 train.py
```

- 助记：`nnodes` = 节点数，`nproc-per-node` = 每节点进程数，`standalone` = 单机模式；DDP 是 DistributedDataParallel。
- 作用：训练脚本需自行初始化分布式通信、选择 LOCAL_RANK 对应设备并使用 DDP；启动器不会自动改造普通脚本。

## 调试与复现

固定随机种子，检查张量形状，定位 NaN。

### 固定种子并检查非有限数值 { #torch-seed-finite }

```python
torch.manual_seed(42)
torch.isfinite(x).all()
```

- 助记：`manual_seed` = 手动设置种子；`isfinite` = 是否为有限值，NaN 和正负无穷会得到 False。
- 作用：固定种子只是复现的一部分，不保证跨平台或非确定性算子结果完全一致。
- 使用前提：x 是已有张量；两条分别固定随机种子、检查所有元素是否为有限值。

**解释性示例：**

```python
torch.manual_seed(42)
x = torch.randn(2, 3)
print(x.shape, x.dtype, torch.isfinite(x).all().item())
```
