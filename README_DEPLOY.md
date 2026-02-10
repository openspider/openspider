# OpenSpider GitHub部署

## 一键部署（选择一种方式）

### 方式1: 交互式部署（推荐）
```bash
cd /root/.openclaw/workspace
python3 deploy_complete.py
# 按提示输入GitHub用户名和Token
```

### 方式2: 环境变量部署
```bash
export GITHUB_USER="你的用户名"
export GITHUB_TOKEN="你的Token"
bash quick-deploy.sh
```

### 方式3: 手动部署
```bash
cd /root/.openclaw/workspace

# 1. 创建仓库 (网页操作)
# https://github.com/new

# 2. 配置并推送
git remote set-url origin "https://[TOKEN]@github.com/[USER]/openspider.git"
git push -u origin main --force
```

## 创建Token

1. 访问: https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. Note: "OpenSpider Deploy"
4. 勾选: repo, admin:org
5. 点击 "Generate token"

## 包含文件

- deploy_complete.py - 交互式部署脚本
- quick-deploy.sh - 快速部署脚本
- deploy.py - 高级部署脚本
- OpenSpider计划.md - 整体架构
- OpenSpider_*.md - 各向任务池策划

## 部署后

访问: https://github.com/[用户名]/openspider
