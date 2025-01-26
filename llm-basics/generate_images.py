import requests
import json
import os
from PIL import Image
from io import BytesIO

class ImageGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.api_base = "https://api.fe8.cn/v1"
        
    def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        """生成图像并返回URL"""
        try:
            response = requests.post(
                f"{self.api_base}/images/generations",
                headers=self.headers,
                json={
                    "model": "dall-e-3",
                    "prompt": prompt,
                    "n": 1,
                    "size": size,
                    "quality": "standard"
                }
            )
            
            if response.status_code != 200:
                print(f"API错误: {response.text}")
                return None
                
            print(f"API响应: {response.text}")  
            return response.json()['data'][0]['url']
            
        except Exception as e:
            print(f"生成图像时出错: {str(e)}")
            return None
            
    def save_image(self, url: str, output_path: str):
        """保存图片到本地
        
        Args:
            url: 图片URL
            output_path: 输出路径
        """
        try:
            # 创建输出目录
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 下载图片
            response = requests.get(url)
            if response.status_code == 200:
                # 将图片数据转换为PIL Image对象
                image = Image.open(BytesIO(response.content))
                # 保存图片
                image.save(output_path)
                print(f"图片已保存到: {output_path}")
            else:
                print(f"下载图片失败: {response.status_code}")
        except Exception as e:
            print(f"保存图片时出错: {str(e)}")

def main():
    # 测试不同风格的提示词
    prompts = [
        # 扁平设计
        """Digital illustration in Flat Design style of a modern workspace with a desk, laptop, and plants, 
        using clean lines and bold colors. The scene is well-lit with natural lighting from a large window. 
        Minimalist aesthetic with a color palette of soft blues and warm grays.""",
        
        # 等距风格
        """Isometric illustration of a smart city concept with modern buildings, flying vehicles, 
        and green energy solutions. Clean geometric shapes, consistent 120-degree angles, 
        bold color palette with tech-inspired blues and whites.""",
        
        # 水彩风格
        """Watercolor illustration of a serene Japanese garden in spring, 
        with blooming cherry blossoms, a small wooden bridge over a koi pond, 
        and traditional stone lanterns. Soft, flowing colors with visible brush strokes.""",
        
        # 数据安全仪表盘
        """Here is the flat illustration of a professional discussing data security on a futuristic dashboard, 
        featuring a gradient color scheme of deep blue, soft purple, and white highlights.""",
        
        # 圣诞树
        """A cute 3D-rendered Christmas tree with bright, vibrant colors in a minimalistic Disney-inspired style. 
        Featuring simple, rounded shapes, soft lighting, and a cheerful festive atmosphere on a clean background.""",
        
        # 礼物盒
        """A cute 3D-rendered gift box with bright, playful colors in a simple, Disney-inspired style. 
        Designed with smooth, rounded edges, soft lighting, and a festive, minimalistic appearance, 
        set against a clean background."""
    ]
    
    generator = ImageGenerator("sk-HJZYbJr4678xRYeHxnm8IwgYbQohng5RFrAeghDzTlIZyLwp")
    
    # 为每个提示词生成图像
    for i, prompt in enumerate(prompts, 1):
        print(f"\n生成图像 {i}...")
        print(f"原始提示词: {prompt[:100]}...")
        url = generator.generate_image(prompt)
        if url:
            print(f"图像URL: {url}")
            # 保存图片到本地
            output_path = f"images/generated_image_{i}.png"
            generator.save_image(url, output_path)
        print("-" * 80)

if __name__ == "__main__":
    main()
