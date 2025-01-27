---
title: "向量数据库基础：AI 时代的智能存储引擎"
slug: "basics"
sequence: 1
description: "了解向量数据库的核心概念、工作原理和应用场景，掌握 AI 应用中的智能数据检索基础"
is_published: true
estimated_minutes: 35
language: "zh-CN"
permalink: "https://www.agi01.com/course/agi/vector-db/basics"
course: "agi/course/vector-db"
---

![Header Image](https://z1.zve.cn/tutorial/vector-db/basics_header.png)

# 向量数据库基础

## 从传统数据库说起 🤔

让我们先回顾一下我们熟悉的 MySQL 数据库是如何工作的：

### MySQL 的工作方式

想象你在管理一个图书馆的书籍数据库：

```sql
CREATE TABLE books (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    category VARCHAR(100),
    publish_date DATE
);

-- 查找所有 2023 年出版的科技类书籍
SELECT * FROM books 
WHERE category = '科技' 
AND YEAR(publish_date) = 2023;
```

MySQL 的特点：
1. ✅ **精确匹配**：找到所有"科技"类的书
2. ✅ **范围查询**：找到特定年份的书
3. ❌ **无法理解内容**：不能找到"类似的书"
4. ❌ **不懂语义**：不能理解"这本书讲了什么"

### 现实世界的需求

但在 AI 时代，我们经常需要：
1. 找到"相似的"内容
2. 理解内容的含义
3. 处理图片、声音等非结构化数据

例如：
- 🔍 "找到和这篇文章相似的文章"
- 🖼️ "找到和这张图片风格接近的图片"
- 🤖 "找到能回答这个问题的文档片段"

这就是为什么我们需要向量数据库！

## 什么是向量？🎯

### 通俗理解

向量就是一串数字，用来描述事物的"特征"。

想象你在描述一个人：
- 身高：180cm
- 体重：70kg
- 年龄：25岁

这就可以表示成一个向量：[180, 70, 25]

### AI 中的向量

在 AI 领域，我们用向量来描述：

1. **文本向量**
```python
# 假设我们有一段文本
text = "今天天气真好"

# AI 模型会将其转换为一串数字（向量）
vector = [0.2, -0.5, 0.8, ..., 0.3]  # 可能有几百个数字
```

2. **图片向量**
```python
# 一张猫的图片
image = load_image("cat.jpg")

# AI 模型会将图片转换为向量
vector = [0.1, 0.7, -0.4, ..., 0.6]
```

这些向量有个神奇的特性：**相似的内容会得到相似的向量**！

## 向量数据库是什么？💡

向量数据库就是专门用来存储和检索这些向量的数据库。它能帮我们：
1. 存储大量向量
2. 快速找到相似的向量
3. 支持智能搜索

### 工作原理举例

假设我们在开发一个智能客服系统：

1. **准备知识库**
```python
# 1. 收集常见问题和答案
qa_pairs = [
    "问：如何重置密码？答：点击登录页的「忘记密码」...",
    "问：怎么修改收货地址？答：进入「个人中心」...",
    "问：退款多久到账？答：一般1-3个工作日内..."
]

# 2. 转换为向量并存储
for qa in qa_pairs:
    vector = ai_model.to_vector(qa)  # 转换为向量
    vector_db.save(vector, qa)       # 存储
```

2. **处理用户问题**
```python
# 1. 用户提问
user_question = "密码忘记了怎么办？"

# 2. 转换为向量
question_vector = ai_model.to_vector(user_question)

# 3. 找到最相似的答案
similar_qa = vector_db.find_similar(question_vector)
# 会返回"如何重置密码？"的答案
```

为什么这样就能工作？因为：
- "密码忘记了"和"重置密码"虽然文字不同
- 但它们的"含义"相似
- 所以它们的向量也会相似！

## 向量数据库的发展历史 📚

### 早期探索（2000-2015）
在向量数据库出现之前，工程师们就在尝试解决相似性搜索的问题：

1. **LSH（局部敏感哈希）时代**
   - 2004年：LSH 算法在图像检索中流行
   - 优点：简单快速
   - 缺点：准确率不够理想

2. **树形索引时代**
   - 2006年：各种树形结构被提出
   - 代表：KD树、Ball树
   - 问题：高维数据性能下降严重

### 现代向量数据库的崛起（2016-至今）

1. **FAISS 的诞生（2017）**
   - Facebook AI 团队发布
   - 首次将向量检索变得实用
   - 引入了 IVF（倒排文件）索引

2. **Milvus 的创新（2019）**
   - 首个开源向量数据库
   - 支持分布式部署
   - 引入混合索引技术

3. **云服务时代（2020-至今）**
   - Pinecone：首个向量数据库即服务
   - Weaviate：支持多模态数据
   - Qdrant：注重易用性和性能

## 主流向量数据库对比 🔍

### 1. Milvus
特点：
- ✅ 开源、功能完整
- ✅ 支持分布式部署
- ✅ 性能优秀
- ❌ 部署复杂度较高

适用场景：
```python
# 适合大规模生产环境
from pymilvus import Collection, connections

# 连接 Milvus
connections.connect(host='localhost', port='19530')

# 创建集合
collection = Collection(
    name="articles",
    schema=CollectionSchema(fields)
)
```

### 2. Pinecone
特点：
- ✅ 全托管服务
- ✅ 零运维成本
- ✅ 快速部署
- ❌ 价格较高

适用场景：
```python
# 适合快速验证想法
import pinecone

pinecone.init(api_key="your-api-key")
index = pinecone.Index("quickstart")

# 快速上手
index.upsert([
    ("vec1", [0.1, 0.2, 0.3, 0.4]),
    ("vec2", [0.2, 0.3, 0.4, 0.5])
])
```

### 3. Qdrant
特点：
- ✅ 轻量级
- ✅ 易于部署
- ✅ 性能不错
- ❌ 功能相对简单

适用场景：
```python
# 适合中小规模应用
from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)

# 简单直观的 API
client.upload_collection(
    collection_name="demo",
    vectors=[[1.0, 0.0], [0.0, 1.0]],
    ids=[1, 2]
)
```

### 4. Weaviate
特点：
- ✅ 支持多模态
- ✅ GraphQL 接口
- ✅ 模块化设计
- ❌ 学习曲线较陡

适用场景：
```python
# 适合复杂数据结构
import weaviate

client = weaviate.Client("http://localhost:8080")

# 支持复杂查询
client.query.get(
    "Article", 
    ["title", "content"]
).with_near_text({
    "concepts": ["machine learning"]
}).do()
```

## 实际应用场景 🌟

### 1. 智能搜索
传统搜索：
```sql
-- MySQL 搜索
SELECT * FROM articles 
WHERE title LIKE '%人工智能%';
```

向量搜索：
```python
# 向量数据库搜索
query = "AI 如何改变我们的生活"
vector = model.encode(query)
similar_articles = vector_db.search(vector)
# 能找到讨论 AI、人工智能、机器学习等相关文章
```

### 2. 图片搜索
```python
# 1. 上传一张包包的图片
bag_image = upload_image("my_bag.jpg")

# 2. 转换为向量
bag_vector = image_model.encode(bag_image)

# 3. 搜索相似商品
similar_bags = vector_db.search(bag_vector)
# 能找到类似款式、颜色、风格的包包
```

### 3. 智能推荐
```python
# 1. 用户正在看的文章
current_article = "Python 入门教程"
article_vector = model.encode(current_article)

# 2. 推荐相关文章
recommendations = vector_db.search(article_vector)
# 会推荐编程、教程等相关内容
```

## 向量数据库 vs MySQL 🔄

让我们通过具体例子来对比：

### 1. 文本搜索
MySQL:
```sql
-- 只能找到包含完全相同关键词的结果
SELECT * FROM articles 
WHERE content LIKE '%Python 教程%';
```

向量数据库：
```python
# 能找到相关内容，即使用词不同
query = "Python 怎么入门学习"
results = vector_db.search(encode(query))
# 能找到：
# - "Python 编程入门指南"
# - "零基础学习 Python"
# - "编程初学者教程"
```

### 2. 图片搜索
MySQL:
```sql
-- 只能通过标签或描述搜索
SELECT * FROM products 
WHERE category = '包包' 
AND color = '棕色';
```

向量数据库：
```python
# 上传图片直接搜索相似商品
image = load_image("brown_bag.jpg")
similar_products = vector_db.search(encode(image))
# 能找到相似风格、款式的包包
```

## 什么时候用向量数据库？🤔

### 适合使用向量数据库的场景：

1. **需要理解内容含义**
   - 智能客服
   - 文档检索
   - 相似内容推荐

2. **处理非结构化数据**
   - 图片搜索
   - 语音识别
   - 视频推荐

3. **需要相似度搜索**
   - 商品推荐
   - 人脸识别
   - 抄袭检测

### 继续使用传统数据库的场景：

1. **需要精确查询**
   - 用户账号信息
   - 订单记录
   - 库存管理

2. **简单的 CRUD 操作**
   - 商品目录
   - 用户配置
   - 系统设置

## 实战：使用 ChromaDB 构建智能文档搜索 💻

ChromaDB 是一个简单易用的开源向量数据库，特别适合入门学习。让我们用它来构建一个智能文档搜索系统。

### 1. 环境准备
```bash
# 安装 ChromaDB 和依赖
pip install chromadb sentence-transformers
```

### 2. 创建文档库
```python
import chromadb
from sentence_transformers import SentenceTransformer

# 初始化 ChromaDB
client = chromadb.Client()

# 创建集合
collection = client.create_collection(
    name="documents",
    metadata={"description": "文档搜索示例"}
)

# 准备文档
documents = [
    "Python 是一种简单易学的编程语言，广泛用于 Web 开发、数据分析和人工智能",
    "JavaScript 是网页开发的核心语言，负责网页的交互和动态效果",
    "SQL 是一种用于管理关系型数据库的语言，比如 MySQL、PostgreSQL",
    "Docker 使应用的打包和部署变得更加简单，实现了开发环境的标准化",
]

# 为文档生成 ID
doc_ids = [f"doc_{i}" for i in range(len(documents))]

# 添加文档到集合
collection.add(
    documents=documents,
    ids=doc_ids,
    metadatas=[{"source": "tech_docs"} for _ in documents]
)
```

### 3. 搜索文档
```python
# 执行语义搜索
query = "容器技术"
results = collection.query(
    query_texts=[query],
    n_results=2
)

print("搜索结果：")
for doc in results['documents'][0]:
    print(f"- {doc}")
# 输出：
# - Docker 使应用的打包和部署变得更加简单，实现了开发环境的标准化
```

### 4. 添加元数据过滤
```python
# 添加带标签的文档
collection.add(
    documents=["Kubernetes 是容器编排平台，用于管理容器化应用"],
    ids=["doc_k8s"],
    metadatas=[{"category": "container", "difficulty": "advanced"}]
)

# 带过滤条件的搜索
results = collection.query(
    query_texts=["容器编排"],
    n_results=2,
    where={"category": "container"}
)
```

### 5. 实现相似度排序
```python
# 获取文档的相似度分数
results = collection.query(
    query_texts=["编程语言入门"],
    n_results=3,
    include=["distances"]  # 包含相似度分数
)

# 打印结果和相似度
for doc, distance in zip(results['documents'][0], results['distances'][0]):
    print(f"文档: {doc}")
    print(f"相似度: {1 - distance:.2f}\n")  # 转换距离为相似度
```

### 6. 更新和删除
```python
# 更新文档
collection.update(
    ids=["doc_0"],
    documents=["Python 是最受欢迎的编程语言之一，特别适合初学者"],
    metadatas=[{"updated": True}]
)

# 删除文档
collection.delete(ids=["doc_1"])
```

### 7. 持久化存储
```python
# 创建持久化客户端
persistent_client = chromadb.PersistentClient(path="/path/to/db")

# 现在数据会保存到磁盘
persistent_collection = persistent_client.create_collection(
    name="persistent_docs"
)
```

## 实用技巧 💡

### 1. 批量处理
```python
# 批量添加文档
documents = [...]  # 大量文档
batch_size = 100

for i in range(0, len(documents), batch_size):
    batch = documents[i:i + batch_size]
    collection.add(
        documents=batch,
        ids=[f"doc_{j}" for j in range(i, i + len(batch))]
    )
```

### 2. 错误处理
```python
try:
    results = collection.query(
        query_texts=[query],
        n_results=5
    )
except Exception as e:
    print(f"搜索失败: {str(e)}")
    results = {"documents": [[]]}  # 返回空结果
```

### 3. 结果后处理
```python
def process_results(results, threshold=0.8):
    """只返回相似度高于阈值的结果"""
    filtered_docs = []
    for doc, distance in zip(results['documents'][0], results['distances'][0]):
        similarity = 1 - distance
        if similarity > threshold:
            filtered_docs.append({
                "content": doc,
                "similarity": similarity
            })
    return filtered_docs
```

## 小结 📝

ChromaDB 提供了一个简单但功能强大的入门方案：
1. 简单易用的 API
2. 内置持久化支持
3. 支持元数据过滤
4. 提供相似度评分

接下来，你可以：
1. 尝试处理更多类型的文档
2. 实现更复杂的搜索逻辑
3. 优化搜索结果的质量

记住：向量数据库的选择要根据实际需求，ChromaDB 适合学习和小型项目，而大型项目可能需要考虑 Milvus 或 Pinecone 等更强大的解决方案。
