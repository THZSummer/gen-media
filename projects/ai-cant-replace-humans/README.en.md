# AI Cannot Replace Humans ("Who Says AI Can Never Replace Humans")

> 🌐 Language: **English** | [中文](README.md)

> Back to [project index](../README.en.md) ｜ Skills: [../../.agents/skills/](../../.agents/skills/README.md) ｜ Video methods: [../../methods/](../../methods/README.en.md)

> ⚠️ This project **currently defines the project spec only**: **no sub-topics have been started** (see §10).
> This file pins down the format, the content rules, the technical route, the selection funnel and the
> compliance requirement first; sub-topics come after the spec is confirmed.

---

## 1. Project background

- **Project name**: `ai-cant-replace-humans`
- **Theme**: "Who Says AI Can Never Replace Humans"
- **One-line positioning**: **use absurd plots that only a human could have invented to satirise the question of whether AI can replace humans.**
  The loop closes like this: if the plot is too absurd for AI to have come up with on its own, that in itself proves the title.
- **Goal**: a **vertical short-video series** published on Douyin-style platforms; 15 seconds per episode, image + text + sound together, as easy to watch as possible.
- **Type**: video (reference-to-video: **image + text prompt**)
- **Channel**: Douyin-style short-video platforms (vertical feed)
- **Delivery date**: TBD (spec first, scheduling later)

---

## 2. Deliverables

| # | Purpose | Size or duration | Ratio | Qty |
|---|---------|------------------|-------|-----|
| 1 | **Single episode** (main deliverable) | 1080×1920 / **15.083 s = 362 frames @24fps** | 9:16 | 1 per episode |
| 2 | Vertical reference image (i2v first frame) | 1080×1920 (downscale to ≤1MP before feeding) | 9:16 | 1 per episode |
| 3 | Cover frame | 1080×1920 | 9:16 | 1 per episode |
| 4 | Prompt archive (incl. the 100 candidate briefs and scores) | — | — | 1 per episode |
| 5 | Publish copy + hashtags | — | — | 1 per episode |

**Hard targets ("easy to watch" turned into numbers)**:

- **Duration**: on the i2v **17k+5 frame grid**, 15 s lands on **362 frames = 15.083 s**, not 15.000 s; final renders are counted in 362 frames.
- **Composition**: subject centred and slightly high, with **roughly the bottom quarter of the frame left clear for subtitles/titles** — never let text sit on a face.
- **The first 3 seconds must carry a hook**: open on the single most absurd frame plus a one-line conclusion (completion rate drives reach).
- **Subtitles**: large Chinese type, short phrases; when the information density is high, stack short lines that pop in one by one instead of writing paragraphs.
- **Series**: one episode covers **exactly one thing**, tied together by a fixed opening and end card.

---

## 3. Keywords and hashtags

| Tag | Role | Where it goes |
|-----|------|---------------|
| `#AI无法取代人类` | **Primary topic** | every episode |
| `#这是人能想出来的剧情` | **Primary topic (the hook)** | every episode |
| `#给AI的提示词堪比顶刊论文` | Irony: a deadpan pseudo-academic long prompt | copy + comment bait |
| `#无厘头` `#抽象` | Content positioning | rotate |
| `#嗑药了` `#毒蘑菇吃多了` | Self-deprecating comment-section slang | rotate (not every episode, it dulls) |

> The tags are **platform-native Chinese**; copy them verbatim instead of translating back and forth.

---

## 4. Content rules: how much to pack into 15 seconds

### Time structure (15.083 s = 362 frames)

| Segment | Frames | Job |
|---------|--------|-----|
| 0–1.9 s | 0–45 | **Hook**: show the most absurd frame immediately plus a one-line conclusion (no setup) |
| 1.9–6.3 s | 46–150 | Establish the "normal world" rules so the viewer thinks they understand |
| 6.3–11.1 s | 151–265 | **First twist** (break the rule just established) |
| 11.1–13.3 s | 266–318 | **Second twist** (flip the twist once more) |
| 13.3–15.083 s | 319–361 | **End card**: call back to the title plus one still frame of blank space (something to argue about in the comments) |

### The five absurdity devices (hit at least 2 per episode; more is more "only a human")

| # | Device | Example |
|---|--------|---------|
| 1 | **Logic mismatch**: apply A's rules to B | Play football by exam rules: a goal requires showing your working |
| 2 | **Scale mismatch**: use the small as if it were large | A single grain of rice as a stage, an ant as the lead |
| 3 | **Material mismatch**: make an abstract concept physical | Make "involution" an actual rolled pancake — the more it rolls, the thinner it gets |
| 4 | **Inverted causality**: show the result, reveal the cause later | He falls first, and only then does someone reach out and push him |
| 5 | **Pseudo-technical jargon**: deadpan fake academic naming | "Type-7 irrational folding", "emotional overflow coefficient 3.2" |

### Anti-patterns (any one of these kills an episode)

- Merely "AI drew something weird" with **no human logic** (weird ≠ absurd; absurdity needs a retellable idea)
- Needs a paragraph of explanation to be understood (15 seconds has no room to explain)
- Three stories in one episode (none of them has time to land)
- Carried by real faces, celebrities, existing IP or existing music (compliance and rights risk, see §8)

---

## 5. Skill / method selection

| # | Purpose | Skill or method | Input |
|---|---------|-----------------|-------|
| 1 | Environment check and workflow audit | [comfyui-server](../../.agents/skills/comfyui-server/SKILL.md) | — |
| 2 | Generate the vertical reference image (first frame) | [text-to-image-comfyui](../../.agents/skills/text-to-image-comfyui/SKILL.md) | prompt |
| 3 | **Reference-to-video (main route)** | [image-to-video-fastvideo3](../../.agents/skills/image-to-video-fastvideo3/SKILL.md) | vertical reference image + i2v prompt |
| 4 | Subtitle frames / cover / comparison / metadata strip | [image-tools](../../.agents/skills/image-tools/SKILL.md) | finished frames |
| 5 | Fallback: text-to-video (no reference image) | [text-to-video-fastvideo3](../../.agents/skills/text-to-video-fastvideo3/SKILL.md) | structured prompt |
| 6 | Fallback: cloud video (1080p / long duration) | [methods/](../../methods/README.en.md) (Ark Seedance, pay per use) | first frame + prompt |

---

## 6. Technical route: reference-to-video (image + text prompt)

**Why reference-to-video rather than text-to-video**: this project needs **controllable absurdity** — lock one
frame that is "absurd but instantly legible", then set it in motion. Text-to-video re-gambles the composition
every time and cannot guarantee that frame one is the hook.

**⚠️ Where the vertical format comes from (the easiest trap)**: in i2v the **canvas is decided by the input
image** — the workflow runs `LoadImage → ImageScaleToTotalPixels → GetImageSize → width/height` and exposes
**no aspect-ratio parameter**. Therefore:

- The reference image must be **made 9:16 first** (1080×1920, or 768×1365) — otherwise the output is not vertical and the episode is a redo.
- Keep the image fed to the model **below ~1MP**: `first_frame` receives the **original**, so a big image only wastes memory and time.
- If you want "the bottom quarter clear for subtitles", **push the subject up while making the reference image** (leave the space at image time, do not patch it in video).

**Parameters and cost**:

```bash
cd .agents/skills/image-to-video-fastvideo3
python3 scripts/comfyui_i2v.py --image ../../projects/ai-cant-replace-humans/refs/<slug>.png \
  --prompt-file ../../projects/ai-cant-replace-humans/prompts/<slug>.txt \
  --duration 15 --megapixels 0.4 --seed <N> --out-dir out/ --timeout 3600
```

- Measured baselines: **56 frames ≈ 3 min**, **124 frames ≈ 6–7 min** (576×736 / 8 steps).
- **362 frames extrapolates linearly to ≈ 19–22 min per episode** — ⚠️ **that bracket is not measured yet**, it is an extrapolation, so do not skimp on `--timeout 3600`.
- Validate every parameter set with `--plan` first (free, no GPU, no upload) — make it a habit.

---

## 7. Prompt selection funnel (100 → 1)

**Core discipline: do the selection on the text and keyframe layers; never actually run 100 videos.** The arithmetic makes it obvious:

| Layer | Qty | Unit cost | Total |
|-------|-----|-----------|-------|
| Text scoring | 100 | ~0 | ~0 |
| Keyframe images (T2I) | 10 | ~25 s each | ~4 min |
| Real i2v renders | 3 | ~20 min each | ~1 h |
| ~~All 100 through i2v~~ | ~~100~~ | ~~20 min~~ | ~~**≈33 h GPU**~~ ← never viable |

**Five-step funnel**:

1. **Brief layer (100 → 20)**: each candidate is only "one logline + 5 beats", not a full prompt. Score with the rubric below.
2. **Prompt layer (20 → 10)**: write the **full i2v prompt** for the surviving 20 (all three sections), then score again.
3. **Keyframe layer (10 → 3)**: render the vertical reference images with T2I and **eliminate by eye** (if the frame cannot hold the idea, cut it).
4. **Real-machine layer (3 → 1)**: run i2v for those 3 only, and compare "does it still hold once it moves".
5. **Final pick**: 1 episode goes to delivery, the rest to the archive (they can be revived next period).

**Scorecard** (out of 5; any failed threshold eliminates the candidate outright, one veto):

| Dimension | Weight | Threshold | What it looks at |
|-----------|--------|-----------|------------------|
| Absurdity strength | 0.30 | ≥3 | Is it something "a human could invent and AI could not" |
| Sayable and memorable in one line | 0.20 | ≥3 | Can it serve as the title |
| Fits 15 s | 0.20 | ≥3 | Does it have two twists of setup and payoff |
| Shot feasibility | 0.15 | — | Can i2v actually shoot it (no impossible physics) |
| Platform friendliness | 0.15 | — | No real faces / existing IP / existing music / sensitive elements |

> A total of **≥3.5** is required to enter the keyframe layer; entering the real-machine layer requires **≥4.0**.

**Archive layout**:

```text
prompts/hunt/<date>-r<N>.md   # all 100 briefs + per-item score + reason for elimination (traceable, never deleted)
prompts/<slug>.txt            # the final i2v prompt in full (three sections: reference sentence / shots / two sound sections)
refs/<slug>.png               # the final vertical reference image (9:16)
```

> The required i2v prompt form is documented in [image-to-video-fastvideo3/references/prompt-format.md](../../.agents/skills/image-to-video-fastvideo3/references/prompt-format.md):
> **the first-frame reference sentence + `integrated_multimodal_description` (shots + timecodes) + `overall_soundscape` + `non_diegetic_music` — no section may be omitted**.

---

## 8. Compliance: AI-generated content labelling (mandatory, not optional)

Every episode is AI-generated video published on a domestic short-video platform, so **labelling is required**:

- **Measures for the Labelling of AI-Generated Synthetic Content** (jointly issued by the Cyberspace Administration of China, the Ministry of Industry and Information Technology, the Ministry of Public Security and the National Radio and Television Administration; **in force since 2025-09-01**); the supporting mandatory national standard "Cybersecurity technology — Labelling method for AI-generated synthetic content" took effect the same day.
- **Article 4(4)**: video must carry a **conspicuous notice** at the **opening frame** and around the playback area; it may also be added at the end and in the middle.
- **Article 10**: users publishing generated content through a network information dissemination service must **declare it proactively** and use the labelling features the provider offers; no organisation or individual may maliciously delete, tamper with, forge or conceal the labels.
- On the platform side, Douyin, Tencent, Weibo, Bilibili, Kuaishou and others rolled out AI labelling features (announced 2025-09).

**Execution checklist for this project**:

- [ ] A conspicuous "AI-generated" corner mark on the **opening frame** of the finished video (visible within 0.5 s, permanent or for the first 2 s)
- [ ] **Tick the platform's AI declaration** when publishing (a corner mark alone is not enough)
- [ ] Never remove or alter any AI label; keep **metadata** (this repo's outputs carry `.api.json` / `requests.jsonl` for traceability by default)
- [ ] Copy never claims "really filmed / performed by a real person"; no real-person portraits, existing IP or existing music

Sources: [Four departments issue the Measures for the Labelling of AI-Generated Synthetic Content, in force from September 1 (Guangming Online)](https://m.gmw.cn/2025-03/14/content_1303991453.htm) |
[Tencent, Douyin and others announce AI labelling features (JCRB)](http://news.jcrb.com/pic/202509/t20250902_7119785.html)

---

## 9. Execution plan

| Stage | What happens | Gate |
|-------|--------------|------|
| Direction | **Text-level selection**, 100 → 1 briefs (logline + 5 beats) | 20 → 10 briefs survive |
| Lock-in | 10 **vertical keyframes** rendered and scored on the rubric | 3 enter the real machine |
| Final | 3 runs of i2v → pick 1, add subtitles / cover / compliance mark | 1 episode + complete archive |
| Spin-off | Same brief with a different art style or character; series publishing | Episode count and data review |

---

## 10. Sub-topics (**not started**)

As requested, **this period defines the project spec only and starts no sub-topics**. Before starting them, three things must be decided:

1. **What dimension splits the sub-topics**: content device (logic / scale / material / causality / jargon)? Subject (office / kitchen / space / antiquity)? Or a character?
2. **How many episodes per sub-topic**: compare [shanhai-jing](../shanhai-jing/README.en.md)'s "one creature per episode" with [bio-splice](../bio-splice/README.en.md)'s "5 periods per sub-topic".
3. **Whether to use a fixed character**: a fixed character builds series recognition but stacks i2v consistency risk on top (the look must be re-anchored every episode).

---

## 11. Production log

| Episode | Version | Skill/method | seed / task_id | local_path | Notes |
|---------|---------|--------------|----------------|------------|-------|
| — | — | — | — | — | not started |

---

## 12. Checklist

- [ ] The reference image is **9:16** (otherwise the output is not vertical and the episode is a redo)
- [ ] The reference image is ≤ ~1MP and leaves the **bottom quarter** clear for subtitles
- [ ] `--plan` passes: **362** frames, no warning, all three prompt sections present
- [ ] First frame compared against the reference image (by eye and, when needed, `image-tools` SSIM)
- [ ] The episode tells **one thing** and hits **≥2** absurdity devices (§4)
- [ ] A hook in the first 3 seconds; a still end card after 13.3 s
- [ ] **Compliance**: AI corner mark on the opening frame + platform AI declaration (§8)
- [ ] The final is recorded as the **model + verbatim prompt + parameters + seed** tuple
- [ ] Docs are bilingual (`README.md` + `README.en.md`) and `tools/i18n.py check` reports zero on all three counters
- [ ] No large intermediates (`work/`, `out/`) committed

---

## 13. Revision log

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-11 | v0.1 | **Project created (spec only, no sub-topics started)**: settled the format (vertical 9:16 / 15.083 s = 362 frames / image + text + sound), the keywords and hashtags, the 15-second time structure and the "five absurdity devices", the reference-to-video route (including the hard constraint "the canvas follows the input image, so the reference image must be 9:16 first"), the **100 → 1 selection funnel and scorecard** (with the arithmetic showing that running all 100 through i2v would cost ≈33 h of GPU, so selection must happen on the text and keyframe layers), and the **AI-generated content labelling requirement** (the Labelling Measures took effect 2025-09-01: video needs a conspicuous notice on the opening frame and a proactive declaration when publishing) | 小七 |
