---
title: "LangChain基础：构建智能应用"
slug: "basics"
sequence: 1
description: "掌握LangChain框架的核心概念和基础组件，学习如何构建智能应用"
is_published: true
estimated_minutes: 45
language: "zh-CN"
permalink: "https://www.agi01.com/course/agi/langchain/basics"
course: "agi/course/langchain"
header_image: "images/basics_header.png"
---

# LangChain基础：构建智能应用

![LangChain基础：构建智能应用](images/basics_header.png)

## 什么是 LangChain？🤔

LangChain 是一个强大的框架，它让我们能够：
- 轻松构建基于 LLM 的应用
- 组合不同的 AI 能力
- 创建智能工作流程

就像乐高积木一样，LangChain 提供了各种可组合的组件，让我们能快速搭建智能应用。

### 为什么选择 LangChain？

1. **开箱即用**
   - 丰富的组件库
   - 完整的工具链
   - 简单的接口

2. **灵活可扩展**
   - 自定义组件
   - 插件机制
   - 多种集成

3. **生产可用**
   - 性能优化
   - 错误处理
   - 监控支持

## 核心概念 📚

### 1. Chains（链）

链就像是一条生产线，将不同的处理步骤串联起来：

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

# 创建提示模板
prompt = PromptTemplate(
    input_variables=["product"],
    template="给我介绍下{product}的主要特点和优势"
)

# 创建LLM
llm = OpenAI(temperature=0.7)

# 创建链
chain = LLMChain(
    llm=llm,
    prompt=prompt
)

# 运行链
response = chain.run("iPhone 15")
print(response)
```

### 2. Prompts（提示）

提示是与 LLM 交互的关键：

```python
# 简单的提示模板
simple_prompt = PromptTemplate(
    input_variables=["question"],
    template="请回答这个问题：{question}"
)

# 带有示例的提示模板
few_shot_prompt = FewShotPromptTemplate(
    examples=[
        {"question": "1+1等于几？", "answer": "1+1等于2"},
        {"question": "2+2等于几？", "answer": "2+2等于4"}
    ],
    example_prompt=PromptTemplate(
        input_variables=["question", "answer"],
        template="问：{question}\n答：{answer}"
    ),
    suffix="问：{input}\n答：",
    input_variables=["input"]
)
```

### 3. Memory（记忆）

让 AI 能够记住对话历史：

```python
from langchain.memory import ConversationBufferMemory

# 创建记忆组件
memory = ConversationBufferMemory()

# 创建带记忆的链
chain = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# 对话示例
chain.predict(input="你好！")
chain.predict(input="我们刚才说了什么？")
```

### 4. Tools（工具）

扩展 AI 的能力范围：

```python
from langchain.agents import load_tools
from langchain.agents import initialize_agent

# 加载工具
tools = load_tools([
    "serpapi",     # 搜索引擎
    "calculator",  # 计算器
    "wikipedia"    # 维基百科
])

# 创建代理
agent = initialize_agent(
    tools, 
    llm, 
    agent="zero-shot-react-description",
    verbose=True
)

# 使用代理
agent.run("2023年世界杯冠军是谁？")
```

## 实际应用案例 💡

### 1. 智能客服机器人

```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

class CustomerServiceBot:
    def __init__(self):
        # 初始化记忆
        self.memory = ConversationBufferWindowMemory(
            k=5  # 记住最近5轮对话
        )
        
        # 创建对话链
        self.chain = ConversationChain(
            llm=OpenAI(temperature=0.7),
            memory=self.memory,
            verbose=True
        )
        
    async def handle_message(self, message: str) -> str:
        """处理用户消息"""
        try:
            # 生成回复
            response = await self.chain.apredict(
                input=message
            )
            
            return response
            
        except Exception as e:
            return f"抱歉，我遇到了一些问题：{str(e)}"
```

### 2. 智能文档助手

```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

class DocumentAssistant:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.db = None
        
    def load_document(self, file_path: str):
        """加载文档"""
        # 1. 加载文件
        loader = TextLoader(file_path)
        documents = loader.load()
        
        # 2. 分割文本
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        
        # 3. 创建向量数据库
        self.db = Chroma.from_documents(
            texts,
            self.embeddings
        )
        
    async def answer_question(self, question: str) -> str:
        """回答问题"""
        if not self.db:
            return "请先加载文档"
            
        # 1. 搜索相关内容
        docs = self.db.similarity_search(question)
        
        # 2. 生成回答
        chain = load_qa_chain(OpenAI(), chain_type="stuff")
        response = await chain.arun(
            input_documents=docs,
            question=question
        )
        
        return response
```

### 3. 数据分析助手

```python
from langchain.agents import create_pandas_dataframe_agent
import pandas as pd

class DataAnalysisAssistant:
    def __init__(self):
        self.agent = None
        
    def load_data(self, file_path: str):
        """加载数据"""
        # 读取数据
        df = pd.read_csv(file_path)
        
        # 创建数据分析代理
        self.agent = create_pandas_dataframe_agent(
            OpenAI(temperature=0),
            df,
            verbose=True
        )
        
    def analyze(self, question: str) -> str:
        """分析数据"""
        if not self.agent:
            return "请先加载数据"
            
        try:
            return self.agent.run(question)
        except Exception as e:
            return f"分析过程中出现错误：{str(e)}"
```

## 最佳实践 ✨

### 1. 提示工程

- **明确指令**：给出清晰的任务描述
```python
good_prompt = """
请分析以下文本的情感倾向：
- 如果是正面情感，返回"positive"
- 如果是负面情感，返回"negative"
- 如果是中性情感，返回"neutral"

文本：{text}
"""

bad_prompt = """
分析情感：{text}
"""
```

- **结构化输出**：指定返回格式
```python
structured_prompt = """
分析以下产品评价，返回JSON格式：
{
    "sentiment": "positive/negative/neutral",
    "key_points": ["优点1", "优点2"],
    "rating": 1-5
}

评价：{review}
"""
```

### 2. 错误处理

```python
class RobustChain:
    def __init__(self, llm, max_retries=3):
        self.llm = llm
        self.max_retries = max_retries
        
    async def run_with_retry(self, prompt):
        """带重试的运行"""
        for i in range(self.max_retries):
            try:
                return await self.llm.agenerate([prompt])
            except Exception as e:
                if i == self.max_retries - 1:
                    raise e
                await asyncio.sleep(1 * (i + 1))
```

### 3. 性能优化

```python
class OptimizedChain:
    def __init__(self):
        self.cache = {}
        self.lock = asyncio.Lock()
        
    async def run_with_cache(self, key, func):
        """带缓存的运行"""
        # 检查缓存
        if key in self.cache:
            return self.cache[key]
            
        # 获取锁
        async with self.lock:
            # 双重检查
            if key in self.cache:
                return self.cache[key]
                
            # 执行函数
            result = await func()
            
            # 更新缓存
            self.cache[key] = result
            return result
```

## 实用技巧 💪

### 1. 批量处理

```python
async def batch_process(items, chain, batch_size=5):
    """批量处理数据"""
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        # 并行处理
        tasks = [
            chain.arun(item)
            for item in batch
        ]
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
    return results
```

### 2. 流式处理

```python
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 创建流式LLM
streaming_llm = OpenAI(
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    temperature=0
)

# 流式链
streaming_chain = LLMChain(
    llm=streaming_llm,
    prompt=prompt
)
```

### 3. 调试技巧

```python
from langchain.callbacks import get_openai_callback

# 跟踪token使用
with get_openai_callback() as cb:
    response = chain.run("测试输入")
    print(f"总Token数: {cb.total_tokens}")
    print(f"提示Token数: {cb.prompt_tokens}")
    print(f"完成Token数: {cb.completion_tokens}")
    print(f"总成本: ${cb.total_cost}")
```

## 小结 📝

LangChain 是一个强大而灵活的框架，它能帮助我们：
1. 快速构建 AI 应用
2. 组合多种 AI 能力
3. 优化应用性能

关键要点：
- 掌握核心组件
- 理解最佳实践
- 注重实际应用

下一步：
- 探索更多组件
- 尝试实际项目
- 优化应用性能

记住：好的应用不是一蹴而就的，需要在实践中不断优化和改进。从简单的应用开始，逐步增加复杂性，最终构建出强大而可靠的系统。
