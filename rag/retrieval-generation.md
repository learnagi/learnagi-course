---
title: "检索与生成：RAG系统的核心流程"
slug: "retrieval-generation"
sequence: 2
description: "深入探讨RAG系统中的检索策略和生成技术，掌握相似度计算、上下文处理和答案生成的核心方法"
is_published: true
estimated_minutes: 45
language: "zh-CN"
permalink: "https://www.agi01.com/course/agi/rag/retrieval-generation"
course: "agi/course/rag"
header_image: "images/retrieval-generation_header.png"
---

# 检索与生成：RAG系统的核心流程

![Header Image](https://z1.zve.cn/tutorial/rag/retrieval-generation_header.png)

## 检索策略设计 🔍

### 相似度计算方法

在RAG系统中，相似度计算是检索阶段的核心。常用的相似度计算方法包括：

```python
import numpy as np
from typing import List, Dict

class SimilarityCalculator:
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """计算余弦相似度"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def euclidean_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """计算欧氏距离相似度"""
        distance = np.linalg.norm(vec1 - vec2)
        return 1 / (1 + distance)
    
    def dot_product_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """计算点积相似度"""
        return np.dot(vec1, vec2)

class HybridRetriever:
    def __init__(self):
        self.similarity_calculator = SimilarityCalculator()
        
    def hybrid_search(
        self,
        query_vector: np.ndarray,
        document_vectors: List[np.ndarray],
        weights: Dict[str, float] = {"cosine": 0.4, "euclidean": 0.3, "dot": 0.3}
    ) -> List[float]:
        """混合检索方法"""
        scores = []
        for doc_vector in document_vectors:
            # 计算不同相似度
            cosine_score = self.similarity_calculator.cosine_similarity(
                query_vector, doc_vector
            )
            euclidean_score = self.similarity_calculator.euclidean_similarity(
                query_vector, doc_vector
            )
            dot_score = self.similarity_calculator.dot_product_similarity(
                query_vector, doc_vector
            )
            
            # 加权组合
            final_score = (
                weights["cosine"] * cosine_score +
                weights["euclidean"] * euclidean_score +
                weights["dot"] * dot_score
            )
            scores.append(final_score)
            
        return scores
```

### 重排序技术

检索结果的重排序可以显著提升相关性：

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SearchResult:
    content: str
    score: float
    metadata: dict

class Reranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)
        
    def rerank(
        self,
        query: str,
        results: List[SearchResult],
        top_k: Optional[int] = None
    ) -> List[SearchResult]:
        """重排序检索结果"""
        # 准备文本对
        pairs = [(query, result.content) for result in results]
        
        # 计算相关性分数
        scores = self.model.predict(pairs)
        
        # 更新结果分数
        for result, score in zip(results, scores):
            result.score = score
            
        # 重新排序
        reranked_results = sorted(
            results,
            key=lambda x: x.score,
            reverse=True
        )
        
        # 返回top_k结果
        if top_k:
            reranked_results = reranked_results[:top_k]
            
        return reranked_results
```

## 上下文处理 📝

### 上下文组装

有效的上下文组装对生成质量至关重要：

```python
class ContextAssembler:
    def __init__(
        self,
        max_tokens: int = 2000,
        overlap_tokens: int = 200
    ):
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        
    def assemble_context(
        self,
        retrieved_docs: List[SearchResult],
        query: str
    ) -> str:
        """组装上下文"""
        # 按相关性排序
        sorted_docs = sorted(
            retrieved_docs,
            key=lambda x: x.score,
            reverse=True
        )
        
        context_parts = []
        current_tokens = 0
        
        for doc in sorted_docs:
            # 估算token数量
            estimated_tokens = len(doc.content.split()) * 1.3
            
            if current_tokens + estimated_tokens > self.max_tokens:
                break
                
            # 添加文档内容
            context_parts.append(
                f"相关度: {doc.score:.2f}\n"
                f"来源: {doc.metadata.get('source', '未知')}\n"
                f"内容: {doc.content}\n"
            )
            
            current_tokens += estimated_tokens
            
        # 组合上下文
        context = (
            f"问题: {query}\n\n"
            f"参考信息:\n"
            f"{'='*50}\n"
            f"\n{'='*50}\n".join(context_parts)
        )
        
        return context

class LongTextHandler:
    def __init__(self, max_chunk_size: int = 1000):
        self.max_chunk_size = max_chunk_size
        
    def split_context(self, context: str) -> List[str]:
        """处理长文本"""
        words = context.split()
        chunks = []
        
        for i in range(0, len(words), self.max_chunk_size):
            chunk = ' '.join(words[i:i + self.max_chunk_size])
            chunks.append(chunk)
            
        return chunks
```

## 生成策略 ✨

### 提示词设计

高质量的提示词对生成效果至关重要：

```python
class PromptDesigner:
    def __init__(self):
        self.templates = {
            "qa": {
                "system": "你是一个专业的AI助手，请基于提供的上下文信息回答问题。如果无法从上下文中找到答案，请明确说明。",
                "user": lambda context, query: f"""请基于以下信息回答问题：

上下文信息：
{context}

问题：{query}

请提供准确、完整的回答。如果上下文信息不足以回答问题，请明确指出。
""",
                "assistant": "我将基于提供的上下文信息回答您的问题。"
            },
            "summary": {
                "system": "你是一个专业的AI助手，请总结提供的信息要点。",
                "user": lambda context: f"""请总结以下信息的主要内容：

{context}

请提供简洁、准确的要点总结。
""",
                "assistant": "我将总结信息的主要内容。"
            }
        }
        
    def create_prompt(
        self,
        template_type: str,
        context: str,
        query: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """创建提示词"""
        if template_type not in self.templates:
            raise ValueError(f"未知的模板类型: {template_type}")
            
        template = self.templates[template_type]
        messages = [
            {"role": "system", "content": template["system"]},
            {"role": "assistant", "content": template["assistant"]}
        ]
        
        if template_type == "qa":
            if not query:
                raise ValueError("QA模板需要提供query参数")
            messages.append({
                "role": "user",
                "content": template["user"](context, query)
            })
        else:
            messages.append({
                "role": "user",
                "content": template["user"](context)
            })
            
        return messages
```

### 答案生成

实现高质量的答案生成：

```python
from openai import OpenAI
from typing import Dict, Any

class AnswerGenerator:
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 500
    ):
        self.client = OpenAI()
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.prompt_designer = PromptDesigner()
        
    def generate_answer(
        self,
        context: str,
        query: str,
        **kwargs
    ) -> Dict[str, Any]:
        """生成答案"""
        # 创建提示词
        messages = self.prompt_designer.create_prompt(
            "qa", context, query
        )
        
        # 调用模型生成答案
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        
        return {
            'answer': response.choices[0].message.content,
            'model': self.model_name,
            'tokens_used': response.usage.total_tokens
        }
```

## 质量控制 🎯

### 准确性评估

```python
class QualityEvaluator:
    def __init__(self):
        self.client = OpenAI()
        
    def evaluate_answer(
        self,
        question: str,
        answer: str,
        context: str
    ) -> Dict[str, float]:
        """评估答案质量"""
        prompt = f"""请评估以下问答的质量：

问题：{question}

参考上下文：
{context}

生成的答案：
{answer}

请从以下几个维度评分（0-10分）：
1. 相关性：答案与问题的相关程度
2. 准确性：答案是否准确反映了上下文信息
3. 完整性：答案是否完整覆盖了问题的各个方面
4. 清晰度：答案的表述是否清晰易懂

请以JSON格式返回评分结果。
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是一个专业的QA质量评估专家。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # 解析评分结果
        try:
            scores = json.loads(response.choices[0].message.content)
            return scores
        except:
            return {
                "relevance": 0,
                "accuracy": 0,
                "completeness": 0,
                "clarity": 0
            }
```

### 答案一致性

```python
class ConsistencyChecker:
    def check_consistency(
        self,
        answer: str,
        context: str
    ) -> Dict[str, Any]:
        """检查答案与上下文的一致性"""
        prompt = f"""请检查以下回答与参考上下文的一致性：

参考上下文：
{context}

生成的答案：
{answer}

请检查：
1. 答案中的事实是否都能在上下文中找到依据
2. 是否存在与上下文矛盾的内容
3. 是否有超出上下文范围的推测

请以JSON格式返回检查结果。
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是一个专业的内容一致性检查专家。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            return result
        except:
            return {
                "factual_support": False,
                "contradictions": [],
                "speculations": []
            }
```

## 实践建议 💡

1. **检索策略优化**
   - 根据场景选择合适的相似度计算方法
   - 使用混合检索提高召回率
   - 通过重排序优化相关性

2. **上下文处理技巧**
   - 合理设置上下文长度
   - 保持文档片段的完整性
   - 考虑添加元信息增强上下文

3. **生成质量提升**
   - 精心设计提示词模板
   - 适当调整温度参数
   - 实施多轮对话策略

4. **持续优化**
   - 收集用户反馈
   - 监控系统表现
   - 定期更新评估基准

## 小结 📝

本章我们深入学习了RAG系统的核心流程：

1. **检索策略**
   - 相似度计算方法
   - 混合检索技术
   - 重排序优化

2. **上下文处理**
   - 上下文组装
   - 长文本处理

3. **生成技术**
   - 提示词设计
   - 答案生成
   - 质量控制

通过合理的检索策略、精心的上下文处理和高质量的生成技术，我们可以构建出性能优秀的RAG系统。在实践中，要根据具体场景和需求，不断调整和优化这些组件，以达到最佳效果。
