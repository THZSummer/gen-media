# Shake a Good Cup of Tea (tea-shake-dance)

> 🌐 Language: **English** | [中文](README.md)

> Back to the [project index](../README.en.md) ｜ technical methods in [../../methods/](../../methods/README.en.md)

An art-dance short: with "shake it" as the movement motif, it dances tea culture (the tea liquor, its aroma, the brewing gestures) into a modern dance piece.

---

## 1. Project background

- **Project name**: tea-shake-dance (Shake a Good Cup of Tea)
- **Type**: art-dance video
- **Goal**: a modern-dance short of about 30s that abstracts the gestures of "brewing / shaking tea" into dance vocabulary — the swirl of the tea liquor, the haze of its aroma, the rocking of the cup all become the dancer's body language. A concept/atmosphere-led short, with no narrative plot.
- **Publishing channels**: short-video platforms (Douyin / WeChat Channels / Bilibili vertical, or Xiaohongshu horizontal)
- **Delivery date**: TBD (run a direction-validation pass first)

---

## 2. Deliverables

| # | Video use | Duration | Aspect ratio | Resolution |
|---|----------|------|------|--------|
| 1 | Main video (horizontal, concept version) | 30s | 16:9 | starts at 480p, finalised at 720p |
| 2 | Vertical version (platform delivery) | 30s | 9:16 | starts at 480p, finalised at 720p |

> The resolution ceiling is a model limit (mini max 720p; 1080p requires a model upgrade); see [quality-and-cost](../../methods/quality-and-cost/README.en.md).

---

## 3. Method selection

| # | Method used | Link | Input material |
|---|----------|------|----------|
| 0 | Storyboard image (keyframe, review the visuals first) | [image-to-video first frame](../../methods/image-to-video/README.en.md) | seedream-5.0-lite generation |
| 1 | Image-to-video (main path) | [image-to-video](../../methods/image-to-video/README.en.md) | storyboard image first.jpg |
| 2 | Text-to-video (fallback / pick-up shots) | [text-to-video](../../methods/text-to-video/README.en.md) | - |
| 3 | Audio-driven (optional, beat-matching the music) | [audio-driven](../../methods/audio-driven/README.en.md) | reference audio (tea ceremony / ancient style / electronic) |
| 4 | Reference video (optional, motion transfer) | [reference-video](../../methods/reference-video/README.en.md) | reference dance video |
| 5 | Multi-shot continuation (concatenation into the final film) | [long-video-chain](../../methods/long-video-chain/README.en.md) | each shot's local_path |

> Design notes (updated 2026-08-01):
> - **✅ seedream-5.0-lite is activated** (agent-plan default profile; image generation verified): the storyboard + I2V-first-frame path is unlocked. **Workflow upgrade: seedream produces the 6 keyframes first → human review of the visuals → then I2V brings them to life**, avoiding rework from going straight to T2V.
> - **Main path switched to I2V**: using the approved storyboard image as the first frame, I2V animates it (motion consistency is far better than pure T2V).
> - **audio-driven**: if you want the shot changes cut on the beat, drive them with reference audio; ⛔ mini does not support `--generate-audio` (output is video only), so audio must be synthesised in post (reusing the survival-island TTS/mixing workflow).
> - **R2V**: to let a dance move "borrow the motion and swap the content" (change costume/scene), the `doubao-seedance-2-0-r2v` model is required; its activation status is unverified, **to be confirmed**.
> - **Model routing**: seedream-5.0-lite → agent-plan default profile; mini (I2V/T2V) → platform pay-as-you-go (`--profile platform_cn-beijing_accountwide`).

---

## 4. Storyboard

Theme motif: **shake it**. Story structure (v4): a **dream loop** — suspense opening (a pure girl) → dream eruption (cosmic dance) → waking closure (eyes opening on the bed, linking to shot 1). The whole cosmic miracle is a dream, with the ends joined.

> 💥 Three elements of the hook: ① a suspense hook in the first 3 seconds (shot 1's pure face close-up); ② extreme contrast (shot 2, the same face in world-destroying fury); ③ a loop-closing twist (shot 7, waking and opening her eyes, so the audience realises "it was a dream").
> 🌌 **Core selling point (carried over from the v2 final): mastery over time and space** — in the dream the environment is a causal extension of the character's actions: a step swaps the stars, a raised hand extinguishes the galaxy, a raised cup sets the galaxy spinning.
> 🎨 Visual hammer: in the dream, deep-space nebula cyan-green × magenta opposition; in reality, a plain bed (strongly contrasted with the dream, highlighting the "waking up").

### 4.1 Overview table

| Shot | Rhythm section | Shot size | Camera move | One-line content | Environment | Duration | Transition | Method used |
|------|--------|------|------|------------|------|------|------|----------|
| 1 | 🎣 Suspense opening | Face close-up | Slow push-in | A pure girl lying languidly on her side, big close-up on her face, naive and innocent | Reality · dark minimal (suspense) | 3s | Hard cut | T2V |
| 2 | ⚡ Extreme contrast | Medium close-up | Orbit + fast push-in | The same face suddenly in fury, the galaxy destroying the world | Dream · nebula eruption | 5s | Hard cut | T2V |
| 3 | Rising · develop | Medium shot | Orbit | Wrist circling to shake the tea, the galaxy's spiral arm pulled along | Dream · galactic spiral arm | 5s | Hard cut | T2V |
| 4 | ⚡ Eruption · turn | Medium close-up | Lateral track + hard stop | Spinning combo + flinging the tea, the galaxy explodes | Dream · supernova eruption | 5s | Hard cut | T2V |
| 5 | Quick cuts · rhythm | Close-up ×3 | Static, cut in sequence | Three beat-matched cuts on the downbeat: pinch the cup / tilt the cup / splash the tea | Dream · stardust gathering and scattering | 5s | Hard cut | T2V |
| 6 | Waking transition | Close-up → wide shot | Slow pull-back | The dream's energy spirals in and contracts, the sea of stars dimming | Dream → reality transition | 4s | Dissolve | T2V |
| 7 | 🔁 Loop-closing twist | Face close-up | Static | Reality, on the bed; the girl suddenly opens her eyes (links to shot 1) | Reality · plain bed | 3s | Hard cut back to shot 1 | T2V |

> Transition notes: shot 1's suspense opening (the pure girl lying on her side, hooking first) → shot 2's extreme contrast (the same face in world-destroying fury, exploding first) → shots 3-5, the dream dance rising / exploding again / quick cuts → shot 6, the dream's energy contracting and dimming (dissolve back to reality) → shot 7, **waking and opening her eyes**, the instant she opens them hard-cutting back to shot 1's side-lying close-up — the audience realises: the opening was her just waking / about to sleep, so the ends close the loop.
> Core contrast logic: **the more pure and innocent shot 1 is, the more astonishing shot 2 becomes**; **shots 6-7 deliver the waking twist — the whole cosmic miracle was only a dream**.
> Total duration 30s.
> 📦 Version evolution: v1-classic (calm tea room) → v1.5-cyber-ink (cyber ink) → v2-astro (mastery over time and space) → v3 spec (real girl × microscopic universe) → **v4 dream loop (current)**.

### 4.3 Storyboard image (keyframe) generation and review

**Why generate images first**: with direct T2V you only see after generation whether the visuals / costume / scene / composition match expectations, and rework is expensive (one 5s video ≈ several tokens + time). Use seedream to produce **each shot's keyframe (storyboard image)** first, review the composition, style and subject consistency by hand, and only then bring it to life with I2V — when the visuals miss, you only regenerate the image, at an order of magnitude less cost.

**Generation command** (model `doubao-seedream-5-0-lite`, default agent-plan profile):

```bash
MODEL="doubao-seedream-5-0-lite"
# 镜号 N 的分镜图：prompt = 通用锚点 + 该镜静止姿态描述（取 §4.2 每镜"姿态/手位"定格）
# ⚠️ 图片比例用 --size（像素）不用 --ratio（--ratio 仅视频有效，忽略后默认 2048x2048 正方形）
arkcli +gen --model "$MODEL" --size "2560x1440" --output-format jpeg \
  "<通用视觉锚点> <该镜关键姿态描述，如：舞者双手捧盏低头凝神，茶烟升腾，淡雅茶室，青绿水墨色调，留白氛围>" \
  --save-to out/storyboard/
```

> Tip: the storyboard image captures **the shot's most representative static instant** (such as shot 1's "flinging the tea tears the galaxy apart" or shot 4's "galaxy exploding"), not a dynamic process; motion is left to I2V.
> 📦 Version archive (all kept for reference): `v1-classic/` (calm tea room) / `v1.5-cyber-ink/` (cyber ink) / `v2-astro/` (mastery over time and space) / `v3-spec-iterations/` (spec iteration versions) / the current final `shot1-7_final.jpg` (all 7 shots of the v4 dream loop).
> For the vertical storyboard images, generate a separate set with `--size "1440x2560"` (9:16) (aspect ratio affects composition; you cannot just hard-crop a horizontal image).

**Review checklist** (check item by item when a shot's image comes through; regenerate if it fails):

- [ ] Dancer's look consistent: high ponytail with hair flying, off-shoulder ink-gradient long dress, Eastern woman, vivid expression (same across all 6 shots)
- [ ] Background consistent: modern neon teahouse at night (glass curtain wall / cyan-green + magenta neon / mist)
- [ ] Era contrast: classical dancer × futuristic neon in one frame holds up (core selling point)
- [ ] Composition matches the shot's framing (medium close-up / wide / medium / close-up / close-up ×3 / close-up → medium close-up)
- [ ] Tea elements land correctly (glowing splash arc / glowing tea liquor / swirl / explosion / three quick cuts / settling back to catch the cup)
- [ ] Poses match the shot's key hand positions in §4.2 (fling the cup airborne / hold the cup / circle the wrist / fling the tea and explode / pinch, tilt, splash / draw the cup back and look over the shoulder)

> Once all 6 shots pass review, each shot uses `shot<N>_v2_astro.jpg` as its I2V first frame (`--input @shotN_v2_astro.jpg`) and moves into video generation.

### 4.2 Shot-by-shot breakdown (director's cut)

Each shot gives: **action breakdown** (beat by beat, split over 0-5s), **pose / hand position / centre of gravity**, **environment / dream linkage**, **camera and mood**, **targeted prompt**.

#### Shot 1 | 🎣 Suspense opening (pure girl · languid, lying on her side)

> The 3-second suspense hook: **show no cosmic elements at all**, just the pure, innocent face of a girl, making the audience wonder "who is she, what is she about to do". **Environment: reality, dark and minimal.**

- **Action breakdown**:
  - 0-1s: the girl lies languidly on her side, one hand under her cheek, gazing forward with clear, innocent eyes (big close-up on her face)
  - 1-2s: the camera pushes in slowly; her face fills most of the frame, the watery light in her eyes, the baby fat, the vermilion mark at the centre of her forehead all clear
  - 2-3s: her lips press slightly, a hint of light dust flickers at the tip of her hair (the film's only supernatural hint, planting the suspense)
- **Pose / hand position**: lying on her side with a hand under her cheek (languid as a kitten) → naive gaze (curious)
- **Environment**: reality · dark minimal background, only the faintest stardust points (suspense, never stealing the scene)
- **Camera and mood**: big close-up on the face with a slow push-in; the mood is pure, languid, innocent — "what is such a lovely girl about to do?"
- **Prompt**: `电影级写实照片，真实人物摄影，慵懒纯净质感，面部大特写：真实的人类东方少女，约十六七岁，清纯懵懂稚气未脱，鹅蛋脸带一点婴儿肥，眼眸清澈无辜带着水光，慵懒地侧卧着，一只手托腮，眼神好奇懵懂地望向前方，唇瓣微抿，真实肌肤凝脂质感带毛孔与薄汗，额心一点朱砂；镜头推得很近，她的面部占据画面绝大部分，清澈的眼眸、婴儿肥的脸颊、微抿的唇、额心朱砂都是焦点；画面边缘保留她侧卧姿态的局部：托腮的手、垂落的几缕真实发丝搭在肩头、素纱衣领与肩颈的柔和线条、裙摆边缘微微化开成一点光尘；背景是极简的暗色虚化，只有极其细微的星尘光点若隐若现；她看起来就像一个不谙世事的邻家少女，纯净、慵懒、无辜、惹人怜爱；史诗级电影布光，柔和侧光勾勒面部轮廓，超高细节，8k摄影质感，完全写实不卡通，留白氛围`

#### Shot 2 | ⚡ Extreme contrast (the same face · world-destroying fury)

> The same face suddenly erupts: **the more pure shot 1 is, the more astonishing shot 2 becomes**. **Environment: dream, nebula eruption.**

- **Action breakdown**:
  - 0-1s: the same pure face, her eyes suddenly radiating a destructive, arrogant divine light (expression flips)
  - 1-3s: mouth open in a shout, hand flung out to hurl the tea cup, the nebula tea liquor splashing and exploding into a supernova
  - 3-5s: hair, hem and light dust all explode at once; the deep-space nebula behind her tears and flickers with her roar
- **Pose / hand position**: expression flips (pure → arrogant) → hurling the cup and shouting (wrist drives the force) → freeze on the explosion
- **Environment / dream linkage**: flinging the tea → the nebula explodes into a supernova; roaring → the nebula tears and flickers
- **Camera and mood**: medium close-up, orbit with a fast push-in; the mood spikes instantly — explosive, contrasting, unstoppable
- **Prompt**: `电影级写实照片，真实人物摄影，神性威严与纯真反差：真实的人类东方少女，约十六七岁，清纯懵懂稚气未脱，鹅蛋脸带一点婴儿肥，眼眸清澈无辜此刻却透出毁灭性的狂傲神光，眼尾上挑，真实肌肤凝脂质感带毛孔与薄汗，额心一点朱砂，她张口呐喊，清纯的脸与狂暴的动作形成极致反差；健康元气不瘦削的少女体态，匀称饱满；真实青丝高束马尾，发梢化开成光尘炸开，发间一支彗尾银簪；她耳畔垂着一枚正常尺寸的星髓珠耳坠——直径约两厘米如一颗大珍珠，半透明珠体内封存着一整条微型银河旋臂，青绿与品红星云在珠内剧烈旋转，珠体辉光迸发，物小意大；颈间星链坠着微缩恒星，右腕星环臂钏，左手正常戒指戒面是微型黑洞；她身着一身改良水墨长裙素纱为底，领口袖口衣摆用极细星尘线绣出星座图谱，腰间纤细银河束带泛青白微光，衣摆边缘化开成星尘又凝回布料；手中握一只温润青瓷茶盏，盏中盛着流动的星云茶汤；她扬手甩出茶盏，星云茶汤泼溅炸开化作超新星爆发，发丝衣摆光尘同时炸开，身后深空星云随着她的咆哮撕裂明灭，青绿品红对冲、明暗层次、颗粒感、体积光，她是一个人也是一个宇宙，外表是清纯元气的邻家少女，狂时如神怒星河为之明灭，史诗级电影布光，超高细节，8k摄影质感，完全写实不卡通，比例协调`

#### Shot 3 | Rising · develop (wrist circling to shake the tea · galactic spiral arm)

> The dream hits its stride. **Environment: dream, the wrist is the axis of the galaxy.**

- **Action breakdown**:
  - 0-2s: cup in her right hand, the wrist begins to circle — forearm as the axis, the wrist drawing a circle (the start of the tea shake)
  - 2-4s: the circling widens, turning fabric and hair into swirling stardust, while her left arm stretches the other way, pulling the star stream on the opposite side
  - 4-5s: both hands circle in turn, her body pivoting half a turn with the motion, and the galactic spiral arm speeds up
- **Pose / hand position**: cup in hand, wrist circling (elbow fixed, wrist drawing circles) → both arms counter-rotating (the wrist drives the galaxy)
- **Environment / dream linkage**: the wrist = the galaxy's axis — the nebula is pulled into a huge spiral arm, stardust flying around her like silk ribbons
- **Camera and mood**: medium shot with an orbit (the camera circles half-way around the dancer); the mood rises again from stillness — nimble, flowing, hitting its stride
- **Prompt**: `宇宙级意象，时空主宰：充满力量感的现代东方舞者，高马尾长发扬起发丝化作星尘轨迹，皮肤真实质感带汗珠，表情专注投入；宽松飘逸改良水墨渐变长裙，露肩设计；她悬浮于浩瀚星海中央，是宇宙的中心——右手持青瓷茶盏手腕画圆旋绕，盏中发光茶汤旋成小漩涡，整个星系随之旋转，周围星云被牵引成巨大旋臂，星尘如绸带绕她环绕飞舞，左臂反向舒展带动另一侧星流呼应，仿佛她的手腕就是银河的轴心，时间与空间都随主体人物而动，深空星云青绿与品红对冲，史诗级电影打光，超高对比度，真实人物摄影质感`

#### Shot 4 | ⚡ Eruption · turn (spinning combo + galaxy exploding)

> The film's biggest explosion: echoing shot 2's "tea fling", this time the whole galaxy explodes with her — the emotional peak. **Environment: dream, one turn and the universe restarts.**

- **Action breakdown**:
  - 0-2s: the dancer bends low to gather force, both arms rising from below as if pouring water (low → high, winding up)
  - 2-4s: using the momentum she spins through a combo (more than two turns), the skirt flaring wide, hand flung out to sling the tea
  - 4-5s: the galaxy explodes with it, billions of stars scattering like a supernova, the dancer freezing in a half-crouch as she settles
- **Pose / hand position**: bending to gather force (low centre of gravity) → spinning combo (centrifugal extension) → freezing on the tea fling (arm like a whip, wrist exploding)
- **Environment / dream linkage**: one turn and the universe restarts — the nebula collapses into a vortex then bursts open, space is torn into cracks, and the glowing tea liquor becomes a waterfall of stardust
- **Camera and mood**: medium close-up, lateral track with a hard stop (following the hand's path then stopping abruptly); the mood is pushed to its peak — eruption, tension
- **Prompt**: `宇宙级意象，时空主宰：充满力量感的现代东方舞者，高马尾长发扬起发丝化作星尘炸开，皮肤真实质感带汗珠，张口呐喊表情爆发；宽松飘逸改良水墨渐变长裙，露肩设计，旋转时裙摆炸开翻飞；她悬浮于浩瀚星海中央，是宇宙的中心——俯身蓄力后旋转连击，扬手甩出青瓷茶盏的瞬间，整个星系随她的爆发而炸裂，星云坍缩成漩涡又轰然炸开，亿万星辰四散飞溅如超新星爆发，空间被撕出裂缝，发光茶汤泼溅化作星尘瀑布，所有星光绕她旋转，仿佛她一转身宇宙就为她重启，时间与空间都随主体人物而动，举世无双的视觉奇观，深空星云青绿与品红对冲，史诗级电影打光，戏剧张力，超高对比度，真实人物摄影质感`

#### Shot 5 | Quick cuts · rhythm (three beat-matched close-ups on the downbeat · stardust gathering and scattering)

> Rhythm hook: three 0.5s+ close-up quick cuts within 5s (pinch the cup / tilt the cup / splash the tea), switched on the downbeat to create a "rush". **Environment: dream, one touch of a fingertip and the universe answers.**

- **Action breakdown**:
  - 0-1.5s: close-up one — fingertips pinch the cup's rim, stardust gathers into points of light toward the cup (still)
  - 1.5-3s: close-up two — the cup tilts slightly, the glowing tea liquor pouring out as a waterfall of stardust (moving)
  - 3-5s: close-up three — the tea splashes and sprays, the stars flicker and burst with it (exploding)
- **Pose / hand position**: three fingers pinch the cup (light but steady) → tilt the cup (wrist rotating) → splash (wrist exploding)
- **Environment / dream linkage**: pinch → stardust gathers; tilt → a stardust waterfall falls; splash → stardust bursts and stars flicker
- **Camera and mood**: three static close-ups cut in sequence (beat-matched in post); the fastest rhythm — quick, satisfying, on the beat
- **Prompt**: `宇宙级意象，时空主宰：现代东方舞者手部特写，皮肤真实质感——指尖轻拈青瓷茶盏杯沿的瞬间，周围星尘向茶盏聚拢成光点；倾盏时，发光茶汤倾泻成星尘瀑布垂落；泼洒时，茶汤化作星尘炸开四散，星辰随之明灭；背景是浩瀚星海，亿万星辰环绕她指尖流转，仿佛她轻轻一动整个宇宙都随之呼应，时间与空间都随主体人物而动，三连特写节奏，深空星云青绿与品红对冲，史诗级电影打光，超高对比度，微距真实质感`

#### Shot 6 | Waking transition (the dream's energy spiralling · the sea of stars dimming)

> The dream begins to collapse and contract, setting up the "waking". **Environment: dream → reality transition, dissolve.**

- **Action breakdown**:
  - 0-2s: all the stardust and starlight in the dream start spiralling inward (energy collapse)
  - 2-3s: the sea of stars dims, the nebula disperses, and the dark of reality starts showing at the frame's edges (the dream fading)
  - 3-4s: the whole dream disperses as a wisp of light dust and the frame settles into reality's darkness (dissolve transition)
- **Pose / hand position**: the girl stands at the centre of the dream, stardust spiralling inward around her as she gradually fades into the dark
- **Environment / dream linkage**: the dream's energy collapses inward → disperses; the sea of stars dims → reality's darkness emerges
- **Camera and mood**: close-up → wide shot with a slow pull-back; the mood falls back from the dream's peak — contracting, quietening, waiting to wake
- **Prompt**: `电影级写实照片，梦境消散的过渡瞬间：真实的人类东方少女，约十六七岁，清纯懵懂，身着素纱水墨长裙，立于渐暗的星海中央，周身所有星尘与星光向中心回旋收拢，星云逐渐消散褪色，她闭着眼睛，神情安详，仿佛梦即将醒来；画面边缘透出现实中素净床榻的暗色剪影，梦境与现实在这一帧叠化交错；深空星云的青绿品红逐渐暗去，只余一缕光尘绕她盘旋后消散；史诗级电影布光，超现实与写实的过渡质感，超高细节，8k摄影质感，留白氛围`

#### Shot 7 | 🔁 Loop-closing twist (reality, the bed · eyes suddenly opening)

> The waking twist: back on the real bed, eyes suddenly opening — the instant they open, a hard cut back to shot 1's side-lying close-up, and the audience realises "it was a dream". **Environment: reality, plain bed.**

- **Action breakdown**:
  - 0-1s: a plain bed in reality, the girl lying quietly (echoing shot 1's side-lying pose)
  - 1-2s: she suddenly opens her eyes, clear-eyed, a thread of galaxy light lingering in her pupils (the dream's afterglow)
  - 2-3s: the instant of opening them freezes — hard cut back to shot 1 (closing the loop)
- **Pose / hand position**: lying flat and quiet (relaxed) → eyes suddenly opening (pupils contracting)
- **Environment**: reality · plain bed, soft morning light, real domestic textures (strongly contrasted with the dream's sea of stars)
- **Camera and mood**: static face close-up; the mood moves from the dream's afterglow to real-world clarity — realisation, closure, an aftertaste
- **Prompt**: `电影级写实照片，真实人物摄影，清晨梦醒瞬间：真实的人类东方少女，约十六七岁，清纯懵懂，躺在现实素净的床榻上，素色棉被，柔和晨光从窗外透入，真实的家居质感；她刚刚醒来，突然睁开眼睛，眼神清澈无辜，瞳孔中残存着一线微弱的星河光点（梦的余韵），额心一点朱砂，肌肤真实凝脂质感；她的侧卧姿态与开场第一镜完全呼应——同一个少女，同一张脸，仿佛梦境与现实在这一刻重合；史诗级电影布光，柔和自然光，超高细节，8k摄影质感，完全写实不卡通，留白氛围`

---

## 5. Prompt & parameters

### 5.0 Character design spec (v3 final · design first, generate after)

> 📖 **Design philosophy (v3)**: rather than piling up large areas of nebula, go for **real human × microscopic universe** — winning through "scale contrast": the person is only a real fist's size, yet an entire galaxy hangs at her ear. Decoration should be **fine, not broad**: one galaxy earring beats a body covered in nebulae. Describe every detail with the precision of a character's entrance in *Dream of the Red Chamber*, then let the AI generate from that.

**Character: the Galaxy Tea Deity** (an Eastern girl of about sixteen or seventeen)

- **Face**: a real human Eastern **girl's** face — **pure, naive, still childish**: an oval face with a little baby fat, clear, innocent eyes with a watery sheen, brows and eyes like a painting, lips slightly pressed; skin with the texture of real congealed cream, fine pores and a thin sheen of sweat; a mark of vermilion at the centre of her forehead — a solidified supernova core. **The expression contrast is the core: ordinarily as pure and naive as a girl who knows nothing of the world, but when she erupts she is like a god's wrath destroying the world** — the more innocent the exterior, the more astonishing the action. **Never cartoonify, never mature her.**
- **Build**: a **healthy, energetic girl's figure** — not skinny, not sickly: a well-proportioned, full figure, cheeks with baby fat, round and lively arms and legs, like a girl next door full of energy (likeable), not a bony runway model. **Gaunt is not likeable; full is what feels warm.**
- **Hair**: real black hair tied high in a ponytail, dissolving into fine light dust only at the very tips; a **comet-tail silver hairpin** in her hair, with a miniature planet hanging from its end that sways slightly as she turns her head.
- **Earring (the core scale contrast)**: a **galaxy earring** on her left ear — a silver chain fine as a needle tip, with a complete spiral-arm galaxy hanging from its lower end (a spiral structure visible to the naked eye, cyan-green and magenta nebulae slowly turning inside); when she moves, the galaxy flickers and rotates at her ear. **The person is small, the galaxy is large: a single earring is a universe.**
- **Neckpiece**: a **star chain** across her collarbone, seven miniature stars strung in a line, the middle one the size of a fingernail, burning with real stellar white light.
- **Arm / wrist**: a **ring armlet** on her right wrist — a tiny Saturn ring, ice-blue in lustre, floating and turning as she circles her wrist; a **black-hole ring** on her left ring finger, with a miniature black hole curled on its face, its accretion disc giving off a dark-gold glow.
- **Clothing (fine, not broad)**: a modified ink-wash long dress on a plain gauze base, **with large nebula areas rejected** — only the collar, cuffs and hem are embroidered with star charts in extremely fine stardust thread, the stitches like light; a **galaxy sash** at the waist, thin as a thread yet condensed from an entire galaxy, giving off a faint cyan-white glow; as she walks, the hem's edge occasionally dissolves into stardust and condenses back into cloth, like breathing.
- **Props**: a smooth **celadon tea cup** in her hand (keeping its mortal texture, contrasting with her divinity), filled with **flowing nebula tea liquor**, with three points of light hovering at the rim like stars in the cup.
- **Feet**: barefoot, with an extremely fine stardust chain around her ankle that scatters a few motes of light dust with every step.
- **Temperament**: she is one person and also a universe — furious she is like a god's wrath, and the galaxy flickers with her; calm she is like a mortal holding a cup of tea.

**Universal visual anchor (required in every shot, ensuring consistency)**

```
真实的人类东方少女，约十六七岁，清纯懵懂稚气未脱，鹅蛋脸带一点婴儿肥，眼眸清澈无辜带水光，肌肤真实凝脂质感带毛孔与汗珠，健康元气不瘦削的少女体态，身形匀称饱满圆润有活力，额心一点朱砂，表情平时清纯懵懂、爆发时如神怒灭世；
高马尾真实青丝，发梢化开成光尘，发间彗尾银簪；
左耳一枚星髓珠耳坠——正常尺寸如一颗大珍珠，半透明珠体内封存一整条微型银河旋臂，青绿与品红星云在珠内缓缓旋转，物小意大；
颈间星链坠着微缩恒星，右腕星环臂钏，左手无名指黑洞戒；
一身改良水墨长裙素纱为底，领口袖口衣摆用极细星尘线绣出星座图谱，腰间一条纤细银河束带，衣摆边缘化开成星尘又凝回布料；
手中一只温润青瓷茶盏，盏中盛着流动的星云茶汤，盏沿悬三粒光点；
赤足脚踝系星屑链；她是一个人也是一个宇宙，平时是清纯懵懂的元气少女，狂时如神怒星河为之明灭。
```

> Scale-contrast principle: **the person at real size, the universe miniaturised into accessories** — the galaxy is an earring, a star is a necklace, Saturn's ring is an armlet, a black hole is a ring. Better one fierce piece than light all over.
> Persona-contrast principle: **a pure, naive face × violent, explosive action**; the more innocent the exterior, the more astonishing the eruption.
> Realism principle: materials may be cosmic, but face / skin / hair / fabric must be photo-real, following v2's realism; no cartoonification, no maturing.

### Shot 1 (I2V main path, with the storyboard image as the first frame)

```bash
# 首帧：out/storyboard/shot1_final.jpg（v4 梦境闭环·悬念开场，已定版）
# 模型：mini（platform 按量）
MODEL="doubao-seedance-2-0-mini"
arkcli +gen --model "$MODEL" \
  --input @out/storyboard/shot1_final.jpg \
  --ratio 16:9 --resolution 480p --duration 5 \
  "电影级写实照片，真实人物摄影，慵懒纯净质感，面部大特写：真实的人类东方少女，约十六七岁，清纯懵懂稚气未脱，鹅蛋脸带一点婴儿肥，眼眸清澈无辜带着水光，慵懒地侧卧着，一只手托腮，眼神好奇懵懂地望向前方，唇瓣微抿，真实肌肤凝脂质感带毛孔与薄汗，额心一点朱砂；镜头推得很近，她的面部占据画面绝大部分，清澈的眼眸、婴儿肥的脸颊、微抿的唇、额心朱砂都是焦点；画面边缘保留她侧卧姿态的局部：托腮的手、垂落的几缕真实发丝搭在肩头、素纱衣领与肩颈的柔和线条、裙摆边缘微微化开成一点光尘；背景是极简的暗色虚化，只有极其细微的星尘光点若隐若现；她看起来就像一个不谙世事的邻家少女，纯净、慵懒、无辜、惹人怜爱；史诗级电影布光，柔和侧光勾勒面部轮廓，超高细节，8k摄影质感，完全写实不卡通，留白氛围" --open
```

- Parameters: ratio 16:9 / resolution 480p (direction test) / duration 5
- First frame: `out/storyboard/shot1_final.jpg` (I2V keeps the visuals consistent)
- Reproduction: record the seed value and fill it back in

### Shots 2-7 (I2V main path)

The per-shot command is identical in form to shot 1 (`--input @out/storyboard/<该镜分镜图>` + the verbatim prompt at the end of each shot in §4.2), with identical parameters: `--ratio 16:9 --resolution 480p --duration 5` (direction-test stage). The model is always `doubao-seedance-2-0-mini` (platform pay-as-you-go).

> 💡 If a shot's I2V motion is unsatisfactory, fall back to the T2V option (drop `--input` and generate from the prompt alone), or adjust duration (4-6s) and align with `-t` when concatenating.
> ⚡ Dream rhythm: shot 1 suspense (3s) → shot 2 contrast explosion (5s) → shot 3 rising (5s) → shot 4 exploding again (5s) → shot 5 quick cuts (5s) → shot 6 waking transition (4s) → shot 7 loop-closing eye opening (3s).

### 5.1 Post-production audio design (reusing the survival-island mixing workflow)

| Track | Source | Notes |
|----|------|------|
| BGM | external material (atmosphere build → guzheng → electronic drums → fading away) | matching the dream's rhythm: 0-3s quiet suspense → 3s heavy drum burst → 8-18s the dream dance rising and falling → 22s fading → 26-30s waking into reality, quiet afterglow |
| Ambience | external material | dream: nebula rumble / wind chant; reality: morning birdsong, the soft creak of the bed |
| Narration | TTS (seed-tts-2.0, optional) | one poetic line (can be omitted): "以星河为梦，以茶为引。" |

> Mixing: video `-c:v copy` + audio track `-c:a copy` (mp3 dropped straight into mp4; do not use `-c:a aac`); see the TTS section of [methods/README.md](../../methods/README.en.md).

---

## 6. Execution plan

| Stage | Configuration | Purpose |
|------|------|------|
| 0. Storyboard | seedream-5.0-lite, produce 7 keyframes | **Review the visuals first**: whether composition / costume / scene / colour match expectations; if not, only the image is regenerated (low rework cost) |
| 1. Direction test | 480p I2V (first frame = storyboard image) | Validate whether mini can express the "shake it" motion and whether the 7-shot dream loop joins consistently |
| 2. Finalisation | 720p | Lock the plan, add an audio-driven beat-matched version (if needed) |
| 3. Final cut | 720p + post | Concatenate the final film (including the dissolve transitions), music/ambience, vertical crop |

> ⚠️ mini does not support `--draft`, so run the direction test straight at 480p; for cost and limits see [quality-and-cost](../../methods/quality-and-cost/README.en.md).
> The storyboard stage is a rework firewall: images before video, so visual problems are solved on the image and not carried into the video stage.

---

## 7. Output log

| Shot | Version | task_id | local_path | Notes |
|------|------|---------|------------|------|
| 1 | v1 | cgt-20260801140736-rgt6x | out/video/shot1.mp4 | Suspense opening · side-lying face close-up |
| 2 | v1 | cgt-20260801141409-mptxz | out/video/shot2.mp4 | Extreme contrast · world-destroying fury |
| 3 | v1 | cgt-20260801141656-t5hvf | out/video/shot3.mp4 | Rising · wrist circling to shake the tea |
| 4 | v1 | cgt-20260801141857-tq9sf | out/video/shot4.mp4 | Eruption · galaxy exploding |
| 5 | v1 | cgt-20260801142149-4srnq | out/video/shot5.mp4 | Quick cuts · three hand close-ups |
| 6 | v1 | cgt-20260801142325-cccxk | out/video/shot6.mp4 | Waking transition · the sea of stars dimming |
| 7 | v1 | cgt-20260801142546-dlssk | out/video/shot7.mp4 | Loop closure · eyes opening on the bed |

> Direction versions of all 7 shots are generated (480p / 864×496 / 5.09s / mini-260615 / platform pay-as-you-go); awaiting overall review before finalisation.

---

## 8. Checklist

- [x] Every video has a chosen method linked to methods/
- [x] Prompts written according to the method README strategy
- [x] Model IDs complete (doubao-seedance-2-0-mini / doubao-seedream-5-0-lite)
- [ ] Storyboard images generated and passed review (see §4.3)
- [ ] Parameters within the supported_params range
- [ ] Executed in stages (storyboard → direction test → finalisation → final cut)
- [ ] Outputs saved to local_path (URLs expire after 24h)
- [ ] Content passed review (see [content-safety](../../methods/content-safety/README.en.md))

---

## Revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-08-01 | v1.0 | Project initialised: art-dance short "Shake a Good Cup of Tea", 6-shot 30s storyboard + T2V main-path plan | 小七 |
| 2026-08-01 | v1.1 | Storyboard refined: overview table + shot-by-shot breakdown (action breakdown / poses and hand positions / tea-element landing points / camera and mood / prompt), per-shot standalone prompts, added the post-production audio design | 小七 |
| 2026-08-01 | v1.2 | I2V unlocked: seedream-5.0-lite verified activated; added §4.3 storyboard generation and review (images before video to prevent rework); main path switched to I2V (storyboard image as the first frame); the storyboard stage inserted into the execution plan | 小七 |
| 2026-08-01 | v1.3 | Produced 6 storyboard images (2560×1440, 16:9); fixed the storyboard command: use `--size` for image aspect ratio rather than `--ratio` (`--ratio` is video-only, and ignoring it defaults to square); recorded seedream's size pixel floor | 小七 |
| 2026-08-01 | v1.4 | Reworked for explosive hooks (A+C combination): first-frame hook + still-then-burst contrast structure; the new 6-shot rhythm "burst → still → rise → burst → quick → hook"; added the amber tea liquor / vermilion visual hammers; earlier storyboard images archived to out/storyboard/v1-classic/ | 小七 |
| 2026-08-01 | v1.5 | Finalised "cyber ink + released character": the contrast upgraded to a collision across eras (classical dancer × neon teahouse); the character released (high ponytail with hair flying / off-shoulder long dress flaring / vivid expression); after shot 1 passed validation, all 6 storyboard images were generated (2560×1440); all per-shot prompts synced to the cyber-ink version | 小七 |
| 2026-08-01 | v2.0 | Hooks upgraded again to "mastery over time and space": the environment goes from backdrop to a causal extension of the character's actions (a step swaps the stars, a raised hand extinguishes the galaxy); v1.5 archived to v1.5-cyber-ink/; 6 mastery-over-time-and-space storyboard images generated, shot*_v2_astro.jpg (2560×1440); per-shot prompts include bespoke environment linkage | 小七 |
| 2026-08-01 | v2.1 | The 6 v2-astro shot images archived to out/storyboard/v2-astro/ (all three versions complete: v1-classic / v1.5-cyber-ink / v2-astro) | 小七 |
| 2026-08-01 | v3.0 | Character design spec (Dream of the Red Chamber-style entrance description): real human × microscopic universe, scale contrast (galaxy = earring / star = necklace / planetary ring = armlet / black hole = ring), fine not broad; the persona contrast of a pure, energetic girl × world-destroying fury | 小七 |
| 2026-08-01 | v3.1 | Opening structure changed to a "suspense-then-contrast pair": shot 1's pure, languid face close-up (the suspense hook, lying on her side with a hand under her cheek, her face absolutely centred) → shot 2, the same face in world-destroying fury (extreme contrast); shot1_final.jpg / shot2_final.jpg finalised, iteration versions archived to v3-spec-iterations/ | 小七 |
| 2026-08-01 | v4.0 | The overall story changed to a 7-shot "dream loop" structure: shot 1 suspense opening → shots 2-5 cosmic dream dance → shot 6 waking transition (the sea of stars dimming in a dissolve) → shot 7 eyes suddenly opening on the real bed (linking to shot 1, closing the loop); generated shot6_dream_end.jpg / shot7_wake.jpg; per-shot prompts, rhythm and audio design synced to v4 | 小七 |
| 2026-08-01 | v4.1 | Filled in the storyboard images for shots 3/4/5 (shot3/4/5_final.jpg), completing all 7 (shot1-7_final.jpg, 2560×1440) with unified naming; removed redundant older-named copies | 小七 |
