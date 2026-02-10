#!/usr/bin/env node
/**
 * OpenSpider自动部署脚本
 * 支持交互式输入token
 */

const { Octokit } = require("@octokit/rest");
const { execSync } = require('child_process');
const readline = require('readline');

const REPO_NAME = 'openspider';
const WORKSPACE = '/root/.openclaw/workspace';

async function askQuestion(question) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    return new Promise((resolve) => {
        rl.question(question, (answer) => {
            rl.close();
            resolve(answer);
        });
    });
}

async function deploy() {
    console.log('\n🚀 OpenSpider自动部署');
    console.log('='.repeat(50));

    // 获取token
    const GITHUB_TOKEN = '5loveopenspider';
    const GITHUB_USER = 'openspider';
    const GITHUB_EMAIL = 'luwen678@163.com';

    // 验证token是否有效
    console.log('\n🔐 验证GitHub认证...');
    const octokit = new Octokit({
        auth: GITHUB_TOKEN
    });

    try {
        const { data: user } = await octokit.users.getAuthenticated();
        console.log(`   ✅ 认证成功: ${user.login} (${user.email})`);
    } catch (e) {
        console.log(`   ❌ 认证失败: ${e.message}`);
        console.log('\n💡 GitHub已禁用密码认证，需要使用Personal Access Token');
        console.log('请访问: https://github.com/settings/tokens 创建token');
        console.log('需要的权限: repo, admin:org');
        process.exit(1);
    }

    // 创建仓库
    console.log('\n📦 创建GitHub仓库...');
    try {
        const { data: repo } = await octokit.repos.createForAuthenticatedUser({
            name: REPO_NAME,
            description: 'OpenSpider Plan - NRT组织建设方案',
            private: false,
            auto_init: false
        });
        console.log(`   ✅ 仓库创建成功: ${repo.full_name}`);
    } catch (e) {
        if (e.status === 422) {
            console.log('   ⚠️ 仓库已存在，跳过创建');
        } else {
            console.log(`   ❌ 创建失败: ${e.message}`);
        }
    }

    // 配置Git
    console.log('\n⚙️ 配置Git...');
    try {
        execSync(`git config user.email "${GITHUB_EMAIL}"`, { cwd: WORKSPACE });
        execSync(`git config user.name "${GITHUB_USER}"`, { cwd: WORKSPACE });
        console.log('   ✅ Git配置完成');
    } catch (e) {
        console.log(`   ⚠️ Git配置警告: ${e.message}`);
    }

    // 设置remote
    const remoteUrl = `https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git`;
    try {
        execSync('git remote get-url origin', { cwd: WORKSPACE });
        execSync(`git remote set-url origin "${remoteUrl}"`, { cwd: WORKSPACE });
    } catch (e) {
        execSync(`git remote add origin "${remoteUrl}"`, { cwd: WORKSPACE });
    }
    console.log('   ✅ 远程仓库配置完成');

    // 提交代码
    console.log('\n📝 提交代码...');
    execSync('git add -A', { cwd: WORKSPACE });
    try {
        execSync('git commit -m "feat: OpenSpider计划初始提交\\n\\n- NRT组织建设完整方案\\n- 四向任务池策划\\n- 曹操任务池系统"', {
            cwd: WORKSPACE,
            env: { ...process.env, GIT_AUTHOR_NAME: GITHUB_USER, GIT_AUTHOR_EMAIL: GITHUB_EMAIL }
        });
        console.log('   ✅ 代码已提交');
    } catch (e) {
        console.log('   ⚠️ 没有新文件或已提交');
    }

    // 推送代码
    console.log('\n🚀 推送代码到GitHub...');
    try {
        execSync('git branch -M main', { cwd: WORKSPACE });
        execSync('git push -u origin main --force', { cwd: WORKSPACE, encoding: 'utf8' });
        console.log('   ✅ 推送成功!');
    } catch (e) {
        console.log(`   ❌ 推送失败: ${e.message}`);
        process.exit(1);
    }

    // 完成
    console.log('\n' + '='.repeat(50));
    console.log('✅ 部署完成!');
    console.log(`\n🌐 仓库地址: https://github.com/${GITHUB_USER}/${REPO_NAME}`);
    console.log('\n📦 包含文件:');
    const files = execSync('git ls-tree --name-only -r HEAD', { cwd: WORKSPACE }).toString().split('\n').filter(f => f);
    files.forEach(f => console.log(`   📄 ${f}`));
    console.log();
}

deploy().catch(e => {
    console.error('部署失败:', e.message);
    process.exit(1);
});
