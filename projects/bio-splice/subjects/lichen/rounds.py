"""地衣（真菌 + 藻）子主题的 prompt 权威源与轮次定义。

概念
----
**地衣本身就是一种拼接生物**——真菌菌丝 + 藻/蓝细菌的共生体。
这是「生物拼接」**最本体的例子**：自然界已经把这件事拼好了，
我们只是把它拍出来。

所以这个子主题与前面五个**都不一样**：
- 前五个是"给动物加一个外来部件"，本子主题是"**把已经拼好的共生体呈现出来**"；
- 底座不是动物，而是**真菌菌丝体**；供体是**藻**（绿色细胞 / 藻丝）
  与**地衣形态**（壳状 / 叶状 / 枝状）。

机制预测（依据本仓已实测的规律）
--------------------------------
- 规律 67/90/91：**形态**（壳状/叶状/枝状）是本子主题的"不同形、高辨识度"件 →
  按 91 应当最容易成；**绿色藻细胞**是跨域材质 → 按 67 属"同材质/新材料"档，待测。
- 规律 85：生境必须兼容——地衣长在**岩面 / 树皮**上，所以每个期的场景都用岩面、树皮、冻原。
- 尺度问题：这是**微距**题材（几厘米的生物），所以
  取景句换成「微距特写」、摄影层换成 `macro photograph, focus-stacked`，
  不复用动物子主题的「全身像 + 600mm 长焦」。
"""
from __future__ import annotations

PREFIX = "bs-lc"  # bio-splice / lichen

# ---------------------------------------------------------------------------
# 本子主题的恒定层：微距取景句 + 显微/生态摄影底子
# ---------------------------------------------------------------------------

CN_FRAME = "微距特写，一个生物体独自占据画面："

PHOTO_BASE = ("macro photograph, focus-stacked, fine surface detail, natural colour, "
              "no digital sharpening, no text, no watermark")

# ---------------------------------------------------------------------------
# 底座：真菌菌丝体（不写形态、不写颜色 —— 把这两处留给移植件）
# ---------------------------------------------------------------------------

FULL_MYCELIUM = ("a dense mat of pale fungal mycelium with fine branching threads "
                 "and a soft dusty surface")

assert " with " in FULL_MYCELIUM, "_with 依赖「X with ...」结构"
assert "lichen" not in FULL_MYCELIUM, "底座不许点名地衣（那是移植后的形态）"
assert "green" not in FULL_MYCELIUM and "alga" not in FULL_MYCELIUM, "绿色要留给藻件"

# ---------------------------------------------------------------------------
# 移植件
#   形态件：壳状 CR1 / 叶状 FL1 / 枝状 FR1
#   藻件： 绿色细胞 AL1 / 藻丝 AL2
# ---------------------------------------------------------------------------

CRUST = "a hard crustose lichen crust with a cracked areolate surface"
FOLIOSE = "leafy foliose lichen lobes with pale rims"
FRUTICOSE = "branching fruticose lichen tufts standing up like tiny shrubs"
ALGAE_CELLS = "clusters of bright green algal cells"
ALGAE_FILAMENTS = "fine bright green algal filaments woven through the surface"

for _n, _p in (("CR1", CRUST), ("FL1", FOLIOSE), ("FR1", FRUTICOSE),
               ("AL1", ALGAE_CELLS), ("AL2", ALGAE_FILAMENTS)):
    assert "mycelium" not in _p, f"{_n}: 移植件里不该出现底座"
    assert " whose " not in _p and "body is entirely" not in _p, f"{_n}: 不许用「整只」句式"
    assert len(_p.split()) >= 6, f"{_n}: 部位描述太短，容易被当成一个词丢掉"


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
# R1（期 01 候选）：壳状地衣 —— 一次把单件与组合都测掉
#   底座对照 / 形态件 CR1 / 藻件 AL1 / 形态 + 藻（真正的共生体）
# ---------------------------------------------------------------------------

L1 = dict(pose="它铺在岩面上、表面朝向镜头：",
          scene="on a bare granite rock face",
          light="raking side light that picks out every crack in the surface",
          lens="a level macro view, 100mm macro lens at f/8")

ROUNDS[1] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 8101,
    "note": "地衣·第一期候选：菌丝体底座 + 壳状形态 CR1 / 绿色藻细胞 AL1（含同轮底座对照）",
    "shots": [
        {"name": "base-mycelium", "seed": 8101, "prompt": _styled(FULL_MYCELIUM, [], **L1)},
        {"name": "mycelium-crust", "seed": 8101,
         "prompt": _styled(FULL_MYCELIUM, [CRUST], **L1)},
        {"name": "mycelium-algae", "seed": 8101,
         "prompt": _styled(FULL_MYCELIUM, [ALGAE_CELLS], **L1)},
        {"name": "mycelium-crust-algae", "seed": 8101,
         "prompt": _styled(FULL_MYCELIUM, [CRUST, ALGAE_CELLS], **L1)},
    ],
}

# 守卫：姿态句不许提到目标部位（规律 79）
for _w in ("壳", "藻", "绿", "crust", "alga", "green", "leafy", "branch"):
    assert _w not in L1["pose"], f"姿态句里出现了 {_w}（规律 79）"


# ---------------------------------------------------------------------------
# R1 结论：本子主题是本项目**第一次跨域件 100% 落地**
#
#   底座（菌丝体）是一团**先验很弱**的东西 → 形态件与藻件都能长上去，
#   与 deer-crane（鹿颈/鹿腿是典范结构）形成最鲜明的对照：
#   **底座越"没有固定形状"，移植件越容易落地**（规律 92）。
#
# R2–R5：把剩下四期一次做完
#   02 叶状地衣（树皮 · 湿润 · 侧俯）
#   03 枝状地衣（冻原 · 逆光 · 低机位竖幅）
#   04 藻层可见（拟剖面 · 环形光 · 深景深）
#   05 共生体（雾林 · 散射光 · 广角横幅，收官）
# ---------------------------------------------------------------------------

# 期 02：树皮 · 湿润 · 微距侧俯
L2 = dict(pose="它贴在树皮上、表面斜向镜头：",
          scene="on the wet bark of an old tree trunk",
          light="soft wet light with a faint sheen on the surface",
          lens="a macro view from slightly above, 100mm macro lens at f/8")

ROUNDS[2] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 8101,
    "note": "地衣·第二期候选：菌丝体底座 + 叶状体 FL1 / 藻丝 AL2（含同轮底座对照）",
    "shots": [
        {"name": "base-mycelium", "seed": 8101, "prompt": _styled(FULL_MYCELIUM, [], **L2)},
        {"name": "mycelium-foliose", "seed": 8101,
         "prompt": _styled(FULL_MYCELIUM, [FOLIOSE], **L2)},
        {"name": "mycelium-foliose-algae", "seed": 8102,
         "prompt": _styled(FULL_MYCELIUM, [FOLIOSE, ALGAE_FILAMENTS], **L2)},
    ],
}

# 期 03：冻原 · 逆光 · 低机位 · 竖
L3 = dict(pose="它立在冻原的石面上、整体朝向镜头：",
          scene="on a frost-covered stone in open tundra",
          light="low backlight through ice fog, rimming every tip",
          lens="a low three-quarter macro view, 90mm macro lens at f/8")

ROUNDS[3] = {
    "engine": "zimage", "size": (1024, 1280), "steps": 12, "seed": 8101,
    "note": "地衣·第三期候选：菌丝体底座 + 枝状体 FR1（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-mycelium", "seed": 8101, "prompt": _styled(FULL_MYCELIUM, [], **L3)},
        {"name": "mycelium-fruticose", "seed": 8101,
         "prompt": _styled(FULL_MYCELIUM, [FRUTICOSE], **L3)},
        {"name": "mycelium-fruticose-b", "seed": 8103,
         "prompt": _styled(FULL_MYCELIUM, [FRUTICOSE], **L3)},
    ],
}

# 期 04：拟剖面 · 环形光 · 深景深（把"藻层"当主体）
L4 = dict(pose="它的表层被掀开、露出内部结构：",
          scene="as if in cross-section, the upper cortex lifted away",
          light="ring light, deep even depth of field, everything in focus",
          lens="a flat-on macro view, 100mm macro lens at f/16")

ROUNDS[4] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 8101,
    "note": "地衣·第四期候选【藻层可见】：菌丝体底座 + 绿色细胞 AL1 + 藻丝 AL2（拟剖面）；含同轮底座对照",
    "shots": [
        {"name": "base-mycelium", "seed": 8101, "prompt": _styled(FULL_MYCELIUM, [], **L4)},
        {"name": "mycelium-algal-layer", "seed": 8101,
         "prompt": _styled(FULL_MYCELIUM, [ALGAE_CELLS, ALGAE_FILAMENTS], **L4)},
        {"name": "mycelium-algal-layer-b", "seed": 8102,
         "prompt": _styled(FULL_MYCELIUM, [ALGAE_CELLS, ALGAE_FILAMENTS], **L4)},
    ],
}

# 期 05：雾林 · 散射光 · 广角 · 横幅（收官：三种形态 + 藻）
L5 = dict(pose="它铺在林地上的石面上、整体展开：",
          scene="on a mossy boulder in a misty forest, the background dissolving into fog",
          light="soft scattered light, no hard shadows",
          lens="a wide macro view, 45mm lens at f/11")

D_ALL = [CRUST, FOLIOSE, FRUTICOSE]
D_ALL_ALGAE = [FOLIOSE, FRUTICOSE, ALGAE_CELLS]

assert len(D_ALL) == 3 and len(D_ALL_ALGAE) == 3

ROUNDS[5] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 8101,
    "note": "地衣·第五期收官【共生体】：菌丝体底座 + 三种形态 / 两种形态+藻（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-mycelium", "seed": 8101, "prompt": _styled(FULL_MYCELIUM, [], **L5)},
        {"name": "mycelium-3forms", "seed": 8101,
         "prompt": _styled(FULL_MYCELIUM, D_ALL, **L5)},
        {"name": "mycelium-forms-algae", "seed": 8102,
         "prompt": _styled(FULL_MYCELIUM, D_ALL_ALGAE, **L5)},
    ],
}
