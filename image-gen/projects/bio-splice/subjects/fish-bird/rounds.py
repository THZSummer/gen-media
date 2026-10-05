"""鱼 + 鸟（鲲鹏）子主题的 prompt 权威源与轮次定义。

概念
----
**《庄子·逍遥游》：北冥有鱼…化而为鸟**——典籍里明写的形态转换。
所以这个子主题的钩子是**一次形态转换**：鱼的躯干上长出鸟的飞行件。

底座 = **大鱼**（鲤）。
供体 = 鸟的飞行件：翼 B1 / 尾羽 B2 / 羽 B5。

> ~~喙 B3 / 爪 B4~~ 已删：喙是头部件（规律 73），鱼没有四肢（规律 74）。

机制预测（依据本仓已实测的规律）
--------------------------------
- 规律 62/74：**部位需要载体结构**。鱼**有**胸鳍与尾鳍，所以翼与尾羽是
  "近位结构"——比 cat-eagle 的猫掌（脚被鹰爪占住）更有机会；
  但底座描述里如果写明了鳍，就会按规律 56 把位置占住 → 需要**腾出占位**。
- 规律 83：腾出占位能否成立，取决于**底座对该部位的依赖程度**。
  鱼鳍删掉不太伤"这是鱼"的判断（还有鳞、体形、头），所以这里值得一试。
- 规律 81：**空间关系从句失效** → 不用 `in place of its pectoral fins` 这种写法，
  改用 `on both sides of its body` 这类直白的位置短语（本轮同时验证这一条）。
- 规律 79：姿态句不许提「翼」「翅」「尾」「鳍」。
"""
from __future__ import annotations

PREFIX = "bs-fb"  # bio-splice / fish-bird

CN_FRAME = "全身像，一只动物独自占据画面："

PHOTO_BASE = ("fine surface detail, slight film grain, no digital sharpening, "
              "no text, no watermark")

# ---------------------------------------------------------------------------
# 三个底座：按"腾出哪一处"分。鱼鳞、体形、头始终保留——它们是"这是鱼"的锚。
#   FISH_NO_PAIRED：不写成对的鳍（把胸鳍位腾给 B1）
#   FISH_NO_TAIL  ：不写尾鳍（把尾位腾给 B2）
#   FISH_BARE     ：两处都不写（给 B1+B2 叠加用）
# ---------------------------------------------------------------------------

FISH_NO_PAIRED = ("a large wild carp with a long scaled body, a blunt head, small eyes, "
                  "a dorsal fin and a broad forked tail")
FISH_NO_TAIL = ("a large wild carp with a long scaled body, a blunt head, small eyes "
                "and four fins")
FISH_BARE = ("a large wild carp with a long scaled body, a blunt head, small eyes "
             "and a dorsal fin")

for _n, _b in (("NO_PAIRED", FISH_NO_PAIRED), ("NO_TAIL", FISH_NO_TAIL), ("BARE", FISH_BARE)):
    assert " with " in _b, f"{_n}: _with 依赖「X with ...」结构"
    assert "carp" in _b and "scaled body" in _b, f"{_n}: 鳞与体形是「这是鱼」的锚，不能删"
assert "fin" not in FISH_NO_PAIRED.split(",")[-1] or "dorsal fin" in FISH_NO_PAIRED
assert "forked tail" not in FISH_NO_TAIL and "forked tail" not in FISH_BARE
assert "four fins" not in FISH_BARE.split("with")[1]

# ---------------------------------------------------------------------------
# 移植件（只出部位，绝不写成"整只鸟"）
# ---------------------------------------------------------------------------

B_WING = "broad feathered bird wings on both sides of its body"          # B1 位置短语
B_WING_REL = "broad feathered bird wings in place of its pectoral fins"  # B1 关系从句（对照）
B_WING_FLANK = "a pair of broad feathered bird wings along its flanks"   # B1 另一种位置短语
B_TAIL = "a fan of long bird tail feathers"                              # B2
B_TAIL_REL = "long bird tail feathers spreading where the tail fin would be"  # B2 关系从句
B_COAT = "a covering of fine bird feathers over its back"                # B5 覆体

for _n, _p in (("B1", B_WING), ("B1rel", B_WING_REL), ("B1flank", B_WING_FLANK),
               ("B2", B_TAIL), ("B2rel", B_TAIL_REL), ("B5", B_COAT)):
    assert "carp" not in _p and "fish" not in _p, f"{_n}: 移植件里不该出现底座动物"
    assert " whose " not in _p and "body is entirely" not in _p, f"{_n}: 不许用「整只」句式"
    assert "bird" in _p, f"{_n}: 必须点名供体"
    assert "beak" not in _p and "claw" not in _p, f"{_n}: 喙/爪已删（规律 73/74）"


def _with(base: str, parts: list[str]) -> str:
    head, _, rest = base.partition(" with ")
    return f"{head} with {' and '.join(parts)}, {rest}"


def _styled(base: str, parts: list[str], *, frame: str = CN_FRAME, pose: str,
            scene: str, light: str, lens: str) -> str:
    core = _with(base, parts) if parts else base
    return (f"{frame}{pose}{core}. {scene}. {light}. "
            f"Photograph, {lens}, {PHOTO_BASE}.")


ARCHIVE_LAYERS = f"{CN_FRAME}<姿态><底座 with 部位>. <生境>. <光线>. Photograph, <镜头>, {PHOTO_BASE}."

ROUNDS: dict[int, dict] = {}

# ---------------------------------------------------------------------------
# R1（期 01 候选）：有翅的鱼 —— 三种写法同轮对比
#   位置短语 ×2 + 关系从句 ×1，用来同时验两条：
#     ① 腾出占位的底座上，翼能不能长出来
#     ② 位置短语与关系从句哪个落地（规律 81 在"替代"语义上的复验）
# ---------------------------------------------------------------------------

F1 = dict(pose="它悬停在水中、侧身朝向镜头：",
          scene="in shallow clear water over pale gravel",
          light="soft side light through the water",
          lens="a level view from the side, 100mm lens at f/5.6, the whole body in frame")

ROUNDS[1] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 6101,
    "note": "鲲鹏·第一期候选：鱼底座（腾出胸鳍位）+ 鸟翼的三种写法；含同轮底座对照",
    "shots": [
        {"name": "base-fish", "seed": 6101, "prompt": _styled(FISH_NO_PAIRED, [], **F1)},
        {"name": "fish-wings", "seed": 6101,
         "prompt": _styled(FISH_NO_PAIRED, [B_WING], **F1)},
        {"name": "fish-wings-flank", "seed": 6101,
         "prompt": _styled(FISH_NO_PAIRED, [B_WING_FLANK], **F1)},
        {"name": "fish-wings-rel", "seed": 6101,
         "prompt": _styled(FISH_NO_PAIRED, [B_WING_REL], **F1)},
    ],
}

# ---------------------------------------------------------------------------
# R2（期 02 候选）：羽尾的鱼 —— 底座换成"腾出尾鳍"的那一个
#   关系从句 vs 名词短语，再验一次规律 81。
# ---------------------------------------------------------------------------

F2 = dict(pose="它悬在水中、身侧朝向镜头：",
          scene="in dark water a little below the surface",
          light="backlight coming down through the surface",
          lens="a level view from the side, 100mm lens at f/5.6, the whole body in frame")

ROUNDS[2] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 6101,
    "note": "鲲鹏·第二期候选：鱼底座（腾出尾鳍位）+ 鸟尾羽的两种写法；含同轮底座对照",
    "shots": [
        {"name": "base-fish", "seed": 6101, "prompt": _styled(FISH_NO_TAIL, [], **F2)},
        {"name": "fish-tailfeathers", "seed": 6101,
         "prompt": _styled(FISH_NO_TAIL, [B_TAIL], **F2)},
        {"name": "fish-tailfeathers-rel", "seed": 6101,
         "prompt": _styled(FISH_NO_TAIL, [B_TAIL_REL], **F2)},
    ],
}

# 守卫：姿态句不许提到目标部位（规律 79）
for _t in (F1, F2):
    for _w in ("翼", "翅", "尾", "鳍", "wing", "tail", "fin", "feather"):
        assert _w not in _t["pose"], f"姿态句里出现了 {_w}（规律 79）"


# ---------------------------------------------------------------------------
# R3：R1/R2 全灭之后的追问 —— **不要去抢鱼鳍的位置，改长在空位上**
#
# R1/R2 实测：把胸鳍/尾鳍的描述删掉（腾出占位）之后，
#   翼 ❌ 0% 落地、尾羽 ❌ 0% 落地，三种写法（位置短语 ×2 + 关系从句）全都没用；
#   而且鱼自己把鳍又长了回来（典范结构会被模型补回，同规律 83 的"高依赖"档）。
#
# 结论：**鱼鳍不是"腾得出"的占位，它是鱼的典范结构**（同 cat-eagle 的猫掌、dragon-nines 的蛇鳞）。
#
# 换一个思路（这是 wing-atlas 改写与 cat-eagle 期 05「颈羽」都验证过的）：
#   **不在被占住的位置上硬来，把件长在空位上。**
#   鱼的背脊上方、尾鳍上方都是空的 → 翼改成"从背上生出"、尾羽改成"在尾之上张开"。
#
# 本轮统一用 FISH_BARE（胸鳍与尾都不描述）作为底座，三个探针 + 一个对照，
# 满足规律 76（一轮一个底座）。
# ---------------------------------------------------------------------------

B_WING_BACK = "a pair of broad feathered bird wings rising from its back"
B_TAIL_ABOVE = "a fan of long bird tail feathers rising above its tail"

assert "carp" not in B_WING_BACK + B_TAIL_ABOVE and "fish" not in B_WING_BACK + B_TAIL_ABOVE
assert "bird" in B_WING_BACK and "bird" in B_TAIL_ABOVE

ROUNDS[3] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 6101,
    "note": "鲲鹏·空位探针：翼从背上生出 / 尾羽在尾之上张开 / 羽覆背（同一底座）；含同轮底座对照",
    "shots": [
        {"name": "base-fish", "seed": 6101, "prompt": _styled(FISH_BARE, [], **F1)},
        {"name": "fish-wings-back", "seed": 6101,
         "prompt": _styled(FISH_BARE, [B_WING_BACK], **F1)},
        {"name": "fish-tail-above", "seed": 6101,
         "prompt": _styled(FISH_BARE, [B_TAIL_ABOVE], **F1)},
        {"name": "fish-feathercoat", "seed": 6101,
         "prompt": _styled(FISH_BARE, [B_COAT], **F1)},
    ],
}


# ---------------------------------------------------------------------------
# R4：第三个假设 —— **部件与生境的语义冲突**
#
# R1/R2/R3 七张全部 0%：翼（胸鳍位 / 背上方）、尾羽（尾位 / 尾上方）、羽覆背，
# 在水下的场景里一件都没落地。
#
# 对比本仓成功的例子：蛇 + 鹿角、龟 + 蛇颈、猫 + 鹰翼——它们的生境
# （芦苇/溪石/林地）与移植件**不冲突**。
# 而"羽毛/翅膀"在水下是**语义矛盾**的：鸟的飞行件不该出现在水里。
# 假设：模型把场景当强约束，**冲突时宁可丢掉部件也要保住场景**。
#
# 测法：把同一个鱼底座放到**水面之上**（跃出水面、水花四溅），重跑同样的三个部件。
# 如果这时落地了 → 假设成立，fish-bird 的呈现必须改到"离水"场景。
# ---------------------------------------------------------------------------

F4 = dict(pose="它跃出水面、身体完全离水：",
          scene="in open air above the water surface, spray falling away below it",
          light="backlight through the flying spray",
          lens="a level view from the side, 100mm lens at f/5.6, the whole body in frame")

assert all(_w not in F4["pose"] for _w in ("翼", "翅", "尾", "鳍", "wing", "tail", "fin"))

ROUNDS[4] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 6101,
    "note": "鲲鹏·离水探针：同样的鱼底座 + 同样的三个部件，只把场景换到水面之上；含同轮底座对照",
    "shots": [
        {"name": "base-fish", "seed": 6101, "prompt": _styled(FISH_BARE, [], **F4)},
        {"name": "fish-wings-back", "seed": 6101,
         "prompt": _styled(FISH_BARE, [B_WING_BACK], **F4)},
        {"name": "fish-wings", "seed": 6101,
         "prompt": _styled(FISH_BARE, [B_WING], **F4)},
        {"name": "fish-feathercoat", "seed": 6101,
         "prompt": _styled(FISH_BARE, [B_COAT], **F4)},
    ],
}


# ---------------------------------------------------------------------------
# R5：离水场景下把剩下的部件补齐
#
# R4 已证明：**水面之上，翼立即落地**（背上生出的翼、体侧的翼都成）。
# 本轮把尾羽、羽覆背、翼+尾羽叠加补齐——全部用同一个离水场景与底座。
# ---------------------------------------------------------------------------

ROUNDS[5] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 6101,
    "note": "鲲鹏·离水补齐：尾羽（尾位 / 尾上方）/ 羽覆背 / 翼+尾羽叠加；含同轮底座对照",
    "shots": [
        {"name": "base-fish", "seed": 6101, "prompt": _styled(FISH_BARE, [], **F4)},
        {"name": "fish-tail", "seed": 6101,
         "prompt": _styled(FISH_BARE, [B_TAIL], **F4)},
        {"name": "fish-tail-above", "seed": 6101,
         "prompt": _styled(FISH_BARE, [B_TAIL_ABOVE], **F4)},
        {"name": "fish-feathercoat", "seed": 6101,
         "prompt": _styled(FISH_BARE, [B_COAT], **F4)},
        {"name": "fish-wings-tail", "seed": 6101,
         "prompt": _styled(FISH_BARE, [B_WING, B_TAIL], **F4)},
    ],
}


# ---------------------------------------------------------------------------
# R5 结论与**期内容重排**
#
# 离水场景下：翼 ✅ 落地（R4/R5 两次复现）；尾羽 ❌ 仍不落地；羽覆背 ❌ 仍不落地。
#
# 于是 fish-bird 重新排期——**主轴从"换部件"改成"出水的阶段"**：
# 唯一落地的部件是翼，5 期就用**同一个部件的 5 个出水瞬间**来区分身份
# （期内恒定：同一部件；期间各异：水线位置 / 机位 / 光线 / 画幅）。
# 两条否定结论（尾羽、羽覆背）写进 parts.md 与 PLAN。
#
# 出水的五个阶段（每期都是一个可以停住的时间点）：
#   01 跃出水面（刚离水，水花未落）
#   02 半出水（水线仍穿过身体）
#   03 完全离水、双翼全展
#   04 低空掠过水面
#   05 鲲鹏（暮色海面、剪影）
# ---------------------------------------------------------------------------

OUT_WING_SPREAD = "a pair of broad feathered bird wings spread wide from its back"
OUT_WING_HALF = "a pair of broad feathered bird wings half-opened along its flanks"

assert "bird" in OUT_WING_SPREAD and "bird" in OUT_WING_HALF

# 期 01：跃出水面（刚离水）
S1 = dict(pose="它刚从水里跃出、身体还在往上冲：",
          scene="in open air just above the surface, spray still falling from its body",
          light="low backlight through the flying spray",
          lens="a level view from the side, 100mm lens at f/4, the whole body in frame")

ROUNDS[6] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 6101,
    "note": "期 01 定稿【跃出水面·水花未落】：鱼 + 鸟翼（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-fish", "seed": 6101, "prompt": _styled(FISH_BARE, [], **S1)},
        {"name": "fish-wings", "seed": 6101,
         "prompt": _styled(FISH_BARE, [B_WING], **S1)},
        {"name": "fish-wings-spread", "seed": 6102,
         "prompt": _styled(FISH_BARE, [OUT_WING_SPREAD], **S1)},
    ],
}

# 期 02：半出水（水线穿过身体）
S2 = dict(pose="它半个身体还在水里、前半身已经抬起：",
          scene="at the water surface, the waterline cutting across its body",
          light="soft side light with the surface breaking into highlights",
          lens="a level view from the side, 135mm lens at f/4, the whole animal in frame")

ROUNDS[7] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 6101,
    "note": "期 02 定稿【半出水·水线穿过身体】：鱼 + 鸟翼（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-fish", "seed": 6101, "prompt": _styled(FISH_BARE, [], **S2)},
        {"name": "fish-wings", "seed": 6101,
         "prompt": _styled(FISH_BARE, [B_WING], **S2)},
        {"name": "fish-wings-half", "seed": 6103,
         "prompt": _styled(FISH_BARE, [OUT_WING_HALF], **S2)},
    ],
}

# 期 03：完全离水、双翼全展（侧上方视角）
S3 = dict(pose="它悬在空中、身体横向展开：",
          scene="well above the water, only sky and a distant shoreline behind it",
          light="strong backlight rimming every feather",
          lens="a view from slightly above and to the side, 85mm lens at f/5.6")

ROUNDS[8] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 6101,
    "note": "期 03 定稿【完全离水·双翼全展·侧上方】：鱼 + 鸟翼（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-fish", "seed": 6101, "prompt": _styled(FISH_BARE, [], **S3)},
        {"name": "fish-wings-spread", "seed": 6101,
         "prompt": _styled(FISH_BARE, [OUT_WING_SPREAD], **S3)},
        {"name": "fish-wings-spread-b", "seed": 6102,
         "prompt": _styled(FISH_BARE, [OUT_WING_SPREAD], **S3)},
    ],
}

# 期 04：低空掠过水面（长焦压缩）
S4 = dict(pose="它贴着水面低飞、身体近乎水平：",
          scene="skimming low over open water, the far shore compressed behind it",
          light="flat overcast light on grey water",
          lens="a 400mm telephoto compressing the distance, f/4")

ROUNDS[9] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 6101,
    "note": "期 04 定稿【低空掠水·长焦压缩】：鱼 + 鸟翼（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-fish", "seed": 6101, "prompt": _styled(FISH_BARE, [], **S4)},
        {"name": "fish-wings", "seed": 6101,
         "prompt": _styled(FISH_BARE, [B_WING], **S4)},
        {"name": "fish-wings-spread", "seed": 6103,
         "prompt": _styled(FISH_BARE, [OUT_WING_SPREAD], **S4)},
    ],
}

# 期 05：鲲鹏（暮色海面、逆光剪影、广角）
S5 = dict(pose="它在暮色海面上高高跃起、双翼全展：",
          scene="above a dark open sea at dusk, the horizon far behind",
          light="low backlight throwing the whole animal into near-silhouette",
          lens="a wide-angle 35mm lens at eye height, f/4, the whole animal in frame")

ROUNDS[10] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 6101,
    "note": "期 05 收官【鲲鹏】：暮色海面逆光剪影 + 全展鸟翼（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-fish", "seed": 6101, "prompt": _styled(FISH_BARE, [], **S5)},
        {"name": "fish-wings-spread", "seed": 6101,
         "prompt": _styled(FISH_BARE, [OUT_WING_SPREAD], **S5)},
        {"name": "fish-wings-spread-b", "seed": 6102,
         "prompt": _styled(FISH_BARE, [OUT_WING_SPREAD], **S5)},
    ],
}


# ---------------------------------------------------------------------------
# R11：期 02「半出水」补 take
#
# R7 只成了一张：`fish-wings`（翼在体侧）在水线穿过身体时**被场景吃掉**，
# 而 `fish-wings-half`（半张的翼在体侧偏上）落地。
# → 规律 85 的精细版：**场景兼容性是"按区域"判断的**——
#   翼长在**露出水面的那部分**上能成，长在**水下那部分**上不成。
# 所以期 02 的定稿写法固定用「半张的翼、位置偏上」，多出几个 take 备选。
# ---------------------------------------------------------------------------

ROUNDS[11] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 6101,
    "note": "期 02 定稿（补 take）【半出水·水线穿过身体】：半张的翼在体侧偏上（三个 seed）；含同轮底座对照",
    "shots": [
        {"name": "base-fish", "seed": 6101, "prompt": _styled(FISH_BARE, [], **S2)},
        {"name": "fish-wings-half", "seed": 6101,
         "prompt": _styled(FISH_BARE, [OUT_WING_HALF], **S2)},
        {"name": "fish-wings-half-b", "seed": 6102,
         "prompt": _styled(FISH_BARE, [OUT_WING_HALF], **S2)},
        {"name": "fish-wings-half-c", "seed": 6104,
         "prompt": _styled(FISH_BARE, [OUT_WING_HALF], **S2)},
    ],
}
