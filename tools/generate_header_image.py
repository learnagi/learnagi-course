#!/usr/bin/env python3
"""
教程题图生成工具，支持自定义输出路径、课程内容和品牌 Logo。
"""

import argparse
from datetime import datetime
from dotenv import load_dotenv
import os
from pathlib import Path
import requests
import sys

load_dotenv()

class HeaderImageGenerator:
    """教程题图生成器"""
    
    def __init__(self, api_key=None, api_base=None):
        self.api_base = api_base or "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_header_image(self, title, content, doc_path, brand_logo_text="AGI01"):
        """生成课程封面图片"""
        prompt = f"""
        Flat illustration of {content} concepts presented on a modern dashboard interface, 
        designed for an educational course cover titled "{title}" with a balanced 16:9 layout. 
        The design features a vibrant blue color scheme with smooth gradients, 
        sleek UI elements, and a clean white background. 
        
        Key elements to include:
        - Data visualization charts (line, bar, pie charts)
        - Security icons (shield, lock, fingerprint)
        - Network topology visualization
        - Friendly 3D robot character analyzing data
        - {brand_logo_text} logo in top-left corner with modern typography
        
        Style requirements:
        - Minimalist flat design
        - Consistent blue color palette (#2A5CAA to #4A90E2 gradients)
        - Subtle drop shadows for depth
        - 4K resolution quality
        - Corporate but approachable tone
        """
        
        try:
            print(f"正在调用API: {self.api_base}")
            response = requests.post(
                f"{self.api_base}/images/generations",
                headers=self.headers,
                json={
                    "model": "dall-e-3",
                    "prompt": prompt,
                    "n": 1,
                    "size": "1792x1024",
                    "quality": "standard"
                }
            )
            
            print(f"API响应状态码: {response.status_code}")
            print(f"API响应内容: {response.text}")
            
            if response.status_code != 200:
                print(f"API错误: {response.text}")
                return None
                
            response_data = response.json()
            print(f"解析的响应数据: {response_data}")
            
            if not response_data.get('data'):
                print("响应中没有data字段")
                return None
                
            image_url = response_data['data'][0]['url']
            
            # 根据文档路径动态生成输出路径
            output_dir = os.path.dirname(doc_path)
            filename = "header.png"
            output_path = os.path.join(output_dir, "images", filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 下载并保存图片
            self._download_image(image_url, output_path)
            
            # 更新文档中的图片引用
            self._update_documentation(filename, doc_path)
            
            return output_path
            
        except Exception as e:
            print(f"图像生成失败: {str(e)}")
            return None

    def _download_image(self, url: str, save_path: str):
        """下载图片并保存"""
        response = requests.get(url)
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"图片已保存至: {save_path}")

    def _update_documentation(self, filename, doc_path):
        """更新文档中的图片引用"""
        new_header = f"![Header Image](./images/{filename})"
        
        with open(doc_path, "r+", encoding="utf-8") as f:
            content = f.read()
            updated_content = content.replace(
                "![Header Image](./images/image-generation/header.png)",
                new_header
            )
            f.seek(0)
            f.write(updated_content)
            f.truncate()
        
        print("文档封面图片已更新")

def main():
    parser = argparse.ArgumentParser(description="生成教程题图")
    parser.add_argument("--title", required=True, help="课程标题")
    parser.add_argument("--content", required=True, help="课程内容描述")
    parser.add_argument("--doc-path", required=True, help="当前文档路径")
    parser.add_argument("--api-base", default="https://api.openai.com/v1", help="API基础URL")
    parser.add_argument("--brand-logo", default="AGI01", help="品牌 Logo 文字")
    parser.add_argument("--api-key", help="OpenAI API密钥")
    
    args = parser.parse_args()
    
    # 获取API密钥（优先使用命令行参数，其次使用环境变量）
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("错误：未提供 API 密钥。请通过 --api-key 参数或 OPENAI_API_KEY 环境变量提供。")
        sys.exit(1)
    
    try:
        generator = HeaderImageGenerator(api_key=api_key, api_base=args.api_base)
        print(f"正在为《{args.title}》生成题图...")
        image_path = generator.generate_header_image(args.title, args.content, args.doc_path, args.brand_logo)
        if image_path:
            print(f"封面图片生成成功: {image_path}")
    
    except Exception as e:
        print(f"错误：生成题图失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
