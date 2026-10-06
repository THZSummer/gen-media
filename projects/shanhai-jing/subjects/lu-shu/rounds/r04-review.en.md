# Score review · R4 (lu-shu 鹿蜀 · cross-engine comparison: Z-Image-Turbo vs Seedream 5.0 Pro)

> 🌐 Language: **English** | [中文](r04-review.md)

> Nature of this round: **hand the same prompt to a remote paid model and measure two things** — ① how often the
> four traits (horse body / white head / tiger markings / red tail) land, ② whether it also stamps fake seals into
> the paper margins. **All six images in this round are billed.**
> Engine: the `seedream-text-to-image` skill → ComfyUI partner node `ByteDanceSeedreamNodeV3` (seedream 5.0 pro)
> Canvas: 1024×1360 (Custom, the same canvas as the Z-Image main rounds) | seeds: 101 / 202 / 303 | steps: n/a (remote model)
> Round archive: `work/shanhai-jing/lu-shu/r04/` (`round-r04-seedream.json` + the engine's own `requests.jsonl`)

---

## 1. How it was run, and what it cost

```bash
python3 scripts/run_round.py --subject lu-shu 4 --engine seedream \
  --api-key-file ../../work/comfy_api_key --sheet
```

| Item | Value |
|------|-------|
| Images | 6 (2 variants × 3 seeds) |
| Variants | x1 = the R1 v1 wording (the sentence behind the first-choice final) | x2 = the R2 v5 wording (traits first, red confined to the tail) |
| Measured duration | first image 19:06:39 → last image 19:12:17, **5 min 38 s** in total (≈56 s per image, queueing and download included) |
| Canvas | 1024×1360 (`--size Custom`; the saved PNGs measure the same) |
| Billing | ComfyUI account credits, **billed per image**; this repository has no billing integration, so the unit price is unmeasured |
| Credential | `extra_data.api_key_comfy_org`; the ledger records only channel and source, never the secret (asserted by test) |

---

## 2. Side-by-side results

| Item | Z-Image-Turbo (R1 first choice v1-101) | Seedream 5.0 Pro (the six R4 images) |
|------|----------------------------------------|--------------------------------------|
| Horse body / white head | ✅ / ✅ | ✅ / ✅ (6/6) |
| Tiger markings | ✅ soft (fine grey-black stripes) | ✅✅ **bold** (all 6 paint heavy black tiger stripes; the x2 group especially tiger-like) |
| Red tail | ✅ | ✅ (6/6, but 4/6 also paint the **mane** red) |
| Background / composition | single subject on a rocky ledge, generous empty space | distant mountains, mist, moon, pines — **the frame fills up**, beyond the "album leaf, negative space" brushwork |
| **Inscription and seals** | 1/9 clean (the first choice's four corners verified seal-free at 4× zoom) | **6/6 carry inscription and seals**: vertical Chinese characters (some real, e.g. 「鹿蜀」 「南山經」, the rest pseudo-characters) plus name and leisure seals |
| Verdict | ✅ usable (A=4, F=5) | ⛔ **6/6 disqualified**: model-written Chinese characters are a hard defect in this project |

**Image by image** (`work/shanhai-jing/lu-shu/r04/sheet-r04.jpg`):

| Shot | Traits | Inscription / seals | Note |
|------|--------|---------------------|------|
| x1-101 | all four | inscription top-right + name seal, leisure seal bottom-left | also added a red mane |
| x1-202 | all four | inscription top-right + name seal | the cleanest white head |
| x1-303 | all four | two-line inscription top-right + two seals | heaviest distant mountains, fullest frame |
| x2-101 | all four, **boldest tiger markings** | inscription top-left + seal | red mane + red tail |
| x2-202 | all four | large 「南山經」 top-left + vermilion seal | the most convincing "real" characters |
| x2-303 | all four | inscription top-right + seal | red mane + red tail; composition close to x1 |

---

## 3. Conclusions

1. **No engine switch.** Seedream renders the three shape traits more strongly (tiger markings above all), but it
   **reliably** writes characters and stamps seals inside the picture (6/6), and "characters are never written by
   the model" is this project's first iron rule. That rule is not for sale: once it is, "verifiable scholarship"
   and "an inscription the model invented" end up in the same image and the whole claim collapses.
2. **Its value is proving that bold tiger markings are reachable**: the R2 v5 direction (traits first, red
   confined) is right, Z-Image merely draws it softly; a future round can add `bold` / `clearly marked` to that
   sentence and retry.
3. **If Seedream is ever adopted**, the precondition is solving the inscription problem first: rewrite the style
   wording (to break the Chinese-painting inscription prior), crop the inscription area away, or erase it with
   `scripts/patch_region.py` (the tool now self-checks). None of the three is verified, so nothing is promised
   this period.
4. **Cost scale**: about 56 s per image, billed per image; these six were a comparison budget the user explicitly
   approved and do not become a routine round.

---

## 4. Scores (A–F, weights in [PLAN.md](../../../PLAN.en.md) §5)

| Work | A research | F spirit | B brushwork | C format | D legibility | E consistency | Total | Verdict |
|------|-----------|----------|-------------|----------|--------------|---------------|-------|---------|
| R4 x2-101 (strongest traits) | 5 | 5 | 3 | 2 | 5 | 2 | 3.95 | ⛔ hard defect: model inscription and seals |
| R4 x1-202 (cleanest) | 5 | 4 | 3 | 2 | 5 | 2 | 3.80 | ⛔ same |
| (reference) R1 v1-101 Z-Image | 4 | 5 | 5 | 4 | 5 | 5 | 4.60 | ✅ this period's first choice |

> **Why B/C/E score low**: Seedream paints "a complete Chinese painting" (distant scenery + inscription + seals),
> which is **inconsistent** with the already-shipped jiu-wei-hu pieces (single subject, generous empty space, no
> inscription). The brushwork is still coloured gongbi, but a full frame with an inscription is not this project's
> album-leaf format.

---

## 5. Takeaways

1. **Both models "complete the object into a collectible"**: Z-Image adds seals (faintly), Seedream adds seals
   **and an inscription** (conspicuously). In the training data a Chinese painting *is* picture + inscription +
   seal; what the model learned is the whole object, not "just the picture".
2. **Paying does not buy control**: the traits are stronger, but what the project needs is not the strongest traits
   — it is "correct traits **and** no model-written characters", and the paid model is worse at the latter.
3. **The cross-engine comparison was worth running**: it answers "did we pick the wrong engine" once and for all,
   and it incidentally produced reference images of what bold tiger markings look like, for six images.

---

## 6. Open items

| Item | Status |
|------|--------|
| Seedream's inscription problem | ⏳ unsolved (rewording / cropping / tool erasure all unverified) |
| Z-Image tiger-marking strength | ⏳ next round to try `bold` / `clearly marked` phrasing |
| Credential handling | `work/comfy_api_key` (gitignored, 0600); the ledger and the test suite both assert no plaintext |
