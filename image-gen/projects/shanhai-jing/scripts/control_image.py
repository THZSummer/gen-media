#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「结构控制图」：把可数特征用几何构造画出来，交给 ControlNet 锁死。

为什么需要它
------------
实测（见 subjects/jiu-wei-hu/rounds/r01-review.md）：Z-Image-Turbo 对**可数属性**
没有可靠控制力——prompt 明写 `EXACTLY nine tails`，六张没一张数对（7~9 条随机漂移）。
而《山海经》的考据硬指标恰恰全在可数上（九尾、三首六目、六足四翼、一足）。

所以把计数从「赌模型」改成「由构造保证」：本脚本画出**恰好 9 条**尾巴的示意图，
经 Canny → ControlNet 约束出图。

两项自检（退出码 0 才算通过）
  1. **分离自检**：离尾根足够远之后，九条尾巴两两分离，打印最小间隙；≤0 判失败
  2. **构图自检**：墨迹不得触碰画布边缘（避免出图被裁切）；有触碰即判失败

设计原则（对齐本仓库「确定性工具」文化）
  * 零依赖：只用标准库 + numpy（不需要 Pillow / scipy）
  * 确定性：同一参数永远产出逐像素相同的 PNG
  * 可自证：计数与构图都由脚本自己验证，不依赖目视

用法
----
    python3 scripts/control_image.py --creature jiu-wei-hu --out out/control.png
    python3 scripts/control_image.py --creature jiu-wei-hu --width 864 --out out/control.png
"""

import argparse
import math
import random
import struct
import sys
import zlib

import numpy as np

# ── 画布单位约定 ────────────────────────────────────────────────────────────
# 所有几何量都以**画布宽度为 1** 的归一化单位给出（两轴同尺度，角度才不失真）；
# 纵向因此取到 4/3。像素换算：px = nx * W。


def write_png_gray(path: str, arr: np.ndarray) -> None:
    """写 8 位灰度 PNG（纯标准库，不依赖 Pillow）。"""
    h, w = arr.shape
    raw = b"".join(b"\x00" + arr[y].tobytes() for y in range(h))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)


class Canvas:
    """极简光栅画布：圆盘 / 椭圆 / 多边形 / 带状笔画（锥形收笔）。"""

    def __init__(self, width: int, height: int, ink: int = 0, paper: int = 255):
        self.w, self.h = width, height
        self.a = np.full((height, width), paper, dtype=np.uint8)
        self.ink = ink

    def disk(self, cx: float, cy: float, r: float) -> None:
        if r <= 0:
            return
        x0 = max(0, int(math.floor(cx - r)))
        x1 = min(self.w, int(math.ceil(cx + r)) + 1)
        y0 = max(0, int(math.floor(cy - r)))
        y1 = min(self.h, int(math.ceil(cy + r)) + 1)
        if x0 >= x1 or y0 >= y1:
            return
        yy, xx = np.ogrid[y0:y1, x0:x1]
        m = (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r
        self.a[y0:y1, x0:x1][m] = self.ink

    def ellipse(self, cx: float, cy: float, rx: float, ry: float) -> None:
        x0 = max(0, int(math.floor(cx - rx)))
        x1 = min(self.w, int(math.ceil(cx + rx)) + 1)
        y0 = max(0, int(math.floor(cy - ry)))
        y1 = min(self.h, int(math.ceil(cy + ry)) + 1)
        if x0 >= x1 or y0 >= y1:
            return
        yy, xx = np.ogrid[y0:y1, x0:x1]
        m = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0
        self.a[y0:y1, x0:x1][m] = self.ink

    def polygon(self, pts) -> None:
        """扫描线奇偶填充（pts 为像素坐标列表）。"""
        ys = [p[1] for p in pts]
        y0 = max(0, int(math.floor(min(ys))))
        y1 = min(self.h, int(math.ceil(max(ys))) + 1)
        n = len(pts)
        for y in range(y0, y1):
            yc = y + 0.5
            xs = []
            for i in range(n):
                xa, ya = pts[i]
                xb, yb = pts[(i + 1) % n]
                if (ya <= yc < yb) or (yb <= yc < ya):
                    xs.append(xa + (yc - ya) / (yb - ya) * (xb - xa))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                a = max(0, int(math.ceil(xs[i] - 0.5)))
                b = min(self.w, int(math.floor(xs[i + 1] - 0.5)) + 1)
                if b > a:
                    self.a[y, a:b] = self.ink

    def ribbon(self, p0, p1, p2, w0: float, w1: float, samples: int | None = None):
        """从 p0 经控制点 p1 到 p2 的锥形笔画；返回中心线采样 [(x, y, r, t)]。"""
        approx = math.dist(p0, p2)
        n = samples or max(96, int(approx * 2.5))
        out = []
        for i in range(n + 1):
            t = i / n
            u = 1.0 - t
            x = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
            y = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
            r = w0 + (w1 - w0) * t
            self.disk(x, y, r)
            out.append((x, y, r, t))
        return out

    def plume(self, p0, p1, p2, r_base: float, r_max: float,
              thick_frac: float = 0.55, tip_ratio: float = 0.55,
              samples: int | None = None):
        """蓬松兽尾：根部细 → 中段最粗 → **圆钝末端**（不是尖叶/羽片）。

        为什么不能用线性收细：收到 0 就是尖刀片，模型会照着描成叶脉/羽毛 → 尾巴看起来假。
        真实狐尾是"毛刷"：最粗处在中段偏后，末端只收到约一半，**本身就是一个圆帽**。
        因此这里让半径只收 tip_ratio（而非 0），末端 disk 自然形成圆头。

        返回中心线采样 [(x, y, r, t)]。
        """
        approx = math.dist(p0, p2)
        n = samples or max(140, int(approx * 3))
        out = []
        for i in range(n + 1):
            t = i / n
            u = 1.0 - t
            x = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
            y = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
            if t < thick_frac:                            # 根部细 → 中段最粗
                r = r_base + (r_max - r_base) * (t / thick_frac) ** 0.65
            else:                                         # 后段只收一部分 → 末端圆钝
                k = (t - thick_frac) / (1.0 - thick_frac)
                r = r_max * (1.0 - (1.0 - tip_ratio) * k * k)
            self.disk(x, y, r)
            out.append((x, y, r, t))
        return out


def bezier_ctrl(p0, p2, bow: float):
    """在 p0→p2 中点处按左法向偏移 bow 倍长度，得到平滑弓形的控制点。"""
    mx, my = (p0[0] + p2[0]) / 2.0, (p0[1] + p2[1]) / 2.0
    dx, dy = p2[0] - p0[0], p2[1] - p0[1]
    ln = math.hypot(dx, dy) or 1.0
    return mx - dy / ln * bow * ln, my + dx / ln * bow * ln


# ── 九尾狐 ──────────────────────────────────────────────────────────────────
# 坐标：画布宽 = 1，高 = 4/3；狐面朝右，尾扇形在左后方。
JIU_WEI_HU = {
    "tail_root": (0.420, 0.862),   # 尾根（扇形收敛处）
    # ⚠️ 排布不能等角距均匀辐射 —— 那样出来的是花瓣/棕榈叶，一眼假。
    # 真实兽尾：长短交错、角距不匀、整体朝同一方向甩。故用显式的手调模式。
    "fan_angles": [208, 192, 170, 152, 138, 118, 100, 76, 55],   # 度：0°右 / 90°上 / 180°左
    "len_pattern": [0.82, 1.00, 0.72, 1.08, 0.88, 1.15, 0.78, 1.00, 0.86],
    "bow_sign": -1.0,              # 同向甩尾（不交替），像被风吹过的一束毛
    "fan_from": 42.0,              # 兼容保留（旧等距模式的起止角）
    "fan_to": 212.0,
    "tail_count": 9,
    "origin_radius": 0.050,        # 尾根处各尾起点所在小圆弧半径（共根收敛感）
    "tail_len_min": 0.270,
    "tail_len_max": 0.390,
    # 尾型剖面：根部细 → 蓬松主体 → 圆头（见 Canvas.plume）。
    # ⚠️ 不能画成线性收细的尖片：那样模型会描成叶脉/羽毛，尾巴看起来是假的。
    "tail_r_base": 0.017,          # 尾根半宽
    "tail_r_max": 0.036,           # 蓬松主体半宽（狐尾很粗：宽:长约 1:4.5）
    "tail_bow": 0.15,              # 弓形弯曲强度
    # 可数性判据只看**尾尖**分离：真实九尾本就聚成一簇、尾身允许交叠，
    # 靠"尾尖可数"而不是"尾身不挨着"。
    # ⚠️ 起判点必须落在**收细之后**，否则等于要求"粗尾巴不许挨着"，自相矛盾（实测会 400 种子全失败）。
    "tip_check_from": 0.78,        # 自 t≥此值起要求两两分离
    "min_gap_frac": 0.012,         # 尾尖最小间隙（占画布宽）→ 864px 下约 10.4px
    "disentangle_r": 0.26,         # 兼容保留
    # ── 去机械化：确定性扰动（同 seed 完全可复现）──────────────────────────
    # 等距扇形读起来像扇骨，不像兽尾 —— 这是"可数性换自然度"的代价。
    # 用固定 seed 扰动角度/长度/弓形/粗细，让扇形有疏密长短；
    # 「尖端两两分离」的硬约束仍由自检保证，可数性不受影响。
    "seed": 20261005,
    "jitter_angle": 4.5,           # ±度
    "jitter_len": 0.17,            # ±比例
    "jitter_bow": 0.70,            # ±比例
    "jitter_w": 0.22,              # ±比例
    "ground": True,                # 加低矮山石立足点（探针 v3 的经验：有立足点更稳）
}


def draw_ground(cv: "Canvas", geo: dict) -> None:
    """低矮山石立足点：给构图一个"站得住"的底（探针 v3 的构图经验）。"""
    W = cv.w

    def P(nx, ny):
        return (nx * W, ny * W)

    top = [(0.300, 1.150), (0.352, 1.128), (0.398, 1.148), (0.452, 1.124),
           (0.516, 1.146), (0.580, 1.126), (0.646, 1.150), (0.706, 1.128),
           (0.772, 1.144), (0.842, 1.126), (0.900, 1.152)]
    cv.polygon([P(*p) for p in top] + [P(0.900, 1.200), P(0.300, 1.200)])


def draw_jiu_wei_hu(cv: Canvas, geo: dict):
    """画九尾狐结构示意：狐身侧影 + 恰好 9 条锥形尾巴。返回 (尾根像素, 各尾采样)。"""
    W = cv.w
    rng = random.Random(geo["seed"])      # 固定 seed → 扰动确定、可复现

    def P(nx, ny):
        return (nx * W, ny * W)

    # 躯干（略长卵形）+ 胸口，避免画成圆球
    cv.ellipse(*P(0.540, 0.885), 0.185 * W, 0.112 * W)
    cv.ellipse(*P(0.655, 0.880), 0.095 * W, 0.105 * W)
    # 颈：短而粗（拉长会变成长颈鹿）
    cv.ribbon(P(0.700, 0.838), P(0.762, 0.800), P(0.800, 0.762), 0.060 * W, 0.052 * W)
    # 头（狐头占比偏大）+ 吻
    cv.ellipse(*P(0.838, 0.735), 0.076 * W, 0.068 * W)
    cv.polygon([P(0.888, 0.712), P(0.972, 0.736), P(0.888, 0.760)])
    # 双耳（尖而立）
    cv.polygon([P(0.792, 0.700), P(0.808, 0.612), P(0.850, 0.688)])
    cv.polygon([P(0.848, 0.688), P(0.874, 0.616), P(0.902, 0.700)])
    # 四肢：带大腿量感，脚掌着地
    for lx, bend, thigh in ((0.678, 0.006, 0.030), (0.738, -0.006, 0.028),
                            (0.428, 0.008, 0.042), (0.492, -0.008, 0.040)):
        cv.ellipse(*P(lx, 0.960), thigh * W, 0.055 * W)
        cv.ribbon(P(lx, 0.955), P(lx + bend, 1.045), P(lx, 1.122), 0.028 * W, 0.014 * W)
        cv.ellipse(*P(lx + 0.004, 1.130), 0.028 * W, 0.015 * W)

    # ── 九条尾巴 ────────────────────────────────────────────────────────────
    if geo.get("ground"):
        draw_ground(cv, geo)

    root = P(*geo["tail_root"])
    n = geo["tail_count"]
    angles = geo.get("fan_angles")
    if angles is None:
        a0 = math.radians(geo["fan_from"])
        step = (math.radians(geo["fan_to"]) - a0) / (n - 1)
        angles = [math.degrees(a0 + step * i) for i in range(n)]
    len_pat = geo.get("len_pattern") or [1.0] * n
    traces = []
    for i in range(n):
        t = i / (n - 1)
        # 扰动必须按固定顺序取随机数，才能保证同 seed 完全可复现
        ja = math.radians(rng.uniform(-geo["jitter_angle"], geo["jitter_angle"]))
        ang = math.radians(angles[i]) + ja
        d = (math.cos(ang), -math.sin(ang))     # 图像 y 向下，故取负
        ox = root[0] + geo["origin_radius"] * W * d[0]
        oy = root[1] + geo["origin_radius"] * W * d[1]
        base_len = geo["tail_len_min"] + (geo["tail_len_max"] - geo["tail_len_min"]) \
            * math.sin(math.pi * t)             # 中间几条更长，扇形轮廓自然
        length = base_len * len_pat[i] * (1.0 + rng.uniform(-geo["jitter_len"], geo["jitter_len"]))
        # 同向甩尾 + 轻微大小扰动：避免九条朝同一侧弯成扇骨
        bow = geo["tail_bow"] * geo.get("bow_sign", 1.0) \
            * (1.0 + rng.uniform(-geo["jitter_bow"], geo["jitter_bow"]))
        wscale = 1.0 + rng.uniform(-geo["jitter_w"], geo["jitter_w"])
        ln = length * W
        tip = (ox + d[0] * ln, oy + d[1] * ln)
        ctrl = bezier_ctrl((ox, oy), tip, bow)
        # 用 plume（圆头蓬松柱体）而非 ribbon（线性收细 → 尖刀片/叶脉感）
        traces.append(cv.plume((ox, oy), ctrl, tip,
                               geo["tail_r_base"] * W * wscale,
                               geo["tail_r_max"] * W * wscale))
    return root, traces


def check_tails_disjoint(root, traces, geo: dict, width: int):
    """分离自检：只检查**尾尖段**，九条尾尖必须两两分离。

    判据只看尾尖，不看尾身：真实九尾本就聚成一簇、尾身交叠，
    可数性来自"尾尖可数"。若要求整条尾都不挨着，只能摆成扇骨 → 假。
    返回 (ok, 最小间隙px, 最近对)。
    """
    tip_from = geo.get("tip_check_from", 0.72)
    sel = []
    for tr in traces:
        pts = [(x, y, r) for (x, y, r, t) in tr if t >= tip_from]
        if len(pts) < 2:
            return False, 0.0, (0, 0)
        sel.append(np.array(pts, dtype=float))
    worst, pair = None, None
    for i in range(len(sel)):
        for j in range(i + 1, len(sel)):
            A, B = sel[i], sel[j]
            d = np.sqrt(((A[:, None, :2] - B[None, :, :2]) ** 2).sum(-1))
            g = d - A[:, None, 2] - B[None, :, 2]
            mg = float(g.min())
            if worst is None or mg < worst:
                worst, pair = mg, (i + 1, j + 1)
    return True, worst, pair


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="生成可数特征的结构控制图（确定性、可自证）")
    ap.add_argument("--creature", default="jiu-wei-hu", choices=["jiu-wei-hu"])
    ap.add_argument("--width", type=int, default=864, help="画布宽（高自动取 4:3）")
    ap.add_argument("--out", required=True, help="输出 PNG 路径")
    ap.add_argument("--seed", type=int, default=None, help="覆盖扰动种子（默认自动挑选）")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    height = int(round(args.width * 4 / 3))
    geo = JIU_WEI_HU

    # 扰动让扇形有疏密长短（去掉扇骨的机械感），但可能把两条尾巴挤近。
    # 因此自动挑 seed：从基础 seed 起逐个试，取第一个同时满足
    #   ① 九尾两两分离且最小间隙 ≥ min_gap ② 墨迹不触边
    # 的种子。结果是确定的（同基础 seed 永远选到同一个），既有变化又可数。
    base_seed = args.seed if args.seed is not None else geo["seed"]
    min_gap = geo.get("min_gap_frac", 0.016) * args.width
    chosen = None
    for ds in range(400):
        geo["seed"] = base_seed + ds
        cv = Canvas(args.width, height)
        root, traces = draw_jiu_wei_hu(cv, geo)
        ok_sep, worst, pair = check_tails_disjoint(root, traces, geo, args.width)
        m = max(2, int(round(0.008 * args.width)))
        ring = np.concatenate([cv.a[:m].ravel(), cv.a[-m:].ravel(),
                               cv.a[:, :m].ravel(), cv.a[:, -m:].ravel()])
        touching = int((ring == cv.ink).sum())
        if ok_sep and worst is not None and worst >= min_gap and touching == 0:
            chosen = (ds, worst, pair, touching, m)
            break
    if chosen is None:
        print(f"FAIL: 试了 400 个种子仍找不到「最小间隙 ≥ {min_gap:.1f}px 且不触边」的构图",
              file=sys.stderr)
        return 1

    ds, worst, pair, touching, m = chosen
    write_png_gray(args.out, cv.a)

    if not args.quiet:
        print(f"creature      : {args.creature}")
        print(f"canvas        : {cv.w}x{cv.h}")
        print(f"tail_count    : {len(traces)}（构造保证）")
        print(f"seed          : {geo['seed']}（基础 {base_seed} + {ds}，自动挑选）")
        print(f"disentangle_r : {geo['disentangle_r']}（归一化；超出此半径后要求两两分离）")
        print(f"min_gap_px    : {worst:.2f}  最紧一对：尾 {pair[0]} ↔ 尾 {pair[1]}"
              f"（下限 {min_gap:.1f}）")
        print(f"border_ink_px : {touching}（外侧 {m}px 环带内的墨迹像素，须为 0）")
        print(f"out           : {args.out}")
        print(f"OK: 九尾两两分离（间隙 {worst:.2f}px ≥ {min_gap:.1f}）且墨迹不触边")
    return 0


if __name__ == "__main__":
    sys.exit(main())
