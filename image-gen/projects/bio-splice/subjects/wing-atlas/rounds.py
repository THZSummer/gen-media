"""翅 · 图鉴（wing-atlas）子主题的 prompt 权威源与轮次定义。

概念
----
把「翅」当成一个**可加的器官**做成一册图鉴：
**固定一只鸟（保留它自己的翅膀），在背上再加一对别人的翅。**

底座 = 一种标准中型鸟（统一底座）。
供体 = 四种「翅」：
  W2 昆虫膜翅 / W3 蝙蝠皮翼 / W4 鱼胸鳍 / W5 枫树种子翅
  （W1 羽翼由底座自己承担，作为第一部分「基准」）

机制预判（按 92/96/97/99/105 的四问 + 两条门槛）
--------------------------------
- **落点 = 背部**：一个**空面**（鸟背上本来没有第三对附肢）→ 规律 97/99 双过。
- **不同形 + 高辨识度**：膜翅/皮翼/胸鳍/种子翅与鸟的羽翼形状完全不同 → 规律 91/90。
- **不需要承载结构**：从背部表面直接生出 → 规律 97。
- 本册是**唯一不用换底座**的子主题（统一底座），所以规律 106 的"换底座风险"不存在；
  要做出期身份只能靠**呈现**与**四种翅本身**。

> 原计划是「把鸟翼换成别的翅」（同材质替换），已按规律 67/99 改为
> **「在背上再加一对」**（空位新增）——这是本册能成立的前提。
"""
from __future__ import annotations

PREFIX = "bs-wa"  # bio-splice / wing-atlas

CN_FRAME = "全身像，一只动物独自占据画面："

PHOTO_BASE = ("Wildlife photograph, fine surface detail, slight film grain, "
              "no digital sharpening, no text, no watermark")

# ---------------------------------------------------------------------------
# 统一底座：一只中型鸟（**保留它自己的翅膀**）
# ---------------------------------------------------------------------------

BIRD = ("a medium-sized brown bird with a rounded head, a short dark beak, "
        "folded feathered wings and a long tail")

assert " with " in BIRD, "_with 依赖「X with ...」结构"
assert "wings" in BIRD, "底座必须保留自己的翅膀（本册是「再加一对」，不是「换掉」）"
assert "bird" in BIRD, "物种名是「这是鸟」的锚"

# ---------------------------------------------------------------------------
# 四种「第二对翅」——一律写成"从背上生出"（空面 + 直白的位置短语）
# ---------------------------------------------------------------------------

W_MEMBRANE = "a pair of translucent insect membranous wings rising from its back"
W_BAT = "a pair of leathery bat wings rising from its back"
W_FIN = "a pair of stiff fish pectoral fins rising from its back"
W_SEED = "a pair of dry maple seed wings rising from its back"

for _n, _p in (("W2", W_MEMBRANE), ("W3", W_BAT), ("W4", W_FIN), ("W5", W_SEED)):
    assert "bird" not in _p, f"{_n}: 移植件里不该出现底座"
    assert " whose " not in _p and "body is entirely" not in _p, f"{_n}: 不许用「整只」句式"
    assert "rising from its back" in _p, f"{_n}: 必须是「从背上生出」的位置短语（规律 97/99）"
    assert "a pair of" in _p, f"{_n}: 一定是一对（图鉴的规格要统一）"


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
# R1（期 01 · 基准）：枝头 · 侧逆光 · 平视 · 方 —— 只有底座，三个 take
#   本册的第一部分是"基准"：作为后四部分的参照，所以**没有移植件**，也没有对照镜头
#   （基准本身就是对照）。
# ---------------------------------------------------------------------------

A1 = dict(pose="它停在枝头、侧身朝向镜头：",
          scene="on a bare branch in a woodland clearing",
          light="soft side-backlight rimming its outline",
          lens="a level view at eye height, 400mm lens at f/4")

ROUNDS[1] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 13101,
    "note": "翅图鉴·第一部分【双翼基准】：只有统一底座（三个 take），作为后四部分的参照",
    "shots": [
        {"name": "base-bird", "seed": 13101, "prompt": _styled(BIRD, [], **A1)},
        {"name": "base-bird-b", "seed": 13102, "prompt": _styled(BIRD, [], **A1)},
        {"name": "base-bird-c", "seed": 13103, "prompt": _styled(BIRD, [], **A1)},
    ],
}

# ---------------------------------------------------------------------------
# 期 02–05 的呈现（各自不同，用来给四部分不同的期身份）
# ---------------------------------------------------------------------------

A2 = dict(pose="它停在枝头、身体微微抬起：",
          scene="on a branch in a sunlit woodland clearing",
          light="flat top light, no shadows",
          lens="a level view at eye height, 400mm lens at f/5.6")

A3 = dict(pose="它停在岩壁上、侧身朝向镜头：",
          scene="at the mouth of a dim limestone cave",
          light="hard light from the cave mouth, deep shadows behind",
          lens="a level view at eye height, 300mm lens at f/5.6")

A4 = dict(pose="它立在水边的石头上、侧身朝向镜头：",
          scene="on a wet stone at the edge of a stream",
          light="soft wet light, reflections from the water below",
          lens="a level view at eye height, 400mm lens at f/5.6")

A5 = dict(pose="它停在秋枝上、身体侧向镜头：",
          scene="among turning leaves in an autumn wood",
          light="strong backlight through the leaves",
          lens="a wide view at eye height, 135mm lens at f/5.6")

ROUNDS[2] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 13101,
    "note": "翅图鉴·第二部分【膜翅】：统一底座 + 昆虫膜翅（背上第二对，两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-bird", "seed": 13101, "prompt": _styled(BIRD, [], **A2)},
        {"name": "bird-membrane", "seed": 13101,
         "prompt": _styled(BIRD, [W_MEMBRANE], **A2)},
        {"name": "bird-membrane-b", "seed": 13102,
         "prompt": _styled(BIRD, [W_MEMBRANE], **A2)},
    ],
}

ROUNDS[3] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 13101,
    "note": "翅图鉴·第三部分【皮翼】：统一底座 + 蝙蝠皮翼（背上第二对，两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-bird", "seed": 13101, "prompt": _styled(BIRD, [], **A3)},
        {"name": "bird-bat", "seed": 13101, "prompt": _styled(BIRD, [W_BAT], **A3)},
        {"name": "bird-bat-b", "seed": 13102, "prompt": _styled(BIRD, [W_BAT], **A3)},
    ],
}

ROUNDS[4] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 13101,
    "note": "翅图鉴·第四部分【鳍翼】：统一底座 + 鱼胸鳍（背上第二对，两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-bird", "seed": 13101, "prompt": _styled(BIRD, [], **A4)},
        {"name": "bird-fin", "seed": 13101, "prompt": _styled(BIRD, [W_FIN], **A4)},
        {"name": "bird-fin-b", "seed": 13102, "prompt": _styled(BIRD, [W_FIN], **A4)},
    ],
}

ROUNDS[5] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 13101,
    "note": "翅图鉴·第五部分【种子翅】：统一底座 + 枫树种子翅（背上第二对，两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-bird", "seed": 13101, "prompt": _styled(BIRD, [], **A5)},
        {"name": "bird-seed", "seed": 13101, "prompt": _styled(BIRD, [W_SEED], **A5)},
        {"name": "bird-seed-b", "seed": 13102, "prompt": _styled(BIRD, [W_SEED], **A5)},
    ],
}

# 守卫：姿态句不许提到目标部位（规律 79）
for _t in (A1, A2, A3, A4, A5):
    for _w in ("翅", "翼", "背", "wing", "back", "membrane", "bat", "fin", "seed"):
        assert _w not in _t["pose"], f"姿态句里出现了 {_w}（规律 79）"


# ---------------------------------------------------------------------------
# R2–R5 判读结论与追问
#
#   ✅ W2 昆虫膜翅（2/2）：背上多出一对半透膜翅，一眼可辨
#   ✅ W3 蝙蝠皮翼（2/2）：背上一对皮革质翼
#   ❌ W4 鱼胸鳍（0/2）：背部区放大 ×1.7 后只有普通羽翼
#   ⚠️ W5 枫树种子翅（判读存疑）：翅膀散开了、变浅了，但没有"种子翅"的形状
#
#   → 假设：**「第二对翅」这个落点有一条语义门槛**——
#     供体必须**本身就是"翅"**（昆虫膜翅、蝙蝠皮翼都有"翼"的语义与形态），
#     而"鱼鳍""种子"在背上没有"翅"的先例，于是被读成普通羽翼或被丢掉。
#     （这是规律 85「生境语义相容」在**部件-落点**层面的版本 → 记为 107。）
#
#   R6 追问：换三种"更接近翅"的供体，看哪两种能落。
# ---------------------------------------------------------------------------

W_FLYFISH = ("a pair of long gliding flying-fish fins rising from its back")
W_CRANE = ("a pair of long white crane wings rising from its back")
W_SAMARA = ("a pair of broad papery samara wings rising from its back")

for _n, _p in (("飞鱼鳍", W_FLYFISH), ("鹤羽翼", W_CRANE), ("种子翅·改", W_SAMARA)):
    assert "rising from its back" in _p and "a pair of" in _p, _n

ROUNDS[6] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 13101,
    "note": "翅图鉴·追问轮：飞鱼鳍翼 / 鹤羽翼 / 纸翅（三种更接近「翅」的供体）；含同轮底座对照",
    "shots": [
        {"name": "base-bird", "seed": 13101, "prompt": _styled(BIRD, [], **A2)},
        {"name": "bird-flyfish", "seed": 13101,
         "prompt": _styled(BIRD, [W_FLYFISH], **A2)},
        {"name": "bird-crane", "seed": 13101,
         "prompt": _styled(BIRD, [W_CRANE], **A2)},
        {"name": "bird-samara", "seed": 13101,
         "prompt": _styled(BIRD, [W_SAMARA], **A2)},
    ],
}


# ---------------------------------------------------------------------------
# R6 判读：**语义门槛成立**（记为规律 107）
#   ✅ 飞鱼鳍翼：`flying-fish fins` 自带"飞"的语义 → 落成一对可当翅用的长鳍
#   ✅ 鹤羽翼：`crane wings` 本身就是翅 → 一对白翼从背上生出（最漂亮的一张）
#   ⚠️ 纸翅（samara）：只到"散开变浅"，形状仍不像种子翅
#   ❌ 之前的鱼胸鳍（`pectoral fins` 无"飞"义）、枫树种子翅（无"翅"的先例）
#
# → **规律 107：供体的"语义类别"必须与落点的功能匹配。**
#   在"背上加一对翅"这个落点上，供体必须**本身是翅、或自带飞行语义**；
#   光有"像翅的形状"不够（鱼鳍/种子翅的形状也像，但没有"能飞"的语义）。
# ---------------------------------------------------------------------------

# 期 04：飞鱼鳍翼（水边 · 湿润光 · 方）
ROUNDS[7] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 13101,
    "note": "期 04 定稿【飞鱼鳍翼】：统一底座 + 飞鱼的长鳍（背上第二对，两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-bird", "seed": 13101, "prompt": _styled(BIRD, [], **A4)},
        {"name": "bird-flyfish", "seed": 13101,
         "prompt": _styled(BIRD, [W_FLYFISH], **A4)},
        {"name": "bird-flyfish-b", "seed": 13102,
         "prompt": _styled(BIRD, [W_FLYFISH], **A4)},
    ],
}

# 期 05：鹤羽翼（秋林 · 逆光 · 广角横幅）
ROUNDS[8] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 13101,
    "note": "期 05 收官【鹤羽翼】：统一底座 + 鹤的白翼（背上第二对，两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-bird", "seed": 13101, "prompt": _styled(BIRD, [], **A5)},
        {"name": "bird-crane", "seed": 13101,
         "prompt": _styled(BIRD, [W_CRANE], **A5)},
        {"name": "bird-crane-b", "seed": 13102,
         "prompt": _styled(BIRD, [W_CRANE], **A5)},
    ],
}
