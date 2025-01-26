#!/usr/bin/env python3
"""
文本到语音转换示例集合，展示不同的使用场景和功能。
"""

import os
from pathlib import Path
from openai import OpenAI
import time

class SpeechExamples:
    def __init__(self, api_key: str = None):
        """初始化客户端
        
        Args:
            api_key: OpenAI API密钥，如果为None则从环境变量获取
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.fe8.cn/v1"
        )
        self.output_dir = Path(__file__).parent / "audio_outputs"
        self.output_dir.mkdir(exist_ok=True)
        
    def basic_speech(self):
        """基础语音生成示例"""
        print("\n=== 基础语音生成 ===")
        
        speech_file = self.output_dir / "basic_speech.mp3"
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input="你好！这是一个基础的语音生成示例。"
        )
        response.stream_to_file(str(speech_file))
        print(f"基础语音已保存到: {speech_file}")
        
    def different_voices(self):
        """展示不同的声音选项"""
        print("\n=== 不同声音示例 ===")
        
        text = "人工智能正在改变我们的生活方式。"
        voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        
        for voice in voices:
            speech_file = self.output_dir / f"voice_{voice}.mp3"
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            response.stream_to_file(str(speech_file))
            print(f"{voice} 声音已保存到: {speech_file}")
            time.sleep(1)  # 避免请求过快
            
    def different_formats(self):
        """展示不同的音频格式"""
        print("\n=== 不同格式示例 ===")
        
        text = "这是一个音频格式测试。"
        formats = ["mp3", "opus", "aac", "flac", "pcm"]
        
        for format in formats:
            speech_file = self.output_dir / f"format_{format}.{format}"
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text,
                response_format=format
            )
            response.stream_to_file(str(speech_file))
            print(f"{format} 格式已保存到: {speech_file}")
            time.sleep(1)  # 避免请求过快
            
    def different_languages(self):
        """多语言示例"""
        print("\n=== 多语言示例 ===")
        
        languages = {
            "chinese": "人工智能正在改变世界。",
            "english": "Artificial Intelligence is changing the world.",
            "japanese": "人工知能は世界を変えています。",
            "korean": "인공지능이 세상을 바꾸고 있습니다.",
            "french": "L'intelligence artificielle change le monde.",
            "german": "Künstliche Intelligenz verändert die Welt.",
            "spanish": "La inteligencia artificial está cambiando el mundo."
        }
        
        for lang, text in languages.items():
            speech_file = self.output_dir / f"lang_{lang}.mp3"
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="nova",  # nova适合多语言
                input=text
            )
            response.stream_to_file(str(speech_file))
            print(f"{lang} 语音已保存到: {speech_file}")
            time.sleep(1)  # 避免请求过快
            
    def high_quality_speech(self):
        """高质量语音示例"""
        print("\n=== 高质量语音示例 ===")
        
        # 使用较长的文本来展示质量差异
        text = """
        欢迎来到AGI课程！在这里，我们将探索人工智能的前沿技术。
        从基础的机器学习算法到先进的神经网络架构，
        从自然语言处理到计算机视觉，
        我们将带您深入了解AI的每个重要领域。
        让我们一起开启这段激动人心的学习之旅！
        """
        
        # 标准质量
        speech_file_standard = self.output_dir / "quality_standard.mp3"
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        response.stream_to_file(str(speech_file_standard))
        print(f"标准质量语音已保存到: {speech_file_standard}")
        
        # 高质量
        speech_file_hd = self.output_dir / "quality_hd.mp3"
        response = self.client.audio.speech.create(
            model="tts-1-hd",
            voice="nova",
            input=text
        )
        response.stream_to_file(str(speech_file_hd))
        print(f"高清质量语音已保存到: {speech_file_hd}")
        
    def streaming_example(self):
        """流式输出示例"""
        print("\n=== 流式输出示例 ===")
        
        speech_file = self.output_dir / "streaming.mp3"
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input="这是一个流式输出测试，音频可以在生成的同时播放。" * 5  # 重复5次使效果更明显
        )
        
        # 使用流式方式写入文件
        with open(speech_file, 'wb') as f:
            for chunk in response.iter_bytes(chunk_size=4096):
                f.write(chunk)
                print(".", end="", flush=True)  # 显示进度
        print(f"\n流式音频已保存到: {speech_file}")

def main():
    # 从环境变量获取API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("请设置OPENAI_API_KEY环境变量")
        return
        
    examples = SpeechExamples(api_key)
    
    # 运行所有示例
    examples.basic_speech()
    examples.different_voices()
    examples.different_formats()
    examples.different_languages()
    examples.high_quality_speech()
    examples.streaming_example()
    
    print("\n所有示例已生成完成！")
    print(f"音频文件保存在: {examples.output_dir}")

if __name__ == "__main__":
    main()
