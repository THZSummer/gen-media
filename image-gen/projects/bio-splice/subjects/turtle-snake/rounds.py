"""龟 + 蛇（玄武）子主题的 prompt 权威源与轮次定义。

概念
----
**四象之「玄武」就是龟蛇合体**——典籍里的拼接体（《礼记》《楚辞》等有龟蛇之说）。
与 cat-eagle（拆一个词）、dragon-nines（执行古人的部件表）不同，
这个子主题的钩子是**一个已经存在的合体形象**。

底座 = **龟**（背甲 / 腹甲 / 短足 / 小尾）。
供体 = 蛇的**身体件**：颈 N1 / 尾 N2 / 缠体 N3 / 鳞 N5。

机制预测（依据本仓已实测的规律）
--------------------------------
- 规律 67：**空位新增 > 腾出占位 > 同材质替换**。龟有短颈、小尾 →
  这两处属"腾出占位"；缠体 N3 是**空位新增**（龟壳上本来没有东西），最容易成。
- 规律 73：**头部件不可移植** → 本轮**不给蛇头**（只给颈/尾/缠体），
  收官期「玄武」也不含蛇头。这是 PLAN 已经改过的一处。
- 规律 79：**姿态句必须对目标部位保持沉默**——不许写「长颈」「尾巴」这类词，
  否则连底座对照都会长出该部件。
- 规律 80：**呈现层不是中性的**——低机位 + 竖幅曾让"尾巴"句拖出一整只供体
  （cat-eagle R10/R14），所以本轮与期 02 都用**平视全身**。
"""
from __future__ import annotations

PREFIX = "bs-ts"  # bio-splice / turtle-snake

# ---------------------------------------------------------------------------
# 轮内恒定层：CN 取景句 + 摄影底子（系列恒定层，只留这两条）
# ---------------------------------------------------------------------------

CN_FRAME = "全身像，一只动物独自占据画面："

PHOTO_BASE = ("fine surface detail, slight film grain, no digital sharpening, "
              "no text, no watermark")

# ---------------------------------------------------------------------------
# 底座：龟。**刻意不描述颈的长短与尾**——把这两处腾出来给 N1/N2
# （规律 66：占位可以腾出）。壳与四肢照常描述，保证底座本身可信。
# ---------------------------------------------------------------------------

FULL_TURTLE = ("a large wild river turtle with a dark domed shell, a small wrinkled head, "
               "four short webbed legs")

assert " with " in FULL_TURTLE, "_with 依赖「X with ...」结构"
assert "tail" not in FULL_TURTLE, "腾出占位：底座不许先描述尾"
assert "neck" not in FULL_TURTLE, "腾出占位：底座不许先描述颈"
assert "shell" in FULL_TURTLE and "legs" in FULL_TURTLE, "底座的可信度靠壳与四肢"

# ---------------------------------------------------------------------------
# 移植件（只出部位，绝不写成"整只蛇"；也不出现底座动物名）
# ---------------------------------------------------------------------------

N_NECK = "a long sinuous snake's neck with fine keeled scales"          # N1 蛇颈
N_TAIL = "a long tapering snake's tail with keeled scales"             # N2 蛇尾
N_COIL = "the thick coiled body of a large snake wrapped around its shell"   # N3 缠体
N_SCALE = "large overlapping snake scales"                             # N5 鳞（备用）

for _n, _p in (("N1", N_NECK), ("N2", N_TAIL), ("N3", N_COIL), ("N5", N_SCALE)):
    assert "turtle" not in _p, f"{_n}: 移植件里不该出现底座动物"
    assert " whose " not in _p and "body is entirely" not in _p, f"{_n}: 不许用「整只」句式"
    assert "snake's" in _p or "snake " in _p or "snake scales" in _p, f"{_n}: 必须是蛇的部位"

assert "head" not in N_NECK and "head" not in N_TAIL and "head" not in N_COIL, \
    "规律 73：不给蛇头"


def _with(base: str, parts: list[str]) -> str:
    """把移植部位插到底座名之后：`a wild river turtle with X and Y, <其余描述>`。"""
    head, _, rest = base.partition(" with ")
    joined = " and ".join(parts)
    return f"{head} with {joined}, {rest}"


def _styled(base: str, parts: list[str], *, frame: str = CN_FRAME, pose: str,
            scene: str, light: str, lens: str) -> str:
    """期专属呈现：{CN 取景句}{姿态}{底座 with 部位}. {生境} {光线} {镜头} {摄影底子}"""
    core = _with(base, parts) if parts else base
    return (f"{frame}{pose}{core}. {scene}. {light}. "
            f"Wildlife photograph, {lens}, {PHOTO_BASE}.")


# 存档抬头用的"轮内恒定层"模板（换行只影响排版，不进入 prompt）
ARCHIVE_LAYERS = f"{CN_FRAME}<姿态><底座 with 部位>. <生境>. <光线>. Wildlife photograph, <镜头>, {PHOTO_BASE}."


# ---------------------------------------------------------------------------
# R1：一次性把单件与叠加都测掉（期 01 的呈现即"中性"呈现）
#
# 期 01「蛇颈的龟」= 溪石浅滩 · 晨光 · 平视 600mm · 方。
# 这一轮同时出：底座对照 / N1 / N2 / N3 / N1+N2 ——
# 单件先各自验证，叠加才有归因（规律 69：先验证单件、再叠加）。
#
# 姿态句刻意只说"爬上岸、正面朝向镜头"：**不提颈、不提尾**（规律 79）。
# ---------------------------------------------------------------------------

T1 = dict(pose="它从水里爬上溪石、正面朝向镜头：",
          scene="on wet river stones at the edge of a shallow stream in early morning",
          light="soft low morning light",
          lens="a level camera at eye height, 600mm telephoto lens at f/4, "
               "the whole body in frame")

ROUNDS: dict[int, dict] = {}

ROUNDS[1] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 5101,
    "note": "玄武·第一期候选：龟底座 + 蛇颈 N1 / 蛇尾 N2 / 缠体 N3（含同轮底座对照）",
    "shots": [
        {"name": "base-turtle", "seed": 5101, "prompt": _styled(FULL_TURTLE, [], **T1)},
        {"name": "turtle-snakeneck", "seed": 5101,
         "prompt": _styled(FULL_TURTLE, [N_NECK], **T1)},
        {"name": "turtle-snaketail", "seed": 5101,
         "prompt": _styled(FULL_TURTLE, [N_TAIL], **T1)},
        {"name": "turtle-coil", "seed": 5101,
         "prompt": _styled(FULL_TURTLE, [N_COIL], **T1)},
        {"name": "turtle-neck-tail", "seed": 5101,
         "prompt": _styled(FULL_TURTLE, [N_NECK, N_TAIL], **T1)},
    ],
}

# 守卫：对照镜头必须逐字等于底座；姿态句不许提到目标部位（规律 79）
assert ROUNDS[1]["shots"][0]["prompt"].rsplit("：", 1)[1].startswith(FULL_TURTLE)
for _w in ("颈", "尾", "neck", "tail", "coil", "缠"):
    assert _w not in T1["pose"], f"姿态句里出现了 {_w}（规律 79：会污染对照）"


# ---------------------------------------------------------------------------
# R2：追问「缠体 N3」为什么没落地（空位新增却失败）
#
# R1 实测：N1 蛇颈 ✅ 完整成立、N2 蛇尾 ✅ 成立（翘得有点高）、**N3 缠体 ❌ 完全没出现**。
# N3 本来是按规律 67 排的"空位新增、最容易成"那一档，所以它的失败值得追。
#
# 三个候选解释，各写一句来测：
#   a) **关系从句太绕**：`wrapped around its shell` 要求模型处理"环绕"这个空间关系
#      → 改成名词化的 `thick snake coils around the rim of its shell`
#   b) **壳面被占位**：底座写着 `a dark domed shell`，龟壳正面已被描述占住
#      → 改成"盘在龟身下方的石面上"（地面是空位）
#   c) **只是写法太冗长** → 最短写法 `thick snake coils around its shell`
#
# 呈现换到期 03 计划的**侧俯视**（俯视才看得见壳面上的缠绕），
# 但**不用低机位竖幅**——那个组合在 cat-eagle 上出过"拖出整个供体"的问题（规律 80）。
# ---------------------------------------------------------------------------

T3 = dict(pose="它伏在井边的石台上、龟壳朝向镜头：",
          scene="on a mossy stone ledge beside an old stone well",
          light="hard side light raking across the shell",
          lens="a view from slightly above, 100mm lens at f/5.6, the whole shell in frame")

N_COIL_RIM = "thick snake coils around the rim of its shell"
N_COIL_GROUND = "a thick snake's body coiled on the stones beneath it, its coils visible on both sides"
N_COIL_MIN = "thick snake coils around its shell"

assert "head" not in N_COIL_RIM + N_COIL_GROUND + N_COIL_MIN, "规律 73：不给蛇头"

ROUNDS[2] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 5101,
    "note": "玄武·第三期候选：缠体 N3 的三种写法（环绕壳沿 / 盘在身下石面 / 最短式）；含同轮底座对照",
    "shots": [
        {"name": "base-turtle", "seed": 5101, "prompt": _styled(FULL_TURTLE, [], **T3)},
        {"name": "coil-rim", "seed": 5101,
         "prompt": _styled(FULL_TURTLE, [N_COIL_RIM], **T3)},
        {"name": "coil-ground", "seed": 5101,
         "prompt": _styled(FULL_TURTLE, [N_COIL_GROUND], **T3)},
        {"name": "coil-min", "seed": 5101,
         "prompt": _styled(FULL_TURTLE, [N_COIL_MIN], **T3)},
    ],
}


# ---------------------------------------------------------------------------
# R2 结论：缠体**能成**，失败原因是写法
#
#   ❌ `the thick coiled body of a large snake wrapped around its shell`（关系从句 + 长定语）
#   ✅ `thick snake coils around the rim of its shell` / `... coiled on the stones beneath it`
#      / `thick snake coils around its shell`（名词短语）
#
#   → 规律 81：**空间关系从句（`X wrapped around Y`）会失效，改成名词短语（`coils around Y`）
#     才落地**——这是规律 69（复合部件要拆开写）的延伸。
#   三种写法都出现了"蛇身盘绕龟壳"的弧，其中 `coil-ground` 与 `coil-min` 最像玄武。
# ---------------------------------------------------------------------------

N_COIL_OK = N_COIL_MIN  # 定稿用的缠体写法（最短、最稳）

# ---------------------------------------------------------------------------
# 期 01–05 的定稿轮（R3–R6；期 03 直接用 R2）
#
# 期 01 = R3（T1 溪石浅滩·晨光·平视 600mm·方）—— 同一呈现下的两个 take
# 期 02 = R4（**湿地泥岸·阴天·平视全身 400mm·方**）
#         ⚠️ PLAN 原定"低机位贴地·竖"，按规律 80 改成平视全身：
#         低机位竖幅在 cat-eagle 上把"尾巴句"变成了另一只完整动物。
# 期 04 = R5（雨后溪石·逆光·平视 400mm·横）
# 期 05 = R6（暮色水面·平视广角 35mm·横幅）—— 收官「玄武」= 颈 + 尾 + 缠体
#
# 每个 take 用不同 seed，但**呈现层完全一致**（期内恒定，规律 70）。
# ---------------------------------------------------------------------------

ROUNDS[3] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 5101,
    "note": "期 01 定稿【溪石浅滩·晨光·平视 600mm】：龟底座 + 蛇颈 N1（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-turtle", "seed": 5101, "prompt": _styled(FULL_TURTLE, [], **T1)},
        {"name": "turtle-snakeneck", "seed": 5101,
         "prompt": _styled(FULL_TURTLE, [N_NECK], **T1)},
        {"name": "turtle-snakeneck-b", "seed": 5102,
         "prompt": _styled(FULL_TURTLE, [N_NECK], **T1)},
        {"name": "turtle-snakeneck-c", "seed": 5103,
         "prompt": _styled(FULL_TURTLE, [N_NECK], **T1)},
    ],
}

T2 = dict(pose="它正在泥岸上爬行、侧身朝向镜头：",
          scene="on the muddy bank of a marsh pool, wet silt and trampled reeds",
          light="flat overcast light",
          lens="a level camera at eye height, 400mm lens at f/4, the whole body in frame")

ROUNDS[4] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 5101,
    "note": "期 02 定稿【湿地泥岸·阴天·平视全身 400mm】：龟底座 + 蛇尾 N2（两个 take）；含同轮底座对照",
    "shots": [
        {"name": "base-turtle", "seed": 5101, "prompt": _styled(FULL_TURTLE, [], **T2)},
        {"name": "turtle-snaketail", "seed": 5101,
         "prompt": _styled(FULL_TURTLE, [N_TAIL], **T2)},
        {"name": "turtle-snaketail-b", "seed": 5102,
         "prompt": _styled(FULL_TURTLE, [N_TAIL], **T2)},
        {"name": "turtle-snaketail-c", "seed": 5103,
         "prompt": _styled(FULL_TURTLE, [N_TAIL], **T2)},
    ],
}

T4 = dict(pose="它伏在湿石上、侧身朝向镜头：",
          scene="on rain-soaked stones in a mountain stream",
          light="backlight through the spray, rimming its outline",
          lens="a level camera at eye height, 400mm lens at f/4")

ROUNDS[5] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 5101,
    "note": "期 04 定稿【雨后溪石·逆光·平视 400mm·横】：龟底座 + 蛇颈 N1 + 蛇尾 N2；含同轮底座对照",
    "shots": [
        {"name": "base-turtle", "seed": 5101, "prompt": _styled(FULL_TURTLE, [], **T4)},
        {"name": "turtle-neck-tail", "seed": 5101,
         "prompt": _styled(FULL_TURTLE, [N_NECK, N_TAIL], **T4)},
        {"name": "turtle-neck-tail-b", "seed": 5102,
         "prompt": _styled(FULL_TURTLE, [N_NECK, N_TAIL], **T4)},
    ],
}

T5 = dict(pose="它伏在水边的石台上、身体横向展开：",
          scene="on a flat stone at the edge of dark water at dusk",
          light="low backlight from across the water, throwing the animal into near-silhouette",
          lens="a wide-angle 35mm lens at eye height, f/4, the whole animal and its reflection in frame")

D_ALL3 = [N_NECK, N_TAIL, N_COIL_OK]

assert len(D_ALL3) == 3
assert sum("coil" in p for p in D_ALL3) == 1, "缠体只放一处"

ROUNDS[6] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 5101,
    "note": "期 05 收官【玄武】：龟底座 + 蛇颈 N1 + 蛇尾 N2 + 缠体 N3；暮色水面·平视广角·横幅",
    "shots": [
        {"name": "base-turtle", "seed": 5101, "prompt": _styled(FULL_TURTLE, [], **T5)},
        {"name": "turtle-all3", "seed": 5101,
         "prompt": _styled(FULL_TURTLE, D_ALL3, **T5)},
        {"name": "turtle-all3-b", "seed": 5102,
         "prompt": _styled(FULL_TURTLE, D_ALL3, **T5)},
    ],
}
