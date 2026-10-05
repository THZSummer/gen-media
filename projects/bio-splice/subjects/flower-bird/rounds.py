"""花 + 鸟子主题的 prompt 权威源与轮次定义。

概念
----
**「花鸟」是中国画的基本单元**——花冠与鸟羽互为拟态（蜂鸟如花、兰花如蜂）。
本子主题把这个"画科"变成**同体**：花的部件位置上长出鸟的羽。

底座 = **大花**（玉兰 / 兰花）。
供体 = 鸟的羽类三件：
  P1 羽（落在**花瓣环**上——花最定型的结构，预期最难）
  P5 绒羽（落在**花心**——空面）
  P6 翎羽（从**花梗**上生出——只有"表面"作为承载面，同 cordyceps 的子座）

机制预判（按 92/96/97/99 的四问）
--------------------------------
- 落点 P1 花瓣：**典范结构**（花之所以是花）→ 预期只到部分（改质不改形？待测）
- 落点 P5 花心：底座不写花心时是**空面** → 预期易成
- 落点 P6 花梗：从表面生出的件，**不需要承载结构**（规律 97）→ 预期易成
- 写法：P1 有三种可能写法（关系从句 / 纯名词短语 / 覆盖式），本轮一次测清。
"""
from __future__ import annotations

PREFIX = "bs-fb2"  # bio-splice / flower-bird（fb 已被 fish-bird 占用）

CN_FRAME = "微距特写，一个生物体独自占据画面："

PHOTO_BASE = ("macro photograph, fine surface detail, soft natural colour, "
              "no digital sharpening, no text, no watermark")

# ---------------------------------------------------------------------------
# 底座：大花（白玉兰）。三个版本按"腾出哪一处"分
#   FLOWER          ：花瓣 + 花心都写（占用版）
#   FLOWER_PETALS   ：不写花瓣环（把花瓣位腾给 P1）
#   FLOWER_CENTRE   ：不写花心（把花心位腾给 P5）
# ---------------------------------------------------------------------------

FLOWER = ("a large white magnolia flower with broad rounded petals and a ring "
          "of pale stamens")
FLOWER_PETALS = "a large white magnolia flower with a ring of pale stamens"
FLOWER_CENTRE = "a large white magnolia flower with broad rounded petals"

for _n, _b in (("FLOWER", FLOWER), ("PETALS", FLOWER_PETALS), ("CENTRE", FLOWER_CENTRE)):
    assert " with " in _b, f"{_n}: _with 依赖「X with ...」结构"
    assert "magnolia" in _b, f"{_n}: 物种名是「这是花」的锚"
assert "petal" not in FLOWER_PETALS, "腾出版：不许写花瓣"
assert "stamen" not in FLOWER_CENTRE, "腾出版：不许写花心"

# ---------------------------------------------------------------------------
# 移植件：三种写法（P1）+ 绒羽 P5 + 翎羽 P6
# ---------------------------------------------------------------------------

P1_REL = "broad pale bird feathers in place of the petals"          # 关系从句（规律 81 预期失效）
P1_RING = "a ring of broad pale bird feathers"                       # 纯名词短语（位置＝花瓣环）
P1_COAT = "broad pale bird feathers covering the flower"             # 覆盖式（cordyceps 菌丝那种）

P5 = "a tuft of soft downy bird feathers in the centre of the flower"
P6 = "long pale bird plume feathers rising from the stem"

for _n, _p in (("P1rel", P1_REL), ("P1ring", P1_RING), ("P1coat", P1_COAT),
               ("P5", P5), ("P6", P6)):
    assert "magnolia" not in _p and "flower" not in _p or _n in ("P1coat", "P5"), \
        f"{_n}: 移植件里尽量不出现底座词"
    assert " whose " not in _p and "body is entirely" not in _p, f"{_n}: 不许用「整只」句式"
    assert "bird" in _p, f"{_n}: 必须点名供体"
    assert "beak" not in _p and "claw" not in _p and "eye" not in _p, \
        f"{_n}: 喙/爪/眼已删（头部件 73 / 花无四肢 74）"


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
# R1（期 01 候选 · 腾出版底座）：晨露柔光微距 —— 三种写法同轮对比
# ---------------------------------------------------------------------------

B1 = dict(pose="它开在枝头、正面朝向镜头：",
          scene="on a spring branch, dew on the petals",
          light="soft diffused morning light",
          lens="a level macro view, 100mm macro lens at f/8")

ROUNDS[1] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 11101,
    "note": "花鸟·第一期候选：底座腾出花瓣环 + 鸟羽的三种写法（含同轮底座对照）",
    "shots": [
        {"name": "base-flower", "seed": 11101, "prompt": _styled(FLOWER_PETALS, [], **B1)},
        {"name": "flower-feathers-rel", "seed": 11101,
         "prompt": _styled(FLOWER_PETALS, [P1_REL], **B1)},
        {"name": "flower-feathers-ring", "seed": 11101,
         "prompt": _styled(FLOWER_PETALS, [P1_RING], **B1)},
        {"name": "flower-feathers-coat", "seed": 11101,
         "prompt": _styled(FLOWER_PETALS, [P1_COAT], **B1)},
    ],
}

# ---------------------------------------------------------------------------
# R2（期 01 对照 · 占用版底座）：花瓣照常写，用 R1 里最可能成的写法
# ---------------------------------------------------------------------------

ROUNDS[2] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 11101,
    "note": "花鸟·第一期对照【占用版】：底座照常写花瓣 + 鸟羽（含同轮底座对照）",
    "shots": [
        {"name": "base-flower", "seed": 11101, "prompt": _styled(FLOWER, [], **B1)},
        {"name": "flower-feathers", "seed": 11101,
         "prompt": _styled(FLOWER, [P1_RING], **B1)},
    ],
}

# 守卫：姿态句不许提到目标部位（规律 79）
for _w in ("羽", "绒", "翎", "花心", "花瓣", "feather", "down", "plume", "petal", "centre"):
    assert _w not in B1["pose"], f"姿态句里出现了 {_w}（规律 79）"


# ---------------------------------------------------------------------------
# R1/R2 结论：**花瓣环是典范结构，羽替花瓣 0%**
#
#   三种写法（关系从句 / 纯名词短语 / 覆盖式）在**腾出版与占用版上都 0%**；
#   连"覆盖式"（cordyceps 上成功的 mycelium 写法）在花上也失效。
#   → 与鹿颈、鱼鳍同类：**落点是典范结构 → 换不掉**（规律 89/99）。
#     而且腾出版里模型**自己把花瓣补了回来**（规律 87）。
#
# 按规律 99 换到**空面落点**：
#   P5 绒羽 → 花心（把花蕊描述腾掉）
#   P6 翎羽 → 花梗（从表面生出的件，同 cordyceps 的子座）
#
# R3 测花心，R4 测花梗。
# ---------------------------------------------------------------------------

B2 = dict(pose="它开在枝头、正面朝向镜头：",
          scene="on a spring branch, dew on the petals",
          light="raking side light picking out the surface",
          lens="a level macro view, 100mm macro lens at f/8")

ROUNDS[3] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 11101,
    "note": "花鸟·第二期候选【绒心的花】：底座腾出花心 + 绒羽 P5；含同轮底座对照",
    "shots": [
        {"name": "base-flower", "seed": 11101, "prompt": _styled(FLOWER_CENTRE, [], **B2)},
        {"name": "flower-down", "seed": 11101,
         "prompt": _styled(FLOWER_CENTRE, [P5], **B2)},
        {"name": "flower-down-b", "seed": 11102,
         "prompt": _styled(FLOWER_CENTRE, [P5], **B2)},
    ],
}

B3 = dict(pose="它开在枝头、侧面朝向镜头：",
          scene="on a spring branch among new leaves",
          light="soft light against a dark background",
          lens="a level macro view, 100mm macro lens at f/8")

ROUNDS[4] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 11101,
    "note": "花鸟·第三期候选【翎梗的花】：底座 + 翎羽 P6（从花梗生出）；含同轮底座对照",
    "shots": [
        {"name": "base-flower", "seed": 11101, "prompt": _styled(FLOWER, [], **B3)},
        {"name": "flower-plume", "seed": 11101,
         "prompt": _styled(FLOWER, [P6], **B3)},
        {"name": "flower-plume-b", "seed": 11102,
         "prompt": _styled(FLOWER, [P6], **B3)},
    ],
}


# ---------------------------------------------------------------------------
# R3/R4 结论与五期重排
#
#   P5 绒羽 → 花心：⚠️ **部分成立**（花蕊被读成绒状，但不如 P6 显眼）
#   P6 翎羽 → 花梗/花轴：✅ **完整成立**（一束直立的羽翎从花心/花轴升起，非常醒目）
#   P1 羽替花瓣：❌ 0%（花瓣是典范结构）
#
# 于是花鸟的五期改排为「**翎 / 绒 / 翎+绒 × 花种**」——
# 与 fish-bird 一样：**只用落得下的部件，靠呈现与花种做出期身份**。
# ---------------------------------------------------------------------------

# 期 04 换一个花种（百合），仍用两个可用的落点
LILY_CENTRE = ("a white lily flower with six long recurved petals")
LILY = ("a white lily flower with six long recurved petals and prominent stamens")

assert " with " in LILY and " with " in LILY_CENTRE

# 期 01 定稿：翎枝的花（三个 seed）
ROUNDS[5] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 11101,
    "note": "期 01 定稿【翎枝的花】：玉兰 + 翎羽 P6（三个 seed）；晨露柔光微距；含同轮底座对照",
    "shots": [
        {"name": "base-flower", "seed": 11101, "prompt": _styled(FLOWER, [], **B1)},
        {"name": "flower-plume", "seed": 11101,
         "prompt": _styled(FLOWER, [P6], **B1)},
        {"name": "flower-plume-b", "seed": 11102,
         "prompt": _styled(FLOWER, [P6], **B1)},
        {"name": "flower-plume-c", "seed": 11103,
         "prompt": _styled(FLOWER, [P6], **B1)},
    ],
}

# 期 03 定稿：翎 + 绒（暗背景硬光）
B4 = dict(pose="它开在枝头、正面朝向镜头：",
          scene="against a dark blurred background of twigs",
          light="hard light from one side, the background falling to near-black",
          lens="a level macro view, 100mm macro lens at f/8")

ROUNDS[6] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 11101,
    "note": "期 03 定稿【翎绒俱全】：玉兰 + 翎羽 P6 + 绒羽 P5（两个 take）；暗背景硬光",
    "shots": [
        {"name": "base-flower", "seed": 11101, "prompt": _styled(FLOWER, [], **B4)},
        {"name": "flower-plume-down", "seed": 11101,
         "prompt": _styled(FLOWER, [P6, P5], **B4)},
        {"name": "flower-plume-down-b", "seed": 11102,
         "prompt": _styled(FLOWER, [P6, P5], **B4)},
    ],
}

# 期 04 定稿：百合（换花种）+ 绒 + 翎（逆光竖幅）
B5 = dict(pose="它开在枝头、侧面朝向镜头：",
          scene="on a leafy stem in a spring garden",
          light="strong backlight through the petals",
          lens="a level macro view, 100mm macro lens at f/8")

ROUNDS[7] = {
    "engine": "zimage", "size": (1024, 1280), "steps": 12, "seed": 11101,
    "note": "期 04 定稿【百合的绒与翎】：百合底座 + 绒羽 P5 + 翎羽 P6（两个 take）；逆光竖幅",
    "shots": [
        {"name": "base-flower", "seed": 11101, "prompt": _styled(LILY_CENTRE, [], **B5)},
        {"name": "lily-down-plume", "seed": 11101,
         "prompt": _styled(LILY_CENTRE, [P5, P6], **B5)},
        {"name": "lily-down-plume-b", "seed": 11102,
         "prompt": _styled(LILY_CENTRE, [P5, P6], **B5)},
    ],
}

# 期 05 收官：花鸟（广角横幅 + 满枝）
B6 = dict(pose="一枝上开着好几朵、整体朝向镜头：",
          scene="a whole flowering branch in a spring grove",
          light="warm low backlight, the plumes glowing",
          lens="a wide macro view, 45mm lens at f/11")

ROUNDS[8] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 11101,
    "note": "期 05 收官【花鸟】：玉兰 + 翎羽 P6 + 绒羽 P5（两个 take）；满枝逆光广角横幅",
    "shots": [
        {"name": "base-flower", "seed": 11101, "prompt": _styled(FLOWER, [], **B6)},
        {"name": "flower-bird", "seed": 11101,
         "prompt": _styled(FLOWER, [P6, P5], **B6)},
        {"name": "flower-bird-b", "seed": 11102,
         "prompt": _styled(FLOWER, [P6, P5], **B6)},
    ],
}


# ---------------------------------------------------------------------------
# R9：期 04（百合）补 take —— 花种一换，命中率就掉
#
# R7 里百合两张只有一张长出翎羽：**同一个写法，换花种后命中率下降**。
# 补三个 seed 把期 04 的成品凑齐；这条命中率差异如实记进 parts.md。
# ---------------------------------------------------------------------------

ROUNDS[9] = {
    "engine": "zimage", "size": (1024, 1280), "steps": 12, "seed": 11101,
    "note": "期 04 定稿（补 take）【百合的绒与翎】：百合底座 + 绒羽 P5 + 翎羽 P6（三个 seed）；含同轮底座对照",
    "shots": [
        {"name": "base-flower", "seed": 11101, "prompt": _styled(LILY_CENTRE, [], **B5)},
        {"name": "lily-down-plume", "seed": 11101,
         "prompt": _styled(LILY_CENTRE, [P5, P6], **B5)},
        {"name": "lily-down-plume-c", "seed": 11103,
         "prompt": _styled(LILY_CENTRE, [P5, P6], **B5)},
        {"name": "lily-down-plume-d", "seed": 11104,
         "prompt": _styled(LILY_CENTRE, [P5, P6], **B5)},
    ],
}
