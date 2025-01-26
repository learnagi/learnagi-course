# 环境搭建

## 课程目标
- 掌握 AI 开发环境的基本配置
- 了解不同 LLM 开发框架的特点
- 能够独立搭建完整的开发环境

## 环境要求
### 硬件要求
- CPU: 4核及以上
- 内存: 16GB及以上
- 硬盘空间: 20GB以上
- GPU: 推荐但不强制要求

### 软件要求
- Python 3.8+
- pip 包管理器
- Git 版本控制
- 代码编辑器 (VS Code推荐)

## 开发环境配置
### 1. Python环境配置
```bash
# 创建虚拟环境
python -m venv llm-env
source llm-env/bin/activate  # Linux/Mac
.\llm-env\Scripts\activate   # Windows
```

### 2. 基础依赖安装
```bash
pip install -r requirements.txt
```

必要的基础包包括：
- openai
- langchain
- transformers
- torch
- numpy
- pandas

### 3. IDE配置
VS Code推荐插件：
- Python
- Jupyter
- GitLens
- Python Docstring Generator

## API密钥配置
### 1. OpenAI API
- 注册OpenAI账号
- 获取API密钥
- 配置环境变量

### 2. 其他模型API
- Anthropic Claude
- Google PaLM
- Azure OpenAI

## 本地开发环境
### 1. 代码版本控制
```bash
git init
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2. 项目结构设置
```
project/
├── src/
├── tests/
├── notebooks/
├── data/
├── config/
└── requirements.txt
```

## 云端开发环境
### 1. Google Colab配置
- 免费GPU资源
- Jupyter环境
- 协作功能

### 2. Hugging Face Spaces
- 模型部署
- 应用托管
- 社区资源

## 开发最佳实践
### 1. 环境管理
- 使用虚拟环境
- 依赖版本控制
- 环境变量管理

### 2. 代码组织
- 模块化结构
- 配置分离
- 日志记录

### 3. 安全实践
- API密钥保护
- 访问控制
- 数据安全

## 常见问题解决
### 1. 依赖冲突
- 版本兼容性检查
- 依赖树分析
- 虚拟环境隔离

### 2. API连接问题
- 网络代理设置
- 身份验证
- 错误处理

## 练习作业
1. 完整配置开发环境
2. 测试API连接
3. 创建基础项目结构
4. 编写环境测试脚本

## 参考资源
- [Python官方文档](https://docs.python.org/)
- [OpenAI API文档](https://platform.openai.com/docs/)
- [VS Code Python教程](https://code.visualstudio.com/docs/python/python-tutorial)