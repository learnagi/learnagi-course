# AI辅助测试

## 课程目标
- 理解AI辅助测试的基本概念
- 掌握自动化测试生成技术
- 学习测试用例优化方法

## AI测试基础
### 1. 什么是AI辅助测试
- 定义和原理
- 应用场景
- 优势和局限

### 2. 测试类型
- 单元测试
- 集成测试
- 端到端测试
- 性能测试
- 安全测试

## 测试用例生成
### 1. 单元测试生成
```python
# 目标函数
def calculate_discount(price: float, discount_rate: float) -> float:
    """计算折扣价格
    
    Args:
        price (float): 原价
        discount_rate (float): 折扣率（0-1之间）
    
    Returns:
        float: 折扣后价格
    
    Raises:
        ValueError: 当折扣率不在0-1之间时
    """
    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1")
    return price * (1 - discount_rate)

# 生成的测试用例
import unittest

class TestCalculateDiscount(unittest.TestCase):
    def test_normal_discount(self):
        """测试正常折扣计算"""
        self.assertEqual(calculate_discount(100, 0.2), 80)
        self.assertEqual(calculate_discount(50, 0.5), 25)
    
    def test_zero_discount(self):
        """测试零折扣"""
        self.assertEqual(calculate_discount(100, 0), 100)
    
    def test_full_discount(self):
        """测试全额折扣"""
        self.assertEqual(calculate_discount(100, 1), 0)
    
    def test_invalid_discount(self):
        """测试无效折扣率"""
        with self.assertRaises(ValueError):
            calculate_discount(100, -0.1)
        with self.assertRaises(ValueError):
            calculate_discount(100, 1.1)
```

### 2. 集成测试生成
```python
# 用户服务
class UserService:
    def __init__(self, db):
        self.db = db
    
    def create_user(self, username: str, email: str) -> dict:
        """创建新用户"""
        if self.db.find_by_email(email):
            raise ValueError("Email already exists")
        user = {"username": username, "email": email}
        return self.db.save(user)

# 生成的集成测试
import pytest
from unittest.mock import Mock

class TestUserService:
    @pytest.fixture
    def db_mock(self):
        return Mock()
    
    @pytest.fixture
    def user_service(self, db_mock):
        return UserService(db_mock)
    
    def test_create_user_success(self, user_service, db_mock):
        # Arrange
        db_mock.find_by_email.return_value = None
        db_mock.save.return_value = {"id": 1, "username": "test", "email": "test@example.com"}
        
        # Act
        result = user_service.create_user("test", "test@example.com")
        
        # Assert
        assert result["username"] == "test"
        assert result["email"] == "test@example.com"
        db_mock.find_by_email.assert_called_once_with("test@example.com")
        db_mock.save.assert_called_once()
    
    def test_create_user_duplicate_email(self, user_service, db_mock):
        # Arrange
        db_mock.find_by_email.return_value = {"id": 1, "email": "test@example.com"}
        
        # Act & Assert
        with pytest.raises(ValueError, match="Email already exists"):
            user_service.create_user("test", "test@example.com")
```

### 3. API测试生成
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_item():
    """测试创建商品API"""
    # 准备测试数据
    test_item = {
        "name": "Test Item",
        "price": 9.99,
        "description": "Test Description"
    }
    
    # 发送请求
    response = client.post("/items/", json=test_item)
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_item["name"]
    assert data["price"] == test_item["price"]
    assert "id" in data

def test_get_item():
    """测试获取商品API"""
    # 创建测试数据
    test_item = {
        "name": "Test Item",
        "price": 9.99
    }
    create_response = client.post("/items/", json=test_item)
    item_id = create_response.json()["id"]
    
    # 获取数据
    response = client.get(f"/items/{item_id}")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_item["name"]
    assert data["price"] == test_item["price"]
```

## 测试数据生成
### 1. 测试数据工厂
```python
import factory
from datetime import datetime
from models import User, Order

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    created_at = factory.LazyFunction(datetime.now)

class OrderFactory(factory.Factory):
    class Meta:
        model = Order
    
    user = factory.SubFactory(UserFactory)
    amount = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    status = factory.Iterator(['pending', 'paid', 'shipped', 'delivered'])
```

### 2. 模拟数据生成
```python
from faker import Faker

fake = Faker()

def generate_user_data(count: int = 1):
    """生成用户测试数据"""
    users = []
    for _ in range(count):
        user = {
            'name': fake.name(),
            'email': fake.email(),
            'address': fake.address(),
            'phone': fake.phone_number(),
            'birthday': fake.date_of_birth().isoformat()
        }
        users.append(user)
    return users if count > 1 else users[0]
```

## 测试覆盖率分析
### 1. 代码覆盖率
```python
import coverage

def run_coverage():
    """运行测试覆盖率分析"""
    cov = coverage.Coverage()
    cov.start()
    
    # 运行测试
    unittest.main()
    
    cov.stop()
    cov.save()
    
    # 生成报告
    cov.html_report(directory='coverage_report')
```

### 2. 分支覆盖率
```python
def analyze_branch_coverage(source_file: str):
    """分析分支覆盖率"""
    import ast
    
    class BranchVisitor(ast.NodeVisitor):
        def __init__(self):
            self.branches = []
        
        def visit_If(self, node):
            self.branches.append({
                'line': node.lineno,
                'test': ast.unparse(node.test)
            })
            self.generic_visit(node)
    
    with open(source_file) as f:
        tree = ast.parse(f.read())
        visitor = BranchVisitor()
        visitor.visit(tree)
    return visitor.branches
```

## 测试报告生成
### 1. HTML报告
```python
import unittest
from HtmlTestRunner import HTMLTestRunner

def generate_test_report():
    """生成HTML测试报告"""
    test_suite = unittest.TestLoader().discover('tests')
    runner = HTMLTestRunner(
        output='test_reports',
        report_title='Test Report',
        report_name='test_results',
        combine_reports=True
    )
    runner.run(test_suite)
```

### 2. JSON报告
```python
import json
from datetime import datetime

def generate_json_report(test_results):
    """生成JSON格式测试报告"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_tests': len(test_results),
        'passed': sum(1 for r in test_results if r['status'] == 'passed'),
        'failed': sum(1 for r in test_results if r['status'] == 'failed'),
        'results': test_results
    }
    
    with open('test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
```

## 持续集成测试
### 1. GitHub Actions配置
```yaml
name: Python Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest --cov=./ --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

### 2. Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'python -m pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'python -m pytest tests/'
            }
            post {
                always {
                    junit 'test-reports/*.xml'
                }
            }
        }
    }
}
```

## 测试优化
### 1. 性能优化
```python
import pytest
import time

@pytest.mark.benchmark
def test_performance(benchmark):
    """性能测试"""
    def slow_function():
        time.sleep(0.1)
        return sum(range(1000))
    
    # 使用benchmark装饰器测量性能
    result = benchmark(slow_function)
    assert result == 499500
```

### 2. 并行测试
```python
# pytest.ini
[pytest]
addopts = -n auto

# test_parallel.py
@pytest.mark.parallel
def test_parallel_1():
    """并行测试1"""
    time.sleep(1)
    assert True

@pytest.mark.parallel
def test_parallel_2():
    """并行测试2"""
    time.sleep(1)
    assert True
```

## 最佳实践
### 1. 测试策略
- 测试金字塔
- 测试优先级
- 测试范围
- 测试维护

### 2. 测试规范
- 命名规范
- 结构组织
- 断言使用
- 文档编写

### 3. 持续改进
- 测试反馈
- 缺陷跟踪
- 测试优化
- 流程改进

## 常见问题
### 1. 测试覆盖不足
- 边界条件
- 错误处理
- 异常场景
- 并发情况

### 2. 测试维护困难
- 测试代码质量
- 测试依赖
- 测试数据管理
- 测试环境配置

## 练习作业
1. 编写单元测试
2. 实现集成测试
3. 配置CI/CD
4. 生成测试报告

## 参考资源
- [Python单元测试文档](https://docs.python.org/3/library/unittest.html)
- [Pytest文档](https://docs.pytest.org/)
- [测试驱动开发指南](https://www.agilealliance.org/glossary/tdd/)