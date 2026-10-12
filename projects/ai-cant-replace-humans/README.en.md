# AI Cannot Replace Humans ("Who Says AI Can Never Replace Humans")

> 🌐 Language: **English** | [中文](README.md)

> Back to [project index](../README.en.md) ｜ Skills: [../../.agents/skills/](../../.agents/skills/README.md) ｜ Video methods: [../../methods/](../../methods/README.en.md)

> 🎭 **Account identity in [ACCOUNT.en.md](ACCOUNT.en.md)**: the name **`硅基小张`**, the protagonist sheet, the opening-line / title-template / end-card kit, the naming rationale and the pre-launch checklist.

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
| 1 | **Single episode** (main deliverable) | 1080×1920 / **15 s** (cloud: `--duration 15`; local i2v route: 362 frames = 15.083 s) | 9:16 | 1 per episode |
| 2 | Vertical reference image (r2v first frame, made/edited with **Seedream**) | 1080×1920 (vertical preset) | 9:16 | 1–3 per episode |
| 3 | Cover frame | 1080×1920 | 9:16 | 1 per episode |
| 4 | Topic and prompt archive (**100-topic** funnel + **10-prompt** funnel + scores) | — | — | 1 per episode |
| 5 | Publish copy + hashtags | — | — | 1 per episode |

**Hard targets ("easy to watch" turned into numbers)**:

- **Duration**: target **15 s**. On the cloud route (Seedance) that is simply `--duration 15`; on the local i2v route the **17k+5 frame grid** puts it at **362 frames = 15.083 s** — the two routes quantise differently, so **report 15 s and state in the record which route produced it**.
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

### Time structure (15 s; frame numbers are the local i2v 362-frame grid, the cloud route only takes seconds)

| Segment | Frames (local i2v reference) | Job |
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
| 1 | Environment check and workflow audit (what templates / weights / nodes exist) | [comfyui-server](../../.agents/skills/comfyui-server/SKILL.md) | — |
| 2 | **Generate the vertical reference image (main route)** | [seedream-text-to-image](../../.agents/skills/seedream-text-to-image/SKILL.md) — ByteDance Seedream cloud paid node, **billed per image** | prompt |
| 3 | **Edit the reference image** (background / outfit / local retouch / multi-reference) | [seedream-image-edit](../../.agents/skills/seedream-image-edit/SKILL.md) — same Seedream cloud node | base image (+ annotation layer) + instruction |
| 4 | **Reference-to-video (main route)** | [seedance-reference-to-video](../../.agents/skills/seedance-reference-to-video/SKILL.md) — Seedance 2.5 cloud paid node (r2v), **billed per run**; reference images wired to `model.reference_images.image_N` | vertical reference images (1–30) + r2v prompt |
| 5 | Subtitle frames / cover / comparison / metadata strip | [image-tools](../../.agents/skills/image-tools/SKILL.md) | finished frames |
| 6 | Fallback (**free, local**): text-to-image / image-to-video / text-to-video | [text-to-image-comfyui](../../.agents/skills/text-to-image-comfyui/SKILL.md) · [image-to-video-fastvideo3](../../.agents/skills/image-to-video-fastvideo3/SKILL.md) · [text-to-video-fastvideo3](../../.agents/skills/text-to-video-fastvideo3/SKILL.md) | local weights, unlimited reruns |
| 7 | Fallback: direct Ark API (bypassing ComfyUI) | [methods/](../../methods/README.en.md) (Seedance, pay per use) | first frame + prompt |

> ⚠️ **All three stages of the main route are paid cloud services**: image generation per image (Seedream), image editing per image (Seedream), video per run (Seedance). **This repo contains no price table for any of them**; the unit price follows the ComfyUI account credits (platform.comfy.org) and **this project has not verified it**. Hence the rule: do the text-level selection properly (see §7) and **never burn the selection funnel on paid endpoints**.
>
> ⚠️ **`seedance-reference-to-video` is currently "built but unverified"**: it has scripts and `--list/--check/--plan` entry points but **no real-machine validation record**. Before this project starts for real, walk its SKILL.md "5 steps before the first real run" (`--check` → `--list` → `--plan` → one shortest-duration run → record the verification). Until then treat the video stage as an **unverified dependency**; if you need certainty, use the free local route in row 6 first.

---

## 6. Technical route: reference-to-video (image + text prompt)

**Why reference-to-video rather than text-to-video**: this project needs **controllable absurdity** — lock one
frame that is "absurd but instantly legible", then set it in motion. Text-to-video re-gambles the composition
every time and cannot guarantee that frame one is the hook.

**⚠️ The canvas differs between the two routes — do not confuse them** (this is where swapping routes silently voids an episode):

| Route | Where the canvas comes from | Reference image requirement |
|-------|-----------------------------|-----------------------------|
| **Main route: Seedance 2.5 r2v (paid cloud)** | **explicit `--ratio`** (use `9:16`; only `adaptive` follows the reference image) | generate a 9:16 vertical image with **Seedream** (keeps the series consistent) |
| Fallback: local FastH3 i2v (free) | **decided by the input image** (`LoadImage → ImageScaleToTotalPixels → GetImageSize`, **no aspect-ratio parameter**) | must be **made 9:16 first**, and ≤ ~1MP (the original goes straight into the model) |

Either way: if you want "the bottom quarter clear for subtitles", **push the subject up while making the reference image** (leave the space at image time, do not patch it in video).

**Main route (paid cloud) — image first, then video**:

```bash
# ① vertical reference image (Seedream, **billed per image**)
cd .agents/skills/seedream-text-to-image
python3 scripts/seedream_gen.py --prompt-file <ref-prompt.txt> \
    --size Custom --width 1080 --height 1920 --out-dir out/
# need to change that image (background / outfit / local retouch)?
# hand it to seedream-image-edit — also billed per image

# ② reference-to-video (Seedance 2.5 r2v, **billed per run**)
cd ../seedance-reference-to-video
python3 scripts/seedance_r2v.py --reference <ref.png> --prompt-file <slug>.txt \
    --resolution 1080p --ratio 9:16 --duration 15 --plan     # free parameter check first
python3 scripts/seedance_r2v.py --reference <ref.png> --prompt-file <slug>.txt \
    --resolution 1080p --ratio 9:16 --duration 15 --out-dir out/
```

- **Cost**: images per image, video per run; **this project has not verified the unit prices** — they follow the ComfyUI account credits.
- **Duration**: on the cloud route `--duration 15` simply means 15 s; there is no frame-grid quantisation.
- ⚠️ `seedance-reference-to-video` is a **built-but-unverified** skill; before the first real run, walk the 5 steps in its SKILL.md.

**Fallback (free, local, unlimited reruns)**:

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

## 7. Two selection funnels: **topics 100 → 1, then prompts 10 → 1**

**Keep the two layers apart; never merge them into one scorecard.** Eliminate 99 ideas on the **topic layer** first,
then 9 wordings on the **prompt layer**. The reason is practical: the topic decides "**is this an idea only a human
could have come up with**", while the prompt only decides "**can it actually be shot**". Scored together, "the frame
looks good" always beats "the idea is absurd enough" — and that is exactly the thing this project cannot afford to lose.

| Layer | What is chosen | Funnel | Unit cost | Total |
|-------|----------------|--------|-----------|-------|
| ① **Topic selection** | one logline + 5 beats | **100 → 1** | ~0 (text only) | ~0 |
| ② **Prompt selection** | the full r2v prompt (10 wordings of the same topic) | **10 → 1** | ~0 (text only) | ~0 |
| ③ Keyframes | vertical reference images for the winning prompt (**Seedream, billed per image**) | 3 versions | per image (unverified) | 3 images |
| ④ Real renders | **Seedance r2v, billed per run** | 1–2 | per run (unverified) | 1–2 runs |
| ~~Shoot all 100 topics~~ | ~~every topic through video~~ | ~~100~~ | ~~per run~~ | ~~**100 paid cloud runs**~~ ← never viable |

> **Core discipline**: both layers are decided **on text**, so paid endpoints only pay for the last two rows (3 images + 1–2 runs).
> On the free local route ([text-to-image-comfyui](../../.agents/skills/text-to-image-comfyui/SKILL.md) +
> [image-to-video-fastvideo3](../../.agents/skills/image-to-video-fastvideo3/SKILL.md)) rows ③④ cost about
> **75 s + 20–40 min of GPU** and no money — but image quality and consistency are below the cloud route.
> **"Trial and error locally, final render in the cloud" is the cheap-and-solid combination.**

### ① Topic selection (100 → 1)

Write **100 topics** first; each one contains **only** a **single logline + 5 beats** (**no prompts** — writing prompts now makes reaching 100 impossible).

| Dimension | Weight | Threshold | What it looks at |
|-----------|--------|-----------|------------------|
| Absurdity strength | 0.35 | **≥3** | Is it something "a human could invent and AI could not" |
| Sayable and memorable in one line | 0.25 | **≥3** | Can it be the title as-is |
| Fits 15 s | 0.20 | **≥3** | Does it have two twists (see the §4 time structure) |
| Shot feasibility | 0.10 | — | Can i2v actually shoot it (no impossible physics) |
| Platform friendliness | 0.10 | — | No real faces / existing IP / existing music / sensitive elements |

Flow: **100 → 20** (by score) → **20 → 5** (re-scored, and checked against "has this idea been done already") → **5 → 1** (the final topic).
**Any failed threshold is an outright veto**, regardless of the total.

### ② Prompt selection (10 → 1)

Write **10 full r2v prompts** (all three sections, see the format note below) for the **final topic only**, and score each one:

| Dimension | Weight | Threshold | What it looks at |
|-----------|--------|-----------|------------------|
| Fidelity | 0.30 | **≥3** | Which of the 10 actually shoots that logline (instead of turning into another story) |
| Shot executability | 0.25 | **≥3** | Do the 5 beats land on the cuts at **0 / 1.9 / 6.3 / 11.1 / 13.3 s**; is the action a **process** rather than a state |
| The two sound sections hold | 0.20 | **≥3** | Does `overall_soundscape` carry **concrete physical sounds** (steps, fabric, objects), and does `non_diegetic_music` rise and fall with the emotion |
| First-frame compatibility | 0.15 | — | Does it match the reference image (look / composition / the clear bottom quarter) |
| Per-frame information density | 0.10 | — | Is there any section of the 15 s that idles |

Flow: **10 → 3** (by score) → render a **vertical keyframe** for each of the 3 and judge by eye → **3 → 1** (the final prompt).
The other 9 versions are **all archived**: they can be re-shot next period in another art style, or kept as "different solutions to the same topic".

**Archive layout**:

```text
topics/hunt/<date>-r<N>.md        # all 100 topics + per-item score + reason for elimination (traceable, never deleted)
prompts/hunt/<slug>/<date>.md     # the 10 prompts for that topic + per-version score
prompts/<slug>.txt                # the final prompt in full (three sections: reference sentence / shots / two sound sections)
refs/<slug>.png                   # the final vertical reference image (9:16)
```

> **In this project a "topic" means one shootable brief (a logline + 5 beats), not a Douyin hashtag**; hashtags are in §3.
> ⚠️ Both layers must keep **the eliminated entries and the reasons** — half the value of a selection funnel is "what was chosen", the other half is "what was dropped and why".

> The required prompt form (**the main route and the local fallback share one three-section structure**) is documented in
> [seedance-reference-to-video/references/api-node.md](../../.agents/skills/seedance-reference-to-video/references/api-node.md) §5
> and [image-to-video-fastvideo3/references/prompt-format.md](../../.agents/skills/image-to-video-fastvideo3/references/prompt-format.md):
> **the first-frame reference sentence (`<Picture 1>`…) + `integrated_multimodal_description` (shots + timecodes) + `overall_soundscape` + `non_diegetic_music` — no section may be omitted**.

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
| Direction | **Topic selection 100 → 1** (text only: one logline + 5 beats) | all 100 archived with scores; **1 final topic** |
| Lock-in | **Prompt selection 10 → 1** (10 full prompts for the final topic) + 3 vertical keyframes rendered with **Seedream** | all 10 archived with scores; **1 final prompt** + reference image |
| Final | 1–2 runs of **Seedance r2v** (paid; `--plan` first) → pick 1, add subtitles / cover / compliance mark | 1 episode + both archives complete |
| Spin-off | Same topic with a different art style or character; series publishing | Episode count and data review |

> Money-saving combination: **try things locally** (Z-Image + FastH3, free and unlimited), **render the final in the cloud** (Seedream + Seedance, paid but better consistency and quality).

---

## 10. Sub-topics (**not started**)

As requested, **this period defines the project spec only and starts no sub-topics**. Before starting them, four things must be decided:

1. **What dimension splits the sub-topics**: content device (logic / scale / material / causality / jargon)? Subject (office / kitchen / space / antiquity)? Or a character?
2. **How many episodes per sub-topic**: compare [shanhai-jing](../shanhai-jing/README.en.md)'s "one creature per episode" with [bio-splice](../bio-splice/README.en.md)'s "5 periods per sub-topic".
3. **Whether to use a fixed character**: a fixed character builds series recognition but stacks i2v consistency risk on top (the look must be re-anchored every episode).
4. **Every sub-topic runs both funnels separately** (topics 100 → 1, prompts 10 → 1); **scores are not reused across sub-topics** — "absurdity strength" does not mean the same thing under a different dimension.

---

## 11. Production log

| Episode | Version | Skill/method | seed / task_id | local_path | Notes |
|---------|---------|--------------|----------------|------------|-------|
| — | — | — | — | — | not started |

---

## 12. Checklist

- [ ] **Main route**: the reference image is generated as **9:16** with Seedream (series consistency); **fallback route**: the reference image must also be 9:16 (local i2v takes the canvas from the input image — anything else is a redo)
- [ ] The reference image leaves the **bottom quarter** clear for subtitles; on the local i2v route it must also be ≤ ~1MP
- [ ] **Topic selection 100 → 1** archived: all 100 entries + per-item score + reason for elimination (§7①)
- [ ] **Prompt selection 10 → 1** archived: 10 full prompts + per-version score (§7②)
- [ ] Both cloud stages **validated for free first**: Seedance `--plan` (no submit, no upload); confirm all three prompt sections are present
- [ ] Cloud render parameters confirmed: `--duration 15`, `--ratio 9:16`, `--resolution` (or, on the local fallback route, **362** frames with no warning)
- [ ] The **"5 steps before the first real run" of `seedance-reference-to-video` have been walked** (it is currently built-but-unverified, §5)
- [ ] First frame compared against the reference image (by eye and, when needed, `image-tools` SSIM)
- [ ] The episode tells **one thing** and hits **≥2** absurdity devices (§4)
- [ ] A hook in the first 3 seconds; a still end card after 13.3 s
- [ ] **Compliance**: AI corner mark on the opening frame + platform AI declaration (§8)
- [ ] **Brand kit applied**: the opening line "我是那个 AI。我叫硅基小张。", the title template and the end card "收到，人类。" ([ACCOUNT.en.md](ACCOUNT.en.md) §2/§4)
- [ ] The final is recorded as the **model + verbatim prompt + parameters + seed** tuple
- [ ] Docs are bilingual (`README.md` + `README.en.md`) and `tools/i18n.py check` reports zero on all three counters
- [ ] No large intermediates (`work/`, `out/`) committed

---

## 13. Revision log

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-11 | v0.1 | **Project created (spec only, no sub-topics started)**: settled the format (vertical 9:16 / 15.083 s = 362 frames / image + text + sound), the keywords and hashtags, the 15-second time structure and the "five absurdity devices", the reference-to-video route (including the hard constraint "the canvas follows the input image, so the reference image must be 9:16 first"), the **100 → 1 selection funnel and scorecard** (with the arithmetic showing that running all 100 through i2v would cost ≈33 h of GPU, so selection must happen on the text and keyframe layers), and the **AI-generated content labelling requirement** (the Labelling Measures took effect 2025-09-01: video needs a conspicuous notice on the opening frame and a proactive declaration when publishing) | 小七 |
| 2026-10-11 | v0.2 | **The funnel was split into two layers (as requested)**: §7 rewritten as "**topic selection 100 → 1** → **prompt selection 10 → 1**" — the topic layer scores only "is this an idea only a human could have" (100 → 20 → 5 → 1, with veto thresholds) and the prompt layer scores only "can it be shot" (10 → 3 → 1, across fidelity / shot executability / the two sound sections / first-frame compatibility / information density); both layers are decided **on text**, so the GPU only pays for 3 keyframes and 1–2 real renders (≈1 h instead of 33 h). Also updated §2 deliverables, §9 execution plan (Direction = topics 100 → 1, Lock-in = prompts 10 → 1), §10 sub-topics (each runs both funnels; scores not reused), §12 checklist (one item per archive) and the archive paths (`topics/hunt/` and `prompts/hunt/<slug>/`) | 小七 |
| 2026-10-11 | v0.3 | **The technical route moved to three cloud stages (as requested)**: §5 rewritten — **images with [seedream-text-to-image](../../.agents/skills/seedream-text-to-image/SKILL.md), image edits with [seedream-image-edit](../../.agents/skills/seedream-image-edit/SKILL.md), reference-to-video with [seedance-reference-to-video](../../.agents/skills/seedance-reference-to-video/SKILL.md)**; the local Z-Image / FastH3 routes were demoted to **free fallbacks for trial and error**. Three stale assumptions were corrected as a consequence: ① §6 where the canvas comes from (cloud = explicit `--ratio 9:16`, only `adaptive` follows the reference image; local = still "the input image decides"); ② §2/§4 duration quantisation (cloud `--duration 15` has no frame grid; local is 362 frames = 15.083 s); ③ §7 cost table (keyframes and renders are now **per-image / per-run paid**, with "never burn the selection funnel on paid endpoints" written in as a rule). §5 also states plainly that **the unit prices of all three cloud stages are unverified by this project**, and that `seedance-reference-to-video` is a **built-but-unverified** skill whose "5 steps before the first real run" must be walked first | 小七 |
| 2026-10-11 | v0.4 | **The account identity got its own file**: added [ACCOUNT.en.md](ACCOUNT.en.md) (bilingual pair) — the name **`硅基小张`** (a proper noun: silicon-based identity + an everyday human name), the protagonist as a silicon-based worker hired by humans, **first person throughout**, the opening line "我是那个 AI。我叫硅基小张。", the end card "收到，人类。", employee number 07 and a three-part title template; plus the protagonist sheet, the brand "kit + corpus", the future-topic extension test, the naming rationale (why not a descriptive name), the alternative persona "碳基小张" with its switching cost, the open items and the pre-launch checklist. A navigation line was added to this file's header and one checklist item ("brand kit applied") to §12 | 小七 |
