# Wing · Atlas (wing-atlas) part table

> 🌐 Language: **English** | [中文](parts.md)

> Back to the [sub-theme home](README.en.md) ｜ [project home](../../README.en.md)

**Design**: treat "wings" as an **addable organ** and make an atlas of it —
**fix one bird (keeping its own wings) and add another creature's pair of wings on its back.**

Unified base = a medium-sized bird (keeping its own wings). **This volume is the only sub-theme in the whole project that "does not swap the base".**

---

## 1. Five kinds of "wing" and the tests

| # | Part | Donor wording | Semantic category | Result |
|---|------|----------|----------|------|
| 01 | **Baseline** | — (the base itself, three takes) | — | ✅ Baseline (the A/B control is itself) |
| 02 | Membranous wings | `translucent insect membranous wings` | **Is a wing** | ✅ **Fully holds** (5.00 ×2) |
| 03 | Leathery wings | `leathery bat wings` | **Is a wing** | ✅ **Fully holds** (5.00 ×2) |
| 04 | Flying-fish fin wings | `long gliding flying-fish fins` | **Carries the sense of "flight"** | ✅ **Fully holds** (5.00 ×2) |
| 05 | Crane feather wings | `long white crane wings` | **Is a wing** | ✅ **Fully holds** (5.00 ×2) |
| ❌ | ~~Fish pectoral fins~~ | `stiff fish pectoral fins` | Merely fins | ❌ **0%** (after ×1.7 zoom on the back area, only ordinary feathered wings) |
| ⚠️ | ~~Maple seed wings~~ | `dry maple seed wings` / `broad papery samara wings` | Merely seeds | ⚠️ Partial (they spread out and go pale, but there is no samara shape) |

## 2. Rule 107: **the donor's semantic category must match the function of the landing site**

Same landing site (the back), same sentence pattern (`a pair of … rising from its back`), same seed:

| Donor | Semantics | Result |
|------|------|------|
| Insect membranous wings | wings that fly | ✅ |
| Bat leathery wings | wings that fly | ✅ |
| **Flying fish** long fins | fins, but **carrying "flight" in themselves** | ✅ |
| Fish pectoral fins | fins, unrelated to flight | ❌ |
| Maple seed wings | plant seeds, unrelated to flight | ⚠️ |

> **A "wing-like shape" alone is not enough** (fish fins and samaras are wing-shaped too);
> **it must carry the semantics of "being able to fly"**. This is rule 85 (habitat semantic compatibility) at the **part–landing-site** level.

## 3. This volume's design focus: the **baseline period**

Part 1 **carries no transplant**, only three takes of the unified base:
it is both "the atlas's first page" and the **frame of reference** for the last four parts.
→ Atlas-type sub-themes (this volume and horn-atlas) both use this structure:
**part 1 = baseline, parts 2–5 = four candidate organs.**

## 4. Wording discipline

```
✅ a pair of translucent insect membranous wings rising from its back   ← 位置短语 + 空面
✅ a pair of long white crane wings rising from its back
❌ a pair of stiff fish pectoral fins rising from its back                ← 语义不匹配（Rule 107）
❌ 把鸟自己的翅换掉（原计划）                                              ← 同材质替换（Rule 67）
```

---

## Revision history

| Date | Version | Change | Author |
|------|------|------|------|
| 2026-10-05 | v0.1 | Wing atlas part table (five kinds of wings) + **rule 107 (the semantic category must match the landing site's function)** | 小七 |
