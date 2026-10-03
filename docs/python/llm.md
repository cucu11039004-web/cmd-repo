# LLM 开发

下载、运行、微调和调用大语言模型。

## 模型下载与缓存

从 Hugging Face 下载模型，设置镜像站和缓存目录。

## Transformers 推理

用 `AutoTokenizer`、`AutoModelForCausalLM` 加载模型，`generate` 生成文本，套用对话模板。

## 微调（LoRA）

用 PEFT 做 LoRA 微调，合并和保存权重。

## 推理服务（vLLM）

用 vLLM 启动兼容 OpenAI 接口的推理服务。

## 调用模型 API

用官方 SDK 调用在线大模型接口，读取环境变量里的密钥。
