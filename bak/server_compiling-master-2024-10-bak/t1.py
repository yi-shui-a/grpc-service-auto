import re

def extract_documentation_info(file_path):
    # 正则表达式来匹配文档信息
    doc_pattern = re.compile(
        r'/\*\*\s*\n'  # 开始标记
        r'(\s*@file\s+(?P<file>.*?))\n'  # 匹配文件名
        r'(\s*@author\s+(?P<author>.*?))\n'  # 匹配作者
        r'(\s*@version\s+(?P<version>.*?))\n'  # 匹配版本
        r'(\s*@date\s+(?P<date>.*?))\n'  # 匹配日期
        r'(\s*@brief\s+(?P<brief>.*?))'  # 匹配简介
        r'.*\*/',  # 结束标记
        re.DOTALL | re.MULTILINE
    )

    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 查找所有匹配项
    match = doc_pattern.search(content)

    if match:
        info = match.groupdict()
        return {
            'file': info.get('file', '').strip(),
            'author': info.get('author', '').strip(),
            'version': info.get('version', '').strip(),
            'date': info.get('date', '').strip(),
            'brief': info.get('brief', '').strip()
        }
    else:
        return None

# 使用函数
file_path = 't1.h'  # 替换为你的文件路径
doc_info = extract_documentation_info(file_path)

if doc_info:
    print(f"File: {doc_info['file']}")
    print(f"Author: {doc_info['author']}")
    print(f"Version: {doc_info['version']}")
    print(f"Date: {doc_info['date']}")
    print(f"Brief: {doc_info['brief']}")
else:
    print("No documentation information found.")