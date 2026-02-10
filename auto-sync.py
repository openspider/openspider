#!/usr/bin/env python3
"""
OpenSpider自动同步脚本
监控workspace文件变化，自动提交并推送到GitHub
"""

import os
import sys
import time
import subprocess
import hashlib
from pathlib import Path

# 配置
WORKSPACE = "/root/.openclaw/workspace"
GITHUB_TOKEN = "${GITHUB_TOKEN}"
GITHUB_USER = "openspider"
REPO_NAME = "openspider"
BRANCH = "main"
CHECK_INTERVAL = 10  # 检查间隔(秒)

def get_file_hash(filepath):
    """获取文件hash"""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def get_tracked_files():
    """获取Git追踪的文件"""
    result = subprocess.run(
        ['git', 'ls-files'],
        cwd=WORKSPACE,
        capture_output=True,
        text=True
    )
    return set(result.stdout.strip().split('\n'))

def commit_and_push(message=None):
    """提交并推送"""
    try:
        # 添加所有变更
        subprocess.run(['git', 'add', '-A'], cwd=WORKSPACE, capture_output=True)
        
        # 检查是否有变更
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=WORKSPACE,
            capture_output=True,
            text=True
        )
        
        if not result.stdout.strip():
            return False, "无变更"
        
        # 生成提交信息
        if not message:
            message = f"docs: 更新 {time.strftime('%Y-%m-%d %H:%M:%S')}"
        
        # 提交
        subprocess.run(
            ['git', 'commit', '-m', message],
            cwd=WORKSPACE,
            capture_output=True
        )
        
        # 推送
        result = subprocess.run(
            ['git', 'push', 'origin', BRANCH],
            cwd=WORKSPACE,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return True, "推送成功"
        else:
            return False, f"推送失败: {result.stderr}"
            
    except Exception as e:
        return False, str(e)

def main():
    print(f"\n🔄 OpenSpider自动同步服务已启动")
    print(f"📁 监控目录: {WORKSPACE}")
    print(f"🎯 目标仓库: {GITHUB_USER}/{REPO_NAME}")
    print(f"⏰ 检查间隔: {CHECK_INTERVAL}秒")
    print("-" * 50)
    
    # 记录文件hash
    file_hashes = {}
    
    while True:
        try:
            # 检查所有md、py、sh文件
            current_files = {}
            for ext in ['*.md', '*.py', '*.sh', '*.js', '*.json']:
                for filepath in Path(WORKSPACE).glob(f"**/{ext}"):
                    if 'node_modules' in str(filepath) or '.git' in str(filepath):
                        continue
                    current_files[str(filepath)] = get_file_hash(filepath)
            
            # 检测变更
            changes = []
            for filepath, file_hash in current_files.items():
                rel_path = os.path.relpath(filepath, WORKSPACE)
                prev_hash = file_hashes.get(rel_path)
                if prev_hash != file_hash:
                    changes.append(rel_path)
                file_hashes[rel_path] = file_hash
            
            # 移除已删除的文件
            for rel_path in list(file_hashes.keys()):
                if rel_path not in current_files:
                    del file_hashes[rel_path]
                    changes.append(f"[删除] {rel_path}")
            
            # 有变更则提交推送
            if changes:
                print(f"\n📝 检测到 {len(changes)} 个文件变更:")
                for change in changes[:5]:  # 只显示前5个
                    print(f"   - {change}")
                if len(changes) > 5:
                    print(f"   ... 共 {len(changes)} 个")
                
                success, msg = commit_and_push()
                if success:
                    print(f"   ✅ {msg}")
                else:
                    print(f"   ⚠️ {msg}")
            
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n\n🔴 自动同步服务已停止")
            break
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    # 首次同步
    print("🚀 执行首次同步...")
    success, msg = commit_and_push("docs: 初始同步")
    if success:
        print(f"   ✅ {msg}")
    else:
        print(f"   ⚠️ {msg}")
    
    # 启动监控
    main()
