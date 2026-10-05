#!/usr/bin/env python3
"""Locate the shared ComfyUI engine that lives in the sibling skill.

``image-edit-comfyui`` reuses the generic HTTP plumbing (queue / poll /
download / prompt recording) and the UI->API workflow converter from
``text-to-image-comfyui``; only the workflow and its parameter profile differ.

Both skills must sit in the same ``.agents/skills/`` directory. Import order:

    import _shared
    _shared.ensure()
    import comfyui_gen as cg          # generic engine helpers
    from comfyui_convert import convert_ex, load_profile
"""
from __future__ import annotations

import os
import sys

SIBLING = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "text-to-image-comfyui", "scripts"))
# AI-free deterministic image tooling: pixel comparison, contact sheets, PNG
# encode/decode.  This skill depends on that layer, never the other way round.
TOOLS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "image-tools", "scripts"))


def ensure() -> str:
    """Put the sibling skill's (and image-tools') scripts on sys.path.

    Raises a clear error when a dependency is absent, so a half-installed
    .agents/skills/ tree fails loudly instead of failing on a confusing ImportError.
    """
    if not os.path.isdir(SIBLING):
        raise RuntimeError(
            "shared engine not found: expected the sibling skill at "
            f"{SIBLING}. Install text-to-image-comfyui next to image-edit-comfyui."
        )
    if not os.path.isdir(TOOLS):
        raise RuntimeError(
            f"image-tools not found at {TOOLS}. Install the image-tools skill "
            "next to image-edit-comfyui (it provides pngdiff / contact_sheet)."
        )
    for path in (SIBLING, TOOLS):
        if path not in sys.path:
            sys.path.insert(0, path)
    return SIBLING
