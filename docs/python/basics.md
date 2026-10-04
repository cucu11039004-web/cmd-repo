# Python 常用写法

写脚本和工具函数时常用的语法与标准库。

基础条目参考：[Python 官方教程](https://docs.python.org/3/tutorial/)、[Python 标准库](https://docs.python.org/3/library/)。

## 字符串与格式化

f-string 格式化数字、对齐和日期，常用的字符串方法。

### 格式化浮点数和编号 { #python-fstring }

```python
print(f"step={step:04d}, loss={loss:.4f}")
```

- 助记：f-string = formatted string（格式化字符串）；`.4f` 表示小数点后 4 位，`04d` 表示整数宽度 4、用 0 补齐。
- 使用前提：step 是整数编号，loss 是浮点数。

**解释性示例：**

```python
loss = 0.123456
step = 7
print(f"step={step:04d}, loss={loss:.4f}")
```

## 容器与推导式

列表、字典、集合的推导式，以及 `enumerate`、`zip`、`sorted` 等常用内置函数。

### 筛选并转换列表 { #python-list-comprehension }

```python
squares = [x * x for x in values if x % 2 == 0]
```

- 助记：`for` 给出遍历来源，`if` 给出筛选条件，最前面的表达式决定放进新列表的值。
- 使用前提：values 是已有的数字列表；表达式先筛选偶数，再计算平方。

**解释性示例：**

```python
values = [1, 2, 3, 4]
squares = [x * x for x in values if x % 2 == 0]
print(squares)
```

### 给列表元素配上序号 { #python-enumerate }

```python
enumerate(names, start=1)
```

- 助记：`enumerate` = 枚举／编号；函数同时返回 index（序号）和当前元素，start 指起始序号。
- 使用前提：names 是已有列表；返回可遍历的“序号、元素”对，循环写法见下方示例。

**解释性示例：**

```python
names = ["camera", "motor"]
for index, name in enumerate(names, start=1):
    print(index, name)
```

## 文件与路径

`pathlib` 处理路径，`open` 读写文本，`json` 读写配置。

### 读取和写入 UTF-8 文本 { #python-pathlib-text }

```python
path.read_text(encoding="utf-8")
path.write_text("hello\n", encoding="utf-8")
```

- 助记：`pathlib` = path（路径）+ library（库）的功能联想；read / write 是读／写，text 表示按文本处理。
- 作用：写入会覆盖同名文件；示例使用独立文件名。
- 使用前提：先用 pathlib.Path 创建 path；这两条分别为读取和写入，写入会覆盖文件内容。

**解释性示例：**

```python
from pathlib import Path

path = Path("notes-demo.txt")
path.write_text("hello\n", encoding="utf-8")
print(path.read_text(encoding="utf-8"))
```

### 把字典转换为 JSON 再读回 { #python-json-roundtrip }

```python
text = json.dumps(config, ensure_ascii=False, indent=2)
restored = json.loads(text)
```

- 助记：`JSON` ← JavaScript Object Notation（JavaScript 对象表示法）；dumps 转字符串，loads 从字符串加载，末尾 s 表示 string。
- 使用前提：先 import json，config 是已有字典；两条分别编码为字符串、从字符串解码。

**解释性示例：**

```python
import json

config = {"name": "实验", "epochs": 10}
text = json.dumps(config, ensure_ascii=False, indent=2)
restored = json.loads(text)
print(restored)
```

## 命令行参数

用 `argparse` 给脚本加参数。

### 声明一个可选参数 { #python-argparse }

```python
parser.add_argument("--epochs", type=int, default=10)
```

- 助记：`argparse` = argument parsing（参数解析）；`type` 指转换类型，`default` 指未传参数时的默认值。
- 作用：保存为脚本后用 python 脚本名.py --epochs 20 运行。
- 使用前提：parser 是 argparse.ArgumentParser() 创建的解析器；声明参数后调用 parse_args() 读取命令行。

**解释性示例：**

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--epochs", type=int, default=10)
args = parser.parse_args()
print(args.epochs)
```

## 日志与调试

`logging` 输出日志，`breakpoint()` 和 `pdb` 断点调试。

### 输出带时间的日志 { #python-logging }

```python
logging.info("训练开始，epoch=%s", 1)
```

- 助记：`logging` = 记录日志；INFO 是信息级别，`%(asctime)s` 代表格式化时间。
- 使用前提：先 import logging 并配置日志级别；时间格式通过 basicConfig 设置，见下方示例。

**解释性示例：**

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logging.info("训练开始，epoch=%s", 1)
```

## 类型与数据类

类型注解和 `dataclass`，用来写配置类。

### 创建数据类配置 { #python-dataclass }

```python
config = Config(epochs=20)
```

- 助记：`dataclass` = data class（数据类）；按字段生成初始化等方法，适合表达配置数据。
- 使用前提：Config 是用 dataclass 声明的数据类；字段声明与自动生成初始化方法的写法见下方。

**解释性示例：**

```python
from dataclasses import dataclass

@dataclass
class Config:
    epochs: int = 10
    learning_rate: float = 1e-3

print(Config(epochs=20))
```

## 子进程与并发

`subprocess` 调用外部命令，`multiprocessing` 和 `concurrent.futures` 并行处理。

### 调用子进程并检查是否成功 { #python-subprocess }

```python
result = subprocess.run([sys.executable, "--version"], check=True, capture_output=True, text=True)
```

- 助记：`subprocess` = 子进程；`check` 检查退出码，`capture_output` 捕获输出，`text` 让输出以字符串返回。
- 作用：参数列表避免 shell 转义问题；非零退出码会抛出异常。
- 使用前提：先 import subprocess 和 sys；返回值 result 中包含退出码与捕获的输出。

**解释性示例：**

```python
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "--version"],
    check=True, capture_output=True, text=True,
)
print(result.stdout.strip())
```
