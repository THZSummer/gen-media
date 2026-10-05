#!/bin/bash
# 检查并放大视频音量（seedance-2.0 --generate-audio 音量过低问题）
# 用法: ./boost_audio.sh <input.mp4> [output.mp4]
set -e
IN="$1"
OUT="${2:-${IN%.mp4}_boosted.mp4}"
VOL=$(ffmpeg -i "$IN" -af volumedetect -f null - 2>&1 | grep max_volume | sed 's/.*max_volume: //' | sed 's/ dB//')
echo "$IN max_volume=${VOL}dB"
# 目标 max 约 -3dB；用 awk 计算增益
GAIN=$(awk -v v="$VOL" 'BEGIN{printf "%.1f", -3 - v}')
if [ "$GAIN" = "-0.0" ] || [ "$GAIN" = "0.0" ] || awk "BEGIN{exit !($GAIN<1)}"; then
  echo "  音量足够，跳过 ($GAIN)"
else
  echo "  增益 +${GAIN}dB -> $OUT"
  ffmpeg -y -i "$IN" -af "volume=${GAIN}dB" -c:v copy "$OUT" 2>/dev/null
fi
