# gen-media · Generative Media

> 🌐 Language: **English** | [中文](README.md)

> A knowledge base and portfolio for **image generation** (local ComfyUI: Z-Image-Turbo / Qwen-Image / Fun Union ControlNet) and **video generation** (local fastvideo3; cloud Seedance via `arkcli`).
> This repository is the standalone archive of the `Book/image-gen` and `Book/video-gen` libraries from the `gits` workspace: the tracked files were exported with `git archive` and rebuilt as a **single initial commit**, so the original repository's commit history is not preserved.

---

## 1. Layout

```
gen-media/
├── README.md          ← you are here (main entry)
├── .dsh/skills/       DSH project skill: dev-guide (the development conventions; skills stay Chinese-only)
├── image-gen/         image generation: skills + projects + final images   (824 files / ~435 MB)
│   ├── README.md          image library home
│   ├── skills/            3 executable skills (text-to-image / control-image edit / deterministic tools)
│   └── projects/          bio-splice, bone-china-doll, character-lookbook, _template
├── site/              gallery front end (bilingual): app.css / app.js / data/*.json
├── tools/             toolchain: build_site.py, preview.sh, i18n.py
└── video-gen/         video generation: methods + skills + projects + films (235 files / ~114 MB)
    ├── README.md          video library home
    ├── methods/           10 method notes (text-to-video / image-to-video / reference video / audio-driven / cinematography …)
    ├── skills/            local ComfyUI executable skills (fastvideo3 t2va / fl2va)
    └── projects/          giant-kingdom, step-scenery, step-scenery-v2, survival-island, tea-shake-dance
```

**1059 files / about 550 MB** in total.

---

## 2. Entry points

| I want to… | Go to |
|------|------|
| **Add something to this repository / align with the conventions before committing** | [`.dsh/skills/dev-guide/SKILL.md`](.dsh/skills/dev-guide/SKILL.md) (bilingual docs, site, skills, generation, assets, collaboration + a check script) |
| Generate an image from text | [image-gen/skills/text-to-image-comfyui](image-gen/skills/text-to-image-comfyui/SKILL.md) (local ComfyUI: Z-Image-Turbo for speed / Qwen-Image for detail) |
| Edit an image / change the background following a control image | [image-gen/skills/image-edit-comfyui](image-gen/skills/image-edit-comfyui/SKILL.md) (Fun Union ControlNet) |
| Build a contact sheet / compare two images / strip metadata / resize | [image-gen/skills/image-tools](image-gen/skills/image-tools/SKILL.md) (no AI, fully deterministic) |
| Study a complete image project's plan and output | [image-gen/projects/](image-gen/projects/README.en.md) |
| Turn storyboard frames into video | [video-gen/skills/image-to-video-fastvideo3](video-gen/skills/image-to-video-fastvideo3/SKILL.md) |
| Generate a video with audio from text alone | [video-gen/skills/text-to-video-fastvideo3](video-gen/skills/text-to-video-fastvideo3/SKILL.md) |
| Look up video techniques and cost | [video-gen/methods/](video-gen/methods/README.en.md) |

---

## 3. How the two libraries divide the work

| Library | Answers | Organised as |
|----|------|----------|
| [image-gen](image-gen/README.en.md) | **what to generate / how to generate images** | skills (technical paths) × projects (concrete work) |
| [video-gen](video-gen/README.en.md) | **how to turn images into video / how to generate video directly** | method notes × executable skills × projects |

Images are the upstream step of video: the storyboard frames and first frames produced by `image-gen` are consumed by the I2V skills in `video-gen`. Conversely, `video-gen`'s `methods/text-to-image/` overlaps historically with `image-gen` (the video library was split off from the image capabilities).

---

## 4. Flagship project: bio-splice

A cross-species, cross-kingdom "part transplant" image experiment series, and by far the largest project here:

- **12 sub-themes × 5 periods = 60 periods, 135 finals** (cat-eagle, dragon-nines, turtle-snake, fish-bird, deer-crane, lichen, cordyceps, flytrap-fang, flower-bird, tree-beast, wing-atlas, horn-atlas)
- Engine **Z-Image-Turbo** (ComfyUI, 1024² / 1280², 12 steps, about 25 s per image)
- Every round carries a same-round **base control**; only images passing the five-axis A–E review are curated; **110 mechanism findings** accumulated so far (topic selection / wording / layout / presentation / process)
- Entry: [image-gen/projects/bio-splice/README.md](image-gen/projects/bio-splice/README.en.md) ｜ full summary and 12 sub-theme contact sheets: [SUMMARY.md](image-gen/projects/bio-splice/SUMMARY.en.md)

---

## 5. Prerequisites

| Dependency | Purpose |
|------|------|
| ComfyUI HTTP API (`192.168.3.5:18000`, remote Windows + RTX 4060 Ti 8 GB) | image text-to-image / control-image edit, video (Z-Image-Turbo, Qwen-Image, Fun Union ControlNet, fastvideo3) |
| `ffmpeg` | image encode/decode, contact sheets, compositing, metadata stripping, video concatenation |
| Python 3 + numpy | scoring, per-pixel diffs, sheet generation (`image-tools` does not need Pillow) |
| `arkcli` (Volcengine Ark) | **video library only**: Seedance video, TTS/ASR (the cloud image doc-skills were removed on 2026-10-05) |

> 📌 **Path convention**: every path in these documents is relative to the repository root (e.g. `image-gen/skills/...`, `video-gen/projects/...`).
> On 2026-10-05 the remaining old absolute paths (`/home/usb/wks/gits/Book/...`, a layout that no longer exists) were all rewritten to relative paths, so they can be copied and run as-is.

---

## 6. Size and provenance

- **Source**: `Book/image-gen` + `Book/video-gen` at commit `b1e14ad` of the `gits` repository (Gitee).
- **Import method**: `git archive` exported the tracked files (automatically excluding ignored intermediates) → moved to the repository root → one initial commit.
- **The original repository no longer contains this material**: both directories were removed from the `gits` index and history with `filter-branch` (1059 files / 168→69 commits), and the local working copies were deleted. **This repository is the only copy of this content.**
- **Not included**: `work/` and similar intermediates and rejected rounds — they are **deterministic** and can be reproduced pixel-for-pixel from a fixed seed, so they are not committed. Those intermediates on the workstation were removed along with the directories: the image ones can be regenerated from their seeds; the old intermediate videos under `video-gen` are superseded versions (the finals are all in this repository) and were not kept.
- **Size**: 1059 files / about 550 MB, largest single file about 13 MB (a final `.mp4`), **no Git LFS** (every file is far below GitHub's 100 MB per-file limit).
- **Image convention**: finals and controls are PNG (lossless, metadata stripped); contact sheets and audit sheets are JPEG (to keep the size down).

---

## 7. Maintenance and extension

**This repository *is* the source of truth** — there is no upstream. To add a skill or project, create the directory under `image-gen/` or `video-gen/`, organise it according to that library's `README.md`, then `git commit` + `git push` as usual.

| What to add | Where | Reference |
|----------|------|----------|
| A new image project | `image-gen/projects/<project>/` | copy `image-gen/projects/_template/`; index in `image-gen/projects/README.md` |
| A new image skill | `image-gen/skills/<skill>/SKILL.md` | skill index in `image-gen/skills/README.md` |
| A new video project / method / skill | `video-gen/{projects,methods,skills}/` | see `video-gen/README.md` |

> Large intermediates (`work/`, `out/r*/`, per-shot mp4s, …) stay **out of the repository** per each directory's `.gitignore`; only finals and documents are kept, and anything else can be regenerated from the fixed seeds when needed.

---

## 8. Language versions (i18n)

**The Chinese `X.md` is the default version; the English one is the same-named `X.en.md`.** Both files start with a language-switch line, so **always update the pair together**.

| Convention | Detail |
|------|------|
| Naming | `README.md` ↔ `README.en.md`; `period-01/README.md` ↔ `period-01/README.en.md` |
| Excluded | `.dsh/skills/**`, `image-gen/skills/**` and `video-gen/skills/**` stay Chinese-only (skill docs are meant for execution, not translation) |
| Links | relative links inside an English file point at `.en.md`; when the target has no English version they point at the Chinese file (no dead links) |
| Code | **kept verbatim**: commands, paths, filenames, model IDs, parameter names, seeds, raw prompts, sample strings |
| Comments inside code blocks | **translated**: directory-tree annotations (the Chinese in `├── skills/   ← …`), `#` comments in bash examples, labels in ASCII diagrams — those are explanation, not content |
| Tooling | `python3 tools/i18n.py status / switch / links / check` — coverage report, switch lines, link rewriting, health check |

```bash
python3 tools/i18n.py status          # which .md files still lack an English version
python3 tools/i18n.py check           # health check: missing pairs / untranslated files / broken links
python3 tools/i18n.py switch          # create or update the language-switch lines on both sides
python3 tools/i18n.py links           # point relative links in English files at .en.md
```

---

## Revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v1.0 | Split `Book/image-gen` and `Book/video-gen` out of `gits` into a standalone repository | 小七 |
| 2026-10-05 | v1.1 | Added `tools/sync-from-gits.sh` and the "Maintenance" section | 小七 |
| 2026-10-05 | v1.2 | The original `gits` working copy and history were cleaned up; this repository became the only copy; the obsolete sync script was removed and "Maintenance" became "Maintenance and extension" | 小七 |
| 2026-10-05 | v1.3 | Added the bilingual convention (Chinese default + `X.en.md`) and `tools/i18n.py`; wording updated after the skill library was reduced to 3 executable skills | 小七 |
