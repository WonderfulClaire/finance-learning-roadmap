# 发布到 GitHub（PUBLISH）

> 本项目内容已完整构建并通过自测。由于当前环境的 GitHub 集成没有「建仓」权限，
> 仓库需要你（仓库所有者）用 Personal Access Token 一键推上去。
> 全过程约 1 分钟，仓库完全属于你，内容随便改。

## 方式 A：一键脚本（推荐，Windows / Mac / Linux 通用）

1. 在 GitHub 上生成一个有 `repo` 权限的 Token：
   - 打开 https://github.com/settings/tokens （或用 fine-grained token，勾 repo 权限）
   - 生成后**复制**那一长串（只显示一次）
2. 在本仓库目录下运行（把 `xxxx` 换成你的 token）：

   ```bash
   bash publish.sh xxxx
   ```

   脚本会：创建公开仓库 `finance-learning-roadmap` → 提交 → 推送到 `main`。
   成功后打印仓库地址。

> 安全提示：token 只用于这一次推送，用完可在 GitHub 撤销。脚本不会把 token 写进任何文件。
> 若担心，用方式 B 手动推。

## 方式 B：手动推送

```bash
# 1. 在 GitHub 网页手动 New repository，名字填 finance-learning-roadmap，公开，不要勾 README
# 2. 本地执行：
git init
git add -A
git commit -m "init: 个人理财系统学习路线 v1.0"
git branch -M main
git remote add origin https://github.com/WonderfulClaire/finance-learning-roadmap.git
git push -u origin main
# 推送时用 GitHub 账号 + 刚才的 token 作为密码（或 GitHub Desktop 登录推送）
```

## 验证

打开 https://github.com/WonderfulClaire/finance-learning-roadmap ，应能看到 README 渲染的路线图与课程目录。

---

完成后欢迎在仓库开 Issue / PR 一起完善，也欢迎点 Star ⭐ 让更多人少踩坑。
