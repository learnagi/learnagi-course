---
title: "语言模型使用：掌握LangChain中的模型操作"
slug: "models"
sequence: 2
description: "深入了解LangChain中的各类模型及其使用方法"
is_published: true
estimated_minutes: 30
language: "zh-CN"
permalink: "https://www.agi01.com/course/agi/langchain/models"
course: "agi/course/langchain"
header_image: "images/models_header.png"
---

# 语言模型使用：掌握LangChain中的模型操作

## 模型类型概览 🗂️

LangChain支持多种类型的模型：

1. **LLMs（传统语言模型）**
   - 输入文本，输出文本
   - 适合文本生成任务

2. **Chat Models（聊天模型）**
   - 支持多轮对话
   - 理解对话上下文

3. **Embeddings（嵌入模型）**
   - 将文本转换为向量
   - 用于相似度计算

## LLMs的使用 📝

### 1. 基本使用

```python
from langchain.llms import OpenAI

# 创建LLM
llm = OpenAI(temperature=0.7)

# 生成文本
text = llm.invoke("写一首关于春天的诗")
print(text)
# 输出：
# 春风轻抚绿柳梢，
# 百花争艳闹枝头。
# 蝴蝶翩翩舞春光，
# 细雨润物皆温柔。
```

### 2. 批量处理

```python
# 准备多个提示
prompts = [
    "写一句关于春天的诗",
    "写一句关于夏天的诗",
    "写一句关于秋天的诗"
]

# 批量生成
results = llm.batch(prompts)
for prompt, result in zip(prompts, results):
    print(f"提示: {prompt}")
    print(f"生成: {result}\n")
```

### 3. 流式输出

```python
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 创建流式LLM
streaming_llm = OpenAI(
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    temperature=0.7
)

# 生成文本（实时输出）
streaming_llm.invoke("讲一个关于人工智能的故事")
```

## Chat Models的使用 💭

### 1. 基本对话

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage

# 创建聊天模型
chat = ChatOpenAI(temperature=0)

# 进行对话
messages = [
    SystemMessage(content="你是一位友好的助手"),
    HumanMessage(content="你好！"),
    AIMessage(content="你好！很高兴见到你。"),
    HumanMessage(content="今天天气真好！")
]

response = chat.invoke(messages)
print(response.content)
# 输出: 是的，确实是个好天气！希望你能好好享受这美好的一天。
```

### 2. 角色扮演

```python
# 创建特定角色的助手
messages = [
    SystemMessage(content="""你是一位经验丰富的Python编程教师。
    - 使用简单的语言解释概念
    - 提供具体的代码示例
    - 鼓励学生思考和实践
    """),
    HumanMessage(content="什么是列表推导式？")
]

response = chat.invoke(messages)
print(response.content)
# 输出：
# 让我用简单的方式解释列表推导式：
# 
# 列表推导式是Python中一种简洁地创建列表的方法。想象你有一个"加工流水线"：
# 
# 1. 基本语法：
# [表达式 for 元素 in 可迭代对象]
# 
# 举个例子：
# ```python
# # 创建1-5的平方数列表
# squares = [x**2 for x in range(1, 6)]
# print(squares)  # [1, 4, 9, 16, 25]
# ```
# 
# 试试自己写一个？把一个字符串列表转换成大写：
# ```python
# words = ["hello", "world", "python"]
# upper_words = [word.upper() for word in words]
# ```
```

### 3. 多轮对话管理

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# 创建带记忆的对话链
conversation = ConversationChain(
    llm=ChatOpenAI(),
    memory=ConversationBufferMemory()
)

# 进行多轮对话
print(conversation.predict(input="你好！"))
print(conversation.predict(input="我叫小明"))
print(conversation.predict(input="还记得我的名字吗？"))
# 输出：
# 你好！很高兴见到你。
# 你好小明！很高兴认识你。
# 当然记得，你是小明！
```

## Embeddings的使用 🔤

### 1. 文本向量化

```python
from langchain.embeddings import OpenAIEmbeddings

# 创建嵌入模型
embeddings = OpenAIEmbeddings()

# 获取文本向量
text = "人工智能正在改变世界"
vector = embeddings.embed_query(text)
print(f"向量维度: {len(vector)}")  # 1536
```

### 2. 批量处理

```python
# 准备多个文本
texts = [
    "人工智能正在改变世界",
    "机器学习是AI的一个子领域",
    "深度学习推动了AI的发展"
]

# 批量获取向量
vectors = embeddings.embed_documents(texts)
print(f"文本数量: {len(vectors)}")
print(f"每个向量的维度: {len(vectors[0])}")
```

### 3. 相似度计算

```python
import numpy as np

def cosine_similarity(v1, v2):
    """计算余弦相似度"""
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# 准备文本
text1 = "人工智能正在改变世界"
text2 = "AI技术推动社会发展"
text3 = "今天天气真好"

# 获取向量
vec1 = embeddings.embed_query(text1)
vec2 = embeddings.embed_query(text2)
vec3 = embeddings.embed_query(text3)

# 计算相似度
sim12 = cosine_similarity(vec1, vec2)
sim13 = cosine_similarity(vec1, vec3)

print(f"{text1} 和 {text2} 的相似度: {sim12:.4f}")
print(f"{text1} 和 {text3} 的相似度: {sim13:.4f}")
# 输出：
# 人工智能正在改变世界 和 AI技术推动社会发展 的相似度: 0.8912
# 人工智能正在改变世界 和 今天天气真好 的相似度: 0.2134
```

## 模型参数调优 ⚙️

### 1. 温度控制

```python
# 创建不同温度的模型
creative_llm = OpenAI(temperature=0.9)  # 更有创意
balanced_llm = OpenAI(temperature=0.5)  # 平衡
precise_llm = OpenAI(temperature=0)     # 更确定

prompt = "给一个科幻故事的开头"

print("创意版本：")
print(creative_llm.invoke(prompt))

print("\n平衡版本：")
print(balanced_llm.invoke(prompt))

print("\n精确版本：")
print(precise_llm.invoke(prompt))
```

### 2. 输出控制

```python
# 控制输出长度
short_llm = OpenAI(max_tokens=50)
long_llm = OpenAI(max_tokens=200)

# 控制停止标记
custom_llm = OpenAI(
    stop=["\n", "。"],  # 遇到换行或句号停止
    max_tokens=100
)

# 示例
prompt = "写一个关于未来科技的故事"
print("简短版本：")
print(short_llm.invoke(prompt))

print("\n详细版本：")
print(long_llm.invoke(prompt))
```

### 3. 采样策略

```python
# 使用不同的采样策略
from langchain.llms import OpenAI

# Top-P采样
creative_llm = OpenAI(
    temperature=0.7,
    top_p=0.9
)

# Top-K采样
focused_llm = OpenAI(
    temperature=0.7,
    top_k=40
)

# 频率惩罚
diverse_llm = OpenAI(
    temperature=0.7,
    frequency_penalty=0.5,
    presence_penalty=0.5
)
```

## 最佳实践 ✨

### 1. 模型选择

```python
def choose_model(task_type, requirements):
    """根据任务类型和要求选择合适的模型"""
    if task_type == "对话":
        if requirements.get("创造性", False):
            return ChatOpenAI(temperature=0.8)
        else:
            return ChatOpenAI(temperature=0)
    
    elif task_type == "生成":
        if requirements.get("长文本", False):
            return OpenAI(
                temperature=0.7,
                max_tokens=500
            )
        else:
            return OpenAI(
                temperature=0.5,
                max_tokens=100
            )
    
    elif task_type == "分析":
        return OpenAI(temperature=0)
```

### 2. 错误处理

```python
import time
from typing import Optional

class RobustModel:
    def __init__(self, model, max_retries=3, delay=1):
        self.model = model
        self.max_retries = max_retries
        self.delay = delay
    
    def invoke(self, prompt: str) -> Optional[str]:
        """带重试的模型调用"""
        for attempt in range(self.max_retries):
            try:
                return self.model.invoke(prompt)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    print(f"最终错误: {str(e)}")
                    return None
                print(f"尝试 {attempt + 1} 失败: {str(e)}")
                time.sleep(self.delay * (attempt + 1))
```

### 3. 性能优化

```python
class ModelManager:
    def __init__(self):
        self._models = {}
        
    def get_model(self, model_type: str, **kwargs):
        """获取或创建模型（单例模式）"""
        key = f"{model_type}_{hash(frozenset(kwargs.items()))}"
        
        if key not in self._models:
            if model_type == "chat":
                self._models[key] = ChatOpenAI(**kwargs)
            elif model_type == "llm":
                self._models[key] = OpenAI(**kwargs)
            elif model_type == "embeddings":
                self._models[key] = OpenAIEmbeddings(**kwargs)
                
        return self._models[key]

# 使用示例
manager = ModelManager()

# 获取相同配置的模型实例（复用）
chat1 = manager.get_model("chat", temperature=0)
chat2 = manager.get_model("chat", temperature=0)
print(chat1 is chat2)  # True

# 获取不同配置的模型实例（新建）
chat3 = manager.get_model("chat", temperature=0.5)
print(chat1 is chat3)  # False
```

## 小结 📝

本章我们学习了：
1. 不同类型的模型及其特点
2. 如何使用和配置各种模型
3. 模型参数调优的方法
4. 实用的最佳实践

关键点：
- 选择合适的模型类型
- 正确设置模型参数
- 做好错误处理
- 注意性能优化

下一步：
- 探索更多模型类型
- 尝试不同的参数组合
- 在实际项目中应用
