# Nine-Tailed Fox R9 · Seal suppression by rewriting the prior

> 🌐 Language: **English** | [中文](r09-review.md)

> Back to the [project entry](../../../README.en.md) ｜ wording and seal rules: [PLAN.en.md](../../../PLAN.en.md) §3/§5 ｜ the same experiment on the horse: [lu-shu r05-review](../../lu-shu/rounds/r05-review.en.md)

## 1. Why this round ran

Lu-shu R3 had already falsified the **negative** route for seal suppression
(`no seal / no stamp / no writing`, all 9 images failed), and under this bone method the seal hit rate is
very high — **even this subject's shipped R7 final has faint red seals in its corners**. So the hypothesis
changed: **the seal comes from the "mounted old painting" prior**; instead of negating it, **rewrite the prior**.

The four bone sentences are **byte-identical** to [lu-shu R5](../../lu-shu/rounds/r05-review.en.md)
(the same experiment run on both subjects):

| Variant | The clause that changes | Hypothesis |
|---------|------------------------|------------|
| **s1** | nothing (current bone sentence, verbatim) | **same-round control** |
| **s2** | `album leaf` → `a single unmounted sheet of xuan paper` | seals belong to the mounted album-leaf form |
| **s3** | the scene fills the sheet with no empty margins | a seal needs blank paper to sit in |
| **s4** | `aged paper` → `plain white paper` | seals belong to the old-painting prior |

The subject clause (`The nine-tailed fox ... nine long tails spread out behind it...`, R7's final sentence)
is byte-identical across all four.

## 2. Generation

12 images = 4 variants × 3 seeds (1811 / 1922 / 2033), Z-Image-Turbo, 1024×1360 / 20 steps, **free and local**,
about 60 s each. Verbatim prompts are in [`rounds.py` R9](../rounds.py); outputs and `requests.jsonl` land in
`work/shanhai-jing/jiu-wei-hu/r09/` (**not committed**).

**Tail count**: all 12 read as nine tails (fan spread with gaps between the plumes), consistent with R7/R8's
name-the-creature result (8/8 and 4/4).

## 3. Seal census (mechanical screen + 6× visual inspection of the corners)

| Output | Mechanical screen | What the corners actually show | Verdict |
|--------|-------------------|-------------------------------|---------|
| s1-1811 (control) | 2 candidates | both right corners | sealed |
| s1-1922 (control) | 8 candidates | both right corners + mid-left | sealed |
| s1-2033 (control) | 7 candidates | a cluster in the bottom right | sealed |
| s2-1811 | 5 candidates | both right corners | sealed |
| s2-1922 | 15 candidates | both right corners + mid-left | sealed |
| s2-2033 | 2 candidates | **one clear red seal in TR** (plus a faint one in BR) | sealed |
| s3-1811 | **0 (CLEAN)** | **one clear red seal in BR** | sealed (screen missed it) |
| s3-1922 | 2 candidates | two spots mid-left | sealed |
| s3-2033 | 8 candidates | both right corners | sealed |
| s4-1811 | 1 candidate | one spot mid-left | sealed |
| s4-1922 | **0 (CLEAN)** | **one clear red seal in BL** | sealed (screen missed it) |
| s4-2033 | 6 candidates | both right corners | sealed |

> **Finding 1: 12/12 sealed — all four rewordings failed.** Together with lu-shu R5 this means
> **both "suppress the seal with the prompt" routes are falsified**: negation (9 images) and rewriting the
> prior (24 images).
>
> **Finding 2: the mechanical screen's `CLEAN` verdict is not trustworthy** (the fox adds two more cases:
> s3-1811 and s4-1922 were both called CLEAN yet each carries a **clear** red seal). The fox also produces
> far more false positives — the orange tail fur is itself a big patch of "cinnabar". `seal_check.py` can
> **raise suspicion**, never give **clearance**.

## 4. Scoring and the trade-off: why we do **not** switch

R9's tails are much stronger and the nine tails read more clearly than R7's, but on the same rubric
(A–F, weights in [PLAN.en.md](../../../PLAN.en.md) §5):

| Dimension (weight) | Shipped final R7 m202 | Best R9 candidate s2-1811 |
|---|---|---|
| A textual accuracy (.25) | 4.5 (pale tails, counting takes effort) | **5** (clear fan, distinct plumes) |
| F spirit and life (.25) | **5** (refined, breathing white space) | 4.5 (fur a bit cottony, heavier ink) |
| B bone-method purity (.15) | **5** | 4.5 |
| C format completeness (.15) | 4.5 | 4.5 |
| D recognisability (.10) | 5 | 5 |
| E series consistency (.10) | **5** (same hand as the lu-shu final) | 4 (heavier tails and paper tone, a different register) |
| **Weighted total** | **4.80** | **4.63** |

> **Switching would be a downgrade** (and lu-shu did not switch either this round: its bold-stripe candidate
> scored 4.38 against a 4.60 final). Read together, the conclusion is the same: **"stronger" carries a
> series-consistency bill**; either darken the bone method for the whole series or leave it alone.

**The final is unchanged**: the plate remains R7 m202. But its **faint seals have been erased** (below).

## 5. Fixing the seal defect: two faint seals on the R7 final

The R7 final has one **extremely faint** model seal in each of the BL and BR corners (visible at 4×;
`seal_check.py`'s band thresholds missed them, a false negative). Following the existing rule in PLAN §5 it
was erased with `scripts/patch_region.py`:

| Item | Value |
|---|---|
| Patch boxes | BL `(0,1266,66,94)`, BR `(950,1284,74,76)`, feather 12 |
| Self-checks | residual cinnabar 22→0 and 60→0; seam luma delta 2.0 (threshold ≤30) |
| **Pixel proof** | against `controls/jiu-wei-hu-r7-m202-seal-tainted.png`: **7024 px differ, all inside the two boxes (0 px outside)** |
| Visual re-check | corners at 12% / 6×: BL and BR now clean; the bottom band re-checked at 4× with no residue |
| Typesetting | `typeset_zanzhi.py` re-run (5 layout self-checks pass); the new card differs from the old one only in a 55×57 px area where the patch lands |

> The un-erased final is kept as `controls/jiu-wei-hu-r7-m202-seal-tainted.png` so this erasure can be reproduced.

## 6. Takeaways

1. The seal is a **strong prior** of this bone method: stable locations (both right corners and the bottom
   margin) and immune to wording (negation + prior rewriting, 33 images in total, all failed).
2. **The mechanical screen can raise suspicion but never give clearance** — all five images it called CLEAN
   (3 lu-shu + 2 fox) carry seals to the eye.
3. "Stronger tails" and "bolder tiger stripes" share a cause: they push ink and contrast up, and the price
   is series consistency (E). A future subject that wants stronger should darken the whole bone sentence and
   **re-run both subjects in the same round**.
4. What still guarantees cleanliness: **corners at 12% / 6× visual inspection** (`scripts/corner_sheet.py`
   with a fixed layout and self-checks) plus `scripts/patch_region.py` erasure (self-checks + pixel proof).

## 7. Open items

| Item | Status |
|------|--------|
| s2's medium clause × R7's **pale-tail** subject clause | ⏳ Untested (all four variants kept R7's subject clause, so that variable is not confounded; but the "pale tails + new medium clause" combination was not tried) |
| Real seal layer in seal script | ⛔ Still missing (font unresolved) |
| Guo Pu's commentary | ⏳ To be transcribed (no commentary may appear in deliverables before then) |
