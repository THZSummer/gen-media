#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""图赞制版：把白描画心做成完整的小红书竖版图文（主图 + 原文卡）。

产出两张 1080x1440（3:4）的成品：
  1. **图赞主图** —— 卷次 + 榜题（兽名）+ 画心 + 原文点睛句 + 出處，用于封面/首图
  2. **原文卡**   —— 竖排榜题 + 卷次 + 竖排原文（右起），承载完整考据信息

设计原则
  * **文字由工具叠真字**，绝不由模型生成（见 PLAN.md 两条铁律之一）
  * **纸色从画心采样**，两张卡与画心同底，拼在一起不跳色
  * **画心自动收紧**：用 cropdetect 求内容包围盒，再等比装入面板——
    画心自带大量留白，直接缩放会让主体偏小
  * **排版有自检**：渲染后用 signalstats 检查榜题区与原文区**确实有墨**，
    防止 drawtext 因转义/字面问题静默不画（对齐本仓库"参数必须真生效"的纪律）
  * 内容全部取自 `manifest.json`，不硬编码，可复用到其它条目

用法
----
    python3 scripts/typeset_zanzhi.py --check                    # 只做字面覆盖检查
    python3 scripts/typeset_zanzhi.py                            # 默认用 period-01
    python3 scripts/typeset_zanzhi.py --period-dir <dir>
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)

FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
FONT_REG = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"

W, H = 1080, 1440
INK = "0x1C1A17"
FRAME_OUT = 5
FRAME_IN = 2


def esc(s: str) -> str:
    """drawtext 的 text 值转义（反斜杠 / 单引号 / 冒号 / 百分号）。"""
    return (s.replace("\\", "\\\\").replace("'", "\\'")
             .replace(":", "\\:").replace("%", "\\%"))


def run(cmd, capture=False):
    return subprocess.run(cmd, check=True, text=True,
                          stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.STDOUT if capture else None)


def require_ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if not exe:
        raise SystemExit("找不到 ffmpeg")
    return exe


def sample_paper(ffmpeg: str, art: str, w: int, h: int) -> str:
    """从画心**空白纸区**采样纸色（取右上角一片纯纸，避开主体与暗角）。"""
    sx, sy = int(w * 0.72), int(h * 0.03)
    sw, sh = int(w * 0.24), int(h * 0.07)
    out = subprocess.run(
        [ffmpeg, "-v", "error", "-i", art,
         "-vf", f"crop={sw}:{sh}:{sx}:{sy},scale=1:1", "-frames:v", "1",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        check=True, stdout=subprocess.PIPE).stdout
    if len(out) < 3:
        raise SystemExit("采样纸色失败")
    return "0x%02X%02X%02X" % (out[0], out[1], out[2])


def detect_content_bbox(ffmpeg: str, path: str, size: tuple, thresh: int = 140,
                        min_px: int = 2, pad_frac: float = 0.02):
    """求内容包围盒：解码成灰度 rawvideo 交给 numpy 统计，不依赖 cropdetect。

    画心自带大量留白；不收紧就等比缩放会把主体缩得很小。
    判据是"该行/列至少有 min_px 个暗于 thresh 的像素"，以忽略纸底噪点。
    失败时返回 None（退回整幅），不阻断制版。
    """
    w, h = size
    raw = subprocess.run(
        [ffmpeg, "-v", "error", "-i", path, "-f", "rawvideo",
         "-pix_fmt", "gray", "-"], check=True, stdout=subprocess.PIPE).stdout
    if len(raw) < w * h:
        return None
    arr = np.frombuffer(raw[:w * h], dtype=np.uint8).reshape(h, w)
    mask = arr < thresh
    rows = np.where(mask.sum(axis=1) >= min_px)[0]
    cols = np.where(mask.sum(axis=0) >= min_px)[0]
    if rows.size == 0 or cols.size == 0:
        return None
    py = max(2, int(h * pad_frac))
    px = max(2, int(w * pad_frac))
    y0 = max(0, int(rows[0]) - py)
    y1 = min(h, int(rows[-1]) + 1 + py)
    x0 = max(0, int(cols[0]) - px)
    x1 = min(w, int(cols[-1]) + 1 + px)
    cw, ch = x1 - x0, y1 - y0
    if cw < 32 or ch < 32:
        return None
    return cw, ch, x0, y0


def ink_present(ffmpeg: str, path: str, x: int, y: int, w: int, h: int,
                ymax: float = 120.0) -> tuple:
    """检查指定区域是否真的有墨（signalstats 的 YMIN，不依赖肉眼）。"""
    res = subprocess.run(
        [ffmpeg, "-v", "info", "-i", path,
         "-vf", f"crop={w}:{h}:{x}:{y},signalstats,metadata=print:file=-",
         "-frames:v", "1", "-f", "null", "-"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    m = re.search(r"lavfi\.signalstats\.YMIN=([0-9.]+)", res.stdout)
    if not m:
        raise SystemExit("无法读取 signalstats（自检失败，不产出成品）")
    v = float(m.group(1))
    return v <= ymax, v


def vtext(text, font, size, step, x, y0, color=INK):
    """竖排文本：逐字一个 drawtext，自上而下。"""
    return [f"drawtext=fontfile={font}:text='{esc(ch)}':fontsize={size}"
            f":fontcolor={color}:x={x}:y={y0 + i * step}"
            for i, ch in enumerate(text)]


def htext(text, font, size, y, color=INK, opacity=1.0):
    """横排居中文本。"""
    return (f"drawtext=fontfile={font}:text='{esc(text)}':fontsize={size}"
            f":fontcolor={color}@{opacity}:x=(w-text_w)/2:y={y}")


def split_columns(text, per_col):
    return [text[i:i + per_col] for i in range(0, len(text), per_col)]


def frame_boxes():
    return [
        f"drawbox=x=30:y=30:w={W - 60}:h={H - 60}:color={INK}@1:t={FRAME_OUT}",
        f"drawbox=x=48:y=48:w={W - 96}:h={H - 96}:color={INK}@1:t={FRAME_IN}",
    ]


# 主图面板：**竖版 3:4**，与画心同比例 —— 面板比例不匹配时画心只能按高度缩，
# 两侧空一大片、主体显得很小（实测教训）。比例一致时画心正好填满，也无接缝问题。
PANEL_X, PANEL_Y, PANEL_W, PANEL_H = 180, 240, 720, 960


def build_plate(ffmpeg, paper, art, title, volume, cover_line, origin, out, bbox):
    art_chain = ""
    if bbox:
        cw, ch, cx, cy = bbox
        art_chain = f"crop={cw}:{ch}:{cx}:{cy},"
    art_chain += (f"scale={PANEL_W}:{PANEL_H}:force_original_aspect_ratio=decrease:flags=lanczos,"
                  f"pad={PANEL_W}:{PANEL_H}:(ow-iw)/2:(oh-ih)/2:color={paper}")

    base = [
        *frame_boxes(),
        htext(volume, FONT_REG, 28, 72, INK, 0.8),
        htext(title, FONT_BOLD, 88, 110),
        htext(cover_line, FONT_REG, 42, 1245),
        htext(origin, FONT_REG, 28, 1350, INK, 0.75),
    ]
    fc = (
        f"[1:v]{art_chain}[art];"
        f"[0:v]{','.join(base)}[bg];"
        f"[bg][art]overlay={PANEL_X}:{PANEL_Y}[ov];"
        f"[ov]drawbox=x={PANEL_X - 5}:y={PANEL_Y - 5}:w={PANEL_W + 10}:h={PANEL_H + 10}"
        f":color={INK}@1:t=3[out]"
    )
    run([ffmpeg, "-v", "error",
         "-f", "lavfi", "-i", f"color=c={paper}:s={W}x{H}",
         "-i", art, "-filter_complex", fc, "-map", "[out]",
         "-frames:v", "1", "-update", "1", "-y", out])


def build_text_card(ffmpeg, paper, title, volume, passage, out):
    """原文卡：竖排榜题（左，竖向居中）+ 卷次（右）+ 竖排原文（右起）。"""
    vol_x, vol_y0, vol_size, vol_step = 990, 150, 30, 40
    col_x0, col_pitch, col_y0, col_size, col_step, per_col = 880, 84, 170, 46, 60, 17

    cols = split_columns(passage, per_col)
    # 榜题竖向居中
    title_size, title_step = 104, 124
    block_h = len(title) * title_step
    title_y0 = int((48 + (H - 48)) / 2 - block_h / 2)
    title_x = 190

    parts = [*frame_boxes()]
    parts += vtext(title, FONT_BOLD, title_size, title_step, title_x, title_y0)
    parts += vtext(volume, FONT_REG, vol_size, vol_step, vol_x, vol_y0)
    for c, col in enumerate(cols):
        parts += vtext(col, FONT_REG, col_size, col_step,
                       col_x0 - c * col_pitch, col_y0)

    run([ffmpeg, "-v", "error",
         "-f", "lavfi", "-i", f"color=c={paper}:s={W}x{H}",
         "-filter_complex", f"[0:v]{','.join(parts)}[out]", "-map", "[out]",
         "-frames:v", "1", "-update", "1", "-y", out])
    return dict(
        title=(title_x, title_y0, title_size + 20, block_h),
        volume=(vol_x - 10, vol_y0, 70, len(volume) * vol_step),
        passage=(col_x0 - (len(cols) - 1) * col_pitch, col_y0,
                 (len(cols) - 1) * col_pitch + col_size + 8, per_col * col_step),
    )


def check_fonts(texts):
    """字面覆盖自检（复用 font_coverage.py 的 cmap 解析）。"""
    sys.path.insert(0, HERE)
    from font_coverage import font_charset
    problems = []
    for font in (FONT_BOLD, FONT_REG):
        if not os.path.exists(font):
            problems.append(f"字体缺失：{font}")
            continue
        cs = font_charset(font)
        for label, text in texts.items():
            miss = [ch for ch in text if ord(ch) not in cs]
            if miss:
                problems.append(f"{os.path.basename(font)} 对「{label}」缺字：{''.join(miss)}")
    return problems


def subject_slug(period_dir: str) -> str:
    """`.../subjects/<slug>/period-NN` → `<slug>`；推不出来就直接报错，不猜。"""
    parts = os.path.normpath(os.path.abspath(period_dir)).split(os.sep)
    if "period" in os.path.basename(period_dir):
        for i in range(len(parts) - 1, -1, -1):
            if parts[i] == "subjects" and i + 1 < len(parts) - 1:
                return parts[i + 1]
    raise SystemExit("无法从 --period-dir 推出子主题 slug；请在 manifest.json 里写 slug 字段")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="图赞制版：画心 → 完整竖版图文")
    ap.add_argument("--period-dir",
                    default=os.path.join(PROJ, "subjects", "jiu-wei-hu", "period-01"))
    ap.add_argument("--check", action="store_true", help="只做字面覆盖检查")
    args = ap.parse_args(argv)

    mpath = os.path.join(args.period_dir, "manifest.json")
    if not os.path.exists(mpath):
        raise SystemExit(f"找不到 manifest.json：{mpath}")
    man = json.load(open(mpath, encoding="utf-8"))

    ref = man["text_ref"]
    volume, passage = ref["volume"], ref["passage"]
    title = man.get("cartouche", "")
    cover_line = man.get("cover_line", "")
    origin = ref.get("place", "")
    if not title:
        raise SystemExit("manifest.json 缺少 cartouche（榜题/兽名），拒绝凭空编造")

    texts = {"卷次": volume, "原文": passage, "榜题": title, "点睛句": cover_line, "出處": origin}
    problems = check_fonts({k: v for k, v in texts.items() if v})
    if args.check:
        for p in problems:
            print("❌", p)
        print("OK: 字面全覆盖" if not problems else f"FAIL: {len(problems)} 项问题")
        return 1 if problems else 0
    if problems:
        for p in problems:
            print("❌", p, file=sys.stderr)
        raise SystemExit("字面覆盖自检未通过，拒绝制版")

    ffmpeg = require_ffmpeg()
    final = man["entries"][0]["final"]
    art = os.path.join(args.period_dir, final)
    aw, ah = image_size(ffmpeg, art)
    paper = sample_paper(ffmpeg, art, aw, ah)
    bbox = detect_content_bbox(ffmpeg, art, (aw, ah))

    # 输出名跟着子主题走：`subjects/<slug>/period-NN` → `02-<slug>-zan.png`
    # （初版硬编码 jiu-wei-hu，换一件就会把别人的成品覆盖掉）
    slug = man.get("slug") or subject_slug(args.period_dir)
    plate_out = os.path.join(args.period_dir, f"02-{slug}-zan.png")
    text_out = os.path.join(args.period_dir, f"03-{slug}-wen.png")

    build_plate(ffmpeg, paper, art, title, volume, cover_line, origin, plate_out, bbox)
    tb = build_text_card(ffmpeg, paper, title, volume, passage, text_out)

    checks = []
    checks.append(("主图·榜题区有墨",) + ink_present(ffmpeg, plate_out, 300, 105, 480, 100))
    checks.append(("主图·点睛句有墨",) + ink_present(ffmpeg, plate_out, 200, 1240, 680, 56))
    checks.append(("原文卡·原文区有墨",) + ink_present(ffmpeg, text_out, *tb["passage"]))
    checks.append(("原文卡·卷次区有墨",) + ink_present(ffmpeg, text_out, *tb["volume"]))
    checks.append(("原文卡·榜题有墨",) + ink_present(ffmpeg, text_out, *tb["title"]))

    print(f"paper         : {paper}（采样自画心空白纸区）")
    print(f"content bbox  : {bbox if bbox else '未检出（退回整幅）'}")
    print(f"画心          : {final} → 面板 {PANEL_W}x{PANEL_H}")
    print(f"榜题 / 卷次   : {title} / {volume}")
    print(f"点睛句        : {cover_line}")
    print(f"原文          : {len(passage)} 字，竖排 {len(split_columns(passage, 17))} 列（右起）")
    for name, ok, v in checks:
        print(f"  {'✅' if ok else '❌'} {name}（YMIN={v:.1f}）")
    print(f"out           : {os.path.relpath(plate_out)}\n                {os.path.relpath(text_out)}")

    failed = [c[0] for c in checks if not c[1]]
    if failed:
        print(f"FAIL: 排版自检未通过 → {', '.join(failed)}", file=sys.stderr)
        return 1
    print("OK: 两张卡已产出，文字渲染自检通过")
    return 0


def image_size(ffmpeg, path):
    # 注意：必须用 -v info —— -v error 会把含尺寸的流信息一起压掉
    res = subprocess.run([ffmpeg, "-v", "info", "-i", path,
                          "-frames:v", "1", "-f", "null", "-"],
                         text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    m = re.search(r"(\d{2,5})x(\d{2,5})", res.stdout)
    if not m:
        raise SystemExit("无法读取画心尺寸")
    return int(m.group(1)), int(m.group(2))


if __name__ == "__main__":
    sys.exit(main())
