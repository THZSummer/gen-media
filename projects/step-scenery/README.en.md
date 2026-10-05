# Shifting Scenery (step-scenery)

> 🌐 Language: **English** | [中文](README.md)

> Back to the [project index](../README.en.md) ｜ technical methods in [../../methods/](../../methods/README.en.md)

A girl travels through time and space: with every step the whole environment switches — one step, one world; a visual-spectacle short.

---

## 1. Project background

- **Project name**: step-scenery (shifting scenery)
- **Type**: time-travelling girl · visual spectacle short
- **Goal**: with every step a pure, innocent girl takes forward, the whole surroundings switch (bamboo grove → desert → cyber city → starry sky → snowfield → tea room) — one step, one world. The core selling point is the instantaneous spectacle of "the scenery changing the moment her foot lands", plus the girl's calm contrast amid the scene transitions.
- **Publishing channels**: short-video platforms (Douyin / WeChat Channels / Bilibili vertical, or Xiaohongshu horizontal)
- **Delivery date**: TBD (run a direction-validation pass first)

> Continuing the tea-shake-dance experience: character design spec first → storyboard review → I2V chained continuation → TTS narration.

---

## 2. Deliverables

| # | Video use | Duration | Aspect ratio | Resolution |
|---|----------|------|------|--------|
| 1 | Main video (horizontal) | 30s | 16:9 | starts at 480p, finalised at 720p |
| 2 | Vertical version (platform delivery) | 30s | 9:16 | starts at 480p, finalised at 720p |

> The resolution ceiling is a model limit (mini max 720p); see [quality-and-cost](../../methods/quality-and-cost/README.en.md).

---

## 3. Method selection

| # | Method used | Link | Input material |
|---|----------|------|----------|
| 1 | Text-to-image (storyboard image / keyframe) | [text-to-image](../../methods/text-to-image/README.en.md) | seedream-5.0-lite |
| 2 | Image-to-video (main path) | [image-to-video](../../methods/image-to-video/README.en.md) | storyboard image first.jpg |
| 3 | Long-video continuation (chained linking) | [long-video-chain](../../methods/long-video-chain/README.en.md) | last frame of the previous shot |
| 4 | Speech synthesis (narration voice-over) | [text-to-speech](../../methods/text-to-speech/README.en.md) | seed-tts-2.0 |

> Design notes (v1.0):
> - **Main path I2V**: the storyboard image serves as the first frame (seedream generates the image → review → I2V), so the visuals stay controllable.
> - **Chained continuation (v1.1 correction)**: ⚠️ **the video's last frame gets blocked as real-person privacy** (`InputImageSensitiveContentDetected.PrivacyInformation`; the last frame is judged to be a real human face). Correction from testing: **use a seedream storyboard image as the first frame for every shot** (storyboard images do not trigger real-person blocking), and achieve the scene-switch continuity through the prompt line "she takes one step and the whole environment switches to X" plus character-anchor consistency, rather than through the video's last frame.
> - **Model routing**: seedream-5.0-lite → agent-plan default; mini (I2V) → platform pay-as-you-go (`--profile platform_cn-beijing_accountwide`, full ID `doubao-seedance-2-0-mini-260615`).
> - **No audio-driven pass**: the scenery switch is beat-matched with the music in post, it is not audio-driven.

---

## 4. Storyboard

Theme motif: **shifting scenery**. 7 shots = one step, one world, paced as "suspense → chain of switches → big switch → rapid switches → waking close".

### 4.1 Overview table

| Shot | Rhythm section | Shot size | Camera move | One-line content | Scene switch | Duration | Transition | Method used |
|------|--------|------|------|------------|----------|------|------|----------|
| 1 | 🎣 Suspense opening | Face close-up | Slow push-in | A pure girl lying on her side, languid and innocent | Reality · tea room | 3s | Hard cut | I2V |
| 2 | ⚡ One step into the scene | Wide shot | Orbit | She takes one step and the surroundings burst into a bamboo grove | Tea room → bamboo grove | 5s | Continuation | I2V |
| 3 | Chain switch · two | Wide shot | Lateral track | One more step and the bamboo grove becomes a desert | Bamboo grove → desert | 5s | Continuation | I2V |
| 4 | Explosive switch · three | Medium close-up | Orbit + fast push-in | One step into the cyber city, neon bursting open | Desert → cyber | 5s | Continuation | I2V |
| 5 | Chain switch · four | Wide shot | Pull out | One step onto the starry sky, the galaxy under her feet | Cyber → starry sky | 5s | Continuation | I2V |
| 6 | Waking transition | Medium shot | Slow pull-back | One step into the snowfield, the wind and snow gradually dying | Starry sky → snowfield | 5s | Continuation | I2V |
| 7 | 🔁 Closure | Face close-up | Static | Back on the tea-room bed, eyes opening (links to shot 1) | Snowfield → tea room | 3s | Hard cut back to shot 1 | I2V |

> Continuation note: shots 2-6 continue from the previous shot's last frame, with the prompt stressing "she takes one step and the surrounding environment switches entirely" — the scenery changes the moment her foot lands.
> Core contrast: the girl stays pure and composed throughout while the world switches rapidly beneath her feet — "the whole world changes, only she is unshaken".
> Total duration 31s.
> Scene sequence: tea room (reality) → bamboo grove → desert → cyber city → starry sky → snowfield → tea room (reality, closing the loop).

### 4.2 Shot-by-shot breakdown (director's cut)

Each shot gives: **action breakdown**, **scene switch (core)**, **camera and mood**, **targeted prompt**.

#### Shot 1 | 🎣 Suspense opening (tea room · languid, lying on her side)

- **Action breakdown**: the girl lies on her side on the tea-room bed, languidly propping her cheek on one hand, her eyes clear and innocently wide (the same opening positioning as tea-shake-dance, establishing the character)
- **Scene switch**: reality · a plain tea room, morning light, no cosmic elements
- **Camera and mood**: big close-up on the face with a slow push-in — suspense: "where is she going?"
- **Prompt**: `电影级写实，真实人物摄影：真实的人类东方少女，约十六七岁，清纯懵懂稚气未脱，鹅蛋脸带一点婴儿肥，眼眸清澈无辜带着水光，慵懒地侧卧在茶室床榻上，一只手托腮，眼神好奇懵懂地望向前方，唇瓣微抿，肌肤真实凝脂质感，额心一点朱砂；镜头缓缓推近她的面部，清澈眼眸与婴儿肥脸颊占据画面中心；背景是素净茶室，柔和晨光从纸窗透入，极简留白；史诗级电影布光，完全写实不卡通`

#### Shot 2 | ⚡ One step into the scene (tea room → bamboo grove)

- **Action breakdown**: she slowly rises and takes her first step — the instant her foot lands, the tea room bursts into a bamboo grove
- **Scene switch**: tea room (reality) → bamboo grove (lush green, morning mist, swaying bamboo shadows)
- **Camera and mood**: wide-shot orbit; the scenery switches on her very first step — the audience sees the "shifting scenery" spectacle for the first time
- **Prompt**: `电影级写实，时空奇观：延续上一镜的清纯东方少女（同面容同装扮），她缓缓起身向前迈出一步，脚落地的瞬间，周围素净茶室轰然化作青翠竹林，晨雾缭绕，竹影摇曳，竹叶簌簌飘落，阳光透过竹隙洒下光柱；少女站在竹林中央，神情从容好奇，仿佛世界为她让路；史诗级电影布光，青绿竹海色调，完全写实不卡通`

#### Shot 3 | Chain switch · two (bamboo grove → desert)

- **Action breakdown**: she takes another step; the bamboo grove recedes and the ground beneath her becomes an endless desert
- **Scene switch**: bamboo grove → desert (golden dunes, heat haze, lone smoke over the waste)
- **Camera and mood**: wide shot with a lateral track; the second switch — steady rhythm, and the audience starts anticipating the next scene
- **Prompt**: `电影级写实，时空奇观：延续上一镜的清纯东方少女（同面容同装扮），她再向前迈出一步，脚落地的瞬间，周围青翠竹林退去，脚下化作无垠金黄沙漠，热浪蒸腾，大漠孤烟直，沙丘起伏连绵；少女立于沙海中央，裙摆在热风中轻扬，神情依旧从容；史诗级电影布光，金黄暖色与青绿服饰对比，完全写实不卡通`

#### Shot 4 | Explosive switch · three (desert → cyber city)

- **Action breakdown**: she strides forward; the desert bursts apart and a neon city rises from every direction
- **Scene switch**: desert → cyber city (neon light boxes, glass curtain walls, car light trails, rainy night)
- **Camera and mood**: medium close-up, orbit with a fast push-in; the third switch is the explosion point — the ultimate contrast from desolation to bustle
- **Prompt**: `电影级写实，时空奇观：延续上一镜的清纯东方少女（同面容同装扮），她大步向前迈出，脚落地的瞬间，沙漠轰然炸开，赛博都市从四面八方升起——霓虹灯箱、玻璃幕墙、车流光轨、雨夜霓虹，青绿与品红霓虹对冲；少女立于霓虹雨夜街头，清纯的脸与赛博都市形成极致反差，雨滴在她伞沿飞溅；史诗级电影布光，赛博朋克美学，完全写实不卡通`

#### Shot 5 | Chain switch · four (cyber → starry sky)

- **Action breakdown**: she lifts her foot lightly; the neon beneath recedes and becomes a vast starry sky
- **Scene switch**: cyber city → starry sky (deep-space nebula, galactic spiral arms, stardust underfoot)
- **Camera and mood**: wide shot pulling out; the fourth switch — a leap in scale from the ground to the cosmos
- **Prompt**: `电影级写实，时空奇观：延续上一镜的清纯东方少女（同面容同装扮），她轻轻抬步向前迈出，脚落地的瞬间，脚下赛博都市霓虹退去，化作浩瀚星空，她悬浮于深空星海之上，脚下是旋转的银河旋臂与星尘，星云青绿品红对冲，亿万星辰环绕她流转；少女立于星河中央，素纱裙摆在星光中飘动，神情静谧；史诗级电影布光，宇宙级意象，完全写实不卡通`

#### Shot 6 | Waking transition (starry sky → snowfield)

- **Action breakdown**: she slowly sets a step down; the sea of stars dims and the ground becomes a snowfield as the wind and snow die away
- **Scene switch**: starry sky → snowfield (vast snow, falling flakes, cold-toned morning light)
- **Camera and mood**: medium shot with a slow pull-back; after the fifth switch the mood falls back — the dream begins to close
- **Prompt**: `电影级写实，时空奇观：延续上一镜的清纯东方少女（同面容同装扮），她缓缓落下一步，脚落地的瞬间，脚下星海渐暗消散，化作苍茫雪原，漫天雪花飘落，冷色调晨光洒在雪地上，远山轮廓隐约；少女立于雪原中央，哈气成雾，神情安详，仿佛梦即将醒来；史诗级电影布光，清冷银白与素纱裙对比，完全写实不卡通，留白氛围`

#### Shot 7 | 🔁 Closure (snowfield → tea room)

- **Action breakdown**: the snowfield fades; she is back on the tea-room bed and suddenly opens her eyes (links to shot 1)
- **Scene switch**: snowfield → tea room (reality, closing the loop)
- **Camera and mood**: static face close-up; the waking twist — "one step, one world, and it was all a dream"
- **Prompt**: `电影级写实，真实人物摄影，清晨梦醒瞬间：延续人物，清纯东方少女躺在现实素净的茶室床榻上，素色棉被，柔和晨光从纸窗透入；她突然睁开眼睛，眼神清澈无辜，瞳孔中残存一线微弱的星尘光点（梦的余韵）；她的侧卧姿态与开场第一镜完全呼应，同一个少女同一张脸；史诗级电影布光，柔和自然光，完全写实不卡通，留白氛围`

---

## 5. Prompt & parameters

### 5.0 Character design spec (reusing the mature tea-shake-dance design)

> 📖 The same "pure girl × microscopic universe" character design continues to be used, ensuring cross-project consistency and fast image generation.

```
真实的人类东方少女，约十六七岁，清纯懵懂稚气未脱，鹅蛋脸带一点婴儿肥，眼眸清澈无辜带水光，肌肤真实凝脂质感带毛孔与汗珠，健康元气不瘦削的少女体态，额心一点朱砂；
高马尾真实青丝，发梢化开成光尘；一身素纱水墨长裙，腰间纤细银河束带，裙摆边缘化开成星尘；
左耳一枚星髓珠耳坠（正常尺寸，珠内封存微型银河旋臂），颈间星链，右腕星环臂钏，左手无名指黑洞戒；
她是一个人也是一个宇宙，外表清纯从容，世界在她脚下切换。
```

> ⚠️ Note: this project's "shifting scenery" core is the **scene switch**; the character only needs to stay pure and composed (no furious expression needed), which distinguishes her from the "world-destroying fury" persona of tea-shake-dance.

### 5.1 Generation command template

```bash
# 分镜图（seedream，agent-plan）
MODEL="doubao-seedream-5-0-lite"
arkcli +gen --model "$MODEL" --size "2560x1440" --output-format jpeg \
  "<人物锚点> <该镜场景切换描述>" --save-to out/storyboard/

# 视频（mini，platform 按量）
MODEL="doubao-seedance-2-0-mini-260615"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @out/storyboard/shot<N>.jpg --ratio 16:9 --resolution 480p --duration 5 --wait \
  "<该镜 Prompt>" 
# 链式续接：下一镜 --input 用上一镜末帧（ffmpeg -sseof -0.1 抽取）
```

> ⚠️ For image aspect ratio use `--size` (`--ratio` is video-only); the `--size` pixel floor is 3,686,400 (use 2560×1440).

---

## 6. Execution plan

| Stage | Configuration | Purpose |
|------|------|------|
| 0. Storyboard | seedream-5.0-lite, produce 7 keyframes | Review the visuals first: character consistency + whether the 6 scenes hold up |
| 1. Direction test | 480p chained I2V (first frame = storyboard image / previous shot's last frame) | Validate whether the "shifting scenery" switch moment holds up |
| 2. Finalisation | 720p | Lock the plan, add beat-matched music |
| 3. Final cut | 720p + post | Concatenate the final film, narration/music, vertical crop |

> ⚠️ mini does not support `--draft`, so run the direction test straight at 480p; for cost and limits see [quality-and-cost](../../methods/quality-and-cost/README.en.md).

---

## 7. Output log

| Shot | Version | task_id | local_path | Notes |
|------|------|---------|------------|------|
| 1 | v1 | cgt-20260801190751-fzt7g | out/video/shot1.mp4 | Suspense opening · lying on her side in the tea room |
| 2 | v1 | cgt-20260801191244-66vrd | out/video/shot2.mp4 | One step into the scene · tea room → bamboo grove |
| 3 | v1 | cgt-20260801191551-2mhnv | out/video/shot3.mp4 | Chain switch · bamboo grove → desert |
| 4 | v1 | cgt-20260801191837-grr8d | out/video/shot4.mp4 | Explosive switch · desert → cyber city |
| 5 | v1 | cgt-20260801192109-t6drc | out/video/shot5.mp4 | Chain switch · cyber → starry sky |
| 6 | v1 | cgt-20260801192351-wrxnz | out/video/shot6.mp4 | Waking transition · starry sky → snowfield |
| 7 | v1 | cgt-20260801192732-zgzjx | out/video/shot7.mp4 | Closure · snowfield → tea room, eyes opening |

> Direction versions of all 7 shots are generated (480p / 864×496 / 5.09s / mini-260615 / platform pay-as-you-go); the full film is `out/video/step_scenery_full.mp4` (35.6s).
> All 7 storyboard images (`out/storyboard/shot1-7.jpg`, 2560×1440) are generated.

---

## 8. Checklist

- [x] Every video has a chosen method linked to methods/
- [x] Prompts written according to the method README strategy
- [x] Model IDs complete (doubao-seedance-2-0-mini-260615 / doubao-seedream-5-0-lite)
- [ ] Storyboard images generated and passed review (see §4)
- [ ] Character consistent across the 7 shots (pure girl + star-marrow pearl earring anchor)
- [ ] All 6 scene switches hold up (tea room / bamboo grove / desert / cyber / starry sky / snowfield)
- [ ] Parameters within the supported_params range
- [ ] Executed in stages (storyboard → direction test → finalisation → final cut)
- [ ] Outputs saved to local_path (URLs expire after 24h)
- [ ] Content passed review (see [content-safety](../../methods/content-safety/README.en.md))

---

## Revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-08-01 | v1.0 | Project initialised: "Shifting Scenery", a time-travelling girl, 7 shots / 31s, one step one world (tea room → bamboo grove → desert → cyber → starry sky → snowfield → tea room, closing the loop), reusing the tea-shake-dance character design and chained workflow | 小七 |
| 2026-08-01 | v1.1 | Correction from testing: the video's last frame triggers real-person privacy blocking, so chained continuation switched to "each shot uses a seedream storyboard image as the first frame + prompt describing the scene switch"; all 7 storyboard images and videos generated; full film step_scenery_full.mp4 | 小七 |
