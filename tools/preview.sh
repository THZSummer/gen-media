#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# 本地预览画廊：重新生成站点数据，然后起一个只读 HTTP 服务。
#
# 用法：
#   tools/preview.sh                 # 默认 http://127.0.0.1:8090/（仅本机可访问）
#   tools/preview.sh 8123            # 换端口
#   tools/preview.sh 8123 lan        # 绑定 0.0.0.0：同局域网的手机/平板也能看
#   tools/preview.sh stop [端口]     # 停掉本脚本起过的预览（默认 8090）
#   tools/preview.sh --help
#
# 端口被占时不会抛异常：若占用者就是本画廊，会提示直接用；若是别的程序，自动换端口。
#
# 注意：必须通过 HTTP 打开——直接双击 index.html（file://）会被浏览器的跨源策略挡住，
# 读不到 site/data/*.json。
# ─────────────────────────────────────────────────────────────────────────────

# 允许用 sh 调用（dash 不支持 pipefail / /dev/tcp，直接换 bash 重跑自己）
if [ -z "${BASH_VERSION:-}" ]; then exec bash "$0" "$@"; fi
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
PORT=${1:-8090}
MODE=${2:-}
BIND=127.0.0.1
[ "$MODE" = "lan" ] && BIND=0.0.0.0

usage() {
  sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

# 端口是否已被监听（优先 ss，退化到 bash 的 /dev/tcp）
busy() {
  if command -v ss >/dev/null 2>&1; then
    ss -ltn 2>/dev/null | awk '{print $4}' | grep -qE "[:.]$1\$"
  else
    (exec 3<>"/dev/tcp/127.0.0.1/$1") 2>/dev/null
  fi
}

# 该端口上跑的，是不是就是本画廊
is_ours() {
  curl -fsS --max-time 3 "http://127.0.0.1:$1/" 2>/dev/null | grep -q '生成式媒体\|Generative Media'
}

find_free() {
  local p=$1
  while busy "$p"; do p=$((p + 1)); done
  echo "$p"
}

stop_preview() {
  local port=$1 pids pid n=0
  if ! command -v ss >/dev/null 2>&1; then
    echo "需要 ss 才能定位进程（iproute2），请手动停止：pkill -f 'http.server $port'" >&2
    return 1
  fi
  # 注意：grep 无匹配时状态码为 1，配合 set -e/pipefail 会中断整个函数，故收尾 || true
  pids=$(ss -ltnp 2>/dev/null | awk -v p=":$port" '$4 ~ p"$"' | grep -o 'pid=[0-9]*' | cut -d= -f2 | sort -u || true)
  if [ -z "$pids" ]; then
    echo "端口 $port 上没有监听进程，无需停止"
    return 0
  fi
  for pid in $pids; do
    # 只杀 http.server，避免误伤别的程序
    if tr '\0' ' ' <"/proc/$pid/cmdline" 2>/dev/null | grep -q 'http\.server'; then
      kill "$pid" 2>/dev/null && { echo "已停止进程 $pid（端口 $port）"; n=$((n + 1)); }
    else
      echo "跳过 PID $pid：不是 http.server（$(tr '\0' ' ' <"/proc/$pid/cmdline" 2>/dev/null | cut -c1-60)）"
    fi
  done
  [ "$n" -gt 0 ] || echo "没有停止任何进程（端口 $port 被非 http.server 程序占用）"
}

case "$PORT" in
  -h|--help|help) usage ;;
  stop)
    stop_preview "${2:-8090}"
    exit 0
    ;;
esac

case "$PORT" in
  ''|*[!0-9]*) echo "端口必须是数字：$PORT" >&2; exit 2 ;;
esac

cd "$ROOT"

echo "→ 生成站点数据"
python3 tools/build_site.py

if busy "$PORT"; then
  if is_ours "$PORT"; then
    echo
    echo "ℹ️  端口 $PORT 上已经有一个本画廊的预览在跑（可能是上一次没退出的会话）。"
    echo "    直接打开：http://127.0.0.1:$PORT/"
    echo "    要自己起一个：先 tools/preview.sh stop $PORT，或换端口 tools/preview.sh $((PORT + 1))"
    exit 0
  fi
  NEWPORT=$(find_free $((PORT + 1)))
  echo
  echo "⚠️  端口 $PORT 被其它程序占用，改用空闲端口 $NEWPORT"
  PORT=$NEWPORT
fi

echo
echo "→ 站点根目录：$ROOT"
echo "→ 本机打开：  http://127.0.0.1:$PORT/"
if [ "$BIND" = "0.0.0.0" ]; then
  ip=$(hostname -I 2>/dev/null | awk '{print $1}')
  echo "→ 局域网打开：http://${ip:-<本机IP>}:$PORT/   （手机/平板同一 WiFi 可用）"
fi
echo "→ Ctrl-C 停止（或在别处跑 tools/preview.sh stop $PORT）"
echo

exec python3 -m http.server "$PORT" --bind "$BIND"
