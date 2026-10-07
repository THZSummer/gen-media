#!/usr/bin/env python3
"""
荒岛求生 - 旁白 TTS 生成
调用火山方舟 seed-tts-2.0（Agent Plan）生成 6 镜旁白音频。

用法：
  python3 tts_narration.py            # 生成全部 6 段
  python3 tts_narration.py 1 3 5      # 只生成指定镜号

输出：out/narration_<镜号>.mp3
"""
import requests
import json
import base64
import os
import sys

API_KEY = os.environ.get("ARK_API_KEY") or ""
if not API_KEY:
    _kf = os.path.join(os.path.dirname(__file__), "..", "..", "..", "work", "ark_api_key")
    if os.path.isfile(_kf):
        API_KEY = open(_kf, encoding="utf-8").read().strip()
if not API_KEY:
    raise SystemExit("ARK_API_KEY 未设置：请 export ARK_API_KEY=... 或写入 work/ark_api_key（已 gitignore）")
URL = "https://openspeech.bytedance.com/api/v3/plan/tts/unidirectional"
RESOURCE_ID = "seed-tts-2.0"
# 旁白用沉稳女声（uranus 系列），适合反思叙事
SPEAKER = "zh_female_vv_uranus_bigtts"

# 6 镜旁白脚本（反差弧线：天堂海岛 vs 落难少女）
NARRATION = {
    1: "天堂般的海岛，与一个被遗忘的灵魂。",
    2: "她爬上洁白的沙滩，离开了海，却没离开孤独。",
    3: "丰饶的雨林里，她只为了一口水而拼命。",
    4: "火光亮起的那一刻，绝望也成了希望。",
    5: "黄昏柔美如度假，她却用残枝搭起今夜的床。",
    6: "银河璀璨，她蜷缩在火旁，眼里有不灭的光。",
}

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "out")


def tts_one(text: str, out_path: str) -> bool:
    """调用 TTS 流式接口，合成一段音频写入 out_path。成功返回 True。"""
    headers = {
        "X-Api-Key": API_KEY,
        "X-Api-Resource-Id": RESOURCE_ID,
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "X-Control-Require-Usage-Tokens-Return": "*",
    }
    payload = {
        "req_params": {
            "text": text,
            "speaker": SPEAKER,
            "audio_params": {"format": "mp3", "sample_rate": 24000},
        }
    }
    session = requests.Session()
    try:
        resp = session.post(URL, headers=headers, json=payload, stream=True, timeout=60)
        audio = bytearray()
        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            data = json.loads(line)
            code = data.get("code", 0)
            if code == 0 and data.get("data"):
                audio.extend(base64.b64decode(data["data"]))
            if code == 20000000:  # 结束码
                break
            if code > 0 and code != 20000000:
                print(f"  ❌ 错误 code={code}: {data}")
                return False
        if audio:
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "wb") as f:
                f.write(audio)
            print(f"  ✅ {out_path} ({len(audio)/1024:.1f} KB)")
            return True
        print("  ❌ 无音频数据返回")
        return False
    except Exception as e:
        print(f"  ❌ 请求异常: {e}")
        return False
    finally:
        session.close()


def main():
    shots = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(NARRATION.keys())
    ok = 0
    for n in shots:
        text = NARRATION.get(n)
        if not text:
            print(f"镜{n}: 无旁白定义，跳过")
            continue
        print(f"镜{n}: {text}")
        out = os.path.join(OUT_DIR, f"narration_{n}.mp3")
        if tts_one(text, out):
            ok += 1
    print(f"\n完成 {ok}/{len(shots)} 段")


if __name__ == "__main__":
    main()
