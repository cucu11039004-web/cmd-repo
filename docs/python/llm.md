# LLM 开发

下载、运行、微调和调用大语言模型。

示例展示基础流程；安装这些工具应使用独立 Python 环境，不需要装入本站的 MkDocs 环境。

基础条目参考：[Hugging Face CLI](https://huggingface.co/docs/huggingface_hub/guides/cli)、[Transformers 生成文档](https://huggingface.co/docs/transformers/main_classes/text_generation)、[PEFT 入门](https://huggingface.co/docs/peft/quicktour)、[vLLM serve](https://docs.vllm.ai/en/latest/cli/serve/)、[vLLM 对话 API](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/)。

## 模型下载与缓存

从 Hugging Face 下载模型，设置镜像站和缓存目录。

### 下载一个小模型到指定目录 { #llm-hf-download }

```bash
hf download HuggingFaceTB/SmolLM2-135M-Instruct --local-dir ./models/smollm2
```

- 助记：`hf` 指 Hugging Face，`download` = 下载；local-dir = 本地目录，模型名的最后一段是仓库名。
- 作用：需要 huggingface_hub 提供的 hf 命令和网络；模型名仅作示例。

### 为一次下载指定缓存目录 { #llm-hf-cache }

```bash
HF_HOME="$HOME/.cache/huggingface-demo" hf download HuggingFaceTB/SmolLM2-135M-Instruct
```

- 助记：`HF_HOME` 指 Hugging Face 数据与缓存的根位置；命令前的变量赋值只传给这次启动的进程。
- 作用：不改变后续终端命令的缓存配置；未加 --local-dir 时存入缓存。

## Transformers 推理

用 `AutoTokenizer`、`AutoModelForCausalLM` 加载模型，`generate` 生成文本，套用对话模板。

### 用对话模板生成文本 { #llm-transformers-generate }

```python
tokens = model.generate(**inputs, max_new_tokens=64, do_sample=False)
```

- 助记：`tokenizer` 把文本转成 token（词元）编号；chat template 格式化对话，generate 生成编号，decode 还原文本。
- 作用：需要 torch 与 transformers；示例默认在 CPU 运行，首次运行会下载模型。对话模板由模型 tokenizer 提供。
- 使用前提：先加载 model 和 tokenizer，用对话模板与 tokenizer 生成 inputs；生成后再解码 token。准备流程见下方。

**解释性示例：**

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "HuggingFaceTB/SmolLM2-135M-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)
model.eval()
messages = [{"role": "user", "content": "Explain what a robot is."}]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
with torch.inference_mode():
    tokens = model.generate(**inputs, max_new_tokens=64, do_sample=False)
new_tokens = tokens[0, inputs["input_ids"].shape[1]:]
print(tokenizer.decode(new_tokens, skip_special_tokens=True))
```

## 微调（LoRA）

用 PEFT 做 LoRA 微调，合并和保存权重。

### 为因果语言模型配置 LoRA { #llm-lora-config }

```python
model = get_peft_model(model, config)
```

- 助记：`LoRA` ← Low-Rank Adaptation（低秩适配），`PEFT` ← Parameter-Efficient Fine-Tuning（参数高效微调）；r 是低秩矩阵的秩。
- 作用：需要 peft，并先加载上一节的 model；目标层名称按模型结构调整。这一步只配置可训练参数，尚未训练。
- 使用前提：先从 peft 导入 get_peft_model，准备基础 model 和 LoraConfig；配置字段见下方示例。

**解释性示例：**

```python
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    task_type="CAUSAL_LM", r=8, lora_alpha=16,
    lora_dropout=0.05, target_modules=["q_proj", "v_proj"],
)
model = get_peft_model(model, config)
model.print_trainable_parameters()
```

## 推理服务（vLLM）

用 vLLM 启动兼容 OpenAI 接口的推理服务。

### 启动仅监听本机的模型服务 { #llm-vllm-serve }

```bash
vllm serve ./models/smollm2 --host 127.0.0.1 --port 8000 --served-model-name demo
```

- 助记：`LLM` ← large language model（大语言模型）；serve = 提供服务，host = 监听地址，served-model-name = 接口使用的模型名。
- 作用：先下载模型，并在符合 vLLM 安装与硬件要求的环境执行；默认上下文、显存等参数按设备调整。

### 查看服务公开的模型名称 { #llm-vllm-models }

```bash
curl http://127.0.0.1:8000/v1/models
```

- 助记：`/v1/models` 是模型列表端点；端点返回的 id 才是客户端请求里应填写的 model 名。
- 作用：在服务启动后执行；请求中的模型名应与返回的 ID 一致。

## 调用模型 API

用官方 SDK 调用在线大模型接口，读取环境变量里的密钥。

### 向本地模型服务发送对话请求 { #llm-local-chat-api }

```bash
curl http://127.0.0.1:8000/v1/chat/completions -H 'Content-Type: application/json' -d '{"model":"demo","messages":[{"role":"user","content":"Hello"}],"max_tokens":64}'
```

- 助记：`API` ← application programming interface（应用编程接口）；chat completions 表示对话生成，messages 是角色与文本的列表。
- 作用：对应上一节的本机 vLLM 服务，需模型提供对话模板；在线服务的地址、认证与字段按其官方文档配置。
- 使用前提：这是一条 HTTP 请求；下方保留分行写法帮助读清请求头与数据。

**解释性示例：**

```bash
curl http://127.0.0.1:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"demo","messages":[{"role":"user","content":"Hello"}],"max_tokens":64}'
```
