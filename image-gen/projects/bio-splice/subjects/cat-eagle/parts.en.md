# Part List and Combination Plan

> 🌐 Language: **English** | [中文](parts.md)

> Back to the [sub-theme home page](README.en.md) ｜ [project home page](../../README.en.md)
> This is the sub-theme's **design source**: the periods were not thrown together round by round, but picked as combinations from one part table.

---

## 1. Why Split into Parts

The diagnosis from R2–R5 is: **a named animal renders as a whole** (the head slot → only one head; the body slot → a whole animal,
its own head included). So as soon as "a cat / an eagle" appears in the sentence, the model fills in that species'
whole plan rather than taking only a part of it.

**Splitting into parts neatly avoids this**: `a cat's ears`, `an eagle's wings` are **local parts** with no "whole plan" to complete.
Period 01 worked (cat head + eagle body) for the same reason—the head slot renders only one head.

## 2. Part List

### cat (**weak species**: a generic body plan—quadruped + fur, low recognizability)

| No. | Part | English anchor (the phrasing used in the prompt) |
|------|------|------------------------------|
| C1 | cat ears | `a domestic cat's triangular tufted ears` |
| C2 | cat head | `a domestic cat's short muzzle, whiskers, slit-pupil eyes` |
| C3 | cat body (torso + fur) | `dense striped tabby fur, a furry torso` |
| C4 | cat limbs and paws | `four furry legs with soft paw pads` |
| C5 | cat tail | `a long ringed tabby tail` |
| C6 | cat whiskers | `long whiskers` |

### eagle (**strong species**: a recognizable body plan—wings / talons / feathers appear as a whole the moment they are mentioned)

| No. | Part | English anchor |
|------|------|----------|
| E1 | eagle head (incl. beak) | `a hooked yellow beak, a dark brown feathered crown, a piercing amber eye` |
| E2 | eagle wings | `broad folded feathered wings` |
| E3 | eagle body (torso) | `a dark brown feathered body` |
| E4 | eagle legs and talons | `scaled yellow legs with black talons` |
| E5 | eagle tail feathers | `a fan of dark brown tail feathers` |
| E6 | eagle neck ruff / crest | `a feathered neck ruff` |

## 3. Mechanism Predictions for the Combinations

Once the parts are split out, the combinations are no longer only "head × body" but "base + several parts". The base decides the whole, and the parts are local modifications.
Given the mechanisms pinpointed so far, one can predict which kinds of combination work easily:

| Combination type | Prediction | Basis |
|----------|------|------|
| **strong base + a small piece of a weak species** (eagle + cat ears/tail/paws) | ✅ easy, but **with a precondition** | measured: cat ears ✅ cat tail ✅, **cat paws ❌**. The precondition = the base description **has no placeholder** for that part (the eagle does not mention ears and tail, but explicitly writes talons) |
| **weak base + a local piece of a strong species** (cat + eagle wings/tail feathers) | ✅ **works** (the original prediction was too conservative) | measured: all three images succeeded. `eagle wings` is a **part modifier** and does not trigger "whole completion" |
| **weak base + the head of a strong species** (cat body + eagle head) | ❌ impossible | already proven by the four rounds R2–R5 (two heads, or regression to a pure eagle); needs Qwen negatives / ControlNet |
| **stacking multiple parts** | ⚠️ **depends on whether regions conflict** | measured: three cross-region parts (neck + tail + back) ✅ work; two stacked in the same region (ears + whiskers) ✅ also work; **two in the same region plus a third across regions → ❌ the model draws another individual to fill the order** |

## 4. Period Plan

Each period = the finals of one group of **selected parts**, **finals only** (see [project discipline](../../README.en.md)).

| Period | Theme | Base | Transplant part | Count | Status |
|----|------|------|----------|------|------|
| [period-01](period-01/README.en.md) | **Owl** (literal translation of the word) | eagle | C2 cat head | 3 finals + 2 controls | ✅ delivered |
| [period-02](period-02/README.en.md) | **Eagle with beast ears and beast tail** | eagle | C1 cat ears · C5 cat tail | 3 | ✅ delivered (C4 cat paws failed and were excluded) |
| [period-03](period-03/README.en.md) | **Winged cat** | cat | E2 eagle wings · E5 eagle tail feathers | 3 | ✅ delivered |
| [period-04](period-04/README.en.md) | **Whiskered eagle** | eagle | C6 cat whiskers (+ C1 cat ears) | 2 | ✅ delivered (the three-part version was excluded for summoning a second individual) |
| [period-05](period-05/README.en.md) | **Thrice eagle-ized cat** | cat | E6 neck ruff · E5 tail feathers · E2 eagle wings | 3 | ✅ delivered |
| ~~period-06~~ | ~~**eagle-headed cat** (reverse splice)~~ | cat | E1 eagle head | — | ⛔ **judged infeasible** (rule 73: a head swap is a two-way dead end; D2 camel head/D3 rabbit eyes reproduced it independently) |

> The period order = from easy to hard: first a strong base + a small piece (02), then a weak base + a strong local piece (03), then multiple parts (04/05).
>
> **Head parts (C2 cat head / E1 eagle head) appear only in period 01**, and in the **reverse** usage (the head slot renders only one head,
> so "cat head + eagle body" works). **Swapping a head on properly (eagle head + cat body) is a dead end in both rounds** and is no longer a period target.

---

## Document Revision History

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Part list (cat C1–C6 / eagle E1–E6) + combination mechanism predictions + period plan (02–05) | 小七 |
| 2026-10-04 | v0.2 | All five periods present; period-06 eagle-headed cat judged infeasible (rule 73); periods 02–05 given their own presentations | 小七 |
