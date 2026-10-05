# Butterfly Girl's Adventure (butterfly-girl)

> 🌐 Language: **English** | [中文](README.md)

> Back to [project index](../README.en.md) ｜ Technical methods see [../../methods/](../../methods/README.en.md)

Butterfly Girl's Adventure · butterfly sprite micro-adventure (v4 final: reference images, independent and parallel)

> 📌 This directory was originally named giant-kingdom (the giant daughters' kingdom); in v3 the title was changed to "Butterfly Girl's Adventure". The giant-version attempts (v1 spectacle / v2 fear escape) are both archived.

---

## 1. Project Background

- **Project name**: butterfly-girl (Butterfly Girl's Adventure)
- **Type**: butterfly sprite micro-adventure short film
- **Objective**: the protagonist is a **butterfly sprite girl** — a girl's physique + butterfly wings + **butterfly size** (about 15cm, insect scale) — who can fly on adventures through everyday human scenes. The core selling point is **everyday adventure from a micro perspective**: she flies, dodges and explores in a human's one-room flat / dining table / flower pot, and everyday human objects are enormous in her eyes (a water glass like a swimming pool, a book like a city wall, a fan like a storm).
- **Publishing channels**: short video platforms (Douyin / WeChat Channels / Bilibili portrait, or Xiaohongshu landscape)
- **Delivery time**: TBD (validate the tone with the direction stage first)

> **Theme evolution**: v1 giant spectacle (wonder) → v2 giant fear (fear; the giant's proportions never matched the scene, scrapped) → **v3 Butterfly Girl's Adventure (chained 10 shots, strongly linear dependencies)** → **v4 (reference images, independent and parallel, solving the linear dependency)**.
> **v3 problem**: each shot had to wait for the previous shot's last frame before it could start, so 10 shots ran serially (2-5 minutes each) and a single point of failure broke the whole chain.
> **v4 plan (quality first, redesigned 2026-08-09)**: **storyboard keyframe driven** — each storyboard first generates 3 keyframes (start image / end image / key action image) as video references, so the model has a complete "start-stop-key action" trajectory to follow and quality improves dramatically; every shot is independent with no dependencies (all keyframes are recursively derived from the reference image library, not from video last frames). **The core objective is quality, not parallel efficiency.**

---

## 2. Deliverables List

| # | Video purpose | Duration | Ratio | Resolution |
|---|----------|------|------|--------|
| 1 | Main video (landscape, one-shot generation + native sound effects) | 15s | 16:9 | Start at 480p, lock at 720p |
| 2 | Portrait version (platform delivery) | 15s | 9:16 | Start at 480p, lock at 720p |

> The resolution ceiling is limited by the model (seedance-2.0 caps at 720p); see [quality-and-cost](../../methods/quality-and-cost/README.en.md) for details.

---

## 3. Method Selection

| # | Method used | Link | Input material |
|---|----------|------|----------|
| 1 | Text-to-image (storyboard frames / reference images) | [text-to-image](../../methods/text-to-image/README.en.md) | seedream-5.0-pro |
| 2 | Text-to-video (one-shot 15s) | [text-to-video](../../methods/text-to-video/README.en.md) | - |
| 3 | Official API direct-connection script | [scripts/gen_video.py](scripts/gen_video.py) | generate_audio native sound effects |

> Design notes (v3):
> - **One-shot 15s generation**: seedance-2.0 `--duration 15` produces the film in one go (already validated by step-scenery-v2); the prompt describes the complete adventure line.
> - **Official API direct connection**: `scripts/gen_video.py`, with `generate_audio` defaulting to true for native sound effects (✅ validated as working).
> - **Butterfly micro perspective**: the protagonist is butterfly-sized and flies through everyday human scenes — a water glass like a swimming pool, a book like a city wall, a fan like a storm, a human like a deity.
> - **Model**: `doubao-seedance-2-0-260128` (platform pay-as-you-go).

---

## 4. Storyboard Design (15s × 5 storyboards, one continuous shot)

Theme motif: **butterfly micro-adventure**. 5 scenes in a row, about 3s per shot, one continuous shot.

> ⚠️ The v3 storyboard is pending redesign. Produce the first storyboard first to set the tone (butterfly sprite + everyday scene), then complete the rest after confirmation.

### 4.1 Quick-reference table (v3 final · complete 10-shot adventure line)

| Storyboard | Scene | Content | Adventure element | Sound effect |
|------|------|------|----------|------|
| 1 | Desk + flower pot | The heroine reads lazily; the butterfly girl hides in the gap of the flower pot and peeks | First observation | Page turning, faint wing flutter |
| 2 | Desk surface | The butterfly girl plucks up courage and flies out of the flower pot, landing on the edge of a page | First approach | Wing beats, paper |
| 3 | Teacup rim | The butterfly girl flies to the teacup to drink | Adventurous act | Water sounds, wings |
| 4 | Desk lamp / book | The heroine's page-turning hand suddenly comes close; the butterfly girl flies off startled | Startled turn | Wind, page turning |
| 5 | Windowsill / outside the window | The butterfly girl flies out of the window and looks back once | Escape | Wind, wings |
| 6 | By the window | The little sister spots the butterfly girl; the chase begins | Chase begins | Footsteps, laughter |
| 7 | Desk | The butterfly girl dodges the little sister's hand on the desk | Dodging chase | Rapid wing beats, laughter |
| 8 | Beside the reading girl | The butterfly girl flies to the reading girl and dodges around her | Seeking shelter | Wings, surprise |
| 9 | On the book | The butterfly girl lands on the book the reading girl has open | Protected | Gentle laughter |
| 10 | On the book | The reading girl shields the butterfly girl; the little sister is envious; a warm ending | Warm ending | Background music |

> Complete adventure line: first observation → approach → drinking → startle → escape → chase begins → dodging chase → seeking shelter → protected → warm ending.
> Chained continuation: each shot uses the previous shot's last frame as its first frame (official API return_last_frame; consistency is guaranteed).
> The first shot is finalised as `shot1_v3_lazy.jpg` (heroine reading lazily + butterfly girl peeking through the flower pot gap).

### 4.2 One-shot generation prompt (core)

```bash
# 用官方 API 脚本（复用 step-scenery-v2 的 gen_video.py）
python3 scripts/gen_video.py --duration 15 --ratio 16:9 --resolution 480p \
  "电影级写实，体型反差视觉奇观，一镜到底：一位正常人类大小的清纯少女穿越到巨人女儿国——
  0-3秒她坠落在巨人国青翠草地上，抬头看到远处一位巨大女性的剪影，她的身形高耸入云，发丝如瀑布垂落，脚步落地时大地微微震颤；
  3-6秒一只巨大的手从头顶缓缓降临，五指张开如遮天巨幕，拇指就能遮住整片天空，手背皮肤纹理清晰可见如山峦沟壑，少女在巨手下渺小如尘；
  6-9秒巨人女性缓缓俯身，用掌心轻轻托起少女，少女站在掌心如站在一片大地，巨人瞳孔如清澈湖泊倒映着少女的身影，她好奇地凝视；
  9-12秒巨人低头，如瀑布般的发丝倾泻而下，掠过少女身侧，发丝根根分明如垂落的天幕，少女在发丝间穿行；
  12-15秒少女坐在巨人肩头远眺整个王国，巨人身形巍峨如山脉，她迈步时大地轰鸣震颤，城池在她脚下如玩具；
  全程以巨人为视觉参照系强调体型反差，少女恒定正常大小，电影级打光，完全写实不卡通，音画同步：风声、巨人呼吸声、脚步轰鸣、发丝掠过声"
```

> Notes:
> - All 5 storyboards are placed into a single 15s prompt as one continuous shot
> - The language of scale is the key: `拇指遮天 / 掌心如大地 / 瞳孔如湖泊 / 发丝如天幕 / 一肩一世界`
> - The sound effects are natively generated by generate_audio (✅ the official API is validated as working)
> - If the volume is too low after generation: `ffmpeg -i out.mp4 -af "volume=XdB" -c:v copy out_boosted.mp4`

---

## 5. Prompt & Parameters

### 5.0 Character design spec (v3 consistency anchor)

> v3 optimisation (2026-08-01): consistency enhancement — the official limit says "first frame + reference image cannot be mixed", so a **unified character anchor prompt template** is used: every shot's prompt starts with a fixed character appearance description, combined with the last-frame chain as double insurance, stabilising the person / scene.

**Character anchors (the opening every shot's prompt must carry)**:

```
蝴蝶精灵少女：约3-4厘米，蝴蝶大小，身穿浅蓝色轻盈纱裙，背生一对晶莹的半透明蓝色闪蝶翅膀，
翅膀扇动时洒下细碎光尘，清纯可爱，鹅蛋脸带婴儿肥，眼眸清澈，发丝柔软。
```

```
读书女：约二十出头，穿宽松米色家居服，长发扎成低马尾，安静温柔，坐在书桌旁看书。
```

```
小妹妹：约五六岁，扎着两根小辫子，穿浅粉色家居服，活泼淘气，好奇爱笑。
```

**Micro-world setting (v3)**

```
人类日常场景：现代一居室书桌（台灯、茶杯、书本、绿植盆栽），午后阳光，暖色温馨；
在蝴蝶女的视角下：书页如平原、文字如石雕、茶杯如宫殿、手指如巨柱；
蝴蝶女在人类日常物品间飞行冒险，人类物品的庞大体量制造奇幻感。
```

> The core is **everyday adventure from the butterfly's micro perspective** — she flies and explores among everyday human objects, and their enormous volume creates the fantasy feel.
> ⚠️ Content safety: an everyday, warm adventure tone; avoid horror / inappropriate implications; the heroine wears loose loungewear (to avoid sensitive moderation), see [content-safety](../../methods/content-safety/README.en.md).

### 5.1 Reference image library (v3.5 · recursive generation version)

> v3.5 optimisation (2026-08-02): seedream-5.0-pro supports **generating images with images as references** (multi-image reference `@图像N` fusion, generating new viewpoints from a reference image while keeping the appearance). **Recursive generation** replaces independent generation — recursively deriving multiple angles from a baseline image greatly improves appearance consistency.
> The old independently generated images have been backed up to `out/refs/v1-independent/`.

**Recursive generation flow**:

```
基准图（seedream 独立生成）──► 递归派生（以基准图为 --input 参考）
butterfly_base.jpg ──► butterfly_front/back/side（保持形象改视角）
reader_base.jpg    ──► reader_front/back（慵懒吊带短裤）
sister_base.jpg    ──► sister_front
scene_desk_base    ──► scene_desk/door/window（场景图）
```

**Character reference images (multi-angle · all three viewpoints complete)**:

| Character | Front | Back | Side |
|------|------|------|------|
| Butterfly girl (~3-4cm, pale blue gauze dress + blue morpho wings) | `butterfly_front.jpg` | `butterfly_back.jpg` | `butterfly_side.jpg` |
| Reading girl (lazy camisole + shorts, barefoot) | `reader_front.jpg` | `reader_back.jpg` | `reader_side.jpg` |
| Little sister (twin braids + pink loungewear) | `sister_front.jpg` | `sister_back.jpg` | `sister_side.jpg` |

**Scene reference images (multiple camera positions in the same room · consistent space)**:

| Scene | File | Purpose |
|------|------|------|
| Room panorama (spatial baseline) | `room_base.jpg` | Room layout baseline; derives each camera position |
| Desk camera position (close-up + spatial extension) | `scene_desk.jpg` | Main scene |
| Doorway camera position (doorway→indoors) | `scene_door.jpg` | Door viewpoint / chase scene |
| Window camera position (inside→outside the window) | `scene_window.jpg` | Escape scene |

> All three camera-position images are recursively derived from `room_base.jpg` ("same room, same space, different camera position"), so the spatial layout is consistent.

> Usage (multi-image reference during video generation):
> ```
> --input reference_image:@butterfly_front.jpg
> --input reference_image:@reader_noface.jpg
> --input reference_image:@scene_desk.jpg
> prompt: "参考@图像1的蝴蝶女形象、@图像2的读书女背影、@图像3的书桌场景，生成……"
> ```
> ⚠️ **Real-person reference blocking**: a photorealistic portrait reference image (the reading girl's front view) triggers `InputImageSensitiveContentDetected.PrivacyInformation` (real-person privacy blocking). Solution: **use a "no-face version" for character references** (back view / head down / long shot, `reader_noface.jpg`), which both locks the appearance and passes moderation; the butterfly girl (a sprite) and the scene images are unaffected.
> Recursive generation command example (deriving the back view from the butterfly girl's front view as the baseline):
> ```
> arkcli +gen --model doubao-seedream-5-0-pro-260628 --profile platform_cn-beijing_accountwide \
>   --size 2560x1440 --output-format jpeg --input @butterfly_front.jpg \
>   "保持@图像1中蝴蝶女的形象、服装和翅膀设计完全不变，改为背面视角……" --save-to out/refs/
> ```


---

## 6. Execution Plan

| Stage | Configuration | Purpose |
|------|------|------|
| 0. Reference image library | seedream-5.0-pro (out/refs/) | ✅ Ready: three characters × three viewpoints + four scene images |
| 1. Storyboard keyframes | seedream-5.0-pro (out/keyframes/) | v4 core: 3 keyframes per shot (start / end / key action) |
| 2. Direction | 480p independent generation (multi-image reference: keyframes + character + scene) | Validate quality |
| 3. Lock-in | 720p | Settle the plan |
| 4. Final | 720p + gain + optional narration | Produce the final, crop portrait |

### v4 storyboard keyframe plan (quality first)

**3 keyframes per shot** (`out/keyframes/`, seedream recursive generation, consistent characters):

| Frame | Content | Purpose |
|----|------|------|
| **Start image** `shotN_start.jpg` | The shot's opening picture (character position / scene / lighting) | Video start reference |
| **End image** `shotN_end.jpg` | The shot's closing picture (the story point where that shot ends) | Video end reference |
| **Key action image** `shotN_action.jpg` | The shot's most core action / scene instant | Key action reference |

**Generation method**: recursively derive from the reference image library (butterfly girl multi-angle / reading girl's back / little sister / scene images) as --input, with the prompt describing the key instant of that shot's plot.

**Video generation**: each shot is independent; pass that shot's 3 keyframes + character images + scene images via `reference_image`, and reference them in the prompt as `@图像1/2/3...`. No last-frame dependency, so a single shot can be re-run independently.

> Design the plan + generate the keyframe material first → the user reviews it → batch-generate the videos only after confirmation.

---

## 7. Output Record

| Version | task_id | local_path | Notes |
|------|---------|------------|------|
| - | - | - | To be produced |

---

## 8. Checklist

- [x] A method has been chosen for every video and linked to methods/
- [x] The model ID is complete (doubao-seedance-2-0-260128)
- [ ] Chained continuation generation succeeded (each shot uses the previous shot's last frame as its first frame)
- [ ] Multi-image reference consistency (character / scene reference library locked)
- [ ] The butterfly girl's appearance is consistent (pale blue gauze dress + blue morpho wings) + the heroine's lazy style
- [ ] The adventure line is complete (observation→approach→drinking→startle→escape→chase→shelter→protection→ending)
- [ ] The audio is native synchronous sound effects (generate_audio true), boosted and audible
- [ ] The parameters are within supported_params
- [ ] Execution is staged (reference image library → Direction → Lock-in → Final)
- [ ] Outputs are saved to local_path (URLs expire after 24h)
- [ ] The content has passed review (warm adventure tone, see content-safety)

---

## Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-08-01 | v1.0 | Project initialisation: "crossing into the giant daughters' kingdom", a visual spectacle of body-size contrast, 15s×5 storyboards generated in one shot, reusing step-scenery-v2's official API + generate_audio chain | 小七 |
| 2026-08-01 | v1.1 | Generated the v1 five storyboard images (spectacle-and-awe direction); user feedback that the direction was wrong | 小七 |
| 2026-08-01 | v2.0 | Direction changed to "fear escape + everyday hidden perspective": the protagonist is frightened, the main line is escape, the scenes are realistically everyday (the oppressive feel of giant furniture / giant objects); v1 storyboard images backed up to v1-wonder/; storyboards redesigned | 小七 |
| 2026-08-01 | v2.1 | Multiple rounds of attempts on v2's first storyboard (modern / cosy / crowded / mouse perspective) — the giant's proportions never matched the scene (feet bigger than the sofa); scrapped | 小七 |
| 2026-08-01 | v3.0 | Title changed to "Butterfly Girl's Adventure": a butterfly sprite girl (girl's physique + butterfly wings + butterfly size ~15cm) on a micro-adventure in everyday human scenes; the giant version archived to v2-giant-fear/; produce the first storyboard first to set the tone | 小七 |
| 2026-08-01 | v3.1 | Multiple rounds of storyboard finalisation: the heroine reading lazily (loose loungewear) + the butterfly girl peeking through the flower pot gap (shot1_v3_lazy.jpg finalised) | 小七 |
| 2026-08-01 | v3.2 | Chained continuation of the complete 10-shot adventure line: first observation→approach→drinking→startle→escape→chase begins→dodging→shelter→protected→warm ending; official API return_last_frame last-frame chaining; moderation blocking handled (loose loungewear + sprite girl to avoid sensitive content); complete film butterfly_girl_full.mp4 (50.8s) | 小七 |
| 2026-08-01 | v3.3 | Backed up the v3 results to out/v3-chain-10shots/; v3 optimisation plan: consistency enhancement — the official limit forbids mixing first frame + reference image, so switched to a unified character anchor prompt template (every shot carries the character appearance description) + last-frame chain as double insurance | 小七 |
| 2026-08-01 | v3.4 | Reference image library established (out/refs/): multiple reference_image entries officially usable (validated); isolated multi-angle character images (butterfly girl front/back/side, reading girl front/back in lazy camisole and shorts, little sister front) + multi-viewpoint scene images (desk / door / window); multi-image reference during video generation locks consistency | 小七 |
| 2026-08-02 | v3.5 | Recursive generation of the reference image library: the old independent generation version backed up to v1-independent/; using seedream-5.0-pro reference images to derive multiple angles (keep the appearance, change the viewpoint), improving consistency; README §5.1 updated | 小七 |
| 2026-08-02 | v3.6 | Reference image library standards unified: all characters completed with three viewpoints (reading girl / little sister given side + back), consistent with the butterfly girl standard | 小七 |
| 2026-08-02 | v3.7 | Scene image space unified: added room_base room panorama baseline, with the desk / door / window camera positions all derived from the baseline (same room, same space, different camera position), solving layout inconsistency | 小七 |
| 2026-08-02 | v3.8 | v3 optimised 10-shot chained generation (the last frame passed in as reference_image, bypassing the first_frame limit, with scene continuity + character consistency as double insurance); complete film butterfly_girl_v3_full.mp4 (50.8s) | 小七 |
| 2026-08-02 | v4.0 | v4 plan: reference images independent and parallel — each shot independently generated with multiple reference_image entries from the reference library, no last-frame dependency, all 10 shots fully parallel; solves v3's strongly linear dependency; v3 backed up to out/v3-optimized/ | 小七 |
| 2026-08-09 | v4.1 | v4 redesign (quality first): storyboard keyframe driven — 3 keyframes per shot (start / end / key action) as video references, independent with no dependencies; design the plan + generate the material for review first, then batch-generate | 小七 |
