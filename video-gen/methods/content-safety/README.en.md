# Content Safety and Moderation (Content Safety)

> 🌐 Language: **English** | [中文](README.md)

> A cross-cutting topic on handling video generation moderation blocks and keeping output stable; applies to every input path.
> Back to [method overview](../README.en.md)

---

## 1. Topic positioning

Video generation goes through content safety moderation. When a prompt or reference material hits sensitive content, the task is blocked (`ContentRiskBlocked` / `*SensitiveContentDetected`, etc.). **`--force` does not get around content moderation** — it only skips parameter validation, not the safety policy. This topic covers how to avoid blocks at the source and how to adjust after one.

### Applicable scenarios

- Generation is blocked by moderation and you need to find out why
- Proactively avoiding sensitive words when writing prompts
- Compliance checking of reference materials
- You need stable batch output and a lower block rate

---

## 2. What a moderation block looks like

### Common error codes / statuses

| Error | Meaning |
|------|------|
| `ContentRiskBlocked` | Content risk block |
| `*SensitiveContentDetected` | Sensitive content detected |
| Sensitive word / copyright hit | The prompt or material contains sensitive/copyrighted content |

### Key facts to internalise

- **`--force` does not work**: `--force` only skips **parameter validation** (letting unsupported parameters pass through); it does **not** skip the content safety policy
- The block happens server-side; the client cannot bypass it
- A blocked task produces no video but may already count towards part of the cost (actual billing prevails)

---

## 3. Main categories of sensitive content

| Category | Typical | Avoidance |
|------|------|------|
| Violence/gore | Fighting, wounds, close-ups of weapons | Soften the description, use symbols/metaphors |
| Pornography/exposure | Over-exposure, sexual suggestion | Adjust the clothing and the composition |
| Politically sensitive | Political figures, political symbols, flags | Avoid concrete political elements |
| Real people | The likeness of stars or public figures | Describe a fictional character instead |
| Copyrighted content | Well-known IP characters, brand logos | Replace with generic descriptions |
| Illegal activity | Drugs, the process of a crime | Remove the related description |
| Terror/extremism | Terrorism, extreme scenes | Avoid the related elements |
| Safety-trial quota | Triggers SetLimitExceeded and the model service is suspended | Turn off "safety trial mode" in console model management, or raise the quota |

---

## 4. Prompt avoidance strategy

### Principle: describe positively, avoid negation

Models are **weak at negations** ("do not show blood" may in fact reinforce the concept of blood). Use positive substitute descriptions instead:

| Bad (negative/sensitive) | Good (positive substitute) |
|----------------|----------------|
| "no gore" | "crisp action, a close-up of a resolute expression" |
| "not a real celebrity" | "a fictional young female character" |
| "no weapons" | "hands hanging naturally at the sides" |

### Specify rather than name

- Avoid naming real people/IP -> describe a fictional character by appearance
- Avoid brand logos -> use "a smartphone" rather than a specific brand
- Avoid concrete political symbols -> use generic scene elements

### Softening the sensitive intensity

- Violence -> symbolic action ("confrontation", "staring" rather than "fighting and bleeding")
- Danger -> metaphor ("a storm is coming" rather than a concrete disaster)
- Dilute it with stylisation (animation/watercolour styles pass review more easily than photorealism)

---

## 5. Reference material compliance

The **input materials** of I2V / R2V / audio-driven are moderated too:

| Material type | Checkpoint |
|----------|--------|
| First-frame image | Whether the image content contains sensitive elements |
| Reference video | Whether the video footage is compliant |
| Reference audio | Whether the audio content/lyrics are sensitive |

### Self-checking materials

- Image: does it contain real faces, brand logos, violent/exposing elements
- Video: is the footage compliant, does it contain copyrighted content
- Audio: are the lyrics/speech sensitive

> When the material is non-compliant, changing the prompt is useless; you must **change the material**.

---

## 6. Workflow after a block

```
Task blocked (ContentRiskBlocked)
   │
   ▼ 1. Locate the source
   │   ├─ prompt sensitive?    -> change the prompt (positive substitute / soften)
   │   ├─ input material sensitive?   -> change the material
   │   └─ unsure?         -> eliminate one by one (drop the material and try pure T2V first)
   │
   ▼ 2. Retry after adjusting
   │   change one thing and test once, to locate the exact sensitive point
   │
   ▼ 3. Still blocked?
       ├─ soften the description further
       ├─ change the style (photoreal -> animation/watercolour)
       └─ diagnose with doctor
```

### Diagnosing a block with doctor

For a structured block reason + fix guidance, use `arkcli doctor error <code>`:

```bash
arkcli doctor error ContentRiskBlocked
```

doctor fully covers the 5 subtypes of video-generation blocks and gives the concrete subtype and repair suggestions. See the arkcli-doctor skill for details.

---

## 7. Strategies for stable batch output

In batch generation a high block rate wastes money. Preventive measures:

| Strategy | Notes |
|------|------|
| Pre-review the prompt template | Try a single clip before the batch; confirm the prompt passes review before batching |
| Uniformly compliant materials | Run every material through the self-check before batching |
| Use a safe style consistently | Photorealism carries more risk than animation/watercolour; prefer safe styles for batches |
| Isolate failed tasks | One failure does not affect the batch; log the failures and retry them separately |
| Test with draft first | `--draft` is cheap: batch-test the pass rate first, then run for real |

---

## 8. Command templates

```bash
# 1) diagnose after a block
arkcli doctor error ContentRiskBlocked

# 2) eliminate one by one (drop the material and try pure T2V, to see whether it is a prompt problem)
arkcli +gen --model "$MODEL" "<只保留 prompt，去掉 --input>" --open

# 3) soften with a safe style
arkcli +gen --model "$MODEL" \
  "水彩画风格，一位虚构旅人在山间行走，宁静氛围" --open

# 4) before batching, use draft to test the pass rate
arkcli +gen --model "$FAST" --draft --resolution 480p \
  "<批量 prompt 模板>" --open
```

---

## 9. Pitfalls

| Symptom | Cause | Fix |
|------|------|------|
| Still blocked with `--force` | force does not skip content moderation | Fix it at the source: prompt/materials |
| Still blocked after changing the prompt | The material is non-compliant | Change the material, not the prompt |
| Negative descriptions do not work | Models are weak at negation | Use positive substitute descriptions |
| Many blocks in a batch | Prompt/materials were not pre-reviewed | Try a single clip + a draft pass-rate test before batching |
| Real-person likeness blocked | A real person was named | Describe the appearance of a fictional character |
| Not knowing what violated the rules | Multiple sources are hard to isolate | Eliminate one by one (drop the materials and try pure T2V) |

---

## 10. Checklist

- [ ] The prompt uses positive descriptions and avoids negations
- [ ] Do not name real people/IP/brands; describe features instead
- [ ] Input materials have been self-checked (image/video/audio)
- [ ] Sensitive elements have been softened or stylised
- [ ] Before a batch, try a single clip + a draft pass-rate test
- [ ] After a block, diagnose with `arkcli doctor error`
- [ ] Eliminate one by one to locate the source (prompt vs material)
- [ ] Do not rely on `--force` to bypass moderation

---

## Document revision history

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-07-18 | v1.0 | Initial topic plan | 小七 |
| 2026-07-18 | v1.1 | Added the SetLimitExceeded (safety-trial quota) entry | 小七 |
