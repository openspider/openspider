#!/usr/bin/env python3
"""Simple push script"""

import subprocess
import sys

WORKSPACE = "/root/.openclaw/workspace"
REPO = "openspider/openspider"
TOKEN = "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"

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
    print(result.stderr)
    sys.exit(1)

print("✅ Done!")
