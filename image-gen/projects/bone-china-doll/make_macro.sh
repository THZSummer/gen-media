#!/usr/bin/env bash
# 真微距生成脚本（裁切法）
#
# 背景：R10 / R11 / R13 三次证明 Qwen-Image 2512 在存在长材质描述时会无视一切
# "裁切前置 / ONLY / 无脸" 措辞；R11 当年只有靠删掉材质词汇才拿到微距，代价是
# 整体质量崩掉。R14 又证明提高分辨率只买到更大的画布、买不到细节密度。
#
# 结论：真微距不应该向 prompt 索取，而应该 **从高分辨率成品裁切**。
# 本脚本自动化这件事：源图 = R14 的 3.43 MP 成品（bytes/px 1.3345，全项目最高），
# 用 lanczos 重采样做大，得到既有微距构图、又保留完整人脸与眼睛的成品。
#
# 用法：bash make_macro.sh
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/out/r14/bc-r14-res-125_00001_.png"   # 1600x2144, 3.43MP
OUT="$HERE/out/macro"

[ -f "$SRC" ] || { echo "missing source render: $SRC" >&2; exit 1; }
mkdir -p "$OUT"

# 1) 冠冕微距：银 filigree + 钻石 + 蓝宝石 + 发顶；下缘带到眼睛，避免"无眼瓷脸"
ffmpeg -loglevel error -y -i "$SRC" \
  -vf "crop=560:640:520:20,scale=1120:1280:flags=lanczos" \
  "$OUT/macro-tiara.png"

# 2) 腕部球关节微距：关节球 + 内部金属张力环 + 釉面高光 + 金线锦缎/蕾丝边缘
ffmpeg -loglevel error -y -i "$SRC" \
  -vf "crop=320:420:1290:1730,scale=960:1260:flags=lanczos" \
  "$OUT/macro-wrist.png"

echo "wrote:"
ls -la "$OUT"
