#!/usr/bin/env bash
# 第四阶段（半真半骨瓷）微距脚本
#
# 皮肤：R25 的 2048² 方画布底板 —— 方画布让脸占的像素翻倍，才能看见釉面的缩釉点。
#       这是"还不够细致"的正面回答：细节不是靠更高的整图分辨率，而是靠
#       (a) 把瓷面缺陷具名写进 prompt，(b) 让裁切目标占更多像素。
# 纱罗：R26 的肖像底板 —— 展示"半纱半骨瓷"：纱的透光层次 + 瓷一般挺括的边缘与经纬。
#
# 用法：bash make_macro_gauze.sh
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKIN="$HERE/out/r25/bc-r25-skin-square_00001_.png"   # 2048x2048
GAUZE="$HERE/out/r26/bc-r26-portrait_00001_.png"     # 1280x1712
OUT="$HERE/out/macro-gauze"

for f in "$SKIN" "$GAUZE"; do
  [ -f "$f" ] || { echo "missing source plate: $f" >&2; exit 1; }
done
mkdir -p "$OUT"

# 1) 皮肤微距：釉光 + 真人血色 + 釉面缩釉点/橘皮起伏 + 睫毛与虹膜
ffmpeg -loglevel error -y -i "$SKIN" \
  -vf "crop=780:950:640:470,scale=936:1140:flags=lanczos" "$OUT/skin-macro.png"

# 2) 纱罗微距：数层素纱的透光层次、挺括的纱边与经纬
ffmpeg -loglevel error -y -i "$GAUZE" \
  -vf "crop=430:680:40:620,scale=860:1360:flags=lanczos" "$OUT/gauze-macro.png"

echo "wrote:"
ls -la "$OUT"
