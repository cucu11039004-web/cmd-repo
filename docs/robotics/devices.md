# 相机与 USB 设备

在 Linux 上识别相机和其他 USB 设备。

基础条目参考：[v4l2-ctl 官方手册源码](https://raw.githubusercontent.com/gjasny/v4l-utils/master/utils/v4l2-ctl/v4l2-ctl.1.in)、[udevadm 官方手册源码](https://raw.githubusercontent.com/systemd/systemd/main/man/udevadm.xml)。

## USB 设备

`lsusb`、`dmesg`，确认设备是否被识别。

### 列出 USB 设备 { #devices-lsusb }

```bash
lsusb
```

- 助记：`lsusb` = list USB devices（列出 USB 设备）；USB 是 Universal Serial Bus（通用串行总线）。
- 作用：Linux 命令，需要 usbutils。

### 查看 USB 拓扑与连接速率 { #devices-usb-tree }

```bash
lsusb -t
```

- 助记：`-t` = tree（树状结构），按连接层级显示 USB 拓扑与速率。

### 实时查看内核设备日志 { #devices-dmesg-follow }

```bash
sudo dmesg -w
```

- 助记：`dmesg` 可按 diagnostic message（诊断消息）记；显示内核消息，`-w` = follow（跟随新消息）。
- 作用：插拔设备时观察识别日志；ctrl + c 结束。

## 相机

用 `v4l2-ctl` 查看相机和支持的格式；RealSense 相机的查看工具。

### 列出视频设备及对应节点 { #devices-video-list }

```bash
v4l2-ctl --list-devices
```

- 助记：`V4L2` = Video for Linux 2，`ctl` = control；list-devices = 列设备，/dev/video* 是设备节点。
- 作用：Linux 命令，需要 v4l-utils。

### 查看相机支持的格式和分辨率 { #devices-video-formats }

```bash
v4l2-ctl -d /dev/video0 --list-formats-ext
```

- 助记：`formats` = 格式，`ext` = extended（扩展）；`-d` = device（设备），列出格式、分辨率和帧率。
- 作用：先用 list-devices 确认设备节点；同一相机可能暴露多个节点。

### 查看相机当前设置 { #devices-video-settings }

```bash
v4l2-ctl -d /dev/video0 --all
```

- 助记：`--all` = 全部常规信息，检查的是当前设置；支持哪些设置要看 formats 等列表。

## 设备规则

用 udev 规则设置设备权限和固定名字。

### 查看可用于 udev 规则的设备属性 { #devices-udev-attributes }

```bash
udevadm info --attribute-walk --name=/dev/video0
```

- 助记：`attribute` = 属性，`walk` = 逐层走访；attribute-walk 展示设备及父设备的可匹配属性。
- 作用：根据实际设备属性写规则；不要直接复制其他设备的 vendor / product / serial。
