---
title: "大语言模型能做什么"
slug: "capabilities"
sequence: 3.2
description: "了解大语言模型的核心能力和应用场景，学会如何更好地使用AI助手"
is_published: false
estimated_minutes: 35
language: "zh-CN"
status: "draft"
created_at: "2024-03-19"
updated_at: "2024-03-19"
---

![AI能力图谱](./images/llm-capabilities.png)
*探索AI助手的"十八般武艺"*

# 大语言模型能做什么

## 本节你将学到

通过本节学习，你将：
- 全面了解AI助手的各项能力
- 掌握不同场景下的最佳使用方法
- 学会如何让AI输出更好的结果
- 认识AI能力的局限性

💡 重点内容：
- AI的核心能力和特点
- 常见应用场景和示例
- 提示词编写技巧
- 输出质量的评估方法

## 1. 语言理解能力

### 1.1 自然对话
就像和人类聊天一样，AI可以：
- 理解日常用语
- 保持对话连贯
- 回答跟进问题
- 记住上下文信息

📝 实际示例：
```
用户：今天天气真不错
AI：是的！阳光明媚的日子特别适合户外活动。
    您有什么户外计划吗？

用户：我在考虑去公园跑步
AI：好主意！跑步前记得：
1. 做好热身运动
2. 带足水分
3. 注意防晒
4. 选择合适的跑步时段

需要我帮您制定一个简单的跑步计划吗？
```

### 1.2 多语言处理
AI就像一个"语言通"：
- 支持100多种语言
- 实时翻译对话
- 理解地方俚语
- 保持语言风格

![语言能力](./images/language-support.png)
*AI支持的部分语言示例*

## 2. 创作与生成

### 2.1 文本创作
AI可以帮你：
- ✍️ 写文章和报告
- 📝 编写商业方案
- 🎵 创作诗歌歌词
- 📧 起草邮件通知

#### 创作示例
```markdown
提示词：写一个关于春天的短诗

AI的创作：
春风轻抚柳枝弯，
新绿初染满山间。
蝴蝶翩跹花丛里，
春天悄悄把门敲。
```

### 2.2 代码编程
像个资深程序员：
- 编写各种语言的代码
- 解释代码功能
- 找出代码错误
- 优化代码性能

![代码助手](./images/coding-assistant.png)
*AI作为编程助手的工作场景*

## 3. 分析与推理

### 3.1 数据分析
帮你理解数据背后的故事：
- 📊 数据可视化
- 📈 趋势分析
- 🔍 异常检测
- 📑 报告生成

### 3.2 逻辑推理
解决复杂问题：
- 数学计算
- 逻辑谜题
- 因果分析
- 决策建议

#### 推理示例
```
问题：一个房间里有3只猫，每只猫看到了2只猫。
     这种情况可能吗？为什么？

AI分析：
1. 这种情况是可能的
2. 解释：房间里有一面镜子
3. 每只猫看到镜子中的2只其他猫
4. 所以每只猫都"看到"了2只猫
```

## 4. 辅助工具

### 4.1 学习助手
像个耐心的老师：
- 讲解复杂概念
- 提供练习题
- 检查作业
- 答疑解惑

### 4.2 工作助手
提高工作效率：
- 会议记录整理
- 日程安排建议
- 项目计划制定
- 文档校对修改

## 5. 实战案例

### 5.1 智能对话系统
使用 OpenAI API 构建一个简单的对话系统：

```python
import openai

def chat_with_ai(prompt, system_role="你是一个友好的AI助手"):
    """基础对话示例"""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"发生错误: {str(e)}"

# 使用示例
prompt = "你能用通俗的语言解释一下什么是大语言模型吗？"
response = chat_with_ai(prompt)
print(response)
```

### 5.2 多轮对话
实现上下文记忆的对话系统：

```python
def chat_with_memory(messages):
    """带记忆的对话系统"""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"发生错误: {str(e)}"

# 对话历史
messages = [
    {"role": "system", "content": "你是一个AI助教，专门解答编程问题"},
    {"role": "user", "content": "Python中的列表和元组有什么区别？"},
    {"role": "assistant", "content": "主要区别是：\n1. 列表可修改，元组不可修改\n2. 列表用[]，元组用()"},
    {"role": "user", "content": "那字典呢？"}
]

response = chat_with_memory(messages)
print(response)
```

### 5.3 创意写作助手
让AI帮你进行创意写作：

```python
def creative_writer(topic, style="诗歌", length="短篇"):
    """创意写作助手"""
    prompt = f"请以{style}的形式创作一个关于'{topic}'的{length}作品"
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个专业的文学创作者"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# 使用示例
topic = "月光"
print(creative_writer(topic))
```

### 5.4 代码助手
AI辅助编程示例：

```python
def code_assistant(task, language="Python"):
    """代码编写助手"""
    prompt = f"""
    请用{language}编写代码实现以下功能：
    {task}
    
    要求：
    1. 代码要简洁易懂
    2. 包含必要的注释
    3. 考虑异常处理
    """
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个专业的程序员"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# 使用示例
task = "编写一个函数，判断一个字符串是否是回文字符串"
print(code_assistant(task))
```

## 6. 使用技巧

### 6.1 提示词工程
写好提示词的关键：

1. **明确指令**
```python
# 不好的例子
prompt = "写一篇文章"

# 好的例子
prompt = """
请写一篇关于人工智能的文章，要求：
1. 800字左右
2. 面向普通读者
3. 重点介绍AI的实际应用
4. 使用通俗易懂的语言
"""
```

2. **角色设定**
```python
system_role = """
你是一位经验丰富的技术作家，擅长：
1. 把复杂的技术概念解释得通俗易懂
2. 使用生动的类比和例子
3. 循序渐进地展开内容
4. 注重实用性和可操作性
"""
```

### 6.2 参数调优

```python
def generate_with_params(prompt, temperature=0.7, max_tokens=1000):
    """不同参数的效果示例"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,  # 控制创造性
        max_tokens=max_tokens,    # 控制长度
        presence_penalty=0.6,     # 鼓励话题多样性
        frequency_penalty=0.3     # 减少重复
    )
    return response.choices[0].message.content
```

[继续补充实践练习和常见问题...] 