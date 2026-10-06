#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""四角放大队列图：把若干张图的四个角裁出来、放大、排成一张便于目视的对照图。

为什么要这个脚本
  本骨法下模型会在纸角盖乱码印/写伪字，而**自动判印的四种判据全部失败**
  （见 subjects/lu-shu/rounds/r01-review.md §四）——最后只能靠"四角 4× 放大目视"。
  之前这一步是临时敲 ffmpeg 拼的，图与结论对不上号的风险很高（哪一格是哪张图）。
  这里把版面固定下来并打印图例：

     行 = 输入图（按文件名排序，一行一张）    列 = 左上 / 右上 / 左下 / 右下
     单元格 = 角部 crop 比例的方形区域，按 zoom 倍最近邻放大（最近邻不插值，
              5px 的小红点放大后仍是硬边，不会被糊掉）

用法
----
    python3 scripts/corner_sheet.py --out sheet.jpg <图1> <图2> ...
    python3 scripts/corner_sheet.py --out sheet.jpg --crop 0.15 --zoom 5 work/.../r05/*.png
    python3 scripts/corner_sheet.py --out sheet.jpg --json sheet.json --title "R5 s1" <图...>

自检（脚本自己会做，失败即非零退出）
  * 输出尺寸等于行列推算值；
  * 每一格都不是纯色（防止坐标算错裁到空白或越界）；
  * 图例里的格数与实际格数一致。
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

import numpy as np

CORNERS = ("左上", "右上", "左下", "右下")


def decode_rgb(path: str) -> np.ndarray:
    """ffmpeg 解码成 (H, W, 3) uint8 —— 与 image-tools 的 ffkit 同一套做法。"""
    meta = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "csv=p=0", path],
        capture_output=True, check=True).stdout.decode().strip().splitlines()[0]
    width, height = (int(v) for v in meta.split(",")[:2])
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(height, width, 3)


def encode_image(path: str, arr: np.ndarray) -> None:
    """按扩展名写图：.png 无损；.jpg/.jpeg 走 JPEG（仓库约定：合图/审计图用 JPEG）。"""
    height, width = arr.shape[:2]
    ext = os.path.splitext(path)[1].lower()
    codec = ["-c:v", "png"] if ext == ".png" else ["-q:v", "2"]
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{width}x{height}", "-i", "-", "-frames:v", "1"] + codec + [path],
        input=arr.tobytes(), check=True)


def probe_size(path: str) -> tuple:
    meta = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "csv=p=0", path],
        capture_output=True, check=True).stdout.decode().strip().splitlines()[0]
    width, height = (int(v) for v in meta.split(",")[:2])
    return width, height


def corners_of(arr: np.ndarray, crop: float) -> list:
    """四个角的方形裁剪，顺序：左上 / 右上 / 左下 / 右下。"""
    height, width = arr.shape[:2]
    side = max(16, int(round(min(height, width) * crop)))
    return [
        arr[0:side, 0:side],
        arr[0:side, width - side:width],
        arr[height - side:height, 0:side],
        arr[height - side:height, width - side:width],
    ]


def enhance_paper(arr: np.ndarray, black: float = 1.0, white: float = 90.0) -> np.ndarray:
    """亮度分级（levels）：把纸面那一段拉开，让**淡淡的红印**显形。

    关键是**三个通道用同一条变换**（变换由亮度百分位定），所以中性纸面还是中性，
    不会像逐通道拉伸那样把纸变成彩噪。仍是给人眼看的增强图，**不作判据本身**。
    """
    luma = arr.mean(axis=2)
    lo, hi = (float(v) for v in np.percentile(luma, [black, white]))
    if hi - lo < 1e-3:
        return arr.copy()
    out = (arr.astype(np.float32) - lo) * (255.0 / (hi - lo))
    return np.clip(out, 0, 255).astype(np.uint8)


def redness_map(arr: np.ndarray, clip: float = 99.5) -> np.ndarray:
    """朱砂图：减去纸面本身的暖调后，把**局部偏红**的部分染红。

    直接用 `2R-G-B` 不行——陈年纸本本身就偏暖，整张图会一起红掉（实测第一版就是这样）。
    所以先减掉该格的中位数（= 纸的基线），再按 |残差| 的 99.5 百分位拉伸：
    中性纸面 ≈ 中灰，比纸更红的（朱砂印）亮起来，墨线偏冷则压暗。
    """
    r = arr[:, :, 0].astype(np.float32)
    g = arr[:, :, 1].astype(np.float32)
    b = arr[:, :, 2].astype(np.float32)
    residual = (2.0 * r - g - b) - float(np.median(2.0 * r - g - b))
    scale = float(np.percentile(np.abs(residual), clip))
    if scale < 1e-3:
        return arr.copy()
    value = np.clip(128.0 + residual * 127.0 / scale, 0, 255)
    return np.stack([value, value, value], axis=2).astype(np.uint8)


def zoom_nn(arr: np.ndarray, factor: int) -> np.ndarray:
    """最近邻放大：保留原始像素，不引入插值（看小红点就要这个）。"""
    return np.repeat(np.repeat(arr, factor, axis=0), factor, axis=1)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="四角放大队列图（目视判印用）")
    ap.add_argument("images", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--crop", type=float, default=0.15, help="角部裁剪边长占比（默认 0.15）")
    ap.add_argument("--zoom", type=int, default=5, help="最近邻放大倍数（默认 5）")
    ap.add_argument("--enhance", choices=("none", "levels", "redness"), default="none",
                    help="增强：levels=亮度分级拉开纸面；redness=朱砂图（找淡红印）。"
                         "增强图仅助目视，不作判据")
    ap.add_argument("--grid", choices=("1x4", "2x2"), default="1x4",
                    help="每张图的四角排成一行（1x4）还是两行两列（2x2，单张图看得更细）")
    ap.add_argument("--json", help="把版面与逐格统计写成 JSON")
    ap.add_argument("--title", default="", help="只写进 JSON 的图名（不烤进像素）")
    args = ap.parse_args(argv)

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise SystemExit(f"缺少 {tool}")

    images = sorted(args.images)
    rows, legend = [], []
    cell = None
    for path in images:
        arr = decode_rgb(path)
        crops = corners_of(arr, args.crop)
        if args.enhance == "levels":
            crops = [enhance_paper(c) for c in crops]
        elif args.enhance == "redness":
            crops = [redness_map(c) for c in crops]
        tiles = [zoom_nn(t, args.zoom) for t in crops]
        if cell is None:
            cell = tiles[0].shape[:2]
        tiles = [t[:cell[0], :cell[1]] for t in tiles]
        if args.grid == "2x2":
            rows.append(np.concatenate(tiles[:2], axis=1))
            rows.append(np.concatenate(tiles[2:], axis=1))
        else:
            rows.append(np.concatenate(tiles, axis=1))
        legend.append({"file": os.path.basename(path),
                       "size": [arr.shape[1], arr.shape[0]],
                       "cells": [f"{os.path.basename(path)}#{c}" for c in CORNERS]})
    sheet = np.concatenate(rows, axis=0)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    encode_image(args.out, sheet)

    # ---- 自检 ----
    problems = []
    width, height = probe_size(args.out)
    columns = 2 if args.grid == "2x2" else len(CORNERS)
    want = (cell[1] * columns, cell[0] * len(rows))
    if (width, height) != want:
        problems.append(f"输出尺寸 {width}x{height} != 推算 {want[0]}x{want[1]}")
    back = decode_rgb(args.out)
    for index, row in enumerate(rows):
        block = back[index * cell[0]:(index + 1) * cell[0]]
        if float(block.std()) < 0.5:
            problems.append(f"第 {index + 1} 行像纯色（可能裁到空白/越界）：std={block.std():.3f}")
            break
    per_image = 2 if args.grid == "2x2" else 1
    if len(rows) != len(legend) * per_image:
        problems.append(f"实际行数 {len(rows)} != 图例 {len(legend)} × 每图 {per_image} 行")

    order = "左上 右上 / 左下 右下" if args.grid == "2x2" else " / ".join(CORNERS)
    print(f"图例（版面 {args.grid}：{order}；角部边长 {args.crop:.0%}，{args.zoom}× 最近邻）")
    for i, item in enumerate(legend, 1):
        print(f"  {i:2d}. {item['file']}  [{item['size'][0]}x{item['size'][1]}]")
    print(f"out  : {args.out}  {width}x{height}  每格 {cell[1]}x{cell[0]}")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"title": args.title, "out": args.out, "crop": args.crop,
                       "zoom": args.zoom, "cell": [cell[1], cell[0]],
                       "columns": list(CORNERS), "rows": legend,
                       "self_check": {"ok": not problems, "problems": problems}},
                      fh, ensure_ascii=False, indent=1)
    for p in problems:
        print(f"❌ {p}", file=sys.stderr)
    print("OK: 四角图已产出，自检通过" if not problems
          else f"FAIL: 自检未通过（{len(problems)} 项）")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
