#!/usr/bin/env node
/**
 * OpenSpider一键部署脚本
 * 自动创建GitHub仓库并推送代码
 * 
 * 使用方法:
 * 1. 创建GitHub Personal Access Token:
 *    https://github.com/settings/tokens
 *    权限: repo, admin:org
 * 
 * 2. 设置环境变量并运行:
 *    export GITHUB_USER="你的用户名"
 *    export GITHUB_TOKEN="你的token"
 *    node deploy.js
 */

const https = require('https');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 配置
const REPO_NAME = 'openspider';
const REPO_DESC = 'OpenSpider Plan - NRT组织建设方案';
const WORKSPACE = '/root/.openclaw/workspace';

// 获取环境变量
const GITHUB_USER = process.env.GITHUB_USER || '';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || '';

if (!GITHUB_USER || !GITHUB_TOKEN) {
    console.log('\n❌ 错误: 请设置环境变量');
    console.log('\n📝 设置方法:');
    console.log('   export GITHUB_USER="你的GitHub用户名"');
    console.log('   export GITHUB_TOKEN="你的GitHub Personal Access Token"');
    console.log('\n🔗 创建Token: https://github.com/settings/tokens');
    console.log('   需要的权限: repo, admin:org\n');
    process.exit(1);
}

// GitHub API请求封装
function githubRequest(method, path, data = null) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'api.github.com',
            port: 443,
            path: path,
            method: method,
            headers: {
                'Authorization': `token ${GITHUB_TOKEN}`,
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'OpenSpider-Deploy/1.0'
            }
        };

        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(body);
                    if (res.statusCode >= 200 && res.statusCode < 300) {
                        resolve(json);
                    } else {
                        reject(new Error(json.message || 'API请求失败'));
                    }
                } catch (e) {
                    reject(e);
                }
            });
        });

        req.on('error', reject);
        if (data) {
            req.write(JSON.stringify(data));
        }
        req.end();
    });
}

// 获取所有文件
function getAllFiles(dir, baseDir = dir) {
    const files = [];
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        const relativePath = path.relative(baseDir, fullPath);
        
        if (entry.isDirectory()) {
            if (!relativePath.includes('.git')) {
                files.push(...getAllFiles(fullPath, baseDir));
            }
        } else if (entry.isFile()) {
            if (!relativePath.includes('.git') && 
                !relativePath.includes('deploy') &&
                !relativePath.includes('node_modules')) {
                files.push({
                    path: relativePath,
                    content: fs.readFileSync(fullPath, 'utf8'),
                    sha: null
                });
            }
        }
    }
    return files;
}

async function deploy() {
    console.log('\n🚀 OpenSpider部署脚本');
    console.log('='.repeat(40));

    try {
        // 1. 创建仓库
        console.log('\n1️⃣ 创建GitHub仓库...');
        try {
            await githubRequest('POST', '/user/repos', {
                name: REPO_NAME,
                description: REPO_DESC,
                private: false,
                auto_init: false
            });
            console.log(`   ✅ 仓库 ${GITHUB_USER}/${REPO_NAME} 创建成功`);
        } catch (e) {
            if (e.message.includes('already exists')) {
                console.log(`   ⚠️ 仓库已存在，跳过创建`);
            } else {
                throw e;
            }
        }

        // 2. 配置git
        console.log('\n2️⃣ 配置Git...');
        execSync('git config user.email "seeker@kai.com"', { cwd: WORKSPACE });
        execSync('git config user.name "SeekerOfKai"', { cwd: WORKSPACE });
        
        // 添加远程仓库
        const remoteUrl = `https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git`;
        try {
            execSync('git remote get-url origin', { cwd: WORKSPACE });
            execSync(`git remote set-url origin ${remoteUrl}`, { cwd: WORKSPACE });
        } catch (e) {
            execSync(`git remote add origin ${remoteUrl}`, { cwd: WORKSPACE });
        }
        console.log('   ✅ Git配置完成');

        // 3. 获取文件SHA
        console.log('\n3️⃣ 获取文件列表...');
        let existingFiles = {};
        try {
            const { tree } = await githubRequest('GET', `/repos/${GITHUB_USER}/${REPO_NAME}/git/trees/main?recursive=1`);
            for (const item of tree.tree) {
                if (item.type === 'blob') {
                    existingFiles[item.path] = item.sha;
                }
            }
            console.log(`   ✅ 已有 ${Object.keys(existingFiles).length} 个文件`);
        } catch (e) {
            console.log('   ⚠️ 仓库为空，这是首次推送');
        }

        // 4. 获取要推送的文件
        console.log('\n4️⃣ 准备推送文件...');
        const files = getAllFiles(WORKSPACE);
        console.log(`   📁 待推送: ${files.length} 个文件`);

        // 5. 上传文件
        console.log('\n5️⃣ 上传文件中...');
        let uploaded = 0;
        for (const file of files) {
            // 检查文件是否需要更新
            const content = Buffer.from(file.content).toString('base64');
            const sha = crypto.createHash('sha1')
                .update(`blob ${file.content.length}\0${file.content}`)
                .digest('hex');
            
            // 如果文件已存在且SHA相同，跳过
            if (existingFiles[file.path] === sha) {
                continue;
            }

            try {
                await githubRequest('PUT', `/repos/${GITHUB_USER}/${REPO_NAME}/contents/${file.path}`, {
                    message: `feat: add ${file.path}`,
                    content: content,
                    sha: existingFiles[file.path] || undefined
                });
                uploaded++;
                process.stdout.write(`   📤 ${file.path}\r`);
            } catch (e) {
                console.error(`   ❌ 上传失败 ${file.path}: ${e.message}`);
            }
        }
        console.log(`\n   ✅ 完成: ${uploaded} 个文件上传`);

        // 6. 创建提交
        console.log('\n6️⃣ 创建提交...');
        const filePaths = files.map(f => f.path);
        const treeData = filePaths.map(p => ({
            path: p,
            mode: '100644',
            type: 'blob',
            sha: crypto.createHash('sha1')
                .update(`blob ${fs.readFileSync(path.join(WORKSPACE, p)).length}\0${fs.readFileSync(path.join(WORKSPACE, p))}`)
                .digest('hex')
        }));

        // 获取当前commit
        let parentSha;
        try {
            const ref = await githubRequest('GET', `/repos/${GITHUB_USER}/${REPO_NAME}/git/ref/heads/main`);
            const commit = await githubRequest('GET', `/repos/${GITHUB_USER}/${REPO_NAME}/git/commits/${ref.object.sha}`);
            parentSha = commit.sha;
        } catch (e) {
            parentSha = null;
        }

        // 创建tree
        const treeSha = (await githubRequest('POST', `/repos/${GITHUB_USER}/${REPO_NAME}/git/trees`, {
            tree: filePaths.map(p => ({
                path: p,
                mode: '100644',
                type: 'blob',
                content: fs.readFileSync(path.join(WORKSPACE, p), 'utf8')
            })),
            base_tree: parentSha
        })).sha;

        // 创建commit
        const commitSha = (await githubRequest('POST', `/repos/${GITHUB_USER}/${REPO_NAME}/git/commits`, {
            message: `feat: OpenSpider计划初始提交

- NRT组织建设完整方案
- 四向任务池策划(东/西/南/北)
- 曹操任务池系统
- 任务跟踪与汇报机制

Generated by SeekerOfKai`,
            tree: treeSha,
            parents: parentSha ? [parentSha] : []
        })).sha;

        // 更新ref
        await githubRequest('PATCH', `/repos/${GITHUB_USER}/${REPO_NAME}/git/refs/heads/main`, {
            sha: commitSha,
            force: true
        });

        console.log('   ✅ 提交创建成功');

        // 7. 完成
        console.log('\n' + '='.repeat(40));
        console.log('✅ 部署完成!');
        console.log(`\n🌐 仓库地址: https://github.com/${GITHUB_USER}/${REPO_NAME}`);
        console.log('📋 包含文件:');
        files.forEach(f => console.log(`   - ${f.path}`));

    } catch (error) {
        console.error('\n❌ 部署失败:', error.message);
        process.exit(1);
    }
}

deploy();
