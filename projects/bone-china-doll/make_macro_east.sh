#!/usr/bin/env bash
# 东方工艺微距生成脚本（裁切法）
#
# 与 make_macro.sh 同一套方法论：R10/R11/R13 三次证明 Qwen-Image 2512 在存在长材质
# 描述时会无视一切"裁切前置 / ONLY / 无脸"措辞，所以真微距**不向 prompt 索取**，
# 而是从高分辨率成品裁切。R14 测出 3.43 MP 是细节密度性价比最高的水位，故 R20 的
# plate-portrait 用 1600x2144。
#
# 用法：bash make_macro_east.sh
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
P="$HERE/out/r20/bc-r20-plate-portrait_00001_.png"   # 1600x2144, 3.43MP
F="$HERE/out/r20/bc-r20-plate-figure_00001_.png"    # 1200x2560, 3.07MP
OUT="$HERE/out/macro-east"

for f in "$P" "$F"; do
  [ -f "$f" ] || { echo "missing source plate: $f" >&2; exit 1; }
done
mkdir -p "$OUT"

# 1) 金镶玉步摇 + 冠饰：金 filigree 镂空、爪镶巴洛克珍珠、珠→玉→水滴珠垂坠
ffmpeg -loglevel error -y -i "$P" \
  -vf "crop=340:380:440:110,scale=1020:1140:flags=lanczos" "$OUT/macro-hairpin.png"

# 2) 璎珞 + 交领金线绣 + 云肩：玉珠半透蜡光、珍珠珠光、金 filigree 隔珠、双道细珠滚边
ffmpeg -loglevel error -y -i "$P" \
  -vf "crop=700:430:460:970,scale=1400:860:flags=lanczos" "$OUT/macro-necklace.png"

# 3) 金镶玉胸带：盘金绣线卷 + 玉璧（玉环）半透蜡光
ffmpeg -loglevel error -y -i "$F" \
  -vf "crop=280:220:490:620,scale=1120:880:flags=lanczos" "$OUT/macro-chest.png"

# 4) 青釉瓷鞋 + 金 filigree + 珍珠 + 红木座木纹
ffmpeg -loglevel error -y -i "$F" \
  -vf "crop=280:300:480:2150,scale=980:1050:flags=lanczos" "$OUT/macro-slipper.png"

# 5) 腕部球关节：关节缝 + 内部金属张力销 + 纱罗经纬
ffmpeg -loglevel error -y -i "$F" \
  -vf "crop=210:330:335:1120,scale=840:1320:flags=lanczos" "$OUT/macro-wrist.png"

echo "wrote:"
ls -la "$OUT"
