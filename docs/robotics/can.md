# CAN 总线

用 SocketCAN 和 can-utils 调试电机。以下命令在 Linux 上执行。

命令需要 iproute2 / can-utils，Python 示例需要 python-can。电机控制报文、ID 与数据字节含义由具体型号决定，确认手册后再填写「电机通信备忘」。

基础条目参考：[Linux SocketCAN 文档](https://docs.kernel.org/networking/can.html)、[can-utils 官方项目](https://github.com/linux-can/can-utils)、[python-can SocketCAN 文档](https://python-can.readthedocs.io/en/stable/interfaces/socketcan.html)。

## 启用接口

设置波特率，启用或关闭 `can0` 等接口。

### 设置并启用物理 CAN 接口 { #can-interface-up }

```bash
sudo ip link set can0 down
sudo ip link set can0 type can bitrate 500000
sudo ip link set can0 up
```

- 助记：`CAN` ← Controller Area Network（控制器局域网）；link 是网络接口，bitrate 是每秒比特数，up / down 是启用／关闭。
- 作用：需要硬件、驱动和正确接线；500000 是示例比特率，必须与总线设备一致。

### 创建虚拟 CAN 接口用于练习 { #can-vcan-create }

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up
```

- 助记：`vcan` = virtual CAN（虚拟 CAN）；modprobe 加载模块，link add 创建接口，up 启用接口。
- 作用：vcan0 仅在本机模拟 CAN，不连接物理电机；已有接口时不必重复创建。

## 收发与抓包

`candump` 抓包，`cansend` 发送单帧，按 ID 过滤。

### 监听 CAN 帧 { #can-dump }

```bash
candump can0
```

- 助记：`dump` = 把接收到的内容转储／显示；candump 是 CAN 帧查看工具，不会自动解释电机协议。
- 作用：替换接口名；虚拟练习可使用 candump vcan0。ctrl + c 结束。

### 向虚拟总线发送测试帧 { #can-send-virtual }

```bash
cansend vcan0 123#11223344
```

- 助记：`send` = 发送；`ID#DATA` 用 # 分开十六进制帧 ID 与数据，两个十六进制字符表示一个字节。
- 作用：先在另一个终端运行 candump vcan0；123 是十六进制标准帧 ID，数据为四字节。

### 只监听一个标准帧 ID { #can-filter-id }

```bash
candump can0,123:7FF
```

- 助记：过滤格式是 `ID:MASK`；mask（掩码）决定比较哪些位，0x7FF 对应标准 CAN ID 的 11 个位。
- 作用：按掩码筛选标准帧 ID 0x123；若还需严格排除扩展帧，应加入扩展帧标志位掩码。

## Python CAN

用 python-can 收发 CAN 帧。

### 在虚拟总线上发送并接收自己的帧 { #can-python-loopback }

```python
bus.send(message, timeout=1)
bus.recv(timeout=1)
```

- 助记：`arbitration_id` = 仲裁标识，`is_extended_id=False` 选标准帧；receive_own_messages 允许接收自己发出的帧。
- 作用：需要 python-can 与已启用的 vcan0；只用于虚拟总线示例。
- 使用前提：bus 是启用 receive_own_messages 的 vcan0 SocketCAN 连接，message 是准备好的测试帧。

**解释性示例：**

```python
import can

with can.Bus(interface="socketcan", channel="vcan0", receive_own_messages=True) as bus:
    message = can.Message(arbitration_id=0x123, data=[0x11, 0x22], is_extended_id=False)
    bus.send(message, timeout=1)
    print(bus.recv(timeout=1))
```

## 电机通信备忘

电机 ID、控制模式、报文格式等电机相关备忘。

## 排错

总线无响应、bus-off、错误帧时的检查步骤。

### 查看 CAN 状态与错误统计 { #can-link-statistics }

```bash
ip -details -statistics link show can0
```

- 助记：`details` = 详细参数，`statistics` = 统计；bus-off 是控制器因错误退出总线的状态。
- 作用：核对 bitrate、CAN state、bus-off 和错误计数；通信协议还需查设备手册。
