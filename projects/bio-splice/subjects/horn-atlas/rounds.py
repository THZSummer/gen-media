"""角 · 图鉴（horn-atlas）子主题的 prompt 权威源与轮次定义。

设计
----
把「角」当成一个**可加的器官**做成一册图鉴：
**固定一匹本来没有角的马，轮流给它长五种角。**

底座 = 一匹标准马（统一底座，**本来无角**）。
供体 = 五种「角」：鹿 H1 / 牛 H2 / 羊 H3 / 犀 H4 / 独角鲸 H5。

机制预判（按 92/96/97/99/105/107）
--------------------------------
| 问题 | 答案 | 结论 |
|------|------|------|
| ① 底座整体多定型？ | 马很定型 | 但 **92 是整体视角**，要看落点 |
| ② 落点是不是典范结构？ | 额顶/鼻梁——**马本来无角** | ✅ 空面 |
| ③ 要腾结构还是属性？ | 不需要腾（底座不写角） | ✅ |
| ④ 承载面？ | 额骨/鼻骨表面 | ✅ 从表面生出（规律 97） |
| 语义（107）？ | 五种供体**本身就是角** | ✅ 语义匹配 |

> 五条全过——这是全项目**先验最有利**的一个子主题。
> 唯一的不确定性是"独角鲸的长牙"：它是牙而不是角（语义上略有偏差），
> 以及"犀角"是角质而非骨角——两条都在实测里检验。
"""
from __future__ import annotations

PREFIX = "bs-ha"  # bio-splice / horn-atlas

CN_FRAME = "全身像，一只动物独自占据画面："

PHOTO_BASE = ("Wildlife photograph, fine surface detail, slight film grain, "
              "no digital sharpening, no text, no watermark")

# ---------------------------------------------------------------------------
# 统一底座：一匹**本来无角**的马
# ---------------------------------------------------------------------------

HORSE = ("a bay horse with a long dark mane, a dark muzzle, four slender legs "
         "and a flowing tail")

assert " with " in HORSE, "_with 依赖「X with ...」结构"
assert "horn" not in HORSE and "antler" not in HORSE, "底座必须本来无角（空位）"
assert "horse" in HORSE, "物种名是「这是马」的锚"

# ---------------------------------------------------------------------------
# 五种「角」——一律"从额顶/鼻梁生出"（空面 + 位置短语）
# ---------------------------------------------------------------------------

H_DEER = "a pair of branching deer antlers rising from its forehead"
H_OX = "a pair of thick curved ox horns rising from its forehead"
H_SHEEP = "a pair of curled ram horns rising from its forehead"
H_RHINO = "a single heavy rhinoceros horn rising from its nose"
H_NARWHAL = "a single long spiral narwhal tusk rising from its forehead"

for _n, _p in (("H1", H_DEER), ("H2", H_OX), ("H3", H_SHEEP), ("H4", H_RHINO),
               ("H5", H_NARWHAL)):
    assert "horse" not in _p, f"{_n}: 移植件里不该出现底座"
    assert " whose " not in _p and "body is entirely" not in _p, f"{_n}: 不许用「整只」句式"
    assert "rising from its" in _p, f"{_n}: 必须是「从额顶/鼻梁生出」的位置短语（规律 97/99）"
    assert ("a pair of" in _p) or ("a single" in _p), f"{_n}: 成对或单支要写清楚（图鉴规格）"


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
# R1（第一部分 · 基准）：晨雾草场 · 柔光 · 平视 · 方 —— 只有底座，三个 take
# ---------------------------------------------------------------------------

K1 = dict(pose="它立在雾里、侧身朝向镜头：",
          scene="in a misty meadow at dawn",
          light="soft diffused light through the mist",
          lens="a level view at eye height, 400mm lens at f/4")

ROUNDS[1] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 14101,
    "note": "角图鉴·第一部分【无角基准】：统一底座（三个 take），作为后四部分的参照",
    "shots": [
        {"name": "base-horse", "seed": 14101, "prompt": _styled(HORSE, [], **K1)},
        {"name": "base-horse-b", "seed": 14102, "prompt": _styled(HORSE, [], **K1)},
        {"name": "base-horse-c", "seed": 14103, "prompt": _styled(HORSE, [], **K1)},
    ],
}

# ---------------------------------------------------------------------------
# 第二–四部分：晨雾草场（同机位） + 侧逆光 / 顶光，只换角
#   图鉴的"期内恒定"在这里体现为：**同一个底座、同一片草场、同一焦段**，
#   只让光线与角变化——这样才像"同一册图鉴里的几页"。
# ---------------------------------------------------------------------------

K2 = dict(K1, light="low side-backlight rimming its outline")
K3 = dict(K1, light="flat top light, the coat dull and even")

ROUNDS[2] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 14101,
    "note": "角图鉴·第二部分【鹿角】：统一底座 + 分叉鹿角（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-horse", "seed": 14101, "prompt": _styled(HORSE, [], **K2)},
        {"name": "horse-antlers", "seed": 14101, "prompt": _styled(HORSE, [H_DEER], **K2)},
        {"name": "horse-antlers-b", "seed": 14102, "prompt": _styled(HORSE, [H_DEER], **K2)},
    ],
}

ROUNDS[3] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 14101,
    "note": "角图鉴·第三部分【牛角】：统一底座 + 粗壮牛角（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-horse", "seed": 14101, "prompt": _styled(HORSE, [], **K3)},
        {"name": "horse-oxhorns", "seed": 14101, "prompt": _styled(HORSE, [H_OX], **K3)},
        {"name": "horse-oxhorns-b", "seed": 14102, "prompt": _styled(HORSE, [H_OX], **K3)},
    ],
}

ROUNDS[4] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 14101,
    "note": "角图鉴·第四部分【羊角】：统一底座 + 卷曲羊角（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-horse", "seed": 14101, "prompt": _styled(HORSE, [], **K2)},
        {"name": "horse-ramhorns", "seed": 14101, "prompt": _styled(HORSE, [H_SHEEP], **K2)},
        {"name": "horse-ramhorns-b", "seed": 14102, "prompt": _styled(HORSE, [H_SHEEP], **K2)},
    ],
}

# ---------------------------------------------------------------------------
# 第五部分（收官）：霜晨草原 · 侧逆光 · 贴面特写 · 竖
#   两种"单支角"（独角鲸长牙 / 犀角）各出一张——都是"从鼻梁/额顶向上的一支"，
#   正好作为图鉴的收尾（从成对的角走到单支的角）。
# ---------------------------------------------------------------------------

K5 = dict(frame="头部特写，一只动物独自占据画面：",
          pose="它抬起头、正面朝向镜头：",
          scene="on frost-covered grassland at first light",
          light="low side-backlight, frost glittering",
          lens="a tight portrait of the head, 200mm lens at f/5.6")

ROUNDS[5] = {
    "engine": "zimage", "size": (1024, 1280), "steps": 12, "seed": 14101,
    "note": "角图鉴·第五部分【独角鲸长牙 / 犀角】：统一底座 + 两种单支角（各一张）；含同轮底座对照",
    "shots": [
        {"name": "base-horse", "seed": 14101, "prompt": _styled(HORSE, [], **K5)},
        {"name": "horse-narwhal", "seed": 14101, "prompt": _styled(HORSE, [H_NARWHAL], **K5)},
        {"name": "horse-rhino", "seed": 14102, "prompt": _styled(HORSE, [H_RHINO], **K5)},
    ],
}

# 守卫：姿态句不许提到目标部位（规律 79）
for _t in (K1, K2, K3, K5):
    for _w in ("角", "牙", "额", "鼻", "horn", "antler", "tusk", "forehead", "nose"):
        assert _w not in _t["pose"], f"姿态句里出现了 {_w}（规律 79）"
