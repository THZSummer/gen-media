#!/usr/bin/env python3
"""Locate the shared ComfyUI engine used by the image-gen skills.

``text-to-video-fastvideo3`` reuses the generic HTTP plumbing (queue / poll /
download / prompt recording) and the UI->API workflow converter from
``Book/image-gen/skills/text-to-image-comfyui``; only the workflow, its
parameter profile and the video download path differ.

The engine lives in a *sibling library* (image-gen), so the search order is:

1. ``$COMFYUI_SHARED_SCRIPTS`` (explicit override)
2. ``<repo>/Book/image-gen/skills/text-to-image-comfyui/scripts`` (real layout)
3. ``../text-to-image-comfyui/scripts`` (if both skills ever share one skills/)

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
CANDIDATES = [
    os.environ.get("COMFYUI_SHARED_SCRIPTS") or "",
    os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "image-gen", "skills",
                                  "text-to-image-comfyui", "scripts")),
    os.path.normpath(os.path.join(HERE, "..", "..", "text-to-image-comfyui", "scripts")),
]
SIBLING = next((p for p in CANDIDATES if p and os.path.isdir(p)), CANDIDATES[1])


def ensure() -> str:
    """Put the shared engine on sys.path; raise a clear error if it is absent."""
    if not os.path.isdir(SIBLING):
        raise RuntimeError(
            "shared ComfyUI engine not found; looked in:\n  "
            + "\n  ".join(p for p in CANDIDATES if p)
            + "\nInstall image-gen/skills/text-to-image-comfyui next to video-gen,"
            " or point $COMFYUI_SHARED_SCRIPTS at its scripts/ directory."
        )
    if SIBLING not in sys.path:
        sys.path.insert(0, SIBLING)
    return SIBLING
