# All Rounds · Raw Prompt Archive

> 🌐 Language: **English** | [中文](prompts-all.md)

> This file is generated automatically by `python3 run_round.py --prompts`; its content = **the string actually submitted to ComfyUI**.
> For easier reading and round-by-round comparison, the code blocks are broken at sentence boundaries; **the line breaks are not part of the prompt, they are layout only**.
> Unwrapping rule: when the end of a line is an ASCII character, that line break equals one space; otherwise there was no character at the break to begin with.
> `run_round.py`'s `unwrap_prompt()` is exactly this rule, and generation asserts "unwrap == original" for every entry.
> The verbatim original (single line) is in the constants of `run_round.py` (`python3 run_round.py <N> --dry` prints it directly)
> and in `work/rN/round.json`; the final authority is the server's `GET /history/{prompt_id}`.
> To change a prompt, edit `subjects/<子主题>/rounds.py` and then regenerate this file.
> Back to the [sub-theme home page](../README.en.md) ｜ [project home page](../../../README.en.md)

## Where It Is Recorded (three layers)

| Layer | Location | Content |
|----|------|------|
| Authoritative source | `subjects/<子主题>/rounds.py` | the verbatim prompt (what is really sent out, single line) |
| Readable document | this file / `docs/rN.md` | the full prompt with sentence line breaks; each round's changes and self-checks |
| Machine record | `work/rN/round.json` | filename / seed / prompt_id / engine / parameters / **prompt verbatim** |
| Server side | `GET /history/{prompt_id}` | the complete graph ComfyUI actually executed (the final authority) |

## R1 · the four corners of the 2×2 splice matrix + splice semantics A/B/C with same-seed controls (pure cat / pure eagle as the control group)

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 8 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<主体>.
<拼接句> in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### cat　seed 4201

```text
全身像，一只动物独自占据画面：a feral tabby cat, head to tail, with a broad feline head,
tufted ears, whiskers, green slit-pupil eyes, dense striped fur, four legs and a long tail.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### eagle　seed 4201

```text
全身像，一只动物独自占据画面：a golden eagle, head to tail, with a hooked yellow beak,
a dark brown feathered head, a piercing amber eye, a feathered neck ruff, folded wings,
and scaled yellow legs with black talons.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### owl-seamless　seed 4201

```text
全身像，一只动物独自占据画面：
a single animal whose head is entirely a domestic cat's and whose body is entirely a golden eagle's
-- the head with a cat's short muzzle,
whiskers, triangular tufted ears, green slit-pupil eyes and soft striped fur;
the body with an eagle's dark brown feathering,
folded wings and scaled yellow legs with black talons;
the head and the body are joined at the neck.
The join is invisible:
the fur of the head and the feathers of the body meet in a natural transition,
as if this animal had evolved this way.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### owl-seam　seed 4201

```text
全身像，一只动物独自占据画面：
a single animal whose head is entirely a domestic cat's and whose body is entirely a golden eagle's
-- the head with a cat's short muzzle,
whiskers, triangular tufted ears, green slit-pupil eyes and soft striped fur;
the body with an eagle's dark brown feathering,
folded wings and scaled yellow legs with black talons;
the head and the body are joined at the neck.
The join is a visible seam:
a line of coarse dark stitching runs right around the neck where the two halves are sewn together,
the two halves are mismatched in texture and slightly in scale,
and the whole animal looks assembled from two different animals like a museum specimen.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### owl-surreal　seed 4201

```text
全身像，一只动物独自占据画面：
a single animal whose head is entirely a domestic cat's and whose body is entirely a golden eagle's
-- the head with a cat's short muzzle,
whiskers, triangular tufted ears, green slit-pupil eyes and soft striped fur;
the body with an eagle's dark brown feathering,
folded wings and scaled yellow legs with black talons;
the head and the body are joined at the neck.
Everything is slightly wrong: the head is a little too large for the body,
the gaze is uncanny and too still,
and the proportions are deliberately impossible -- yet the animal is photographed as calmly and
plainly as if it were an ordinary species.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### eaglecat-seamless　seed 4201

```text
全身像，一只动物独自占据画面：
a single animal whose head is entirely a golden eagle's and whose body is entirely a domestic cat's
-- the head with a hooked yellow beak,
a dark brown feathered crown, a piercing amber eye and a feathered neck ruff;
the body with dense tabby fur, four feline legs, sheathed claws and a long tail,
with no wings at all; the head and the body are joined at the neck.
The join is invisible:
the fur of the head and the feathers of the body meet in a natural transition,
as if this animal had evolved this way.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### eaglecat-seam　seed 4201

```text
全身像，一只动物独自占据画面：
a single animal whose head is entirely a golden eagle's and whose body is entirely a domestic cat's
-- the head with a hooked yellow beak,
a dark brown feathered crown, a piercing amber eye and a feathered neck ruff;
the body with dense tabby fur, four feline legs, sheathed claws and a long tail,
with no wings at all; the head and the body are joined at the neck.
The join is a visible seam:
a line of coarse dark stitching runs right around the neck where the two halves are sewn together,
the two halves are mismatched in texture and slightly in scale,
and the whole animal looks assembled from two different animals like a museum specimen.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### eaglecat-surreal　seed 4201

```text
全身像，一只动物独自占据画面：
a single animal whose head is entirely a golden eagle's and whose body is entirely a domestic cat's
-- the head with a hooked yellow beak,
a dark brown feathered crown, a piercing amber eye and a feathered neck ruff;
the body with dense tabby fur, four feline legs, sheathed claws and a long tail,
with no wings at all; the head and the body are joined at the neck.
Everything is slightly wrong: the head is a little too large for the body,
the gaze is uncanny and too still,
and the proportions are deliberately impossible -- yet the animal is photographed as calmly and
plainly as if it were an ordinary species.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R2 · four single-variable hypotheses for the eagle-headed cat collapsing into a pure eagle (baseline = R1-A's original sentence, comparable at the same seed 4201)

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 4 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<主体>.
<拼接句> in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### minus-wings-clause　seed 4201

```text
全身像，一只动物独自占据画面：
a single animal whose head is entirely a golden eagle's and whose body is entirely a domestic cat's
-- the head with a hooked yellow beak,
a dark brown feathered crown, a piercing amber eye and a feathered neck ruff;
the body with dense tabby fur, four feline legs, sheathed claws and a long tail;
the head and the body are joined at the neck.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### body-first　seed 4201

```text
全身像，一只动物独自占据画面：
a single animal whose body is entirely a domestic cat's and whose head is entirely a golden eagle's
-- the body with dense tabby fur,
four feline legs, sheathed claws and a long tail; the head with a hooked yellow beak,
a dark brown feathered crown, a piercing amber eye and a feathered neck ruff, with no wings at all;
the head and the body are joined at the neck.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### feather-scope　seed 4201

```text
全身像，一只动物独自占据画面：
a single animal whose head is entirely a golden eagle's and whose body is entirely a domestic cat's
-- the head with a hooked yellow beak,
a dark brown feathered crown, a piercing amber eye and a feathered neck ruff;
the body with dense tabby fur, four feline legs, sheathed claws and a long tail,
with no wings at all;
the head and the body are joined at the neck Feathers grow only on the head and the neck;
the whole body is covered in fur..
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### no-eagle-token　seed 4201

```text
全身像，一只动物独自占据画面：
a single animal whose head is entirely a large bird of prey's and whose body is entirely a domestic
cat's -- the head with a hooked yellow beak,
a dark brown feathered crown, a piercing amber eye and a feathered neck ruff;
the body with dense tabby fur, four feline legs, sheathed claws and a long tail,
with no wings at all; the head and the body are joined at the neck.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R3 · fixing H2's two heads: positively bounding the body's extent with "from the neck down" (baseline = R2's body-first)

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 4 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<主体>.
<拼接句> in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### neck-down　seed 4201

```text
全身像，一只动物独自占据画面：
a single animal whose body is entirely a domestic cat's and whose head is entirely a golden eagle's
-- the body from the neck down,
with dense tabby fur, four feline legs, sheathed claws and a long tail;
the head with a hooked yellow beak, a dark brown feathered crown,
a piercing amber eye and a feathered neck ruff, with no wings at all;
the head and the body are joined at the neck.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### neck-down-mix　seed 4201

```text
全身像，一只动物独自占据画面：
a single animal whose body is entirely a domestic cat's and whose head is entirely a golden eagle's
-- the body from the neck down,
with dense tabby fur, four feline legs, sheathed claws and a long tail;
the head with a hooked yellow beak, a dark brown feathered crown,
a piercing amber eye and a feathered neck ruff, with no wings at all;
the head and the body are joined at the neck The two halves come from two different animals and are
joined at the neck..
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### neck-down-paws　seed 4201

```text
全身像，一只动物独自占据画面：
a single animal whose body is entirely a domestic cat's and whose head is entirely a golden eagle's
-- the body from the neck down,
with dense tabby fur, four feline legs, sheathed claws and a long tail;
the head with a hooked yellow beak, a dark brown feathered crown,
a piercing amber eye and a feathered neck ruff, with no wings at all;
the head and the body are joined at the neck It stands on four furry paws with soft toe pads..
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### neck-down-no-token　seed 4201

```text
全身像，一只动物独自占据画面：
a single animal whose body is entirely a domestic cat's and whose head is entirely a large bird of
prey's -- the body from the neck down,
with dense tabby fur, four feline legs, sheathed claws and a long tail;
the head with a hooked yellow beak, a dark brown feathered crown,
a piercing amber eye and a feathered neck ruff, with no wings at all;
the head and the body are joined at the neck.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R4 · the real cause of the two heads: unname the body (write only parts, never "cat") —— baseline = R2 body-first / R3 neck-down

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 4 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<主体>.
<拼接句> in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### parts-body　seed 4201

```text
全身像，一只动物独自占据画面：a single animal:
a four-legged furry body with dense striped tabby fur, four furry legs with soft paws,
and a long ringed tail; and the head of a golden eagle with a hooked yellow beak,
a dark brown feathered crown and a piercing amber eye;
the head and the body are joined at the neck.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### parts-body-mix　seed 4201

```text
全身像，一只动物独自占据画面：a single animal:
a four-legged furry body with dense striped tabby fur, four furry legs with soft paws,
and a long ringed tail; and the head of a golden eagle with a hooked yellow beak,
a dark brown feathered crown and a piercing amber eye;
the head and the body are joined at the neck The two halves come from two different animals and are
joined at the neck..
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### parts-head-first　seed 4201

```text
全身像，一只动物独自占据画面：a single animal:
the head of a golden eagle with a hooked yellow beak,
a dark brown feathered crown and a piercing amber eye;
and a four-legged furry body with dense striped tabby fur, four furry legs with soft paws,
and a long ringed tail; the head and the body are joined at the neck.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### parts-no-token　seed 4201

```text
全身像，一只动物独自占据画面：a single animal:
a four-legged furry body with dense striped tabby fur, four furry legs with soft paws,
and a long ringed tail; and the head of a large bird of prey with a hooked yellow beak,
a dark brown feathered crown and a piercing amber eye;
the head and the body are joined at the neck.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R5 · getting around "naming it renders it whole": bind the name to a part / positive single-head count / remove the coordination structure

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<主体>.
<拼接句> in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### parts-of-cat　seed 4201

```text
全身像，一只动物独自占据画面：a single animal: the torso, flanks,
four furry legs and long ringed tail of a domestic tabby cat, with soft paws;
and the head of a golden eagle, with a hooked yellow beak,
a dark brown feathered crown and a piercing amber eye;
the head and the body are joined at the neck.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### one-head　seed 4201

```text
全身像，一只动物独自占据画面：a single animal with exactly one head: the torso, flanks,
four furry legs and long ringed tail of a domestic tabby cat, with soft paws;
and the head of a golden eagle, with a hooked yellow beak,
a dark brown feathered crown and a piercing amber eye;
the head and the body are joined at the neck.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### single-phrase　seed 4201

```text
全身像，一只动物独自占据画面：a single animal:
the body of a domestic tabby cat from the neck down -- furry striped flanks,
four furry legs with soft paws and a long ringed tail -- topped by the head of a golden eagle,
with a hooked yellow beak, a dark brown feathered crown and a piercing amber eye;
the two halves are joined at the neck.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R6 · period 02 candidates: eagle base + small cat pieces (ears / tail / paws) —— strong base + small pieces of a weak species

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 4 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<主体>.
<拼接句> in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### e-cat-ears　seed 4201

```text
全身像，一只动物独自占据画面：a golden eagle with a domestic cat's triangular tufted ears,
a hooked yellow beak, a dark brown feathered head, a feathered neck ruff, a piercing amber eye,
folded wings, and scaled yellow legs with black talons.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### e-cat-tail　seed 4201

```text
全身像，一只动物独自占据画面：a golden eagle with a domestic cat's long ringed tabby tail,
a hooked yellow beak, a dark brown feathered head, a feathered neck ruff, a piercing amber eye,
folded wings, and scaled yellow legs with black talons.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### e-cat-paws　seed 4201

```text
全身像，一只动物独自占据画面：a golden eagle with soft furry domestic cat's paws on its feet,
a hooked yellow beak, a dark brown feathered head, a feathered neck ruff, a piercing amber eye,
folded wings, and scaled yellow legs with black talons.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### e-cat-ears-tail　seed 4201

```text
全身像，一只动物独自占据画面：
a golden eagle with a domestic cat's triangular tufted ears and a domestic cat's long ringed tabby
tail,
a hooked yellow beak, a dark brown feathered head, a feathered neck ruff, a piercing amber eye,
folded wings, and scaled yellow legs with black talons.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R7 · period 03 candidates: cat base + local eagle pieces (wings / tail feathers) —— weak base + local pieces of a strong species

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<主体>.
<拼接句> in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### c-eagle-wings　seed 4201

```text
全身像，一只动物独自占据画面：a feral tabby cat with broad folded feathered eagle wings,
a broad feline head, tufted ears, whiskers, green slit-pupil eyes, dense striped fur,
four legs and a long tail.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### c-eagle-tail　seed 4201

```text
全身像，一只动物独自占据画面：a feral tabby cat with a fan of dark brown eagle tail feathers,
a broad feline head, tufted ears, whiskers, green slit-pupil eyes, dense striped fur,
four legs and a long tail.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### c-eagle-wings-tail　seed 4201

```text
全身像，一只动物独自占据画面：
a feral tabby cat with broad folded feathered eagle wings and a fan of dark brown eagle tail
feathers,
a broad feline head, tufted ears, whiskers, green slit-pupil eyes, dense striped fur,
four legs and a long tail.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R8 · period 04 candidates: eagle base + three cat pieces (C1 ears / C5 tail / C6 whiskers); includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 4 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<主体>.
<拼接句> in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-eagle　seed 4201

```text
全身像，一只动物独自占据画面：a golden eagle with a hooked yellow beak,
a dark brown feathered head, a feathered neck ruff, a piercing amber eye, folded wings,
and scaled yellow legs with black talons.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### e-cat-whiskers　seed 4201

```text
全身像，一只动物独自占据画面：a golden eagle with a domestic cat's long thin whiskers,
a hooked yellow beak, a dark brown feathered head, a feathered neck ruff, a piercing amber eye,
folded wings, and scaled yellow legs with black talons.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### e-cat-ears-whiskers　seed 4201

```text
全身像，一只动物独自占据画面：
a golden eagle with a domestic cat's triangular tufted ears and a domestic cat's long thin
whiskers,
a hooked yellow beak, a dark brown feathered head, a feathered neck ruff, a piercing amber eye,
folded wings, and scaled yellow legs with black talons.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### e-cat-3parts　seed 4201

```text
全身像，一只动物独自占据画面：
a golden eagle with a domestic cat's triangular tufted ears and a domestic cat's long ringed tabby
tail and a domestic cat's long thin whiskers,
a hooked yellow beak, a dark brown feathered head, a feathered neck ruff, a piercing amber eye,
folded wings, and scaled yellow legs with black talons.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R9 · period 05 candidates: cat base + three eagle pieces (E2 wings / E5 tail feathers / E6 neck ruff); includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 4 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<主体>.
<拼接句> in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-cat　seed 4201

```text
全身像，一只动物独自占据画面：a feral tabby cat with a broad feline head, tufted ears, whiskers,
green slit-pupil eyes, dense striped fur, four legs and a long tail.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### c-eagle-ruff　seed 4201

```text
全身像，一只动物独自占据画面：
a feral tabby cat with a thick ruff of dark brown eagle feathers around its neck,
a broad feline head, tufted ears, whiskers, green slit-pupil eyes, dense striped fur,
four legs and a long tail.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### c-eagle-tail-ruff　seed 4201

```text
全身像，一只动物独自占据画面：
a feral tabby cat with a fan of dark brown eagle tail feathers and a thick ruff of dark brown eagle
feathers around its neck,
a broad feline head, tufted ears, whiskers, green slit-pupil eyes, dense striped fur,
four legs and a long tail.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### c-eagle-3parts　seed 4201

```text
全身像，一只动物独自占据画面：
a feral tabby cat with broad folded feathered eagle wings and a fan of dark brown eagle tail
feathers and a thick ruff of dark brown eagle feathers around its neck,
a broad feline head, tufted ears, whiskers, green slit-pupil eyes, dense striped fur,
four legs and a long tail.
in a misty autumn meadow, the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

