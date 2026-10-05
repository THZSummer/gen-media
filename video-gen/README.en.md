# Video Generation - Main Navigation

> 🌐 Language: **English** | [中文](README.md)

> A video generation knowledge base built on **Volcengine Ark** video generation capabilities (Doubao Seedance series).
> 💰 **Profile routing**: the Seedance 2.0 series (including mini) goes through platform pay-as-you-go (`--profile platform_cn-beijing_accountwide`); all other models (seedream images / seedance-1.5-pro / TTS / ASR) go through agent-plan. The Medium plan does not include the 2.0 series, and 1.5-pro is about to be retired.
> Tool entry: `arkcli +gen` (three-step workflow: ① `resources list` to find available models -> ② `models get` to check supported_params -> ③ `+gen` to generate).

---

## 1. Organisation

This library is organised along three lines: **"methods" + "skills" + "projects"**:

```
video-gen/
├── README.md          ← you are here (main navigation)
├── methods/           technical method handbook: covers "how to generate" by generation path
│   ├── README.md        method overview (capability map + three-step workflow + 8 methods)
│   ├── text-to-video/   text-to-video
│   ├── image-to-video/  image-to-video
│   ├── reference-video/ reference video
│   ├── audio-driven/    audio-driven
│   ├── cinematography/  cinematography
│   ├── quality-and-cost/quality and cost
│   ├── long-video-chain/long-video chaining
│   └── content-safety/  content safety
├── skills/            executable skills: with scripts and workflow assets, covers "how to run it" (local ComfyUI)
│   ├── README.md        skill index + local/cloud path-selection table
│   ├── text-to-video-fastvideo3/   text-to-video + synchronized audio (t2va)
│   └── image-to-video-fastvideo3/  image-to-video + synchronized audio (fl2va, first/last frame)
└── projects/          concrete projects: one directory per project, covers "what to generate"
    ├── README.md        project index + project conventions
    └── _template/       project template (copy and use)
```

### How the three lines relate

| Line | Answers | Organised as |
|----|------|----------|
| **[methods/](methods/README.en.md)** | **How to generate** (technical paths, cloud Ark first) | One directory per technical method, reusable |
| **[skills/](skills/README.md)** | **How to run it** (executable skills, local ComfyUI) | One directory per skill, with `SKILL.md` + scripts + workflows |
| **[projects/](projects/README.en.md)** | **What to generate** (concrete business) | One directory per project, referencing methods / skills |

A **project** picks and combines several **methods** or **skills** as needed: for example, a "product ad project" = image-to-video (first frame) + cinematography + long-video chain.

---

## 2. Navigation

- 📚 **[methods/](methods/README.en.md)** — technical method handbook
  - Four input paths — text-to-video / image-to-video / reference video / audio-driven — plus four cross-cutting controls: cinematography / quality / chaining / safety
  - Each method covers: capability mapping, prompt strategy, parameter selection, command templates, pitfalls, checklists
- 🛠️ **[skills/](skills/README.md)** — executable skills (local ComfyUI)
  - [text-to-video-fastvideo3](skills/text-to-video-fastvideo3/SKILL.md): FastH3 text-to-video + **synchronized audio**, an 8-step render
  - [image-to-video-fastvideo3](skills/image-to-video-fastvideo3/SKILL.md): FastH3 image-to-video (first frame / optional last frame) + synchronized audio
  - ⚠️ Cost: 35 GB of weights squeezed into 8 GB of VRAM, so slowness is inevitable (the skill has a cost section and workarounds); the two share weights and cannot run at the same time
- 🗂️ **[projects/](projects/README.en.md)** — concrete projects
  - One directory per project; each project's `README.md` is that project's video generation plan
  - To create a project: copy [_template/](projects/_template/README.en.md) and adapt it

---

## 3. Quick start

### Find a method

Open [methods/README.md](methods/README.en.md) for the capability map and pick a path based on the material you have:

| What you have | Which method |
|----------|-----------|
| Only a text description | [text-to-video](methods/text-to-video/README.en.md) |
| One image | [image-to-video](methods/image-to-video/README.en.md) |
| A reference video | [reference-video](methods/reference-video/README.en.md) |
| A piece of audio | [audio-driven](methods/audio-driven/README.en.md) |

### Create a project

Go to [projects/](projects/README.en.md), copy `_template/` to create a project directory, and plan the deliverables, the storyboard, and the methods to use in the project README.

### The universal three-step workflow (applies to every method)

```bash
arkcli resources list --modality video                   # Step 1: list available models
arkcli models get "$MODEL" --transform supported_params  # Step 2: check the parameters
arkcli +gen --model "$MODEL" "<prompt>" --open           # Step 3: generate (video is asynchronous, returns task_id)
arkcli gen get <task_id> --open                          # poll until succeeded, then auto-download
```

See [methods/README.md](methods/README.en.md) for details. The glossary is in that document too.

---

## Document revision history

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-07-18 | v1.0 | Initial plan; created the 8 topic subdirectories and the main navigation | 小七 |
| 2026-07-18 | v2.0 | Restructured the top level around "projects": methods/ aggregates technical methods, projects/ is organised by concrete project | 小七 |
| 2026-07-18 | v2.1 | Noted that agent-plan does not include video and platform pay-as-you-go is required (only mini is available); added draft/last-frame/save-to pitfalls | 小七 |
| 2026-07-18 | v2.2 | Corrected the plan description: Medium includes seedream-5.0-lite/seedance-1.5-pro/TTS/ASR and excludes only the 2.0 series; recorded the profile routing rules | 小七 |

> 📦 **Size policy (2026-10-05)**: to bring the repository size back below Gitee's warning threshold,
> **per-round intermediate artifacts are no longer committed** (local files are kept, and a fixed seed makes them reproducible):
> - intermediates such as `out/v3-optimized/`, `out/v3-chain-10shots/`, per-shot `shot*.mp4`, `test_*.mp4`, `cgt-*.mp4`
- Each project keeps **one final film** (`*_full.mp4` / `*_narrated.mp4`) plus all documents and storyboard images

> So the relevant links in this document point to **local files**, which do not exist in the remote repository.
