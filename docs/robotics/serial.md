# 串口

调试串口设备和总线舵机。Linux 设备名一般是 `/dev/ttyUSB*` 或 `/dev/ttyACM*`，macOS 是 `/dev/cu.*`。

Python 示例需要 pyserial：在独立环境中执行 python -m pip install pyserial。舵机协议、波特率和 ID 扫描方式应在确认型号后记录到最后一节。

基础条目参考：[pySerial 官方入门](https://pyserial.readthedocs.io/en/latest/shortintro.html)、[udevadm 手册源码](https://raw.githubusercontent.com/systemd/systemd/main/man/udevadm.xml)。

## 查找设备

插上 USB 转串口后，找到对应的设备名。

### 列出串口及 USB 标识 { #serial-list-ports }

```bash
python -m serial.tools.list_ports -v
```

- 助记：`serial` = 串行通信，`list_ports` = 列出端口；这里的 port 是串口设备，不是 TCP 网络端口。
- 作用：需要在 Python 环境中安装 pyserial；Linux 和 macOS 均可用。

### 查看 Linux 的稳定串口路径 { #serial-by-id }

```bash
ls -l /dev/serial/by-id/
```

- 助记：`by-id` = 按标识组织；ttyUSB0 是动态编号，by-id 路径用于识别具体设备。
- 作用：路径由 udev 生成，部分设备可能没有唯一序列号或该目录不存在。

## 权限与固定设备名

把用户加入 `dialout` 组；用 udev 规则给设备起固定名字，避免重新插拔后编号变化。

### 把当前用户加入串口访问组 { #serial-dialout-group }

```bash
sudo usermod -aG dialout "$USER"
```

- 助记：`usermod` = user modification（修改用户）；`-a` = append（追加），`-G` 指附加组，dialout 是这里使用的串口访问组名。
- 作用：适用于使用 dialout 组的 Linux；重新登录后生效，用 ls -l /dev/ttyUSB0 核对设备所属组。

### 查看串口的 udev 属性 { #serial-udev-properties }

```bash
udevadm info --query=property --name=/dev/ttyUSB0
```

- 助记：`udevadm` 是 udev 管理工具；info 查信息，property = 属性，name 指设备路径。
- 作用：Linux 命令；用 ID_SERIAL 等实际属性确定稳定标识，不依赖 ttyUSB 编号。

## 调试工具

`screen`、`picocom`、`minicom`，打开串口收发数据。

### 用 Python 串口终端交互调试 { #serial-miniterm }

```bash
python -m serial.tools.miniterm /dev/ttyUSB0 115200
```

- 助记：`miniterm` = mini terminal（小型终端）；设备路径后面的 115200 是 baud rate（波特率），须与设备一致。
- 作用：波特率按设备手册设置；macOS 换成实际 /dev/cu.* 路径。`ctrl + ]` 退出，`ctrl + t → ctrl + h` 查看帮助。

## Python 串口

用 pyserial 列出端口、打开串口、收发数据。

### 带超时读取串口数据 { #serial-python-read }

```python
data = port.read(64)
```

- 助记：`baudrate` = 波特率，`timeout` = 超时秒数；read(64) 最多读 64 字节，不保证每次都读满。
- 作用：read 可能因超时返回少于 64 字节；打开串口可能改变 DTR / RTS 状态。
- 使用前提：port 是已经打开且设置 timeout 的串口对象；连接与关闭流程见下方。

**解释性示例：**

```python
import serial

with serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1) as port:
    data = port.read(64)
    print(data.hex())
```

### 用回环串口练习收发 { #serial-python-loopback }

```python
port.write(b"hello\n")
port.readline()
```

- 助记：`loopback` = 回环；write 写出的字节回到同一模拟端口，readline 按换行或超时结束读取。
- 作用：loop:// 是 pySerial 的软件回环，不需要连接真实设备。
- 使用前提：port 通过 serial.serial_for_url("loop://", timeout=1) 创建；两条分别写入、读回软件回环中的一行。

**解释性示例：**

```python
import serial

with serial.serial_for_url("loop://", timeout=1) as port:
    port.write(b"hello\n")
    print(port.readline())
```

## 舵机通信备忘

波特率、ID 扫描、协议格式等舵机相关备忘。
