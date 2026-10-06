# Lu-Shu R5 · Seal-suppression by rewording the prior

> 🌐 Language: **English** | [中文](r05-review.md)

> Back to the [project entry](../../../README.en.md) ｜ wording and seal rules: [PLAN.en.md](../../../PLAN.en.md) §3/§5 ｜ previous round: [r04-review](r04-review.en.md) (cross-engine comparison)

## 1. Why change the approach

R3 had already falsified the **negative** route: `no seal / no stamp / no writing` — all **9 images failed**.
Under this bone method (ochre colour, album leaf, aged paper) the seal hit rate is very high:
R1 8/9, R2 English group 6/6, and **even the shipped nine-tailed fox R7 final has faint red seals in its corners**.

So the hypothesis changed: **the seal is not something "the model wants to stamp" — it comes from the
"mounted old painting" prior**. Instead of negating it, **rewrite the prior itself**, changing one variable at a time:

| Variant | The clause that changes | Hypothesis |
|---------|------------------------|------------|
| **s1** | nothing (the current bone sentence, verbatim) | **same-round control**: measures seed variance and the seal baseline |
| **s2** | medium noun: `album leaf` → `a single unmounted sheet of xuan paper` | seals belong to the *mounted album leaf* form |
| **s3** | layout: the scene fills the sheet with no empty margins | a seal needs blank space to sit in |
| **s4** | paper age: `aged paper` → `plain white paper` | seals belong to the *old painting* temporal prior |

The subject clause (`...bold black tiger stripes... only its long tail is cinnabar red...`, R2's final v5)
stays **byte-identical** across all four; the four bone sentences are **byte-identical** to the fox's
[R9](../../jiu-wei-hu/rounds/r09-review.en.md) — the same experiment is run on both subjects so the conclusions cross-check.

## 2. Generation

12 images = 4 variants × 3 seeds (1811 / 1922 / 2033), Z-Image-Turbo, 1024×1360 / 20 steps, **free and local**.
Verbatim prompts are in [`rounds.py` R5](../rounds.py); outputs and `requests.jsonl` land in
`work/shanhai-jing/lu-shu/r05/` (**not committed**). About 59 s per image.

## 3. Seal census (mechanical screen + 6× visual inspection of the corners)

The criterion follows PLAN §5: `seal_check.py` only **screens candidates**; the verdict is always
**visual at magnification** (corners cropped at 12% of the short side, 6× nearest-neighbour, rendered by
`scripts/corner_sheet.py`, archived per image).

| Output | Mechanical screen | What the corners actually show | Verdict |
|--------|-------------------|-------------------------------|---------|
| s1-1811 (control) | 1 candidate | one red seal (BR) | sealed |
| s1-1922 (control) | 1 candidate | one seal each in BL and BR | sealed |
| s1-2033 (control) | 5 candidates | both right corners | sealed |
| s2-1811 | **0 (CLEAN)** | **one clear red seal in TR and one in BR** | sealed (screen missed it) |
| s2-1922 | **0 (CLEAN)** | **one clear red seal in TR** | sealed (screen missed it) |
| s2-2033 | 1 candidate | one in BR | sealed |
| s3-1811 | **0 (CLEAN)** | one in BL and two in BR | sealed (screen missed it) |
| s3-1922 | 1 candidate | one in BL | sealed |
| s3-2033 | 5 candidates | several in the bottom-right corner | sealed |
| s4-1811 | 2 candidates | one extremely faint in BL, one in BR | sealed |
| s4-1922 | 2 candidates | one each in BL and BR | sealed |
| s4-2033 | 3 candidates | two in BR | sealed |

> **Finding 1 (the main result of this round): 12/12 sealed — all four rewordings failed.**
> In other words **both "suppress the seal with the prompt" routes are now falsified**: negation (R3)
> and rewriting the prior (R5). The seals also sit in stable places (mostly the two right corners and the
> bottom margin), which looks like a strong prior rather than random noise.
>
> **Finding 2: the mechanical screen's `CLEAN` verdict is not trustworthy.** Of the three images it called
> `CLEAN`, two carry a **clear** red seal to the eye (not a faint one). `seal_check.py` is useful for
> "pointing at suspects" but **cannot be used in reverse (to declare an image clean)** — which also
> explains why its four automatic criteria all failed earlier: cinnabar, ochre, fur colour and paper are
> indistinguishable at the pixel level, so any threshold either over-reports or under-reports.

## 4. Scoring and the trade-off: why we do **not** switch

The bold tiger stripes are this round's biggest gain (`bold black tiger stripes` really does land), but
put the best candidate and the shipped final on the same rubric (A–F, weights in [PLAN.en.md](../../../PLAN.en.md) §5):

| Dimension (weight) | Shipped final R1 v1-101 | Best R5 candidate s2-1922 |
|---|---|---|
| A textual accuracy (.25) | 4 (stripes fairly soft) | **5** (all four traits, stripes clearly countable) |
| F spirit and life (.25) | **5** (clean linework, breathing white space) | 4 (heavy ink, hatching on neck and chest) |
| B bone-method purity (.15) | **5** (fine brushwork, pale colour) | 4 (harder contrast, closer to heavy colour) |
| C format completeness (.15) | 4 | 4.5 (fuller composition, larger subject) |
| D recognisability (.10) | 5 | 5 |
| E series consistency (.10) | **5** (same hand as the fox final) | 3.5 (visibly heavier and harder) |
| **Weighted total** | **4.60** | **4.38** |

> **Switching would be a downgrade.** Bold stripes are not free: they drag ink weight, contrast and
> shading up, and **the price is series consistency** (E drops a step and a half) plus one step each in
> spirit and bone method. This is the same lesson as R4: one dimension being stronger does not make the
> whole picture better; reading all six dimensions together is what keeps the answer honest.

**The final is unchanged**: `01-lu-shu.png` remains R1 v1-101 (clean corners, total 4.60). The 12 R5
images are not promoted; `work/` keeps them as the archive.

## 5. Takeaways

1. **The seal cannot be suppressed by wording**: negation (9 images, R3) and rewriting the prior
   (12 images, R5) are both falsified. What remains is "generate several and pick a clean one"
   (hit rate around 1/20) and "erase it with a tool".
2. **Bolder tiger stripes incur a series-consistency bill.** If a future subject wants bold stripes, the
   bone sentence's paper tone and ink weight should be darkened together and the fox should be re-run in
   the same round — otherwise the series splits into two hands.
3. **The mechanical screen can raise suspicion, never give clearance.** The criterion stays visual at
   magnification; the tool's job is to put candidates in front of the eye.
4. That visual step now has a fixed layout and self-checks (`scripts/corner_sheet.py`), which lowers the
   risk of a sheet being mismatched with its conclusions (rows = images, columns = corners, with
   `--enhance levels|redness`).

## 6. Open items

| Item | Status |
|------|--------|
| s2's medium clause × the final's **delicate** subject clause | ⏳ Untested: expected only to lower the hit rate, not to reach zero (this round used the bold subject clause throughout, which confounds the variable) |
| Fox R9 (the same experiment on the fox) | see [r09-review](../../jiu-wei-hu/rounds/r09-review.en.md) |
| Real seal layer in seal script | ⛔ Still missing (font unresolved) |
