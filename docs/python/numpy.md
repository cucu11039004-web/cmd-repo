# NumPy

数组计算的常用函数。示例默认已执行 `import numpy as np`。

基础条目参考：[NumPy 官方入门](https://numpy.org/doc/stable/user/absolute_beginners.html)。

## 创建数组

`np.array`、`zeros`、`ones`、`arange`、`linspace` 等创建数组的方法。

### 从列表创建浮点数组 { #numpy-array-create }

```python
a = np.array([1, 2, 3], dtype=np.float32)
```

- 助记：`NumPy` ← Numerical Python（数值 Python）；`array` 是数组，`dtype` = data type（数据类型），float32 是 32 位浮点数。
- 使用前提：本页默认已执行 import numpy as np。

**解释性示例：**

```python
a = np.array([1, 2, 3], dtype=np.float32)
print(a)
```

### 创建全零数组和等距数列 { #numpy-zeros-linspace }

```python
np.zeros((2, 3))
np.linspace(0, 1, 5)
```

- 助记：`zeros` = 全零；`linspace` = linearly spaced（线性等距），三个参数是起点、终点、点数。
- 使用前提：两条分别创建 2×3 的全零数组、从 0 到 1 的 5 个等距数值。

**解释性示例：**

```python
zeros = np.zeros((2, 3))
steps = np.linspace(0, 1, 5)
print(zeros, steps)
```

## 形状变换

`reshape`、`transpose`、`concatenate`、`stack`、`squeeze`、`expand_dims`。

### 改变数组形状并转置 { #numpy-reshape-transpose }

```python
a.reshape(2, 3).T
```

- 助记：`arange` 可按 array range（数组序列）记；`reshape` = 重新塑形，`T` = transpose（转置）。
- 使用前提：a 是含 6 个元素的数组；先改为 2×3，再转置为 3×2。

**解释性示例：**

```python
a = np.arange(6).reshape(2, 3)
print(a.shape)  # (2, 3)
print(a.T.shape)  # (3, 2)
```

## 索引与切片

切片、布尔索引、花式索引，以及 `np.where`。

### 按条件筛选数组元素 { #numpy-boolean-index }

```python
a[a > 3]
```

- 助记：`boolean` = 布尔值；条件先生成 True / False 数组，索引只保留 True 对应的元素。
- 使用前提：a 是已有数组；先产生布尔条件，再取出满足条件的元素。

**解释性示例：**

```python
a = np.array([1, 4, 2, 8])
print(a[a > 3])  # [4, 8]
```

## 广播与运算

广播规则、矩阵乘法和 `einsum`。

### 用广播给每行加同一个向量 { #numpy-broadcast-add }

```python
a + offset
```

- 助记：`broadcast` = 广播：较小的数组按兼容维度扩展参与运算，无需手动复制每一行。
- 使用前提：a 的形状为 (2, 3)，offset 的形状为 (3,)；广播把同一偏移向量加到每一行。

**解释性示例：**

```python
a = np.zeros((2, 3))
offset = np.array([1, 2, 3])
print(a + offset)
```

### 进行矩阵乘法 { #numpy-matmul }

```python
a @ b
```

- 助记：`matmul` = matrix multiplication（矩阵乘法）；`@` 执行该运算，内侧维度必须相等。
- 作用：@ 是矩阵乘法，* 是逐元素乘法。
- 使用前提：a、b 是维度兼容的矩阵，例如 (2, 3) 与 (3, 4)，结果为 (2, 4)。

**解释性示例：**

```python
a = np.ones((2, 3))
b = np.ones((3, 4))
print((a @ b).shape)  # (2, 4)
```

## 统计与归约

`sum`、`mean`、`max`、`argmax` 等，以及 `axis` 参数的含义。

### 分别计算每列和每行的均值 { #numpy-mean-axis }

```python
a.mean(axis=0)
a.mean(axis=1)
```

- 助记：`mean` = 均值，`axis` = 轴；axis=0 沿行方向归约得到每列结果，axis=1 得到每行结果。
- 使用前提：a 是二维数组；两条分别计算每列、每行的均值。

**解释性示例：**

```python
a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.mean(axis=0))  # 每列均值
print(a.mean(axis=1))  # 每行均值
```

## 随机数

`np.random.default_rng` 生成随机数，固定随机种子。

### 使用独立随机数生成器 { #numpy-random-generator }

```python
rng = np.random.default_rng(42)
```

- 助记：`rng` ← random number generator（随机数生成器）；`normal` = 正态分布，seed（种子）决定随机序列的起点。
- 作用：同一环境中固定种子可重复生成结果；跨 NumPy 版本不保证完全相同。
- 使用前提：创建独立随机数生成器；可继续用 rng.normal(size=(2, 3)) 生成正态分布样本。

**解释性示例：**

```python
rng = np.random.default_rng(42)
print(rng.normal(size=(2, 3)))
```

## 保存与读取

`np.save`、`np.load`、`np.savez`，保存和读取数组。

### 保存并加载 NumPy 数组 { #numpy-save-load }

```python
np.save("array-demo.npy", a)
b = np.load("array-demo.npy", allow_pickle=False)
```

- 助记：`save` = 保存，`load` = 加载；`.npy` 是 NumPy 单数组文件格式。
- 作用：会覆盖同名文件；数值数组不需要开启 pickle。
- 使用前提：a 是已有数值数组；两条分别保存和读取。

**解释性示例：**

```python
a = np.arange(6)
np.save("array-demo.npy", a)
b = np.load("array-demo.npy", allow_pickle=False)
print(b)
```
