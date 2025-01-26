#!/usr/bin/env python3
import sys
import PyPDF2
import argparse

def read_pdf(pdf_path):
    """读取PDF文件内容"""
    try:
        with open(pdf_path, 'rb') as file:
            # 创建PDF阅读器对象
            pdf_reader = PyPDF2.PdfReader(file)
            
            # 获取页数
            num_pages = len(pdf_reader.pages)
            print(f"\nPDF文件共有 {num_pages} 页\n")
            
            # 读取每一页的内容
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                print(f"=== 第 {page_num + 1} 页 ===")
                print(text)
                print()
                
    except Exception as e:
        print(f"读取PDF时出错: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='读取PDF文件内容')
    parser.add_argument('pdf_path', help='PDF文件路径')
    
    args = parser.parse_args()
    read_pdf(args.pdf_path)

if __name__ == '__main__':
    main()
