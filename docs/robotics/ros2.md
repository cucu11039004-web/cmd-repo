# ROS 2

这里只做记录，Mac 上不需要安装 ROS 2：命令在机械臂工控机、Ubuntu 主机或 [Docker](../linux/docker.md) 容器里执行。

示例以 ROS 2 Jazzy 的基础 CLI 为准；用前先在每个终端加载环境。未注明的节点、话题与坐标系名称均为示例，需按实际系统替换。

基础条目参考：[ROS 2 官方话题教程源码](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.rst)、[ROS 2 官方参数教程源码](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.rst)、[ROS 2 官方录包教程源码](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.rst)。

## 环境与工作空间

`source` 环境脚本，用 `colcon build` 编译工作空间。

### 加载 ROS 2 环境 { #ros2-source-environment }

```bash
source /opt/ros/jazzy/setup.bash
```

- 助记：`ROS` ← Robot Operating System（机器人操作系统）；setup 准备环境，source 让设置在当前 shell 生效。
- 作用：以 Ubuntu + bash + Jazzy 为例；发行版目录按安装情况替换，zsh 使用 setup.zsh。

### 编译并加载当前工作空间 { #ros2-colcon-build }

```bash
colcon build --symlink-install
source install/setup.bash
```

- 助记：`colcon` 名称来自 [collective construction](https://colcon.readthedocs.io/en/released/)（统一构建）；build 编译，symlink-install 用符号链接安装部分产物。
- 作用：在含 src/ 的工作空间根目录执行，先加载 ROS 2 基础环境；编译成功后再 source。

## 节点与话题

查看节点和话题，打印话题内容，查看发布频率。

### 列出节点 { #ros2-node-list }

```bash
ros2 node list
```

- 助记：`node` = 节点，`list` = 列出；一个节点代表 ROS 图中的一个计算参与者。

### 列出话题及消息类型 { #ros2-topic-list }

```bash
ros2 topic list -t
```

- 助记：`topic` = 话题，`-t` = show types（显示类型）；话题名是通道名，消息类型决定字段结构。

### 打印话题消息 { #ros2-topic-echo }

```bash
ros2 topic echo /chatter
```

- 助记：`echo` = 回显；把订阅到的消息打印出来，通常持续运行直到 ctrl + c。
- 作用：需已有发布者；/chatter 是演示话题，实际替换为 topic list 的结果。

### 查看话题发布频率 { #ros2-topic-hz }

```bash
ros2 topic hz /chatter
```

- 助记：`Hz` = hertz（赫兹，每秒次数）；命令统计收到的消息频率，不是消息大小。

## 服务、动作与参数

调用服务、发送动作目标，查看和修改参数。

### 查看服务和动作类型 { #ros2-service-action-list }

```bash
ros2 service list -t
ros2 action list -t
```

- 助记：`service` 是请求／响应，`action` 是有反馈且可取消的长任务；list 只查看接口，不调用动作。

### 查看节点的参数及参数值 { #ros2-param-get }

```bash
ros2 param list /talker
ros2 param get /talker use_sim_time
```

- 助记：`param` ← parameter（参数）；list 列名称，get 读取某个参数的值。
- 作用：节点名按实际替换；use_sim_time 是常见参数，若节点没有声明则无法读取。

### 查看消息或服务的字段定义 { #ros2-interface-show }

```bash
ros2 interface show std_msgs/msg/String
```

- 助记：`interface` = 接口定义，`show` = 展示；msg 是 message（消息），srv 是 service（服务）。

## 启动

`ros2 run` 运行单个节点，`ros2 launch` 用启动文件一次运行多个节点。

### 运行演示发布节点 { #ros2-run-talker }

```bash
ros2 run demo_nodes_cpp talker
```

- 助记：`run` = 运行可执行程序，后面先写 package（包）再写 executable（程序）；talker 是演示发布者的名字。
- 作用：需要安装 demo_nodes_cpp；运行后可在另一个已加载环境的终端检查 /chatter。

## 数据包录制

`ros2 bag` 录制、回放和查看数据包。

### 录制一个话题 { #ros2-bag-record }

```bash
ros2 bag record -o chatter-demo /chatter
```

- 助记：`bag` 联想装消息的袋子；record = 录制，`-o` = output（输出目录）。
- 作用：输出目录应尚不存在；ctrl + c 停止录制并保存。

### 查看录包概要 { #ros2-bag-info }

```bash
ros2 bag info chatter-demo
```

- 助记：`info` ← information（信息）；先看录包里的话题、时长和消息量，再决定如何回放。

### 回放录制的数据包 { #ros2-bag-play }

```bash
ros2 bag play chatter-demo
```

- 助记：`play` = 播放；回放是重新发布消息，可能被订阅者当成新的实时数据。
- 作用：回放会重新发布话题；在隔离的调试环境中使用，避免触发连接的机器人控制节点。

## TF 与可视化

查看坐标变换，用 RViz 显示机器人状态。

### 查看两坐标系之间的变换 { #ros2-tf-echo }

```bash
ros2 run tf2_ros tf2_echo base_link tool0
```

- 助记：`TF` 可按 transform（坐标变换）记，tf2 是 ROS 的坐标变换库；echo 显示两个坐标系的关系。
- 作用：需要运行中的 TF 发布者；坐标系名称按机器人替换。

### 启动 RViz { #ros2-rviz }

```bash
rviz2
```

- 助记：`RViz` 可按 ROS visualization（ROS 可视化）记；Fixed Frame 是所有数据显示时使用的参考坐标系。
- 作用：需要 rviz2 和图形界面，启动后设置 Fixed Frame 并添加显示项。
