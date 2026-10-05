"""树 + 兽子主题的 prompt 权威源与轮次定义。

概念
----
**树皮 ↔ 兽皮、根系 ↔ 足、年轮 ↔ 骨**——
「生物拼接」里**体量最大**的一组：跨越的不是物种，是**生命形态**（植物 ↔ 动物）。

底座 = **老树**（多节、树皮皲裂、粗根、巨大树干）。
供体 = 兽的部位：皮纹 K1 / 足 K2 / 角 K4。
> ~~眼 K5~~ 已删：小部件且无载体（规律 75/97）。

机制预判（按 92/96/97/99 的四问）
--------------------------------
| 部件 | 落点 | 落点性质 | 预判 |
|------|------|----------|------|
| K1 兽皮纹 | 树皮 | **属性**（纹理） | 可腾出 → 可能成（对照 cordyceps 的体表） |
| K2 足 | 根系 | 结构（根是树的器官） | 中等：需要根系作承载面 |
| K4 角 | 树干 | **空面** | 易成（从表面生出的件，规律 97） |
"""
from __future__ import annotations

PREFIX = "bs-tb"  # bio-splice / tree-beast

CN_FRAME = "全身像，一个生物体独自占据画面："

PHOTO_BASE = ("fine surface detail, natural colour, slight film grain, "
              "no digital sharpening, no text, no watermark")

# ---------------------------------------------------------------------------
# 底座：老树。两个版本按"腾出哪一处"分
#   TREE           ：树皮 + 根 + 树干都写（占用版）
#   TREE_OPEN_BARK ：不写树皮纹理（把树皮位腾给 K1）
# ---------------------------------------------------------------------------

TREE = ("an old gnarled tree with rough fissured bark, thick roots spreading over "
        "the ground and a massive trunk")
TREE_OPEN_BARK = ("an old gnarled tree with thick roots spreading over the ground "
                  "and a massive trunk")

for _n, _b in (("TREE", TREE), ("OPEN_BARK", TREE_OPEN_BARK)):
    assert " with " in _b, f"{_n}: _with 依赖「X with ...」结构"
    assert "tree" in _b and "trunk" in _b, f"{_n}: 物种名与树干是「这是树」的锚"
assert "bark" not in TREE_OPEN_BARK, "腾出版：不许写树皮"

# ---------------------------------------------------------------------------
# 移植件（只出兽的部位）
# ---------------------------------------------------------------------------

K_SKIN = "a covering of coarse tawny mammal hide"                 # K1 皮纹（覆盖式）
K_FEET = "heavy clawed mammal feet among the roots"               # K2 足
K_HORN = "a pair of massive curved mammal horns rising from the trunk"  # K4 角

for _n, _p in (("K1", K_SKIN), ("K2", K_FEET), ("K4", K_HORN)):
    assert "tree" not in _p and "trunk" not in _p or _n == "K4", f"{_n}: 移植件里尽量不出现底座词"
    assert " whose " not in _p and "body is entirely" not in _p, f"{_n}: 不许用「整只」句式"
    assert "mammal" in _p, f"{_n}: 必须点名供体类别"
    assert "eye" not in _p, f"{_n}: 眼已删（小部件且无载体）"


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
# R1（期 01 候选 · 占用版）：雾林柔光平视 —— 树皮已描述
# ---------------------------------------------------------------------------

T1 = dict(pose="它立在雾里、树干正面朝向镜头：",
          scene="deep in a misty forest, undergrowth fading into fog",
          light="soft diffused light through the mist",
          lens="a level view at eye height, 50mm lens at f/8")

ROUNDS[1] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 12101,
    "note": "树兽·第一期候选【占用版】：底座照常写树皮 + 兽皮纹 K1（含同轮底座对照）",
    "shots": [
        {"name": "base-tree", "seed": 12101, "prompt": _styled(TREE, [], **T1)},
        {"name": "tree-hide", "seed": 12101, "prompt": _styled(TREE, [K_SKIN], **T1)},
    ],
}

# ---------------------------------------------------------------------------
# R2（期 01 对照 · 腾出版）：同呈现、同 seed，只换底座写法
# ---------------------------------------------------------------------------

ROUNDS[2] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 12101,
    "note": "树兽·第一期对照【腾出版】：底座不写树皮 + 兽皮纹 K1（含同轮底座对照）",
    "shots": [
        {"name": "base-tree", "seed": 12101, "prompt": _styled(TREE_OPEN_BARK, [], **T1)},
        {"name": "tree-hide", "seed": 12101, "prompt": _styled(TREE_OPEN_BARK, [K_SKIN], **T1)},
    ],
}

# 守卫：姿态句不许提到目标部位（规律 79）
for _w in ("皮", "根", "角", "蹄", "足", "hide", "root", "horn", "foot", "feet"):
    assert _w not in T1["pose"], f"姿态句里出现了 {_w}（规律 79）"


# ---------------------------------------------------------------------------
# R1/R2 结论：**树皮是"属性"，兽皮纹可落**（腾出版更清楚）
#   R1 占用版：树皮纹理被部分替换成兽皮（A=3）
#   R2 腾出版：树干上出现一条明显的**兽皮/毛皮带**（A=4）
#   → 与 cordyceps 的体表、flytrap 的缘齿同型：**属性可以腾出**（规律 96/100）。
#
# 剩下的两个落点：
#   K2 足 → 根系（结构）：中等难度
#   K4 角 → 树干（空面）：从表面生出的件（规律 97），预期易成
# ---------------------------------------------------------------------------

# 期 02：根成足的树（泥岸 · 低机位 · 竖）
T2 = dict(pose="它长在泥岸边、露出的根系朝向镜头：",
          scene="on a muddy riverbank, the roots exposed above the water line",
          light="low morning light, long shadows across the mud",
          lens="a low view looking up the trunk, 35mm lens at f/8")

ROUNDS[3] = {
    "engine": "zimage", "size": (1024, 1280), "steps": 12, "seed": 12101,
    "note": "树兽·第二期候选【根成足的树】：老树 + 兽足 K2（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-tree", "seed": 12101, "prompt": _styled(TREE, [], **T2)},
        {"name": "tree-feet", "seed": 12101, "prompt": _styled(TREE, [K_FEET], **T2)},
        {"name": "tree-feet-b", "seed": 12102, "prompt": _styled(TREE, [K_FEET], **T2)},
    ],
}

# 期 03：有角的树（霜林 · 侧逆光 · 方）
T3 = dict(pose="它立在霜林里、树干侧面朝向镜头：",
          scene="in a frost-covered forest, bare branches around it",
          light="low side-backlight, frost glittering on the bark",
          lens="a level view at eye height, 50mm lens at f/8")

ROUNDS[4] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 12101,
    "note": "树兽·第三期候选【有角的树】：老树 + 兽角 K4（从树干生出，两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-tree", "seed": 12101, "prompt": _styled(TREE, [], **T3)},
        {"name": "tree-horns", "seed": 12101, "prompt": _styled(TREE, [K_HORN], **T3)},
        {"name": "tree-horns-b", "seed": 12102, "prompt": _styled(TREE, [K_HORN], **T3)},
    ],
}

# 期 04：皮足俱全（雨后 · 硬光 · 横）
T4 = dict(pose="它长在坡地上、树干与根系都朝向镜头：",
          scene="on a forest slope just after rain, wet leaves everywhere",
          light="hard light breaking through after the rain, crisp shadows",
          lens="a level view at eye height, 35mm lens at f/11")

ROUNDS[5] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 12101,
    "note": "树兽·第四期候选【皮足俱全】：底座不写树皮 + 兽皮纹 K1 + 兽足 K2；含同轮底座对照",
    "shots": [
        {"name": "base-tree", "seed": 12101, "prompt": _styled(TREE_OPEN_BARK, [], **T4)},
        {"name": "tree-hide-feet", "seed": 12101,
         "prompt": _styled(TREE_OPEN_BARK, [K_SKIN, K_FEET], **T4)},
        {"name": "tree-hide-feet-b", "seed": 12102,
         "prompt": _styled(TREE_OPEN_BARK, [K_SKIN, K_FEET], **T4)},
    ],
}

# 期 05（收官）：树兽（暮色林 · 逆光剪影 · 广角 · 横幅）
T5 = dict(pose="它立在暮色林里、整棵树朝向镜头：",
          scene="in a forest at dusk, the far trees lost in haze",
          light="low backlight throwing the whole tree into near-silhouette",
          lens="a wide-angle 24mm lens at eye height, f/8")

D_ALL = [K_SKIN, K_FEET, K_HORN]
assert len(D_ALL) == 3

ROUNDS[6] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 12101,
    "note": "树兽·第五期收官【树兽】：底座不写树皮 + 兽皮纹 K1 + 兽足 K2 + 兽角 K4；暮色逆光广角",
    "shots": [
        {"name": "base-tree", "seed": 12101, "prompt": _styled(TREE_OPEN_BARK, [], **T5)},
        {"name": "tree-beast", "seed": 12101,
         "prompt": _styled(TREE_OPEN_BARK, D_ALL, **T5)},
        {"name": "tree-beast-b", "seed": 12102,
         "prompt": _styled(TREE_OPEN_BARK, D_ALL, **T5)},
    ],
}


# ---------------------------------------------------------------------------
# R3–R6 判读结论（**含一条否定结论**）
#
#   ✅ K1 兽皮纹：树干上出现明显的兽皮/毛皮带（腾出版更清楚）
#   ❌ **K2 兽足：0% 落地** —— 根系区放大后只有形状漂移，根还是根
#        → 与 dragon-nines 的鹰爪同型：**「足」需要一个关节/肢体结构，树没有**
#          （规律 74 载体结构 + 97 承载面）
#   ✅ K4 兽角：树干上长出一对巨大的弯角，非常清楚（林下霜林两轮都成）
#
# 于是重排五期（与 fish-bird / flower-bird 同样的处置）：
#   01 兽皮的树（K1）
#   02 有角的树（K4）
#   03 皮角俱全（K1+K4）
#   04 枯木的皮与角（**换树**，验证 102）
#   05 树兽（收官，K1+K4[+K2 保留写法但预期不落]）
# ---------------------------------------------------------------------------

DEAD_TREE = ("a dead standing tree with a splintered bare trunk and exposed roots")
assert " with " in DEAD_TREE and "tree" in DEAD_TREE

# 期 01 定稿：兽皮的树（腾出版，三个 seed）
ROUNDS[7] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 12101,
    "note": "期 01 定稿【兽皮的树】：底座不写树皮 + 兽皮纹 K1（三个 seed）；含同轮底座对照",
    "shots": [
        {"name": "base-tree", "seed": 12101, "prompt": _styled(TREE_OPEN_BARK, [], **T1)},
        {"name": "tree-hide", "seed": 12101, "prompt": _styled(TREE_OPEN_BARK, [K_SKIN], **T1)},
        {"name": "tree-hide-b", "seed": 12102, "prompt": _styled(TREE_OPEN_BARK, [K_SKIN], **T1)},
        {"name": "tree-hide-c", "seed": 12103, "prompt": _styled(TREE_OPEN_BARK, [K_SKIN], **T1)},
    ],
}

# 期 03：皮角俱全（雨后 · 硬光 · 横）
ROUNDS[8] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 12101,
    "note": "期 03 定稿【皮角俱全】：底座不写树皮 + 兽皮纹 K1 + 兽角 K4（两个 take）；雨后硬光横",
    "shots": [
        {"name": "base-tree", "seed": 12101, "prompt": _styled(TREE_OPEN_BARK, [], **T4)},
        {"name": "tree-hide-horns", "seed": 12101,
         "prompt": _styled(TREE_OPEN_BARK, [K_SKIN, K_HORN], **T4)},
        {"name": "tree-hide-horns-b", "seed": 12102,
         "prompt": _styled(TREE_OPEN_BARK, [K_SKIN, K_HORN], **T4)},
    ],
}

# 期 04：枯木的皮与角（换树 · 霜晨 · 方）
T6 = dict(pose="它立在霜晨的空地上、树干正面朝向镜头：",
          scene="standing dead in a clearing on a frosty morning",
          light="cold flat light, frost on every surface",
          lens="a level view at eye height, 50mm lens at f/8")

ROUNDS[9] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 12101,
    "note": "期 04 定稿【枯木的皮与角】：**换底座（枯立木）** + 兽皮纹 K1 + 兽角 K4（两个 take）",
    "shots": [
        {"name": "base-tree", "seed": 12101, "prompt": _styled(DEAD_TREE, [], **T6)},
        {"name": "deadwood-hide-horns", "seed": 12101,
         "prompt": _styled(DEAD_TREE, [K_SKIN, K_HORN], **T6)},
        {"name": "deadwood-hide-horns-b", "seed": 12102,
         "prompt": _styled(DEAD_TREE, [K_SKIN, K_HORN], **T6)},
    ],
}
