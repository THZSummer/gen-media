# Projects

> 🌐 Language: **English** | [中文](README.md)

> Back to [home](../README.en.md) ｜ Techniques in [../.agents/skills/](../.agents/skills/README.md) ｜ Video method notes in [../methods/](../methods/README.en.md)

> This directory merges `image-gen/projects/` and `video-gen/projects/` (flattened on 2026-10-05):
> **image and video are no longer separate libraries; everything is organised by project.**

---

## 1. What this directory is

Organised by **concrete project**: **one directory per project**, with a `README.md` inside as that project's generation plan.

| | [.agents/skills/](../.agents/skills/README.md) | [methods/](../methods/README.en.md) | projects/ (here) |
|---|---|---|---|
| Answers | **how to do it** (executable technique) | **how to generate** (method notes) | **what to make** (concrete work) |
| Organised | one directory per skill, with scripts and self-checks | one directory per method, reusable | one directory per project, planned once |
| Relation | referenced by projects | referenced by projects | references skills / methods |

A project picks the **skills** (images/video) or **methods** (cloud video) it needs and turns them into a concrete batch of deliverables.

---

## 2. Project conventions

### Directory naming

- lowercase English with hyphens, reflecting the project: `character-lookbook/`, `product-launch-2026q3/`, `brand-intro/`
- one project = one independent delivery goal (a batch of images/videos plus a plan)

### What a project README should contain

| Section | Content |
|---------|---------|
| Background | why it exists, who it is for, where it is used / published |
| Deliverables | purpose, size or duration and ratio of each final |
| Technique / method selection | which skill or method each final uses (link into .agents/skills/ or methods/) |
| Image list / shot list | image or shot number / subject / scene / angle / style (images); shot number / framing / camera move / content (video) |
| Prompt & parameters | prompt, model, key parameters, seed for each final |
| Execution plan | direction / shaping / final stages |
| Output log | model, seed, prompt_id or task_id, local_path, version |
| Checklist | items to verify before delivery |

### Creating a new project

```bash
cd projects
cp -r _template <your-project>
# edit <your-project>/README.md (and add README.en.md)
```

---

## 3. Project list

| Project | Kind | Description | Status |
|---------|------|-------------|--------|
| [_template/](_template/README.en.md) | Template | Project template (copy and use, do not use directly) | Template |
| [bio-splice/](bio-splice/README.en.md) | Image | **Bio-splice**: attach A's **organs** to B's body and shoot it in the realistic language of documentary photography (or microscopy/specimen). **Not limited to animals** — plants, fungi, algae and lichens can all serve as base or donor. Structure = project → sub-theme (by **biological combination**, **12** in total) → **period** (5 periods per sub-theme, finals only). See [PLAN.md](bio-splice/PLAN.en.md); **all delivered: 12 sub-themes / 60 periods / 135 finals** (see [SUMMARY.md](bio-splice/SUMMARY.en.md)); every period and every sub-theme has its own contact sheet | Iterating (planning first) |
| [bone-china-doll/](bone-china-doll/README.en.md) | Image | **Bone China Princess**: R1–R29 iterations. Stage 1 R1–R6 (Z-Image-Turbo); stage 2 R7–R16 (Qwen-Image 2512, quality highland R8–R10, final R10 `window-light`, R11/R12 are located degeneration rounds); stage 3 R17–R21 **theme changed to Eastern classical beauty**; stage 4 R22–R26 **de-figurinization + half-real half-bone-china**; **stage 5 R27–R29 natural makeup + languid daily-life poses**, current delivery set `out/final-set-life/` | Iterating |
| [character-lookbook/](character-lookbook/README.en.md) | Image | Character design lookbook: front/side/back/multi-scene/multi-outfit design sheets for one character, reusable by video and design | Planning |
| [shanhai-jing/](shanhai-jing/README.en.md) | Image | **Shan Hai Jing · illustrated verses**: a series driven by the verbatim *Shan Hai Jing*, one creature per period, each with **volume + original passage + Guo Pu's commentary**. Built for Xiaohongshu vertical posts (3:4). Plan in [PLAN.en.md](shanhai-jing/PLAN.en.md); the nine-tailed fox tuning period is delivered (R1–R8 fully recorded) | Tuning period complete |
| [survival-island/](survival-island/README.en.md) | Video | Survival island: a 6-shot 30s narrative short, an 18-year-old Eastern girl × extreme contrast | Planning |
| [tea-shake-dance/](tea-shake-dance/README.en.md) | Video | Tea shake dance: an art-dance short built on the "shake" motif, tea culture as modern dance (6 shots detailed) | Planning |
| [step-scenery/](step-scenery/README.en.md) | Video | Step scenery: a girl crossing time, one step one world (tea room → bamboo → desert → cyber → starfield → snow → tea room, closing the loop) | Planning |
| [step-scenery-v2/](step-scenery-v2/README.en.md) | Video | Step scenery v2: same story, seedance-2.0 native-audio version (each shot carries its own ambience) | Planning |
| [giant-kingdom/](giant-kingdom/README.en.md) | Video | Into the giant kingdom: body-scale contrast spectacle | Planning |

> New projects append a row here.

---

## 4. Linking images to video

Image projects often serve as the upstream step of a video project; the two sides meet through `out/` artifacts:

```
projects/<image project>/out/storyboard/  ──►  projects/<video project>/ (I2V final video)
```

- The same subject may have one project directory on each side (image plan + video plan), interfacing through `out/`
- Storyboard images / T2I first frames are finished and reviewed in the image project; the video side only makes them move
- Keep the ratios aligned: an image final's ratio must match the target video, otherwise it must be regenerated

---

## Revision history

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-02 | v1.0 | image-gen side: project system and template created, character-lookbook included | 小七 |
| 2026-08-01 | v1.4 | video-gen side: project system and template, 5 video projects accumulated | 小七 |
| 2026-10-05 | v1.5 | image-gen side: bone-china-doll added; shanhai-jing added later | 小七 |
| **2026-10-05** | **v2.0** | **Flattening merge**: `image-gen/projects/README.md` and `video-gen/projects/README.md` merged into this file; directory moved to `projects/` at the repo root; templates merged into `_template/`; project list became one unified image/video table (9 projects) | 小七 |
