# 全部轮次原始 Prompt 存档

> 本文件由 `python3 run_round.py --prompts` 自动生成，内容 = **实际提交给 ComfyUI 的字符串**。
> 为便于查阅与逐轮对照，代码块内已按分句换行；**换行符不属于 prompt，仅排版**。
> 还原规则：行尾是 ASCII 字符时，该换行等于一个空格；否则换行处原本没有字符。
> `run_round.py` 的 `unwrap_prompt()` 就是这条规则，生成时会逐条断言「还原 == 原文」。
> 逐字原文（单行）见 `run_round.py` 的常量（`python3 run_round.py <N> --dry` 可直接打印）
> 与 `work/rN/round.json`；最终依据是服务器 `GET /history/{prompt_id}`。
> 修改 prompt 请改 `subjects/<子主题>/rounds.py`，然后重新生成本文件。
> 返回[子主题首页](../README.md) ｜ [项目首页](../../../README.md)

## 记录在哪（三层）

| 层 | 位置 | 内容 |
|----|------|------|
| 权威源 | `subjects/<子主题>/rounds.py` | 逐字 prompt（真正发出去的，单行） |
| 可读文档 | 本文件 / `docs/rN.md` | 分句换行的 prompt 全文；每轮改动与自检 |
| 机器记录 | `work/rN/round.json` | 文件名 / seed / prompt_id / 引擎 / 参数 / **prompt 原文** |
| 服务器侧 | `GET /history/{prompt_id}` | ComfyUI 实际执行的完整图（最终依据） |

## R1 · 2×2 拼接矩阵四角 + 拼接语义 A/B/C 同 seed 对照（纯猫/纯鹰为对照组）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：8（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R2 · 鹰头猫塌成纯鹰的四个单变量假设（基线 = R1-A 原句，同 seed 4201 可比）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R3 · 修 H2 的双头：用「from the neck down」正向限定身体范围（基线 = R2 身在前）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R4 · 双头真因：给身体去名（只写部件，不写「猫」）—— 基线 = R2 身在前 / R3 neck-down

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R5 · 绕开「点名即整体渲染」：名字绑部件 / 正向单头计数 / 去并列结构

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R6 · 期 02 候选：鹰底座 + 猫的小件（耳 / 尾 / 掌）—— 强底座 + 弱物种小件

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R7 · 期 03 候选：猫底座 + 鹰的局部件（翼 / 尾羽）—— 弱底座 + 强物种局部件

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R8 · 期 04 候选：鹰底座 + 猫的三处（C1 耳 / C5 尾 / C6 胡须）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R9 · 期 05 候选：猫底座 + 鹰的三处（E2 翼 / E5 尾羽 / E6 颈羽）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

