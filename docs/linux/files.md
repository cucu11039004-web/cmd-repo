# 文件与目录

以下命令也适用于 macOS 的 zsh / bash。既有示例的来源表示建站演示，不代表你的学习经历。

基础条目参考：[GNU Coreutils 手册](https://www.gnu.org/software/coreutils/manual/coreutils.html)、[GNU tar 手册](https://www.gnu.org/software/tar/manual/tar.html)。

## 浏览与定位

确认当前位置，列出目录内容。

### 查看当前所在目录 { #pwd }

```bash
pwd
```

- 助记：`pwd` ← print working directory（打印工作目录）：working directory 就是当前终端所在目录。
- 作用：显示当前工作目录的完整路径。
- 遇到场景：运行项目命令前，确认终端所在的目录。
- 来源：[GNU Coreutils：pwd](https://www.gnu.org/s/coreutils/manual/html_node/pwd-invocation.html)。

### 查看目录里的全部文件 { #ls-all }

```bash
ls -la
```

- 助记：`ls` ← list（列出）；`-l` = long（详细格式），`-a` = all（包括隐藏文件）。
- 作用：以详细列表显示当前目录内容，包括以点开头的隐藏文件。
- 遇到场景：想确认项目里有没有 `.gitignore`，或查看文件权限。
- 来源：命令速查表建站示例。

### 返回上一个工作目录 { #files-cd-previous }

```bash
cd -
```

- 助记：`cd` ← change directory（切换目录）；参数 `-` 表示上一次的工作目录，而不是父目录。

## 查找文件

按名称、类型、大小或修改时间找到文件。

### 按名称查找 Markdown 文件 { #find-markdown }

```bash
find . -type f -name '*.md'
```

- 助记：`find` = 查找；`-type f` 中 f 是 file（文件），`-name` 按名字筛选，`*.md` 是文件名模式。
- 作用：从当前目录向下查找所有以 `.md` 结尾的文件；引号让通配符交给 `find` 处理。
- 遇到场景：文档分散在多个子目录，不知道某篇笔记放在哪里。
- 来源：命令速查表建站示例。

### 查找大于 100 MiB 的文件 { #files-find-large }

```bash
find . -type f -size +100M
```

- 助记：`find` = 查找；`-size` 是大小，`+100M` 表示大于 100 MiB，`+` 是超过的意思。
- 作用：常用于定位大日志、数据文件和模型权重。

## 复制、移动与删除

`cp`、`mv`、`rm`、`mkdir` 等文件操作，以及防止误删的写法。

### 创建多层目录 { #files-mkdir-parents }

```bash
mkdir -p experiments/run01
```

- 助记：`mkdir` ← make directory（创建目录）；`-p` 对应 parents（父目录），缺少的上层目录一起创建。

### 复制目录并保留属性 { #files-copy-directory }

```bash
cp -a data data-backup
```

- 助记：`cp` ← copy（复制）；`-a` = archive（归档模式），递归复制并尽量保留属性。
- 作用：目标不存在时得到完整副本；目标已存在时可能在其下新建子目录。

### 移动或重命名文件 { #files-move-interactive }

```bash
mv -i old.txt new.txt
```

- 助记：`mv` ← move（移动）；同一目录中换名字就是重命名，`-i` = interactive（交互确认）。
- 作用：若目标已存在，-i 会询问是否覆盖。

### 确认后删除单个文件 { #files-remove-interactive }

```bash
rm -i old.txt
```

- 助记：`rm` ← remove（移除）；`-i` = interactive（交互），所以删除前先问一次。
- 作用：删除通常无法从回收站恢复；-i 在删除前确认。

## 链接

软链接和硬链接，比如把数据集目录链接到项目里。

### 为数据目录建立软链接 { #files-symlink }

```bash
ln -s "$HOME/datasets" ./datasets
```

- 助记：`ln` ← link（链接）；`-s` = symbolic（符号链接），保存的是指向目标的路径。
- 作用：示例目标为绝对路径；删除软链接不会删除目标目录。

## 权限与所有者

`chmod`、`chown`，以及权限不足时的排查。

### 给脚本添加执行权限 { #files-chmod-executable }

```bash
chmod u+x run.sh
```

- 助记：`chmod` ← change mode（改变权限模式）；`u` = user（所有者），`+x` = 增加 execute（执行）权限。
- 作用：仅给文件所有者添加执行权限。

## 压缩与归档

`tar`、`zip`、`unzip` 打包和解压，包括数据集和模型权重。

### 打包目录为 gzip 归档 { #files-tar-create }

```bash
tar -czf data.tar.gz data/
```

- 助记：`tar` ← tape archiver（磁带归档工具）；`c` = create（创建），`z` = gzip 压缩，`f` = file（后接归档文件名）。

### 先查看归档内容再解压 { #files-tar-extract }

```bash
tar -tzf data.tar.gz
mkdir -p extracted
tar -xzf data.tar.gz -C extracted
```

- 助记：`t` = list（列目录），`x` = extract（提取），`z` = gzip，`f` = file；`-C` 先切换到指定目录再解压。
- 作用：先检查路径，再解压到单独目录。
