#!/usr/bin/env bash
# gen-media 交付前自检（dev-guide 技能自带）
#
# 用法：.agents/skills/dev-guide/scripts/check.sh
# 退出码：0 = 全部通过；非 0 = 有检查未通过（逐项打印）。
#
# 只做机械检查；人工项（新文档是否配了英文版、新界面文案是否中英两份、
# 新图是否进 manifest.json）见 SKILL.md 的「交付前校验」。

set -uo pipefail

SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)
ROOT=$(cd "$SKILL_DIR/../../.." && pwd)   # dev-guide → skills → .agents → 仓库根
cd "$ROOT"

pass=0
fail=0
ok()   { printf '  ✅ %s\n' "$1"; pass=$((pass + 1)); }
bad()  { printf '  ❌ %s\n' "$1"; fail=$((fail + 1)); }
hdr()  { printf '\n%s\n' "── $1"; }

hdr "1/5 双语文档（缺件 / 疑似未翻译 / 英文版断链 必须全 0）"
if [ -f tools/i18n.py ]; then
  out=$(python3 tools/i18n.py check 2>&1)
  echo "$out" | head -1 | sed 's/^/     /'
  if echo "$out" | grep -q '缺英文版 0' && echo "$out" | grep -q '疑似未翻译 0' && echo "$out" | grep -q '英文版断链 0'; then
    ok "双语三项均为 0"
  else
    bad "双语体检未通过（明细见上）"
  fi
else
  bad "缺少 tools/i18n.py"
fi

hdr "2/5 站点数据可重新生成且幂等"
if [ -f tools/build_site.py ]; then
  before=$(git status --porcelain -- site/data/ 2>/dev/null | wc -l)
  if python3 tools/build_site.py --quiet >/dev/null 2>&1; then
    after=$(git status --porcelain -- site/data/ 2>/dev/null | wc -l)
    if [ "$after" -le "$before" ]; then
      ok "生成成功且未产生额外改动（幂等）"
    else
      bad "重新生成后 site/data/ 有变化：需要一并提交"
    fi
  else
    bad "build_site.py 执行失败"
  fi
else
  bad "缺少 tools/build_site.py"
fi

hdr "3/5 技能自检"
run_check() { # $1=描述 $2=解释器 $3=脚本路径 ...
  local desc=$1; shift
  if [ ! -e "$2" ]; then printf '  ⏭  %s（%s 不存在，跳过）\n' "$desc" "$2"; return; fi
  if "$@" >/dev/null 2>&1; then ok "$desc"; else bad "$desc"; fi
}
run_check "image-tools 离线自检"          python3 .agents/skills/image-tools/scripts/test_skill.py
run_check "text-to-image-comfyui mock"    python3 .agents/skills/text-to-image-comfyui/scripts/test_skill.py
run_check "seedream-text-to-image mock"   python3 .agents/skills/seedream-text-to-image/scripts/test_skill.py
run_check "seedream-image-edit mock"      python3 .agents/skills/seedream-image-edit/scripts/test_skill.py
run_check "image-edit-comfyui mock"       python3 .agents/skills/image-edit-comfyui/scripts/test_skill.py
run_check "comfyui_gen --check（真机）"    python3 .agents/skills/text-to-image-comfyui/scripts/comfyui_gen.py --check
run_check "comfyui_edit --check（真机）"   python3 .agents/skills/image-edit-comfyui/scripts/comfyui_edit.py --check
# seedream 的 --check 只看"节点在位 + schema 对账 + 有没有凭据"，不花钱；
# 付费矩阵 verify_params.py / verify_edits.py 故意不放进这里（每步一张图，要人工决定）
run_check "seedream_gen --check（真机）"   python3 .agents/skills/seedream-text-to-image/scripts/seedream_gen.py --check
run_check "seedream_edit --check（真机）"  python3 .agents/skills/seedream-image-edit/scripts/seedream_edit.py --check

hdr "4/5 站点界面文案双语（T.zh / T.en）"
if [ -f tools/i18n.py ]; then
  if out=$(python3 tools/i18n.py ui 2>&1); then
    echo "$out" | head -1 | sed 's/^/     /'
    ok "界面文案双语一致（键一致 / 英文无中文 / 无 T 表外中文串）"
  else
    echo "$out" | sed 's/^/     /'
    bad "界面文案体检未通过"
  fi
else
  bad "缺少 tools/i18n.py"
fi

hdr "5/5 开发规范技能自身格式（DSH 项目技能）"
SK="$SKILL_DIR/SKILL.md"
if [ -f "$SK" ]; then
  name=$(sed -n 's/^name:[[:space:]]*//p' "$SK" | head -1)
  desc=$(sed -n 's/^description:[[:space:]]*//p' "$SK" | head -1)
  case "$name" in
    *[!a-z0-9-]*|'') bad "name 不是 kebab-case：'$name'" ;;
    -*)              bad "name 以连字符开头" ;;
    *)               ok "name 合法：$name" ;;
  esac
  if [ "$name" = "$(basename "$SKILL_DIR")" ]; then ok "name 与目录名一致"; else bad "name 与目录名不一致（$name vs $(basename "$SKILL_DIR")）"; fi
  dlen=${#desc}
  if [ "$dlen" -gt 0 ] && [ "$dlen" -le 1024 ]; then
    ok "description 存在（$dlen 字符）"
    [ "$dlen" -le 500 ] || printf '  ⚠️  description 超过 DSH 目录默认上限 500 字符，会被截断\n'
  else
    bad "description 缺失或超过 1024 字符"
  fi
  for d in references scripts templates assets; do
    [ -d "$SKILL_DIR/$d" ] && find "$SKILL_DIR/$d" -name 'SKILL.md' | grep -q . && bad "$d/ 下不应再有 SKILL.md（DSH 不支持嵌套发现）"
  done
  ok "无嵌套 SKILL.md"
else
  bad "缺少 $SK"
fi

printf '\n结果：%d 项通过，%d 项未通过\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
