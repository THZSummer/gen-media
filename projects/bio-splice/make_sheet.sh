#!/usr/bin/env bash
# 速览图（**不用 AI**：ffmpeg + numpy，见 .agents/skills/image-tools）
#
#   bash make_sheet.sh round cat-eagle r1              # 开发速览 → work/cat-eagle/r1/sheet.jpg
#   bash make_sheet.sh period subjects/cat-eagle/period-01   # 成品速览 → 期目录/sheet.jpg
#   bash make_sheet.sh subject cat-eagle                     # 跨期总览 → 子主题/sheet.jpg
#   bash make_sheet.sh all                                  # 每期 + 每子主题的合并图，一次全出
#
# 开发速览含失败轮次，只给自己看；成品速览按 manifest.json 出，是交付物的一部分。
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS="$HERE/../../.agents/skills/image-tools/scripts"
MODE="${1:-}"; ARG="${2:-}"

case "$MODE" in
  round)
    # round <子主题> <rN>  —— 轮号是子主题内的编号
    SUB="${2:?子主题名}"; RN="${3:-r1}"
    [ -f "$HERE/work/$SUB/$RN/round.json" ] || { echo "no such round: work/$SUB/$RN" >&2; exit 2; }
    python3 "$TOOLS/contact_sheet.py" --round "$HERE/work/$SUB/$RN/round.json" \
        -o "$HERE/work/$SUB/$RN/sheet.jpg" --cols 3
    ;;
  period)
    [ -f "$HERE/$ARG/manifest.json" ] || { echo "no manifest: $ARG" >&2; exit 2; }
    python3 - "$HERE" "$ARG" "$TOOLS" <<'PY'
import json, os, sys
here, rel, tools = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, tools)
import contact_sheet as cs
period = os.path.join(here, rel)
man = json.load(open(os.path.join(period, "manifest.json"), encoding="utf-8"))
entries = man["entries"]
finals = [e for e in entries if e["role"] == "final"]
others = [e for e in entries if e["role"] != "final"]
order = finals + others
paths = [os.path.join(period, e.get("path", e["final"])) for e in order]
labels = [os.path.splitext(e["final"])[0] + ("（对照）" if e["role"] != "final" else "")
          for e in order]
title = f"{man.get('period','')} · {len(finals)} 成品"
cols = min(3, len(paths))
cs.build_sheet(paths, os.path.join(period, "sheet.jpg"), cols=cols, cell=512,
               labels=labels, title=title)
print(json.dumps({"sheet": os.path.join(rel, "sheet.jpg"), "tiles": len(paths)},
                 ensure_ascii=False))
PY
    ;;
  subject)
    # subject <子主题> —— 跨期总览图：每期一行，把该期全部成品拼到一起
    SUB="${2:?子主题名}"
    python3 - "$HERE" "$SUB" "$TOOLS" <<'PY'
import json, os, sys
here, sub, tools = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, tools)
import contact_sheet as cs
sd = os.path.join(here, "subjects", sub)
periods = sorted(d for d in os.listdir(sd)
                 if d.startswith("period-") and os.path.isdir(os.path.join(sd, d)))
if not periods:
    raise SystemExit(f"no periods under {sd}")
rows = []
for p in periods:
    man = json.load(open(os.path.join(sd, p, "manifest.json"), encoding="utf-8"))
    rows.append([e for e in man["entries"] if e["role"] == "final"])
n = max(len(r) for r in rows)
paths, labels = [], []
for p, row in zip(periods, rows):
    tag = f"P{int(p.split('-')[1]):02d}"
    for i in range(n):                      # 补齐成矩形，短的那期留空格
        if i < len(row):
            e = row[i]
            paths.append(os.path.join(sd, p, e.get("path", e["final"])))
            labels.append(f"{tag} · {os.path.splitext(e['final'])[0]}")
        else:
            paths.append("-")
            labels.append("")
total = sum(len(r) for r in rows)
man = cs.build_sheet(paths, os.path.join(sd, "sheet.jpg"), cols=n, cell=448,
                     labels=labels, title=f"{sub} · {len(periods)} 期 / {total} 成品")

# 子主题合图是"5 期 × N 件"的长条（≈1568×2796），直接嵌进文档会很长；
# 所以同时出一张缩略图（整数倍箱式缩采样 + JPEG），供 SUMMARY.md 等处内嵌，
# 点击缩略图进原图。成品本身不受影响。
thumb = os.path.join(sd, "sheet-thumb.jpg")
import ffkit
ffkit.encode(thumb, ffkit.box_downscale(ffkit.decode(man["out"])[:, :, :3], 700), quality=4)

print(json.dumps({"out": man["out"], "periods": len(periods), "finals": total,
                  "cols": n, "rows": len(periods), "sheet": man["sheet"],
                  "thumb": os.path.relpath(thumb, here), "thumb_bytes": os.path.getsize(thumb),
                  "bytes": man["bytes"]}, ensure_ascii=False))
PY
    ;;
  all)
    # all —— 一次生成**每期**与**每子主题**的合并图（交付物约定见 PLAN.md §二）
    fail=0
    for sd in "$HERE"/subjects/*/; do
      sub="$(basename "$sd")"
      [ -d "$sd" ] || continue
      for pd in "$sd"period-*/; do
        [ -d "$pd" ] || continue
        rel="${pd#$HERE/}"; rel="${rel%/}"
        bash "$0" period "$rel" >/dev/null || { echo "  FAIL period $rel" >&2; fail=1; }
        echo "  period  $rel"
      done
      if ls "$sd"period-*/manifest.json >/dev/null 2>&1; then
        bash "$0" subject "$sub" >/dev/null || { echo "  FAIL subject $sub" >&2; fail=1; }
        echo "  subject $sub"
      else
        echo "  subject $sub （尚无成品，跳过）"
      fi
    done
    [ "$fail" = 0 ] || exit 1
    ;;
  *) echo "usage: bash make_sheet.sh round <子主题> <rN> | period <subjects/.../period-NN> | subject <子主题> | all" >&2; exit 2 ;;
esac
