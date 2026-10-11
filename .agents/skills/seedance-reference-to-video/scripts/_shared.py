#!/usr/bin/env python3
"""Locate the sibling Seedream engine (`seedream-text-to-image/scripts`).

`seedance-reference-to-video` 与 `seedream-text-to-image` / `seedream-image-edit` 走的是
**同一套 ComfyUI 付费 partner 节点机制**：都要把 UI 工作流转成 API 图、都要按节点 schema
校验参数、都要往 `/prompt` 的 `extra_data.api_key_comfy_org` 里带 ComfyUI 账号凭据。
差别只在**用哪个节点**（`ByteDance2ReferenceNodeV2` vs `ByteDanceSeedreamNodeV3`）。

所以这里不复制那份引擎，而是像 `seedream-image-edit/scripts/_shared.py` 那样把它挂上
sys.path —— 凭据通道、动态下拉框（`COMFY_DYNAMICCOMBO_V3`）、dotted 输入名、留档格式
这些事实都只写一遍。

扁平化后技能同处仓库根的 ``.agents/skills/``，本文件位于
``.agents/skills/seedance-reference-to-video/scripts/``，因此兄弟目录就是：

1. ``$SEEDANCE_SHARED_SCRIPTS``（显式覆盖，便于把技能单独拷出去用）
2. ``../../seedream-text-to-image/scripts``（仓库里的唯一真实布局）

Import order::

    import _shared
    _shared.ensure()
    import seedream_api as A       # UI->API 转换 / schema / 参数落图
    import seedream_gen as G       # 凭据 / 排队 / 轮询 / 下载 / 留档
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIBLING = os.path.normpath(
    os.path.join(HERE, "..", "..", "seedream-text-to-image", "scripts"))

CANDIDATES = [
    os.environ.get("SEEDANCE_SHARED_SCRIPTS") or "",
    SIBLING,
]


def ensure() -> str:
    """Put the sibling Seedream engine on sys.path; raise a clear error if absent."""
    override = os.environ.get("SEEDANCE_SHARED_SCRIPTS")
    path = override or SIBLING
    if not os.path.isdir(path):
        raise RuntimeError(
            "找不到兄弟技能的共享引擎；找过：\n  "
            + "\n  ".join(p for p in CANDIDATES if p)
            + "\n预期 .agents/skills/seedream-text-to-image/scripts 与本技能并列，"
            "或把 $SEEDANCE_SHARED_SCRIPTS 指到它的 scripts/ 目录。"
        )
    if path not in sys.path:
        sys.path.insert(0, path)
    return path
