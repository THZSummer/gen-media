# Shifting Scenery v2 (step-scenery-v2)

> 🌐 Language: **English** | [中文](README.md)

> Back to the [project index](../README.en.md) ｜ technical methods in [../../methods/](../../methods/README.en.md)

A time-travelling girl · one step, one world (v2: seedance-2.0 single-pass 15s generation + native audio)

---

## 1. Project background

- **Project name**: step-scenery-v2 (Shifting Scenery v2)
- **Type**: time-travelling girl · visual spectacle short
- **Goal**: with every step the pure girl takes, the whole environment switches (tea room → bamboo grove → desert → cyber → starry sky → tea room, closing the loop). **Key v2 upgrade: seedance-2.0 generates the entire 15s video in a single pass** (not segment-by-segment concatenation), using `reference_audio` to carry native scene sound effects, with one continuous take whose camera moves connect naturally.
- **Publishing channels**: short-video platforms (Douyin / WeChat Channels / Bilibili vertical, or Xiaohongshu horizontal)
- **Delivery date**: TBD

> v1 is kept at [step-scenery/](../step-scenery/README.en.md) (mini version, 7×3s concatenation, silent so it needs post narration). v2 is independent: 15s × 5 storyboards generated in a single pass.
> 📚 Single-pass long video has been validated as feasible (2026-08-01): seedance-2.0 `--duration 15` succeeded in testing (15.07s single generation) and supports continuous multi-scene storytelling.

---

## 2. Deliverables

| # | Video use | Duration | Aspect ratio | Resolution |
|---|----------|------|------|--------|
| 1 | Main video (horizontal, single-pass generation + native sound effects) | 15s | 16:9 | starts at 480p, finalised at 720p |
| 2 | Vertical version (platform delivery) | 15s | 9:16 | starts at 480p, finalised at 720p |

> The resolution ceiling is a model limit (seedance-2.0 caps at 720p); see [quality-and-cost](../../methods/quality-and-cost/README.en.md).

---

## 3. Method selection

| # | Method used | Link | Input material |
|---|----------|------|----------|
| 1 | Text-to-image (reference image / keyframe) | [text-to-image](../../methods/text-to-image/README.en.md) | seedream-5.0-lite (v1 images reusable) |
| 2 | Text-to-video (single-pass 15s) | [text-to-video](../../methods/text-to-video/README.en.md) | - (pure prompt or reference_image) |
| 3 | Multimodal audio reference | [methods README multimodal section](../../methods/README.en.md) | reference_audio ambient sound |
| 4 | Speech synthesis (optional narration) | [text-to-speech](../../methods/text-to-speech/README.en.md) | seed-tts-2.0 |

> Design notes (v2.1 redesign):
> - **Single-pass 15s generation**: no segment-by-segment concatenation; the prompt describes the complete "shifting scenery" journey (tea room → bamboo grove → desert → cyber → starry sky → tea room) and `--duration 15` produces the film in one go, with camera moves and transitions handled by the model as one continuous take.
> - **Audio**: `reference_audio:@环境音参考` multimodal reference (✅ works in testing; the model transcribes the reference audio); after generation, use ffmpeg to boost it to an audible level.
> - **Model**: `doubao-seedance-2-0-260128` (platform pay-as-you-go).
> - **Reference image (optional)**: use `reference_image:@分镜图` to lock the character's look; or describe her purely in the prompt (in multimodal mode you cannot pass a first frame, but reference_image does not conflict).

---

## 4. Storyboard design (15s × 5 storyboards, one continuous take)

Theme motif: **shifting scenery**. 5 scenes switch continuously, about 3s each, as one continuous take with no cuts.

### 4.1 Overview table

| Storyboard | Time | Scene | Content | Native sound effects | Transition |
|------|------|------|------|----------|------|
| 1 | 0-3s | Tea room (reality) | The girl lies languidly on her side, then rises | Morning light, soft rustle of fabric | Rises and steps forward |
| 2 | 3-6s | Bamboo grove | One step into the bamboo grove, morning mist and bamboo shadows | Wind in the bamboo, birdsong | Step switches the scene |
| 3 | 6-9s | Desert | One step into the desert, heat haze rising | Desert wind, grains of sand | Step switches the scene |
| 4 | 9-12s | Cyber city | One step into the city's rainy night, neon | Rain, traffic, neon hum | Step switches the scene |
| 5 | 12-15s | Starry sky → tea room | One step onto the starry sky, then falling back into the tea room and opening her eyes | Galaxy hum → morning light | Scene switch + closure |

> Scene sequence: tea room (reality) → bamboo grove → desert → cyber city → starry sky → tea room (reality, closing the loop).
> One continuous take: the prompt describes "with every step she takes, the surrounding environment switches entirely to X"; the camera moves continuously without cuts.

### 4.2 Single-pass generation prompt (core)

```bash
MODEL="doubao-seedance-2-0-260128"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input "reference_image:@out/storyboard/shot1.jpg" \
  --ratio 16:9 --resolution 480p --duration 15 \
  --extra-body '{"generate_audio": true}' --wait \
  "电影级写实，时空奇观，一镜到底，移步换景：清纯东方少女（约十六七岁，婴儿肥鹅蛋脸，清澈眼眸，额心朱砂，高马尾发梢化开光尘，素纱水墨长裙，星髓珠耳坠），参考@图像1的人物形象；0-3秒她在素净茶室床榻慵懒侧卧，缓缓起身，晨光从纸窗透入；她迈出第一步，周围茶室轰然化作青翠竹林，晨雾缭绕竹叶簌簌飘落，她从容前行；她再迈一步，竹林退去化作无垠金黄沙漠，热浪蒸腾沙粒飞扬，裙摆在热风中轻扬；她继续迈步，沙漠炸开化作赛博都市雨夜，霓虹灯箱车流光轨，青绿品红霓虹照亮雨雾，雨滴在她伞沿飞溅；她抬步踏上星空，脚下化作浩瀚银河星海，星云青绿品红对冲，星辰环绕流转；最后她落入苍茫雪原又瞬间回到素净茶室床榻，睁开眼，瞳孔残留一线星河微光，梦境与现实重合；全程少女神情从容，一镜到底运镜丝滑连贯不卡顿，完全写实不卡通，音画同步：环境音效匹配画面（茶室静谧、竹林风声、沙漠风沙、都市雨声、星空空灵）"
```

> ⚠️ **Audio key point**: you must pass the request-body parameter explicitly with `--extra-body '{"generate_audio": true}'` (the `--generate-audio` flag did not map correctly in testing and the audio came out weak); the `reference_audio` reference actually lowers the volume, so **do not pass it**. If it is still weak after generation: `ffmpeg -i out.mp4 -af "volume=XdB" -c:v copy out_boosted.mp4`.

---

## 5. Prompt & parameters

### 5.0 Character design spec (reusing the v1/tea-shake-dance design)

```
真实的人类东方少女，约十六七岁，清纯懵懂稚气未脱，鹅蛋脸带一点婴儿肥，眼眸清澈无辜带水光，肌肤真实凝脂质感带毛孔与汗珠，健康元气不瘦削的少女体态，额心一点朱砂；
高马尾真实青丝，发梢化开成光尘；一身素纱水墨长裙，腰间纤细银河束带；
左耳一枚星髓珠耳坠（正常尺寸，珠内封存微型银河旋臂）；
她是一个人也是一个宇宙，外表清纯从容，世界在她脚下切换。
```

### 5.1 Ambient-sound reference preparation (ffmpeg synthesis, reusable)

```bash
# 竹林风声（粉噪+风感）
ffmpeg -f lavfi -i "anoisesrc=colour=pink:duration=15:amplitude=0.8" \
  -af "lowpass=f=1800,highpass=f=200,tremolo=f=0.8:d=0.6" -c:a libmp3lame out/audio/env_bamboo.mp3
# 雨声（白噪+低通调制）
ffmpeg -f lavfi -i "anoisesrc=colour=white:duration=15:amplitude=0.5" \
  -af "lowpass=f=4000,highpass=f=800,tremolo=f=3:d=0.4" -c:a libmp3lame out/audio/env_rain.mp3
# 沙漠风（粉噪+更重低通）
ffmpeg -f lavfi -i "anoisesrc=colour=pink:duration=15:amplitude=0.7" \
  -af "lowpass=f=1200,highpass=f=150,tremolo=f=0.5:d=0.8" -c:a libmp3lame out/audio/env_desert.mp3
```

> The model transcribes the sound effects from the reference audio so they follow the picture (✅ verified: the wind reference was 82% low-frequency → the generation came out 84%); alternatively, use one combined ambient-sound reference for the whole film.

---

## 6. Execution plan

| Stage | Configuration | Purpose |
|------|------|------|
| 1. Direction test | 480p 15s single pass (seedance-2.0) | Validate one-take scene switching + native sound effects |
| 2. Finalisation | 720p | Lock the plan |
| 3. Final cut | 720p + gain + optional narration | Produce the final, vertical crop |

> The single-pass 15s is the core of v2: **no concatenation, no editing** — the model handles every scene transition in one continuous take.

---

## 7. Output log

| Version | task_id | local_path | Notes |
|------|---------|------------|------|
| - | - | - | To be produced |

---

## 8. Checklist

- [x] Every video has a chosen method linked to methods/
- [x] Model IDs complete (doubao-seedance-2-0-260128)
- [ ] 15s single-pass generation succeeded (not concatenated)
- [ ] All 5 scene switches hold up + the continuous take connects naturally
- [ ] Character consistent (pure-girl anchor)
- [ ] Audio transcribed from the reference audio (not silent) and boosted to an audible level
- [ ] Parameters within the supported_params range
- [ ] Executed in stages (direction test → finalisation → final cut)
- [ ] Outputs saved to local_path (URLs expire after 24h)
- [ ] Content passed review (see [content-safety](../../methods/content-safety/README.en.md))

---

## Revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-08-01 | v2.0 | Project initialised: Shifting Scenery v2 (seedance-2.0 + generate-audio native audio, 7×3s segmented plan) | 小七 |
| 2026-08-01 | v2.1 | Redesigned: 15s total × 5 storyboards (3s each), the whole video generated in a single pass (--duration 15 verified successful); audio switched to a reference_audio multimodal reference (transcription verified); one continuous take with no concatenation | 小七 |
