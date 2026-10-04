# Markdown

写博客和这份速查表用到的 Markdown 语法。扩展语法以本站使用的 MkDocs Material 为准，其他平台可能不支持。

基础条目参考：[CommonMark 规范](https://spec.commonmark.org/0.31.2/)、[Material 提示框](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)、[Material 数学公式](https://squidfunk.github.io/mkdocs-material/reference/math/)。

## 基础语法

标题、段落、列表、强调、引用和分割线。

### 写标题和列表 { #markdown-headings-lists }

```text
# 一级标题

## 二级标题

- 第一项
- 第二项

1. 第一步
2. 第二步
```

- 助记：`#` 的数量对应标题层级；`-` 是无序列表标记，`1.` 是有序步骤标记。

### 写强调和引用 { #markdown-emphasis-quote }

```text
**加粗**，*斜体*

> 引用内容
```

- 助记：单个 `*` 表示 emphasis（强调），成对 `**` 表示更强的强调；`>` 把文字标成引用。

## 链接与图片

内部链接、外部链接、锚点链接和图片。

### 插入链接和图片 { #markdown-link-image }

```text
[文件与目录](../linux/files.md)

![图片说明](../images/example.png)
```

- 助记：`[显示文字](目标)` 是链接；前面加 `!` 就变成图片嵌入，括号里的仍是路径或地址。
- 作用：图片路径是写法示例，需要先放入真实图片；本站内部链接使用相对路径。

## 代码块

行内代码、带语言标注的代码块，以及代码块里包含反引号时的写法。

### 写带语言的代码块 { #markdown-fenced-code }

````text
```bash
ls -la
```
````

- 助记：`fence` 是围栏：用反引号围住代码；开头的 `bash` 指定语法高亮语言，不会执行代码。
- 作用：行内代码用单对反引号；展示含三反引号的内容时，外层围栏用四个反引号。

## 表格

表格写法和对齐方式。

### 写带对齐的表格 { #markdown-table }

```text
| 命令 | 作用 | 次数 |
| :--- | :--- | ---: |
| pwd | 当前目录 | 1 |
```

- 助记：`|` 分隔列；对齐行中的 `:` 放左边就左对齐，放右边就右对齐，两边都有就居中。
- 作用：本站支持表格；冒号控制列的左、右或居中对齐。

## 数学公式

行内公式和独立公式的 LaTeX 写法。

### 记录行内和独立公式 { #markdown-math }

```text
$E = mc^2$

$$
y = wx + b
$$
```

- 助记：单对 `$` 标记 inline（行内）公式，双对 `$$` 标记独立公式；渲染需要数学扩展。
- 作用：这是数学扩展写法；本站当前未配置数学扩展和 MathJax / KaTeX，因此不能直接渲染成公式。

## 扩展语法

提示框（admonition）、固定锚点（attr_list）、图表等扩展。

### 添加提示框 { #markdown-admonition }

```text
!!! note "提示"
    这里写提示内容，正文缩进四个空格。
```

- 助记：`admonition` 是提示／告诫；`note` 指提示类型，缩进告诉解析器哪些正文属于这个提示框。
- 作用：本站已启用 admonition；固定标题锚点写法可参考现有条目的 { #tool-action }。
