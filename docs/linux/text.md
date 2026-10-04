# 文本处理

以下命令也适用于 macOS 的 zsh / bash。`rg` 需要安装 ripgrep。

基础条目参考：[ripgrep 官方指南](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md)、[jq 官方手册](https://jqlang.org/manual/)、[GNU Coreutils 手册](https://www.gnu.org/software/coreutils/manual/coreutils.html)、[GNU Awk 手册](https://www.gnu.org/software/gawk/manual/gawk.html)。

## 查看文件

`cat`、`less`、`head`、`tail -f`，查看配置文件和训练日志。

### 分页查看长文件 { #text-less }

```bash
less train.log
```

- 助记：`less` 是分页查看器；名字与早期分页工具 more 呼应，可按“分屏阅读”记用途。
- 作用：按 / 搜索，按 q 退出。

### 持续查看日志末尾 { #text-tail-follow }

```bash
tail -n 50 -f train.log
```

- 助记：`tail` = 尾部；`-n` = number（行数），`-f` = follow（跟随），所以先看末尾再等新内容。
- 作用：先显示最后 50 行，再跟随新内容；ctrl + c 结束。

## 搜索文本

在文件或项目里搜索关键词。

### 搜索项目里的文本 { #rg-text }

```bash
rg '关键词' .
```

- 助记：`rg` 是 ripgrep 的命令名；它递归搜索文本，先记“在项目中找匹配行”。
- 作用：递归搜索当前目录中的文本，显示匹配的文件和内容；默认跳过隐藏文件和被忽略的文件。
- 遇到场景：查找某个配置项或报错信息出现在哪个文件中；把 `关键词` 换成要搜索的文本，搜索纯文本时可加 `-F`。
- 来源：[ripgrep 官方指南](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md)。

### 按字面文本搜索并显示行号 { #text-rg-fixed }

```bash
rg -n -F 'CUDA out of memory' .
```

- 助记：`-n` 对应 line number（行号），`-F` = fixed strings（固定字符串），不把内容当正则解释。
- 作用：-F 不把输入当正则表达式。

### 只列出包含关键词的 Python 文件 { #text-rg-files-match }

```bash
rg -l -g '*.py' 'import torch' .
```

- 助记：`-l` 是 files with matches（只列匹配文件名），`-g` = glob（文件名筛选模式）。

## 替换与提取

`sed`、`awk`、`cut`，批量替换文本或取出某一列。

### 预览全文替换结果 { #text-sed-preview }

```bash
sed 's/old/new/g' config.txt
```

- 助记：`sed` ← stream editor（流编辑器）；`s/old/new/g` 中 s 是 substitute（替换），g 是 global（每行所有匹配）。
- 作用：只把替换结果输出到终端，不改原文件。

### 提取空白分隔的第一列 { #text-awk-column }

```bash
awk '{print $1}' data.txt
```

- 助记：`awk` 来自作者 Aho、Weinberger、Kernighan 的姓氏首字母；`$1` 是第一字段，`print` 是打印。

## 排序与统计

`sort`、`uniq`、`wc`，统计行数、去重和计数。

### 统计文件行数 { #text-line-count }

```bash
wc -l data.txt
```

- 助记：`wc` ← word count（词数统计）；`-l` = lines（行数），这个选项让它数行。

### 统计每行内容出现次数 { #text-sort-count }

```bash
sort labels.txt | uniq -c | sort -nr
```

- 助记：`sort` = 排序，`uniq` = unique（合并相邻重复项）；`-c` = count（计数），`-n` 数值排序，`-r` 反向。
- 作用：先排序让相同记录相邻，按出现次数降序排列。

## 批量处理

`xargs`、`tee` 和管道组合，把一条命令的结果交给下一条处理。

### 显示输出并同时保存日志 { #text-tee-log }

```bash
python train.py 2>&1 | tee train.log
```

- 助记：`tee` 名称联想 T 形管接头：输出分成两路，一路到屏幕，一路到文件。
- 作用：tee 默认覆盖文件；追加可用 tee -a。上游退出码需结合 shell 的 pipefail 判断。

## JSON 处理

用 `jq` 查看和提取 JSON，比如接口返回值和配置文件。

### 格式化查看 JSON { #text-jq-format }

```bash
jq '.' config.json
```

- 助记：`jq` 是 JSON 处理工具名；过滤器 `.` 代表整个输入，把它原样输出并格式化。

### 提取数组中每项的名字 { #text-jq-names }

```bash
jq -r '.items[].name' response.json
```

- 助记：`.items` 取字段，`[]` 遍历数组，`.name` 取每项的名字；`-r` = raw output（直接输出字符串）。
- 作用：示例要求顶层有 items 数组，每项有 name 字段；-r 输出不带引号的字符串。
