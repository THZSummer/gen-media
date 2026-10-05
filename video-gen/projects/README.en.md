# Projects

> 🌐 Language: **English** | [中文](README.md)

> Back to [home](../README.en.md) ｜ Technical methods see [../methods/](../methods/README.en.md)

---

## 1. What this directory is

Organised by **concrete project**: **one project, one directory**, and inside each project directory a `README.md` serves as that project's video generation plan.

Difference from [methods/](../methods/README.en.md):

| | methods/ | projects/ (this directory) |
|---|----------|---------------------|
| Answers | **How to generate** (technical) | **What to generate** (business) |
| Organisation | Directories by technical method, reusable | Directories by project, one-off planning |
| Relationship | Referenced by projects | References methods |

A project picks a combination of methods as needed and turns it into a concrete set of video deliverables.

---

## 2. Project Conventions

### Directory naming

- Lowercase English + hyphens, reflecting the project's characteristics: `product-launch-2026q3/`, `spring-festival-greeting/`, `brand-intro/`
- One project = one independent delivery objective (a batch of videos + one plan)

### What a project README should contain

| Section | Content |
|------|------|
| Project background | Why do it, who it is for, where it is published |
| Deliverables list | Each video's purpose, duration and ratio |
| Method selection | Which method each video uses (link to methods/) |
| Storyboard table | Shot number / shot size / camera movement / content for multi-shot projects |
| Prompt & parameters | Each video's prompt, model and key parameters |
| Execution plan | The draft / lock / final stages arrangement |
| Output record | task_id, local_path, version |
| Checklist | Items to verify before publishing |

### Creating a new project

```bash
cd video-gen/projects
cp -r _template <your-project>
# edit <your-project>/README.md
```

---

## 3. Project List

| Project | Description | Status |
|------|------|------|
| [_template/](_template/README.en.md) | Project template (copy and use, do not use directly) | Template |
| [survival-island/](survival-island/README.en.md) | Survival island: a 6-shot 30s narrative short, an 18-year-old Eastern girl × extreme contrast (the island is not barren, the person is worse off) | Planning |
| [tea-shake-dance/](tea-shake-dance/README.en.md) | Have a nice cup of tea, shake it: an art dance short using "shake it" as the action motif, tea culture dancing into modern dance (all 6 shots detailed shot by shot) | Planning |
| [step-scenery/](step-scenery/README.en.md) | Change of scenery: a girl travels through time, one step one world (tea room→bamboo forest→desert→cyber→starry sky→snowfield→tea room, a closed loop) | Planning |
| [step-scenery-v2/](step-scenery-v2/README.en.md) | Change of scenery v2: the same story, seedance-2.0 native audio version (each shot carries its own scene sound effects) | Planning |
| [giant-kingdom/](giant-kingdom/README.en.md) | Crossing into the giant daughters' kingdom: a visual spectacle of body-size contrast (a giant hand blots out the sky / a palm like land / one shoulder one world) | Planning |

> Add new projects as one more row here.

---

## Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-07-18 | v1.0 | Top-level restructure adding projects/, establishing the project system and template | 小七 |
| 2026-08-01 | v1.1 | Added project tea-shake-dance (art dance short) | 小七 |
| 2026-08-01 | v1.2 | Added project step-scenery (girl crossing time · change of scenery) | 小七 |
| 2026-08-01 | v1.3 | Added project step-scenery-v2 (change of scenery v2, seedance-2.0 native audio version) | 小七 |
| 2026-08-01 | v1.4 | Added project giant-kingdom (crossing into the giant daughters' kingdom, a visual spectacle of body-size contrast) | 小七 |
