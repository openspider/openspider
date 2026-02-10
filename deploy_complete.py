#!/usr/bin/env python3
"""
OpenSpider一键部署脚本
支持交互式输入GitHub认证信息
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error

REPO_NAME = "openspider"
REPO_DESC = "OpenSpider Plan - NRT组织建设方案"
WORKSPACE = "/root/.openclaw/workspace"

def run_cmd(cmd, check=True):
    """运行命令"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"命令失败: {cmd}")
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    print("\n🚀 OpenSpider一键部署脚本")
    print("=" * 50)
    
    # 交互式输入
    print("\n📋 请提供GitHub认证信息:")
    print("-" * 50)
    
    GITHUB_USER = input("GitHub用户名: ").strip()
    GITHUB_TOKEN = input("Personal Access Token: ").strip()
    
    if not GITHUB_USER or not GITHUB_TOKEN:
        print("\n❌ 错误: 用户名和Token都不能为空")
        sys.exit(1)
    
    print("\n⏳ 部署中，请稍候...")
    
    # 配置Git
    os.chdir(WORKSPACE)
    run_cmd(f'git config user.email "seeker@kai.com"')
    run_cmd(f'git config user.name "SeekerOfKai"')
    
    # 设置远程URL
    remote_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"
    
    # 检查remote
    result = run_cmd("git remote get-url origin", check=False)
    if result.returncode == 0:
        run_cmd(f'git remote set-url origin "{remote_url}"')
    else:
        run_cmd(f'git remote add origin "{remote_url}"')
    
    # 创建main分支
    run_cmd("git branch -M main", check=False)
    
    # 提交代码
    run_cmd("git add -A", check=False)
    result = run_cmd("git status --porcelain", check=False)
    if result.stdout.strip():
        run_cmd('git commit -m "feat: OpenSpider计划初始提交"')
    
    # 推送
    print("\n🚀 推送到GitHub...")
    result = run_cmd("git push -u origin main --force", check=False)
    
    if result.returncode == 0:
        print("\n" + "=" * 50)
        print("✅ 部署完成!")
        print(f"\n🌐 仓库地址: https://github.com/{GITHUB_USER}/{REPO_NAME}")
    else:
        print(f"\n❌ 部署失败: {result.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    main()
