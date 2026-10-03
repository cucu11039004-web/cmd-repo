# Python 环境

以下命令适用于 macOS / Linux 的 zsh 或 bash，在项目目录中执行。

## .venv

需要已安装 Python 3。这一组用 Python 自带的 `venv` 创建环境，再用 pip 安装依赖。

### 给项目创建独立的 Python 环境 { #venv-create }

```bash
python3 -m venv .venv
```

- 作用：在当前目录创建 `.venv`，把这个项目的 Python 依赖与系统环境隔离。
- 遇到场景：开始新项目，需要安装依赖，又不想影响其他项目。
- 来源：命令速查表建站示例。

### 激活项目的虚拟环境 { #venv-activate }

```bash
source .venv/bin/activate
```

- 作用：让当前终端优先使用 `.venv` 里的 Python 和工具；执行 `deactivate` 可以退出。
- 遇到场景：重新打开终端后，需要继续运行项目或安装依赖。
- 来源：命令速查表建站示例。

### 退出当前虚拟环境 { #venv-deactivate }

```bash
deactivate
```

- 作用：撤销当前终端的虚拟环境激活状态，不删除 `.venv` 或其中的依赖。
- 遇到场景：已经用 `source .venv/bin/activate` 激活环境，现在要切回原来的终端环境。
- 来源：[Python 官方文档：venv](https://docs.python.org/3/library/venv.html)。

### 安装项目列出的依赖 { #venv-install }

```bash
python -m pip install -r requirements.txt
```

- 作用：用当前 Python 对应的 pip 安装依赖文件中的包。
- 遇到场景：项目存在 `requirements.txt`，创建并激活 `.venv` 后，需要准备运行环境。
- 来源：[Python 官方文档：venv](https://docs.python.org/3/library/venv.html)。

## Conda

需要已安装 Conda，并已初始化当前 shell。以下 `demo` 是环境名示例；Python 3.12 是指定版本示例，可按项目要求替换。

### 创建指定 Python 版本的环境 { #conda-create }

```bash
conda create -n demo python=3.12
```

- 作用：创建名为 `demo` 的独立环境，并安装 Python 3.12。
- 遇到场景：项目要求特定 Python 版本，希望用命名环境管理依赖。
- 来源：[Conda 官方文档：管理环境](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html)。

### 激活一个 Conda 环境 { #conda-activate }

```bash
conda activate demo
```

- 作用：让当前终端使用 `demo` 环境中的 Python 和工具。
- 遇到场景：环境已创建，开始运行项目或安装依赖；把 `demo` 换成实际环境名。
- 来源：[Conda 官方文档：管理环境](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html)。

### 退出当前 Conda 环境 { #conda-deactivate }

```bash
conda deactivate
```

- 作用：退出当前 Conda 激活层，恢复之前的环境。
- 遇到场景：完成当前环境的工作后退出；如果只想回到 `base`，可用 `conda activate base`。
- 来源：[Conda 官方文档：管理环境](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html)。

### 列出已有的 Conda 环境 { #conda-list }

```bash
conda env list
```

- 作用：显示已有环境的名称和位置，星号标出当前激活的环境。
- 遇到场景：忘记环境名，或想确认当前正在用哪个环境。
- 来源：[Conda 官方文档：管理环境](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html)。

## uv

需要已安装 uv。以下使用 uv 的项目模式：先初始化或进入已有的 uv 项目，依赖记录在 `pyproject.toml`，项目环境默认位于 `.venv`。uv 会在同步或运行时管理环境，通常不用手动激活。

### 初始化一个 uv 项目 { #uv-init }

```bash
uv init
```

- 作用：在当前目录初始化项目，生成 `pyproject.toml` 等项目文件。
- 遇到场景：开始一个由 uv 管理的新项目，在准备好的项目目录中执行。
- 来源：[uv 官方文档：项目指南](https://docs.astral.sh/uv/guides/projects/)。

### 添加项目依赖 { #uv-add }

```bash
uv add requests
```

- 作用：将 `requests` 加入项目依赖，并更新锁文件和项目环境。
- 遇到场景：已有 uv 项目需要使用新的库；把 `requests` 换成实际包名。
- 来源：[uv 官方文档：项目指南](https://docs.astral.sh/uv/guides/projects/)。

### 同步 uv 项目的环境 { #uv-sync }

```bash
uv sync
```

- 作用：根据项目依赖与锁文件同步 `.venv`，不存在时自动创建；默认移除未声明的额外包。
- 遇到场景：进入已有 uv 项目，或项目依赖发生变化，需要准备对应的环境。
- 来源：[uv 官方文档：uv sync](https://docs.astral.sh/uv/reference/cli/#uv-sync)。

### 用项目环境运行 Python { #uv-run }

```bash
uv run python --version
```

- 作用：同步项目环境后，在其中运行 Python 并显示版本。
- 遇到场景：已有 uv 项目，不想手动激活环境；运行脚本时可改用 `uv run python 脚本名.py`。
- 来源：[uv 官方文档：运行命令](https://docs.astral.sh/uv/concepts/projects/run/)。

## pip 与镜像源

查看和导出已安装的包，配置国内镜像源加速下载。

## Jupyter 内核

把虚拟环境或 Conda 环境注册为 Jupyter 内核，在 Notebook 里切换使用。
