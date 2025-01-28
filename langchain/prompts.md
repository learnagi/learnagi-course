---
title: "提示工程：掌握LangChain中的提示模板和技巧"
slug: "prompts"
sequence: 3
description: "深入了解LangChain中的提示工程，包括提示模板、示例学习和提示优化"
is_published: true
estimated_minutes: 35
language: "zh-CN"
permalink: "https://www.agi01.com/course/agi/langchain/prompts"
course: "agi/course/langchain"
header_image: "images/prompts_header.png"
---

# 提示工程：掌握LangChain中的提示模板和技巧

## 提示工程基础 🎯

### 1. 什么是提示工程？

提示工程就像是与AI对话的艺术：
- 如何提问（输入设计）
- 如何引导（上下文控制）
- 如何获得期望的答案（输出控制）

### 2. 为什么需要提示工程？

- 提高回答质量
- 确保输出格式
- 控制生成内容
- 优化交互效果

## 提示模板 📝

### 1. 基础模板

```python
from langchain.prompts import PromptTemplate

# 简单模板
template = PromptTemplate.from_template(
    "请给我一个关于{topic}的{length}字简介"
)

# 使用模板
prompt = template.format(
    topic="人工智能",
    length="100"
)

print(prompt)
# 输出: 请给我一个关于人工智能的100字简介
```

### 2. 带验证的模板

```python
from langchain.prompts import PromptTemplate

# 创建带验证的模板
template = PromptTemplate(
    input_variables=["product_name", "price"],
    template="产品名称：{product_name}\n价格：{price}元\n请生成一个产品推广文案。",
    # 验证器确保价格是数字
    validate_template=True
)

try:
    # 正确使用
    prompt1 = template.format(
        product_name="智能手表",
        price="1999"
    )
    print("正确示例：")
    print(prompt1)
    
    # 错误使用
    prompt2 = template.format(
        product_name="智能手表",
        price="很贵"  # 这会引发错误
    )
except ValueError as e:
    print("\n错误示例：")
    print(f"错误：{str(e)}")
```

### 3. 聊天提示模板

```python
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessage, HumanMessage

# 创建聊天模板
chat_template = ChatPromptTemplate.from_messages([
    SystemMessage(content="你是一位专业的{role}"),
    HumanMessage(content="请问{question}")
])

# 格式化消息
messages = chat_template.format_messages(
    role="Python教师",
    question="什么是装饰器？"
)

for message in messages:
    print(f"{message.type}: {message.content}")
# 输出:
# system: 你是一位专业的Python教师
# human: 请问什么是装饰器？
```

## 示例学习（Few-Shot Learning）📚

### 1. 基本示例学习

```python
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts import PromptTemplate

# 定义示例
examples = [
    {"word": "开心", "antonym": "难过"},
    {"word": "高兴", "antonym": "沮丧"},
    {"word": "兴奋", "antonym": "平静"}
]

# 创建示例格式模板
example_template = """
词语: {word}
反义词: {antonym}
"""
example_prompt = PromptTemplate(
    input_variables=["word", "antonym"],
    template=example_template
)

# 创建Few-Shot提示模板
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="请根据以下示例，给出词语的反义词：",
    suffix="词语: {input}\n反义词:",
    input_variables=["input"]
)

# 使用模板
prompt = few_shot_prompt.format(input="快乐")
print(prompt)
# 输出:
# 请根据以下示例，给出词语的反义词：
#
# 词语: 开心
# 反义词: 难过
#
# 词语: 高兴
# 反义词: 沮丧
#
# 词语: 兴奋
# 反义词: 平静
#
# 词语: 快乐
# 反义词:
```

### 2. 动态示例选择

```python
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

# 准备更多示例
examples = [
    {"word": "开心", "antonym": "难过"},
    {"word": "高兴", "antonym": "沮丧"},
    {"word": "兴奋", "antonym": "平静"},
    {"word": "勇敢", "antonym": "胆怯"},
    {"word": "聪明", "antonym": "愚笨"},
    {"word": "勤奋", "antonym": "懒惰"}
]

# 创建示例选择器
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    FAISS,
    k=2  # 选择2个最相关的示例
)

# 创建动态Few-Shot提示模板
dynamic_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="请根据以下示例，给出词语的反义词：",
    suffix="词语: {input}\n反义词:",
    input_variables=["input"]
)

# 使用动态模板
prompt = dynamic_prompt.format(input="智慧")
print(prompt)
# 输出会包含最相关的示例（如"聪明"）
```

## 提示优化技巧 💡

### 1. 结构化输出

```python
# 定义JSON输出格式的提示模板
json_template = PromptTemplate.from_template("""
分析以下文本的情感，返回JSON格式：
文本: {text}

要求返回格式如下：
{
    "sentiment": "positive/negative/neutral",
    "confidence": 0.0-1.0,
    "keywords": ["关键词1", "关键词2"]
}
""")

# 使用模板
prompt = json_template.format(
    text="这家餐厅的服务态度很好，食物也很美味，就是价格有点贵。"
)
```

### 2. 分步骤提示

```python
# 创建分步骤提示模板
step_template = PromptTemplate.from_template("""
请按照以下步骤分析这个编程问题：

问题描述：{problem}

1. 理解问题
   - 输入是什么？
   - 输出应该是什么？
   - 有什么限制条件？

2. 设计解决方案
   - 可以使用什么算法？
   - 需要什么数据结构？
   - 时间和空间复杂度是多少？

3. 编写代码
   - 提供Python代码实现
   - 包含必要的注释
   - 处理边界情况

4. 测试验证
   - 给出测试用例
   - 验证代码正确性
   - 考虑极端情况

请按照上述步骤，详细分析并解决这个问题。
""")

# 使用模板
prompt = step_template.format(
    problem="实现一个函数，找出数组中第K大的数字"
)
```

### 3. 角色设定

```python
# 创建带角色设定的模板
role_template = ChatPromptTemplate.from_messages([
    SystemMessage(content="""你是一位经验丰富的{role}，具有以下特点：
    1. {trait_1}
    2. {trait_2}
    3. {trait_3}
    
    在回答问题时，请始终保持这个角色定位。
    """),
    HumanMessage(content="{question}")
])

# 使用模板
messages = role_template.format_messages(
    role="Python技术面试官",
    trait_1="深入理解Python原理和最佳实践",
    trait_2="擅长引导候选人思考和分析问题",
    trait_3="注重代码质量和设计模式",
    question="请评估一下这段代码的优缺点：\n```python\ndef process_data(data):\n    return [x*2 for x in data if x > 0]```"
)
```

## 高级应用 🚀

### 1. 提示链组合

```python
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

# 创建多个专门的提示模板
analysis_template = PromptTemplate.from_template(
    "分析以下文本的主要观点：{text}"
)

summary_template = PromptTemplate.from_template(
    "基于以下分析生成总结：{analysis}"
)

suggestion_template = PromptTemplate.from_template(
    "基于以下总结提供改进建议：{summary}"
)

# 创建链
llm = ChatOpenAI(temperature=0)

analysis_chain = LLMChain(
    llm=llm,
    prompt=analysis_template
)

summary_chain = LLMChain(
    llm=llm,
    prompt=summary_template
)

suggestion_chain = LLMChain(
    llm=llm,
    prompt=suggestion_template
)

# 组合使用
async def process_text(text):
    # 1. 分析
    analysis = await analysis_chain.arun(text=text)
    
    # 2. 总结
    summary = await summary_chain.arun(analysis=analysis)
    
    # 3. 建议
    suggestions = await suggestion_chain.arun(summary=summary)
    
    return {
        "analysis": analysis,
        "summary": summary,
        "suggestions": suggestions
    }
```

### 2. 动态提示生成

```python
class PromptGenerator:
    def __init__(self):
        self.templates = {
            "formal": "尊敬的{title}{name}，{content}",
            "casual": "嗨，{name}！{content}",
            "business": "亲爱的{title}{name}：\n\n{content}\n\n此致\n敬礼"
        }
    
    def generate_prompt(self, style, **kwargs):
        """根据场景生成合适的提示"""
        if style not in self.templates:
            raise ValueError(f"不支持的样式：{style}")
            
        template = PromptTemplate.from_template(
            self.templates[style]
        )
        
        return template.format(**kwargs)

# 使用示例
generator = PromptGenerator()

# 正式场合
formal_prompt = generator.generate_prompt(
    "formal",
    title="张",
    name="总",
    content="感谢您参加我们的年度会议。"
)

# 日常场合
casual_prompt = generator.generate_prompt(
    "casual",
    name="小明",
    content="周末要不要一起打球？"
)

print("正式场合：")
print(formal_prompt)
print("\n日常场合：")
print(casual_prompt)
```

### 3. 提示模板管理

```python
class PromptManager:
    def __init__(self):
        self._templates = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """加载默认模板"""
        self._templates = {
            "translation": PromptTemplate.from_template(
                "将以下{source_lang}文本翻译成{target_lang}：\n{text}"
            ),
            "summary": PromptTemplate.from_template(
                "用{length}字总结以下内容：\n{text}"
            ),
            "analysis": PromptTemplate.from_template(
                "从{aspect}角度分析以下内容：\n{text}"
            )
        }
    
    def add_template(self, name, template):
        """添加新模板"""
        if name in self._templates:
            raise ValueError(f"模板 {name} 已存在")
        self._templates[name] = template
    
    def get_template(self, name):
        """获取模板"""
        if name not in self._templates:
            raise ValueError(f"模板 {name} 不存在")
        return self._templates[name]
    
    def list_templates(self):
        """列出所有可用模板"""
        return list(self._templates.keys())
    
    def format_prompt(self, template_name, **kwargs):
        """使用指定模板格式化提示"""
        template = self.get_template(template_name)
        return template.format(**kwargs)

# 使用示例
manager = PromptManager()

# 使用翻译模板
translation_prompt = manager.format_prompt(
    "translation",
    source_lang="中文",
    target_lang="英文",
    text="人工智能正在改变世界"
)

# 使用总结模板
summary_prompt = manager.format_prompt(
    "summary",
    length="100",
    text="这是一段很长的文本..."
)

# 添加自定义模板
manager.add_template(
    "email",
    PromptTemplate.from_template(
        "主题：{subject}\n收件人：{recipient}\n\n{content}"
    )
)

# 列出所有模板
print("可用模板：", manager.list_templates())
```

## 最佳实践 ✨

### 1. 提示设计原则

- **明确性**：清晰指定要求和期望
- **结构化**：使用格式化的结构
- **示例性**：提供具体的示例
- **可测试性**：便于验证输出

### 2. 常见问题解决

- **输出不稳定**：降低temperature值
- **格式不统一**：使用结构化模板
- **内容不相关**：加强上下文约束
- **质量不高**：使用Few-Shot示例

### 3. 性能优化

- **模板缓存**：重用常用模板
- **批量处理**：合并相似请求
- **异步处理**：并行处理多个请求

## 小结 📝

本章我们学习了：
1. 提示工程的基础概念
2. 各类提示模板的使用
3. Few-Shot学习的应用
4. 高级提示技巧和优化方法

关键点：
- 选择合适的模板类型
- 设计清晰的提示结构
- 使用示例提升质量
- 注意性能和可维护性

下一步：
- 实践不同类型的提示
- 优化提示模板
- 构建模板库
- 应用到实际项目
