# gen-media · Generative Media

> 🌐 Language: **English** | [中文](README.md)

> A knowledge base and portfolio for **image generation** (local ComfyUI: Z-Image-Turbo / Qwen-Image / Fun Union ControlNet) and **video generation** (local FastVideo FastH3; cloud Seedance via `arkcli`).
>
> 🗂️ **Flattened structure (2026-10-05)**: `image-gen/` and `video-gen/` are gone; the repository is split by **content kind** into three parts — `.agents/skills/`, `projects/` and `methods/`. Image and video techniques now live in **one skill library**.

---

## 1. Layout

```
gen-media/
├── README.md          <- you are here (main entry)
├── .agents/skills/    Skill library: dev-guide (the development spec) + 5 executable techniques, image and video together
│   ├── README.md          skill index (capability map + routing table + prerequisites and self-checks)
│   ├── dev-guide/                 the repository development spec: load before adding or changing anything
│   ├── text-to-image-comfyui/     text to image: Z-Image-Turbo (fast) + Qwen-Image (detailed)
│   ├── image-edit-comfyui/        ControlNet image editing: Z-Image Fun Union ControlNet
│   ├── image-tools/               deterministic image tooling (no AI): contact sheets / diffs / metadata strip / resize
│   ├── text-to-video-fastvideo3/  text to video with synced audio (t2va)
│   └── image-to-video-fastvideo3/ image to video with synced audio (fl2va, first/last frame)
├── projects/          Project library: 9 projects, one directory each (image and video together)
│   ├── README.md          project index + conventions
│   ├── _template/         project template (copy and use; shared by image and video)
│   ├── bio-splice/ bone-china-doll/ character-lookbook/ shanhai-jing/     (image)
│   └── giant-kingdom/ step-scenery/ step-scenery-v2/ survival-island/ tea-shake-dance/  (video)
├── methods/           video method notes: 10 of them (mostly cloud Ark Seedance)
├── site/              bilingual gallery front end: app.css / app.js / data/*.json
└── tools/             toolchain: build_site.py, preview.sh, i18n.py
```

---

## 2. Entries

| I want to... | Go to |
|--------------|-------|
| **add something here / align with the spec before committing** | [`.agents/skills/dev-guide/SKILL.md`](.agents/skills/dev-guide/SKILL.md) (bilingual, site, skill, generation, asset and collaboration conventions + a check script) |
| make an image from text | [.agents/skills/text-to-image-comfyui](.agents/skills/text-to-image-comfyui/SKILL.md) (Z-Image-Turbo fast / Qwen-Image detailed) |
| edit an image from a control image / change background | [.agents/skills/image-edit-comfyui](.agents/skills/image-edit-comfyui/SKILL.md) (Fun Union ControlNet) |
| contact sheet / diff two images / strip metadata / resize | [.agents/skills/image-tools](.agents/skills/image-tools/SKILL.md) (no AI, deterministic) |
| make a video with audio from text alone | [.agents/skills/text-to-video-fastvideo3](.agents/skills/text-to-video-fastvideo3/SKILL.md) (local FastH3) |
| make a video from a storyboard image | [.agents/skills/image-to-video-fastvideo3](.agents/skills/image-to-video-fastvideo3/SKILL.md) (local FastH3) |
| look up video technique and cost (cloud) | [methods/](methods/README.en.md) |
| see a complete project's plan and finals | [projects/](projects/README.en.md) |
| pick a technique / confirm the environment is healthy | [.agents/skills/README.md](.agents/skills/README.md) (routing table + one self-check command per technique) |

---

## 3. What the three parts do

| Part | Answers | Organisation |
|------|---------|--------------|
| [.agents/skills/](.agents/skills/README.md) | **how to do it** (executable technique) | one directory per technique, with `SKILL.md` + scripts + a self-check; **only what runs on the real machine is admitted** |
| [projects/](projects/README.en.md) | **what to make** (concrete work) | one directory per project, planned once, referencing skills / methods |
| [methods/](methods/README.en.md) | **how to generate** (video method notes, mostly cloud) | one directory per method, reusable |

A **project** picks the **techniques** or **methods** it needs: for example bio-splice = text to image (Z-Image-Turbo, round by round) + deterministic tooling (contact sheets / pixel diffs / scoring evidence).
Image projects are often the upstream step of video projects: storyboard images and first frames are produced under `projects/<image project>/out/` and consumed by `image-to-video-fastvideo3`.

---

## 4. Flagship project: bio-splice

A cross-species, cross-kingdom "part transplant" image series, the largest project here:

- **12 sub-themes × 5 periods = 60 periods, 135 finals** (cat-eagle, dragon-nines, turtle-snake, fish-bird, deer-crane, lichen, cordyceps, flytrap-fang, flower-bird, tree-beast, wing-atlas, horn-atlas)
- Engine **Z-Image-Turbo** (ComfyUI, 1024² / 1280², 12 steps, about 25 s per image)
- Every round carries a same-round **base control**; only images passing the five-dimension A–E scoring become finals; **110 mechanism conclusions** accumulated
- Entry: [projects/bio-splice/README.en.md](projects/bio-splice/README.en.md) ｜ full summary and 12 sub-theme contact sheets: [SUMMARY.en.md](projects/bio-splice/SUMMARY.en.md)

Another one worth reading is [projects/shanhai-jing](projects/shanhai-jing/README.en.md): a project that records all eight rounds — including three failed iterations and one overturned path — in full.

---

## 5. Prerequisites

| Dependency | Purpose |
|------------|---------|
| ComfyUI HTTP API (`192.168.3.5:18000`, remote Windows + RTX 4060 Ti 8 GB) | image text-to-image / image editing, video (Z-Image-Turbo, Qwen-Image, Fun Union ControlNet, FastH3) |
| `ffmpeg` | image codecs, contact sheets, compositing, metadata stripping, video concatenation |
| Python 3 + numpy | scoring, per-pixel diffs, sheet generation (`image-tools` does not need Pillow) |
| `arkcli` (Volcengine Ark) | **used by `methods/` only**: Seedance video, TTS/ASR |

> NOTE on paths: every path in these docs is relative to the repository root (`.agents/skills/...`, `projects/...`) and can be copied and run directly.
> After changing the environment, run the self-check command listed for each technique in `.agents/skills/README.md` before generating anything.

---

## 6. Size and provenance

- **Source**: `Book/image-gen` + `Book/video-gen` in the `gits` repository (Gitee).
- **Import**: tracked files exported with `git archive` (ignored intermediates excluded automatically) -> moved to the repository root -> a single initial commit.
- **`gits` now references this repository as a submodule**: `GitHub/gen-media` in `.gitmodules` (branch `main`) — it stores a **pointer, not a copy**. The original directories were removed from `gits` history (1059 files / 168 -> 69 commits).
- **Not included**: intermediates such as `work/` and half-finished rounds — they are **deterministic** and reproduce pixel-for-pixel from a fixed seed, so they are not committed.
- **Size**: largest single file about 13 MB (video `.mp4`), **no Git LFS**.
- **Image conventions**: finals and controls are PNG (lossless, metadata stripped); contact sheets and audit images are JPEG (to control size).

---

## 7. Maintenance and extension

**This repository is the source of truth**: add techniques / projects / methods by creating directories under `.agents/skills/`, `projects/` and `methods/`, following each area's `README.md`.

| What to add | Where | Convention |
|-------------|-------|------------|
| a new technique | `.agents/skills/<name>/SKILL.md` | [.agents/skills/README.md](.agents/skills/README.md); only with scripts, a self-check and a real-machine run |
| a new project | `projects/<name>/` | copy `projects/_template/`; index in [projects/README.en.md](projects/README.en.md) |
| a new video method | `methods/<name>/` | see [methods/README.en.md](methods/README.en.md) |

### Committing and collaborating (including the submodule pointer)

```bash
# 1) this repository
git add -A && git commit -m "<what changed + the evidence>" && git push

# 2) advance the submodule pointer in the parent repository gits
#    (otherwise gits still records the old revision)
cd ../.. && git submodule update --remote GitHub/gen-media \
  && git add GitHub/gen-media \
  && git commit -m "chore(submodule): gen-media → <sha>" && git push
```

> WARNING — **Gitee quota**: the `gits` repository already exceeds Gitee's 819 MB threshold (usage > 80%),
> so pushing more large files may be hard-blocked.
> Large intermediates (`work/`, `out/r*/`, per-shot mp4) stay uncommitted per each directory's `.gitignore`.

---

## 8. Language versions (i18n)

**The Chinese `X.md` is the default; the English version is `X.en.md` with the same name.** Both files carry a language-switch line at the top; **edit them in pairs**.

| Convention | Detail |
|------------|--------|
| Naming | `README.md` ↔ `README.en.md`; `projects/<project>/README.md` ↔ `README.en.md` |
| Excluded | `.agents/skills/**` (including `.agents/skills/README.md`) and `.agents/skills/**` stay Chinese-only (skill docs are written for execution, not translation) |
| Links | relative links inside an English file point to `.en.md`; when no English version exists they point to the Chinese one (no dead links) |
| Code | **kept verbatim**: commands, paths, filenames, model IDs, parameter names, seeds, verbatim prompts, sample strings |
| Comments inside code blocks | **translated**: directory-tree annotations, `#` comments in bash examples, labels in ASCII diagrams |
| Tooling | `python3 tools/i18n.py status / switch / links / check` — coverage report, switch lines, link fixing, health check |

```bash
python3 tools/i18n.py status          # which markdown files still lack an English version
python3 tools/i18n.py check           # health check: missing / apparently untranslated / broken English links
python3 tools/i18n.py switch          # write or refresh the language-switch line on both sides
python3 tools/i18n.py links           # repoint English relative links at .en.md
```

---

## Revision history

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-05 | v1.0 | Split `Book/image-gen` and `Book/video-gen` out of `gits` into a standalone repository | 小七 |
| 2026-10-05 | v1.3 | Added the bilingual convention (Chinese default + `X.en.md`) and `tools/i18n.py` | 小七 |
| 2026-10-05 | v2.0 | **Flattening refactor**: dropped the `image-gen/` + `video-gen/` split in favour of `.agents/skills/` (5 techniques together) + `projects/` (9 projects) + `methods/` (video methods); the two skill indexes merged, the two project indexes and templates merged; `tools/{i18n,build_site}.py` and dev-guide updated; **corrected the inaccurate claim that "this repository is the only copy and has no upstream"** — `gits` references it as a submodule | 小七 |
