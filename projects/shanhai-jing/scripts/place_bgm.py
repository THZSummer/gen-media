#!/usr/bin/env python3
"""把生成好的配乐转码落位到期目录，并把 `audio` 段写回 manifest。

站点详情页的配乐开关读的是期 manifest 的 `audio`（见 dev-guide references/site.md §5.1），
但**不能把 227–245 kbps 的母版直接塞进仓库**：30 s 的 V0 约 850 KB，站点上没人听得出区别。
本脚本负责：转码到 128 kbps → 剥元数据 → 落位 `bgm/<slug>-bgm.mp3` → 算 sha256 / 时长 →
写回 manifest → 自检。

用法：
  # 1) 先看会做什么（不写任何文件）
  python3 scripts/place_bgm.py --slug jiu-wei-hu --src work/music-out/jwh-bgm-30s_00001.mp3 \
      --preset "模板 A · 古琴独奏" --seed 9097 --dry

  # 2) 真正落位
  python3 scripts/place_bgm.py --slug jiu-wei-hu --src work/music-out/jwh-bgm-30s_00001.mp3 \
      --preset "模板 A · 古琴独奏" --seed 9097 --caption-file work/music-out/jwh-caption.txt

自检（任一不过就非零退出）：
  ① 转码产物存在、体积 < 2 MB、时长与母版差 ≤ 1 s
  ② ffprobe 复核：mp3 / 44100 Hz / 双声道
  ③ sha256 与写进 manifest 的一致
  ④ manifest 仍能解析，`audio.file` 指向的文件真的在
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.normpath(os.path.join(HERE, ".."))
REPO = os.path.normpath(os.path.join(PROJECT, "..", ".."))

MAX_BYTES = 2 * 1024 * 1024          # 单条配乐上限：超过就说明码率/时长要重新想
DUR_TOL = 1.0                        # 与母版时长容差（秒）


def ffprobe(path: str) -> dict:
    exe = shutil.which("ffprobe")
    if not exe:
        raise SystemExit("ffprobe not found (install ffmpeg)")
    out = subprocess.run(
        [exe, "-v", "error", "-show_entries",
         "stream=codec_name,sample_rate,channels,bit_rate",
         "-show_entries", "format=duration,size", "-of", "json", path],
        capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        raise SystemExit(f"ffprobe failed on {path}: {out.stderr.strip()}")
    data = json.loads(out.stdout)
    st = (data.get("streams") or [{}])[0]
    fmt = data.get("format") or {}
    return {
        "codec": st.get("codec_name"),
        "sample_rate": int(st["sample_rate"]) if st.get("sample_rate") else None,
        "channels": st.get("channels"),
        "bit_rate": int(st["bit_rate"]) if st.get("bit_rate") else None,
        "duration": float(fmt["duration"]) if fmt.get("duration") else None,
        "bytes": int(fmt["size"]) if fmt.get("size") else os.path.getsize(path),
    }


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", required=True, help="子主题目录名，如 jiu-wei-hu")
    ap.add_argument("--src", required=True, help="生成出来的母版 mp3（V0/高码率）")
    ap.add_argument("--period", default="period-01")
    ap.add_argument("--preset", default="", help='用词模板，如 "模板 A · 古琴独奏"')
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--skill", default="comfyui-music-minimax3")
    ap.add_argument("--generated", default="", help="生成日期 YYYY-MM-DD（默认今天）")
    ap.add_argument("--caption-file", default="", help="母版用的 caption 存档（可选，写进 manifest）")
    ap.add_argument("--bitrate", default="128k")
    ap.add_argument("--dry", action="store_true", help="只打印计划，不写文件")
    args = ap.parse_args(argv)

    pdir = os.path.join(PROJECT, "subjects", args.slug, args.period)
    if not os.path.isdir(pdir):
        raise SystemExit(f"period dir not found: {pdir}")
    if not os.path.isfile(args.src):
        raise SystemExit(f"source audio not found: {args.src}")

    bgm_dir = os.path.join(pdir, "bgm")
    dst = os.path.join(bgm_dir, f"{args.slug}-bgm.mp3")
    rel_file = os.path.join("bgm", os.path.basename(dst))

    src_info = ffprobe(args.src)
    print(f"母版 {args.src}\n  {src_info['codec']} {src_info['sample_rate']}Hz "
          f"{src_info['channels']}ch {src_info['bit_rate']}bps {src_info['duration']:.3f}s "
          f"{src_info['bytes']}B")

    if args.dry:
        print(f"\n[dry] 会转码 -> {dst} @ {args.bitrate}（剥元数据），并写回 {pdir}/manifest.json 的 audio 段")
        return 0

    os.makedirs(bgm_dir, exist_ok=True)
    tmp = dst + ".tmp.mp3"
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", args.src,
           "-map_metadata", "-1", "-c:a", "libmp3lame", "-b:a", args.bitrate,
           "-ar", "44100", "-ac", "2", tmp]
    if subprocess.run(cmd, capture_output=True, text=True).returncode != 0:
        raise SystemExit("ffmpeg transcode failed")
    os.replace(tmp, dst)

    info = ffprobe(dst)
    problems = []
    if info["bytes"] > MAX_BYTES:
        problems.append(f"体积 {info['bytes']}B 超过上限 {MAX_BYTES}B")
    if info["duration"] is None or abs(info["duration"] - (src_info["duration"] or 0)) > DUR_TOL:
        problems.append(f"时长 {info['duration']} 与母版 {src_info['duration']} 差超过 {DUR_TOL}s")
    if info["codec"] != "mp3":
        problems.append(f"编码不是 mp3（{info['codec']}）")
    if info["sample_rate"] != 44100:
        problems.append(f"采样率不是 44100（{info['sample_rate']}）")
    if info["channels"] != 2:
        problems.append(f"不是双声道（{info['channels']}）")
    if problems:
        for p in problems:
            print(f"  ✗ {p}", file=sys.stderr)
        raise SystemExit(2)

    digest = sha256(dst)
    caption = ""
    if args.caption_file and os.path.isfile(args.caption_file):
        caption = open(args.caption_file, encoding="utf-8").read().strip()

    mpath = os.path.join(pdir, "manifest.json")
    man = json.load(open(mpath, encoding="utf-8"))
    audio = {
        "file": rel_file.replace(os.sep, "/"),
        "duration_s": round(info["duration"], 3),
        "seed": args.seed,
        "preset": args.preset or None,
        "skill": args.skill,
        "generated": args.generated or __import__("time").strftime("%Y-%m-%d"),
        "sha256": digest,
        "note": ("AI 生成配乐（开放权重，商用前读模型许可）；母版 %d kbps 留在 work/，"
                 "入库版本为 %s 转码" % (round((src_info["bit_rate"] or 0) / 1000), args.bitrate)),
    }
    if caption:
        audio["caption"] = caption
    audio = {k: v for k, v in audio.items() if v is not None}
    man["audio"] = audio
    with open(mpath, "w", encoding="utf-8") as fh:
        json.dump(man, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    # ④ 回读复核
    back = json.load(open(mpath, encoding="utf-8"))["audio"]
    target = os.path.join(pdir, back["file"])
    assert os.path.isfile(target), "manifest audio.file 指向的文件不存在"
    assert back["sha256"] == sha256(target), "manifest 记录的 sha256 与实际文件不一致"

    print(f"\n✅ 落位 {dst}\n   {info['codec']} {info['sample_rate']}Hz {info['channels']}ch "
          f"{info['bit_rate']}bps {info['duration']:.3f}s {info['bytes']}B\n"
          f"   sha256 {digest[:16]}…（已写回 manifest）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
