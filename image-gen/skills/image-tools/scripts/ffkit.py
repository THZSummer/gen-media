#!/usr/bin/env python3
"""Image primitives built on ffmpeg + numpy.

**No AI, no model, no network.**  ffmpeg does decode/encode/transform, numpy does
the array work.  Both are mature, battle-tested and already present on this
machine (ffmpeg is what ``bone-china-doll/make_macro.sh`` crops and rescales
with), so there is no reason to hand-roll a PNG codec.

Why the determinism still matters
---------------------------------
These tools make *evidence* about generated images: a contact sheet you judge
prompts against, a pixel diff you trust as "reproducible".  If any step involved
a generative model the output would stop being a faithful copy of the
deliverables.  Every operation here is a pure function of its inputs, and the
only non-Python dependency is ffmpeg itself.

Usage
-----
  python3 ffkit.py info a.png b.png
  python3 ffkit.py strip in.png -o out.png          # drop PNG tEXt/ancillary chunks
  python3 ffkit.py resize in.png -o small.png --max-edge 512
  python3 ffkit.py crop in.png -o face.png --box 100,200,400,400
  python3 ffkit.py pngchunks in.png                 # chunk list (metadata forensics)
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import struct
import subprocess
import sys
from dataclasses import dataclass

import numpy as np

FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
FFPROBE = os.environ.get("FFPROBE", "ffprobe")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class ToolError(RuntimeError):
    """An external tool is missing or refused the input."""


def require_ffmpeg() -> tuple[str, str]:
    """Return (ffmpeg, ffprobe) or raise with an actionable message."""
    ffmpeg = shutil.which(FFMPEG)
    ffprobe = shutil.which(FFPROBE)
    if not ffmpeg or not ffprobe:
        raise ToolError(
            "ffmpeg/ffprobe not found on PATH (looked for "
            f"{FFMPEG!r} and {FFPROBE!r}). Install it, e.g. "
            "`sudo apt-get install -y ffmpeg`, or point $FFMPEG / $FFPROBE at the binaries."
        )
    return ffmpeg, ffprobe


def require_numpy() -> str:
    return np.__version__


def _run(cmd: list[str], *, capture: bool = True) -> bytes:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.PIPE)
    if proc.returncode != 0:
        tail = (proc.stderr or b"").decode("utf-8", "replace").strip().splitlines()[-3:]
        raise ToolError(f"{cmd[0]} failed ({proc.returncode}): " + " | ".join(tail))
    return proc.stdout or b""


# ------------------------------------------------------------------- PNG bytes

def png_chunks(path: str) -> list[str]:
    """Chunk tags in file order (no decoding) -- metadata forensics.

    ComfyUI writes the executed graph into ``tEXt``, which is why two files with
    identical pixels routinely have different sha256.  Cheap and exact, so it
    stays pure Python rather than going through ffprobe.
    """
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] != PNG_SIGNATURE:
        return []
    names: list[str] = []
    pos = 8
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        names.append(data[pos + 4:pos + 8].decode("latin-1"))
        pos += 12 + length
    return names


# Ancillary chunks carrying no pixels.  ffmpeg always writes pHYs (pixel
# density) and offers no flag to suppress it, so ``drop_metadata`` removes it
# afterwards -- ComfyUI does not write one, so this also keeps our output on the
# same convention as the files we compare against.
DROPPABLE_CHUNKS = ("tEXt", "zTXt", "iTXt", "eXIf", "tIME", "pHYs", "sPLT")


def drop_metadata(path: str, tags: tuple[str, ...] = DROPPABLE_CHUNKS) -> list[str]:
    """Rewrite a PNG without the given ancillary chunks; returns what was dropped.

    Only ancillary metadata is touched: the structural chunks a decoder needs
    (IHDR/PLTE/tRNS/IDAT/IEND) are always kept.
    """
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] != PNG_SIGNATURE:
        return []
    pos = 8
    kept: list[bytes] = []
    dropped: list[str] = []
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        tag = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if tag.decode("latin-1") in tags:
            dropped.append(tag.decode("latin-1"))
        else:
            kept.append(data[pos:end])
        pos = end
    if dropped:
        with open(path, "wb") as fh:
            fh.write(PNG_SIGNATURE + b"".join(kept))
    return dropped


def probe(path: str) -> dict:
    """Geometry/codec/size via ffprobe (works for any format ffmpeg reads)."""
    ffmpeg, ffprobe = require_ffmpeg()
    raw = _run([ffprobe, "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=width,height,pix_fmt,codec_name",
                "-show_entries", "format=format_name",
                "-of", "json", path])
    data = json.loads(raw.decode("utf-8"))
    stream = (data.get("streams") or [{}])[0]
    chunks = png_chunks(path)
    return {
        "path": path,
        "width": stream.get("width"),
        "height": stream.get("height"),
        "codec": stream.get("codec_name"),
        "pix_fmt": stream.get("pix_fmt"),
        "container": (data.get("format") or {}).get("format_name"),
        "bytes": os.path.getsize(path),
        "chunks": chunks,
        "has_workflow_metadata": "tEXt" in chunks,
    }


# ------------------------------------------------------------------ decode/encode

def decode(path: str, pix_fmt: str = "rgb24") -> np.ndarray:
    """Decode any readable image to a uint8 array ``(H, W, C)``.

    ``rgb24`` composites any alpha over black, which is what a review sheet
    wants; pass ``rgba`` to keep the alpha channel.
    """
    ffmpeg, _ = require_ffmpeg()
    meta = probe(path)
    if not meta["width"] or not meta["height"]:
        raise ToolError(f"{path}: no video stream / unknown geometry")
    channels = {"rgb24": 3, "rgba": 4, "gray": 1}[pix_fmt]
    raw = _run([ffmpeg, "-v", "error", "-i", path,
                "-f", "rawvideo", "-pix_fmt", pix_fmt, "-"])
    want = meta["width"] * meta["height"] * channels
    if len(raw) != want:
        raise ToolError(f"{path}: decoded {len(raw)} bytes, expected {want}")
    return np.frombuffer(raw, dtype=np.uint8).reshape(meta["height"], meta["width"], channels)


_JPEG_SUFFIXES = (".jpg", ".jpeg", ".jpe")


def encode(path: str, arr: np.ndarray, compression: int = 6, vf: str | None = None,
           minimal: bool = True, quality: int | None = None) -> str:
    """Encode a uint8 ``(H, W, 3|4)`` array to **PNG or JPEG** (by extension).

    - ``.png``  → lossless PNG. ``minimal`` strips the ancillary chunks ffmpeg
      adds by default, leaving a deterministic IHDR/IDAT/IEND file.
    - ``.jpg`` / ``.jpeg`` → lossy JPEG at ``quality`` (ffmpeg ``-q:v`` scale,
      2 = visually lossless, 31 = worst; default 3). Metadata is dropped so the
      output stays reproducible. **Use this for review/overview sheets**, whose
      job is to be looked at; keep deliverables as PNG.

    ``vf`` optionally runs ffmpeg filters on the way out (e.g. a ``drawtext``
    chain for contact-sheet labels), so burn-in needs no intermediate file.
    """
    ffmpeg, _ = require_ffmpeg()
    arr = np.ascontiguousarray(arr.astype(np.uint8, copy=False))
    if arr.ndim != 3 or arr.shape[2] not in (3, 4):
        raise ToolError(f"encode expects (H, W, 3|4), got {arr.shape}")
    h, w, c = arr.shape
    is_jpeg = path.lower().endswith(_JPEG_SUFFIXES)
    cmd = [ffmpeg, "-v", "error", "-y", "-f", "rawvideo",
           "-pix_fmt", "rgb24" if c == 3 else "rgba", "-s", f"{w}x{h}", "-i", "-"]
    if vf:
        cmd += ["-vf", vf]
    if is_jpeg:
        # JPEG has no alpha: composite over nothing (rgb24 input already did).
        cmd += ["-frames:v", "1", "-map_metadata", "-1",
                "-q:v", str(3 if quality is None else quality), path]
    else:
        cmd += ["-frames:v", "1", "-compression_level", str(compression), path]
    proc = subprocess.run(cmd, input=arr.tobytes(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        tail = (proc.stderr or b"").decode("utf-8", "replace").strip().splitlines()[-3:]
        raise ToolError(f"ffmpeg encode failed ({proc.returncode}): " + " | ".join(tail))
    if minimal and not is_jpeg:
        drop_metadata(path)
    return path


# -------------------------------------------------------------------- transform

def box_downscale(arr: np.ndarray, max_edge: int) -> np.ndarray:
    """Integer-factor box average; returns the input unchanged if already small.

    Box rather than nearest: review sheets are used to judge beaks, seams and fur
    transitions, and nearest-neighbour aliasing would hide exactly that.
    """
    if max_edge <= 0 or max(arr.shape[:2]) <= max_edge:
        return arr
    factor = max(1, round(max(arr.shape[:2]) / max_edge))
    if factor <= 1:
        return arr
    h, w = arr.shape[:2]
    oh, ow = h // factor, w // factor
    if oh < 1 or ow < 1:
        return arr
    trimmed = arr[:oh * factor, :ow * factor]
    # (oh, f, ow, f, C) -> average over the block axes: exact and vectorised
    blocks = trimmed.reshape(oh, factor, ow, factor, arr.shape[2])
    return blocks.mean(axis=(1, 3)).round().astype(np.uint8)


def crop(arr: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:
    """Crop a rectangle, clipped to the array bounds."""
    H, W = arr.shape[:2]
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        raise ToolError(f"empty crop box ({x},{y},{w},{h}) for a {W}x{H} image")
    return arr[y0:y1, x0:x1]


def scale_to(arr: np.ndarray, factor: int) -> np.ndarray:
    """Integer nearest-neighbour upscale (for enlarging small crops)."""
    if factor <= 1:
        return arr
    return np.repeat(np.repeat(arr, factor, axis=0), factor, axis=1)


def strip_metadata(src: str, dst: str) -> dict:
    """Rewrite an image from decoded pixels, dropping all metadata.

    Pixels are re-encoded (so the workflow/tEXt blob cannot survive) and the
    ancillary chunks ffmpeg re-adds are dropped afterwards.
    """
    arr = decode(src)
    encode(dst, arr, minimal=False)
    dropped = drop_metadata(dst)
    before, after = os.path.getsize(src), os.path.getsize(dst)
    return {"in": src, "out": dst, "bytes_before": before, "bytes_after": after,
            "saved": before - after, "chunks_after": png_chunks(dst),
            "chunks_dropped": [c for c in probe(src)["chunks"]
                               if c in DROPPABLE_CHUNKS] + dropped}


def info(path: str) -> dict:
    meta = probe(path)
    if meta["width"]:
        meta["megapixels"] = round(meta["width"] * meta["height"] / 1e6, 3)
    return meta


def _parse_box(text: str) -> tuple[int, int, int, int]:
    parts = [int(p) for p in text.replace(" ", "").split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("--box needs x,y,w,h")
    return parts[0], parts[1], parts[2], parts[3]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_info = sub.add_parser("info", help="geometry + codec + metadata chunks")
    p_info.add_argument("images", nargs="+")

    p_chunks = sub.add_parser("pngchunks", help="list PNG chunk tags")
    p_chunks.add_argument("images", nargs="+")

    p_strip = sub.add_parser("strip", help="drop all metadata (re-encode from pixels)")
    p_strip.add_argument("image")
    p_strip.add_argument("-o", "--out", required=True)

    for name in ("resize", "crop", "scale"):
        p = sub.add_parser(name)
        p.add_argument("image")
        p.add_argument("-o", "--out", required=True)
        if name == "resize":
            p.add_argument("--max-edge", type=int, required=True)
        elif name == "crop":
            p.add_argument("--box", type=_parse_box, required=True, help="x,y,w,h")
        else:
            p.add_argument("--factor", type=int, required=True)
    args = ap.parse_args(argv)

    try:
        if args.cmd == "info":
            for path in args.images:
                print(json.dumps(info(path), ensure_ascii=False))
            return 0
        if args.cmd == "pngchunks":
            for path in args.images:
                print(json.dumps({"path": path, "chunks": png_chunks(path)}, ensure_ascii=False))
            return 0
        if args.cmd == "strip":
            print(json.dumps(strip_metadata(args.image, args.out), ensure_ascii=False))
            return 0

        # everything else reads through numpy: no alpha, ffmpeg composites on black
        arr = decode(args.image)[:, :, :3]
        if args.cmd == "resize":
            out = box_downscale(arr, args.max_edge)
        elif args.cmd == "crop":
            out = crop(arr, *args.box)
        else:
            out = scale_to(arr, args.factor)
        encode(args.out, out)
        print(json.dumps({"in": args.image, "out": args.out, "from": list(arr.shape[:2]),
                          "to": list(out.shape[:2]), "bytes": os.path.getsize(args.out)},
                         ensure_ascii=False))
        return 0
    except ToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
