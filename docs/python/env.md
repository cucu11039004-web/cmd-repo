# Python 环境

以下命令适用于 macOS / Linux 的 zsh 或 bash，在项目目录中执行。

基础条目参考：[pip 官方文档](https://pip.pypa.io/en/stable/cli/pip/)、[IPython 内核安装文档](https://ipython.readthedocs.io/en/stable/install/kernel_install.html)。

## .venv

需要已安装 Python 3。这一组用 Python 自带的 `venv` 创建环境，再用 pip 安装依赖。

### 给项目创建独立的 Python 环境 { #venv-create }

```bash
python3 -m venv .venv
```

- 助记：`venv` ← virtual environment（虚拟环境）；`-m` = module（模块），让 Python 运行自带的 venv 模块。
- 作用：在当前目录创建 `.venv`，把这个项目的 Python 依赖与系统环境隔离。
- 遇到场景：开始新项目，需要安装依赖，又不想影响其他项目。
- 来源：命令速查表建站示例。

### 激活项目的虚拟环境 { #venv-activate }

```bash
source .venv/bin/activate
```

- 助记：`activate` = 激活；`source` 在当前 shell 执行脚本，所以当前终端的 PATH 才会改变。
- 作用：让当前终端优先使用 `.venv` 里的 Python 和工具；执行 `deactivate` 可以退出。
- 遇到场景：重新打开终端后，需要继续运行项目或安装依赖。
- 来源：命令速查表建站示例。

### 退出当前虚拟环境 { #venv-deactivate }

```bash
deactivate
```

- 助记：`de-` 有撤销的含义；deactivate = 取消激活，只退出环境，不删除环境目录。
- 作用：撤销当前终端的虚拟环境激活状态，不删除 `.venv` 或其中的依赖。
- 遇到场景：已经用 `source .venv/bin/activate` 激活环境，现在要切回原来的终端环境。
- 来源：[Python 官方文档：venv](https://docs.python.org/3/library/venv.html)。

### 安装项目列出的依赖 { #venv-install }

```bash
python -m pip install -r requirements.txt
```

- 助记：`pip` 是 Python 包安装工具名；install 是安装，`-r` 读取 requirements（依赖要求）文件。
- 作用：用当前 Python 对应的 pip 安装依赖文件中的包。
- 遇到场景：项目存在 `requirements.txt`，创建并激活 `.venv` 后，需要准备运行环境。
- 来源：[Python 官方文档：venv](https://docs.python.org/3/library/venv.html)。

## Conda

需要已安装 Conda，并已初始化当前 shell。以下 `demo` 是环境名示例；Python 3.12 是指定版本示例，可按项目要求替换。

### 创建指定 Python 版本的环境 { #conda-create }

```bash
conda create -n demo python=3.12
```

- 助记：`create` = 创建，`-n` = name（环境名称）；`python=3.12` 指定要装的解释器版本。
- 作用：创建名为 `demo` 的独立环境，并安装 Python 3.12。
- 遇到场景：项目要求特定 Python 版本，希望用命名环境管理依赖。
- 来源：[Conda 官方文档：管理环境](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html)。

### 激活一个 Conda 环境 { #conda-activate }

```bash
conda activate demo
```

- 助记：`activate` = 激活，后面直接写环境名；不是文件系统路径。
- 作用：让当前终端使用 `demo` 环境中的 Python 和工具。
- 遇到场景：环境已创建，开始运行项目或安装依赖；把 `demo` 换成实际环境名。
- 来源：[Conda 官方文档：管理环境](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html)。

### 退出当前 Conda 环境 { #conda-deactivate }

```bash
conda deactivate
```

- 助记：`deactivate` = 取消激活；Conda 与 venv 虽然名称相似，但由各自的工具管理。
- 作用：退出当前 Conda 激活层，恢复之前的环境。
- 遇到场景：完成当前环境的工作后退出；如果只想回到 `base`，可用 `conda activate base`。
- 来源：[Conda 官方文档：管理环境](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html)。

### 列出已有的 Conda 环境 { #conda-list }

```bash
conda env list
```

- 助记：`env` ← environment（环境），`list` = 列出；`env list` 读作“列出环境”。
- 作用：显示已有环境的名称和位置，星号标出当前激活的环境。
- 遇到场景：忘记环境名，或想确认当前正在用哪个环境。
- 来源：[Conda 官方文档：管理环境](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html)。

## uv

需要已安装 uv。以下使用 uv 的项目模式：先初始化或进入已有的 uv 项目，依赖记录在 `pyproject.toml`，项目环境默认位于 `.venv`。uv 会在同步或运行时管理环境，通常不用手动激活。

### 初始化一个 uv 项目 { #uv-init }

```bash
uv init
```

- 助记：`init` ← initialize（初始化）；uv 是工具名，不强行解释成单词首字母缩写。
- 作用：在当前目录初始化项目，生成 `pyproject.toml` 等项目文件。
- 遇到场景：开始一个由 uv 管理的新项目，在准备好的项目目录中执行。
- 来源：[uv 官方文档：项目指南](https://docs.astral.sh/uv/guides/projects/)。

### 添加项目依赖 { #uv-add }

```bash
uv add requests
```

- 助记：`add` = 添加，把包加入项目声明的依赖，之后可由项目配置重建环境。
- 作用：将 `requests` 加入项目依赖，并更新锁文件和项目环境。
- 遇到场景：已有 uv 项目需要使用新的库；把 `requests` 换成实际包名。
- 来源：[uv 官方文档：项目指南](https://docs.astral.sh/uv/guides/projects/)。

### 同步 uv 项目的环境 { #uv-sync }

```bash
uv sync
```

- 助记：`sync` ← synchronize（同步），让实际安装的环境与项目声明／锁文件一致。
- 作用：根据项目依赖与锁文件同步 `.venv`，不存在时自动创建；默认移除未声明的额外包。
- 遇到场景：进入已有 uv 项目，或项目依赖发生变化，需要准备对应的环境。
- 来源：[uv 官方文档：uv sync](https://docs.astral.sh/uv/reference/cli/#uv-sync)。

### 用项目环境运行 Python { #uv-run }

```bash
uv run python --version
```

- 助记：`run` = 运行；uv 先准备项目环境，再把后面的命令放到该环境中执行。
- 作用：同步项目环境后，在其中运行 Python 并显示版本。
- 遇到场景：已有 uv 项目，不想手动激活环境；运行脚本时可改用 `uv run python 脚本名.py`。
- 来源：[uv 官方文档：运行命令](https://docs.astral.sh/uv/concepts/projects/run/)。

## pip 与镜像源

查看和导出已安装的包，配置国内镜像源加速下载。

### 查看 Python 解释器的实际路径 { #python-interpreter-path }

```bash
python -c "import sys; print(sys.executable)"
```

- 助记：`sys` ← system（系统），`executable` = 可执行程序；这个属性告诉你当前到底用了哪个 Python。

### 列出当前环境的依赖 { #pip-list-packages }

```bash
python -m pip list
```

- 助记：`list` = 列出；`python -m pip` 指定“当前这个 Python 对应的 pip”，减少装错环境的机会。

### 导出当前环境的依赖版本 { #pip-freeze-requirements }

```bash
python -m pip freeze > requirements-snapshot.txt
```

- 助记：`freeze` = 冻结；这里是把当前已安装版本记成固定版本文本，不是锁住环境禁止修改。
- 作用：导出整个环境，包含间接依赖；不会覆盖项目现有 requirements.txt。

### 检查已安装依赖是否冲突 { #pip-check-dependencies }

```bash
python -m pip check
```

- 助记：`check` = 检查；pip 对照各包声明的依赖关系检查已安装版本是否兼容。

### 只为一次安装指定包索引 { #pip-index-once }

```bash
python -m pip install --index-url https://pypi.org/simple requests
```

- 助记：`index` = 索引，`URL` 是资源地址；index-url 指定到哪个包索引查找，而不是程序运行时的代理。
- 作用：示例使用官方 PyPI；按需要替换为可信镜像地址，不修改全局配置。

## Jupyter 内核

把虚拟环境或 Conda 环境注册为 Jupyter 内核，在 Notebook 里切换使用。

### 把当前环境注册成 Notebook 内核 { #jupyter-register-kernel }

```bash
python -m ipykernel install --user --name demo --display-name "Python (demo)"
```

- 助记：`kernel` 是 Notebook 执行代码的内核；`--name` 是内部名，`--display-name` 是界面显示名，`--user` 只给当前用户注册。
- 作用：在目标虚拟环境内执行；之后在 Jupyter 选择 Python (demo)，内核名按项目替换。
- 使用前提：在目标环境中先用 python -m pip install ipykernel 安装内核依赖。

**解释性示例：**

```bash
python -m pip install ipykernel
python -m ipykernel install --user --name demo --display-name "Python (demo)"
```
