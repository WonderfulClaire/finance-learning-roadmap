#!/usr/bin/env bash
# 一键发布到 GitHub：创建公开仓库并推送。
# 用法: bash publish.sh <github_pat>
set -e

TOKEN="${1:-$GITHUB_TOKEN}"
REPO="finance-learning-roadmap"
USER="WonderfulClaire"

if [ -z "$TOKEN" ]; then
  echo "用法: bash publish.sh <github_pat>"
  echo "或:   GITHUB_TOKEN=xxxx bash publish.sh"
  exit 1
fi

echo "==> 1/3 创建仓库（已存在则忽略）"
HTTP=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$REPO\",\"description\":\"📈 个人理财系统学习路线：从复利到资产配置，零基础也能看懂的中文开源教程\",\"homepage\":\"\",\"public\":true}" || true)
echo "    创建接口返回: $HTTP (201=新建, 422=已存在)"

echo "==> 2/3 本地提交"
git init -q 2>/dev/null || true
git add -A
git commit -q -m "init: 个人理财系统学习路线 v1.0" 2>/dev/null || echo "    (无新提交，跳过)"
git branch -M main 2>/dev/null || true

echo "==> 3/3 推送到 main"
git remote remove origin 2>/dev/null || true
git remote add origin "https://$USER:$TOKEN@github.com/$USER/$REPO.git"
git push -u origin main

echo ""
echo "✅ 已推送：https://github.com/$USER/$REPO"
echo "提示：token 仅用于此次推送，可在 GitHub 设置里随时撤销。"
