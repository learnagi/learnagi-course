from pathlib import Path
from openai import OpenAI
import os
from dotenv import load_dotenv

def generate_test_speech():
    """生成测试语音"""
    # 加载环境变量
    load_dotenv()
    
    # 从环境变量获取API密钥
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("请在.env文件中设置OPENAI_API_KEY")
    
    # 初始化客户端
    client = OpenAI(api_key=api_key)
    
    # 创建输出目录
    output_dir = Path(__file__).parent / "audio_outputs"
    output_dir.mkdir(exist_ok=True)
    
    # 生成测试语音
    text = "大家好！这是一个测试音频。我们正在使用OpenAI的TTS API，将文本转换为自然流畅的语音。让我们一起来探索更多有趣的功能吧！"
    
    print("正在生成语音...")
    
    try:
        # 使用普通响应方式
        response = client.audio.speech.create(
            model="tts-1",      # 使用标准音质
            voice="nova",       # 使用自然流畅的声音
            input=text,
            response_format="mp3"  # 明确指定格式
        )
        
        # 打印响应信息
        print("响应类型:", type(response))
        
        # 保存音频
        output_file = output_dir / "test_speech.mp3"
        
        # 检查响应内容
        if hasattr(response, 'content'):
            content = response.content
            # 检查是否为JSON错误响应
            try:
                import json
                error_json = json.loads(content)
                print("错误响应:", json.dumps(error_json, indent=2, ensure_ascii=False))
            except:
                # 不是JSON，应该是二进制音频数据
                with open(output_file, 'wb') as f:
                    f.write(content)
                print("成功保存音频文件")
        else:
            print("错误：响应中没有音频内容")
            if hasattr(response, 'text'):
                print("响应文本:", response.text)
            
        print(f"\n音频文件位置: {output_file}")
        
    except Exception as e:
        print(f"错误：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_test_speech()
