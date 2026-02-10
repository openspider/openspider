#!/bin/bash
# OpenSpider一键部署脚本
# 运行此脚本前请确保已创建GitHub Personal Access Token

set -e

REPO_NAME="openspider"
WORKSPACE="/root/.openclaw/workspace"

echo "🚀 OpenSpider部署脚本"
echo "===================="

# 检查是否已有token
if [ -z "$GITHUB_TOKEN" ]; then
    echo ""
    echo "📋 请提供以下信息:"
    echo ""
    
    if [ -z "$GITHUB_USER" ]; then
        read -p "GitHub用户名: " GITHUB_USER
    fi
    
    echo ""
    echo "🔗 创建Personal Access Token:"
    echo "   1. 访问 https://github.com/settings/tokens"
    echo "   2. 点击 'Generate new token (classic)'"
    echo "   3. 设置名称: 'OpenSpider Deploy'"
    echo "   4. 勾选权限: repo, admin:org"
    echo "   5. 点击 'Generate token'"
    echo ""
    read -s -p "Paste Token here: " GITHUB_TOKEN
    
    echo ""
    echo ""
fi

# 检查token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 错误: 需要GitHub Token"
    exit 1
fi

if [ -z "$GITHUB_USER" ]; then
    echo "❌ 错误: 需要GitHub用户名"
    exit 1
fi

# 设置远程URL
REMOTE_URL="https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git"

cd "$WORKSPACE"

echo ""
echo "📦 配置Git仓库..."
git config user.email "seeker@kai.com" 2>/dev/null || true
git config user.name "SeekerOfKai" 2>/dev/null || true

# 检查remote是否存在
if git remote get-url origin &>/dev/null; then
    CURRENT_URL=$(git remote get-url origin)
    if [[ "$CURRENT_URL" != *"$GITHUB_TOKEN"* ]]; then
        git remote set-url origin "$REMOTE_URL"
    fi
else
    git remote add origin "$REMOTE_URL"
fi

# 创建main分支并推送
echo "🚀 推送代码到GitHub..."

# 确保使用main分支
git branch -M main 2>/dev/null || true

# 尝试推送
if git push -u origin main --force 2>&1; then
    echo ""
    echo "✅ 部署完成!"
    echo ""
    echo "🌐 仓库地址: https://github.com/${GITHUB_USER}/${REPO_NAME}"
    echo ""
    echo "📦 包含文件:"
    ls -1 *.md *.js *.sh 2>/dev/null | grep -v node_modules | head -20
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "💡 可能的原因:"
    echo "   - Token权限不足 (需要repo权限)"
    echo "   - 仓库不存在或无权访问"
    echo ""
    echo "🔧 手动部署:"
    echo "   git remote set-url origin 'https://[TOKEN]@github.com/${GITHUB_USER}/${REPO_NAME}.git'"
    echo "   git push -u origin main --force"
fi
