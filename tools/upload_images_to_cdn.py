#!/usr/bin/env python3
import os
import re
import sys
import hashlib
from datetime import datetime
from qiniu import Auth, put_file, etag
import argparse
import glob
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

class ImageUploader:
    def __init__(self, access_key=None, secret_key=None, bucket_name=None, domain=None):
        """初始化七牛云配置"""
        self.access_key = access_key or os.getenv('QINIU_ACCESS_KEY')
        self.secret_key = secret_key or os.getenv('QINIU_SECRET_KEY')
        self.bucket_name = bucket_name or os.getenv('QINIU_BUCKET')
        self.domain = domain or os.getenv('QINIU_DOMAIN')
        
        if not all([self.access_key, self.secret_key, self.bucket_name, self.domain]):
            print("错误: 缺少必要的配置信息。请确保以下环境变量已设置：")
            print("- QINIU_ACCESS_KEY")
            print("- QINIU_SECRET_KEY")
            print("- QINIU_BUCKET")
            print("- QINIU_DOMAIN")
            print("\n或者通过命令行参数提供这些值。")
            sys.exit(1)
            
        self.auth = Auth(self.access_key, self.secret_key)
        
    def get_file_hash(self, filepath):
        """获取文件的MD5哈希值"""
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    
    def upload_file(self, local_file, markdown_file):
        """上传单个文件到七牛云"""
        try:
            # 获取文件名
            filename = os.path.basename(local_file)
            
            # 获取教程名称（从markdown文件路径中提取）
            # 例如：从 ml-basics/linear-regression.md 提取 linear-regression
            md_path = os.path.dirname(markdown_file)  # 获取markdown文件所在目录
            tutorial_name = os.path.basename(md_path)  # 获取教程名称
            
            # 构建七牛云上的文件名
            key = f"tutorial/{tutorial_name}/{filename}"
            
            # 生成上传凭证
            token = self.auth.upload_token(self.bucket_name, key, 3600)
            
            # 上传文件
            ret, info = put_file(token, key, local_file)
            
            if info.status_code == 200:
                return f"https://z1.zve.cn/{key}"
            else:
                print(f"上传失败: {info}")
                return None
        except Exception as e:
            print(f"上传出错: {e}")
            return None

def process_markdown_file(file_path, uploader):
    """处理单个markdown文件"""
    print(f"\n处理文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 创建备份
    backup_path = f"{file_path}.bak"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"创建备份: {backup_path}")

    # 查找所有图片链接
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.finditer(pattern, content)
    
    uploaded_count = 0
    for match in matches:
        alt_text, image_path = match.groups()
        
        # 如果是本地图片路径
        if not image_path.startswith(('http://', 'https://')):
            # 转换为绝对路径
            if image_path.startswith('./'):
                image_path = image_path[2:]
            abs_image_path = os.path.join(os.path.dirname(file_path), image_path)
            
            # 检查文件是否存在
            if not os.path.exists(abs_image_path):
                print(f"✗ 文件不存在: {abs_image_path}")
                continue
                
            # 上传图片
            print(f"上传图片: {abs_image_path}")
            cdn_url = uploader.upload_file(abs_image_path, file_path)  # 传入markdown文件路径以获取教程名称
            if cdn_url:
                content = content.replace(match.group(0), f'![{alt_text}]({cdn_url})')
                print(f"✓ 成功上传: {cdn_url}")
                uploaded_count += 1
        else:
            # 对于已经是CDN链接的图片，检查是否需要更新文件名
            if 'z1.zve.cn/tutorial/images/' in image_path:
                # 获取本地对应的图片
                old_filename = image_path.split('/')[-1]
                if old_filename.startswith(('fee74e00', '4f6cbc99', '87986183', '4c7a2ebb', '00cca07c', 'e1a68097', '0cb9fcf7', '031c1dd1')):
                    # 根据alt_text找到对应的本地文件
                    local_files = [f for f in os.listdir(os.path.join(os.path.dirname(file_path), 'images')) if f.endswith('.png')]
                    for local_file in local_files:
                        if alt_text.replace(' ', '-').lower() in local_file.lower():
                            local_image_path = os.path.join(os.path.dirname(file_path), 'images', local_file)
                            print(f"更新图片: {local_image_path}")
                            cdn_url = uploader.upload_file(local_image_path, file_path)
                            if cdn_url:
                                content = content.replace(match.group(0), f'![{alt_text}]({cdn_url})')
                                print(f"✓ 成功更新: {cdn_url}")
                                uploaded_count += 1
                            break

    if uploaded_count > 0:
        # 写入更新后的内容
        print(f"更新文件: {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"\n完成! 共处理 {uploaded_count} 张图片\n")

def main():
    parser = argparse.ArgumentParser(description='上传Markdown文件中的图片到七牛云CDN')
    parser.add_argument('path', help='Markdown文件路径或目录路径')
    parser.add_argument('--ak', help='七牛云 Access Key')
    parser.add_argument('--sk', help='七牛云 Secret Key')
    parser.add_argument('--bucket', help='七牛云 Bucket 名称')
    parser.add_argument('--domain', help='七牛云域名')
    
    args = parser.parse_args()
    
    # 初始化上传器
    uploader = ImageUploader(args.ak, args.sk, args.bucket, args.domain)
    
    # 处理文件或目录
    if os.path.isfile(args.path):
        if args.path.endswith('.md'):
            process_markdown_file(args.path, uploader)
    elif os.path.isdir(args.path):
        total_count = 0
        for md_file in glob.glob(os.path.join(args.path, '**/*.md'), recursive=True):
            process_markdown_file(md_file, uploader)
            total_count += 1
        print(f"\n完成! 共处理 {total_count} 张图片")
    else:
        print("错误: 指定的路径不存在")
        sys.exit(1)

if __name__ == '__main__':
    main()
