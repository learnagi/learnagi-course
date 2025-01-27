---
title: "提示工程基础"
slug: "prompt-engineering/basics"
description: "学习提示工程的基本概念和通用技巧"
---

# 提示工程基础

## 大语言模型设置

### 模型参数概述
在使用提示词时，我们可以通过配置一些参数来获得不同的提示结果。调整这些设置对于提高响应的可靠性非常重要，通常需要进行实验才能找到适合特定用例的正确设置。

### 核心参数

#### Temperature（温度）
- **定义**：控制输出的随机性和创造性
- **取值范围**：0-2（通常使用0-1）
- **使用建议**：
  - 较低的值（0.1-0.4）：生成更确定和事实性的响应，适合QA、事实提取等任务
  - 较高的值（0.7-1.0）：生成更多样化和创造性的响应，适合创意写作、头脑风暴等任务
- **最佳实践**：从0.7开始，根据需要调整

#### Top_p（核采样）
- **定义**：控制词元选择的累积概率阈值
- **取值范围**：0-1
- **使用建议**：
  - 较低的值：生成更保守和可预测的响应
  - 较高的值：考虑更多可能性，生成更多样化的输出
- **注意事项**：建议只调整Temperature或Top_p其中一个，不要同时使用

#### Max Length（最大长度）
- **定义**：控制模型生成的最大token数
- **使用建议**：
  - 根据任务需求设置合适的长度
  - 较短的限制可以提高响应的相关性
  - 有助于控制API调用成本

#### Stop Sequences（停止序列）
- **定义**：指定模型停止生成的标记
- **使用场景**：
  - 生成列表时控制项目数量
  - 格式化输出时标记结束位置
  - 控制对话轮次
- **示例**：使用数字、特殊符号或关键词作为停止标记

### 高级参数

#### Frequency Penalty（频率惩罚）
- **定义**：根据token出现频率动态调整惩罚权重
- **取值范围**：-2.0到2.0
- **使用建议**：
  - 正值：减少重复，增加多样性
  - 负值：允许更多重复，保持一致性
  - 适用于需要避免重复内容的场景

#### Presence Penalty（存在惩罚）
- **定义**：对所有重复token施加统一惩罚
- **取值范围**：-2.0到2.0
- **使用建议**：
  - 正值：鼓励使用新词，增加话题广度
  - 负值：允许话题重复，保持主题聚焦
  - 适用于控制响应的主题发散程度

### 参数组合建议

1. **事实型任务**（如：QA、知识提取）
   ```json
   {
     "temperature": 0.2,
     "max_tokens": 150,
     "presence_penalty": 0.0,
     "frequency_penalty": 0.0
   }
   ```

2. **创意型任务**（如：写作、创意生成）
   ```json
   {
     "temperature": 0.8,
     "max_tokens": 500,
     "presence_penalty": 0.5,
     "frequency_penalty": 0.2
   }
   ```

3. **对话型任务**（如：聊天机器人）
   ```json
   {
     "temperature": 0.7,
     "max_tokens": 150,
     "presence_penalty": 0.6,
     "frequency_penalty": 0.1
   }
   ```

### 调优技巧
1. 从默认参数开始，逐步调整
2. 保持单一变量原则，每次只调整一个参数
3. 记录参数组合及其效果
4. 针对特定任务建立参数模板
5. 定期评估和优化参数设置

### 代码示例

#### 1. 基础调用示例
```python
import openai

# 设置API密钥
openai.api_key = 'your-api-key'

# 基础对话示例
def basic_chat():
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # 使用的模型
        messages=[
            {"role": "system", "content": "你是一个乐于助人的AI助手。"},
            {"role": "user", "content": "你好！"}
        ]
    )
    print(response.choices[0].message.content)

# 运行示例
basic_chat()
```

#### 2. 参数控制示例
```python
def controlled_chat(
    temperature=0.7,
    max_tokens=150,
    presence_penalty=0.0,
    frequency_penalty=0.0
):
    """
    使用不同参数控制输出的示例
    
    参数：
        temperature：控制随机性 (0-2)
        max_tokens：最大输出长度
        presence_penalty：重复惩罚 (-2.0-2.0)
        frequency_penalty：频率惩罚 (-2.0-2.0)
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "你是一个专业的小说家。"
            },
            {
                "role": "user",
                "content": "写一个关于未来世界的短故事开头"
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty
    )
    return response.choices[0].message.content

# 创意写作 - 高温度设置
creative_story = controlled_chat(temperature=0.9)
print("创意故事:", creative_story)

# 事实性回答 - 低温度设置
factual_response = controlled_chat(temperature=0.2)
print("事实性回答:", factual_response)
```

#### 3. 流式输出示例
```python
def stream_chat():
    """
    流式输出示例，实时显示生成的内容
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "讲一个关于人工智能的故事"
            }
        ],
        stream=True  # 启用流式输出
    )
    
    # 实时打印每个token
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end='')
    print()

# 运行流式输出示例
stream_chat()
```

#### 4. 多轮对话示例
```python
def multi_turn_chat():
    """
    多轮对话示例，展示上下文记忆
    """
    messages = [
        {"role": "system", "content": "你是一个数学老师。"},
        {"role": "user", "content": "什么是勾股定理？"},
    ]
    
    # 第一轮对话
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    print("AI:", response.choices[0].message.content)
    
    # 添加用户的后续问题
    messages.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })
    messages.append({
        "role": "user",
        "content": "给我一个具体的例子"
    })
    
    # 第二轮对话
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    print("AI:", response.choices[0].message.content)

# 运行多轮对话示例
multi_turn_chat()
```

#### 5. 函数调用示例
```python
def function_calling_example():
    """
    展示如何使用函数调用功能
    """
    # 定义可用函数
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "获取指定城市的天气信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称"
                        }
                    },
                    "required": ["city"]
                }
            }
        }
    ]

    # 创建对话
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "北京今天天气怎么样？"
            }
        ],
        tools=tools,
        tool_choice="auto"
    )

    # 处理函数调用
    message = response.choices[0].message
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        print(f"调用函数: {tool_call.function.name}")
        print(f"参数: {tool_call.function.arguments}")

# 运行函数调用示例
function_calling_example()
```

#### 6. 错误处理示例
```python
def error_handling_example():
    """
    展示如何处理API调用中的常见错误
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "你好"
                }
            ],
            temperature=3.0  # 故意设置一个无效的温度值
        )
    except openai.APIError as e:
        print(f"API错误: {e}")
    except openai.RateLimitError as e:
        print(f"速率限制错误: {e}")
    except openai.APIConnectionError as e:
        print(f"连接错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")

# 运行错误处理示例
error_handling_example()
```

### 参数使用建议

#### 1. 创意型任务
```python
# 适合创意写作、头脑风暴等任务
creative_params = {
    "temperature": 0.8,
    "max_tokens": 500,
    "presence_penalty": 0.5,
    "frequency_penalty": 0.2
}
```

#### 2. 事实型任务
```python
# 适合QA、知识提取等任务
factual_params = {
    "temperature": 0.2,
    "max_tokens": 150,
    "presence_penalty": 0.0,
    "frequency_penalty": 0.0
}
```

#### 3. 对话型任务
```python
# 适合聊天机器人等任务
chat_params = {
    "temperature": 0.7,
    "max_tokens": 150,
    "presence_penalty": 0.6,
    "frequency_penalty": 0.1
}
```

## 基本概念

### 提示词的定义与作用
- **定义**：提示词是传递给语言模型的输入信息，包含指令、问题、上下文等
- **作用**：
  - 指导模型完成特定任务
  - 提供必要的上下文信息
  - 控制输出的格式和风格
  - 影响生成内容的质量

### 提示词的组成部分
1. **指令（Instruction）**
   - 明确的任务说明
   - 行为要求
   - 输出规范

2. **上下文（Context）**
   - 背景信息
   - 相关知识
   - 约束条件

3. **输入（Input）**
   - 需要处理的具体内容
   - 用户提供的数据
   - 补充材料

4. **输出格式（Output Format）**
   - 期望的返回格式
   - 结构要求
   - 样式规范

### 提示词格式

#### 基本格式
1. **问题格式**
   ```
   <问题>?
   ```

2. **指令格式**
   ```
   <指令>
   ```

3. **QA格式**
   ```
   Q: <问题>?
   A:
   ```

#### 高级格式
1. **少样本提示**
   ```
   Q: <问题1>?
   A: <答案1>

   Q: <问题2>?
   A: <答案2>

   Q: <新问题>?
   A:
   ```

2. **分类示例**
   ```
   示例1 // 类别1
   示例2 // 类别2
   新示例 //
   ```

### 提示词类型

#### 1. 零样本提示（Zero-shot Prompting）
- 直接提问，不提供示例
- 适用于简单任务
- 依赖模型的基础能力

#### 2. 少样本提示（Few-shot Prompting）
- 提供示例后提问
- 适用于复杂任务
- 通过示例引导模型学习

#### 3. 链式提示（Chain Prompting）
- 将任务分解为多个步骤
- 每个步骤的输出作为下一步输入
- 适用于复杂推理任务

### 提示词设计原则

1. **清晰性**
   - 使用明确的指令
   - 避免模糊的表述
   - 提供具体的要求

2. **完整性**
   - 包含必要的上下文
   - 提供充分的信息
   - 明确输出要求

3. **相关性**
   - 信息要与任务相关
   - 避免无关内容
   - 保持重点

4. **一致性**
   - 格式保持统一
   - 风格保持一致
   - 术语使用统一

### 常见问题与解决方案

1. **输出不符合预期**
   - 检查指令是否清晰
   - 添加更多上下文
   - 提供示例说明

2. **回答不完整**
   - 明确说明需要详细回答
   - 设置合适的最大长度
   - 使用结构化提示

3. **内容重复**
   - 调整惩罚参数
   - 优化提示词结构
   - 添加约束条件

## 提示词要素

### 核心要素

#### 1. 指令（Instruction）
- **定义**：想要模型执行的具体任务或指令
- **特点**：
  - 明确且具体
  - 行为导向
  - 可执行性强
- **示例**：
  ```
  将以下文本翻译成英文：
  总结以下文章的要点：
  分析以下代码的问题：
  ```

#### 2. 上下文（Context）
- **定义**：帮助模型更好理解和执行任务的背景信息
- **作用**：
  - 提供任务背景
  - 设定约束条件
  - 说明特殊要求
- **示例**：
  ```
  你是一位专业的Python开发者，擅长代码优化。
  请以初中学生的知识水平来解释。
  考虑到性能和可维护性的要求。
  ```

#### 3. 输入数据（Input）
- **定义**：需要模型处理的具体内容
- **形式**：
  - 文本内容
  - 代码片段
  - 结构化数据
- **示例**：
  ```
  文本：这是一段需要分析的内容
  代码：def example(): pass
  数据：{"key": "value"}
  ```

#### 4. 输出指示（Output Indication）
- **定义**：期望的输出格式或结构
- **要求**：
  - 格式规范
  - 结构清晰
  - 易于解析
- **示例**：
  ```
  请以JSON格式输出：
  请按以下结构回答：
  1. 分析
  2. 建议
  3. 总结
  ```

### 要素组合示例

#### 1. 文本分类任务
```
指令：将以下文本分类为积极、消极或中性
上下文：这是一个情感分析任务，需要考虑文本的语气和用词
输入：这家餐厅的服务还不错，但价格有点贵
输出格式：情感：[分类结果]
```

#### 2. 代码优化任务
```
指令：优化以下Python代码的性能
上下文：代码将运行在资源受限的环境中，需要最小化内存使用
输入：
def fibonacci(n):
    if n <= 1: return n
    return fibonacci(n-1) + fibonacci(n-2)
输出格式：
1. 优化后的代码
2. 优化说明
3. 性能对比
```

#### 3. 内容生成任务
```
指令：生成一篇博客文章
上下文：面向初学编程的读者，需要使用简单易懂的语言
输入：主题：Python异步编程入门
输出格式：
- 标题
- 引言
- 正文（分3-5个小节）
- 总结
```

### 要素选择原则

1. **任务相关性**
   - 根据任务类型选择必要要素
   - 避免冗余信息
   - 保持简洁清晰

2. **完整性**
   - 确保包含所有必要信息
   - 避免信息缺失
   - 保持逻辑连贯

3. **清晰性**
   - 使用明确的语言
   - 避免歧义
   - 结构化呈现

4. **可扩展性**
   - 便于修改和调整
   - 支持复杂任务
   - 易于维护

### 常见问题

1. **要素过多**
   - 影响：降低响应质量
   - 解决：保持精简，只包含必要要素
   - 建议：先从基本要素开始，根据需要添加

2. **要素缺失**
   - 影响：输出不符合预期
   - 解决：检查并补充必要要素
   - 建议：使用检查清单确保完整性

3. **要素冲突**
   - 影响：造成混淆和错误
   - 解决：确保要素之间的一致性
   - 建议：系统性检查和测试

## 设计提示的通用技巧

### 基本原则

#### 1. 从简单开始
- **渐进式开发**
  - 从基本提示开始
  - 逐步添加元素和上下文
  - 持续迭代和改进
- **任务分解**
  - 将复杂任务分解为子任务
  - 逐步构建和优化
  - 避免初期过度复杂化

#### 2. 指令清晰
- **使用明确的动词**
  - 写入、分类、总结
  - 翻译、排序、分析
  - 比较、评估、推荐
- **结构化格式**
  - 使用分隔符（如 ###）
  - 清晰的层次结构
  - 统一的格式标准

#### 3. 保持具体性
- **详细描述**
  - 明确任务要求
  - 指定输出格式
  - 提供示例说明
- **相关性原则**
  - 包含必要细节
  - 避免无关信息
  - 保持重点

### 实践技巧

#### 1. 避免模糊表述
- **反面示例**：
  ```
  解释提示工程的概念，不要太长。
  ```
- **正面示例**：
  ```
  用2-3句话向高中生解释提示工程的概念。
  ```

#### 2. 明确做什么而非不做什么
- **反面示例**：
  ```
  不要询问用户偏好
  不要包含个人信息
  ```
- **正面示例**：
  ```
  直接推荐当前热门电影
  基于公开数据提供建议
  ```

#### 3. 使用示例引导
```
输入格式：
问题：[问题内容]
背景：[相关背景]
要求：[具体要求]

示例回答：
分析：[分析内容]
建议：[建议内容]
结论：[结论内容]
```

### 优化策略

#### 1. 迭代优化
1. **基线测试**
   - 使用简单提示
   - 记录基础效果
   - 确定改进方向

2. **系统改进**
   - 逐个修改变量
   - 测试不同变体
   - 记录效果变化

3. **效果验证**
   - 使用测试用例
   - 对比改进效果
   - 总结最佳实践

#### 2. 上下文管理
1. **信息量控制**
   - 必要信息优先
   - 控制上下文长度
   - 保持相关性

2. **结构优化**
   - 清晰的层次
   - 逻辑的顺序
   - 一致的格式

3. **示例选择**
   - 典型案例
   - 边界情况
   - 错误示范

### 常见陷阱

#### 1. 过度复杂
- **问题**：提示词过长，包含过多细节
- **解决**：
  - 聚焦核心需求
  - 删除非必要信息
  - 简化指令结构

#### 2. 指令不明
- **问题**：模糊的要求，含糊的表述
- **解决**：
  - 使用明确的动词
  - 提供具体的例子
  - 指定清晰的格式

#### 3. 缺乏上下文
- **问题**：信息不足，背景缺失
- **解决**：
  - 补充必要背景
  - 提供相关示例
  - 说明具体场景

### 最佳实践总结

1. **清晰性优先**
   - 使用简单直接的语言
   - 避免复杂的嵌套结构
   - 保持指令的可理解性

2. **结构化设计**
   - 使用一致的格式
   - 清晰的层次划分
   - 合理的信息组织

3. **持续优化**
   - 收集使用反馈
   - 记录改进效果
   - 建立最佳实践库

## 课后作业

### 基础练习

1. **参数实验**
   - 使用不同的temperature值（0.2, 0.5, 0.8）生成同一个提示的回答
   - 记录和比较结果的差异
   - 分析哪种参数设置最适合特定类型的任务

2. **提示词优化**
   - 选择一个简单的任务（如：文本摘要）
   - 编写3个不同版本的提示词
   - 对比效果并分析原因
   - 总结提示词改进的原则

3. **对话流程设计**
   - 设计一个多轮对话场景（如：客服对话）
   - 实现基本的对话管理代码
   - 处理常见的错误情况
   - 优化对话体验

### 进阶任务

1. **实现一个简单的聊天机器人**
   ```python
   # 要求：
   # 1. 使用上述代码示例中的ChatSession类
   # 2. 添加基本的对话历史管理
   # 3. 实现错误处理和重试机制
   # 4. 添加基本的成本控制
   ```

2. **开发一个文本分析工具**
   ```python
   # 要求：
   # 1. 使用JSON输出格式控制
   # 2. 实现情感分析和关键词提取
   # 3. 使用响应验证确保输出质量
   # 4. 添加异常处理机制
   ```

3. **构建一个批量处理系统**
   ```python
   # 要求：
   # 1. 使用异步处理多个请求
   # 2. 实现速率限制
   # 3. 添加成本统计
   # 4. 处理并记录错误
   ```

### 挑战项目

1. **智能文档助手**
   - 实现一个能够回答文档相关问题的助手
   - 支持上下文管理和多轮对话
   - 实现文档内容的动态加载
   - 添加响应质量控制机制

2. **代码审查助手**
   - 开发一个自动代码审查工具
   - 使用函数调用处理不同类型的代码问题
   - 实现分批处理大型代码库
   - 生成结构化的审查报告

3. **多模态内容生成器**
   - 结合文本和图像的处理能力
   - 实现基于描述生成内容大纲
   - 支持多种输出格式
   - 添加内容质量控制

### 提交要求

1. **代码规范**
   - 遵循PEP 8规范
   - 添加适当的注释和文档
   - 使用类型提示
   - 实现错误处理

2. **文档要求**
   - README文件说明项目结构
   - 安装和使用说明
   - API文档
   - 示例和测试用例

3. **评分标准**
   - 代码质量（30%）
   - 功能完整性（30%）
   - 创新性（20%）
   - 文档完整性（20%）

### 额外资源

1. **参考资料**
   - OpenAI API文档
   - Python异步编程指南
   - 设计模式参考
   - 测试编写指南

2. **工具推荐**
   - API测试工具
   - 代码质量检查工具
   - 性能分析工具
   - 文档生成工具

3. **提示和建议**
   - 从简单任务开始
   - 逐步添加功能
   - 注重代码复用
   - 保持良好的测试覆盖率

## API使用最佳实践

#### 1. API密钥管理
```python
import os
from dotenv import load_dotenv

def setup_api():
    """
    安全地设置API密钥
    """
    # 从环境变量加载API密钥
    load_dotenv()
    
    # 设置API密钥
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    # 可选：设置组织ID
    if os.getenv('OPENAI_ORG_ID'):
        openai.organization = os.getenv('OPENAI_ORG_ID')
```

#### 2. 请求重试机制
```python
import time
from tenacity import retry, stop_after_attempt, wait_random_exponential

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
async def chat_with_retry(messages, **kwargs):
    """
    实现自动重试的API调用
    """
    try:
        response = await openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            **kwargs
        )
        return response
    except openai.RateLimitError:
        # 处理速率限制
        time.sleep(20)  # 等待20秒后重试
        raise  # 重新抛出异常，让重试装饰器处理
    except Exception as e:
        print(f"发生错误: {e}")
        raise
```

#### 3. 成本控制
```python
class CostManager:
    """
    管理和监控API使用成本
    """
    def __init__(self):
        self.price_per_1k_tokens = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002}
        }
        self.total_tokens = 0
        self.total_cost = 0.0
    
    def calculate_cost(self, response, model="gpt-3.5-turbo"):
        """计算单次请求成本"""
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        
        input_cost = (input_tokens * self.price_per_1k_tokens[model]["input"]) / 1000
        output_cost = (output_tokens * self.price_per_1k_tokens[model]["output"]) / 1000
        
        self.total_tokens += input_tokens + output_tokens
        self.total_cost += input_cost + output_cost
        
        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost": input_cost + output_cost
        }

# 使用示例
cost_manager = CostManager()

async def cost_aware_chat():
    response = await chat_with_retry(
        messages=[{"role": "user", "content": "你好"}]
    )
    
    # 计算成本
    cost_info = cost_manager.calculate_cost(response)
    print(f"本次对话使用token数: {cost_info['total_tokens']}")
    print(f"本次对话成本: ${cost_info['cost']:.4f}")
    print(f"累计成本: ${cost_manager.total_cost:.4f}")
```

#### 4. 响应验证
```python
from pydantic import BaseModel, Field
from typing import List, Optional

class AnalysisResponse(BaseModel):
    """定义预期的响应格式"""
    main_points: List[str] = Field(..., min_items=1)
    sentiment: str = Field(..., pattern="^(positive|negative|neutral)$")
    confidence: float = Field(..., ge=0.0, le=1.0)
    keywords: List[str] = Field(..., min_items=1)
    summary: Optional[str] = None

def validate_response(response_text: str) -> AnalysisResponse:
    """验证API响应是否符合预期格式"""
    try:
        # 尝试解析JSON响应
        response_data = json.loads(response_text)
        # 验证数据结构
        validated_response = AnalysisResponse(**response_data)
        return validated_response
    except Exception as e:
        print(f"响应验证失败: {e}")
        raise

async def get_validated_analysis(text: str):
    """获取经过验证的分析结果"""
    try:
        response = await openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个文本分析助手。请以指定的JSON格式返回分析结果。"
                },
                {
                    "role": "user",
                    "content": f"分析以下文本：{text}"
                }
            ],
            response_format={"type": "json_object"}
        )
        
        # 验证响应
        validated_data = validate_response(response.choices[0].message.content)
        return validated_data
    except Exception as e:
        print(f"获取分析结果失败: {e}")
        return None
```

#### 5. 并发请求控制
```python
import asyncio
from asyncio import Semaphore
from typing import List

class RateLimiter:
    """
    控制API并发请求数量
    """
    def __init__(self, max_concurrent: int = 5):
        self.semaphore = Semaphore(max_concurrent)
        self.current_requests = 0
    
    async def acquire(self):
        """获取请求许可"""
        await self.semaphore.acquire()
        self.current_requests += 1
    
    def release(self):
        """释放请求许可"""
        self.semaphore.release()
        self.current_requests -= 1

rate_limiter = RateLimiter()

async def controlled_request(prompt: str):
    """受控的API请求"""
    await rate_limiter.acquire()
    try:
        response = await chat_with_retry(
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    finally:
        rate_limiter.release()

async def process_multiple_requests(prompts: List[str]):
    """处理多个请求"""
    tasks = [controlled_request(prompt) for prompt in prompts]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

这些代码示例展示了在实际应用中如何安全和高效地使用ChatGPT API。包括：

1. 安全的API密钥管理
2. 可靠的重试机制
3. 成本监控和控制
4. 响应数据验证
5. 并发请求控制

这些实践可以帮助开发者构建更稳定、安全和高效的应用。建议在实际项目中根据具体需求选择和调整这些代码。
