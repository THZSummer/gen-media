# Long-Video Chain (Long-Video Chain)

> 🌐 Language: **English** | [中文](README.md)

> The topic of joining several short clips end to end into a coherent long film.
> Back to [method overview](../README.en.md) ｜ Core mechanism: `--return-last-frame` chained continuation

---

## 1. Topic positioning

A single clip's duration is limited (5 s by default, with a model ceiling of usually 5-10 s). To make long content of tens of seconds or even minutes, rely on **chaining**: use the last frame of one clip as the first frame of the next, generating segment by segment and joining them end to end to form a continuous long film.

### When chaining is needed

- One clip is not long enough to express the full narrative
- Multi-shot continuous narrative (together with [cinematography](../cinematography/README.en.md) storyboards)
- The camera keeps moving with the subject (follow shots, a long-take feel)

### When not to choose it

- 5 s is enough -> generate a single clip directly
- The shots are hard cuts (no continuity needed) -> generate each independently and edit them together in post

---

## 2. Chaining mechanism

```
Clip 1: --input @first1.jpg --return-last-frame "镜头向右摇"
         │
         └─► returns last_frame_url (clip 1's last frame)
                 │
                 ▼ download as clip 2's first frame
Clip 2: --input @first2.jpg(= clip 1's last frame) --return-last-frame "镜头继续推进"
         │
         └─► returns last_frame_url (clip 2's last frame)
                 │
                 ▼ ... chain continues
Clip N: ...
```

### Key flags

| flag | Purpose |
|------|------|
| `--return-last-frame` | Additionally returns the last frame's URL at generation time, for the next clip's first frame | 
| `--input @<末帧图>` | The next clip uses the last frame returned by the previous one as its first frame |

> ⚠️ **Measured update (2026-08-01)**: `doubao-seedance-2-0-260128` supports the `--return-last-frame` parameter but **currently returns no last_frame field in the +gen/gen get response** (measured with both `--wait` and `gen get`, neither had it) — not usable for now. Measured workaround: **extract the last frame from the video manually with ffmpeg** (`-sseof -0.1`) to use as the next clip's first frame.

### Keys to join quality

- The previous clip's last frame -> the next clip's first frame **must be identical**, otherwise the seam jumps
- Use the real last frame returned by `--return-last-frame`; **do not pick another image** as the first frame
- The last-frame URL is presigned too and **expires after 24 h**, so download it promptly
- ⛔ **mini models do not return last_frame_url** (--return-last-frame is ignored); switch chaining to the **two-stage I2V**: use seedream to generate the next shot's first-frame still, then I2V to make the video
- ⚠️ **Measured on seedance-2.0**: the parameter is supported but the response has no last_frame field (see the note above), so frames must be extracted manually with ffmpeg; moreover **video frames may trigger real-person privacy blocks** (`InputImageSensitiveContentDetected.PrivacyInformation`) — using a seedream storyboard image as the first frame avoids this

---

## 3. Chaining workflow

### Preparation: storyboard table

Design the storyboard before chaining (see the [cinematography](../cinematography/README.en.md) storyboard table template), making each segment's content, camera move, and transition explicit.

### Execution loop

```bash
VER=$(arkcli models get doubao-seedance-2-0 --transform 'primary_version' | tr -d '"')
MODEL="doubao-seedance-2-0-${VER:-260128}"

# Clip 1: start from the first frame, grab the last frame
arkcli +gen --model "$MODEL" --return-last-frame \
  --input @shot1_first.jpg --ratio 16:9 --resolution 720p \
  "镜头向右摇，展现街道" --wait --open
# -> note the returned last_frame_url, download it as shot2_first.jpg

# Clip 2: use clip 1's last frame as the first frame, grab the last frame again
arkcli +gen --model "$MODEL" --return-last-frame \
  --input @shot2_first.jpg --ratio 16:9 --resolution 720p \
  "镜头继续推进，主角走入画面" --wait --open
# -> download the last frame as shot3_first.jpg

# Clip N: and so on...
```

### Automation script approach

```bash
# pseudocode
first="shot1_first.jpg"
for i in 1 2 3 ...; do
  resp=$(arkcli +gen --model "$MODEL" --return-last-frame \
    --input @"$first" --wait --format json "<shot$i prompt>")
  last_url=$(echo "$resp" | jq -r '.last_frame_url')   # the field name follows the actual response
  first="shot$((i+1))_first.jpg"
  curl -o "$first" "$last_url"                          # download the last frame as the next clip's first frame
done
# finally concatenate the segment mp4s with ffmpeg
```

> The field names follow what `--format json` actually returns; write the downloaded last frame to disk **immediately**, as the URL expires after 24 h.

---

## 4. Parameter selection

| Parameter | Chaining recommendation | Notes |
|------|----------|------|
| `--return-last-frame` | Add to every clip (except the last) | Takes the last frame for the next clip |
| `--input` | The previous clip's last frame | The first frame must be identical |
| `--ratio` | Uniform across the whole chain | Otherwise the seam is cropped |
| `--resolution` | Uniform across the whole chain | Otherwise the image quality jumps |
| `--seed` | Fixed across the whole chain | Keeps the look consistent |
| `--wait` | Recommended | Chaining must run in order; waiting synchronously is less hassle |
| `--draft` | Use when debugging the chain | Remove it for the final render |

### Consistency is the lifeline of chaining

```
ratio + resolution + seed consistent across the whole chain  ──► smooth seam
any parameter change                          ──► seam jump / style break
```

---

## 5. Comparison of transition methods

| Method | Continuity | Implementation | Applies to |
|------|--------|------|------|
| **Last-frame chaining** | High (end to end) | `--return-last-frame` chain | Long takes, continuous narrative |
| Hard-cut concatenation | Low (independent shots) | Generate separately + edit in post | Fast-paced montages |
| Action continuity | Medium | Describe continuous action in the prompt + chaining | Follow shots, continuing motion |

- Chaining suits scenarios that **need visual continuity**
- For fast-paced montages with independent shots, a plain hard cut is more natural; do not force chaining

---

## 6. Post-production concatenation

Once the mp4 segments are generated, concatenate them with ffmpeg:

```bash
# 1) build the concat list
for f in shot1.mp4 shot2.mp4 shot3.mp4; do echo "file '$f'"; done > list.txt

# 2) lossless concatenation (requires identical codec/parameters — this is exactly why ratio/resolution are unified while chaining)
ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4

# 3) re-encode when the parameters differ
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -crf 18 out.mp4
```

> Keeping ratio/resolution/seed uniform across the chain is exactly what makes lossless `-c copy` concatenation possible.

---

## 7. Pitfalls

| Symptom | Cause | Fix |
|------|------|------|
| Seam jump | The last frame does not match the next clip's first frame | Use the real last frame from `--return-last-frame` |
| Look breaks | seed/resolution/ratio changed | Keep ratio/resolution/seed uniform across the chain |
| Last-frame URL expired | It was downloaded more than 24 h later | Download and save it immediately after generation |
| Chain interrupted | One clip failed | Retry just that segment; already-generated segments are unaffected |
| Concatenation error | The segments' encodings differ | Unify the parameters or re-encode when concatenating |
| Protagonist drift | The subject gradually changes across many chained clips | Use an I2V first frame to lock the subject on key segments |

---

## 8. Checklist

- [ ] List the storyboard table first, making each segment's content and transition explicit
- [ ] Keep `--ratio` `--resolution` `--seed` uniform across the chain
- [ ] Add `--return-last-frame` to every clip (except the last)
- [ ] Use the previous clip's real last frame as the next clip's first frame
- [ ] Download the last-frame URL to disk immediately (it expires after 24 h)
- [ ] Use `--wait` to run in order
- [ ] Keep the parameters uniform across segments so ffmpeg can concatenate losslessly
- [ ] Lock subject consistency with an I2V first frame

---

## Document revision history

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-07-18 | v1.0 | Initial topic plan | 小七 |
| 2026-07-18 | v1.1 | Noted that mini models do not return last_frame_url; chaining switched to the two-stage I2V approach | 小七 |
| 2026-08-01 | v1.2 | Measured that seedance-2.0 supports the parameter but the response has no last_frame field; added how to avoid real-person privacy blocks (seedream storyboard image as the first frame) | 小七 |
