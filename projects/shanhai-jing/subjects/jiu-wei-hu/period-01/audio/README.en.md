# Period narration (nine-tailed fox)

> 🌐 Language: **English** | [中文](README.md)

> Back to [project entry](../../../../README.en.md) ｜ Full plan in [PLAN.en.md](../../../../PLAN.en.md) ｜ Distribution in [DOUYIN.en.md](../../../../DOUYIN.en.md)

> **Why this layer exists**: the project's purpose is to **spread traditional culture and help ordinary people understand it**.
> The images let you *see*; **the narration is what lets you *understand*** — an ordinary viewer will never read
> "有獸焉，其狀如狐而九尾", but will listen to one plain sentence. Video is the long-term goal, and **until then the
> picture plus an explaining voice-over is the main form**.

---

## 1. What this audio is

| Item | Value |
|------|-------|
| Track role | **Explaining voice-over** (not BGM; BGM is only a bed, see §4) |
| Script | `narration.txt` (**one sentence per line**; the script splits on lines) |
| Segments / characters | 6 segments / 188 characters |
| Measured length | see §3 (estimated ≈ 43 s; `ffprobe` decides) |
| Voice | `zh_female_vv_uranus_bigtts` (steady female voice, suited to commentary) |
| Synthesis | `doubao-seed-tts-2.0` (`seed-tts-2.0`, see [methods/text-to-speech](../../../../../../methods/text-to-speech/README.en.md)) |
| Command | `python3 projects/shanhai-jing/scripts/tts_narration.py --slug jiu-wei-hu` |

## 2. Sentence-by-sentence table (every sentence has a job)

| # | Spoken line | Chars | What it does | What is checkable |
|---|-------------|-------|--------------|-------------------|
| 1 | 山海经里的九尾狐，和你印象里的不太一样。 | 20 | **Hook**: "what you remember is not what it says" | no source claim, pure setup |
| 2 | 原文是，有兽焉，其状如狐而九尾，其音如婴儿，能食人，食者不蛊。 | 31 | **Reads the source** (its shortest sentence) | character-for-character the first 22 characters of `text_ref.passage` in `manifest.json` |
| 3 | 翻成白话，有一种兽，长得像狐狸，却有九条尾巴。叫声像婴儿。它会吃人。 | 34 | **Plain-language translation**: nobody is left behind by classical Chinese | lands "其状如狐而九尾", "其音如婴儿", "能食人" one by one |
| 4 | 它没说这是妖，也没说是祥瑞。唯一的好处写在最后一句：吃了它的人，不会中蛊毒。 | 38 | **Corrects the myth + finishes the sentence** | "食者不蠱"; and it **never upgrades the text into an efficacy promise** — only "this is what it says" |
| 5 | 九个尾巴到底几条？我们用同一段原文试了两种写法：描述式六张只对一张；改成点名式，八张全对。 | 45 | **The project's spine**: countable, checkable | numbers come from [rounds/r05-review.en.md](../../rounds/r05-review.en.md) (descriptive 1/6, naming 8/8) |
| 6 | 这一期，是我们在青丘之山数出来的九尾狐。 | 20 | **Closes + signals the series** | "青丘之山" comes from the source itself |

> ⚠️ **The spoken script is simplified Chinese on purpose**: TTS reads rare source-edition forms
> (獸／狀／嬰／蠱) unreliably, and this audio is **commentary**, not "a version of the source text".
> **The page still shows the source-edition forms** (see `manifest.json`) — the two do not conflict; this is
> exactly "sourcing stays sourcing, explanation stays explanation".

## 3. Verification (not by feel)

| # | Check | Criterion |
|---|-------|-----------|
| 1 | Length | `ffprobe`: **expected = characters ÷ 4.4 ± 25 %**; too short means a segment was truncated |
| 2 | **Intelligibility** | Transcribe it back with offline ASR ([check_vocals.py](../../../../../../.agents/skills/comfyui-music-minimax3/scripts/check_vocals.py)): **recognised words ≥ 55 % of the script's character count** — narration **must** be recognised; this criterion points the **opposite way** from the music rule |
| 3 | No bleed between segments | 0.35 s of silence at each join; nothing swallowed |
| 4 | No truncation | the final word of the last segment is audible (ASR's last word matches the script's end) |

> Check 2 is this layer's **core criterion**: music must score **0 words** (instrumental), narration must score
> **high word coverage** (audible). Same tool, opposite directions — that is the practical boundary between
> "narration" and "music" in this pipeline.

## 4. BGM is only a bed

- Narration is the subject; `bgm/jiu-wei-hu-bgm.mp3` (guqin, template A) is only a **bed**:
  dropped **14 dB** (`--bgm-duck-db 14`) with sidechain ducking under the voice so it never fights the words.
- The site plays the **mixed** file (`audio/jiu-wei-hu-full.mp3`), so nobody has to balance two tracks.
- If a period has no BGM, the mixing step is skipped and the bare narration becomes the deliverable.

## 5. Revision history

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-07 | v0.1 | Created: a 6-segment, 188-character narration (hook → source → plain language → correction → counted proof → close); criteria are the **inverse** of the music's (**narration needs high word coverage**, music needs 0 words); BGM demoted to a bed | 小七 |
