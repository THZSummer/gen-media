#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给前端资源引用打版本戳：`site/app.css?v=<内容哈希>` / `site/app.js?v=<内容哈希>`。

为什么需要这个脚本
------------------
站点没有构建步骤，`index.html` 里的 `<link>` / `<script>` 是裸 URL。浏览器（尤其是 IDE 内置浏览器）
会按自己的策略缓存它们，于是出现过这种**混合缓存**：新的 `index.html`（带主题按钮）+ 旧的
`app.css`（没有 `.theme` 样式）+ 旧的 `app.js`（没有主题逻辑）——表现是按钮变成一个**空框**、
点了没反应。给 URL 带上内容哈希后，前端一改 URL 就变，浏览器只能取新文件；哈希没变说明没改，
既不会白刷缓存，也不可能新旧混搭。

用法
----
    python3 tools/stamp_frontend.py            # 写入（幂等；内容没变就一个字节都不动）
    python3 tools/stamp_frontend.py --check    # 只检查（进 check.sh，忘了打戳会失败）
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
ASSETS = ("site/app.css", "site/app.js")
STAMP_RE = {
    "site/app.css": re.compile(r'(href="site/app\.css)(?:\?v=[0-9a-f]+)?(")'),
    "site/app.js": re.compile(r'(src="site/app\.js)(?:\?v=[0-9a-f]+)?(")'),
}


def digest() -> str:
    """两个前端文件的内容哈希（前 8 位）——任一文件变了，戳就变。"""
    h = hashlib.sha1()
    for rel in ASSETS:
        with open(os.path.join(ROOT, rel), "rb") as fh:
            h.update(fh.read())
    return h.hexdigest()[:8]


def current() -> str | None:
    """index.html 里现有的戳（两个引用必须一致，否则返回 None）。"""
    src = open(INDEX, encoding="utf-8").read()
    found = set()
    for rel, rx in STAMP_RE.items():
        m = rx.search(src)
        if not m:
            return None
        found.add(re.search(r"\?v=([0-9a-f]+)", m.group(0)).group(1)
                  if "?v=" in m.group(0) else "")
    return found.pop() if len(found) == 1 else None


def write() -> tuple[str, bool]:
    want = digest()
    src = open(INDEX, encoding="utf-8").read()
    out = src
    for rel, rx in STAMP_RE.items():
        out = rx.sub(lambda m: f"{m.group(1)}?v={want}{m.group(2)}", out, count=1)
    if out == src:
        return want, False
    with open(INDEX, "w", encoding="utf-8") as fh:
        fh.write(out)
    return want, True


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="前端资源版本戳（内容哈希）")
    ap.add_argument("--check", action="store_true", help="只检查，不写")
    args = ap.parse_args(argv)

    want, changed = ("", False) if args.check else write()
    got = current()
    if args.check:
        want = digest()
        if got == want:
            print(f"前端版本戳：{want}（{'+'.join(ASSETS)} 一致）")
            return 0
        print(f"❌ 前端版本戳不对：index.html 里是 {got or '（缺失）'}，"
              f"按当前 app.css/app.js 应为 {want}；跑 `python3 tools/stamp_frontend.py` 写入",
              file=sys.stderr)
        return 1
    print(f"前端版本戳：{want}" + ("（已更新 index.html）" if changed else "（已是这个戳，未改动）"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
