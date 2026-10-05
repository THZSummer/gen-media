# Period 1 · The flower of plume branches

> 🌐 Language: **English** | [中文](README.md)

> Back to the [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [scoring review report](../rounds/fb2-r5-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Source: [`manifest.json`](manifest.json)

---

## 1. Features of this period (presentation)

**Morning dew · soft light · macro 100mm · square**

## 2. Theme and results of this period

**Base ＝ large flower**　**Donor ＝ P6 plume feather (flower axis)**

See the landing-site analysis in [parts.md](../parts.en.md): P6 lands on the **flower axis** (a surface, no bearing structure needed),
P5 lands on the **flower centre** (a half-empty face once the stamens and pistil are vacated).

## 3. Finals

Score **5.00×3** (all ✅ first choice). See [`manifest.json`](manifest.json) for details:
each image records its source round, camera name, seed, verbatim prompt and sha256.

Control: [`controls/flower.png`](controls/flower.png) —— the **same-round** pure-flower base.

## 4. Reproduce

```bash
cd ../../..
python3 run_round.py --subject flower-bird r5 --dry
python3 run_round.py --subject flower-bird r5
python3 score.py --round work/flower-bird/rr5/round.json --scores work/flower-bird/rr5/scores.json \
    --control base-flower --audit-sheet subjects/flower-bird/rounds/fb2-r5-audit.jpg \
    --subject flower-bird -o subjects/flower-bird/rounds/fb2-r5-review.md
bash make_sheet.sh period subjects/flower-bird/period-01
```

---

## Document revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 1 delivered | 小七 |
