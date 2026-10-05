# Projects (项目)

> 🌐 Language: **English** | [中文](README.md)

> Back to [home](../README.en.md) ｜ Technical skills in [../skills/](../skills/README.md)

---

## 1. What this directory is

Organized by **concrete project**: **one directory per project**, with a `README.md` under each project directory serving as that project's image generation plan.

Difference from [skills/](../skills/README.md):

| | skills/ | projects/ (this directory) |
|---|----------|---------------------|
| Answers | **How to generate** (technical) | **What to generate** (business) |
| Organization | Directories by technical path, one `SKILL.md` each, reusable | Directories by project, one-off planning |
| Relationship | Referenced by projects | References skills |

A project picks and combines several **skills** as needed and lands them as a concrete batch of image deliverables.

---

## 2. Project conventions

### Directory naming

- Lowercase English + hyphens, reflecting the project's character: `character-lookbook/`, `poster-2026q4/`, `brand-assets/`
- One project = one independent delivery goal (a batch of images + one plan)

### What a project README should contain

| Section | Content |
|------|------|
| Project background | Why do it, who it is for, where it is used |
| Deliverables list | Purpose, size and aspect ratio of each image |
| Skill selection | Which skill each image uses (link to skills/) |
| Image list | Image number / subject / scene / viewpoint / style |
| Prompt & parameters | prompt, model, key parameters, seed for each image |
| Execution plan | Arrangement of the targeting / shaping / final stages |
| Output record | Model, seed, local_path, version |
| Checklist | Items to verify before delivery |

### Creating a new project

```bash
cd image-gen/projects
cp -r _template <your-project>
# edit <your-project>/README.md
```

---

## 3. Project list

| Project | Description | Status |
|------|------|------|
| [_template/](_template/README.en.md) | Project template (copy and use, do not use directly) | Template |
| [character-lookbook/](character-lookbook/README.en.md) | Character design lookbook: front/side/back/multi-scene/multi-outfit design sheets for one character, reusable by video and design | Planning |
| [bone-china-doll/](bone-china-doll/README.en.md) | **Bone China Princess**: R1–R29 iterations. Stage 1 R1–R6 (Z-Image-Turbo); stage 2 R7–R16 (Qwen-Image 2512, quality highland R8–R10, final R10 `window-light`, R11/R12 are located degeneration rounds); stage 3 R17–R21 **theme changed to Eastern classical beauty**; stage 4 R22–R26 **de-figurinization + half-real half-bone-china** (a living princess, glaze sheen + real human blood colour, named glaze defects, half-gauze half-bone-china gauze); **stage 5 R27–R29 natural makeup + languid daily-life poses** (full-body sitting/lying/half-reclining everyday moments), current delivery set `out/final-set-life/` | Iterating |
| [bio-splice/](bio-splice/README.en.md) | **Bio-splice**: attach A's **organs** to B's body and shoot it in the realistic language of documentary photography (or microscopy/specimen). **Not limited to animals** — plants, fungi, algae and lichens can all serve as base or donor. Structure = project → sub-theme (by **biological combination**, **12** in total) → **period** (5 periods per sub-theme, finals only). See [PLAN.md](bio-splice/PLAN.en.md) for the plan; **all delivered: 12 sub-themes / 60 periods / 135 finals** (see [SUMMARY.md](bio-splice/SUMMARY.en.md) for the summary); every period and every sub-theme has its own contact sheet | Iterating (planning first) |

> New projects append a row here.

---

## 4. Relationship with video-gen

Image projects often serve as the upstream step of a [video-gen](../../video-gen/projects/README.en.md) project:

```
image-gen/projects/<project>/out/storyboard/  ──►  video-gen/projects/<project>/ (I2V final video)
```

- The same subject may have one project directory on each side (image plan + video plan), interfacing through `out/` artifacts
- Storyboard images / T2I first frames are finished and reviewed in image-gen; the video side is only responsible for "making them move"

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-02 | v1.0 | Created the project system and template; included the character-lookbook example project | 小七 |
| 2026-10-02 | v1.1 | Following the `methods/`→`skills/` reorganization: terminology changed to "skill", links point to skills/ | 小七 |
| 2026-10-02 | v1.2 | Added project bone-china-doll (bone china doll, 6 iteration rounds completed) | 小七 |
