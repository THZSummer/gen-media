# Kunpeng Part Table (Fish + Bird)

> 🌐 Language: **English** | [中文](parts.md)

> Back to [sub-theme home](README.en.md) ｜ [project home](../../README.en.md)

**Design source**: 《Zhuangzi · Xiaoyaoyou》 "in the Northern Sea there is a fish… it transforms into a bird" — a **form transformation** explicitly stated in the classics.
So the hook of this sub-theme is not "add one part" but **a single transformation**.

**Base = big fish (carp)**; donors = the bird's **flight parts**: wings B1 / tail feathers B2 / plumage B5.
~~Beak B3 / claws B4~~: the beak is a head part (Rule 73), and a fish has no limbs (Rule 74).

---

## 1. Part table and measurements

| ID | Part | prompt anchor | Underwater scene | **Out-of-water scene** |
|------|------|-------------|----------|--------------|
| B1 | Bird wings | `broad feathered bird wings on both sides of its body` / `…spread wide from its back` | ❌ **0%** (three wordings written, none worked) | ✅ **Fully holds** (5 independent reproductions, 5.00) |
| B2 | Bird tail feathers | `a fan of long bird tail feathers` | ❌ 0% | ❌ 0% (the tail position is the fish's **canonical structure**, Rule 87) |
| B5 | Plumage over the back | `a covering of fine bird feathers over its back` | ❌ 0% | ❌ 0% (same-material replacement, Rule 67, tier 3) |

**The only usable part is B1 bird wings**, and whether it works is **entirely decided by the scene**.

## 2. Core finding: habitat is a hard constraint (Rules 85/86)

Same base, same sentence, same seed — **only the scene moves from underwater to above the water surface**:

| Scene | Result |
|------|------|
| `in shallow clear water over pale gravel` (underwater) | ❌ not a single wing appeared (all three wordings wiped out) |
| `in open air above the water surface, spray falling away below it` (out of water) | ✅ wings appear **immediately** |

> **Rule 85: when a transplanted part conflicts semantically with the habitat, the model keeps the scene and drops the part.**
> "Feathers / wings underwater" is a semantic contradiction — the model would rather turn the transplant sentence into a no-op than paint a fish with wings underwater.
>
> **Rule 86: scene compatibility is judged region by region.**
> In period 02 "half out of water", `fish-wings` (the wing written on the flank) **is eaten by the scene**,
> while `fish-wings-half` (a half-open wing positioned high, landing on the side above the water) **lands**.
> → Within one image, the exposed part can grow a piece; the part soaking in water cannot.

## 3. Canonical structures cannot free a placeholder (Rule 87)

Fish fins were once treated as a "freeable placeholder" (the optimistic tier of Rules 66/83), **but measurement says otherwise**:

| Practice | Result |
|------|------|
| The base does not describe the paired fins (freeing the pectoral-fin position for B1) | 0% underwater; out of water the wings land, but **the fish grows its own fins back** |
| The base does not describe the caudal fin (freeing the tail position for B2) | 0% (tail feathers land in no scene) |

> **Rule 87: canonical structures cannot free a placeholder.** Fish fins, cat paws and snake scales are the structures that make an animal what it is;
> deleting them from the description still gets them restored by the model's species prior.
> This forms a control against the turtle's neck / tail (deleting those does not hurt the base, so freeing them works).

## 4. Wording discipline for transplanted parts

```
✅ a pair of broad feathered bird wings spread wide from its back   ← 部位短语 + 空位
✅ a pair of broad feathered bird wings half-opened along its flanks ← 位置偏上（露在水面之上）
❌ broad feathered bird wings in place of its pectoral fins          ← 关系从句（规律 81）
❌ a bird's wings                                                    ← 整只（规律 57）
```

And **the scene must be compatible first**: ask "does this part make sense in this habitat" before asking about wording and placeholders (Rule 85).

---

## Revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Kunpeng part table B1/B2/B5 + three measured rules (85 habitat hard constraint / 86 region-by-region judgement / 87 canonical structures cannot be freed) | 小七 |
