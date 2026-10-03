# 串口

调试串口设备和总线舵机。Linux 设备名一般是 `/dev/ttyUSB*` 或 `/dev/ttyACM*`，macOS 是 `/dev/cu.*`。

## 查找设备

插上 USB 转串口后，找到对应的设备名。

## 权限与固定设备名

把用户加入 `dialout` 组；用 udev 规则给设备起固定名字，避免重新插拔后编号变化。

## 调试工具

`screen`、`picocom`、`minicom`，打开串口收发数据。

## Python 串口

用 pyserial 列出端口、打开串口、收发数据。

## 舵机通信备忘

波特率、ID 扫描、协议格式等舵机相关备忘。
