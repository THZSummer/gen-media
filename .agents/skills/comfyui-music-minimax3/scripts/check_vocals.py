#!/usr/bin/env python3
"""人声（词）核查：用**离线 ASR** 检查一条音频里有没有被识别成"话"的内容。

为什么需要它：`--instrumental` 只是**提示词层面**的约束，听感脚本验不了。
本脚本把"有没有人声"变成可复现的数字，并用**同法对照**证明方法有效：

  # 单条检测（0 词 = 没检出人声词）
  python3 scripts/check_vocals.py out/jwh-bgm.mp3

  # 带对照（推荐）：对照文件必须是有旁白的，用来证明"这套方法真能识别人声"
  python3 scripts/check_vocals.py out/jwh-bgm.mp3 \
      --control ../../../../projects/tea-shake-dance/out/video/tea_shake_narrated.mp4

  # 期望对照至少识别出 5 个词，否则判定"方法未生效"（不算通过）
  python3 scripts/check_vocals.py out/jwh-bgm.mp3 --control narr.mp4 --control-min-words 5

判定（退出码）：
  0  被测音频 0 词，且（若给了对照）对照识别出 ≥ control-min-words 个词
  1  被测音频**识别出了词** → 疑似有人声，必须人耳复核（可能是真唱，也可能是 ASR 幻觉）
  3  环境缺依赖（没装 vosk / 没有模型）→ 打印 SKIPPED_NO_VOSK，**不假装通过**

⚠️ 三条限制（别把 0 词当成"绝对没有人声"）：
  1. ASR 认的是**词**，不是"无词哼唱/气声"。哼鸣可能 0 词。
  2. 模型有语种：默认中文小模型（`vosk-model-small-cn-0.22`）对中文人声敏感；
     英文/其它语种的歌词要换模型（`--model` 或 `$VOSK_MODEL`）。
  3. 音乐上会**幻觉**：实测一段纯音乐/音效轨被识别出 3 个词（「啊 嘿嘿 姐姐」，语音占比 2.6%）。
     所以非 0 词 ≠ 一定有人声；0 词才是我们要的证据，且仍需人耳终判。
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

DEFAULT_MODEL = os.environ.get(
    "VOSK_MODEL", os.path.expanduser("~/.cache/vosk/vosk-model-small-cn-0.22"))


def to_wav(src: str, dst: str) -> None:
    """抽出 16 kHz 单声道 WAV（vosk 的要求）。"""
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", src, "-vn",
         "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", dst],
        check=True, capture_output=True, text=True)


def transcribe(wav: str, model_path: str) -> dict:
    import json as _json
    import wave
    from vosk import KaldiRecognizer, Model, SetLogLevel

    SetLogLevel(-1)
    wf = wave.open(wav, "rb")
    rec = KaldiRecognizer(Model(model_path), wf.getframerate())
    rec.SetWords(True)
    words, segs = [], []
    while True:
        data = wf.readframes(4000)
        if not data:
            break
        if rec.AcceptWaveform(data):
            r = _json.loads(rec.Result())
            words += r.get("result", [])
            if r.get("text"):
                segs.append(r["text"])
    r = _json.loads(rec.FinalResult())
    words += r.get("result", [])
    if r.get("text"):
        segs.append(r["text"])
    dur = wf.getnframes() / wf.getframerate()
    speech = sum(w["end"] - w["start"] for w in words)
    return {
        "duration_s": round(dur, 2),
        "words": len(words),
        "speech_s": round(speech, 2),
        "speech_ratio": round(speech / dur, 4) if dur else 0.0,
        "text": " ".join(segs)[:300],
    }


def probe(path: str, model_path: str) -> dict:
    tmp = tempfile.mkdtemp(prefix="vocals-")
    try:
        wav = os.path.join(tmp, "a.wav")
        to_wav(path, wav)
        out = transcribe(wav, model_path)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    out["file"] = path
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", nargs="+", help="要检测的音频/视频（1 条起）")
    ap.add_argument("--control", help="已知有旁白的对照文件（同法验证方法有效）")
    ap.add_argument("--control-min-words", type=int, default=5,
                    help="对照至少要识别出这么多词，否则算方法未生效（默认 5）")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"vosk 模型目录（默认 {DEFAULT_MODEL}）")
    args = ap.parse_args(argv)

    if not shutil.which("ffmpeg"):
        print(json.dumps({"skipped": "SKIPPED_NO_FFMPEG"}, ensure_ascii=False))
        return 3
    try:
        import vosk  # noqa: F401
    except ImportError:
        print(json.dumps({"skipped": "SKIPPED_NO_VOSK",
                          "hint": "pip install vosk，并准备一个模型目录（--model / $VOSK_MODEL）"},
                         ensure_ascii=False))
        return 3
    if not os.path.isdir(args.model):
        print(json.dumps({"skipped": "SKIPPED_NO_VOSK_MODEL", "model": args.model,
                          "hint": "下载 vosk 中文小模型解压到该目录，或用 --model 指定"},
                         ensure_ascii=False))
        return 3

    results = [probe(p, args.model) for p in args.audio]
    report = {"model": os.path.basename(args.model.rstrip("/")), "audio": results}
    ok = True
    for r in results:
        print(json.dumps(r, ensure_ascii=False))
        if r["words"] > 0:
            ok = False
    if args.control:
        c = probe(args.control, args.model)
        report["control"] = c
        print(json.dumps(c, ensure_ascii=False))
        if c["words"] < args.control_min_words:
            ok = False
            print(f"  ✗ 对照只识别出 {c['words']} 个词（< {args.control_min_words}）"
                  f"→ 方法未生效，本次检测无效")
        else:
            print(f"  ✓ 对照识别出 {c['words']} 个词（语音占比 {c['speech_ratio']:.1%}）"
                  f"→ 方法有效")
    if ok:
        print(f"✅ 被测音频 0 词（未检出人声词）；仍需人耳终判：ASR 认词，不认无词哼唱")
    else:
        print("⚠️  检出词或对照失效 —— 人耳复核；若非幻觉，请加严厉排除词换 seed 重出")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
