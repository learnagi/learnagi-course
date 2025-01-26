# RAG基础

## 课程目标
- 理解RAG（检索增强生成）的基本概念
- 掌握RAG系统的核心组件
- 学习RAG的实现方法

## RAG概述
### 1. 什么是RAG
- 定义和原理
- 工作机制
- 应用场景

### 2. RAG的优势
- 知识更新及时
- 减少幻觉
- 可追溯性强
- 成本效益好

## RAG系统架构
### 1. 核心组件
```
1. 文档处理器
   - 文本提取
   - 文档分块
   - 文本清理

2. 向量数据库
   - 文本嵌入
   - 向量索引
   - 相似度搜索

3. 检索器
   - 查询处理
   - 相关性排序
   - 结果过滤

4. 生成器
   - 上下文整合
   - 答案生成
   - 引用管理
```

### 2. 工作流程
```python
from typing import List, Dict
import numpy as np
from langchain import Document, VectorStore, LLM

class RAGSystem:
    def __init__(self, vector_store: VectorStore, llm: LLM):
        self.vector_store = vector_store
        self.llm = llm
    
    def process_query(self, query: str) -> str:
        """处理用户查询
        
        步骤：
        1. 查询向量化
        2. 相似度检索
        3. 上下文整合
        4. 答案生成
        """
        # 1. 查询向量化
        query_vector = self.vectorize(query)
        
        # 2. 相似度检索
        relevant_docs = self.retrieve_documents(query_vector)
        
        # 3. 上下文整合
        context = self.build_context(relevant_docs)
        
        # 4. 答案生成
        response = self.generate_response(query, context)
        
        return response
```

## 文档处理
### 1. 文本提取
```python
from typing import List
import fitz  # PyMuPDF
from docx import Document
import pandas as pd

class DocumentProcessor:
    def extract_text(self, file_path: str) -> str:
        """从不同格式的文档中提取文本
        
        支持格式：
        - PDF
        - Word
        - Excel
        - Text
        """
        ext = file_path.split('.')[-1].lower()
        
        if ext == 'pdf':
            return self._extract_from_pdf(file_path)
        elif ext == 'docx':
            return self._extract_from_docx(file_path)
        elif ext == 'xlsx':
            return self._extract_from_excel(file_path)
        elif ext == 'txt':
            return self._extract_from_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
```

### 2. 文本分块
```python
def split_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """将文本分割成重叠的块
    
    Args:
        text (str): 输入文本
        chunk_size (int): 每块的最大字符数
        overlap (int): 重叠的字符数
    
    Returns:
        List[str]: 文本块列表
    """
    chunks = []
    start = 0
    
    while start < len(text):
        # 确定当前块的结束位置
        end = start + chunk_size
        
        # 如果不是最后一块，查找合适的分割点
        if end < len(text):
            # 在句子边界处分割
            while end > start and text[end] not in '.!?':
                end -= 1
            if end == start:
                end = start + chunk_size
        
        # 添加文本块
        chunks.append(text[start:end])
        
        # 更新起始位置，考虑重叠
        start = end - overlap
    
    return chunks
```

### 3. 文本清理
```python
import re
from typing import List

def clean_text(text: str) -> str:
    """清理文本
    
    步骤：
    1. 删除多余空白
    2. 统一标点符号
    3. 删除特殊字符
    4. 修复常见错误
    """
    # 1. 删除多余空白
    text = re.sub(r'\s+', ' ', text)
    
    # 2. 统一标点符号
    text = text.replace('"', '"').replace('"', '"')
    
    # 3. 删除特殊字符
    text = re.sub(r'[^\w\s.,!?;:\'"-]', '', text)
    
    # 4. 修复常见错误
    text = text.strip()
    
    return text
```

## 向量化和存储
### 1. 文本嵌入
```python
from sentence_transformers import SentenceTransformer
import numpy as np

class TextEmbedder:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    
    def embed_text(self, text: str) -> np.ndarray:
        """将文本转换为向量
        
        Args:
            text (str): 输入文本
        
        Returns:
            np.ndarray: 文本向量
        """
        return self.model.encode(text)
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """批量将文本转换为向量"""
        return self.model.encode(texts)
```

### 2. 向量索引
```python
import faiss
import numpy as np

class VectorIndex:
    def __init__(self, dimension: int):
        """初始化向量索引
        
        Args:
            dimension (int): 向量维度
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
    
    def add_vectors(self, vectors: np.ndarray):
        """添加向量到索引"""
        self.index.add(vectors)
    
    def search(self, query_vector: np.ndarray, k: int = 5) -> tuple:
        """搜索最相似的向量
        
        Args:
            query_vector (np.ndarray): 查询向量
            k (int): 返回的最相似向量数量
        
        Returns:
            tuple: (距离数组, 索引数组)
        """
        return self.index.search(query_vector.reshape(1, -1), k)
```

## 检索策略
### 1. 相似度计算
```python
from scipy.spatial.distance import cosine
import numpy as np

def calculate_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """计算两个向量的余弦相似度
    
    Args:
        vec1 (np.ndarray): 第一个向量
        vec2 (np.ndarray): 第二个向量
    
    Returns:
        float: 相似度分数 (0-1)
    """
    return 1 - cosine(vec1, vec2)

def rank_documents(query_vec: np.ndarray, doc_vecs: List[np.ndarray]) -> List[tuple]:
    """对文档按相似度排序
    
    Args:
        query_vec (np.ndarray): 查询向量
        doc_vecs (List[np.ndarray]): 文档向量列表
    
    Returns:
        List[tuple]: (文档索引, 相似度分数) 的排序列表
    """
    similarities = [calculate_similarity(query_vec, doc_vec) for doc_vec in doc_vecs]
    return sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
```

### 2. 混合检索
```python
from typing import List, Dict
import numpy as np

class HybridRetriever:
    def __init__(self, vector_store, keyword_index):
        self.vector_store = vector_store
        self.keyword_index = keyword_index
    
    def hybrid_search(self, query: str, k: int = 5) -> List[Dict]:
        """混合搜索策略
        
        结合向量搜索和关键词搜索的结果
        
        Args:
            query (str): 查询文本
            k (int): 返回结果数量
        
        Returns:
            List[Dict]: 搜索结果列表
        """
        # 向量搜索
        vector_results = self.vector_store.similarity_search(query, k)
        
        # 关键词搜索
        keyword_results = self.keyword_index.search(query, k)
        
        # 结果合并和重排序
        combined_results = self._merge_results(vector_results, keyword_results)
        
        return combined_results[:k]
```

## 上下文整合
### 1. 上下文构建
```python
def build_context(query: str, relevant_docs: List[Dict]) -> str:
    """构建查询上下文
    
    Args:
        query (str): 用户查询
        relevant_docs (List[Dict]): 相关文档列表
    
    Returns:
        str: 格式化的上下文
    """
    context = [
        "根据以下信息回答问题：\n",
        f"问题：{query}\n",
        "相关信息：\n"
    ]
    
    for i, doc in enumerate(relevant_docs, 1):
        context.append(f"{i}. {doc['content']}\n")
    
    return "".join(context)
```

### 2. 信息过滤
```python
def filter_relevant_info(docs: List[Dict], query: str, threshold: float = 0.5) -> List[Dict]:
    """过滤相关信息
    
    Args:
        docs (List[Dict]): 文档列表
        query (str): 查询文本
        threshold (float): 相关性阈值
    
    Returns:
        List[Dict]: 过滤后的文档列表
    """
    filtered_docs = []
    
    for doc in docs:
        relevance_score = calculate_relevance(doc['content'], query)
        if relevance_score >= threshold:
            filtered_docs.append(doc)
    
    return filtered_docs
```

## 答案生成
### 1. 提示词模板
```python
class PromptTemplate:
    @staticmethod
    def create_prompt(query: str, context: str) -> str:
        """创建提示词
        
        Args:
            query (str): 用户查询
            context (str): 相关上下文
        
        Returns:
            str: 格式化的提示词
        """
        return f"""
        基于以下提供的上下文信息，回答问题。
        如果无法从上下文中找到答案，请明确说明。
        
        上下文：
        {context}
        
        问题：{query}
        
        回答：
        """
```

### 2. 答案生成
```python
from typing import Dict
import openai

class AnswerGenerator:
    def __init__(self, api_key: str):
        openai.api_key = api_key
    
    def generate_answer(self, prompt: str) -> Dict:
        """生成答案
        
        Args:
            prompt (str): 完整的提示词
        
        Returns:
            Dict: 包含答案和元数据的字典
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的助手，提供准确、简洁的回答。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return {
            'answer': response.choices[0].message.content,
            'model': response.model,
            'tokens_used': response.usage.total_tokens
        }
```

## 评估和优化
### 1. 性能评估
```python
from typing import List, Dict
import time

def evaluate_rag_system(system, test_cases: List[Dict]) -> Dict:
    """评估RAG系统性能
    
    Args:
        system: RAG系统实例
        test_cases (List[Dict]): 测试用例列表
    
    Returns:
        Dict: 评估结果
    """
    results = {
        'latency': [],
        'accuracy': [],
        'relevance': []
    }
    
    for case in test_cases:
        # 测量延迟
        start_time = time.time()
        response = system.process_query(case['query'])
        latency = time.time() - start_time
        
        # 评估准确性和相关性
        accuracy = evaluate_accuracy(response, case['ground_truth'])
        relevance = evaluate_relevance(response, case['context'])
        
        results['latency'].append(latency)
        results['accuracy'].append(accuracy)
        results['relevance'].append(relevance)
    
    return {
        'avg_latency': sum(results['latency']) / len(results['latency']),
        'avg_accuracy': sum(results['accuracy']) / len(results['accuracy']),
        'avg_relevance': sum(results['relevance']) / len(results['relevance'])
    }
```

### 2. 系统优化
```python
class RAGOptimizer:
    def optimize_retrieval(self, query: str, results: List[Dict]) -> List[Dict]:
        """优化检索结果
        
        策略：
        1. 去重
        2. 相关性重排序
        3. 长度归一化
        """
        # 1. 去重
        unique_results = self._remove_duplicates(results)
        
        # 2. 相关性重排序
        ranked_results = self._rerank_by_relevance(query, unique_results)
        
        # 3. 长度归一化
        normalized_results = self._normalize_length(ranked_results)
        
        return normalized_results
    
    def optimize_prompt(self, query: str, context: str) -> str:
        """优化提示词
        
        策略：
        1. 关键信息提取
        2. 结构优化
        3. 指令明确化
        """
        # 实现优化逻辑
        pass
```

## 部署和扩展
### 1. 系统部署
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/rag/query")
async def process_query(query: Query):
    """RAG查询接口
    
    Args:
        query (Query): 查询请求
    
    Returns:
        Dict: 查询结果
    """
    try:
        result = rag_system.process_query(query.text)
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
```

### 2. 性能扩展
```python
from typing import List
import asyncio

class ScalableRAG:
    def __init__(self, num_workers: int = 3):
        self.num_workers = num_workers
        self.worker_pool = []
    
    async def process_batch_queries(self, queries: List[str]) -> List[str]:
        """并行处理多个查询
        
        Args:
            queries (List[str]): 查询列表
        
        Returns:
            List[str]: 结果列表
        """
        tasks = []
        for query in queries:
            task = asyncio.create_task(self.process_single_query(query))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results
```

## 最佳实践
### 1. 系统设计
- 模块化架构
- 错误处理
- 性能监控
- 可扩展性

### 2. 优化策略
- 缓存机制
- 批处理
- 异步处理
- 负载均衡

### 3. 维护指南
- 日志记录
- 监控告警
- 定期更新
- 性能优化

## 常见问题
### 1. 检索问题
- 相关性不足
- 结果重复
- 检索速度慢
- 内存占用高

### 2. 生成问题
- 答案不准确
- 上下文丢失
- 生成延迟高
- 成本控制

## 练习作业
1. 实现基础RAG系统
2. 优化检索策略
3. 改进答案生成
4. 部署和测试

## 参考资源
- [LangChain文档](https://python.langchain.com/docs/get_started/introduction)
- [Faiss文档](https://github.com/facebookresearch/faiss)
- [OpenAI API文档](https://platform.openai.com/docs/api-reference)