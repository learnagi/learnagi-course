---
title: "检索增强生成：构建智能问答系统"
slug: "basics"
sequence: 1
description: "深入解析检索增强生成(RAG)技术，从原理到实践，帮助你构建基于向量数据库的智能问答系统"
is_published: true
estimated_minutes: 45
language: "zh-CN"
permalink: "https://www.agi01.com/course/agi/rag/basics"
course: "agi/course/rag"
header_image: "images/basics_header.png"
---

# 检索增强生成：构建智能问答系统

![检索增强生成：构建智能问答系统](images/basics_header.png)

## RAG 是什么？🤔

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将检索系统与生成式AI模型结合的技术。它通过检索相关信息来增强AI模型的回答能力，使回答更准确、更可靠。

### 工作原理
```python
from langchain import OpenAI, VectorDBQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader

class RAGSystem:
    def __init__(self, api_key):
        """初始化RAG系统"""
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        self.llm = OpenAI(openai_api_key=api_key)
        self.vector_store = None
        
    def load_documents(self, file_path):
        """加载文档"""
        loader = TextLoader(file_path)
        documents = loader.load()
        
        # 文本分割
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        
        # 创建向量存储
        self.vector_store = Chroma.from_documents(
            texts,
            self.embeddings
        )
        
    def query(self, question):
        """查询问题"""
        if not self.vector_store:
            raise ValueError("请先加载文档")
            
        qa = VectorDBQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            vectorstore=self.vector_store
        )
        
        return qa.run(question)
```

## 核心组件 🔧

### 1. 文档处理
```python
from typing import List, Dict
import numpy as np

class DocumentProcessor:
    def __init__(self, chunk_size=1000, overlap=200):
        self.chunk_size = chunk_size
        self.overlap = overlap
        
    def process_document(self, content: str) -> List[Dict]:
        """处理文档内容"""
        # 分割文本
        chunks = self._split_text(content)
        
        # 清理和规范化
        cleaned_chunks = [self._clean_text(chunk) for chunk in chunks]
        
        # 提取元数据
        documents = [
            {
                'content': chunk,
                'metadata': self._extract_metadata(chunk)
            }
            for chunk in cleaned_chunks
        ]
        
        return documents
    
    def _split_text(self, text: str) -> List[str]:
        """智能分割文本"""
        # 实现智能分割逻辑
        chunks = []
        start = 0
        
        while start < len(text):
            # 找到合适的分割点
            end = start + self.chunk_size
            if end < len(text):
                # 寻找句子边界
                while end > start and text[end] not in '.!?':
                    end -= 1
                if end == start:
                    end = start + self.chunk_size
            
            chunks.append(text[start:end])
            start = end - self.overlap
            
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """清理和规范化文本"""
        # 移除多余空白
        text = ' '.join(text.split())
        # 统一标点符号
        text = text.replace('，', ',').replace('。', '.')
        return text
    
    def _extract_metadata(self, chunk: str) -> Dict:
        """提取文本元数据"""
        return {
            'length': len(chunk),
            'sentences': len([s for s in chunk.split('.') if s]),
            'created_at': datetime.now().isoformat()
        }
```

### 2. 向量索引
```python
class VectorIndex:
    def __init__(self, embedding_dim=768):
        self.embedding_dim = embedding_dim
        self.index = None
        self.documents = []
        
    def build_index(self, documents: List[Dict], embeddings: List[np.ndarray]):
        """构建向量索引"""
        # 使用HNSW索引
        self.index = hnswlib.Index(space='cosine', dim=self.embedding_dim)
        self.index.init_index(
            max_elements=len(embeddings),
            ef_construction=200,
            M=16
        )
        
        # 添加向量
        self.index.add_items(
            embeddings,
            np.arange(len(embeddings))
        )
        
        # 存储文档
        self.documents = documents
        
    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Dict]:
        """搜索相关文档"""
        if self.index is None:
            raise ValueError("索引未构建")
            
        # 执行向量搜索
        labels, distances = self.index.knn_query(query_vector, k)
        
        # 返回相关文档
        results = []
        for idx, dist in zip(labels[0], distances[0]):
            results.append({
                'document': self.documents[idx],
                'score': 1 - dist  # 转换距离为相似度分数
            })
            
        return results
```

### 3. 上下文构建
```python
class ContextBuilder:
    def __init__(self, max_tokens=2000):
        self.max_tokens = max_tokens
        
    def build_context(self, retrieved_docs: List[Dict]) -> str:
        """构建问答上下文"""
        context = []
        current_tokens = 0
        
        for doc in retrieved_docs:
            # 估算token数量
            estimated_tokens = len(doc['document']['content'].split()) * 1.3
            
            if current_tokens + estimated_tokens > self.max_tokens:
                break
                
            context.append(doc['document']['content'])
            current_tokens += estimated_tokens
        
        # 组织上下文
        return self._format_context(context)
    
    def _format_context(self, context_parts: List[str]) -> str:
        """格式化上下文"""
        return "\n\n相关信息：\n" + "\n---\n".join(context_parts)
```

### 4. 响应生成
```python
from typing import Optional

class ResponseGenerator:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.model_name = model_name
        self.client = OpenAI()
        
    def generate_response(
        self,
        question: str,
        context: str,
        max_tokens: int = 500
    ) -> Dict:
        """生成回答"""
        # 构建提示词
        prompt = self._build_prompt(question, context)
        
        # 调用模型生成回答
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "你是一个专业的AI助手，请基于提供的上下文信息回答问题。如果无法从上下文中找到答案，请明确说明。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        return {
            'answer': response.choices[0].message.content,
            'model': self.model_name,
            'tokens_used': response.usage.total_tokens
        }
    
    def _build_prompt(self, question: str, context: str) -> str:
        """构建提示词"""
        return f"""请基于以下信息回答问题：

{context}

问题：{question}

请提供准确、完整的回答。如果上下文信息不足以回答问题，请明确指出。"""
```

## 实践案例 💡

### 1. 构建文档问答系统
```python
class DocumentQA:
    def __init__(self, api_key: str):
        self.processor = DocumentProcessor()
        self.embedder = OpenAIEmbeddings(api_key=api_key)
        self.vector_index = VectorIndex()
        self.context_builder = ContextBuilder()
        self.generator = ResponseGenerator()
        
    def load_documents(self, file_paths: List[str]):
        """加载文档"""
        all_documents = []
        all_embeddings = []
        
        for path in file_paths:
            # 读取文件
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 处理文档
            documents = self.processor.process_document(content)
            
            # 生成嵌入
            embeddings = [
                self.embedder.embed_query(doc['content'])
                for doc in documents
            ]
            
            all_documents.extend(documents)
            all_embeddings.extend(embeddings)
        
        # 构建索引
        self.vector_index.build_index(all_documents, all_embeddings)
        
    def answer_question(self, question: str) -> Dict:
        """回答问题"""
        # 生成问题的嵌入向量
        query_vector = self.embedder.embed_query(question)
        
        # 检索相关文档
        relevant_docs = self.vector_index.search(query_vector)
        
        # 构建上下文
        context = self.context_builder.build_context(relevant_docs)
        
        # 生成回答
        response = self.generator.generate_response(question, context)
        
        return {
            'answer': response['answer'],
            'sources': [doc['document']['content'][:200] + "..."
                       for doc in relevant_docs],
            'model_info': {
                'model': response['model'],
                'tokens': response['tokens_used']
            }
        }
```

### 2. 使用示例
```python
# 初始化系统
qa_system = DocumentQA(api_key="your-api-key")

# 加载文档
qa_system.load_documents([
    "company_policies.txt",
    "product_manual.pdf",
    "faq.md"
])

# 提问
question = "我们的退货政策是什么？"
response = qa_system.answer_question(question)

print("回答:", response['answer'])
print("\n来源文档:")
for source in response['sources']:
    print("-", source)
print("\n使用模型:", response['model_info']['model'])
print("消耗Token:", response['model_info']['tokens'])
```

## 优化技巧 🚀

### 1. 提高检索质量
- 合理设置文档分块大小
- 使用重叠来保持上下文
- 优化向量索引参数

### 2. 增强回答准确性
- 优化提示词工程
- 添加相关性过滤
- 使用多轮对话

### 3. 性能优化
- 实现结果缓存
- 批量处理文档
- 异步处理请求

## 注意事项 ⚠️

1. **数据安全**
   - 保护敏感信息
   - 实现访问控制
   - 定期更新文档

2. **成本控制**
   - 优化Token使用
   - 实现缓存机制
   - 监控API调用

3. **系统维护**
   - 定期更新索引
   - 监控系统性能
   - 处理异常情况

## 小结 📝

本章我们深入学习了RAG技术：

1. **基础概念**
   - RAG原理
   - 核心组件
   - 工作流程

2. **实现细节**
   - 文档处理
   - 向量索引
   - 上下文构建
   - 响应生成

3. **实践应用**
   - 系统构建
   - 优化技巧
   - 注意事项

下一章，我们将探讨向量数据库的更多实际应用场景！
