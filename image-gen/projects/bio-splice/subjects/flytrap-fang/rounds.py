"""捕蝇草 + 动物器官子主题的 prompt 权威源与轮次定义。

概念
----
**植物长出动物的器官**（牙 / 眼 / 舌）——「生物拼接」里最有冲击力的方向：
跨越的不是物种，**是界**（植物界 ↔ 动物界）。

底座 = **捕蝇草**（形态很定型：两片夹子 + 边缘硬齿 + 红色内面）。
供体 = 动物的部位：兽牙 T1 / 眼 T2 / 舌 T4。

> ~~爪 T3~~ 已删：捕蝇草没有四肢，没有承载结构（规律 74/97）。

机制预判（按 92/96/97 的"三问"）
--------------------------------
1. **底座形态自由度**：捕蝇草**很低**（它的夹子与硬齿非常定型）→ 规律 92 不利。
2. **要腾的那一处是结构还是属性**：叶缘硬齿是**结构**（夹子的解剖一部分）→
   按规律 96，腾出多半无效，预期只到部分。
3. **承载面**：眼与舌需要的承载面是**叶面**与**夹子内腔**——
   这两处在捕蝇草上都是"空面"，所以它们反而比"牙"更有机会（规律 97）。

这也是乙组里**最难的一个**，本轮把三条一次测清。
"""
from __future__ import annotations

PREFIX = "bs-ff"  # bio-splice / flytrap-fang

CN_FRAME = "微距特写，一个生物体独自占据画面："

PHOTO_BASE = ("macro photograph, focus-stacked, fine surface detail, natural colour, "
              "no digital sharpening, no text, no watermark")

# ---------------------------------------------------------------------------
# 底座：捕蝇草。三个版本按"腾出哪一处"分
#   FLYTRAP      ：照常写硬齿（占用版，用于与腾出版对照）
#   FLYTRAP_OPEN ：不写硬齿（腾出版）
#   FLYTRAP_LEAF ：写宽叶面、不写硬齿（给"叶面上的眼"用）
# ---------------------------------------------------------------------------

FLYTRAP = ("a Venus flytrap with two wide-open trap lobes, a red inner surface "
           "and a fringe of stiff marginal teeth")
FLYTRAP_OPEN = ("a Venus flytrap with two wide-open trap lobes and a red inner surface")
FLYTRAP_LEAF = ("a Venus flytrap with broad flat leaf blades and two wide-open trap lobes "
                "with a red inner surface")

for _n, _b in (("FLYTRAP", FLYTRAP), ("OPEN", FLYTRAP_OPEN), ("LEAF", FLYTRAP_LEAF)):
    assert " with " in _b, f"{_n}: _with 依赖「X with ...」结构"
    assert "flytrap" in _b, f"{_n}: 物种名是「这是捕蝇草」的锚"
assert "teeth" not in FLYTRAP_OPEN and "teeth" not in FLYTRAP_LEAF, "腾出版不许写硬齿"

# ---------------------------------------------------------------------------
# 移植件（只出动物的部位）
# ---------------------------------------------------------------------------

T_FANG = "a row of sharp white mammal fangs along the trap edges"        # T1 牙
T_EYE = "a glossy dark animal eye on the leaf blade"                     # T2 眼
T_TONGUE = "a long pink mammal tongue curling out of the trap"           # T4 舌

for _n, _p in (("T1", T_FANG), ("T2", T_EYE), ("T4", T_TONGUE)):
    assert "flytrap" not in _p and "plant" not in _p, f"{_n}: 移植件里不该出现底座"
    assert " whose " not in _p and "body is entirely" not in _p, f"{_n}: 不许用「整只」句式"
    assert "mammal" in _p or "animal" in _p, f"{_n}: 必须点名供体类别"
    assert "claw" not in _p and "paw" not in _p, f"{_n}: 爪已删（无承载结构）"


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
# R1（期 01 候选 · 占用版）：沼泽 · 侧逆光 · 微距 100mm · 方
# ---------------------------------------------------------------------------

F1 = dict(pose="它张着夹子、内面朝向镜头：",
          scene="in a sphagnum bog among wet moss",
          light="raking side-backlight, the red inner surface glowing",
          lens="a level macro view, 100mm macro lens at f/8")

ROUNDS[1] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 10101,
    "note": "捕蝇草·第一期候选【占用版】：底座照常写硬齿 + 兽牙 T1（含同轮底座对照）",
    "shots": [
        {"name": "base-flytrap", "seed": 10101, "prompt": _styled(FLYTRAP, [], **F1)},
        {"name": "flytrap-fangs", "seed": 10101,
         "prompt": _styled(FLYTRAP, [T_FANG], **F1)},
    ],
}

# ---------------------------------------------------------------------------
# R2（期 01 对照 · 腾出版）：同一呈现、同一 seed、只换底座写法
# ---------------------------------------------------------------------------

ROUNDS[2] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 10101,
    "note": "捕蝇草·第一期对照【腾出版】：底座不写硬齿 + 兽牙 T1（含同轮底座对照）",
    "shots": [
        {"name": "base-flytrap", "seed": 10101, "prompt": _styled(FLYTRAP_OPEN, [], **F1)},
        {"name": "flytrap-fangs", "seed": 10101,
         "prompt": _styled(FLYTRAP_OPEN, [T_FANG], **F1)},
    ],
}

# 守卫：姿态句不许提到目标部位（规律 79）
for _w in ("牙", "齿", "眼", "舌", "fang", "tooth", "teeth", "eye", "tongue"):
    assert _w not in F1["pose"], f"姿态句里出现了 {_w}（规律 79）"


# ---------------------------------------------------------------------------
# R1/R2 结论与定稿安排
#
#   R1【占用版】：底座自带细长的缘齿 → 兽牙句把缘齿变成**粗白三角獠牙**（A=4）
#   R2【腾出版】：底座不写缘齿 → 兽牙句在**光秃的夹子边缘**排出一列獠牙（A=5）
#
#   → 缘齿属"**属性**"而非"结构"：它是一条边缘的形态，删掉不影响"这是捕蝇草"
#     （规律 96 的延伸：**边界性的附属物 ≈ 属性**，可以腾出）。
#   → 期 01 定稿用腾出版。
#
# 期 02–05 用 FLYTRAP_LEAF（宽叶面 + 不写缘齿）：
#   眼需要"叶面"这个承载面、舌需要"夹子内腔"，两者都是空面（规律 97）。
# ---------------------------------------------------------------------------

# 期 01 定稿（腾出版 · 三个 seed）
ROUNDS[3] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 10101,
    "note": "期 01 定稿【有牙的捕蝇草】：底座不写缘齿 + 兽牙 T1（三个 seed）；含同轮底座对照",
    "shots": [
        {"name": "base-flytrap", "seed": 10101, "prompt": _styled(FLYTRAP_OPEN, [], **F1)},
        {"name": "flytrap-fangs", "seed": 10101,
         "prompt": _styled(FLYTRAP_OPEN, [T_FANG], **F1)},
        {"name": "flytrap-fangs-b", "seed": 10102,
         "prompt": _styled(FLYTRAP_OPEN, [T_FANG], **F1)},
        {"name": "flytrap-fangs-c", "seed": 10103,
         "prompt": _styled(FLYTRAP_OPEN, [T_FANG], **F1)},
    ],
}

# 期 02：叶面上的眼（平视叶面 · 方）
F2 = dict(pose="它把宽叶面朝向镜头、夹子在后：",
          scene="in a sphagnum bog among wet moss",
          light="flat overcast light, no glare on the leaf",
          lens="a flat-on macro view of the leaf blade, 100mm macro lens at f/11")

ROUNDS[4] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 10101,
    "note": "期 02 定稿【有眼的捕蝇草】：宽叶面底座 + 眼 T2（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-flytrap", "seed": 10101, "prompt": _styled(FLYTRAP_LEAF, [], **F2)},
        {"name": "flytrap-eye", "seed": 10101,
         "prompt": _styled(FLYTRAP_LEAF, [T_EYE], **F2)},
        {"name": "flytrap-eye-b", "seed": 10102,
         "prompt": _styled(FLYTRAP_LEAF, [T_EYE], **F2)},
    ],
}

# 期 03：夹子里的舌（苔藓 · 低机位 · 竖）
F3 = dict(pose="它张着夹子、内腔朝向镜头：",
          scene="low among wet moss, the trap opening facing the camera",
          light="soft light falling into the open trap",
          lens="a low macro view looking into the trap, 100mm macro lens at f/8")

ROUNDS[5] = {
    "engine": "zimage", "size": (1024, 1280), "steps": 12, "seed": 10101,
    "note": "期 03 定稿【吐信的捕蝇草】：宽叶面底座 + 舌 T4（两个 take）；苔藓低机位竖幅",
    "shots": [
        {"name": "base-flytrap", "seed": 10101, "prompt": _styled(FLYTRAP_LEAF, [], **F3)},
        {"name": "flytrap-tongue", "seed": 10101,
         "prompt": _styled(FLYTRAP_LEAF, [T_TONGUE], **F3)},
        {"name": "flytrap-tongue-b", "seed": 10102,
         "prompt": _styled(FLYTRAP_LEAF, [T_TONGUE], **F3)},
    ],
}

# 期 04：牙舌俱全（雨后 · 硬侧光 · 方）
F4 = dict(pose="它张着夹子、内面朝向镜头：",
          scene="in a bog just after rain, water beading on the lobes",
          light="hard side light after the rain, crisp shadows",
          lens="a level macro view, 100mm macro lens at f/11")

ROUNDS[6] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 10101,
    "note": "期 04 定稿【牙舌俱全】：底座不写缘齿 + 兽牙 T1 + 舌 T4（两个 take）；雨后硬侧光",
    "shots": [
        {"name": "base-flytrap", "seed": 10101, "prompt": _styled(FLYTRAP_OPEN, [], **F4)},
        {"name": "flytrap-fangs-tongue", "seed": 10101,
         "prompt": _styled(FLYTRAP_OPEN, [T_FANG, T_TONGUE], **F4)},
        {"name": "flytrap-fangs-tongue-b", "seed": 10102,
         "prompt": _styled(FLYTRAP_OPEN, [T_FANG, T_TONGUE], **F4)},
    ],
}

# 期 05（收官）：食肉植物（晨雾沼泽 · 逆光 · 广角 · 横幅）
F5 = dict(pose="一整丛捕蝇草张着夹子、朝向镜头：",
          scene="in a misty bog at dawn, several traps in the frame",
          light="low backlight through the mist, the red inner surfaces glowing",
          lens="a wide macro view, 45mm lens at f/11")

D_ALL = [T_FANG, T_EYE, T_TONGUE]
assert len(D_ALL) == 3

ROUNDS[7] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 10101,
    "note": "期 05 收官【食肉植物】：宽叶面底座 + 兽牙 T1 + 眼 T2 + 舌 T4；晨雾沼泽逆光广角横幅",
    "shots": [
        {"name": "base-flytrap", "seed": 10101, "prompt": _styled(FLYTRAP_LEAF, [], **F5)},
        {"name": "flytrap-all3", "seed": 10101,
         "prompt": _styled(FLYTRAP_LEAF, D_ALL, **F5)},
        {"name": "flytrap-all3-b", "seed": 10102,
         "prompt": _styled(FLYTRAP_LEAF, D_ALL, **F5)},
    ],
}
