# Black Tortoise Part Table (Turtle + Snake)

> 🌐 Language: **English** | [中文](parts.md)

> Back to [sub-theme home](README.en.md) ｜ [project home](../../README.en.md)

**Design source**: the Black Tortoise is the only **merged** figure among the Four Symbols — a turtle and a snake sharing one body.
So this sub-theme does not invent a splice; it **reproduces a merger that already exists**.

**Base = turtle** (carapace / plastron / short legs).
In the base description we **deliberately omit the length of the neck and omit the tail** — freeing up these two spots (Rule 66).

---

## 1. Part table and measurements

| ID | Part | Donor | prompt anchor (part only) | Placeholder on the turtle base? | Measured result |
|------|------|------|--------------------------|------------------|----------|
| N1 | Snake neck | Snake | `a long sinuous snake's neck with fine keeled scales` | **Placeholder can be freed** (the turtle has a short neck) | ✅ **Fully holds** (all three seeds succeeded, 5.00) |
| N2 | Snake tail | Snake | `a long tapering snake's tail with keeled scales` | **Placeholder can be freed** (the turtle has a small tail) | ✅ **Fully holds** (5.00 / 4.85 / 4.55) |
| N3 | Coiled body | Snake | `thick snake coils around its shell` | Empty slot (nothing on the shell) | ✅ Holds (4.70), **but wording-sensitive**, see below |
| N4 | ~~Snake head~~ | Snake | — | — | ⛔ **Not done**: head parts are not transplantable (Rule 73) |
| N5 | Snake scales | Snake | `large overlapping snake scales` | Placeholder (the shell has scutes) | Not tested (not needed this period, kept in reserve) |

## 2. N3 coiled body: wording matters more than the placeholder (Rule 81)

N3 is an "empty-slot addition", which per Rule 67 should be the easiest piece of all, **yet in the first round it landed 0% of the time**.
In the same round we swapped in three wordings, and **all three landed**:

| Wording | Result |
|------|------|
| ❌ `the thick coiled body of a large snake wrapped around its shell` | **No-op** |
| ✅ `a thick snake's body coiled on the stones beneath it, its coils visible on both sides` | ✅ |
| ✅ `thick snake coils around its shell` | ✅ (shortest and most stable) |
| ✅ `thick snake coils around the rim of its shell` | ✅ |

> **Rule 81: spatial-relation clauses fail; switch to noun phrases.**
> `X wrapped around Y` (relative clause + long modifier) is not executed;
> only `X coils around Y` (noun phrase + verb) lands.
> This extends Rule 69 (composite parts must be written separately): **the spatial relation between part and base must also be written plainly**.

## 3. Base choice and freeing placeholders

| Practice | Notes |
|------|------|
| What the base spells out | shell (`a dark domed shell`) + head (`a small wrinkled head`) + limbs (`four short webbed legs`) |
| What the base **does not** spell out | the length of the neck, and the tail — these two are reserved for N1 / N2 |
| Why | Rules 56/66: a part already occupied in the base description overrides the transplanted piece; only spots left unoccupied can be freed |

## 4. Wording discipline for transplanted parts

```
✅ a long sinuous snake's neck with fine keeled scales    ← 部位短语，安全
✅ thick snake coils around its shell                    ← 名词短语 + 动词，安全
❌ the thick coiled body of a large snake wrapped around its shell   ← 关系从句，空操作
❌ a snake's body                                          ← 整体名词，会拖出整只蛇
```

And **no snake head is given** (Rule 73: head parts are a dead end in both directions) —
the Black Tortoise's snake starts at the neck and ends at the tail, with the coiled body connecting neck and tail, **and no head at all**.

---

## Revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Black Tortoise part table N1–N5 + measurement results across five periods + Rule 81 (spatial-relation wording) | 小七 |
