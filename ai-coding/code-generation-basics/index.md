# 代码生成基础

## 课程目标
- 理解AI代码生成的基本原理
- 掌握代码生成的最佳实践
- 学习如何有效利用AI辅助编程

## 代码生成概述
### 1. 什么是AI代码生成
- 定义和原理
- 工作机制
- 应用场景

### 2. 主流工具介绍
- GitHub Copilot
- Amazon CodeWhisperer
- Codeium
- Tabnine

## 基础提示技巧
### 1. 代码生成提示
```
请生成一个函数，要求：
- 功能：读取CSV文件并进行数据处理
- 输入参数：文件路径，列名列表
- 返回值：处理后的DataFrame
- 错误处理：文件不存在，格式错误等
- 注释：包含完整的文档字符串
```

### 2. 注释生成
```
# 为以下函数生成详细的文档字符串：
def process_data(file_path: str, columns: List[str]) -> pd.DataFrame:
    """
    [请在这里生成详细的文档字符串，包括：
    1. 函数功能描述
    2. 参数说明
    3. 返回值说明
    4. 异常说明
    5. 使用示例]
    """
```

### 3. 测试用例生成
```
# 为以下函数生成单元测试：
def calculate_discount(price: float, discount_rate: float) -> float:
    if not (0 <= discount_rate <= 1):
        raise ValueError("Discount rate must be between 0 and 1")
    return price * (1 - discount_rate)
```

## 代码生成模式
### 1. 函数生成
```python
def generate_function_template(name, params, return_type, description):
    """生成函数模板
    
    Args:
        name (str): 函数名
        params (dict): 参数字典
        return_type (str): 返回类型
        description (str): 函数描述
    
    Returns:
        str: 生成的函数代码
    """
    pass
```

### 2. 类生成
```python
class UserManager:
    """用户管理类
    
    属性：
        - users: 用户列表
        - db_connection: 数据库连接
    
    方法：
        - add_user: 添加用户
        - remove_user: 删除用户
        - update_user: 更新用户
        - get_user: 获取用户信息
    """
    pass
```

### 3. API生成
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """获取用户信息
    
    参数：
        - user_id: 用户ID
    
    返回：
        - user_info: 用户信息字典
    """
    pass
```

## 代码质量控制
### 1. 代码风格
- PEP 8规范
- 命名约定
- 注释规范
- 类型提示

### 2. 错误处理
```python
def safe_division(a: float, b: float) -> float:
    """安全除法运算
    
    Args:
        a (float): 被除数
        b (float): 除数
    
    Returns:
        float: 除法结果
    
    Raises:
        ValueError: 当除数为0时
        TypeError: 当输入类型不正确时
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be numbers")
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### 3. 性能考虑
- 算法复杂度
- 内存使用
- 并发处理
- 资源管理

## 实践技巧
### 1. 增量生成
```
1. 首先生成基本框架
2. 逐步添加功能
3. 优化和完善
4. 添加测试
```

### 2. 代码重构
```python
# 重构前
def process(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result

# 重构后
def process(data: List[float]) -> List[float]:
    """处理数值列表，将正数翻倍
    
    Args:
        data (List[float]): 输入数值列表
    
    Returns:
        List[float]: 处理后的列表
    """
    return [item * 2 for item in data if item > 0]
```

### 3. 代码优化
- 性能优化
- 可读性优化
- 维护性优化
- 扩展性优化

## 常见应用场景
### 1. Web开发
```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    """获取数据接口
    
    Query参数：
        - page: 页码
        - size: 每页数量
    
    返回：
        - data: 数据列表
        - total: 总数
        - page: 当前页
    """
    pass
```

### 2. 数据处理
```python
import pandas as pd
import numpy as np

def process_dataset(file_path: str) -> pd.DataFrame:
    """处理数据集
    
    步骤：
    1. 读取数据
    2. 清洗数据
    3. 特征工程
    4. 数据转换
    """
    pass
```

### 3. 自动化测试
```python
import unittest

class TestCalculator(unittest.TestCase):
    """计算器测试类
    
    测试用例：
    1. 测试加法
    2. 测试减法
    3. 测试异常情况
    """
    pass
```

## 最佳实践
### 1. 代码生成准则
- 明确需求
- 分步骤生成
- 及时验证
- 持续优化

### 2. 文档和注释
- 完整的文档
- 清晰的注释
- 代码示例
- 使用说明

### 3. 测试和验证
- 单元测试
- 集成测试
- 性能测试
- 安全测试

## 常见问题
### 1. 代码质量
- 问题：生成的代码质量不稳定
- 解决：使用代码检查工具，设定质量标准

### 2. 依赖管理
- 问题：版本冲突
- 解决：使用虚拟环境，明确依赖版本

### 3. 安全隐患
- 问题：潜在的安全问题
- 解决：代码审查，安全扫描

## 练习作业
1. 基础函数生成
2. 类和接口设计
3. API开发实践
4. 测试用例编写

## 参考资源
- [GitHub Copilot文档](https://docs.github.com/en/copilot)
- [Python编码规范](https://www.python.org/dev/peps/pep-0008/)
- [软件测试最佳实践](https://docs.python.org/3/library/unittest.html)