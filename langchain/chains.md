---
title: "链式调用：构建复杂AI应用的基础"
slug: "chains"
sequence: 5
description: "深入了解LangChain中的链式调用，掌握如何组合不同组件以实现复杂功能"
is_published: true
estimated_minutes: 40
language: "zh-CN"
permalink: "https://www.agi01.com/course/agi/langchain/chains"
course: "agi/course/langchain"
header_image: "images/chains_header.png"
---

# 链式调用：构建复杂AI应用的基础

## 什么是链式调用？🔗

链式调用是一种将多个处理步骤组合在一起的方式：
- 通过将不同的组件（模型、工具、提示等）连接在一起，形成一个完整的工作流程。
- 每个步骤的输出可以作为下一个步骤的输入。

### 1. 链的基本概念

- **输入**：用户提供的数据或请求。
- **处理**：通过一系列组件对输入进行处理。
- **输出**：最终生成的结果。

## 创建简单链 🛠️

### 1. 基本链

```python
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# 创建提示模板
prompt = PromptTemplate.from_template("请给我一个关于{topic}的简介")

# 创建LLM
llm = OpenAI(temperature=0.7)

# 创建链
chain = LLMChain(llm=llm, prompt=prompt)

# 运行链
result = chain.invoke({"topic": "人工智能"})
print(result["text"])
# 输出: 人工智能是计算机科学的一个分支...
```

### 2. 组合多个链

```python
from langchain.chains import SimpleSequentialChain

# 创建多个链
chain1 = LLMChain(llm=llm, prompt=PromptTemplate.from_template("写一首关于{topic}的诗"))
chain2 = LLMChain(llm=llm, prompt=PromptTemplate.from_template("请为这首诗写一个总结"))

# 组合链
combined_chain = SimpleSequentialChain(chains=[chain1, chain2])

# 运行组合链
final_result = combined_chain.invoke({"topic": "春天"})
print(final_result["text"])
```

## 高级链式调用 🚀

### 1. 带条件的链

```python
from langchain.chains import ConditionalChain

# 创建条件链
conditional_chain = ConditionalChain(
    chains={
        "是": chain1,
        "否": chain2
    },
    condition_key="user_response"
)

# 运行条件链
response = conditional_chain.invoke({"user_response": "是"})
print(response["text"])
```

### 2. 循环链

```python
from langchain.chains import LoopChain

# 创建循环链
loop_chain = LoopChain(
    chain=chain1,
    max_iterations=3  # 最大迭代次数
)

# 运行循环链
loop_result = loop_chain.invoke({"topic": "机器学习"})
print(loop_result["text"])
```

### 3. 组合多种类型的链

```python
from langchain.chains import MultiChain

# 创建多个不同类型的链
chain_a = LLMChain(llm=llm, prompt=PromptTemplate.from_template("生成一个关于{topic}的故事"))
chain_b = LLMChain(llm=llm, prompt=PromptTemplate.from_template("总结一下这个故事"))

# 创建多链
multi_chain = MultiChain(chains=[chain_a, chain_b])

# 运行多链
multi_result = multi_chain.invoke({"topic": "AI的未来"})
print(multi_result["text"])
```

## 实际应用案例 💡

### 1. 智能问答系统

```python
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# 创建对话链
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=OpenAI(),
    memory=memory
)

# 进行对话
response1 = conversation.predict(input="你好！")
response2 = conversation.predict(input="你能帮我解答一些问题吗？")
print(response1)
print(response2)
```

### 2. 文本分析与总结

```python
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain

# 创建文本分析链
analysis_chain = LLMChain(
    llm=OpenAI(),
    prompt=PromptTemplate.from_template("分析以下文本：{text}")
)

# 创建总结链
summary_chain = LLMChain(
    llm=OpenAI(),
    prompt=PromptTemplate.from_template("总结以下分析：{analysis}")
)

# 组合链
combined_chain = SimpleSequentialChain(chains=[analysis_chain, summary_chain])

# 运行组合链
result = combined_chain.invoke({"text": "人工智能正在改变世界"})
print(result["text"])
```

## 最佳实践 ✨

### 1. 设计清晰的链

- 确保每个链的输入和输出都清晰定义
- 使用适当的提示模板
- 处理链之间的依赖关系

### 2. 错误处理

```python
try:
    result = chain.invoke({"topic": "机器学习"})
except Exception as e:
    print(f"发生错误：{str(e)}")
```

### 3. 性能优化

- 使用异步调用提高效率
- 减少不必要的链调用
- 监控链的性能

## 小结 📝

本章我们学习了：
1. 链式调用的基本概念
2. 如何创建和组合链
3. 高级链式调用的应用
4. 实际应用案例

关键点：
- 理解链的工作原理
- 设计清晰的链结构
- 处理错误和优化性能

下一步：
- 探索更多链的类型
- 在实际项目中应用链式调用
- 参与社区讨论
