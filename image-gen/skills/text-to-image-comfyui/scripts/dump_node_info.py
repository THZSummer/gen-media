#!/usr/bin/env python3
"""Cache the parts of a ComfyUI /object_info we need for offline conversion.

Saves {class_type: {"input_order": {...}, "<input>": {...}}} for the classes used
by the workflow, so comfyui_convert can name widget inputs even when the UI JSON
omits them from a node's "inputs" list.

Usage:
  python3 dump_node_info.py --server http://192.168.3.5:18000 -o references/node-info.json
  python3 dump_node_info.py --server ... --classes KSampler,CLIPLoader
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comfyui_gen import _get_json  # noqa: E402

DEFAULT_CLASSES = [
    "CLIPLoader",
    "UNETLoader",
    "VAELoader",
    "CLIPTextEncode",
    "ConditioningZeroOut",
    "EmptySD3LatentImage",
    "ModelSamplingAuraFlow",
    "KSampler",
    "VAEDecode",
    "SaveImage",
]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", required=True)
    ap.add_argument("-o", "--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "node-info.json"))
    ap.add_argument("--classes", default=",".join(DEFAULT_CLASSES))
    args = ap.parse_args(argv)

    wanted = [c.strip() for c in args.classes.split(",") if c.strip()]
    info = _get_json(f"{args.server.rstrip('/')}/object_info", timeout=60.0)
    subset: dict = {}
    missing: list[str] = []
    for cls in wanted:
        node = info.get(cls)
        if node is None:
            missing.append(cls)
            continue
        entry: dict = {"input_order": node.get("input_order", {})}
        for section in ("required", "optional"):
            for name, spec in (node.get("input", {}) or {}).get(section, {}).items():
                entry[name] = {"required": section == "required", "spec": spec}
        subset[cls] = entry
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(subset, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"wrote {args.out}: {len(subset)} classes" + (f", missing {missing}" if missing else ""))
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
