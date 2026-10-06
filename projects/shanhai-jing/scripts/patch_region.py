#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""工具擦除：把模型自作主张盖的乱码印 / 写的伪字从纸面上抹掉。

为什么要有这一步
  项目铁律是"字不由模型写"（榜题/原文/印章都由 `typeset_zanzhi.py` 叠真字）。实测下来
  Z-Image-Turbo 在「册页淡彩陈年纸本」骨法下**几乎每张都会在四角盖乱码印、写伪字**
  （鹿蜀 R1 8/9、R2 英文组 6/6，连已交付的九尾狐 R7 定稿也有淡淡的红印）。
  R3 试过用 prompt 抑制（"no seal, no stamp, no writing"），**无效**——与 R5 的教训一致：
  给模型下"不要画什么"的指令基本不执行。

  所以这一步和"叠字"是一对：**模型不许写字，工具负责把它写的擦掉**。

做法（确定性、可复核）
  1. 印面位置**由人指定**（`--box x,y,w,h`）——自动判别试过三种都失败（见 R2 review §4），
     与其塞一个会误报/漏报的分类器，不如让复核者从放大图里读坐标，工具只负责执行
  2. 用**同一张图**里垂直镜像的纸面区域覆盖该 box（不引入外来素材，纸色纸纹同源）
  3. 边缘 `--feather` 像素线性羽化，避免硬接缝
  4. 自检（不通过就拒绝产出）：
     * 朱砂像素（R-G ≥ 25）在该 box 内的数量必须降到原来的 ≤5%
     * 接缝梯度：box 内侧一圈与外侧一圈的亮度差中位数不得 > `--max-seam`

用法
----
    python3 scripts/patch_region.py --image in.png --out out.png \
        --box 11,1276,30,34 --box 760,1190,140,60 --report out.json
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

import numpy as np

DEFAULT_FEATHER = 16
DEFAULT_MAX_SEAM = 30.0


def ffmpeg_exe() -> str:
    exe = shutil.which("ffmpeg")
    if not exe:
        raise SystemExit("找不到 ffmpeg")
    return exe


def decode(path: str):
    probe = subprocess.run(
        [ffmpeg_exe(), "-v", "info", "-i", path, "-frames:v", "1", "-f", "null", "-"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    m = re.search(r"(\d{2,5})x(\d{2,5})", probe.stdout)
    if not m:
        raise SystemExit(f"读不出尺寸：{path}")
    w, h = int(m.group(1)), int(m.group(2))
    raw = subprocess.run(
        [ffmpeg_exe(), "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        check=True, stdout=subprocess.PIPE).stdout
    if len(raw) < w * h * 3:
        raise SystemExit(f"解码不完整：{path}")
    return np.frombuffer(raw[:w * h * 3], dtype=np.uint8).reshape(h, w, 3).copy(), w, h


def encode(arr, out: str) -> None:
    h, w, _ = arr.shape
    subprocess.run([ffmpeg_exe(), "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                    "-s", f"{w}x{h}", "-i", "-", "-frames:v", "1", "-update", "1", out],
                   input=arr.tobytes(), check=True)


def cinnabar_px(arr, box, inset: int = 0) -> int:
    x, y, bw, bh = box
    x, y, bw, bh = x + inset, y + inset, max(1, bw - 2 * inset), max(1, bh - 2 * inset)
    sub = arr[y:y + bh, x:x + bw].astype(np.int16)
    return int(((sub[:, :, 0] - sub[:, :, 1] >= 25) &
                (sub[:, :, 0] - sub[:, :, 2] >= 20) &
                (sub[:, :, 0] >= 120)).sum())


def luma(arr) -> np.ndarray:
    a = arr.astype(np.int32)
    if a.ndim == 2:                 # 单行/单列切片
        return a
    return (a[:, :, 0] * 299 + a[:, :, 1] * 587 + a[:, :, 2] * 114) // 1000


def seam_delta(arr, box) -> float:
    """接缝：box 边界"内外相邻像素"的亮度差中位数。

    不要用"内侧中位数 vs 外侧环带中位数"——box 紧贴墨石时，外侧环带本身就很暗，
    那样量到的是画面原有的明暗过渡（实测 BL box 因此误报 49），不是补丁留下的缝。
    """
    x, y, bw, bh = box
    L = luma(arr)
    diffs = []
    if y - 1 >= 0:
        diffs.append(np.abs(L[y, x:x + bw] - L[y - 1, x:x + bw]))
    if y + bh < L.shape[0]:
        diffs.append(np.abs(L[y + bh - 1, x:x + bw] - L[y + bh, x:x + bw]))
    if x - 1 >= 0:
        diffs.append(np.abs(L[y:y + bh, x] - L[y:y + bh, x - 1]))
    if x + bw < L.shape[1]:
        diffs.append(np.abs(L[y:y + bh, x + bw - 1] - L[y:y + bh, x + bw]))
    if not diffs:
        return 0.0
    return float(np.median(np.concatenate(diffs)))


def find_source(arr, box, node_ink: int = 150, step: int = 12, reach: int = 6):
    """就近找一块"干净纸"：同高度左右优先，再上下；打分 = 红 + 墨 + 亮度偏差。

    垂直镜像看着优雅，实测会把上方偏亮的纸贴到下方带灰绿罩染的地面带上，
    接缝亮度差 >30（R2 首次试跑即被自检拦下）。
    """
    x, y, bw, bh = box
    h, w, _ = arr.shape
    # 目标色调取 box **外侧一圈**（box 自身被印面污染，不能当基准）
    ring_rows = []
    for yy in range(max(0, y - 4), y):
        ring_rows.append(luma(arr[yy, x:x + bw]))
    for yy in range(y + bh, min(h, y + bh + 4)):
        ring_rows.append(luma(arr[yy, x:x + bw]))
    ring = np.concatenate(ring_rows) if ring_rows else luma(arr[y:y + bh, x:x + bw])
    target_luma = float(np.median(ring))

    best, best_score = None, None
    for k in range(1, reach + 1):
        for sx, sy in ((x + k * (bw + step), y), (x - k * (bw + step), y),
                       (x, y + k * (bh + step)), (x, y - k * (bh + step)),
                       (x + k * (bw + step), y + k * (bh + step)),
                       (x - k * (bw + step), y - k * (bh + step))):
            if sx < 0 or sy < 0 or sx + bw > w or sy + bh > h:
                continue
            cand = arr[sy:sy + bh, sx:sx + bw]
            red = cinnabar_px(arr, (sx, sy, bw, bh))
            ink = int((luma(cand) < node_ink).sum())
            dl = abs(float(np.median(luma(cand))) - target_luma)
            score = red * 10 + ink + dl * 4          # 色调对不上 = 会留一条亮/暗接缝
            if best_score is None or score < best_score:
                best, best_score = (sx, sy), score
    return best


def patch(arr, box, feather: int, source=None):
    """用同图内一块干净纸覆盖 box，边缘线性羽化。"""
    x, y, bw, bh = box
    if source is None:
        return arr, None
    sx, sy = source
    src = arr[sy:sy + bh, sx:sx + bw].astype(np.float32)
    dst = arr[y:y + bh, x:x + bw].astype(np.float32)
    fy = min(feather, bh // 2)
    fx = min(feather, bw // 2)
    alpha = np.ones((bh, bw), dtype=np.float32)
    for i in range(fy):                           # 上下渐变
        alpha[i, :] = np.minimum(alpha[i, :], i / max(1, fy))
        alpha[bh - 1 - i, :] = np.minimum(alpha[bh - 1 - i, :], i / max(1, fy))
    for j in range(fx):                           # 左右渐变
        alpha[:, j] = np.minimum(alpha[:, j], j / max(1, fx))
        alpha[:, bw - 1 - j] = np.minimum(alpha[:, bw - 1 - j], j / max(1, fx))
    arr[y:y + bh, x:x + bw] = (src * alpha[:, :, None] + dst * (1 - alpha[:, :, None])).astype(np.uint8)
    return arr, (sx, sy)


def parse_box(text: str):
    parts = [int(v) for v in text.replace(" ", "").split(",")]
    if len(parts) != 4:
        raise SystemExit(f"--box 需要 x,y,w,h 四个整数，收到 {text!r}")
    return tuple(parts)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="工具擦除模型盖的乱码印/伪字（确定性，可复核）")
    ap.add_argument("--image", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--box", action="append", required=True, metavar="x,y,w,h")
    ap.add_argument("--feather", type=int, default=DEFAULT_FEATHER)
    ap.add_argument("--max-seam", type=float, default=DEFAULT_MAX_SEAM)
    ap.add_argument("--report", help="把结果写成 JSON")
    args = ap.parse_args(argv)

    arr, w, h = decode(args.image)
    boxes = [parse_box(b) for b in args.box]
    report = {"image": os.path.relpath(args.image), "size": [w, h], "feather": args.feather,
              "boxes": [], "verdict": "OK"}
    work = arr.copy()
    for box in boxes:
        x, y, bw, bh = box
        if x < 0 or y < 0 or x + bw > w or y + bh > h:
            raise SystemExit(f"box {box} 超出图像范围 {w}x{h}")
        before = cinnabar_px(arr, box)
        source = find_source(work, box)
        if source is None:
            raise SystemExit(f"box {box} 周围找不到可用的干净纸面")
        work, used = patch(work, box, args.feather, source)
        after = cinnabar_px(work, box, inset=args.feather)
        seam = seam_delta(work, box)
        ok = after <= max(1, int(before * 0.05))
        report["boxes"].append({"box": list(box), "source": list(used) if used else None,
                                "cinnabar_before": before, "cinnabar_after": after,
                                "seam_luma_delta": round(seam, 2), "removed": ok})
        if not ok:
            report["verdict"] = "FAIL"
        if seam > args.max_seam:
            report["verdict"] = "FAIL"
            report["boxes"][-1]["note"] = f"接缝偏亮（>{args.max_seam}）：羽化不够或源纸面不干净"
    if report["verdict"] != "OK":
        print("自检未通过，拒绝写出成品：", file=sys.stderr)
        print(json.dumps(report, ensure_ascii=False, indent=1), file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    encode(work, args.out)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
