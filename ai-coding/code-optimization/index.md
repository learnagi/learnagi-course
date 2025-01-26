# 代码优化与重构

## 课程目标
- 掌握代码优化的核心原则
- 学习常见的重构模式
- 理解性能优化的关键点

## 代码优化基础
### 1. 什么是代码优化
- 定义与目的
- 优化维度
- 优化原则

### 2. 优化目标
- 可读性
- 性能
- 可维护性
- 可扩展性

## 代码重构
### 1. 重构原则
- 单一职责
- 开闭原则
- 依赖倒置
- 接口隔离
- 里氏替换

### 2. 常见重构模式
```python
# 1. 提取方法
# 重构前
def process_user_data(user):
    print(f"Processing user: {user['name']}")
    # 复杂的数据处理逻辑
    age = calculate_age(user['birth_date'])
    salary = calculate_salary(user['position'], user['experience'])
    tax = calculate_tax(salary)
    return {'age': age, 'salary': salary, 'tax': tax}

# 重构后
def process_user_data(user):
    print(f"Processing user: {user['name']}")
    return {
        'age': calculate_age(user['birth_date']),
        'salary': calculate_salary(user),
        'tax': calculate_tax(user)
    }

def calculate_salary(user):
    return calculate_base_salary(user['position']) * get_experience_multiplier(user['experience'])
```

### 3. 代码清理
```python
# 重构前
def get_user_info(user_id):
    try:
        user = db.query(f"SELECT * FROM users WHERE id = {user_id}")
        if user:
            data = {"id": user[0], "name": user[1], "email": user[2]}
            return data
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# 重构后
def get_user_info(user_id: int) -> Dict[str, Any]:
    """获取用户信息
    
    Args:
        user_id (int): 用户ID
    
    Returns:
        Dict[str, Any]: 用户信息字典
    
    Raises:
        DatabaseError: 数据库查询错误
        UserNotFoundError: 用户不存在
    """
    try:
        user = user_repository.find_by_id(user_id)
        return user.to_dict() if user else None
    except DatabaseError as e:
        logger.error(f"Database error while fetching user {user_id}: {e}")
        raise
```

## 性能优化
### 1. 算法优化
```python
# 优化前：O(n^2)
def find_pairs(numbers, target):
    pairs = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                pairs.append((numbers[i], numbers[j]))
    return pairs

# 优化后：O(n)
def find_pairs(numbers, target):
    seen = set()
    pairs = []
    for num in numbers:
        complement = target - num
        if complement in seen:
            pairs.append((complement, num))
        seen.add(num)
    return pairs
```

### 2. 数据结构优化
```python
# 优化前：使用列表
def check_duplicates(items):
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False

# 优化后：使用集合
def check_duplicates(items):
    return len(set(items)) < len(items)
```

### 3. 内存优化
```python
# 优化前：一次性加载所有数据
def process_large_file(filename):
    with open(filename) as f:
        data = f.readlines()
    return [process_line(line) for line in data]

# 优化后：使用生成器
def process_large_file(filename):
    with open(filename) as f:
        for line in f:
            yield process_line(line)
```

## 并发优化
### 1. 多线程优化
```python
import threading
from concurrent.futures import ThreadPoolExecutor

def process_data_parallel(items):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_item, items))
    return results
```

### 2. 异步优化
```python
import asyncio

async def fetch_user_data(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'/api/users/{user_id}') as response:
            return await response.json()

async def fetch_all_users(user_ids):
    tasks = [fetch_user_data(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)
```

## 代码质量优化
### 1. 代码风格
```python
# 优化前
def calc(x,y,operation):
    if operation=='add':
        return x+y
    elif operation=='subtract':
        return x-y
    elif operation=='multiply':
        return x*y
    else:
        raise Exception('Invalid operation')

# 优化后
from enum import Enum
from typing import Union

class Operation(Enum):
    ADD = 'add'
    SUBTRACT = 'subtract'
    MULTIPLY = 'multiply'

def calculate(x: float, y: float, operation: Operation) -> float:
    """执行基本数学运算
    
    Args:
        x (float): 第一个操作数
        y (float): 第二个操作数
        operation (Operation): 运算类型
    
    Returns:
        float: 计算结果
    
    Raises:
        ValueError: 当操作类型无效时
    """
    operations = {
        Operation.ADD: lambda: x + y,
        Operation.SUBTRACT: lambda: x - y,
        Operation.MULTIPLY: lambda: x * y
    }
    
    if operation not in operations:
        raise ValueError(f"Unsupported operation: {operation}")
        
    return operations[operation]()
```

### 2. 错误处理优化
```python
# 优化前
def save_user(user_data):
    try:
        db.save(user_data)
    except Exception as e:
        print(f"Error: {e}")
        return False
    return True

# 优化后
class UserError(Exception):
    """用户相关操作的基础异常类"""
    pass

class UserValidationError(UserError):
    """用户数据验证错误"""
    pass

class UserDatabaseError(UserError):
    """用户数据库操作错误"""
    pass

def save_user(user_data: dict) -> None:
    """保存用户数据
    
    Args:
        user_data (dict): 用户数据
        
    Raises:
        UserValidationError: 数据验证失败
        UserDatabaseError: 数据库操作失败
    """
    try:
        validate_user_data(user_data)
        user_repository.save(user_data)
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise UserValidationError(str(e))
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise UserDatabaseError(str(e))
```

## 测试优化
### 1. 单元测试
```python
import unittest
from unittest.mock import Mock, patch

class UserServiceTest(unittest.TestCase):
    def setUp(self):
        self.user_repository = Mock()
        self.user_service = UserService(self.user_repository)
    
    def test_get_user_success(self):
        # Arrange
        user_id = 1
        expected_user = User(id=user_id, name="Test User")
        self.user_repository.find_by_id.return_value = expected_user
        
        # Act
        actual_user = self.user_service.get_user(user_id)
        
        # Assert
        self.assertEqual(actual_user, expected_user)
        self.user_repository.find_by_id.assert_called_once_with(user_id)
```

### 2. 性能测试
```python
import time
import statistics

def measure_performance(func, iterations=1000):
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append(end - start)
    
    return {
        'min': min(times),
        'max': max(times),
        'avg': statistics.mean(times),
        'median': statistics.median(times)
    }
```

## 最佳实践
### 1. 代码审查清单
- 代码风格
- 性能考虑
- 安全性
- 可测试性
- 文档完整性

### 2. 性能优化指南
- 先分析后优化
- 重点优化热点代码
- 考虑投入产出比
- 保持代码可维护性

### 3. 重构策略
- 小步重构
- 保持测试覆盖
- 持续集成
- 代码审查

## 常见问题
### 1. 性能问题
- N+1查询问题
- 内存泄漏
- 资源竞争
- 死锁

### 2. 代码质量问题
- 代码重复
- 过度复杂
- 缺乏测试
- 文档不足

## 练习作业
1. 代码重构实践
2. 性能优化案例
3. 测试用例编写
4. 代码审查练习

## 参考资源
- [重构改善既有代码的设计](https://refactoring.com/)
- [Python性能优化指南](https://docs.python.org/3/howto/perf_hints.html)
- [代码整洁之道](https://www.oreilly.com/library/view/clean-code/9780136083238/)