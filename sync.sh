#!/bin/bash
# OpenSpider快速同步命令
# 用法: ./sync.sh [文件列表]
cd /root/.openclaw/workspace
if [ -z "$1" ]; then
    python3 auto_upload.py
else
    shift
    python3 auto_upload.py "$@"
fi

