---
title: "语音转文本"
slug: "speech-to-text"
sequence: 5
description: "学习使用OpenAI的Whisper模型将语音转换为文本，掌握音频转录和翻译的技巧"
is_published: true
estimated_minutes: 25
language: "zh-CN"
updated_at: "2024-01-26"
---

![Header Image](https://z1.zve.cn/tutorial/llm-basics/speech-to-text_header.png)
*让AI倾听你的声音*

# 语音转文本

## 本节概要

通过本节学习，你将学会：
- 使用OpenAI的Whisper API将语音转换为文本
- 掌握音频转录和翻译的关键技术
- 处理长音频和优化转录质量
- 实现多语言音频处理

💡 重点内容：
- Whisper API的基本用法
- 音频转录和翻译的区别
- 时间戳和字幕生成
- 提示词优化技巧

## 1. 基础概念

### 1.1 语音转文本简介
语音转文本（Speech-to-Text，STT）是将口语音频转换为书面文本的技术。OpenAI的音频转文本API基于开源的Whisper large-v2模型，提供两个主要功能：
1. **转录（Transcriptions）**：将音频转换为原始语言的文本
2. **翻译（Translations）**：将音频直接转换为英文文本

### 1.2 支持的格式
目前支持的音频格式包括：
- mp3, mp4, mpeg, mpga, m4a, wav, webm
- 文件大小限制：25 MB

## 2. 基础功能

### 2.1 环境准备
首先，安装必要的依赖：

```bash
pip install openai python-dotenv
```

### 2.2 基础示例
让我们从一个简单的音频转录示例开始。我们将使用上一章生成的语音文件作为输入：

> 🔊 [示例音频文件](https://z1.zve.cn/tutorial/llm-basics/test_speech.mp3)

```python
from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv

def transcribe_audio(input_file, prompt=None):
    """转录音频文件为文本
    
    Args:
        input_file (str): 输入音频文件路径
        prompt (str, optional): 提示词，帮助提高识别准确率
        
    Returns:
        dict: 转录结果，包含文本和详细信息
    """
    # 加载环境变量
    load_dotenv()
    
    # 初始化客户端
    client = OpenAI()
    
    # 打开音频文件
    with open(input_file, "rb") as audio_file:
        try:
            # 调用API转录音频
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",  # 获取详细信息
                timestamp_granularities=["word"]  # 获取词级别时间戳
            )
            return transcription
            
        except Exception as e:
            print(f"转录失败：{str(e)}")
            return None

# 使用示例
audio_file = "test_audio.mp3"
result = transcribe_audio(audio_file)
if result:
    print("转录文本：", result.text)
    print("语言：", result.language)
    print("持续时间：", result.duration, "秒")
```

### 2.3 音频翻译
将非英语音频直接翻译为英文：

```python
def translate_audio(input_file):
    """将音频翻译为英文
    
    Args:
        input_file (str): 输入音频文件路径
        
    Returns:
        str: 英文翻译结果
    """
    client = OpenAI()
    
    with open(input_file, "rb") as audio_file:
        try:
            translation = client.audio.translations.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
            return translation
            
        except Exception as e:
            print(f"翻译失败：{str(e)}")
            return None

# 使用示例
chinese_audio = "chinese_speech.mp3"
english_text = translate_audio(chinese_audio)
print("英文翻译：", english_text)
```

## 3. 高级功能

### 3.1 时间戳生成
获取词级别的时间戳，方便生成字幕：

```python
def get_word_timestamps(audio_file):
    """获取词级别的时间戳
    
    Args:
        audio_file (str): 音频文件路径
        
    Returns:
        list: 包含每个词的时间戳信息
    """
    result = transcribe_audio(audio_file)
    if not result:
        return []
        
    timestamps = []
    for word in result.words:
        timestamps.append({
            'word': word.word,
            'start': word.start,
            'end': word.end
        })
    return timestamps
```

### 3.2 提示词优化
使用提示词提高特定场景的准确率：

```python
# 医疗领域示例
medical_prompt = """
这是一段医疗相关的音频，包含以下专业术语：
- 高血压 (Hypertension)
- 心律失常 (Arrhythmia)
- 冠状动脉疾病 (Coronary Artery Disease)
"""

result = transcribe_audio(
    "medical_audio.mp3",
    prompt=medical_prompt
)
```

### 3.3 长音频处理
使用PyDub处理超过25MB的音频：

```python
from pydub import AudioSegment

def process_long_audio(input_file, segment_duration=600000):
    """处理长音频文件
    
    Args:
        input_file (str): 输入音频文件
        segment_duration (int): 分段时长（毫秒）
    """
    # 加载音频
    audio = AudioSegment.from_mp3(input_file)
    
    # 分段处理
    segments = []
    for i in range(0, len(audio), segment_duration):
        segment = audio[i:i+segment_duration]
        segment_path = f"segment_{i//segment_duration}.mp3"
        segment.export(segment_path, format="mp3")
        segments.append(segment_path)
    
    # 转录每个片段
    full_text = []
    for segment_path in segments:
        result = transcribe_audio(segment_path)
        if result:
            full_text.append(result.text)
    
    return "\n".join(full_text)
```

## 4. 最佳实践

### 4.1 音频预处理
1. **质量优化**：
   - 降低背景噪音
   - 提高音频清晰度
   - 调整采样率和比特率

2. **格式转换**：
   - 选择最佳格式
   - 压缩大文件
   - 保持音质平衡

### 4.2 准确率提升
1. **提示词设计**：
   - 提供领域术语
   - 说明音频上下文
   - 指定输出格式

2. **分段策略**：
   - 按自然停顿分段
   - 避免句子中断
   - 保持上下文连贯

### 4.3 后处理优化
1. **文本清理**：
   - 修正标点符号
   - 格式化段落
   - 统一术语用法

2. **质量检查**：
   - 人工校对关键内容
   - 验证专业术语
   - 保持语言一致性

## 5. 扩展资源

### 5.1 相关文档
- [OpenAI Whisper API文档](https://platform.openai.com/docs/guides/speech-to-text)
- [Whisper模型论文](https://arxiv.org/abs/2212.04356)
- [音频处理最佳实践](https://platform.openai.com/docs/guides/speech-to-text/transcriptions-and-translations)

### 5.2 示例代码
完整的示例代码可以在 [GitHub仓库](examples/) 中找到。

### 5.3 常见问题
1. **如何提高准确率？**
   - 使用高质量音频
   - 提供准确的提示词
   - 选择合适的分段策略

2. **如何处理多语言？**
   - 使用语言检测
   - 选择合适的API
   - 处理代码切换

3. **如何优化性能？**
   - 实现并行处理
   - 使用缓存策略
   - 优化文件大小

## 小结

本节我们学习了：
1. 使用Whisper API进行音频转录和翻译
2. 处理长音频和生成时间戳
3. 优化转录准确率和性能
4. 实现多语言音频处理

下一步，你可以：
- 尝试不同类型的音频转录
- 构建自动字幕生成系统
- 开发多语言音频处理应用
