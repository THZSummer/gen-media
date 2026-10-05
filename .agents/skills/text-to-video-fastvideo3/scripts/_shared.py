#!/usr/bin/env python3
"""Locate the shared ComfyUI engine used by the sibling image skill.

``text-to-video-fastvideo3`` reuses the generic HTTP plumbing (queue / poll /
download / prompt recording) and the UI->API workflow converter from
``.agents/skills/text-to-image-comfyui``; only the workflow, its parameter profile and
the video download path differ.

扁平化后 5 个技能同处仓库根的 ``.agents/skills/``，本文件位于
``.agents/skills/text-to-video-fastvideo3/scripts/``，因此共享引擎就在兄弟目录：

1. ``$COMFYUI_SHARED_SCRIPTS``（显式覆盖）
2. ``../../text-to-image-comfyui/scripts``（扁平化后的唯一真实布局）

Import order::

    import _shared
    _shared.ensure()
    import comfyui_gen as cg            # generic engine helpers
    from comfyui_convert import convert_ex, load_profile
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIBLING = os.path.normpath(
    os.path.join(HERE, "..", "..", "text-to-image-comfyui", "scripts"))

CANDIDATES = [
    os.environ.get("COMFYUI_SHARED_SCRIPTS") or "",
    SIBLING,
]


def ensure() -> str:
    """Put the shared engine on sys.path; raise a clear error if it is absent."""
    if not os.path.isdir(SIBLING):
        raise RuntimeError(
            "shared ComfyUI engine not found; looked in:\n  "
            + "\n  ".join(p for p in CANDIDATES if p)
            + "\nExpected .agents/skills/text-to-image-comfyui/scripts next to this skill,"
            " or point $COMFYUI_SHARED_SCRIPTS at its scripts/ directory."
        )
    if SIBLING not in sys.path:
        sys.path.insert(0, SIBLING)
    return SIBLING
