# 相机与 USB 设备

在 Linux 上识别相机和其他 USB 设备。

## USB 设备

`lsusb`、`dmesg`，确认设备是否被识别。

## 相机

用 `v4l2-ctl` 查看相机和支持的格式；RealSense 相机的查看工具。

## 设备规则

用 udev 规则设置设备权限和固定名字。
