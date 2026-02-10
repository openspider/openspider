#!/usr/bin/env python3
"""
OpenSpider文档自动同步工具
每次文件保存后，运行此脚本自动上传到GitHub

用法:
    python3 auto_upload.py              # 上传所有文件
    python3 auto_upload.py 文件1 文件2  # 上传指定文件
"""

import os
import sys
import base64
import subprocess
import requests
import json
from pathlib import Path
from datetime import datetime

# 配置
TOKEN = "${GITHUB_TOKEN}"
REPO = "openspider/openspider"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "OpenSpider-AutoSync/1.0"
}

# 忽略列表
IGNORE_DIRS = ['.git', 'node_modules', '__pycache__']
IGNORE_FILES = ['.deploy-config.json', 'auto_upload.py', 'auto-sync.py']

def get_file_sha(filename):
    """获取文件的SHA"""
    url = f"https://api.github.com/repos/{REPO}/contents/{filename}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json().get('sha')
    return None

def upload_file(filename, message=None):
    """上传单个文件"""
    filepath = Path(filename)
    if not filepath.exists():
        print(f"   ❌ 文件不存在: {filename}")
        return False
    
    # 读取内容
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 获取SHA
    sha = get_file_sha(filename)
    
    # 上传
    url = f"https://api.github.com/repos/{REPO}/contents/{filename}"
    data = {
        "message": message or f"docs: 更新 {filename}",
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        "sha": sha
    }
    
    resp = requests.put(url, headers=HEADERS, json=data)
    
    if resp.status_code in [200, 201]:
        print(f"   ✅ {filename}")
        return True
    else:
        print(f"   ❌ {filename}: {resp.json().get('message', 'error')}")
        return False

def get_all_files():
    """获取所有需要同步的文件"""
    files = []
    workspace = "/root/.openclaw/workspace"
    
    for ext in ['*.md', '*.py', '*.sh', '*.js', '*.json']:
        for f in Path(workspace).glob(f"**/{ext}"):
            rel_path = str(f.relative_to(workspace))
            
            # 忽略
            skip = False
            for ignore_dir in IGNORE_DIRS:
                if ignore_dir in rel_path:
                    skip = True
                    break
            for ignore_file in IGNORE_FILES:
                if rel_path == ignore_file:
                    skip = True
                    break
            
            if not skip:
                files.append(rel_path)
    
    return files

def sync_all():
    """同步所有文件"""
    print(f"\n🚀 开始同步到 GitHub: {REPO}")
    print(f"📁 工作目录: /root/.openclaw/workspace")
    print("-" * 60)
    
    files = get_all_files()
    success = 0
    failed = 0
    
    for filename in sorted(files):
        if upload_file(filename):
            success += 1
        else:
            failed += 1
    
    print("-" * 60)
    print(f"✅ 成功: {success} 个文件")
    if failed > 0:
        print(f"❌ 失败: {failed} 个文件")
    
    return failed == 0

def main():
    if len(sys.argv) > 1:
        # 指定文件
        files = sys.argv[1:]
        print(f"\n🚀 同步指定文件到 GitHub: {REPO}")
        print("-" * 60)
        for filename in files:
            upload_file(filename)
    else:
        # 同步所有
        sync_all()

if __name__ == "__main__":
    main()
