# Contributing Guide

## Directory Structure

```
repository/
├── README.md                # Tutorial information (双语)
├── contributing-guide.md    # Contribution guidelines
├── foundations/            # Basic concepts directory (基础概念)
│   ├── README.md          # Chapter information
│   ├── introduction.md    # Introduction to ML (机器学习简介)
│   └── math_basics.md     # Mathematical foundations (数学基础)
└── advanced-topics/       # Advanced topics directory (进阶主题)
    ├── README.md
    └── deep-learning.md   # Deep learning concepts (深度学习)
```

## File Format Requirements

### Tutorial README.md
```markdown
---
title: "Tutorial Title"
slug: "tutorial-slug"
description: "Tutorial description"
author: "Author Name"
status: "published"  # or "draft"
created_at: "2024-01-01"
updated_at: "2024-01-01"
---

# Tutorial Title

Tutorial content...
```

### Chapter README.md
```markdown
---
title: "Chapter Title"
slug: "chapter-slug"
sequence: 1
description: "Chapter description"
status: "published"  # or "draft"
---

# Chapter Title

Chapter content...
```

### Section Content (*.md)
```markdown
---
title: "Section Title"
slug: "section-slug"
sequence: 1
description: "Section description"
is_published: true  # or false
estimated_minutes: 10
---

# Section Title

Section content...
```

## Content Update Guidelines

1. **File Naming**
   - Use lowercase English letters only
   - Use hyphens for spaces
   - Keep names short and descriptive
   - Use English names for files regardless of content language
   - Example: `machine-learning-intro.md`, `neural-networks.md`

2. **Content Organization**
   - Each chapter must have its own directory
   - Each directory must have a README.md
   - Sections must be .md files
   - Follow the sequence numbers for ordering

3. **Metadata Fields**
   - `title`: Display name (支持中文)
   - `slug`: URL-friendly identifier (English only)
   - `sequence`: Order number
   - `description`: Brief summary (支持中文)
   - `status/is_published`: Content visibility
   - `estimated_minutes`: Estimated reading time (sections only)
   - `language`: Content primary language ("zh-CN" or "en")
   - `translations`: Object containing translated versions

4. **Content Writing**
   - Write in clear and concise language
   - Support bilingual content (Chinese and English)
   - Include practical code examples
   - Add descriptive comments in code
   - Place images in an `assets` subdirectory
   - Use relative paths for all resources
   - Maintain consistent formatting across languages
   - Add bilingual variable names in code examples when necessary

## Update Process

1. **Before Making Changes**
   ```bash
   # Pull latest changes
   git pull origin main
   
   # Create new branch
   git checkout -b feature/update-content
   ```

2. **Making Changes**
   - Update content following the format guidelines
   - Test content rendering locally
   - Verify all links and references

3. **Testing Changes**
   ```bash
   # Run sync command
   php artisan tutorial:sync-repository /path/to/repository
   
   # Check sync report
   cat storage/logs/tutorial-sync-*.log | tail -n 1
   ```

4. **Committing Changes**
   ```bash
   # Stage changes
   git add .
   
   # Commit with descriptive message
   git commit -m "update: [Chapter/Section] - Brief description"
   
   # Push changes
   git push origin feature/update-content
   ```

5. **Creating Pull Request**
   - Create PR on GitHub
   - Add description of changes
   - Request review if needed
   - Wait for approval

## Best Practices

1. **Content Quality**
   - Maintain consistent formatting
   - Check spelling and grammar
   - Ensure technical accuracy
   - Keep content up-to-date

2. **Collaboration**
   - Communicate changes with team
   - Review others' contributions
   - Provide constructive feedback
   - Follow project guidelines

3. **Version Control**
   - Make atomic commits
   - Write clear commit messages
   - Keep branches up to date
   - Resolve conflicts promptly

4. **Documentation**
   - Update related documentation
   - Add comments where needed
   - Document complex procedures
   - Keep README files current

## Need Help?

If you have questions or need assistance:
1. Check existing documentation
2. Review past commits and PRs
3. Contact project maintainers
4. Open an issue for discussion

Remember: Quality content helps everyone learn better!

## URL 规范

### 链接格式
- 所有教程链接应使用完整的 URL 格式
- 基础 URL: `https://www.agi01.com/course/agi/`
- 链接结构: `https://www.agi01.com/course/agi/{chapter-name}/{section-name}`

示例：
```markdown
- 正确: [AI 基础概念](https://www.agi01.com/course/agi/ai-fundamentals/basic-concepts)
- 错误: [AI 基础概念](ai-fundamentals/basic-concepts/index.md)
```

### 命名规则
- 章节名称（chapter-name）：使用小写字母和连字符
  - 示例：`ai-fundamentals`, `python-basics`
- 小节名称（section-name）：使用小写字母和连字符
  - 示例：`basic-concepts`, `environment-setup`
- 不要在 URL 中包含文件扩展名

### 链接检查
- 确保所有链接都使用完整的 URL
- 验证链接格式是否符合规范
- 检查链接是否可访问

## 目录结构规范

### 基本规则
1. 每个章节对应一个目录
2. 章节目录下只允许有文件，不允许有子目录
3. 文件名即为小节名称
4. 所有文件名使用小写字母和连字符

### 标准目录结构
```
repository/
├── README.md                    # 课程主页
├── contributing-guide.md        # 贡献指南
└── chapters/                    # 所有章节
    ├── getting-started/         # 第1章
    │   ├── intro-llm.md        # 小节1
    │   ├── learning-path.md    # 小节2
    │   └── environment-setup.md # 小节3
    └── python-basics/          # 第2章
        ├── basic-syntax.md     # 小节1
        └── advanced-usage.md   # 小节2
```

### 命名规范
- 章节目录名：使用 slug 格式
  - 示例：`getting-started`, `python-basics`
- 小节文件名：使用 slug 格式，不包含子目录
  - 示例：`intro-llm.md`, `basic-syntax.md`
- 不允许使用以下命名方式：
  - ❌ `getting-started/basics/intro.md`  # 不允许子目录
  - ❌ `Getting-Started.md`  # 不允许大写
  - ❌ `intro_llm.md`  # 不允许下划线

### URL 规范
- 基础 URL: `https://www.agi01.com/course/agi/`
- 链接结构: `https://www.agi01.com/course/agi/{chapter-slug}/{section-slug}`
- 示例：
  ```markdown
  [认识大模型开发](https://www.agi01.com/course/agi/getting-started/intro-llm)
  ```

### 章节标题格式
- 在 README.md 中的章节标题需要包含 slug
- 格式：`### 章节名称 (chapter-slug)`
- 示例：`### 1. 大模型开发学习指南 (getting-started)`

### 文件内容规范
每个 .md 文件都必须包含以下元数据：
```markdown
---
title: "小节标题"
slug: "section-slug"
description: "小节描述"
status: "published"
created_at: "2024-03-19"
updated_at: "2024-03-19"
---
```

### 重要约束
1. 严格遵守目录层级：章节/小节
2. 不允许创建多级目录结构
3. 所有资源文件（图片等）需放在专门的 assets 目录
4. 保持文件命名的一致性和规范性

## 提交规范

### Commit 消息格式
```bash
type(scope): description

[optional body]
[optional footer]
```

### Type 类型
- `feat`: 新功能或内容
- `fix`: 修复错误
- `docs`: 文档更新
- `style`: 格式调整
- `refactor`: 重构
- `chore`: 维护性工作

### Scope 范围
- `chapter`: 章节内容
- `structure`: 目录结构
- `meta`: 元数据
- `assets`: 资源文件
- `config`: 配置文件

### 示例
```bash
# 添加新章节
git commit -m "feat(chapter): add getting-started chapter content"

# 更新文档
git commit -m "docs(meta): update contributing guide with commit standards"

# 修复格式
git commit -m "fix(style): correct markdown formatting in python basics"

# 重构结构
git commit -m "refactor(structure): reorganize directory layout"
```

### 提交建议
1. 每次提交保持原子性，只做一件事
2. 提交信息清晰描述改动
3. 遵循约定的格式规范
4. 及时提交，避免大量积压

### 工作流程
1. 创建新分支
```bash
git checkout -b feat/new-chapter
```

2. 进行修改并提交
```bash
git add .
git commit -m "feat(chapter): add new chapter content"
```

3. 推送分支
```bash
git push origin feat/new-chapter
```

4. 创建 Pull Request
- 标题遵循 commit 消息格式
- 详细描述改动内容
- 关联相关 Issue
