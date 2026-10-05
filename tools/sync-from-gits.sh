#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# 从 gits 工作区同步内容到本仓库（工作机专用）
#
# 约定：gits 工作区（/home/usb/wks/gits）是内容源头，作者日常在那里出图 / 写文档；
#       本仓库（gen-media）是发布镜像。gits 里这两个目录已被 .gitignore 排除，
#       不再进 Gitee 仓库，只保留在本地磁盘上。
#
# 仓库根的 README.md / .gitignore / tools/ 是本仓库自有文件，不参与同步。
#
# 用法：
#   tools/sync-from-gits.sh        # 同步 + 提交 + 推送
#   tools/sync-from-gits.sh -n     # 只预览（dry-run，不提交）
#
# 环境变量：
#   GITS   gits 工作区路径（默认 /home/usb/wks/gits）
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

DEST=$(cd "$(dirname "$0")/.." && pwd)
GITS=${GITS:-/home/usb/wks/gits}
DRY=0
[ "${1:-}" = "-n" ] && DRY=1

cd "$DEST"
REV=$(git -C "$GITS" rev-parse --short HEAD)
BRANCH=$(git rev-parse --abbrev-ref HEAD)

echo "== 源头 gits@$REV → $DEST ($BRANCH) =="

# 1) 导出 gits 里已跟踪的内容（自动排除 work/ 等被忽略的中间产物）
tmp="${TMPDIR:-/tmp}/gen-media-export.$$"
rm -rf "$tmp"; mkdir -p "$tmp"
trap 'rm -rf "$tmp"' EXIT
git -C "$GITS" archive HEAD Book/image-gen Book/video-gen | tar -x -C "$tmp"

# 2) 同步到两个子目录（--delete 与源头严格对齐）
for d in image-gen video-gen; do
  rsync -a --delete "$tmp/Book/$d/" "$DEST/$d/"
done

# 3) 提交
git add -A
if git diff --cached --quiet; then
  echo "无变化，无需提交"
  exit 0
fi
echo "== 变更 =="
git status --short | head -40
echo "（共 $(git status --short | wc -l) 项）"

if [ "$DRY" = 1 ]; then
  echo "[dry-run] 未提交。要撤销: git reset --hard"
  exit 0
fi

git commit -q -m "sync: 从 gits@$REV 同步图片生成与视频生成内容"
git push origin "$BRANCH"
echo "== 已推送 =="
git log --oneline -1
