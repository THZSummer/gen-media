# Speech Synthesis (Text-to-Speech, TTS / post-production dubbing)

> 🌐 Language: **English** | [中文](README.md)

> Input: text. Output: speech audio (mp3). Currently uses `seed-tts-2.0` (included in Agent Plan Medium, agent-plan profile).
> Back to [methods overview](../README.en.md)

> ⚠️ **arkcli does not cover TTS/ASR**. TTS goes through the OpenSpeech service (independent of Ark Runtime) and requires writing your own script to call the HTTP streaming interface. `+chat`/`+gen`/`+code-example` do not support speech models.

---

## 1. Topic Positioning

Speech synthesis is the path of **generating a human voice from text**: give a piece of text, get a piece of speech. In the video generation workflow it is mainly used for **post-production dubbing** — adding narration, dialogue and copy reading to the final film.

### Typical uses

| Use | Description |
|------|------|
| **Video narration** | Documentary / short film commentary; TTS generation → ffmpeg mixing into the video |
| **Product dialogue** | Voice-over copy for commercials |
| **Multilingual dubbing** | Different language narration over the same picture |

### Difference from the video's built-in audio

| | TTS post-production dubbing (this document) | Video generation with built-in audio |
|---|---------------------|-----------------|
| Who generates it | OpenSpeech (an independent service) | Seedance 1.5-pro (`--generate-audio`) |
| Controllability | Text is controllable character by character and can be regenerated repeatedly | Not controllable |
| Applicable models | Any video model (independent of audio-visual capability) | Built-in audio: ✅ 1.5-pro / 2.0 (260128); ⛔ 2.0-fast / mini have no audio and require post-production TTS |
| Workflow | Dub after the video is generated | Audio comes out together with video generation |

> ⚠️ mini has no audio output → post-production TTS + ffmpeg mixing is the standard dubbing path for the 2.0 series.

---

## 2. Models and Routing

| Item | Value |
|----|----|
| Model | Doubao Speech Synthesis 2.0 (`doubao-seed-tts-2.0`) |
| Resource-Id | `seed-tts-2.0` |
| Profile | agent-plan (TTS is included in the Medium plan and uses the ARK API Key) |
| Endpoint | `https://openspeech.bytedance.com/api/v3/plan/tts/unidirectional` (the `/plan/` path = Agent Plan channel)|
| Authentication | Header `X-Api-Key: <ark-api-key>` + `X-Api-Resource-Id: seed-tts-2.0` |

---

## 3. Request and Decoding

### Request body

```json
{
  "req_params": {
    "text": "需要合成的文本",
    "speaker": "zh_female_vv_uranus_bigtts",
    "audio_params": {
      "format": "mp3",
      "sample_rate": 24000
    }
  }
}
```

### Response (streaming JSON Lines)

Each line is `{"code":0,"data":"<base64 audio chunk>"}`; `code=20000000` marks the end; concatenate the per-line `base64.b64decode(data)` into a complete mp3.

### Common speakers

| speaker | Voice | Suitable for |
|---------|------|------|
| `zh_female_vv_uranus_bigtts` | Steady female voice | Narration, commentary |
| Others | See the speech synthesis voice list in the console | - |

---

## 4. Commands / Scripts

For a call example see `projects/survival-island/scripts/tts_narration.py` (streaming receive + base64 concatenation + saving to disk, reusable).

```bash
python3 scripts/tts_narration.py   # 生成全部旁白段
```

> To get the API Key: `arkcli auth status` shows the mask; the full value is in `~/.arkcli/identities/<volc-id>/apikey.json`.

---

## 5. Mixing into the Video (ffmpeg)

> ⚠️ **Do not re-encode with `-c:a aac`**; putting the mp3 straight into the mp4 (`-c:a copy`) is enough — measured, after aac re-encoding players may fail to recognise the audio track.

```bash
# 拼接多段旁白（重编码避免 DTS 错乱）
ffmpeg -f concat -safe 0 -i concat_audio.txt -c:a libmp3lame -b:a 128k narration_full.mp3

# 混入视频（视频 copy + 音频 copy）
ffmpeg -i video.mp4 -i narration_full.mp3 \
  -c:v copy -c:a copy -map 0:v -map 1:a -shortest out.mp4
```

- The video stream is not re-encoded with `-c:v copy`; the audio stream goes straight in with `-c:a copy`
- When concatenating mp3s (concat), `-c copy` is **forbidden** (DTS confusion); re-encode with `-c:a libmp3lame`
- Aligning a single narration segment to the video: `ffmpeg -i seg.mp3 -af apad -t <duration> seg_pad.mp3`

---

## 6. Checklist

- [ ] The endpoint uses the `/plan/` path (Agent Plan channel)
- [ ] The header carries X-Api-Key + X-Api-Resource-Id: seed-tts-2.0
- [ ] Streaming decoding: base64 concatenated line by line, `code=20000000` at the end
- [ ] Narration duration is aligned with the video (apad + -t)
- [ ] Mixing uses `-c:a copy`, not aac
- [ ] The voice choice matches the tone of the content

---

## Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-08-01 | v1.0 | Split out of the TTS chapter of the methods overview into its own document: speech synthesis (seed-tts-2.0), covering endpoint / request body / streaming decoding / speaker / mixing | 小七 |
