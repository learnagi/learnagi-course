#!/usr/bin/env python3
"""
文本到语音转换工具，支持多种声音风格和语言。
"""

import requests
import json
import os
from pathlib import Path

class SpeechGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.api_base = "https://api.openai.com/v1"
        
    def generate_speech(self, text: str, voice="alloy", model="tts-1", output_path="output.mp3"):
        """生成语音并保存到文件
        
        Args:
            text: 要转换的文本
            voice: 声音类型，可选 alloy, echo, fable, onyx, nova, shimmer
            model: TTS模型，可选 tts-1, tts-1-hd
            output_path: 输出文件路径
        """
        try:
            print(f"正在生成语音...")
            print(f"文本: {text}")
            print(f"声音: {voice}")
            print(f"模型: {model}")
            
            response = requests.post(
                f"{self.api_base}/audio/speech",
                headers=self.headers,
                json={
                    "model": model,
                    "input": text,
                    "voice": voice
                }
            )
            
            if response.status_code != 200:
                print(f"API错误: {response.text}")
                return None
            
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 保存音频文件
            with open(output_path, "wb") as f:
                f.write(response.content)
                
            print(f"音频已保存到: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"生成语音时出错: {str(e)}")
            return None

def main():
    # 测试不同的声音和文本
    texts = [
        # 中文测试
        {
            "text": "欢迎来到人工智能课程，今天我们将学习如何使用大语言模型生成语音。",
            "voice": "alloy",
            "filename": "welcome_zh.mp3"
        },
        # 英文测试
        {
            "text": "Welcome to the AI course. Today we'll learn how to generate speech using large language models.",
            "voice": "nova",
            "filename": "welcome_en.mp3"
        },
        # 情感表达测试
        {
            "text": "这是一个激动人心的时刻！人工智能正在改变我们的生活方式。",
            "voice": "shimmer",
            "filename": "excited_zh.mp3"
        }
    ]
    
    # 从环境变量获取API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("请设置OPENAI_API_KEY环境变量")
        return
        
    generator = SpeechGenerator(api_key)
    
    # 生成所有测试音频
    for item in texts:
        print("\n" + "-" * 80)
        generator.generate_speech(
            text=item["text"],
            voice=item["voice"],
            output_path=f"audio/{item['filename']}"
        )
        print("-" * 80)

if __name__ == "__main__":
    main()
