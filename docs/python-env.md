# Python 环境

以下命令适用于 macOS / Linux 的 zsh 或 bash，在项目目录中执行。

### 给项目创建独立的 Python 环境

```bash
python3 -m venv .venv
```

- 作用：在当前目录创建 `.venv`，把这个项目的 Python 依赖与系统环境隔离。
- 遇到场景：开始新项目，需要安装依赖，又不想影响其他项目。
- 来源：命令速查表建站示例。

### 激活项目的虚拟环境

```bash
source .venv/bin/activate
```

- 作用：让当前终端优先使用 `.venv` 里的 Python 和工具；执行 `deactivate` 可以退出。
- 遇到场景：重新打开终端后，需要继续运行项目或安装依赖。
- 来源：命令速查表建站示例。
