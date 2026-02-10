#!/usr/bin/env python3
"""Simple push script - GitHub Token从环境变量读取"""
import subprocess
import os

WORKSPACE = "/root/.openclaw/workspace"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

if not TOKEN:
    print("请设置环境变量: export GITHUB_TOKEN=your_token")
    exit(1)

print("🚀 Pushing to GitHub...")

# Add and commit
subprocess.run(["git", "add", "-A"], cwd=WORKSPACE, capture_output=True)
subprocess.run(["git", "commit", "-m", "docs: 更新"], cwd=WORKSPACE, capture_output=True)

# Push
result = subprocess.run(
    ["git", "push", "origin", "main", "--force"],
    cwd=WORKSPACE,
    capture_output=True,
    text=True,
    timeout=60
)

print(result.stdout)
if result.returncode != 0:
    print(result.stderr[:500])
