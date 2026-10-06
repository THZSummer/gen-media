#!/usr/bin/env python3
"""Locate the sibling Seedream engine (`seedream-text-to-image/scripts`).

`seedream-image-edit` 与 `seedream-text-to-image` 用的是**同一个**付费 partner 节点
（`ByteDanceSeedreamNodeV3`）、同一套凭据通道、同一套 schema 快照与同一套
UI→API 转换器；差别只在"给不给参考图"以及参考图怎么接进去。所以这里不复制那份
引擎代码，而是像 `image-to-video-fastvideo3/scripts/_shared.py` 那样把它挂上 sys.path，
保证修一处两边都受益（凭据通道、dotted 输入名这些事实都只写一遍）。

扁平化后技能同处仓库根的 ``.agents/skills/``，本文件位于
``.agents/skills/seedream-image-edit/scripts/``，因此兄弟目录就是：

1. ``$SEEDREAM_SHARED_SCRIPTS``（显式覆盖，便于把技能单独拷出去用）
2. ``../../seedream-text-to-image/scripts``（仓库里的唯一真实布局）

Import order::

    import _shared
    _shared.ensure()
    import seedream_api as A       # UI->API 转换 / schema 校验 / 尺寸解析
    import seedream_gen as G       # 凭据 / 排队 / 轮询 / 下载 / 留档
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIBLING = os.path.normpath(
    os.path.join(HERE, "..", "..", "seedream-text-to-image", "scripts"))

CANDIDATES = [
    os.environ.get("SEEDREAM_SHARED_SCRIPTS") or "",
    SIBLING,
]


def ensure() -> str:
    """Put the sibling Seedream engine on sys.path; raise a clear error if absent."""
    override = os.environ.get("SEEDREAM_SHARED_SCRIPTS")
    path = override or SIBLING
    if not os.path.isdir(path):
        raise RuntimeError(
            "找不到兄弟技能的 Seedream 引擎；找过：\n  "
            + "\n  ".join(p for p in CANDIDATES if p)
            + "\n预期 .agents/skills/seedream-text-to-image/scripts 与本技能并列，"
            "或把 $SEEDREAM_SHARED_SCRIPTS 指到它的 scripts/ 目录。"
        )
    if path not in sys.path:
        sys.path.insert(0, path)
    return path
