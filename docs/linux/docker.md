# Docker

用容器跑训练环境和机器人软件，比如在 Mac 上运行 ROS 2。

以下命令要求 Docker 引擎正在运行；macOS 通常通过 Docker Desktop 或兼容运行环境提供。

基础条目参考：[Docker CLI 文档](https://docs.docker.com/reference/cli/docker/)、[Docker Compose 文档](https://docs.docker.com/reference/cli/docker/compose/)。

## 镜像

拉取、构建、查看和删除镜像。

### 拉取镜像 { #docker-pull-image }

```bash
docker pull ubuntu:24.04
```

- 助记：`pull` = 拉取，把仓库中的 image（镜像）下载到本机；冒号后是 tag（标签）。

### 列出本机镜像 { #docker-list-images }

```bash
docker image ls
```

- 助记：`image` = 镜像，`ls` = list（列出），按“对象 + 动作”读 Docker 命令。

### 用当前目录的 Dockerfile 构建镜像 { #docker-build-image }

```bash
docker build -t demo:local .
```

- 助记：`build` = 构建，`-t` = tag（标签），结尾 `.` 是构建上下文目录。

## 运行容器

`docker run` 常用参数：使用 GPU、挂载目录、映射端口、交互运行。

### 启动临时交互式容器 { #docker-run-interactive }

```bash
docker run --rm -it ubuntu:24.04 bash
```

- 助记：`run` = 启动，`--rm` = remove（退出后删除），`-i` = interactive，`-t` = tty（伪终端）。
- 作用：退出后删除容器；未挂载到主机的数据随容器删除。

### 挂载当前目录进入容器 { #docker-run-mount }

```bash
docker run --rm -it -v "$PWD:/workspace" -w /workspace ubuntu:24.04 bash
```

- 助记：`-v` = volume（挂载），冒号分隔主机路径与容器路径；`-w` = workdir（容器工作目录）。
- 作用：容器内 /workspace 的写入会修改主机当前目录。

## 进入与日志

`docker exec` 进入运行中的容器，`docker logs` 查看输出。

### 列出全部容器 { #docker-list-containers }

```bash
docker ps -a
```

- 助记：`ps` 沿用进程状态的命名习惯来列容器；`-a` = all（包含已停止容器）。

### 进入正在运行的容器 { #docker-exec-shell }

```bash
docker exec -it demo bash
```

- 助记：`exec` = execute（执行）：在已有容器中运行 bash；与 run 新建容器不同。
- 作用：demo 替换为容器名或 ID，镜像需提供 bash；否则可尝试 sh。

### 持续查看容器日志 { #docker-follow-logs }

```bash
docker logs --tail 100 -f demo
```

- 助记：`logs` = 日志；`tail` 指末尾行数，`-f` = follow（跟随新增输出）。

## 清理

删除停止的容器、无用镜像和缓存，释放磁盘空间。

### 查看 Docker 占用的磁盘空间 { #docker-disk-usage }

```bash
docker system df
```

- 助记：`df` 沿用 disk free 的命名习惯；在 Docker 中显示镜像、容器、卷与缓存的磁盘占用。
- 作用：删除容器前检查数据挂载；可用 docker rm 容器名 删除指定的已停止容器。

## Compose

用 `docker compose` 一次启动多个服务。

### 在后台启动 Compose 服务 { #docker-compose-up }

```bash
docker compose up -d
```

- 助记：`compose` = 组合多个服务；`up` 启动，`-d` = detached（后台模式）。
- 作用：在存在 compose.yaml 或兼容配置文件的目录执行。

### 查看 Compose 服务状态 { #docker-compose-status }

```bash
docker compose ps
```

- 助记：`ps` 查看 Compose 项目中的服务容器状态，与 docker ps 的查看范围不同。
