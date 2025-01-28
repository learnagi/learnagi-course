---
title: "LangChain基础：开启AI应用开发之门"
slug: "basics"
sequence: 1
description: "了解LangChain框架的核心概念，掌握环境配置和基本用法"
is_published: true
estimated_minutes: 45
language: "zh-CN"
permalink: "https://www.agi01.com/course/agi/langchain/basics"
course: "agi/course/langchain"
header_image: "images/basics_header.png"
---

# LangChain基础：开启AI应用开发之门

![LangChain基础：开启AI应用开发之门](images/basics_header.png)

## 什么是 LangChain？🤔

想象你在搭建一个乐高城堡，你需要：
- 各种形状的积木（模型、工具）
- 连接积木的方法（链式调用）
- 建造的说明书（提示模板）
- 特殊功能积木（代理、记忆）

LangChain 就像是一个强大的乐高工具箱，它提供了：
- 统一的接口调用各种语言模型
- 灵活的组件连接方式
- 丰富的工具和集成
- 完整的应用开发框架

### 为什么选择 LangChain？

1. **简化开发**
   - 统一的接口
   - 丰富的组件
   - 快速原型开发

2. **功能强大**
   - 支持多种模型
   - 提供各类工具
   - 灵活的扩展性

3. **生产可用**
   - 完善的文档
   - 活跃的社区
   - 企业级支持

## 环境配置 🛠️

### 1. 安装 Python

确保你的系统已安装 Python 3.8.1 或更高版本：

```bash
# 检查 Python 版本
python --version

# 如果需要安装或升级
brew install python  # macOS
# 或访问 python.org 下载安装包
```

### 2. 安装 LangChain

```bash
# 使用 pip 安装
pip install langchain

# 安装常用依赖
pip install openai chromadb tiktoken
```

### 3. 配置环境变量

```python
# 设置环境变量
import os
os.environ["OPENAI_API_KEY"] = "你的OpenAI API密钥"

# 或者在终端中设置
export OPENAI_API_KEY="你的OpenAI API密钥"
```

## 第一个 LangChain 应用 🚀

让我们从一个简单的翻译应用开始：

```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage

# 1. 创建聊天模型
chat = ChatOpenAI(temperature=0)

# 2. 创建提示模板
template = """你是一个专业的翻译助手。
请将以下文本翻译成{target_language}：
{text}
"""

prompt = ChatPromptTemplate.from_template(template)

# 3. 准备消息
messages = prompt.format_messages(
    target_language="中文",
    text="The early bird catches the worm."
)

# 4. 获取回复
response = chat.invoke(messages)

print(response.content)
# 输出: 早起的鸟儿有虫吃。
```

让我们来分析这个简单应用的每个部分：

1. **导入必要模块**
   ```python
   from langchain.chat_models import ChatOpenAI  # 聊天模型
   from langchain.prompts import ChatPromptTemplate  # 提示模板
   ```

2. **创建模型实例**
   ```python
   chat = ChatOpenAI(temperature=0)  # temperature=0 表示输出最确定的答案
   ```

3. **定义提示模板**
   ```python
   template = """你是一个专业的翻译助手。
   请将以下文本翻译成{target_language}：
   {text}
   """
   ```

4. **格式化提示**
   ```python
   messages = prompt.format_messages(
       target_language="中文",
       text="The early bird catches the worm."
   )
   ```

5. **获取回复**
   ```python
   response = chat.invoke(messages)
   ```

## 基础概念 📚

### 1. Models（模型）

LangChain 支持多种类型的模型：

```python
# 聊天模型
from langchain.chat_models import ChatOpenAI
chat = ChatOpenAI()

# 文本生成模型
from langchain.llms import OpenAI
llm = OpenAI()

# 嵌入模型
from langchain.embeddings import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()
```

### 2. Prompts（提示）

提示是与模型交互的关键：

```python
# 简单提示模板
from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "给我讲一个关于{topic}的笑话"
)

# 聊天提示模板
from langchain.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个幽默的助手"),
    ("human", "讲个笑话吧"),
    ("assistant", "好的，这是一个关于程序员的笑话..."),
    ("human", "{input}")
])
```

### 3. Chains（链）

链可以将多个组件连接起来：

```python
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

# 创建链
chain = LLMChain(
    llm=ChatOpenAI(),
    prompt=prompt
)

# 运行链
result = chain.invoke({"topic": "程序员"})
print(result["text"])
```

## 实用技巧 💡

### 1. 调试输出

```python
# 启用详细输出
import langchain
langchain.debug = True

# 使用 verbose 参数
chain = LLMChain(
    llm=ChatOpenAI(),
    prompt=prompt,
    verbose=True
)
```

### 2. 错误处理

```python
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 创建带有回调的模型
chat = ChatOpenAI(
    streaming=True,
    callback_manager=CallbackManager([
        StreamingStdOutCallbackHandler()
    ]),
    verbose=True
)

# 使用异常处理
try:
    response = chat.invoke([HumanMessage(content="Hello")])
except Exception as e:
    print(f"发生错误：{str(e)}")
```

### 3. 模型参数调优

```python
# 调整创造性
creative_chat = ChatOpenAI(temperature=0.9)  # 更有创意的回答

# 调整确定性
precise_chat = ChatOpenAI(temperature=0)  # 更确定的回答

# 限制输出长度
short_chat = ChatOpenAI(max_tokens=50)  # 限制回答长度
```

## 应用示例 🌟

### 1. 智能问答

```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# 创建带记忆的对话链
conversation = ConversationChain(
    llm=ChatOpenAI(),
    memory=ConversationBufferMemory()
)

# 进行对话
response1 = conversation.predict(input="你好！")
print(response1)
# 输出: 你好！很高兴见到你。有什么我可以帮你的吗？

response2 = conversation.predict(input="我们刚才说了什么？")
print(response2)
# 输出: 我们刚才打了招呼。你说"你好！"，我回复了问候并表示很高兴见到你。
```

### 2. 文本摘要

```python
from langchain.chains.summarize import load_summarize_chain

# 创建摘要链
chain = load_summarize_chain(
    llm=ChatOpenAI(),
    chain_type="map_reduce"  # 使用map_reduce方式处理长文本
)

# 准备文档
from langchain.docstore.document import Document
doc = Document(
    page_content="""
    人工智能(AI)正在改变我们的生活方式。从智能手机助手到自动驾驶汽车，
    AI技术已经渗透到了我们生活的方方面面。未来，AI将继续发展，
    可能带来更多令人兴奋的创新。但同时，我们也需要注意AI发展带来的挑战，
    确保技术发展服务于人类福祉。
    """
)

# 生成摘要
summary = chain.invoke([doc])
print(summary["output_text"])
# 输出: AI技术正在改变生活，带来创新的同时也需关注其挑战，确保造福人类。
```

## 最佳实践 ✨

### 1. 提示设计

```python
# 好的提示模板
good_prompt = PromptTemplate.from_template("""
请完成以下任务：
1. {task_1}
2. {task_2}
3. {task_3}

注意事项：
- 请逐步完成每个任务
- 清晰说明每步的理由
- 最后总结所有结果
""")

# 不好的提示模板
bad_prompt = PromptTemplate.from_template("""
完成{task_1}{task_2}{task_3}
""")  # 缺乏结构和清晰的指示
```

### 2. 链式设计

```python
# 好的链式设计
from langchain.chains import SimpleSequentialChain

# 第一个链：生成大纲
outline_chain = LLMChain(
    llm=ChatOpenAI(),
    prompt=PromptTemplate.from_template("为{topic}生成大纲")
)

# 第二个链：扩展内容
content_chain = LLMChain(
    llm=ChatOpenAI(),
    prompt=PromptTemplate.from_template("基于以下大纲生成详细内容：{outline}")
)

# 组合链
full_chain = SimpleSequentialChain(
    chains=[outline_chain, content_chain]
)

# 运行组合链
result = full_chain.invoke({"topic": "人工智能的未来"})
```

### 3. 错误处理和日志

```python
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SafeChain:
    def __init__(self, chain):
        self.chain = chain
        
    def run(self, input_data):
        try:
            # 记录输入
            logger.info(f"输入: {input_data}")
            
            # 运行链
            result = self.chain.invoke(input_data)
            
            # 记录输出
            logger.info(f"输出: {result}")
            
            return result
            
        except Exception as e:
            # 记录错误
            logger.error(f"错误: {str(e)}")
            
            # 返回友好的错误信息
            return {
                "error": "处理过程中出现错误",
                "details": str(e)
            }
```

## 小结 📝

LangChain 是一个强大的框架，它能帮助我们：
1. 快速构建 AI 应用
2. 灵活组合各种组件
3. 处理复杂的应用场景

关键要点：
- 理解基础概念
- 掌握核心组件
- 注重实践应用

下一步：
- 探索更多组件
- 尝试实际项目
- 参与社区讨论

记住：好的应用是一步步构建的。从简单的例子开始，逐步添加更多功能，最终打造出强大的应用。
