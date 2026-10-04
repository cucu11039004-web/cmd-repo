# 正则表达式

Vim、rg、sed 和 Python 都会用到的正则表达式。各工具的语法略有差异，见最后一节。

基础条目参考：[Python re 官方文档](https://docs.python.org/3/library/re.html)、[ripgrep 官方指南](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md)。

## 字符与字符类

`.`、`\d`、`\w`、`\s`、`[abc]`、`[^abc]` 等匹配单个字符的写法。

### 匹配数字与空白 { #regex-character-classes }

```text
\d
\s
[a-zA-Z]
```

- 助记：`d` = digit（数字），`s` 联想 space（空白，包含空格、制表符和换行等）；`[]` 表示从括号内选一个字符。
- 作用：按 Python re 语法：\d 匹配数字，\s 匹配空白，字符类匹配一个英文字母。

## 量词

`*`、`+`、`?`、`{n,m}`，以及贪婪与非贪婪匹配。

### 匹配一个或多个数字 { #regex-digits-repeat }

```text
\d+
\d{2,4}
```

- 助记：`+` 表示前一项出现一次或更多次；`{2,4}` 给出最少和最多次数，量词作用于它前面的匹配项。
- 作用：两行分别匹配至少一个数字、连续 2 到 4 个数字。

## 锚点与边界

`^`、`$`、`\b`，匹配行首、行尾和单词边界。

### 匹配整行与完整单词 { #regex-anchors }

```text
^ERROR.*$
\bcat\b
```

- 助记：`^` 锚定开头，`$` 锚定末尾；`b` 对应 boundary（边界），`\b` 匹配位置而不是消耗一个字符。
- 作用：第一行匹配 ERROR 开头的一行；第二行按 Python re 规则匹配完整单词 cat。

## 分组与引用

捕获组、非捕获组、命名组，以及在替换中引用分组。

### 交换两个捕获组 { #regex-capture-replace }

```python
import re

result = re.sub(r"(\w+)-(\w+)", r"\2-\1", "left-right")
print(result)  # right-left
```

- 助记：`()` 捕获内容并依次编号；替换里的 `\1`、`\2` 引用第一、第二组，交换顺序就交换文本。

## 环视

前瞻和后顾：只在前后满足条件时匹配。

### 只提取等号后的整数 { #regex-lookbehind }

```python
import re

print(re.findall(r"(?<==)\d+", "id=42 count=7"))
```

- 助记：`lookbehind` = 向后看；`(?<=...)` 检查左侧是否匹配，等号被检查但不计入返回结果。
- 作用：Python re 支持这里的固定长度后顾；rg 默认引擎不支持环视，使用时需 PCRE2 支持。

## 各工具写法差异

同一个需求在 Vim、rg、sed、Python `re` 里的不同写法和转义规则。

### 在不同工具中匹配连续数字 { #regex-tool-differences }

```bash
rg '[0-9]+' data.txt
sed -E 's/[0-9]+/NUM/g' data.txt
```

- 助记：`E` = extended（扩展）；sed 的 `-E` 开启扩展正则，语法是否相同要看具体工具和引擎。
- 作用：rg 默认支持 +；sed 用 -E 开启扩展正则。Vim 可搜索 \v[0-9]+；Python 用 re.findall(r"[0-9]+", text)。
