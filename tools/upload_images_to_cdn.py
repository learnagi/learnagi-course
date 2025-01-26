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

def process_markdown_file(markdown_path, uploader):
    """处理单个markdown文件"""
    print(f"\n处理文件: {markdown_path}")
    
    with open(markdown_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 创建备份
    backup_path = f"{markdown_path}.bak"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"创建备份: {backup_path}")

    # 获取markdown文件的基础目录
    base_dir = os.path.dirname(os.path.abspath(markdown_path))

    # 查找所有图片和音频链接
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    audio_pattern = r'🔊 \[([^\]]*)\]\(([^)]+)\)'
    
    # 处理图片
    matches = re.finditer(image_pattern, content)
    uploaded_count = 0
    for match in matches:
        alt_text, file_path = match.groups()
        
        # 如果是本地文件路径
        if not file_path.startswith(('http://', 'https://')):
            # 转换为绝对路径
            if file_path.startswith('./'):
                file_path = file_path[2:]
            abs_file_path = os.path.normpath(os.path.join(base_dir, file_path))
            
            # 检查文件是否存在
            if os.path.exists(abs_file_path):
                # 上传到七牛
                cdn_url = uploader.upload_file(abs_file_path, markdown_path)
                if cdn_url:
                    # 替换markdown中的链接
                    content = content.replace(f'![{alt_text}]({file_path})', f'![{alt_text}]({cdn_url})')
                    uploaded_count += 1
                    print(f"✓ 上传成功: {file_path} -> {cdn_url}")
            else:
                print(f"× 文件不存在: {abs_file_path}")
    
    # 处理音频
    matches = re.finditer(audio_pattern, content)
    for match in matches:
        alt_text, file_path = match.groups()
        
        # 如果是本地文件路径
        if not file_path.startswith(('http://', 'https://')):
            # 转换为绝对路径
            if file_path.startswith('./'):
                file_path = file_path[2:]
            abs_file_path = os.path.normpath(os.path.join(base_dir, file_path))
            
            # 检查文件是否存在
            if os.path.exists(abs_file_path):
                # 上传到七牛
                cdn_url = uploader.upload_file(abs_file_path, markdown_path)
                if cdn_url:
                    # 替换markdown中的链接
                    content = content.replace(f'🔊 [{alt_text}]({file_path})', f'🔊 [{alt_text}]({cdn_url})')
                    uploaded_count += 1
                    print(f"✓ 上传成功: {file_path} -> {cdn_url}")
            else:
                print(f"× 文件不存在: {abs_file_path}")

    # 如果有文件被上传，保存更新后的内容
    if uploaded_count > 0:
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✓ 更新了 {uploaded_count} 个文件链接")
    else:
        print("\n没有需要上传的文件")
        # 删除备份
        os.remove(backup_path)

def main():
    parser = argparse.ArgumentParser(description='上传markdown文件中的图片和音频到七牛云')
    parser.add_argument('markdown_files', nargs='+', help='要处理的markdown文件路径')
    parser.add_argument('--access-key', help='七牛云 Access Key')
    parser.add_argument('--secret-key', help='七牛云 Secret Key')
    parser.add_argument('--bucket', help='七牛云 Bucket 名称')
    parser.add_argument('--domain', help='七牛云域名')
    
    args = parser.parse_args()
    
    # 创建上传器实例
    uploader = ImageUploader(
        access_key=args.access_key,
        secret_key=args.secret_key,
        bucket_name=args.bucket,
        domain=args.domain
    )
    
    # 处理每个markdown文件
    for md_file in args.markdown_files:
        if not os.path.exists(md_file):
            print(f"文件不存在: {md_file}")
            continue
            
        if not md_file.endswith('.md'):
            print(f"不是markdown文件: {md_file}")
            continue
            
        process_markdown_file(md_file, uploader)

if __name__ == '__main__':
    main()
