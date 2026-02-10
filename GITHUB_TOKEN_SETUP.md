# GitHub Token 创建步骤

GitHub已禁用密码认证，必须使用Personal Access Token (PAT)。

## 步骤1: 在GitHub网页创建Token

1. 打开浏览器，访问:
   https://github.com/settings/tokens

2. 点击 "Generate new token (classic)"

3. 填写信息:
   - Note: "OpenSpider Deploy"
   - Expiration: No expiration
   - 勾选权限:
     ✅ repo - Full control of private repositories
     ✅ admin:org - Full control of orgs and teams

4. 点击 "Generate token"

5. **复制生成的token** (格式: ghp_xxxxxxxxxxxx)

## 步骤2: 告诉我token

回复格式:
```
token: 你的token
```

例如:
```
token: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 步骤3: 我立即完成部署

然后我会自动执行:
```bash
export GITHUB_TOKEN="你的token"
bash quick-deploy.sh
```

## 为什么需要Token?

GitHub API需要token认证，不支持密码。
这是GitHub的安全策略。

## 创建Token后

告诉我token，30秒内完成部署!
