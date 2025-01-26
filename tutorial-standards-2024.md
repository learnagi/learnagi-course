# 教程编写标准 2024更新

## 内容组织规范

### 1. 教程结构
每个教程应包含以下基本组成部分：

#### 1.1 头部信息
```markdown
---
title: "教程标题"
slug: "tutorial-slug"
sequence: 1  # 教程在系列中的顺序号
description: "简短的描述，说明本节内容和学习收益"
is_published: true
estimated_minutes: 预计完成时间（分钟）
language: "zh-CN"  # 或 "en"
---
```

#### 1.2 封面图片
- 使用高质量的封面图片，突出主题
- 添加简短优美的描述，点明章节主旨
```markdown
![章节标题](./images/chapter-title.png)
*一句话描述章节主旨*
```

#### 1.3 学习概要（替代传统目录）
必须包含以下两部分：
```markdown
## 本节概要

通过本节学习，你将学会：
- 列出3-5个具体的学习目标
- 使用动词开头，如"理解"、"掌握"、"学会"
- 确保目标具体且可衡量

💡 重点内容：
- 3-4个核心知识点
- 使用简洁的语言
- 突出实践价值
```

### 2. 图片规范

#### 2.1 命名规则
- 使用有意义的语义化名称
- 采用小写字母和连字符
- 格式：`{主题}-{具体内容}.png`
- 示例：
  - `linear-regression-intro.png`
  - `data-distribution-example.png`
  - `model-comparison.png`

#### 2.2 图片管理流程（SOP）

1. **本地生成**
   ```python
   # 在教程目录下创建generate_images.py
   import matplotlib.pyplot as plt
   import numpy as np
   
   def generate_images():
       # 1. 设置matplotlib样式
       plt.style.use('seaborn')
       plt.rcParams['figure.figsize'] = [10, 6]
       plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 支持中文
       
       # 2. 生成图片
       fig, ax = plt.subplots()
       # ... 绘图代码 ...
       
       # 3. 保存到images目录
       plt.savefig('images/example-plot.png', 
                  dpi=300, 
                  bbox_inches='tight',
                  pad_inches=0.1)
       plt.close()
   
   if __name__ == '__main__':
       generate_images()
   ```

2. **目录结构**
   ```
   ml-basics/
   ├── images/                    # 本地图片目录
   │   ├── classification/        # 按教程分类
   │   │   ├── overview.png
   │   │   └── logistic-regression.png
   │   └── linear-regression/
   │       ├── intro.png
   │       └── comparison.png
   ├── generate_images.py         # 图片生成脚本
   └── classification.md          # 教程文档
   ```

3. **图片生成流程**
   ```bash
   # 1. 生成图片
   cd ml-basics
   python generate_images.py
   
   # 2. 检查图片质量
   open images/classification/*.png
   
   # 3. 上传到CDN
   python ../tools/upload_images_to_cdn.py classification.md
   ```

4. **图片引用规范**
   - 在markdown中首先使用本地路径
   ```markdown
   ![分类算法概述](./images/classification/overview.png)
   ```
   - 上传到CDN后更新为CDN路径
   ```markdown
   ![分类算法概述](https://z1.zve.cn/tutorial/classification/overview.png)
   ```

5. **图片更新流程**
   - 修改generate_images.py生成新图片
   - 在本地确认图片效果
   - 提交代码，包含：
     1. generate_images.py的修改
     2. 新生成的图片文件
     3. 教程文档的更新
   - 上传到CDN并更新文档中的链接
   - 再次提交文档更新

6. **图片质量要求**
   - 分辨率：至少300dpi
   - 格式：优先使用PNG格式
   - 大小：单张图片不超过500KB
   - 配色：使用统一的配色方案
   - 字体：使用支持中文的无衬线字体

7. **版本控制**
   - 图片文件必须纳入版本控制
   - 保留generate_images.py的修改历史
   - 图片更新时同时更新生成脚本

#### 2.3 CDN托管
- 所有图片需上传到七牛云
- 使用语义化的文件名，保持与本地文件名一致
- CDN URL格式：`https://z1.zve.cn/tutorial/{教程名}/{filename}.png`
  - 例如：`https://z1.zve.cn/tutorial/classification/logistic-regression.png`

### 3. 代码示例规范

#### 3.1 代码展示
- 提供完整的可运行代码
- 包含必要的导入语句
- 添加详细的注释说明
- 展示运行结果和可视化输出

#### 3.2 结果展示
```markdown
**运行结果：**
![结果说明图](./images/result-visualization.png)
*结果说明：简要解释图表含义和关键发现*
```

### 4. 文档更新流程

#### 4.1 提交规范
- commit message格式：
  - feat: 新增内容或功能
  - docs: 文档更新
  - fix: 内容修复
  - style: 格式调整
- 示例：
```
docs: 优化线性回归教程结构，添加学习概要

1. 删除冗长的目录结构
2. 添加本节概要，清晰展示学习目标
3. 突出重点内容
```

#### 4.2 图片更新流程
1. 准备新图片，遵循命名规范
2. 将图片放入对应的 `images` 目录
3. 更新文档中的图片引用
4. 运行上传工具同步到CDN
5. 提交代码，包含图片文件和文档更新

### 5. 最佳实践总结

#### 5.1 内容组织
- 删除冗长的目录，用学习概要替代
- 每个概念配备实例和图示
- 使用emoji标注重点内容（如 💡）
- 保持语言简洁清晰

#### 5.2 图片管理
- 统一的命名规范
- 本地和CDN保持同步
- 图片名称要有意义
- 及时清理未使用的图片

#### 5.3 代码展示
- 完整的运行环境
- 清晰的注释说明
- 展示实际运行效果
- 解释关键输出结果
