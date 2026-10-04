# 数据处理与可视化

整理实验数据，画训练曲线。示例默认已执行 `import pandas as pd` 和 `import matplotlib.pyplot as plt`。

基础条目参考：[Pandas 官方入门](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html)、[Matplotlib 官方入门](https://matplotlib.org/stable/users/explain/quick_start.html)。

## Pandas 读写

读写 CSV、JSON、Excel，查看数据的前几行和基本信息。

### 读取 CSV 并查看概要 { #pandas-read-csv }

```python
df = pd.read_csv("metrics.csv")
```

- 助记：`CSV` ← comma-separated values（逗号分隔值）；read 读取，head 看开头，info 看列类型等概要。
- 作用：需要已有 metrics.csv，路径按实际替换。
- 使用前提：本页默认已导入 pandas；读取后可用 df.head() 看前几行、df.info() 看列类型。

**解释性示例：**

```python
df = pd.read_csv("metrics.csv")
print(df.head())
df.info()
```

### 保存 CSV 时省略行索引 { #pandas-write-csv }

```python
df.to_csv("metrics-demo.csv", index=False)
```

- 助记：`to_csv` = 转成 CSV 文件；`index=False` 不把 DataFrame 的行索引写成额外一列。
- 作用：会覆盖同名文件。
- 使用前提：df 是已有 DataFrame；示例数据的构造方式放在下方解释中。

**解释性示例：**

```python
df = pd.DataFrame({"epoch": [1, 2, 3], "loss": [0.8, 0.5, 0.3]})
df.to_csv("metrics-demo.csv", index=False)
```

## 筛选与分组

按条件筛选行、选择列、`groupby` 分组统计。

### 按条件筛选行并选择列 { #pandas-filter-rows }

```python
df.loc[df["loss"] < 0.6, ["epoch", "loss"]]
```

- 助记：`loc` 用标签／布尔条件定位；方括号逗号前选行，逗号后选列。
- 使用前提：df 需包含 loss 和 epoch 列。

**解释性示例：**

```python
df = pd.DataFrame({"epoch": [1, 2, 3], "loss": [0.8, 0.5, 0.3]})
print(df.loc[df["loss"] < 0.6, ["epoch", "loss"]])
```

### 按实验名称分组计算均值 { #pandas-group-mean }

```python
df.groupby("run")["loss"].mean()
```

- 助记：`groupby` = 按某字段分组；`mean` = 均值，先分组再对每组的 loss 计算均值。
- 使用前提：df 需包含 run 和 loss 列；按 run 分组，再计算 loss 均值。

**解释性示例：**

```python
df = pd.DataFrame({"run": ["a", "a", "b"], "loss": [0.8, 0.4, 0.3]})
print(df.groupby("run")["loss"].mean())
```

## Matplotlib 基础绘图

折线图、散点图、柱状图，以及标题、坐标轴和图例。

### 绘制一条曲线 { #matplotlib-line-plot }

```python
ax.plot(epochs, losses, label="loss")
```

- 助记：`fig` = figure（整张图），`ax` = axes（绘图区）；plot 画线，label 指曲线名，legend 是图例。
- 作用：无图形界面的服务器可用下一节的保存图片示例。
- 使用前提：ax 是 plt.subplots() 创建的绘图区；epochs、losses 是长度相同的序列。显示图像与标签设置见下方示例。

**解释性示例：**

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [0.8, 0.5, 0.3], label="loss")
ax.set(xlabel="epoch", ylabel="loss", title="Training loss")
ax.legend()
plt.show()
```

## 训练曲线与子图

画 loss 和准确率曲线，多个子图排版，保存为图片。

### 保存训练曲线图片 { #matplotlib-subplots-save }

```python
fig.savefig("training-demo.png", dpi=150)
```

- 助记：`subplots` = 多个子图，`figsize` = 图尺寸；`savefig` = save figure（保存图），`dpi` = dots per inch（每英寸点数）。
- 作用：保存时覆盖同名图片；用 fig.savefig 避免保存到错误的当前图。
- 使用前提：fig 是已经画好内容的图；创建两个子图与绘制训练曲线的过程放在下方解释中。

**解释性示例：**

```python
fig, axes = plt.subplots(1, 2, figsize=(8, 3))
axes[0].plot([1, 2, 3], [0.8, 0.5, 0.3])
axes[0].set_title("Loss")
axes[1].plot([1, 2, 3], [0.6, 0.75, 0.85])
axes[1].set_title("Accuracy")
fig.tight_layout()
fig.savefig("training-demo.png", dpi=150)
plt.close(fig)
```
