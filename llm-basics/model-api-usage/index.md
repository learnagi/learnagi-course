# 模型 API 使用

## 课程目标
- 掌握主流 LLM API 的调用方法
- 理解不同模型的特点和适用场景
- 能够进行基本的模型响应处理和错误处理

## OpenAI API
### 1. API基础
```python
import openai

# 设置API密钥
openai.api_key = 'your-api-key'

# 基本调用
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "你是一个助手"},
        {"role": "user", "content": "介绍下你自己"}
    ]
)
```

### 2. 模型参数
- temperature
- max_tokens
- top_p
- frequency_penalty
- presence_penalty

### 3. 流式响应
```python
for chunk in openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "写一个故事"}],
    stream=True
):
    content = chunk.choices[0].delta.get("content", "")
    print(content, end="")
```

## Anthropic Claude API
### 1. 基本使用
```python
from anthropic import Anthropic

anthropic = Anthropic(api_key="your-api-key")
completion = anthropic.completions.create(
    model="claude-2",
    prompt="Human: 你好\n\nAssistant:",
    max_tokens_to_sample=100
)
```

### 2. 特点和优势
- 更长的上下文窗口
- 代码能力强
- 安全性高

## Google PaLM API
### 1. 初始化和调用
```python
import google.generativeai as palm

palm.configure(api_key='your-api-key')
response = palm.chat(messages=["你好"])
```

### 2. 模型特性
- 多语言支持
- 代码生成
- 文本分析

## Azure OpenAI
### 1. 配置和使用
```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="your-api-key",
    api_version="2023-05-15",
    azure_endpoint="your-endpoint"
)

response = client.chat.completions.create(
    model="gpt-35-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### 2. 企业特性
- 区域部署
- 合规性保证
- SLA保障

## 错误处理
### 1. 常见错误类型
- API密钥错误
- 请求超时
- 速率限制
- Token超限

### 2. 错误处理示例
```python
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except openai.error.RateLimitError:
    print("已达到速率限制")
except openai.error.InvalidRequestError:
    print("无效的请求")
except Exception as e:
    print(f"发生错误: {str(e)}")
```

## 响应处理
### 1. 解析响应
```python
def parse_response(response):
    return {
        'content': response.choices[0].message.content,
        'finish_reason': response.choices[0].finish_reason,
        'usage': response.usage.total_tokens
    }
```

### 2. 响应格式化
- JSON解析
- Markdown渲染
- 特殊标记处理

## 最佳实践
### 1. API调用优化
- 批量处理
- 缓存机制
- 重试策略

### 2. 成本控制
- Token计数
- 模型选择
- 缓存利用

### 3. 安全考虑
- API密钥轮换
- 请求日志
- 输入验证

## 性能优化
### 1. 并发请求
```python
import asyncio
import aiohttp

async def async_completion(prompt):
    async with aiohttp.ClientSession() as session:
        # 异步API调用实现
        pass
```

### 2. 批处理
- 请求合并
- 响应拆分
- 并行处理

## 练习作业
1. 实现基本的API调用
2. 处理流式响应
3. 实现错误处理机制
4. 优化API调用性能

## 参考资源
- [OpenAI API参考](https://platform.openai.com/docs/api-reference)
- [Anthropic API文档](https://docs.anthropic.com/claude/reference)
- [Google PaLM文档](https://developers.generativeai.google/guide)