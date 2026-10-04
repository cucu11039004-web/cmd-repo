# gRPC 与 Protobuf

用 gRPC 在机器人各模块之间通信。

示例在独立环境中安装 grpcio 和 grpcio-tools 后运行，演示仅绑定本机的明文连接。跨主机部署按实际需求配置 TLS 和认证。

基础条目参考：[gRPC Python 官方教程](https://grpc.io/docs/languages/python/basics/)、[grpcurl 官方项目](https://github.com/fullstorydev/grpcurl)。

## 编译 proto

用 `protoc` 或 `grpc_tools.protoc` 从 `.proto` 文件生成代码。

### 声明一个 RPC 方法 { #grpc-proto-definition }

```protobuf
rpc SayHello (HelloRequest) returns (HelloReply);
```

- 助记：`proto` = protocol（协议）相关定义；rpc 是 remote procedure call（远程过程调用），request / reply 是请求／响应消息。
- 作用：把下方完整解释性示例保存为 demo.proto；生成接口、服务端和客户端示例都使用这个定义。
- 使用前提：这条声明放在 .proto 的 service 内；请求／响应 message 与完整文件结构见下方解释。

**解释性示例：**

```protobuf
syntax = "proto3";
package demo;

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply);
}
message HelloRequest { string name = 1; }
message HelloReply { string message = 1; }
```

### 为 proto 生成 Python 接口 { #grpc-generate-python }

```bash
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. demo.proto
```

- 助记：`protoc` = Protocol Buffers 编译器；`-I` 是 import path（导入搜索路径），python_out 指 Python 代码输出目录。
- 作用：需要 grpcio-tools；生成 demo_pb2.py 和 demo_pb2_grpc.py，运行环境需有匹配版本的 grpcio / protobuf。

## 调试服务

用 `grpcurl` 列出服务、查看接口定义、发送请求。

### 列出启用反射的服务 { #grpcurl-list-services }

```bash
grpcurl -plaintext localhost:50051 list
```

- 助记：`grpcurl` 是 gRPC 的命令行请求工具；list 列服务，plaintext = 明文；gRPC 的 g 不固定展开成某个词。
- 作用：仅当服务启用 server reflection 时可用；下方最小服务没有启用反射。-plaintext 仅用于本机明文调试。

### 带 proto 定义调用本机服务 { #grpcurl-call-proto }

```bash
grpcurl -plaintext -import-path . -proto demo.proto -d '{"name":"robot"}' localhost:50051 demo.Greeter/SayHello
```

- 助记：`-proto` 给接口定义，`-d` = data（请求数据）；`包.服务/方法` 指定这次 RPC 调用的目标。
- 作用：不依赖反射；需要同目录的 demo.proto 和已运行的服务端。
- 使用前提：这是一条请求命令；参数较多时可按下方示例分行阅读。

**解释性示例：**

```bash
grpcurl -plaintext -import-path . -proto demo.proto \
  -d '{"name":"robot"}' localhost:50051 demo.Greeter/SayHello
```

## Python 客户端与服务端

用 Python 写 gRPC 服务端和客户端的基本结构。

### 启动最小本机服务端 { #grpc-python-server }

```python
server.start()
```

- 助记：`server` = 服务端，`Servicer` 是服务实现；start 开始监听，wait_for_termination 等待服务结束。
- 作用：先生成 Python 接口；保存为 server.py 后运行，在另一个终端调用。
- 使用前提：server 是已创建、注册服务并绑定端口的 grpc.server 对象；完整准备流程见下方。

**解释性示例：**

```python
from concurrent import futures
import grpc
import demo_pb2
import demo_pb2_grpc

class Greeter(demo_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return demo_pb2.HelloReply(message=f"Hello, {request.name}")

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
demo_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
server.add_insecure_port("127.0.0.1:50051")
server.start()
server.wait_for_termination()
```

### 用超时限制客户端请求 { #grpc-python-client }

```python
reply = stub.SayHello(demo_pb2.HelloRequest(name="robot"), timeout=3)
```

- 助记：`stub` 是客户端代理，把本地方法调用转换成 RPC；channel 是连接通道，timeout 给本次请求截止时间。
- 作用：服务端需已启动；超时或连接失败会抛出 grpc.RpcError。
- 使用前提：先导入生成的接口并创建 channel、stub；这条调用发送请求并限定 3 秒超时。

**解释性示例：**

```python
import grpc
import demo_pb2
import demo_pb2_grpc

with grpc.insecure_channel("127.0.0.1:50051") as channel:
    stub = demo_pb2_grpc.GreeterStub(channel)
    reply = stub.SayHello(demo_pb2.HelloRequest(name="robot"), timeout=3)
    print(reply.message)
```
