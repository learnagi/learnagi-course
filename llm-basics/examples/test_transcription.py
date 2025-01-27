from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv

def transcribe_audio(input_file, prompt=None):
    """转录音频文件为文本"""
    # 加载环境变量
    load_dotenv()
    
    # 从环境变量获取API密钥
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("请在.env文件中设置OPENAI_API_KEY")
    
    # 初始化客户端
    client = OpenAI(api_key=api_key)
    
    # 打开音频文件
    with open(input_file, "rb") as audio_file:
        # 调用API转录音频
        try:
            # 基础转录
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",  # 使用详细JSON格式以获取更多信息
                timestamp_granularities=["word"],  # 获取词级别的时间戳
                prompt=prompt  # 可选的提示词，帮助提高准确性
            )
            
            print("✓ 转录成功！")
            print("\n文本内容：")
            print(transcription.text)
            
            print("\n详细信息：")
            print(f"语言：{transcription.language}")
            print(f"持续时间：{transcription.duration}秒")
            
            print("\n词级别时间戳：")
            for word in transcription.words:
                print(f"{word.word}: {word.start:.2f}s - {word.end:.2f}s")
                
            return transcription
            
        except Exception as e:
            print(f"转录失败：{str(e)}")
            return None

def translate_audio(input_file):
    """将音频翻译为英文"""
    # 加载环境变量
    load_dotenv()
    
    # 从环境变量获取API密钥
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("请在.env文件中设置OPENAI_API_KEY")
    
    # 初始化客户端
    client = OpenAI(api_key=api_key)
    
    # 打开音频文件
    with open(input_file, "rb") as audio_file:
        # 调用API翻译音频
        try:
            translation = client.audio.translations.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"  # 使用纯文本格式
            )
            
            print("✓ 翻译成功！")
            print("\n英文内容：")
            print(translation)
            return translation
            
        except Exception as e:
            print(f"翻译失败：{str(e)}")
            return None

if __name__ == "__main__":
    # 使用之前生成的测试音频文件
    audio_file = Path(__file__).parent / "audio_outputs" / "test_speech.mp3"
    
    print("1. 转录音频为文本")
    print("-" * 50)
    transcription = transcribe_audio(
        audio_file,
        prompt="这是一个OpenAI TTS API的测试音频"  # 提供上下文提示词
    )
    
    print("\n2. 翻译音频为英文")
    print("-" * 50)
    translation = translate_audio(audio_file)
