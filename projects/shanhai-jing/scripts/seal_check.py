#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""印面自检：模型有没有自作主张盖（乱码）印。

为什么需要它
  项目铁律之一是"字不由模型写"——榜题、原文、印章都由工具叠真字。但 Z-Image 在
  「册页淡彩陈年纸本」这类骨法下**会自发在四角盖红色印章**，而且印文全是乱码
  （探针期实测、R1 的 v2-202 四角又各中一枚）。肉眼在缩略图上分不清"淡淡的红印"
  和"纸底噪点"，所以判据要机械化：**数红色像素簇**。

判据（可复核，但不假装能自动定性）
  1. 朱砂像素：R 明显高于 G/B（R-G ≥ 60 且 R-B ≥ 40 且 R ≥ 130）——比做旧纸、赭石暖调更红
  2. 只报**外缘环带**内的簇（默认 band=0.20）：主体与赤尾在中间，落进环带的多是角落小玩意儿
  3. 尺寸/形状像印面的（100–8000 px、近似方形）列为 `seals`（**候选**）；
     更大或长条的列为 `red_objects`（多半是兽自身的赤色部位，如赤尾）
  4. 每个候选自动裁图放大存档 → **必须目视确认**才算判"乱码印"

  ⚠️ 为什么判据停在这里：试过用"周边纸面占比"和"环带墨占比"自动定性，**都失败了**——
     印面若挨着地面墨线，环带墨占比反而更高（v2-202 实测 0.48）；而兽身的赭红部位
     周边也可能全是纸（R7 九尾狐实测 0）。这两条路都写在 R1/R2 的 review 里。
     所以本脚本只做**机械筛 + 裁图**，定性交给人眼（与"目视点数，非机械确证"同一套纪律）。

退出码：0 = 环带内没有朱砂簇（CLEAN）；1 = 有候选，必须目视确认（REVIEW）；2 = 用法错误。

用法
----
    python3 scripts/seal_check.py work/.../r01/*.png
    python3 scripts/seal_check.py --json out.json img.png
    python3 scripts/seal_check.py --crop-dir work/.../seals img.png
"""

import argparse
import json
import os
import subprocess
import sys

import numpy as np

DEFAULT_BAND = 0.20
DEFAULT_MIN_PX = 100          # 印面最小像素簇
DEFAULT_MAX_PX = 8000         # 超过这个尺寸的多半是兽自身的赤色部位（如赤尾），另列 red_objects
ASPECT = (0.6, 1.7)           # 印面近似方形


def decode_rgb(path: str):
    """ffmpeg 解码成 HxWx3 uint8（无 Pillow 依赖，与其它项目脚本一致）。"""
    probe = subprocess.run(
        [ffmpeg_exe(), "-v", "info", "-i", path, "-frames:v", "1", "-f", "null", "-"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    import re
    m = re.search(r"(\d{2,5})x(\d{2,5})", probe.stdout)
    if not m:
        raise SystemExit(f"读不出尺寸：{path}")
    w, h = int(m.group(1)), int(m.group(2))
    raw = subprocess.run(
        [ffmpeg_exe(), "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        check=True, stdout=subprocess.PIPE).stdout
    if len(raw) < w * h * 3:
        raise SystemExit(f"解码不完整：{path}")
    return np.frombuffer(raw[:w * h * 3], dtype=np.uint8).reshape(h, w, 3), w, h


def ffmpeg_exe() -> str:
    import shutil
    exe = shutil.which("ffmpeg")
    if not exe:
        raise SystemExit("找不到 ffmpeg")
    return exe


def clusters(mask: np.ndarray, min_px: int) -> list:
    """连通域（4 邻域，迭代式 flood fill）→ [(area, x0, y0, x1, y1)]。"""
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    out = []
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]:
            continue
        stack = [(y0, x0)]
        seen[y0, x0] = True
        area = 0
        ymin = ymax = y0
        xmin = xmax = x0
        while stack:
            y, x = stack.pop()
            area += 1
            ymin, ymax = min(ymin, y), max(ymax, y)
            xmin, xmax = min(xmin, x), max(xmax, x)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    stack.append((ny, nx))
        if area >= min_px:
            out.append((int(area), int(xmin), int(ymin), int(xmax), int(ymax)))
    return sorted(out, reverse=True)


def cinnabar(arr) -> np.ndarray:
    """朱砂红掩膜：比纸底的暖色（赭石/做旧纸）明显更红。"""
    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)
    return (r - g >= 60) & (r - b >= 40) & (r >= 130)


def check(path: str, band: float, min_px: int, crop_dir: str | None) -> dict:
    arr, w, h = decode_rgb(path)
    r = arr[:, :, 0].astype(np.int16)
    red = cinnabar(arr)
    band_mask = np.zeros_like(red)
    bx, by = int(w * band), int(h * band)
    band_mask[:, :bx] = True
    band_mask[:, w - bx:] = True
    band_mask[:by, :] = True
    band_mask[h - by:, :] = True
    raw = clusters(red & band_mask, min_px)
    found, big = [], []
    for area, x0, y0, x1, y1 in raw:
        bw, bh = x1 - x0 + 1, y1 - y0 + 1
        if area > DEFAULT_MAX_PX or not (ASPECT[0] <= bw / bh <= ASPECT[1]):
            big.append((area, x0, y0, x1, y1))      # 兽自身的赤色部位（赤尾等）
        else:
            found.append((area, x0, y0, x1, y1))
    crops = []
    if crop_dir and (found or big):
        os.makedirs(crop_dir, exist_ok=True)
        for i, (area, x0, y0, x1, y1) in enumerate(found + big):
            pad = 24
            cw, ch = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
            cx, cy = max(0, x0 - pad), max(0, y0 - pad)
            cw, ch = min(cw, w - cx), min(ch, h - cy)
            dst = os.path.join(crop_dir, f"{os.path.splitext(os.path.basename(path))[0]}"
                                         f"-seal{i + 1}.png")
            subprocess.run([ffmpeg_exe(), "-v", "error", "-y", "-i", path, "-vf",
                            f"crop={cw}:{ch}:{cx}:{cy},scale={cw * 3}:{ch * 3}:flags=neighbor",
                            dst], check=True)
            crops.append(dst)
    return {"file": os.path.relpath(path), "size": [w, h],
            "cinnabar_px": int(red.sum()),
            "band_cinnabar_px": int((red & band_mask).sum()),
            "seals": [{"area": a, "bbox": [x0, y0, x1, y1]} for a, x0, y0, x1, y1 in found],
            "red_objects": [{"area": a, "bbox": [x0, y0, x1, y1]} for a, x0, y0, x1, y1 in big],
            "verdict": "REVIEW" if found else "CLEAN", "crops": crops}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="印面自检：环带内有没有模型盖的乱码红印")
    ap.add_argument("images", nargs="+")
    ap.add_argument("--band", type=float, default=DEFAULT_BAND,
                    help=f"外缘环带宽度占比（默认 {DEFAULT_BAND}）")
    ap.add_argument("--min-px", type=int, default=DEFAULT_MIN_PX,
                    help=f"算作候选的最小像素簇（默认 {DEFAULT_MIN_PX}）")
    ap.add_argument("--crop-dir", help="把检出的印面裁图放大存到这里")
    ap.add_argument("--json", help="把完整结果写成 JSON")
    args = ap.parse_args(argv)

    results = [check(p, args.band, args.min_px, args.crop_dir) for p in args.images]
    for r in results:
        marks = "、".join(f"{s['area']}px@{s['bbox'][:2]}" for s in r["seals"]) or "无"
        big = "、".join(f"{s['area']}px@{s['bbox'][:2]}" for s in r["red_objects"]) or "无"
        print(f"{r['verdict']:6s} {r['file']}")
        print(f"       印面候选 {len(r['seals'])} 枚（{marks}）｜兽身赤色部位 {len(r['red_objects'])} 处（{big}）"
              f"｜全图朱砂像素 {r['cinnabar_px']}")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(results, fh, ensure_ascii=False, indent=1)
        print(f"→ {args.json}")
    return 1 if any(r["verdict"] == "REVIEW" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
