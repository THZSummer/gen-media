# Image Generation · Master Navigation

> 🌐 Language: **English** | [中文](README.md)

> An image generation library built on **local ComfyUI** (remote GPU machine `http://192.168.3.5:18000`):
> text-to-image (two engines: Z-Image-Turbo / Qwen-Image), control-image edit (Z-Image Fun Union ControlNet),
> plus a set of **non-AI** deterministic image tools (ffmpeg + numpy: contact sheet / pixel comparison / metadata strip / resize & crop).
> 📌 Images are returned **synchronously**: submit and the image is produced; there is no `task_id` and no polling needed (polling is the asynchronous semantics of video).

> ⚠️ **As of 2026-10-05, this directory keeps only skills that ship scripts and run end-to-end on the real machine.** The original 9 documentation-only skills — which described only Ark Seedream cloud usage and had neither scripts nor a self-check entry point — have been removed: `text-to-image`, `image-editing`,
> `multi-image-reference`, `multi-view-consistency`, `prompt-engineering`, `parameters-and-output`,
> `quality-and-cost`, `content-safety`, `image-workflow`.
> Retrieve them from git history when needed: `git log --diff-filter=D --oneline -- image-gen/skills/`.

---

## 1. Organization

This library is organized along two lines: **"skills" + "projects"**:

```
image-gen/
├── README.md          ← you are here (main navigation)
├── skills/           skill library: one directory per skill, entry point is SKILL.md, covers "how to generate"
│   ├── README.md                 skill index (capability map + path-selection table + runtime prerequisites and self-check)
│   ├── text-to-image-comfyui/    ComfyUI text-to-image: two engines, Z-Image-Turbo (fast) + Qwen-Image (detailed)
│   ├── image-edit-comfyui/       ComfyUI image edit: driven by a Fun Union ControlNet control image
│   └── image-tools/              deterministic image tools (no AI): contact sheet / pixel comparison / metadata strip / resize & crop
└── projects/          concrete projects: one directory per project, covers "what to generate"
    ├── README.md              project index + project conventions
    ├── _template/             project template (copy and use)
    ├── bio-splice/            bio-splice: 12 sub-themes × 5 periods / 135 finals (main project)
    ├── bone-china-doll/       bone china doll series
    └── character-lookbook/    multi-angle character design lookbook (example project)
```

### How the two lines relate

| Line | Answers | Organization |
|------|---------|--------------|
| **[skills/](skills/README.md)** | **How to generate** (technical path) | Directories by technical path; each holds one `SKILL.md`, reusable |
| **[projects/](projects/README.en.md)** | **What to generate** (concrete business) | Directories by project, referencing skills |

A **project** picks and combines several **skills** as needed: for example, "bio-splice" = text-to-image (Z-Image-Turbo, one round at a time) + deterministic tools (contact sheet / per-pixel comparison / score evidence).

---

## 2. Navigation

- 📚 **[skills/](skills/README.md)** — skill library (3 skills, all with scripts)
  - Two generation paths — image out (text-to-image) → image edit (control-image edit) — plus one cross-cutting deterministic image toolbox
  - Each skill contains a `SKILL.md`: frontmatter (trigger description) + when to use + preflight checks + execution steps + pitfalls + checklist
  - `skills/README.md` has a **runtime prerequisites and self-check commands** table: one command per skill, so you can confirm at any time whether the environment is still healthy
- 🗂️ **[projects/](projects/README.en.md)** — concrete projects
  - One directory per project; each project's `README.md` is that project's image generation plan
  - New project: copy [_template/](projects/_template/README.en.md) and adapt it
- 🎬 **Companion video library**: [../video-gen/](../video-gen/README.en.md) (images are the upstream step of video; storyboard images / first frames are consumed over there)

---

## 3. Quick Start

### Find a skill

Go to [skills/README.md](skills/README.md) for the capability map and pick a path by the material at hand:

| What you have | Which skill to load |
|----------|-----------|
| Only a text description | [text-to-image-comfyui](skills/text-to-image-comfyui/SKILL.md) (Z-Image-Turbo for speed / Qwen-Image for high detail) |
| One control image (line art/photo/pose image) and you want to generate by structure | [image-edit-comfyui](skills/image-edit-comfyui/SKILL.md) |
| Combine several images into a contact sheet / compare two images for equality / strip metadata / resize & crop | [image-tools](skills/image-tools/SKILL.md) |

### Create a project

Go to [projects/](projects/README.en.md), copy `_template/` to create a project directory, and plan the deliverables, image list and skills used in the project README.

### Most-used commands (all verified on the real machine)

```bash
# Text-to-image: Z-Image-Turbo (fast, ~25 s/image @1024²)
cd image-gen/skills/text-to-image-comfyui
python3 scripts/comfyui_gen.py --check                       # confirm the server is reachable first
python3 scripts/comfyui_gen.py --prompt "..." --out-dir out/

# Text-to-image: Qwen-Image (detail engine, ~7–10 min/image, true negative prompts supported)
python3 scripts/comfyui_qwen.py --check                      # are the three model files in place
python3 scripts/comfyui_qwen.py --prompt "..." --negative "blurry, plastic, cartoon" \
  --width 1024 --height 1360 --steps 24 --cfg 3.0 --seed 7 --out-dir out/

# Control-image edit (output size defaults to the control image size)
cd ../image-edit-comfyui
python3 scripts/comfyui_edit.py --check                      # are the four model files in place
python3 scripts/comfyui_edit.py --image ref.png --prompt "..." --out-dir out/

# Deterministic tools: per-round contact sheet / pixel comparison / metadata strip
cd ../image-tools
python3 scripts/contact_sheet.py --round out/r1/round.json -o out/r1/sheet.png --cols 3
python3 scripts/pngdiff.py a.png b.png --json                # 0=same 1=different 2=error
python3 scripts/ffkit.py strip in.png -o out.png             # strip tEXt (pixels unchanged)
```

See [skills/README.md](skills/README.md) for details.

---

## 4. Runtime Prerequisites

| Dependency | Purpose | Current status (measured 2026-10-05) |
|------|------|------------------------------|
| ComfyUI `http://192.168.3.5:18000` (remote Windows + RTX 4060 Ti 8GB) | All generation skills | ✅ Reachable (ComfyUI 0.38.0) |
| Models `z_image_turbo_bf16` / `qwen_3_4b` / `ae` | Z-Image text-to-image | ✅ All three present |
| Models `qwen_image_2512_fp8_e4m3fn` / `qwen_2.5_vl_7b_fp8_scaled` / `qwen_image_vae` | Qwen-Image text-to-image | ✅ All three present |
| Model `Z-Image-Turbo-Fun-Controlnet-Union.safetensors` | Control-image edit | ✅ Present (via `ModelPatchLoader` + `ZImageFunControlnet`) |
| `ffmpeg` / `ffprobe` | Image encode/decode, contact sheet, metadata strip | ✅ ffmpeg 8.0.1 |
| Python 3 + numpy | Pixel comparison, score evidence | ✅ numpy 2.5.0 (**Pillow not needed**) |

Every skill ships its own self-check entry point; run it first after changing the environment (see the "Runtime prerequisites and self-check" table in [skills/README.md](skills/README.md) for details).

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-02 | v1.0 | Initial setup: split image generation out of video-gen into its own library; established 9 skills + project system + template + example project | 小七 |
| 2026-10-02 | v2.0 | `methods/` reorganized into the skill library `skills/`: every skill is presented as a `SKILL.md` (YAML frontmatter + instruction body); navigation and terminology fully switched to "skill" | 小七 |
| 2026-10-02 | v2.1 | Added the ComfyUI text-to-image skill (remote Z-Image-Turbo workflow, 192.168.3.5:18000): workflow JSON→/prompt API conversion + submit/poll/download script | 小七 |
| 2026-10-02 | v2.2 | Added the ComfyUI control-image edit skill image-edit-comfyui (Fun Union Controlnet): shared converter supports workflow profile / mute-bypass / link-type subgraph interface / SaveImage filtering; 24/24 real-machine parameter validations passed | 小七 |
| 2026-10-05 | **v3.0** | **Converged to "keep only executable skills"**: removed the 9 documentation-only skills with no scripts and no self-check entry point (Ark Seedream cloud usage) and kept the 3 skills that ship scripts and passed real-machine validation; master navigation, path-selection table, models and prerequisites all rewritten for the local ComfyUI path; 6 old absolute paths of the form `cd /home/usb/wks/gits/Book/...` changed to repository-relative paths | 小七 |
