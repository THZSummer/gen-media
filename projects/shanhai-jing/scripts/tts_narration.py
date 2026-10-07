#!/usr/bin/env python3
"""按讲解稿合成配音，并把"讲解 + BGM 垫底"混成站点播放的那一条。

为什么需要它：项目的宗旨是**传播传统文化、帮普通用户理解**，所以图之后必须有**讲解**。
本脚本把 `audio/narration.txt`（一句一行）变成一条可播放的音轨，并对它做**可复现的校验**。

用法：
  # 0) 先看计划（不联网、不写文件）
  python3 projects/shanhai-jing/scripts/tts_narration.py --slug jiu-wei-hu --dry

  # 1) 只合成讲解（分段落 work/voice-out/，成品落期目录 audio/）
  python3 projects/shanhai-jing/scripts/tts_narration.py --slug jiu-wei-hu

  # 2) 讲解 + BGM 垫底（-14 dB 侧链压缩），站点播放的就是这条
  python3 projects/shanhai-jing/scripts/tts_narration.py --slug jiu-wei-hu \
      --bgm projects/shanhai-jing/subjects/jiu-wei-hu/period-01/bgm/jiu-wei-hu-bgm.mp3

  # 3) 跳过 ASR 回读（默认会做：讲解必须"听得清"）
  python3 projects/shanhai-jing/scripts/tts_narration.py --slug jiu-wei-hu --no-verify

凭据：`$ARK_API_KEY` 或 `work/ark_api_key`（已 gitignore）。**绝不写进代码**——
本仓库曾把 ARK Key 明文提交进两个 tts_narration.py，2026-10-07 已移出（key 需轮换）。

自检（任一不过就非零退出）：
  ① 每段都生成且时长 > 0.3 s（空段/截断会在这里暴露）
  ② 总时长落在 字数÷4.4 ± 25%（过短=有段落被吞）
  ③ ASR 回读：识别词数 ≥ 稿子字数的 55%（**讲解的判据与配乐相反**：配乐要 0 词，讲解要高命中）
"""
from __future__ import annotations

import argparse
import base64
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.normpath(os.path.join(HERE, ".."))
REPO = os.path.normpath(os.path.join(PROJECT, "..", ".."))
WORK = os.path.join(REPO, "work")
SEG_DIR = os.path.join(WORK, "voice-out")
# edge-tts 这类兜底依赖装在工作区内（沙箱允许写工作区，不必动系统 Python）
for _extra in (os.path.join(WORK, "pylibs"),):
    if os.path.isdir(_extra) and _extra not in sys.path:
        sys.path.insert(0, _extra)

URL = "https://openspeech.bytedance.com/api/v3/plan/tts/unidirectional"
RESOURCE_ID = "seed-tts-2.0"
MODEL = "doubao-seed-tts-2.0"
SPEAKER = "zh_female_vv_uranus_bigtts"

# edge-tts 兜底音色（免费、无 Key）。语速放慢 10%、音高略降，贴"沉稳讲解"。
# ⚠️ 实测（2026-10-07，edge-tts 7.2.8）：`--rate=-8%` 会返回 "No audio was received"（0 字节），
#    同一个音色用 `-10%` 正常；`--pitch=-2Hz` 也正常。**别改成 -8%。**
EDGE_VOICE = "zh-CN-XiaoxiaoNeural"
EDGE_RATE = "-10%"
EDGE_PITCH = "-2Hz"


class ArkUnavailable(RuntimeError):
    """ARK TTS 不可用（订阅失效 / 未开通）——不是网络抖动，别重试。"""

CHARS_PER_SEC = 4.4          # 沉稳女声的中文口语语速（实测基准）
GAP_S = 0.35                 # 段间静音
MIN_SEG_S = 0.3
DUR_TOL = 0.25               # 时长容差
ASR_MIN_COVERAGE = 0.55      # ASR 词数 / 稿子字数 的下限
VOSK_MODEL = os.environ.get(
    "VOSK_MODEL", os.path.expanduser("~/.cache/vosk/vosk-model-small-cn-0.22"))


# --------------------------------------------------------------------------- 基础
def load_key() -> str:
    key = os.environ.get("ARK_API_KEY") or ""
    if not key:
        kf = os.path.join(WORK, "ark_api_key")
        if os.path.isfile(kf):
            key = open(kf, encoding="utf-8").read().strip()
    if not key:
        raise SystemExit("ARK_API_KEY 未设置：export ARK_API_KEY=... 或写入 work/ark_api_key（已 gitignore）")
    return key


def probe(path: str) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration,size",
         "-show_entries", "stream=codec_name,sample_rate,channels", "-of", "json", path],
        capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        raise SystemExit(f"ffprobe failed on {path}: {out.stderr.strip()}")
    d = json.loads(out.stdout)
    st = (d.get("streams") or [{}])[0]
    fmt = d.get("format") or {}
    return {"duration": float(fmt["duration"]) if fmt.get("duration") else None,
            "bytes": int(fmt["size"]) if fmt.get("size") else None,
            "codec": st.get("codec_name"),
            "sample_rate": int(st["sample_rate"]) if st.get("sample_rate") else None,
            "channels": st.get("channels")}


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ffmpeg(args: list[str]) -> None:
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("ffmpeg failed:\n" + (r.stderr or "").strip()[:600])


# --------------------------------------------------------------------------- TTS
def tts_one_ark(key: str, text: str, out_path: str, retries: int = 3) -> None:
    """ARK/OpenSpeech 流式接口（仓库文档路径）。订阅失效会抛 ArkUnavailable。"""
    import requests

    headers = {
        "X-Api-Key": key,
        "X-Api-Resource-Id": RESOURCE_ID,
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "X-Control-Require-Usage-Tokens-Return": "*",
    }
    payload = {"req_params": {"text": text, "speaker": SPEAKER,
                              "audio_params": {"format": "mp3", "sample_rate": 24000}}}
    last = ""
    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(URL, headers=headers, json=payload, stream=True, timeout=40)
            if resp.status_code != 200:
                last = f"HTTP {resp.status_code}: {resp.text[:200]}"
                if "InvalidSubscription" in last or "AgentPlan" in last:
                    raise ArkUnavailable(last)
                time.sleep(1.5 * attempt)
                continue
            audio = bytearray()
            for line in resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except ValueError:
                    continue
                code = obj.get("code")
                if code == 0 and obj.get("data"):
                    audio += base64.b64decode(obj["data"])
                elif code == 20000000:
                    break
                elif code not in (0, None):
                    # ⚠️ 必须在**错误码处就停**：服务端出错后不一定关流，
                    # 继续 iter_lines 会一直阻塞到读超时（实测把 6 段拖成 300+ 秒）
                    msg = f"code={code} {obj.get('message','')}"
                    if "InvalidSubscription" in msg or "AgentPlan" in msg:
                        raise ArkUnavailable(msg)
                    last = msg
                    break
            if audio:
                with open(out_path, "wb") as fh:
                    fh.write(bytes(audio))
                return
            last = last or "空音频"
        except ArkUnavailable:
            raise
        except Exception as exc:  # noqa: BLE001 - 网络抖动就重试
            last = f"{type(exc).__name__}: {exc}"
        time.sleep(1.5 * attempt)
    raise SystemExit(f"TTS 失败：{last}")


def tts_one_edge(text: str, out_path: str, voice: str, rate: str, pitch: str) -> None:
    """edge-tts 兜底（免费、无需 Key）。**非官方接口**，商用前自行确认条款。"""
    import asyncio

    try:
        import edge_tts  # 延迟导入：只有走兜底才需要
    except ImportError:
        raise SystemExit(
            "edge 兜底需要 edge-tts：pip install --target work/pylibs edge-tts"
            "（工作区内的依赖目录，脚本已自动加入 sys.path）")

    async def _run() -> None:
        comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        with open(out_path, "wb") as fh:
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    fh.write(chunk["data"])

    asyncio.run(_run())
    if not os.path.getsize(out_path):
        raise SystemExit("edge-tts 返回空音频（网络或音色名有问题）")



# --------------------------------------------------------------------------- 拼接/混音
def concat_with_gaps(seg_files: list[str], out_path: str) -> None:
    """段间插 0.35 s 静音后拼接。mp3 拼接必须重编码（-c copy 会 DTS 错乱，手册有记）。"""
    listing = out_path + ".txt"
    with open(listing, "w", encoding="utf-8") as fh:
        for i, p in enumerate(seg_files):
            fh.write(f"file '{os.path.abspath(p)}'\n")
            if i != len(seg_files) - 1:
                fh.write(f"file '{os.path.abspath(os.path.join(SEG_DIR, 'gap.mp3'))}'\n")
    ffmpeg(["-f", "concat", "-safe", "0", "-i", listing, "-c:a", "libmp3lame", "-b:a", "128k", out_path])
    os.remove(listing)


def make_gap(path: str, seconds: float) -> None:
    ffmpeg(["-f", "lavfi", "-i", f"anullsrc=r=24000:cl=mono", "-t", f"{seconds}", "-c:a", "libmp3lame", path])


def mix_bed(voice: str, bgm: str, out_path: str, duck_db: float) -> None:
    """讲解 + BGM 垫底：BGM 先压低，再用讲解做 sidechain 侧链压缩，最后混音。"""
    fc = (f"[0:a]volume=-{abs(duck_db)}dB[bed];"
          f"[bed][1:a]sidechaincompress=threshold=0.04:ratio=8:attack=20:release=350[ducked];"
          f"[ducked][1:a]amix=inputs=2:duration=longest:dropout_transition=0,"
          f"loudnorm=I=-16:TP=-1.5:LRA=11[out]")
    ffmpeg(["-stream_loop", "-1", "-i", bgm, "-i", voice,
            "-filter_complex", fc, "-map", "[out]",
            "-c:a", "libmp3lame", "-b:a", "128k", "-shortest", out_path])


# --------------------------------------------------------------------------- ASR 回读
def asr_stats(wav: str) -> dict | None:
    try:
        import json as _json
        import wave

        from vosk import KaldiRecognizer, Model, SetLogLevel
    except ImportError:
        return None
    if not os.path.isdir(VOSK_MODEL):
        return None
    SetLogLevel(-1)
    wf = wave.open(wav, "rb")
    rec = KaldiRecognizer(Model(VOSK_MODEL), wf.getframerate())
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
    speech = sum(w["end"] - w["start"] for w in words)
    return {"words": len(words), "speech_s": round(speech, 2), "text": " ".join(segs)[:400]}


# --------------------------------------------------------------------------- 主流程
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", default="jiu-wei-hu")
    ap.add_argument("--period", default="period-01")
    ap.add_argument("--text-file", default="", help="默认 audio/narration.txt")
    ap.add_argument("--bgm", default="", help="BGM 垫底文件（不给就只出纯讲解）")
    ap.add_argument("--bgm-duck-db", type=float, default=14.0)
    ap.add_argument("--engine", choices=("ark", "edge", "auto"), default="auto",
                    help="ark=仓库文档路径（需 Agent Plan）; edge=免费兜底; auto=先 ark，订阅失效则转 edge")
    ap.add_argument("--voice", default="", help=f"edge 音色（默认 {EDGE_VOICE}）")
    ap.add_argument("--rate", default=EDGE_RATE)
    ap.add_argument("--pitch", default=EDGE_PITCH)
    ap.add_argument("--out-name", default="", help="成品文件名（默认 <slug>-full.mp3 / -narration.mp3）")
    ap.add_argument("--no-verify", dest="verify", action="store_false")
    ap.add_argument("--no-manifest", dest="manifest", action="store_false")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args(argv)

    pdir = os.path.join(PROJECT, "subjects", args.slug, args.period)
    tfile = args.text_file or os.path.join(pdir, "audio", "narration.txt")
    if not os.path.isfile(tfile):
        raise SystemExit(f"讲解稿不存在：{tfile}")
    segments = [l.strip() for l in open(tfile, encoding="utf-8") if l.strip()]
    chars = sum(len(s) for s in segments)
    expected = chars / CHARS_PER_SEC
    print(f"讲解稿 {tfile}\n  {len(segments)} 段 / {chars} 字 → 预估 {expected:.1f}s（{CHARS_PER_SEC} 字/秒）")
    for i, s in enumerate(segments, 1):
        print(f"   {i}. [{len(s):>3}字] {s}")

    if args.dry:
        print(f"\n[dry] 会合成 {len(segments)} 段 → {SEG_DIR}/ → 拼接"
              + (f" → 与 {args.bgm} 混音（垫底 -{args.bgm_duck_db:g} dB + 侧链）" if args.bgm else "（无 BGM 垫底）")
              + f"\n      成品落 {pdir}/audio/，并{'更新' if args.manifest else '不更新'} manifest 的 audio 段")
        return 0

    if not shutil.which("ffmpeg"):
        raise SystemExit("需要 ffmpeg")
    engine = args.engine
    key = ""
    if engine in ("ark", "auto"):
        try:
            key = load_key()
        except SystemExit as exc:
            if engine == "ark":
                raise
            print(f"   ⏭  ARK 凭据缺失（{exc}）→ 转 edge 兜底")
            engine = "edge"
    os.makedirs(SEG_DIR, exist_ok=True)
    os.makedirs(os.path.join(pdir, "audio"), exist_ok=True)
    make_gap(os.path.join(SEG_DIR, "gap.mp3"), GAP_S)

    voice = args.voice or EDGE_VOICE
    print("   引擎: " + (f"edge（{voice} rate={args.rate} pitch={args.pitch}）"
                        if engine == "edge" else f"ark（{SPEAKER}）"), flush=True)
    bad = []
    seg_files = []
    for i, text in enumerate(segments, 1):
        out = os.path.join(SEG_DIR, f"{args.slug}-seg-{i:02d}.mp3")
        if engine == "edge":
            tts_one_edge(text, out, voice, args.rate, args.pitch)
        else:
            try:
                tts_one_ark(key, text, out)
            except ArkUnavailable as exc:
                if args.engine != "auto":
                    raise SystemExit(f"ARK TTS 不可用：{exc}")
                print(f"   ⚠️  ARK TTS 订阅不可用（{str(exc)[:140]}…）→ 转 edge 兜底", flush=True)
                engine = "edge"
                tts_one_edge(text, out, voice, args.rate, args.pitch)
        info = probe(out)
        print(f"   段 {i}: {info['duration']:.2f}s {info['bytes']}B", flush=True)
        if not info["duration"] or info["duration"] < MIN_SEG_S:
            bad.append(f"段 {i} 时长为 {info['duration']}（< {MIN_SEG_S}s）")
        seg_files.append(out)

    narration = os.path.join(pdir, "audio", args.out_name or f"{args.slug}-narration.mp3")
    concat_with_gaps(seg_files, narration)
    n_info = probe(narration)
    print(f"讲解轨 {narration}\n  {n_info['duration']:.2f}s / {n_info['bytes']}B / "
          f"{n_info['codec']} {n_info['sample_rate']}Hz {n_info['channels']}ch")
    if abs(n_info["duration"] - expected) > expected * DUR_TOL:
        bad.append(f"总时长 {n_info['duration']:.2f}s 偏离预估 {expected:.1f}s 超过 ±{DUR_TOL:.0%}"
                   "（可能被吞段）")

    final = narration
    if args.bgm:
        if not os.path.isfile(args.bgm):
            raise SystemExit(f"BGM 不存在：{args.bgm}")
        final = os.path.join(pdir, "audio", f"{args.slug}-full.mp3")
        mix_bed(narration, args.bgm, final, args.bgm_duck_db)
        f_info = probe(final)
        print(f"混音成品 {final}\n  {f_info['duration']:.2f}s / {f_info['bytes']}B"
              f"（BGM 垫底 -{args.bgm_duck_db:g} dB + 侧链）")
        if abs(f_info["duration"] - n_info["duration"]) > 1.0:
            bad.append("混音后时长与讲解轨差 > 1s")

    stats = None
    if args.verify:
        tmp = os.path.join(SEG_DIR, f"{args.slug}-asr.wav")
        ffmpeg(["-i", narration, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", tmp])
        stats = asr_stats(tmp)
        if stats is None:
            print("   ⏭  ASR 回读跳过（缺 vosk 或模型）")
        else:
            cover = stats["words"] / max(chars, 1)
            print(f"   ASR 回读：{stats['words']} 词（覆盖 {cover:.0%}，阈值 {ASR_MIN_COVERAGE:.0%}）")
            print(f"   转写：{stats['text']}")
            if cover < ASR_MIN_COVERAGE:
                bad.append(f"ASR 覆盖率 {cover:.0%} < {ASR_MIN_COVERAGE:.0%}（讲解听不清）")

    if args.manifest:
        mpath = os.path.join(pdir, "manifest.json")
        man = json.load(open(mpath, encoding="utf-8"))
        if "bgm" not in man and isinstance(man.get("audio"), dict) and "preset" in man["audio"]:
            man["bgm"] = man.pop("audio")        # 旧的 audio 段描述的是 BGM，挪到 bgm
        f_info = probe(final)
        man["audio"] = {
            "file": os.path.relpath(final, pdir).replace(os.sep, "/"),
            "kind": "narration",
            "duration_s": round(f_info["duration"], 3),
            "sha256": sha256(final),
            "voice": ({"engine": "edge-tts", "voice": voice, "rate": args.rate, "pitch": args.pitch}
                      if engine == "edge" else
                      {"engine": "ark-openspeech", "speaker": SPEAKER, "model": MODEL}),
            "parts": {"narration": os.path.relpath(narration, pdir).replace(os.sep, "/"),
                      **({"bgm": os.path.relpath(args.bgm, pdir).replace(os.sep, "/")} if args.bgm else {})},
            "generated": time.strftime("%Y-%m-%d"),
            "verify": {"asr_words": (stats or {}).get("words"), "script_chars": chars,
                       "expected_s": round(expected, 1)},
            "note": ("讲解旁白（TTS）+ BGM 垫底" if args.bgm else "讲解旁白（TTS）")
                    + "；宗旨是帮普通用户理解，判据与配乐相反：讲解要 ASR 高命中",
        }
        with open(mpath, "w", encoding="utf-8") as fh:
            json.dump(man, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print(f"   manifest 已更新：audio.file={man['audio']['file']} kind=narration")

    if bad:
        for b in bad:
            print(f"  ✗ {b}", file=sys.stderr)
        return 2
    print("✅ 讲解配音完成（自检全过）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
