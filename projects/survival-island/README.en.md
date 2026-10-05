# Project: Survival Island (survival-island)

> 🌐 Language: **English** | [中文](README.md)

> Back to the [project index](../README.en.md) ｜ technical methods in [../../methods/](../../methods/README.en.md)

---

## 1. Project background

- **Project name**: Survival Island (survival-island)
- **Core concept**: **the island is no wasteland — the person is worse off** -- extreme contrast. The tropical island is a paradise of emerald sea, white sand, coconut groves and blossoms; yet an Eastern girl of about eighteen, shipwrecked, in rags, sunburnt and cracked, staggers through this heaven-like island trying to survive. **The more beautiful the island, the more wretched the person — the contrast is the theme**.
- **Goal**: a ~30-second narrative short in 6 shots showing a day of survival — **landing on the island -> finding water -> lighting a fire -> building shelter -> spending the night watching the sea** — using the "paradise set beside hell" contrast to convey loneliness and resilience.
- **Publishing channels**:
  - Main film: portfolio / long-video platforms, horizontal 16:9
  - Derivative: short-video platforms, vertical 9:16 condensed cut
- **Delivery date**: 2026-07-25
- **Style and tone**: cinematic, 35mm film texture; **the island graded in a high-saturation warm-sun paradise palette, the person in a low-saturation cold, harsh palette**, with the same-frame contrast left un-reconciled

---

## 2. Deliverables

| # | Video use | Duration | Aspect ratio | Resolution | Notes |
|---|----------|------|------|--------|------|
| 1 | Main film (horizontal) | ~30s | 16:9 | 1080p | 6 shots × 5s, continuation |
| 2 | Vertical condensed cut | ~25s | 9:16 | 1080p | 5 selected shots, dropping shot 4 or 5 |

---

## 3. Method selection

### Overall strategy

There is **no ready-made footage** for the island scenes, so **T2V dominates**, conceiving the images from scratch; to keep the **protagonist consistent**, key shots use a **two-stage** approach (seedream generates a still as the first frame -> seedance I2V). Multiple shots are joined with [long-video-chain](../../methods/long-video-chain/README.en.md) continuation.

| # | Method used | Link | Input material |
|---|----------|------|----------|
| Shot 1/4/6 | Text-to-video T2V | [text-to-video](../../methods/text-to-video/README.en.md) | - |
| Shot 2/3/5 | Two-stage: image-to-video I2V | [image-to-video](../../methods/image-to-video/README.en.md) | seedream-generated first frame |
| Whole film | Camera movement | [cinematography](../../methods/cinematography/README.en.md) | - |
| Whole film | Long-video continuation | [long-video-chain](../../methods/long-video-chain/README.en.md) | `--return-last-frame` chain |
| Whole film | Quality and cost | [quality-and-cost](../../methods/quality-and-cost/README.en.md) | staged |
| Whole film | Content safety | [content-safety](../../methods/content-safety/README.en.md) | see the safety strategy below |

### Protagonist-consistency strategy (the core difficulty of narrative film)

With pure T2V the protagonist drifts across shots. Countermeasures:

1. **Fix a protagonist description prefix** (carried by every shot's prompt): `"一名约十八岁的东方少女，黑色长发凌乱披散，晒伤泛红的皮肤，干裂的嘴唇，破损的浅色长袖衬衫与长裤，浑身泥沙"`
2. **For I2V shots, first generate a first frame with a unified protagonist look using seedream**, then let seedance animate it (the first frame locks the subject)
3. **Fix `--seed` across the whole chain** to keep the style consistent
4. **When continuing, use the previous shot's real last frame** as the next shot's first frame, so the protagonist carries over naturally at the join

### Contrast devices (expressing the theme)

| Element | Island (paradise) | Person (hardship) |
|------|-----------|-----------|
| Saturation | High saturation | Low saturation |
| Colour temperature | Warm sun | Cold and harsh |
| Keywords | emerald sea, white sand, coconut grove, blossoms, clear stream, brilliant galaxy | rags, sunburn, cracked skin, mud, scrapes, trembling, curled up |
| Composition | postcard-wide openness | cramped, exhausted |

Set side by side in the same frame, **un-reconciled** -- this is the film's visual skeleton.

### Content-safety strategy (key to this film: the brutality must pass review)

Express the "brutality" through **review-safe symbols of hardship**, never touching the gore/nudity red lines. `--force` cannot bypass content moderation, so it must be controlled at the prompt source.

| To express | ✅ Safe wording | ❌ Wording to avoid (gets blocked) |
|--------|-----------|---------------------|
| Injury | covered in wounds, scrapes, sunburnt and peeling skin | bleeding, close-up of a wound, mangled flesh, severed limbs |
| Exhaustion | staggering, trembling, curled up, cracked skin | (nothing sensitive) |
| Torn clothing | torn shirt and trousers, in rags | revealing, skimpy, half-naked, see-through |
| Despair | tear tracks, despairing eyes | self-harm, hints of suicide |

Principles:
- The girl is a **fictional adult** character positioned as "resilient survival"; no glorified abuse or sexualised vulnerability
- Favour **face / hands / upper body** framing; avoid suggestive full-body compositions
- When blocked, rule items out one by one per [content-safety](../../methods/content-safety/README.en.md), preferring to soften concrete injury descriptions

---

## 4. Storyboard

> 6 shots × 5s = 30s main film. One camera move at a time; transitions are mostly continuation, with hard cuts to adjust the rhythm.

| Shot | Shot size | Camera move | Content | Duration | Transition | Method used |
|------|------|------|------|------|------|----------|
| 1 | Long shot | Aerial push-in | Emerald water rings a white-sand islet with coconut groves and blossoms; the girl drifts in the waves clutching a plank, out of place in this paradise island | 5s | Hard cut | T2V |
| 2 | Wide shot | Tracking shot | The girl staggers up onto the white beach in rags, a postcard coastline behind her | 5s | Continuation | I2V (first frame) |
| 3 | Medium shot | Follow move | Lush rainforest ablaze with blossoms; the girl parts the leaves and lunges at a clear stream, bending down to drink | 5s | Continuation | I2V (first frame) |
| 4 | Close-up | Static | The girl's scraped, trembling hands rub sticks to make fire; a flame catches and warm light falls on her wounds | 5s | Hard cut | T2V |
| 5 | Wide shot | Static time-lapse | A crude shelter rises among the coconut grove and flowers; the soft dusk light looks like a resort | 5s | Continuation | I2V (first frame) |
| 6 | Medium shot | Static night shot | Under a brilliant galaxy the girl curls up by the campfire gazing at the stars, in rags but with resolute eyes | 5s | Ending | T2V |

### Contrast arc

```
镜1 天堂海面   vs 漂流少女（孤绝）
镜2 天堂沙滩   vs 狼狈登岛（狼狈）
镜3 丰饶雨林   vs 干渴扑水（渴求）
镜4 暖光火苗   vs 伤痕双手（转机）
镜5 度假黄昏   vs 简陋庇护（安顿）
镜6 绝美银河   vs 蜷缩少女（坚毅）
```

---

## 5. Prompt & parameters

> Unified protagonist description prefix: `一名约十八岁的东方少女，黑色长发凌乱结块披散，晒伤脱皮泛红的皮肤，干裂起皮的嘴唇，衣衫褴褛的浅色长袖衬衫撕成碎条半挂在身上，长裤破洞遍布磨损成毛边，袖口裤脚散线，浑身泥污擦伤，狼狈不堪如落难乞丐`
> 🏝️ Island visual anchor (required in every shot, ensuring the same island across shots): `同一座热带孤岛：碧玉般海水环抱新月形白沙海岸，椰林摇曳，鸡蛋花与三角梅繁花似锦`
> Unified style suffix: `电影感，35mm 胶片质感，浅景深`
> Unified contrast device: high-saturation warm sun for the island, low-saturation cold for the person, un-reconciled in the same frame
> 🎯 **Actual model**: `doubao-seedance-2-0-mini-260615` (pay-as-you-go platform, `--profile platform_cn-beijing_accountwide`)
> ⚠️ mini does not support `--draft` / `--return-last-frame`; continuation switched to two-stage I2V (seedream generates the first frame)
> 🔇 mini has no audio output (`modalities.output` is video only), so this film's sound is synthesised in post (wave ambience + atmospheric music); see the audio design section

### Shot 1 (T2V · aerial push-in)

```bash
MODEL="doubao-seedance-2-0-mini-260615"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --ratio 16:9 --resolution 480p --duration 5 \
  "同一座热带孤岛：碧玉般海水环抱新月形白沙海岸，椰林摇曳，鸡蛋花与三角梅繁花似锦，航拍视角缓缓推近，海浪轻拍礁石，一名约十八岁的东方少女，黑色长发凌乱结块披散，晒伤脱皮泛红的皮肤，干裂起皮的嘴唇，衣衫褴褛的浅色长袖衬衫撕成碎条半挂在身上，长裤破洞遍布磨损成毛边，袖口裤脚散线，浑身泥污擦伤，狼狈不堪如落难乞丐，抱着木质浮板在浪中艰难漂流，与天堂般的孤岛格格不入，逆光，电影感，35mm 胶片质感，浅景深" \
  --open
```
- ⚠️ mini does not return last_frame; continuation uses two-stage I2V (see shot 2)

### Shot 2 (two-stage I2V · tracking shot)

```bash
# 先 seedream 生成主角登岛首帧（带岛锚点，保证与镜 1 同一座岛）
arkcli +gen --model doubao-seedream-5-0-260128 --size 1920x1080 \
  "同一座热带孤岛：碧玉般海水环抱新月形白沙海岸，椰林摇曳，鸡蛋花与三角梅繁花似锦，一名约十八岁的东方少女，黑色长发凌乱结块披散，晒伤脱皮泛红的皮肤，干裂起皮的嘴唇，衣衫褴褛的浅色长袖衬衫撕成碎条半挂在身上，长裤破洞遍布磨损成毛边，浑身泥污擦伤，狼狈不堪，跌坐在洁白沙滩上，背后是碧玉海水椰林明信片般海岸线，电影感，35mm 胶片质感" --open
# 满意后用静图当首帧
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @shot2_first.jpg --ratio 16:9 --resolution 480p --duration 5 \
  "镜头跟拍，少女跌跌撞撞在洁白沙滩上前行，衣衫褴褛碎条翻飞，海风吹动破损衣角，回头望向天堂般的大海，电影感，35mm 胶片质感，浅景深" \
  --open
```
- After seedream generates the first frame, save it as `shot2_first.jpg`; mini does not return last_frame, so shot 3 starts a new first frame for continuation

### Shot 3 (two-stage I2V · follow move)

```bash
arkcli +gen --model doubao-seedream-5-0-260128 --size 1920x1080 \
  "热带雨林郁郁葱葱繁花似锦阳光斑驳，一名约十八岁的东方少女站在丛林边缘，黑色长发凌乱，破损浅色衬衫长裤，电影感，35mm 胶片质感" --open
arkcli +gen --model "$MODEL" --input @shot3_first.jpg \
  --ratio 16:9 --resolution 1080p --duration 5 \
  "镜头跟移，少女拨开宽大热带树叶繁花走进雨林，扑向一条清澈溪流俯身饮水，光影斑驳" \
  --return-last-frame --open
```
- The last frame is downloaded as `shot5_first.jpg` (shot 4 is a T2V hard cut, so the last frame goes to shot 5)

### Shot 4 (T2V · static close-up)

```bash
arkcli +gen --model "$MODEL" --camera-fixed \
  --ratio 16:9 --resolution 1080p --duration 5 \
  "特写，一名少女擦伤泛红、沾满泥沙的双手在颤抖着快速钻木取火，木屑冒烟，火苗突然燃起，暖橙色光照亮手指上的伤痕，浅景深，固定镜头，电影感" \
  --open
```
- Hard cut, no continuation (a rhythmic beat)

### Shot 5 (two-stage I2V · static time-lapse)

```bash
arkcli +gen --model doubao-seedream-5-0-260128 --size 1920x1080 \
  "椰林花丛间用树枝和椰子叶搭起的简陋庇护所半成品，黄昏柔和暖光如度假村，碧海背景，电影感" --open
arkcli +gen --model "$MODEL" --input @shot5_first.jpg --camera-fixed \
  --ratio 16:9 --resolution 1080p --duration 5 \
  "固定镜头延时摄影，树枝椰叶庇护所在花丛间逐渐搭建完成，黄昏柔和光线快速变化，海浪起伏" \
  --return-last-frame --open
```
- The last frame is downloaded as `shot6_first.jpg`

### Shot 6 (T2V · static night shot)

```bash
arkcli +gen --model "$MODEL" --camera-fixed \
  --ratio 16:9 --resolution 1080p --duration 5 \
  "夜晚热带海滩，璀璨银河横跨夜空，篝火噼啪燃烧，一名约十八岁的东方少女衣衫褴褛蜷缩在火旁望向星空与大海，火光映在晒伤的脸上，眼神疲惫却坚毅，固定镜头，电影感，35mm 胶片质感" \
  --open
```

### Reproduction and consistency

- Fix `--seed 7` across the whole chain (locked during the direction test, reused for the final cut)
- Protagonist prefix, style suffix and contrast device are identical across all 6 shots
- I2V shot prompts describe **motion** only; appearance is left to the first frame

---

## 6. Execution plan

| Stage | Configuration | Purpose | Scope |
|------|------|------|------|
| Direction test | `--draft --resolution 480p` `seed=7` | Validate ① whether the contrast holds ② the girl's consistency ③ whether the "brutality" descriptions pass review | run all 6 shots once |
| Finalisation | `--resolution 720p` (drop draft) `seed=7` | Confirm the storyboard joins and the contrast arc | focus on shots 1/2/6 |
| Final cut | `--resolution 1080p --priority 9` `seed=7` | Produce the final, continuing shot by shot | 6 shots + ffmpeg concatenation |

> Use `doubao-seedance-2-0-fast` for the direction test to save money and time; switch to `doubao-seedance-2-0` for the final cut.
> See [quality-and-cost](../../methods/quality-and-cost/README.en.md).

### Continuation execution order

```
镜1(T2V) --末帧--> 镜2(I2V) --末帧--> 镜3(I2V)
                                          │ (镜4硬切，镜3末帧留给镜5)
                                          ▼
镜4(T2V,独立)   镜5(I2V,首帧=镜3末帧) --末帧--> 镜6(T2V 或 I2V)
```

> Between shot 3 and shot 5 there is a hard cut (shot 4's close-up is inserted in between); using shot 3's last frame directly as shot 5's first frame is enough to keep the scene coherent.

### Post-production concatenation

```bash
# 各镜统一 ratio/resolution/seed，可无损拼接
for f in shot1.mp4 shot2.mp4 shot3.mp4 shot4.mp4 shot5.mp4 shot6.mp4; do
  echo "file '$f'"
done > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy survival-island.mp4
```

---

## 7. Output log

| Shot | Version | task_id | local_path | Notes |
|------|------|---------|------------|------|
| 1 | v2 | cgt-20260718180426-rd7sm | out/shot1.mp4 | 480p direction test ✅; new prefix + island anchor; previous version out/shot1_v1.mp4 |
| 2 | v2 | cgt-20260718180428-wpfdk | out/shot2.mp4 | 480p direction test ✅; new prefix + island anchor; originally I2V, changed to T2V; previous version out/shot2_v1.mp4 |
| 3 | v1 | cgt-20260718175645-s4v2t | out/shot3.mp4 | 480p direction test ✅; new prefix + island anchor; originally I2V, changed to T2V (seedream not activated)|
| 4 | v1 | cgt-20260718174806-rfkp8 | out/shot4.mp4 | 480p direction test ✅; new prefix + island anchor |
| 5 | v1 | cgt-20260718180034-vtr4r | out/shot5.mp4 | 480p direction test ✅; new prefix + island anchor; originally I2V, changed to T2V (seedream not activated)|
| 6 | v1 | cgt-20260718175253-mj7zm | out/shot6.mp4 | 480p direction test ✅; new prefix + island anchor |

> Full concatenated preview: `out/survival_island_full.mp4` (6 shots × 5s ≈ 30s, 11MB, h264/864×496/24fps, silent track)
> Shots 1/2 were redone with the new prefix (v2), with the old v1 kept as backup; all 6 shots now share the unified new prefix + island anchor

> Fill task_id and local_path back in after each shot; `output_url` expires after 24h, so local_path is the source of truth.

---

## 8. Checklist

- [ ] All 6 shot prompts contain the unified protagonist prefix (Eastern girl) + style suffix
- [ ] Contrast device in place: high-saturation warm sun for the island vs low-saturation cold for the person, un-reconciled in the same frame
- [ ] "Brutality" uses only safe hardship symbols (scrapes / sunburn / rags / cracked skin / tear tracks), with **no gore or nudity** wording
- [ ] The girl is a fictional adult character; framing favours face/hands/upper body, with no suggestive full-body compositions
- [ ] I2V shot prompts describe motion only and do not repeat appearance
- [ ] `--seed 7` across the whole chain keeps the style consistent
- [ ] `--model` uses the full versioned ID (not the family name)
- [ ] Each shot's parameters are within `supported_params` (only 2.0 can enable `--priority` for the final cut)
- [ ] Executed in the three stages: direction test / finalisation / final cut
- [ ] Continuation uses the real last frame from `--return-last-frame`, not a separately chosen image
- [ ] Last-frame URLs are downloaded to disk immediately
- [ ] ratio/resolution unified across shots for lossless ffmpeg concatenation
- [ ] If blocked, rule items out one by one per [content-safety](../../methods/content-safety/README.en.md), preferring to soften injury descriptions

---

## 9. Audio design (narration voice-over)

> Because mini has no audio output, narration is done in post: TTS generates the narration → ffmpeg mixes it into the video.

### Narration script (narrating the contrast arc)

| Shot | Narration | Duration |
|------|------|------|
| 1 | A paradise island, and one forgotten soul. | 4.3s |
| 2 | She climbed onto the white sand, away from the sea, but not away from loneliness. | 4.8s |
| 3 | In a lush rainforest, she fought desperately for a single mouthful of water. | 3.9s |
| 4 | The moment the flame caught, despair became hope. | 4.3s |
| 5 | Dusk was as soft as a resort, yet she built tonight's bed from broken branches. | 4.7s |
| 6 | The galaxy blazed, and she curled up by the fire with an unquenchable light in her eyes. | 4.4s |

### TTS generation

- Model: `doubao-seed-tts-2.0` (Agent Plan, Resource-Id = `seed-tts-2.0`)
- Voice: `zh_female_vv_uranus_bigtts` (steady female narration voice)
- Script: `scripts/tts_narration.py` (calls the OpenSpeech streaming API, base64-decodes and concatenates)
- Output: `out/narration_<镜号>.mp3`

```bash
python3 scripts/tts_narration.py          # 生成全部 6 段旁白
```

### Mixing workflow

```bash
# 1. 每段旁白补静音到尾音，与视频时长对齐（5.088s）
for n in 1 2 3 4 5 6; do
  ffmpeg -i narration_$n.mp3 -af apad -t 5.088 narration_${n}_pad.mp3
done

# 2. 拼接 6 段成完整 30s 音轨（重编码避免 DTS 错乱）
printf "file 'narration_1_pad.mp3'\n...file 'narration_6_pad.mp3'\n" > concat_audio.txt
ffmpeg -f concat -safe 0 -i concat_audio.txt -c:a libmp3lame -b:a 128k narration_full.mp3

# 3. 混入视频（⚠️ 关键：不要重编码为 aac，播放器可能不识别！mp3 直塞 mp4 即可）
ffmpeg -i survival_island_full.mp4 -i narration_full.mp3 \
  -c:v copy -c:a copy -map 0:v -map 1:a -shortest survival_island_narrated.mp4
```

> Final: `out/survival_island_narrated.mp4` (30.8s, narrated version)
> ⚠️ In testing, re-encoding with `-c:a aac` left players silent (the track has data but fails to decode); `-c:a copy`, keeping the mp3 as-is, works.

---

## Revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-07-18 | v1.0 | Initial plan for Survival Island (6-shot, 30s narrative short) | 小七 |
| 2026-07-18 | v1.1 | Switched to an ~18-year-old Eastern girl + extreme contrast (the island is no wasteland, the person is worse off); added the contrast devices and content-safety strategy, rewrote all storyboards and prompts | 小七 |
| 2026-07-18 | v1.2 | Actually used doubao-seedance-2-0-mini-260615 (platform pay-as-you-go); noted that mini does not support draft/return-last-frame; logged the shot 1/2 outputs | 小七 |
| 2026-07-18 | v1.3 | Confirmed mini has no audio output (output is video only); sound switched to post-production synthesis | 小七 |
| 2026-07-18 | v1.4 | Strengthened the destitution prefix (shredded strips / holes / frayed edges / loose threads / mud and scrapes); added the island visual anchor to solve cross-shot environment consistency | 小七 |
| 2026-07-18 | v1.5 | All 6 direction-test shots finished; shots 3/5 switched to T2V because seedream was not activated; full concatenation survival_island_full.mp4; logged the profile routing (mini -> platform, the rest -> agent-plan)| 小七 |
| 2026-07-18 | v1.6 | Shots 1/2 redone with the new prefix + island anchor (v2), old versions kept as v1 backups; all 6 shots unified on the new prefix | 小七 |
| 2026-07-18 | v1.7 | Added the audio design: narration script + TTS generation (seed-tts-2.0) + ffmpeg mixing workflow; final survival_island_narrated.mp4 | 小七 |
| 2026-07-18 | v1.8 | Fixed the silent narration: mixing switched to `-c:a copy` (mp3 dropped straight into mp4); aac re-encoding made players fail to recognise it | 小七 |
