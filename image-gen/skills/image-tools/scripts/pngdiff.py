#!/usr/bin/env python3
"""Compare images by *decoded pixels*: exact diff, PSNR and SSIM.

Why pixels and not file bytes
-----------------------------
ComfyUI writes the executed graph into the PNG's ``tEXt`` chunk.  Any difference
in the submitted graph -- including ``filename_prefix``, which every batch run
changes on purpose -- therefore changes the file hash while leaving the image
byte-for-byte identical::

    file sha256   1c2aaa2187d2... vs 5e47b6b227ae...        DIFFERENT
    pixels        0 / 1920000 differ (max channel delta 0)  IDENTICAL
    (bone-china-doll R34 vs R35 at the same seed; only filename_prefix differed)

So reproducibility is decided on pixels.  ``mean_abs_diff`` also works as a rough
meter of *how much* a prompt clause changed the render -- useful when a clause
may be doing nothing at all.

SSIM / PSNR
-----------
``psnr`` is the standard MSE form.  ``ssim`` is the windowed index with an 11x11
uniform window and the standard K1=0.01 / K2=0.03 constants.  It is deliberately
*documented as ours*, not as a bit-identical clone of scikit-image's
gaussian-weighted variant -- the repo previously quoted SSIM 0.929 / PSNR 30.3 dB
in a skill doc with no implementation behind it, which made those numbers
unreproducible.  Now they can be recomputed.

Usage
-----
  python3 pngdiff.py A.png B.png                 # 0 = identical, 1 = different, 2 = error
  python3 pngdiff.py A.png B.png --json          # full report incl. psnr/ssim
  python3 pngdiff.py A.png B.png --tolerance 2   # ignore deltas of 1..2

Library::

  from pngdiff import compare, pixels_equal, psnr, ssim
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ffkit  # noqa: E402


@dataclass
class Diff:
    """Result of comparing two decoded images."""

    same: bool
    differing: int
    total: int
    pct: float
    mean_abs_diff: float
    max_diff: int
    psnr: float
    ssim: float
    geometry: str
    detail: str

    def as_dict(self) -> dict:
        return asdict(self)


def _as_rgb(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Drop alpha so comparisons are channel-consistent."""
    if a.ndim == 3 and a.shape[2] == 4:
        a = a[:, :, :3]
    if b.ndim == 3 and b.shape[2] == 4:
        b = b[:, :, :3]
    return a, b


def psnr(a: np.ndarray, b: np.ndarray, peak: float = 255.0) -> float:
    """Peak signal-to-noise ratio in dB; ``inf`` for identical images."""
    a, b = _as_rgb(np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64))
    mse = float(np.mean((a - b) ** 2))
    if mse == 0.0:
        return float("inf")
    return 10.0 * float(np.log10(peak * peak / mse))


def _box_filter(x: np.ndarray, radius: int) -> np.ndarray:
    """Uniform (2r+1)^2 mean filter via summed-area table, edge-clamped."""
    pad = radius
    padded = np.pad(x, ((pad, pad), (pad, pad)), mode="edge")
    csum = np.cumsum(np.cumsum(padded, axis=0), axis=1)
    csum = np.pad(csum, ((1, 0), (1, 0)), mode="constant")
    k = 2 * radius + 1
    h, w = x.shape
    total = (csum[k:k + h, k:k + w] - csum[0:h, k:k + w]
             - csum[k:k + h, 0:w] + csum[0:h, 0:w])
    return total / (k * k)


def ssim(a: np.ndarray, b: np.ndarray, peak: float = 255.0, radius: int = 5) -> float:
    """Windowed SSIM with an 11x11 uniform window (K1=0.01, K2=0.03).

    Grayscale-luminance based (Rec.601 weights), matching the usual convention.
    """
    a, b = _as_rgb(np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64))
    if a.shape != b.shape:
        raise ValueError(f"ssim needs equal shapes, got {a.shape} vs {b.shape}")
    weights = np.array([0.299, 0.587, 0.114]) if a.ndim == 3 else np.array([1.0])
    ax = -1 if a.ndim == 3 else None
    x = np.tensordot(a, weights, axes=([ax], [0])) if a.ndim == 3 else a
    y = np.tensordot(b, weights, axes=([ax], [0])) if b.ndim == 3 else b

    k1, k2 = 0.01, 0.03
    c1, c2 = (k1 * peak) ** 2, (k2 * peak) ** 2
    mu_x, mu_y = _box_filter(x, radius), _box_filter(y, radius)
    xx, yy, xy = _box_filter(x * x, radius), _box_filter(y * y, radius), _box_filter(x * y, radius)
    var_x = xx - mu_x * mu_x
    var_y = yy - mu_y * mu_y
    cov = xy - mu_x * mu_y
    numerator = (2 * mu_x * mu_y + c1) * (2 * cov + c2)
    denominator = (mu_x ** 2 + mu_y ** 2 + c1) * (var_x + var_y + c2)
    return float(np.mean(numerator / denominator))


def compare(path_a: str, path_b: str, tolerance: int = 0, metrics: bool = True) -> Diff:
    """Per-pixel comparison of two images; ``tolerance`` is a max channel delta.

    ``differing`` counts pixels whose largest channel delta exceeds ``tolerance``;
    ``mean_abs_diff`` and ``max_diff`` always describe *all* pixels, so they stay
    meaningful at any tolerance.
    """
    a = ffkit.decode(path_a)
    b = ffkit.decode(path_b)
    geometry = f"{a.shape[1]}x{a.shape[0]}x{a.shape[2]} vs {b.shape[1]}x{b.shape[0]}x{b.shape[2]}"
    if a.shape != b.shape:
        return Diff(False, int(a.shape[0] * a.shape[1]), int(a.shape[0] * a.shape[1]), 100.0,
                    255.0, 255, 0.0, 0.0, geometry, f"geometry differs ({geometry})")
    ai, bi = a.astype(np.int16), b.astype(np.int16)
    delta = np.abs(ai - bi)
    per_pixel = delta.max(axis=2) if delta.ndim == 3 else delta
    differing = int(np.count_nonzero(per_pixel > tolerance))
    total = int(per_pixel.size)
    mean_abs = float(delta.mean())
    max_diff = int(delta.max())
    p = psnr(a, b) if metrics else 0.0
    s = ssim(a, b) if metrics else 0.0
    pct = 100.0 * differing / total if total else 0.0
    same = differing == 0
    if same:
        detail = f"identical pixels ({total} compared, tolerance {tolerance})"
    else:
        detail = (f"{differing}/{total} pixels differ ({pct:.2f}%), "
                  f"mean_abs_diff {mean_abs:.3f}, max_diff {max_diff}, "
                  f"psnr {p:.2f} dB, ssim {s:.4f}")
    return Diff(same, differing, total, pct, mean_abs, max_diff, p, s, geometry, detail)


def pixels_equal(path_a: str, path_b: str, tolerance: int = 0) -> tuple[bool, str]:
    """``(same, human detail)`` -- the criterion to use for reproducibility."""
    try:
        d = compare(path_a, path_b, tolerance)
    except (OSError, ffkit.ToolError, ValueError) as exc:
        return False, f"cannot compare: {exc}"
    return d.same, d.detail


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("a", help="first image")
    ap.add_argument("b", help="second image")
    ap.add_argument("--tolerance", type=int, default=0,
                    help="max per-channel delta still counted as identical (default 0)")
    ap.add_argument("--no-metrics", action="store_true", help="skip PSNR/SSIM (faster)")
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    ap.add_argument("--quiet", action="store_true", help="print nothing; use the exit code")
    args = ap.parse_args(argv)

    try:
        diff = compare(args.a, args.b, args.tolerance, metrics=not args.no_metrics)
    except (OSError, ffkit.ToolError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not args.quiet:
        if args.json:
            payload = diff.as_dict()
            payload["a"], payload["b"] = args.a, args.b
            payload["chunks_a"] = ffkit.png_chunks(args.a)
            payload["chunks_b"] = ffkit.png_chunks(args.b)
            payload["bytes_identical"] = open(args.a, "rb").read() == open(args.b, "rb").read()
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            bytes_same = open(args.a, "rb").read() == open(args.b, "rb").read()
            print(f"a: {args.a}")
            print(f"b: {args.b}")
            print(f"geometry: {diff.geometry}")
            print(f"file bytes: {'identical' if bytes_same else 'DIFFERENT'}"
                  f" (chunks: {','.join(ffkit.png_chunks(args.a)) or 'n/a'})")
            print(f"{'SAME' if diff.same else 'DIFFERENT'}: {diff.detail}")
    return 0 if diff.same else 1


if __name__ == "__main__":
    sys.exit(main())
