"""冬虫夏草（菌 + 虫）子主题的 prompt 权威源与轮次定义。

概念
----
**《本草纲目》里的「冬虫夏草」就是虫与菌的拼接体**：
虫草菌寄生于蝙蝠蛾幼虫，**虫体与子座同现**——
冬天是虫，夏天从虫体上长出菌的子座。这是典籍里明写的、**真实存在**的拼接体。

底座 = **蛾幼虫**（定型的生物，形态自由度**中低**）。
供体 = 菌的部位：菌丝覆体 MY1 / 子座 ST1 / 孢子 SP1。

机制预测（依据本仓已实测的规律）
--------------------------------
- 规律 92（底座形态自由度）：幼虫**是定型的**，比 lichen 的菌丝体难；
  但比鹿/鱼好——因为"虫子表面长菌"在自然界真实存在，模型的先验里本来就有这张图。
- 规律 89/87：**菌丝覆体 MY1 是"同材质替换"**（虫壳 → 菌丝），预期只到部分。
- 规律 67/91：**子座 ST1 是"空位新增 + 不同形 + 高辨识度"**——本子主题的主力件，
  按规律应当**一次就成**（冬虫夏草的那根"草"）。
- 规律 93：这是微距题材（几厘米），取景句与摄影层沿用 lichen 的微距那一套。
"""
from __future__ import annotations

PREFIX = "bs-cd"  # bio-splice / cordyceps

CN_FRAME = "微距特写，一个生物体独自占据画面："

PHOTO_BASE = ("macro photograph, focus-stacked, fine surface detail, natural colour, "
              "no digital sharpening, no text, no watermark")

# ---------------------------------------------------------------------------
# 底座：蛾幼虫。**刻意不描述体表质感**——把那一处留给 MY1（菌丝覆体）
#   FULL_LARVA     ：照常写体表（占用版）
#   LARVA_OPEN     ：不写体表质感（腾出版，用于与占用版对照）
# ---------------------------------------------------------------------------

FULL_LARVA = ("a large moth larva with a segmented pale body, a dark head capsule "
              "and short stubby legs")
LARVA_OPEN = ("a large moth larva with a dark head capsule and short stubby legs")

assert " with " in FULL_LARVA and " with " in LARVA_OPEN, "_with 依赖「X with ...」结构"
assert "larva" in FULL_LARVA, "物种名是「这是虫」的锚，不能删"
assert "segmented" not in LARVA_OPEN and "pale body" not in LARVA_OPEN, \
    "腾出版：底座不许先描述体表质感"

# ---------------------------------------------------------------------------
# 移植件（只出菌的部位，绝不写成「整株真菌」）
# ---------------------------------------------------------------------------

MY1 = "a dense coating of pale fungal mycelium across the whole body"
ST1_ONE = "a single tall club-shaped fungal stroma rising from its body"
ST1_MANY = "several tall club-shaped fungal stromata rising from its body"
SP1 = "clusters of fine pale spores dusting the surface"

for _n, _p in (("MY1", MY1), ("ST1", ST1_ONE), ("ST1x", ST1_MANY), ("SP1", SP1)):
    assert "larva" not in _p and "moth" not in _p, f"{_n}: 移植件里不该出现底座"
    assert " whose " not in _p and "body is entirely" not in _p, f"{_n}: 不许用「整只」句式"
    assert "fungal" in _p or "spores" in _p, f"{_n}: 必须点名供体"


def _with(base: str, parts: list[str]) -> str:
    head, _, rest = base.partition(" with ")
    return f"{head} with {' and '.join(parts)}, {rest}"


def _styled(base: str, parts: list[str], *, frame: str = CN_FRAME, pose: str,
            scene: str, light: str, lens: str) -> str:
    core = _with(base, parts) if parts else base
    return (f"{frame}{pose}{core}. {scene}. {light}. "
            f"{lens}, {PHOTO_BASE}.")


ARCHIVE_LAYERS = f"{CN_FRAME}<姿态><底座 with 部位>. <生境>. <光线>. <镜头>, {PHOTO_BASE}."

ROUNDS: dict[int, dict] = {}

# ---------------------------------------------------------------------------
# R1（期 01/02 候选）：土面 · 柔光 · 微距 —— 一轮里同时测难件与易件
#   底座对照 / 菌丝覆体 MY1 / 单根子座 ST1 / 两者同体
# ---------------------------------------------------------------------------

C1 = dict(pose="它伏在土面上、身体侧向镜头：",
          scene="on damp dark soil among dead leaves",
          light="soft diffused light under a forest canopy",
          lens="a low macro view, 100mm macro lens at f/8")

ROUNDS[1] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 9101,
    "note": "虫草·第一期候选：蛾幼虫底座 + 菌丝覆体 MY1 / 单根子座 ST1（含同轮底座对照）",
    "shots": [
        {"name": "base-larva", "seed": 9101, "prompt": _styled(FULL_LARVA, [], **C1)},
        {"name": "larva-mycelium", "seed": 9101,
         "prompt": _styled(FULL_LARVA, [MY1], **C1)},
        {"name": "larva-stroma", "seed": 9101,
         "prompt": _styled(FULL_LARVA, [ST1_ONE], **C1)},
        {"name": "larva-mycelium-stroma", "seed": 9101,
         "prompt": _styled(FULL_LARVA, [MY1, ST1_ONE], **C1)},
    ],
}

# ---------------------------------------------------------------------------
# R2：MY1 的**占用 vs 腾出**对照（同呈现、同 seed，只换底座）
# ---------------------------------------------------------------------------

ROUNDS[2] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 9101,
    "note": "虫草·第一期对照【腾出版】：底座不写体表质感 + 菌丝覆体 MY1；含同轮底座对照",
    "shots": [
        {"name": "base-larva", "seed": 9101, "prompt": _styled(LARVA_OPEN, [], **C1)},
        {"name": "larva-mycelium", "seed": 9101,
         "prompt": _styled(LARVA_OPEN, [MY1], **C1)},
    ],
}

# 守卫：姿态句不许提到目标部位（规律 79）
for _w in ("菌", "丝", "子座", "孢子", "mycelium", "stroma", "spore", "coat"):
    assert _w not in C1["pose"], f"姿态句里出现了 {_w}（规律 79）"


# ---------------------------------------------------------------------------
# R1/R2 结论与定稿安排
#
#   ✅ ST1 子座（单根）**一次就成**：从虫体上拔出一根棒状子座，正是冬虫夏草的形象
#   ✅ MY1 菌丝覆体成立，但**占用版与腾出版差别明显**：
#        占用版（底座已写 segmented pale body）→ 虫本身就发白，菌丝的边际贡献小
#        腾出版（底座只写头与足）        → 覆盖对比一眼可辨
#      → **规律 96：腾出占位对"体表质感"有效，对"典范器官"无效**（89 的细化）
#
# 定稿：期 01 用**腾出版**底座；期 02–05 用同一个 FULL_LARVA（子座与孢子与体表无关）。
# ---------------------------------------------------------------------------

# 期 01（腾出版 · 土面柔光微距 · 方）—— 三个 seed
ROUNDS[3] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 9101,
    "note": "期 01 定稿【菌丝覆体】：底座不写体表质感 + MY1（三个 seed）；含同轮底座对照",
    "shots": [
        {"name": "base-larva", "seed": 9101, "prompt": _styled(LARVA_OPEN, [], **C1)},
        {"name": "larva-mycelium", "seed": 9101,
         "prompt": _styled(LARVA_OPEN, [MY1], **C1)},
        {"name": "larva-mycelium-b", "seed": 9102,
         "prompt": _styled(LARVA_OPEN, [MY1], **C1)},
        {"name": "larva-mycelium-c", "seed": 9103,
         "prompt": _styled(LARVA_OPEN, [MY1], **C1)},
    ],
}

# 期 02：高山草甸 · 晨光 · 低机位微距 · 竖（一根子座）
C2 = dict(pose="它伏在草甸的土面上、身体侧向镜头：",
          scene="on alpine meadow soil among short grasses",
          light="low morning sun, dew on the ground",
          lens="a low macro view from just above the ground, 100mm macro lens at f/8")

ROUNDS[4] = {
    "engine": "zimage", "size": (1024, 1280), "steps": 12, "seed": 9101,
    "note": "期 02 定稿【单根子座】：蛾幼虫底座 + 单根 ST1（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-larva", "seed": 9101, "prompt": _styled(FULL_LARVA, [], **C2)},
        {"name": "larva-stroma", "seed": 9101,
         "prompt": _styled(FULL_LARVA, [ST1_ONE], **C2)},
        {"name": "larva-stroma-b", "seed": 9102,
         "prompt": _styled(FULL_LARVA, [ST1_ONE], **C2)},
    ],
}

# 期 03：同一草甸 · 逆光 · 方（多根子座）
C3 = dict(C2, light="strong backlight through the grass, rimming the stromata")

ROUNDS[5] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 9101,
    "note": "期 03 定稿【多根子座】：蛾幼虫底座 + 多根 ST1x；逆光 · 方（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-larva", "seed": 9101, "prompt": _styled(FULL_LARVA, [], **C3)},
        {"name": "larva-stromata", "seed": 9101,
         "prompt": _styled(FULL_LARVA, [ST1_MANY], **C3)},
        {"name": "larva-stromata-b", "seed": 9102,
         "prompt": _styled(FULL_LARVA, [ST1_MANY], **C3)},
    ],
}

# 期 04：雪线草甸 · 冷光 · 横（子座 + 孢子）
C4 = dict(pose="它伏在砾石土面上、身体侧向镜头：",
          scene="on gravelly soil at the snow line, patches of old snow behind",
          light="cold flat light, no shadows",
          lens="a low macro view, 100mm macro lens at f/11")

ROUNDS[6] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 9101,
    "note": "期 04 定稿【子座与孢子】：蛾幼虫底座 + 单根 ST1 + 孢子 SP1；雪线冷光 · 横；含同轮底座对照",
    "shots": [
        {"name": "base-larva", "seed": 9101, "prompt": _styled(FULL_LARVA, [], **C4)},
        {"name": "larva-stroma-spores", "seed": 9101,
         "prompt": _styled(FULL_LARVA, [ST1_ONE, SP1], **C4)},
        {"name": "larva-stroma-spores-b", "seed": 9102,
         "prompt": _styled(FULL_LARVA, [ST1_ONE, SP1], **C4)},
    ],
}

# 期 05（收官）：**标本摄影**——本子主题唯一换呈现媒介的一期
C5 = dict(frame="标本照，一个标本独自占据画面：",
          pose="它被放在灰色台面上、身体侧向镜头：",
          scene="on a plain neutral grey background, nothing else in frame",
          light="ring light, deep even illumination, everything in focus",
          lens="a flat-on macro view, 100mm macro lens at f/16")

ROUNDS[7] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 9101,
    "note": "期 05 收官【冬虫夏草·标本照】：蛾幼虫 + 菌丝覆体 MY1 + 子座 ST1 + 孢子 SP1；中性背景环形光（两个 take）",
    "shots": [
        {"name": "base-larva", "seed": 9101, "prompt": _styled(FULL_LARVA, [], **C5)},
        {"name": "cordyceps-specimen", "seed": 9101,
         "prompt": _styled(FULL_LARVA, [MY1, ST1_ONE, SP1], **C5)},
        {"name": "cordyceps-specimen-b", "seed": 9102,
         "prompt": _styled(FULL_LARVA, [MY1, ST1_ONE, SP1], **C5)},
    ],
}
