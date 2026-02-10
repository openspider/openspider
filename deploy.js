#!/usr/bin/env node

const GitHub = require('github');
const exec = require('child_process').execSync;
const fs = require('fs');
const path = require('path');

// 获取token和环境变量
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || '';
const GITHUB_USER = process.env.GITHUB_USER || '';

if (!GITHUB_TOKEN || !GITHUB_USER) {
    console.log('请设置环境变量:');
    console.log('export GITHUB_USER="你的GitHub用户名"');
    console.log('export GITHUB_TOKEN="你的GitHub Personal Access Token"');
    console.log('\n创建Token: https://github.com/settings/tokens');
    console.log('需要的权限: repo, admin:org');
    process.exit(1);
}

const github = new GitHub({
    auth: GITHUB_TOKEN,
    userAgent: 'OpenSpider-Deploy/1.0'
});

async function deploy() {
    const repoName = 'openspider';
    const repoDesc = 'OpenSpider Plan - NRT组织建设方案';
    const workspace = '/root/.openclaw/workspace';

    try {
        // 1. 创建仓库
        console.log('1. 创建GitHub仓库...');
        try {
            await github.repos.createForAuthenticatedUser({
                name: repoName,
                description: repoDesc,
                private: false,
                auto_init: false
            });
            console.log(`   ✓ 仓库 ${GITHUB_USER}/${repoName} 创建成功`);
        } catch (e) {
            if (e.status === 422) {
                console.log(`   ⚠ 仓库 ${GITHUB_USER}/${repoName} 已存在，跳过创建`);
            } else {
                throw e;
            }
        }

        // 2. 初始化git（如果需要）
        console.log('2. 检查git状态...');
        try {
            exec('git remote get-url origin', { cwd: workspace });
            console.log('   ✓ 远程仓库已配置');
        } catch (e) {
            console.log('   配置远程仓库...');
            exec(`git remote add origin https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${repoName}.git`, {
                cwd: workspace
            });
            console.log('   ✓ 远程仓库已添加');
        }

        // 3. 提交代码
        console.log('3. 提交代码...');
        try {
            exec('git add .', { cwd: workspace });
            const files = exec('git diff --cached --name-only', { cwd: workspace }).toString();
            
            if (files.trim()) {
                exec('git commit -m "feat: OpenSpider计划初始提交\\n\\n- NRT组织建设方案\\n- 四向任务池策划\\n- 曹操任务池系统"', {
                    cwd: workspace,
                    env: { ...process.env, GIT_AUTHOR_NAME: 'SeekerOfKai', GIT_AUTHOR_EMAIL: 'seeker@kai.com' }
                });
                console.log(`   ✓ 已提交 ${files.split('\n').length} 个文件`);
            } else {
                console.log('   ⚠ 没有新文件需要提交');
            }
        } catch (e) {
            console.log(`   ⚠ 提交失败: ${e.message}`);
        }

        // 4. 推送代码
        console.log('4. 推送代码到GitHub...');
        try {
            exec('git branch -M main', { cwd: workspace });
            exec('git push -u origin main --force', { cwd: workspace, encoding: 'utf8' });
            console.log('   ✓ 推送成功!');
        } catch (e) {
            console.log(`   ⚠ 推送失败: ${e.message}`);
        }

        console.log('\n✅ 部署完成!');
        console.log(`   仓库地址: https://github.com/${GITHUB_USER}/${repoName}`);

    } catch (error) {
        console.error('部署失败:', error.message);
        process.exit(1);
    }
}

deploy();
