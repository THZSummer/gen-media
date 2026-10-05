#!/usr/bin/env python3
"""Tile generated images into one labelled contact sheet, for quick review.

**No AI, no GPU, no ComfyUI, no network.**  numpy lays the tiles out, ffmpeg
decodes/encodes and burns the labels in with real fonts (``drawtext``, so CJK
works when a CJK font is installed).

That is a requirement, not a shortcut.  A contact sheet is *evidence*: it is what
you judge prompts and seeds against.  If a generative model touched it, the tiles
would no longer be pixel-faithful copies of the deliverables and the sheet could
not be trusted as a record of what was actually produced.

Tiles are downscaled with a box average (numpy), not nearest: the sheet is used
to judge beaks, seams and fur transitions, and aliasing would hide exactly what
is being reviewed.  ``--cell 0`` keeps native resolution and resamples nothing.

Usage
-----
  # a whole round, in round.json order, labelled with shot name + seed
  python3 contact_sheet.py --round out/r1/round.json -o out/r1/sheet.png --cols 3

  # explicit files in the reading order you want (``-`` = blank cell)
  python3 contact_sheet.py a.png b.png - c.png -o sheet.png --cols 3 --title "R1 A/B/C"

  # labels are real text, so Chinese works with a CJK font
  python3 contact_sheet.py --round out/r1/round.json -o s.png --title "第一轮"

Library::

  from contact_sheet import build_sheet
  build_sheet(["a.png", "b.png"], "sheet.png", cols=2, title="R1")
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ffkit  # noqa: E402

BG = (24, 24, 26)
BORDER = (68, 68, 74)
LABEL_FG = "0xE8E8EC"
TITLE_FG = "0xFFFFFF"
BLANK = (40, 40, 44)
PAD = 8
LABEL_SIZE = 22
TITLE_SIZE = 34
LABEL_GAP = 6

# drawtext needs a real font file; prefer one that also covers CJK, because the
# labels in this repo mix ASCII shot names with Chinese round titles.
FONT_CANDIDATES = (
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)


def default_font() -> str | None:
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def has_drawtext() -> bool:
    """True when this ffmpeg build can render text (libfreetype linked)."""
    try:
        ffmpeg, _ = ffkit.require_ffmpeg()
    except ffkit.ToolError:
        return False
    return b" drawtext " in ffkit._run([ffmpeg, "-hide_banner", "-filters"])


def _escape(text: str) -> str:
    """Escape a drawtext option value embedded in a filtergraph.

    The filtergraph is passed as a single argv element (no shell), so only
    ffmpeg's own level-1 escaping applies.  Adversarial labels are covered by the
    self-test.
    """
    out = text.replace("\\", "\\\\")
    for ch in (":", "'", "%", ",", "[", "]", ";", "="):
        out = out.replace(ch, "\\" + ch)
    return out


def _label_for(path: str, label_mode: str) -> str:
    """Tile label: the stem, without ComfyUI's ``_00001_`` counter."""
    stem = os.path.splitext(os.path.basename(path))[0]
    if label_mode == "none":
        return ""
    if label_mode == "name":
        return re.sub(r"_\d+_?$", "", stem)
    return stem


def _drawtext(text: str, font: str, size: int, x: int, y: int, colour: str) -> str:
    return (f"drawtext=fontfile={_escape(font)}:fontsize={size}:fontcolor={colour}"
            f":x={x}:y={y}:text='{_escape(text)}'")


def build_sheet(
    paths: list[str],
    out_path: str,
    cols: int = 3,
    cell: int = 512,
    title: str | None = None,
    label_mode: str = "name",
    labels: list[str] | None = None,
    font: str | None = None,
    label_size: int = LABEL_SIZE,
    title_size: int = TITLE_SIZE,
) -> dict:
    """Compose ``paths`` into a labelled grid.  A ``"-"`` entry leaves a blank cell."""
    if cols < 1:
        raise ValueError("cols must be >= 1")
    tiles: list[tuple[str, np.ndarray | None]] = []
    for path in paths:
        if path == "-":
            tiles.append(("-", None))
            continue
        arr = ffkit.decode(path)[:, :, :3]
        tiles.append((path, ffkit.box_downscale(arr, cell)))
    if not tiles:
        raise ValueError("no images given")

    if labels is None:
        labels = [_label_for(p, label_mode) if p != "-" else "" for p in paths]
    draw = bool(has_drawtext() and (any(labels) or title))
    font = font or default_font()
    if draw and not font:
        print("warning: no usable font found; labels will be omitted", file=sys.stderr)
        draw = False

    label_h = 0 if (label_mode == "none" or not draw) else label_size + LABEL_GAP
    title_h = 0 if not (title and draw) else title_size + 14
    th = max((t[1].shape[0] for t in tiles if t[1] is not None), default=1)
    tw = max((t[1].shape[1] for t in tiles if t[1] is not None), default=1)
    rows = (len(tiles) + cols - 1) // cols
    width = PAD + cols * (tw + PAD)
    height = PAD + title_h + rows * (th + label_h + PAD)

    canvas = np.empty((height, width, 3), dtype=np.uint8)
    canvas[:, :] = BG

    def box(x: int, y: int, w: int, h: int, colour) -> None:
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(width, x + w), min(height, y + h)
        if x1 > x0 and y1 > y0:
            canvas[y0:y1, x0:x1] = colour

    chain: list[str] = []
    if title and draw:
        chain.append(_drawtext(title, font, title_size, PAD + 2, PAD + 4, TITLE_FG))

    manifest = {"out": out_path, "cols": cols, "rows": rows, "cell": cell,
                "tile": [tw, th], "sheet": [width, height], "labels_drawn": draw,
                "font": font if draw else None, "tiles": []}
    for i, (path, arr) in enumerate(tiles):
        cx = PAD + (i % cols) * (tw + PAD)
        cy = PAD + title_h + (i // cols) * (th + label_h + PAD)
        box(cx - 2, cy - 2, tw + 4, th + 4, BORDER)
        if arr is None:
            box(cx, cy, tw, th, BLANK)
        else:
            # 居中对齐：一格内各图的宽高比可能不同（例如竖幅与方图混排），
            # 靠左上角会让留白全堆在右侧/下方，读起来像排错了。
            h, w = arr.shape[:2]
            ox, oy = cx + (tw - w) // 2, cy + (th - h) // 2
            canvas[oy:oy + h, ox:ox + w] = arr
            cx, cy = ox, oy
        label = labels[i] if i < len(labels) else ""
        if label and draw:
            chain.append(_drawtext(label, font, label_size, cx + 2, cy + th + LABEL_GAP, LABEL_FG))
        manifest["tiles"].append({"path": path, "label": label, "x": cx, "y": cy,
                                  "w": arr.shape[1] if arr is not None else 0,
                                  "h": arr.shape[0] if arr is not None else 0})

    ffkit.encode(out_path, canvas, vf=",".join(chain) if chain else None)
    manifest["bytes"] = os.path.getsize(out_path)
    return manifest


def _load_round(path: str) -> tuple[list[str], list[str], str]:
    """Read a round.json written by a project's run_round.py.

    A shot whose file is missing from disk becomes a blank cell, so a partially
    generated round still produces a readable sheet instead of failing.
    """
    data = json.load(open(path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(path))
    paths, labels = [], []
    for shot in data.get("shots", []):
        f = shot.get("file")
        if not f:
            paths.append("-")
            labels.append("")
            continue
        # The recorded path is only a hint: it goes stale when a project is
        # reorganised, so prefer the file sitting next to round.json.
        beside = os.path.join(base, os.path.basename(f))
        paths.append(beside if os.path.exists(beside)
                     else (f if os.path.isabs(f) else os.path.join(base, f)))
        labels.append(f"{shot.get('name', '?')} · seed {shot.get('seed', '?')}")
    seeds = {s.get("seed") for s in data.get("shots", [])}
    title = f"R{data.get('round', '?')} · {data.get('engine', '?')}"
    title += f" · seed {sorted(seeds)[0]}" if len(seeds) == 1 else f" · {len(seeds)} seeds"
    if any(s.get("unapplied") for s in data.get("shots", [])):
        title += " · UNAPPLIED!"
    return paths, labels, title


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("images", nargs="*", help='image paths in reading order ("-" = blank cell)')
    ap.add_argument("--round", action="append", default=[], metavar="ROUND.JSON",
                    help="build from a run_round.py round.json (repeatable; merged in order)")
    ap.add_argument("--glob", dest="pattern", help="glob for image paths, sorted")
    ap.add_argument("-o", "--out", default="sheet.png")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--cell", type=int, default=512,
                    help="max tile edge in px (box-averaged); 0 = native, no resampling")
    ap.add_argument("--scale", type=float, default=0.0,
                    help="tile edge = source edge * scale (overrides --cell)")
    ap.add_argument("--title", help="header text (default: derived from --round)")
    ap.add_argument("--font", help="font file for labels (default: auto-detect, CJK-capable)")
    ap.add_argument("--label-size", type=int, default=LABEL_SIZE)
    ap.add_argument("--label-mode", choices=["name", "file", "none"], default="name")
    ap.add_argument("--manifest", help="also write the layout as JSON here")
    args = ap.parse_args(argv)

    paths: list[str] = []
    labels: list[str] | None = [] if args.round else None
    title = args.title

    if args.round:
        for rj in args.round:
            rpaths, rlabels, rtitle = _load_round(rj)
            paths += rpaths
            labels += rlabels
            title = title or rtitle
    if args.pattern:
        paths += sorted(glob.glob(args.pattern))
        labels = None
    paths += args.images
    if not paths:
        ap.error("no images: pass paths, --glob or --round")

    if args.scale > 0:
        first = next((p for p in paths if p != "-"), None)
        if first is None:
            ap.error("--scale needs at least one real image")
        meta = ffkit.probe(first)
        args.cell = max(1, int(max(meta["width"], meta["height"]) * args.scale))

    try:
        manifest = build_sheet(paths, args.out, cols=args.cols, cell=args.cell,
                               title=title, label_mode=args.label_mode, labels=labels,
                               font=args.font, label_size=args.label_size)
    except ffkit.ToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.manifest:
        with open(args.manifest, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)
    print(json.dumps({k: manifest[k] for k in
                      ("out", "cols", "rows", "tile", "sheet", "bytes", "labels_drawn")},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
