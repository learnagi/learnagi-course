from pathlib import Path
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

def generate_speech(client, text, output_file, **kwargs):
    """生成语音并保存到文件"""
    print(f"生成 {output_file}...")
    try:
        response = client.audio.speech.create(
            model="tts-1",
            input=text,
            **kwargs
        )
        
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"✓ 成功生成: {output_file}")
        
    except Exception as e:
        print(f"✗ 生成失败: {output_file}")
        print(f"  错误: {str(e)}")

def main():
    # 加载环境变量
    load_dotenv()
    
    # 从环境变量获取API密钥
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("请在.env文件中设置OPENAI_API_KEY")
    
    # 初始化OpenAI客户端
    client = OpenAI(api_key=api_key)
    
    # 创建输出目录
    output_dir = Path(__file__).parent / "audio_outputs"
    output_dir.mkdir(exist_ok=True)
    
    # 基础示例
    generate_speech(
        client,
        "这是一个基础的语音生成示例。我们使用OpenAI的TTS API将文本转换为语音。",
        output_dir / "basic_speech.mp3",
        voice="nova"
    )
    
    # 不同格式示例
    formats = {
        "mp3": {
            "text": "这是MP3格式的音频示例。MP3是最常用的音频格式，它在音质和文件大小之间取得了很好的平衡。",
            "response_format": "mp3"
        },
        "opus": {
            "text": "这是Opus格式的音频示例。Opus格式特别适合网络流媒体和实时通信，因为它具有低延迟的特点。",
            "response_format": "opus"
        },
        "aac": {
            "text": "这是AAC格式的音频示例。AAC是一种高效的音频压缩格式，被YouTube和iOS等平台广泛使用。",
            "response_format": "aac"
        },
        "flac": {
            "text": "这是FLAC格式的音频示例。FLAC是一种无损音频压缩格式，非常适合音频存档和高品质音乐播放。",
            "response_format": "flac"
        }
    }
    
    for fmt, config in formats.items():
        generate_speech(
            client,
            config["text"],
            output_dir / f"format_{fmt}.{fmt}",
            voice="nova",
            response_format=config["response_format"]
        )
    
    # 不同声音示例
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    for voice in voices:
        generate_speech(
            client,
            f"你好，我是{voice}声音。这是一个示例。",
            output_dir / f"voice_{voice}.mp3",
            voice=voice
        )
    
    # 多语言示例
    languages = {
        "chinese": "你好，这是中文示例。",
        "english": "Hello, this is an English example.",
        "japanese": "こんにちは、これは日本語の例です。",
        "korean": "안녕하세요, 이것은 한국어 예시입니다.",
        "french": "Bonjour, c'est un exemple en français.",
        "german": "Hallo, dies ist ein Beispiel auf Deutsch.",
        "spanish": "Hola, este es un ejemplo en español."
    }
    
    for lang, text in languages.items():
        generate_speech(
            client,
            text,
            output_dir / f"lang_{lang}.mp3",
            voice="nova"
        )
    
    # 不同质量示例
    for model in ["tts-1", "tts-1-hd"]:
        suffix = "hd" if model == "tts-1-hd" else "standard"
        generate_speech(
            client,
            "这是一个音频质量示例，请仔细听音质的区别。",
            output_dir / f"quality_{suffix}.mp3",
            voice="nova",
            model=model
        )
    
    # 流式输出示例
    generate_speech(
        client,
        "这是一个较长的文本示例，用于演示流式输出功能。在实际应用中，我们可以边生成边播放音频，提供更好的用户体验。",
        output_dir / "streaming.mp3",
        voice="nova"
    )

if __name__ == "__main__":
    main()
