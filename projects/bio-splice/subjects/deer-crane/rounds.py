"""鹿 + 鹤（鹿鹤同春）子主题的 prompt 权威源与轮次定义。

概念
----
**传统吉祥纹样「鹿鹤同春」**（鹿谐「禄」、鹤喻长寿），
本身就是把两种动物**并置成一个图案**——所以这个子主题的钩子不是"加一个部件"，
而是**把两种动物拆开、再把鹤的部件装到鹿身上**。

底座 = **鹿**（红鹿）。
供体 = 鹤的部位：长颈 G1 / 细腿 G2 / 尾羽 G6。

> ~~羽冠 G3 / 翼 G4 / 喙 G5~~ 已删：羽冠与喙在头上（规律 73），鹿没有翼基（规律 74）。

机制预测（依据本仓已实测的规律）
--------------------------------
- 规律 83/87：**鹿的颈与腿是"典范结构"**（删掉描述也会被模型补回来），
  所以 G1/G2 属"腾出占位"里最难的那一档——本轮要实测它到底行不行。
  参照：龟的颈/尾（删掉不伤底座）→ 完整成立；鱼鳍/猫掌/蛇鳞（删掉伤可信度）→ 0~部分。
- 规律 85：**生境必须与部件语义兼容**。鹤的颈/腿/尾羽都是"湿地涉禽"的语言，
  所以每期的场景都用**湿地/水边/雾林**，不用旱地硬光。
- 规律 79：姿态句不许提「颈」「腿」「尾」。
- 规律 80：不用低机位竖幅（末端部件会被画成独立个体）。
"""
from __future__ import annotations

PREFIX = "bs-dc"  # bio-splice / deer-crane

CN_FRAME = "全身像，一只动物独自占据画面："

PHOTO_BASE = ("fine surface detail, slight film grain, no digital sharpening, "
              "no text, no watermark")

# ---------------------------------------------------------------------------
# 三个底座：按"腾出哪一处"分。头、耳、毛色始终保留——它们是"这是鹿"的锚。
#   DEER        ：不写颈（把颈位腾给 G1）
#   DEER_NOLEGS ：不写腿（把腿位腾给 G2）
#   DEER_BARE   ：既不写腿也不写尾（给 G1+G2+G6 用）
# ---------------------------------------------------------------------------

DEER = ("a red deer with a slender head, large ears, a smooth reddish-brown coat, "
        "four long legs and a short tail")
DEER_NOLEGS = ("a red deer with a slender head, large ears, a smooth reddish-brown coat "
               "and a short tail")
DEER_NOTAIL = ("a red deer with a slender head, large ears, a smooth reddish-brown coat "
               "and four long legs")
DEER_BARE = ("a red deer with a slender head, large ears and a smooth reddish-brown coat")

for _n, _b in (("DEER", DEER), ("NOLEGS", DEER_NOLEGS), ("NOTAIL", DEER_NOTAIL),
               ("BARE", DEER_BARE)):
    assert " with " in _b, f"{_n}: _with 依赖「X with ...」结构"
    assert "red deer" in _b and "coat" in _b, f"{_n}: 物种名与毛色是「这是鹿」的锚，不能删"
    assert "neck" not in _b, f"{_n}: 颈位要腾给 G1，底座不许写颈"
assert "leg" not in DEER_NOLEGS and "leg" not in DEER_BARE
assert "tail" not in DEER_NOTAIL and "tail" not in DEER_BARE

# ---------------------------------------------------------------------------
# 移植件（只出部位，绝不写成"整只鹤"）
# ---------------------------------------------------------------------------

G_NECK = "a long slender crane's neck with fine grey feathers"      # G1
G_LEG = "a pair of long thin crane's legs"                          # G2
G_TAIL = "a fan of long white crane tail feathers"                  # G6

for _n, _p in (("G1", G_NECK), ("G2", G_LEG), ("G6", G_TAIL)):
    assert "deer" not in _p, f"{_n}: 移植件里不该出现底座动物"
    assert " whose " not in _p and "body is entirely" not in _p, f"{_n}: 不许用「整只」句式"
    assert "crane" in _p, f"{_n}: 必须点名供体"
    assert "beak" not in _p and "wing" not in _p and "crown" not in _p, \
        f"{_n}: 喙/翼/羽冠已删（规律 73/74）"


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
# R1（期 01）：长颈的鹿 —— 底座不写颈，看鹤的长颈能不能落地
# ---------------------------------------------------------------------------

D1 = dict(pose="它站在雾里、正面朝向镜头：",
          scene="in a misty bamboo grove, thin fog drifting between the stems",
          light="soft diffuse morning light",
          lens="a level camera at eye height, 400mm lens at f/4, the whole body in frame")

ROUNDS[1] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 7101,
    "note": "鹿鹤·第一期候选：鹿底座（腾出颈位）+ 鹤的长颈 G1（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-deer", "seed": 7101, "prompt": _styled(DEER, [], **D1)},
        {"name": "deer-craneneck", "seed": 7101,
         "prompt": _styled(DEER, [G_NECK], **D1)},
        {"name": "deer-craneneck-b", "seed": 7102,
         "prompt": _styled(DEER, [G_NECK], **D1)},
    ],
}

# ---------------------------------------------------------------------------
# R2（期 02 候选）：鹤腿的鹿 —— **腾出版**（底座不写腿）
# R3：同一件事的**占用版**（底座照常写 four long legs），两轮对照着看
#   "典范结构腾不出占位"（规律 87）在鹿腿上到底成不成立。
# ---------------------------------------------------------------------------

D2 = dict(pose="它在浅水里走着、侧身朝向镜头：",
          scene="in shallow marsh water among reeds, ripples around its feet",
          light="low morning sun raking across the water",
          lens="a level camera at eye height, 400mm lens at f/4, the whole body in frame")

ROUNDS[2] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 7101,
    "note": "鹿鹤·第二期候选【腾出版】：鹿底座（不写腿）+ 鹤的细腿 G2；含同轮底座对照",
    "shots": [
        {"name": "base-deer", "seed": 7101, "prompt": _styled(DEER_NOLEGS, [], **D2)},
        {"name": "deer-cranelegs", "seed": 7101,
         "prompt": _styled(DEER_NOLEGS, [G_LEG], **D2)},
        {"name": "deer-cranelegs-b", "seed": 7102,
         "prompt": _styled(DEER_NOLEGS, [G_LEG], **D2)},
    ],
}

ROUNDS[3] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 7101,
    "note": "鹿鹤·第二期对照【占用版】：鹿底座（照常写 four long legs）+ 鹤的细腿 G2；含同轮底座对照",
    "shots": [
        {"name": "base-deer", "seed": 7101, "prompt": _styled(DEER, [], **D2)},
        {"name": "deer-cranelegs", "seed": 7101,
         "prompt": _styled(DEER, [G_LEG], **D2)},
    ],
}

# ---------------------------------------------------------------------------
# R4（期 03）：鹤尾的鹿 —— 鹿的短尾是**真的空位**（短小到几乎看不见）
# ---------------------------------------------------------------------------

D3 = dict(pose="它站在苇丛里、侧身朝向镜头：",
          scene="among tall reeds at the edge of a marsh",
          light="strong backlight through the reed heads",
          lens="a level camera at eye height, 600mm lens at f/4, the whole body in frame")

ROUNDS[4] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 7101,
    "note": "鹿鹤·第三期候选：鹿底座（不写尾）+ 鹤的尾羽 G6（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-deer", "seed": 7101, "prompt": _styled(DEER_NOTAIL, [], **D3)},
        {"name": "deer-cranetait", "seed": 7101,
         "prompt": _styled(DEER_NOTAIL, [G_TAIL], **D3)},
        {"name": "deer-cranetait-b", "seed": 7102,
         "prompt": _styled(DEER_NOTAIL, [G_TAIL], **D3)},
    ],
}

# ---------------------------------------------------------------------------
# R5（期 04）：颈腿俱全 —— 两处跨区域（颈在头侧、腿在下半身）
# R6（期 05）：鹿鹤同春（收官）—— 颈 + 腿 + 尾羽三处
# ---------------------------------------------------------------------------

D4 = dict(pose="它立在结霜的草地上、侧身朝向镜头：",
          scene="on a frost-covered meadow at first light",
          light="cold low light, frost glittering on the grass",
          lens="a level camera at eye height, 400mm lens at f/4")

ROUNDS[5] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 7101,
    "note": "鹿鹤·第四期候选【颈腿俱全】：鹿底座（不写腿）+ 鹤颈 G1 + 鹤腿 G2；含同轮底座对照",
    "shots": [
        {"name": "base-deer", "seed": 7101, "prompt": _styled(DEER_NOLEGS, [], **D4)},
        {"name": "deer-neck-legs", "seed": 7101,
         "prompt": _styled(DEER_NOLEGS, [G_NECK, G_LEG], **D4)},
        {"name": "deer-neck-legs-b", "seed": 7102,
         "prompt": _styled(DEER_NOLEGS, [G_NECK, G_LEG], **D4)},
    ],
}

D5 = dict(pose="它站在花树下、身体横向展开：",
          scene="under blossoming plum trees in spring, petals drifting down",
          light="soft diffused light through the blossom",
          lens="a wide-angle 35mm lens at eye height, f/4, the whole animal in frame")

D_ALL3 = [G_NECK, G_LEG, G_TAIL]

ROUNDS[6] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 7101,
    "note": "鹿鹤·第五期收官【鹿鹤同春】：鹿底座（不写腿尾）+ 鹤颈 G1 + 鹤腿 G2 + 鹤尾羽 G6；含同轮底座对照",
    "shots": [
        {"name": "base-deer", "seed": 7101, "prompt": _styled(DEER_BARE, [], **D5)},
        {"name": "deer-crane-3parts", "seed": 7101,
         "prompt": _styled(DEER_BARE, D_ALL3, **D5)},
        {"name": "deer-crane-3parts-b", "seed": 7102,
         "prompt": _styled(DEER_BARE, D_ALL3, **D5)},
    ],
}

# 守卫：姿态句不许提到目标部位（规律 79）；对照镜头必须逐字等于底座
for _r, _base in ((1, DEER), (2, DEER_NOLEGS), (3, DEER), (4, DEER_NOTAIL),
                  (5, DEER_NOLEGS), (6, DEER_BARE)):
    _p = ROUNDS[_r]["shots"][0]["prompt"]
    assert _base in _p and _p.rsplit("：", 1)[-1].startswith(_base), f"R{_r}: 对照必须是底座原文"
for _t in (D1, D2, D3, D4, D5):
    for _w in ("颈", "腿", "尾", "neck", "leg", "tail", "feather"):
        assert _w not in _t["pose"], f"姿态句里出现了 {_w}（规律 79）"


# ---------------------------------------------------------------------------
# R7：期 03 补 take
#
# R4 里 `deer-cranetait`（seed 7101）落了地——一圈**白色的鹤尾羽**从鹿的臀部长出来，
# 而 seed 7102 没落。尾羽是本子主题唯一"真·空位"（鹿尾短小到几乎看不见），
# 所以它的成功率明显高于颈与腿。补几个 seed 把期 03 的两张成品凑齐。
# ---------------------------------------------------------------------------

ROUNDS[7] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 7101,
    "note": "鹿鹤·第三期定稿（补 take）：鹿底座（不写尾）+ 鹤的尾羽 G6（三个 seed）；含同轮底座对照",
    "shots": [
        {"name": "base-deer", "seed": 7101, "prompt": _styled(DEER_NOTAIL, [], **D3)},
        {"name": "deer-cranetait", "seed": 7101,
         "prompt": _styled(DEER_NOTAIL, [G_TAIL], **D3)},
        {"name": "deer-cranetait-c", "seed": 7103,
         "prompt": _styled(DEER_NOTAIL, [G_TAIL], **D3)},
        {"name": "deer-cranetait-d", "seed": 7104,
         "prompt": _styled(DEER_NOTAIL, [G_TAIL], **D3)},
    ],
}
