# Audio-Driven Video (Audio-Driven)

> 🌐 Language: **English** | [中文](README.md)

> Input: reference audio + prompt. Output: a video whose visual rhythm follows the audio (beat/rhythm).
> Back to [method overview](../README.en.md) ｜ Applicable models: Seedance series (versions that support ref_audio)

---

## 1. Topic positioning

Audio-driven is the path where **the picture follows the sound**: you have a piece of music/beat audio and want the video's shot changes and montage rhythm to synchronise with it. In essence it is "audio rhythm -> picture rhythm".

### When to choose audio-driven

- Beat-cut videos (cutting shots on the drum hits)
- MVs, scored visuals for ad films
- City/product montages that switch on the beat
- You want the sync of "when the music peaks, the picture peaks too"

### When not to choose it

- You want the video to come with its own audio -> use `--generate-audio` (the model generates audio; that is not audio-driven). ✅ Only `doubao-seedance-1-5-pro` / `doubao-seedance-2-0` (260128, measured 2026-08-01) support it; ⛔ 2.0-fast / mini output video only, no audio
- You have no particular audio and only need the picture -> [text-to-video](../text-to-video/README.en.md)
- You want to replicate a video's motion -> [reference-video](../reference-video/README.en.md)

> ⚠️ Distinguish two concepts:
> - **Audio-driven**: you supply the audio and the picture follows its rhythm (this topic)
> - **Audio generation**: the model generates a voice-over/BGM for the video (`--generate-audio`; you do not supply audio). ✅ supported by 1.5-pro / 2.0 (260128); ⛔ 2.0-fast / mini output video only

---

## 2. Capability mapping

| Control dimension | Means under audio-driven |
|----------|----------------|
| Rhythm | Strongly constrained by the reference audio |
| Picture content | Described by the prompt |
| Shot changes | Switch automatically with the beat (montage) |
| Style | Described in the prompt |

### How it works

```
参考音频的节拍/能量变化 ──► 视频的镜头切换/节奏
prompt 描述的画面/风格   ──► 视频的内容
```

The model extracts rhythm features from the audio and maps beat points onto shot-change points, producing the "on-beat" effect.

---

## 3. Audio selection strategy

### Good reference audio

| Characteristic | Notes |
|------|------|
| Clear beat | Crisp drum hits/accents, distinct strong and weak beats |
| Stable tempo | A steady BPM, easy to cut shots to |
| Matching duration | Close to the target video's duration |
| Dynamic range | Has dynamics, with a clear climax section |

### Bad reference audio

- Pure ambient sound/white noise (no beat to extract)
- Chaotic rhythm, free time
- Too long and untrimmed (the key section gets diluted)

### Making your own beat audio

When you have no ready-made music, you can export a clear drum pattern from any DAW/beat generator; the result is often more controllable than complex music.

---

## 4. Prompt strategy

For audio-driven prompts the focus is on **describing the picture content and the switching style**; the rhythm is left to the audio.

### Recommended structure

```
[画面主题/场景] + [蒙太奇/切换风格] + [随节拍切换的元素]
```

**Example**:
> A city night-scene montage switching on the beat, neon signs, traffic and pedestrian close-ups alternating, cyberpunk colour grading

### Key points

- **Say "on the beat/beat-synced" explicitly**: make it clear to the model that rhythmic switching is wanted
- **Give a list of switchable elements**: a montage needs several picture elements rotating
- **Do not write specific time points**: the rhythm is decided by the audio, so writing "cut the shot at second 2" in the prompt has no effect
- **Keep the style consistent**: all switching elements keep one consistent grade/style

---

## 5. Parameter selection

| Parameter | Audio-driven recommendation | Notes |
|------|-------------|------|
| `--input` | `ref:@beat.mp3` | Use the `ref:` prefix to make clear it is reference audio |
| `--ratio` | By publishing channel | Vertical beat-cut videos commonly use `9:16` |
| `--duration` | Close to the duration of the audio's key section | |
| `--generate-audio` | Generally not used | Avoids conflicting with the reference audio; if you need sound in the end, composite it in post |
| `--draft` | Use when testing the beat-sync effect | |

> When audio is passed as `--input`, it is routed automatically by extension (`.mp3`/`.wav`, etc.) to the ref_audio channel. In a video task only the first image is the first frame; audio does not take the first-frame slot.

---

## 6. Command templates

```bash
VER=$(arkcli models get doubao-seedance-2-0 --transform 'primary_version' | tr -d '"')
MODEL="doubao-seedance-2-0-${VER:-260128}"

# 1) 节拍蒙太奇
arkcli +gen --model "$MODEL" \
  --input ref:@beat.mp3 --ratio 9:16 \
  "随节拍切换的城市夜景蒙太奇，霓虹、车流、行人特写交替，赛博朋克色调" --open

# 2) 配乐画面同步
arkcli +gen --model "$MODEL" \
  --input ref:@bgm.mp3 --ratio 16:9 --duration 5 \
  "产品在不同场景中流转，画面随音乐起伏推进，影棚光" --open

# 3) 音频 + 首帧图组合（首帧图 + 参考音频）
arkcli +gen --model "$MODEL" \
  --input @first.jpg --input ref:@beat.mp3 \
  "从首帧开始，随节拍切到不同角度的特写" --open
```

---

## 7. Pitfalls

| Symptom | Cause | Fix |
|------|------|------|
| No sense of being on the beat | The audio has no clear beat | Switch to audio with a distinct drum pattern |
| Chaotic shot changes | Too few/too many prompt elements | Give 3-5 clear switchable elements |
| Audio treated as the first frame | A plain `--input` was used by mistake | Use the `ref:` prefix for audio |
| Duration mismatch | The audio is long but duration is short | Align duration with the audio's key section |
| Silent in the end | Videos carry no audio by default | Composite the reference audio back into the video in post |
| Conflicting generated audio | `--generate-audio` used together with ref audio | Pick one; in an audio-driven scenario turn generate-audio off |

---

## 8. Checklist

- [ ] The audio has a clear beat and a stable tempo
- [ ] `--input ref:@audio.mp3` uses the `ref:` prefix
- [ ] The prompt states "on the beat/beat-synced"
- [ ] The prompt provides 3-5 switchable picture elements
- [ ] `--duration` is aligned with the audio's key section
- [ ] Do not enable `--generate-audio` at the same time
- [ ] For sound in the end, go through post-production compositing

---

## Document revision history

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-07-18 | v1.0 | Initial topic plan | 小七 |
| 2026-07-18 | v1.1 | Noted that --generate-audio is supported only by 1.5-pro and the 2.0 series has no audio output | 小七 |
| 2026-08-01 | v1.2 | Correction: seedance-2.0 (260128) was measured to support --generate-audio; 2.0-fast/mini still have no audio | 小七 |
