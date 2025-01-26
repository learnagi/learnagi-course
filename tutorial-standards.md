# 教程编写标准


# 规则

受众：针对小白，零基础来学习，要增加更多的概念解释，
要增加一些配图解释


## 文件结构规范

每个教程文件（.md）必须包含以下部分：

```markdown
---
title: "教程标题"
slug: "tutorial-slug"
sequence: 1
description: "简短的描述，说明本节内容和学习收益"
is_published: true
estimated_minutes: 预计完成时间（分钟）
language: "zh-CN"  # 或 "en"
---

![Chapter Title](assets/images/chapter-name/header.png)
*一句简短优美的描述，点明章节主旨*

# 教程标题

## 学习目标
清晰列出完成本节后能够掌握的技能点：
- 技能点1
- 技能点2
- 技能点3

## 先修知识
列出学习本节内容需要的前置知识：
- 前置知识1
- 前置知识2

## 1. 概念讲解
### 1.1 核心概念
简明扼要地解释概念，使用类比和图示。

### 1.2 工作原理
详细解释原理，可以使用图表或动画。

## 2. 代码实现
### 2.1 基础实现
```python
# 提供清晰的代码示例
def example():
    """详细的文档字符串，解释功能和参数"""
    return "Hello, World!"

# 运行示例
print(example())
```

**运行结果：**
```
Hello, World!
```

*结果说明：展示代码的基本功能和输出。*

### 2.2 进阶实现
```python
import numpy as np
import matplotlib.pyplot as plt

class DataVisualizer:
    """数据可视化示例类"""
    def __init__(self, data):
        self.data = data
    
    def plot_distribution(self):
        plt.hist(self.data, bins=30)
        plt.title('数据分布图')
        plt.xlabel('值')
        plt.ylabel('频率')
        plt.show()

# 运行示例
data = np.random.normal(0, 1, 1000)
visualizer = DataVisualizer(data)
visualizer.plot_distribution()
```

**运行结果：**
![数据分布图](images/data-distribution.png)

*结果说明：展示了如何创建数据可视化，包括图表输出。*

## 3. 实战项目
### 3.1 项目描述
- 项目目标
- 技术要点
- 预期结果

### 3.2 实现步骤
1. 步骤1
2. 步骤2
3. 步骤3

### 3.3 完整代码
```python
# 项目完整代码
# 包含必要的注释和文档
```

## 练习与作业
提供3-5个练习题，难度递增：
1. 基础练习
2. 提高练习
3. 挑战练习

## 常见问题
Q1: 问题1
A1: 详细解答

Q2: 问题2
A2: 详细解答

## 小测验
包含3-5个问题，检验学习效果：
1. 概念理解题
2. 代码实现题
3. 应用场景题

## 扩展阅读
提供进一步学习的资源：
- 相关文档
- 学术论文
- 在线教程
- 推荐书籍

## 下一步学习
指明学习路径：
- 下一个主题
- 进阶内容
- 相关领域

### 题图设计规范

#### 2.2.1 基本要求
- 位置：元数据后，正文前
- 尺寸：1024px × 400px（DALL-E 3生成尺寸）
- 格式：PNG格式，≤500KB
- 存储：`chapter-name/images/header.png`

#### 2.2.2 设计风格
- 扁平化设计（Flat Design）
- 简洁现代的插画风格
- 抽象几何元素
- 柔和的配色方案
- 适当的留白
- 避免过于复杂的细节

#### 2.2.3 DALL-E 提示词模板
```
A minimalist flat design illustration for [主题], using a modern and clean style. The image should feature [核心元素] with [风格描述]. Use a [配色方案] color palette. The design should be simple yet professional, suitable for a technical tutorial header.
```

示例提示词：

1. 机器学习基础：
```
A minimalist flat design illustration representing machine learning basics. Simple geometric shapes showing data points, patterns, and connections. Use soft blues and teals with clean white space. Include abstract representations of algorithms and data structures. Modern tech education style, no text.
```

2. 神经网络：
```
A flat design illustration of neural network concepts. Minimal connected nodes and pathways in a geometric pattern. Use gentle purples and blues. Abstract representation of data flow and neural connections. Clean and modern educational style, no text.
```

3. 深度学习：
```
A minimalist flat illustration for deep learning concepts. Layered geometric patterns representing neural network depth. Soft gradients in blue and purple. Include abstract data flow representations. Modern technical style, no text.
```

#### 2.2.4 配色方案
建议使用以下配色：
- 主色调：柔和的蓝色、紫色、青色
- 辅助色：浅灰、白色
- 强调色：深蓝、深紫
- 背景色：纯白或极浅的灰色

配色示例：
```
主色调：#4A90E2, #9B51E0
辅助色：#F5F7FA, #E0E6ED
强调色：#2C3E50, #8E44AD
背景色：#FFFFFF, #F8F9FA
```

#### 2.2.5 图片配文要求
- 简短优美，点明主旨
- 使用斜体格式
- 中英文版本保持一致
- 长度控制在20字以内

示例配文：
- *机器学习，数据中的智慧探索*
- *神经网络，模仿大脑的数字建筑*
- *深度学习，层层递进的知识表达*

#### 2.2.6 图片优化
1. 导出设置
   - 分辨率：72 DPI
   - 色彩模式：RGB
   - 格式：PNG-24

2. 压缩优化
   - 使用 TinyPNG 压缩
   - 保持视觉质量
   - 控制文件大小 ≤500KB

3. 响应式考虑
   - 保证在不同设备上的清晰度
   - 预留适当边距
   - 避免重要细节靠近边缘

#### 2.2.7 AI图像生成工具对比

1. **DALL-E 3 (OpenAI)**
   - 优点：
     - 最佳的文本理解能力
     - 高质量的细节表现
     - 优秀的构图能力
     - 支持精确的风格控制
   - 缺点：
     - 价格相对较高
     - 生成速度较慢
   - 适用场景：需要精确控制和高质量输出的专业场景

2. **Midjourney**
   - 优点：
     - 最佳的艺术效果
     - 独特的视觉风格
     - 优秀的光影效果
     - 强大的创意表现
   - 缺点：
     - 需要通过Discord使用
     - 提示词要求较高
   - 适用场景：需要艺术感和创意表现的场景

3. **Stable Diffusion**
   - 优点：
     - 开源免费
     - 可本地部署
     - 高度可定制
     - 支持多种模型
   - 缺点：
     - 需要较强的技术背景
     - 效果依赖模型质量
   - 适用场景：需要自定义和本地部署的场景

4. **Adobe Firefly**
   - 优点：
     - 与Adobe生态集成
     - 商业使用友好
     - 专注于设计场景
     - 支持图片编辑
   - 缺点：
     - 仍在测试阶段
     - 功能相对有限
   - 适用场景：设计师和Adobe用户

5. **Canva Text to Image**
   - 优点：
     - 与Canva集成
     - 使用简单直观
     - 适合设计场景
     - 价格合理
   - 缺点：
     - 功能相对基础
     - 风格选择有限
   - 适用场景：简单的设计需求

#### 2.2.8 不同工具的提示词策略

1. **DALL-E 3提示词**：
```
A minimalist flat design illustration for [主题], modern and clean style...
```

2. **Midjourney提示词**：
```
minimalist flat illustration of [主题], vector art style, clean lines, geometric shapes, soft gradients --ar 16:9 --v 5
```

3. **Stable Diffusion提示词**：
```
minimalist flat design, [主题], vector graphics style, clean modern illustration, geometric patterns, soft colors, professional technical diagram
```

4. **Adobe Firefly提示词**：
```
Create a flat design illustration for [主题] using minimal geometric shapes and soft colors
```

5. **Canva提示词**：
```
Modern flat design technical illustration of [主题] with geometric elements
```

#### 2.2.9 工具选择建议

1. **教程题图首选**：
   - DALL-E 3：最佳文本理解和专业表现
   - Adobe Firefly：商业友好且设计导向

2. **概念图解首选**：
   - Stable Diffusion：可自定义且成本效益高
   - Midjourney：需要特殊艺术效果时

3. **快速原型首选**：
   - Canva：快速且易用
   - Adobe Firefly：设计师友好

4. **商业项目考虑因素**：
   - 版权清晰度
   - 使用成本
   - 定制化需求
   - 生产效率

5. **生产流程建议**：
   1. 使用Canva快速原型
   2. DALL-E 3生成正式版本
   3. 必要时用Photoshop微调
   4. TinyPNG优化压缩

## 内容质量标准

### 1. 知识点覆盖
- 完整性：覆盖主题的所有关键概念
- 准确性：内容必须准确无误
- 时效性：使用最新的技术和方法

### 2. 代码规范
- 可运行：所有代码必须经过测试，确保可以运行
- 规范性：遵循PEP 8编码规范
- 注释：包含详细的注释和文档字符串

### 3. 示例要求
- 实用性：使用实际场景的例子
- 递进性：从简单到复杂
- 完整性：提供完整的输入输出

### 4. 项目设计
- 实战性：解决实际问题
- 综合性：涵盖多个知识点
- 可扩展：留有提高空间

### 5. 交互性
- 练习：提供足够的练习机会
- 反馈：包含自测题目
- 讨论：鼓励思考和探索

## 写作风格指南

### 1. 语言要求
- 清晰：使用简洁明了的语言
- 专业：使用准确的专业术语
- 一致：术语使用保持一致

### 2. 结构组织
- 层次：层次分明，逻辑清晰
- 递进：由浅入深，循序渐进
- 关联：前后内容有机联系

### 3. 格式规范
- 标题：使用统一的标题层级
- 代码：使用正确的代码块格式
- 图表：提供清晰的图表说明

### 4. 可读性增强
- 强调：适当使用加粗和斜体
- 列表：使用项目符号和编号
- 图示：适时使用图表和图示

## 质量检查清单

### 1. 内容检查
- [ ] 知识点完整覆盖
- [ ] 概念解释准确清晰
- [ ] 示例代码可以运行
- [ ] 项目实战具有实用性

### 2. 结构检查
- [ ] 章节结构完整
- [ ] 内容层次分明
- [ ] 学习路径清晰
- [ ] 练习难度适中

### 3. 格式检查
- [ ] Markdown格式正确
- [ ] 代码格式规范
- [ ] 图表清晰美观
- [ ] 链接有效可用

### 4. 交互检查
- [ ] 练习题目合理
- [ ] 测验覆盖重点
- [ ] 提供完整解答
- [ ] 扩展资源可用

---
title: "教程编写标准"
slug: "tutorial-standards"
sequence: 1
description: "详细的教程编写标准和规范，包括内容组织、代码规范、和质量要求"
is_published: true
estimated_minutes: 45
language: "zh-CN"
---

![Tutorial Standards](foundations/images/header.png)
*规范的教程，如同精心设计的建筑，需要严谨的标准和优雅的结构*

# 教程编写标准

## 1. 文件组织规范

### 1.1 目录结构
```
repository/
├── README.md                    # 教程总体介绍
├── contributing-guide.md        # 贡献指南
├── tutorial-standards.md        # 教程标准
├── foundations/                 # 基础概念目录
│   ├── README.md               # 章节说明
│   ├── images/                 # 章节相关图片
│   │   ├── header.png         # 章节题图
│   │   └── *.png              # 其他图片
│   └── *.md                    # 具体小节
├── deep-learning/              # 深度学习目录
│   ├── README.md              # 章节说明
│   ├── images/                # 章节相关图片
│   │   ├── header.png        # 章节题图
│   │   └── *.png             # 其他图片
│   └── *.md                   # 具体小节
└── advanced-topics/            # 进阶主题目录
    ├── README.md              # 章节说明
    ├── images/                # 章节相关图片
    │   ├── header.png        # 章节题图
    │   └── *.png             # 其他图片
    └── *.md                   # 具体小节
```

### 1.2 文件命名规范

#### 1.2.1 Markdown文件
- 使用小写字母和连字符
- 保持简短且描述性
- 示例：`neural-networks.md`, `data-preprocessing.md`

#### 1.2.2 图片文件
- 章节题图：`header.png`
- 内容图片：`{section-name}_{description}.png`
- 示例：
  - `neural-networks/images/header.png`
  - `neural-networks/images/activation_functions.png`
  - `neural-networks/images/network_architecture.png`

## 2. 内容结构规范

### 2.1 元数据要求
```markdown
---
title: "教程标题"
slug: "tutorial-slug"
sequence: 1
description: "简短的描述"
is_published: true
estimated_minutes: 预计时间
language: "zh-CN"
translations:
  en: "filename.en.md"
---
```

### 2.2 题图规范
- 位置：元数据后，正文前
- 尺寸：1024px × 400px（DALL-E 3生成尺寸）
- 格式：PNG格式，≤500KB
- 存储：`chapter-name/images/header.png`

### 2.3 章节结构
1. 学习目标
2. 先修知识
3. 概念讲解
4. 代码实现
5. 实战项目
6. 练习作业
7. 常见问题
8. 小测验
9. 扩展阅读
10. 下一步学习

## 3. 代码规范

### 3.1 代码质量要求
- 遵循PEP 8规范
- 完整的类型注解
- 详细的文档字符串
- 单元测试覆盖
- 性能优化考虑

### 3.2 代码示例格式
```python
def example_function(param1: int, param2: str) -> bool:
    """函数功能的详细描述。

    Args:
        param1: 参数1的说明
        param2: 参数2的说明

    Returns:
        返回值的说明

    Examples:
        >>> example_function(1, "test")
        True
    """
    pass
```

### 3.3 代码安全
- 敏感信息处理
- API密钥管理
- 错误处理
- 输入验证

## 4. 资源管理规范

### 4.1 图片资源
- 命名规范：`{chapter-name}_{description}.{ext}`
- 压缩优化
- 适当的分辨率
- Alt文本规范

### 4.2 代码资源
- 完整示例代码
- requirements.txt
- 运行说明
- 测试用例

### 4.3 数据资源
- 示例数据集
- 数据格式说明
- 数据隐私考虑
- 许可说明

## 5. 质量保证规范

### 5.1 自动化检查
```bash
# Markdown检查
markdownlint *.md

# Python代码检查
pylint *.py
black *.py
mypy *.py

# 测试运行
pytest tests/
```

### 5.2 质量指标
- 代码测试覆盖率 > 80%
- 代码复杂度 < 15
- 文档完整性 100%
- 用户评分 > 4.5/5

### 5.3 评审流程
1. 自动化检查
2. 同行评审
3. 专家审核
4. 用户反馈

## 6. 写作风格指南

### 6.1 语言要求
- 清晰简洁
- 专业准确
- 前后一致
- 循序渐进

### 6.2 专业术语
| 中文术语 | English Term | 说明/Notes |
|---------|--------------|------------|
| 神经网络 | Neural Network | 基本概念 |
| 深度学习 | Deep Learning | 进阶概念 |

### 6.3 格式规范
- 标题层级：最多4级
- 代码块：指定语言
- 图表：清晰的说明
- 引用：规范的格式

## 7. 发布检查清单

### 7.1 内容检查
- [ ] 知识点完整
- [ ] 代码可运行
- [ ] 示例充分
- [ ] 练习合理

### 7.2 格式检查
- [ ] Markdown正确
- [ ] 图片完整
- [ ] 链接有效
- [ ] 代码规范

### 7.3 资源检查
- [ ] 图片已优化
- [ ] 代码已测试
- [ ] 数据已处理
- [ ] 依赖已更新

## 8. 维护更新规范

### 8.1 版本控制
- 语义化版本号
- 更新日志维护
- 重大变更说明

### 8.2 反馈处理
- 问题跟踪
- 更新计划
- 用户沟通

### 8.3 内容更新
- 定期审查
- 技术更新
- 错误修正
- 示例更新

## 参考资源

- [Google Style Guides](https://google.github.io/styleguide/)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Technical Writing Courses](https://developers.google.com/tech-writing)
