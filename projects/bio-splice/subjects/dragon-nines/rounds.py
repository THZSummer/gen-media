"""龙 · 九似子主题的 prompt 权威源与轮次定义。

概念
----
传统**画龙口诀「三停九似」本身就是一张九项部位表**：

    角似鹿、头似驼、眼似兔、项似蛇、腹似蜃、鳞似鱼、爪似鹰、掌似虎、耳似牛
    （王符、罗愿《尔雅翼》、李时珍《本草纲目》等均有记述；「三停九似」见《医暇卮言》等）

所以这个子主题不是我们发明拼接，而是**执行一张古人已经写好的部件表**——
与 cat-eagle 子主题（拆「猫头鹰」这个词）同构，但供体从 1 个变成 8 个动物。

机制契合度（依据本仓 r02–r04 定位的规律）
- 规律 56（移植成败取决于底座有没有"占位"）：蛇**没有**角、耳、爪、掌 → 全是空位，
  属于最容易成的类型；只有「鳞似鱼」是已占位（蛇自己有鳞），预期最难
- 规律 57（危险的是整体名词点名）：移植件一律写成 `X 的 <部位>`
- 规律 59（同区域 ≤2 处）：头部件（角/耳/眼/头）要错开分期，或一期最多两处

底座 = **蛇**（「项似蛇」即身体主轴；蛇也是九似里唯一被反复引用的"本体"）
「腹似蜃」的蜃是神话生物、无真实对应 → 标记为**需视觉代理**，暂不执行。
"""
from __future__ import annotations

PREFIX = "bs-dn"  # bio-splice / dragon-nines

# ---------------------------------------------------------------------------
# 轮内恒定层：CN 取景句 + 生境 + 摄影层
# 生境与 cat-eagle 子主题不同（芦苇湿地而非秋日草甸），但**摄影语言保持一致**，
# 这样两个子主题能并置成一套。
# ---------------------------------------------------------------------------

CN_FRAME = "全身像，一只动物独自占据画面："

MARSH = "among wet reeds at the edge of a misty marsh, the background falling away into soft grey-green bokeh."

PHOTO = (
    "Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast "
    "daylight, muted natural colour, fine surface detail, slight film grain, "
    "no digital sharpening, no text, no watermark."
)

# ---------------------------------------------------------------------------
# 底座：蛇（「项似蛇」）
# ---------------------------------------------------------------------------

FULL_SNAKE = (
    "a large wild snake with its head raised, a blunt scaled head, dark lidless eyes, "
    "a flickering forked tongue, keeled scales along a long muscular body"
)

# ---------------------------------------------------------------------------
# 九似部件（供体只出部位，绝不写成"整只 X"）
#   D1 角似鹿 / D2 头似驼 / D3 眼似兔 / D4 项似蛇（底座本身）
#   D5 腹似蜃（神话，待代理） / D6 鳞似鱼 / D7 爪似鹰 / D8 掌似虎 / D9 耳似牛
# ---------------------------------------------------------------------------

D_ANTLER = "a pair of branching deer antlers"                    # D1 角似鹿
D_CAMEL_HEAD = "an elongated camel's head with a blunt muzzle"  # D2 头似驼
D_RABBIT_EYE = "a pair of round dark rabbit's eyes"              # D3 眼似兔
D_FISH_SCALE = "large overlapping fish scales"                    # D6 鳞似鱼
D_EAGLE_CLAW = "sharp curved eagle talons on the front limbs"     # D7 爪似鹰
D_TIGER_PAW = "broad tiger paws with heavy pads"                  # D8 掌似虎
D_OX_EAR = "a small pointed ox's ear"                             # D9 耳似牛


def _photo(base: str, parts: list[str]) -> str:
    """底座 + 移植部位（插在底座名之后：position = weight）。"""
    head, _, rest = base.partition(" with ")
    joined = " and ".join(parts)
    return f"{CN_FRAME}{head} with {joined}, {rest}. {MARSH} {PHOTO}"


def _base_only() -> str:
    return f"{CN_FRAME}{FULL_SNAKE}. {MARSH} {PHOTO}"


# 守卫：每个移植件必须是"部位"而不是"整只动物"
for _n, _p in (("角", D_ANTLER), ("眼", D_RABBIT_EYE), ("鳞", D_FISH_SCALE),
               ("爪", D_EAGLE_CLAW), ("掌", D_TIGER_PAW), ("耳", D_OX_EAR)):
    assert "a pair of" in _p or "large" in _p or "sharp" in _p or "broad" in _p \
        or "round" in _p or "small" in _p, f"{_n}: 部位描述太弱"
    assert "snake" not in _p, f"{_n}: 移植件里不该出现底座动物"
assert "camel's head" in D_CAMEL_HEAD and "rabbit's eyes" in D_RABBIT_EYE
for _p in (D_ANTLER, D_RABBIT_EYE, D_FISH_SCALE, D_EAGLE_CLAW, D_TIGER_PAW, D_OX_EAR,
           D_CAMEL_HEAD):
    assert " whose " not in _p and "body is entirely" not in _p, "移植件不许用「整只」句式"
assert "with" in FULL_SNAKE, "底座必须是「X with ...」结构，_photo 依赖它"

# 存档抬头用的"轮内恒定层"模板
ARCHIVE_LAYERS = f"{CN_FRAME}<底座 with 部位>. {MARSH} {PHOTO}"

# ---------------------------------------------------------------------------
# 轮次
# ---------------------------------------------------------------------------

ROUNDS: dict[int, dict] = {}

ROUNDS[1] = {
    "engine": "zimage",
    "size": (1024, 1024),
    "steps": 12,
    "seed": 4201,
    "note": "九似·第一期候选：蛇底座 + 鹿角（D1，龙最强的标志）；含同轮底座对照",
    "shots": [
        {"name": "base-snake", "seed": 4201, "prompt": _base_only()},
        {"name": "snake-antler", "seed": 4201, "prompt": _photo(FULL_SNAKE, [D_ANTLER])},
        {"name": "snake-antler-oxear", "seed": 4201,
         "prompt": _photo(FULL_SNAKE, [D_ANTLER, D_OX_EAR])},
        {"name": "snake-antler-claw", "seed": 4201,
         "prompt": _photo(FULL_SNAKE, [D_ANTLER, D_EAGLE_CLAW])},
    ],
}


# ---------------------------------------------------------------------------
# R2：四肢件需要一个有四肢的底座
#
# R1 实测：蛇底座 + 鹰爪 **完全没出现**。原因不是规律 56 的"被底座描述覆盖"，
# 而是**缺少载体结构**——蛇没有前肢，爪无处可长。
#
# 所以 R2 换底座为蜥蜴（有四肢、且同样是蛇形躯干），并且**刻意不描述它的爪**
# （写成 `four stout legs` 而不是 `four clawed legs`），把脚的位置留给移植件。
# 这其实与龙的形象吻合：**中国龙是四足蛇身**——「项似蛇」取蛇，「四足」要另找。
# ---------------------------------------------------------------------------

FULL_LIZARD = (
    "a large monitor lizard with its head raised, a blunt scaled snout, dark lidless "
    "eyes, a flickering forked tongue, four stout legs and a long tapering tail"
)

D_EAGLE_CLAW_FRONT = "sharp curved eagle talons on its front feet"
D_TIGER_PAW_HIND = "broad tiger paws with heavy pads on its hind feet"

assert "with" in FULL_LIZARD
assert "claw" not in FULL_LIZARD and "talon" not in FULL_LIZARD, "R2: 底座不许先占住爪的位置"
assert "eagle talons" in D_EAGLE_CLAW_FRONT and "tiger paws" in D_TIGER_PAW_HIND

ROUNDS[2] = {
    "engine": "zimage",
    "size": (1024, 1024),
    "steps": 12,
    "seed": 4201,
    "note": "九似·第二期候选：蜥蜴底座（有四肢）+ 鹰爪 D7 / 虎掌 D8；含同轮底座对照",
    "shots": [
        {"name": "base-lizard", "seed": 4201,
         "prompt": f"{CN_FRAME}{FULL_LIZARD}. {MARSH} {PHOTO}"},
        {"name": "lizard-talons", "seed": 4201,
         "prompt": _photo(FULL_LIZARD, [D_EAGLE_CLAW_FRONT])},
        {"name": "lizard-talons-paws", "seed": 4201,
         "prompt": _photo(FULL_LIZARD, [D_EAGLE_CLAW_FRONT, D_TIGER_PAW_HIND])},
    ],
}


# ---------------------------------------------------------------------------
# R3：鳞似鱼（D6）—— 测"腾出占位"的手法
#
# D6 是九似里唯一**已占位**的部位：蛇自己有鳞，而 R1 的底座描述里明确写了
# `keeled scales along a long muscular body`。按规律 56，移植件会被底座描述覆盖
# （cat-eagle 的"猫掌"就是这样失败的）。
#
# 对策：**把底座里描述该部位的那几个词删掉**，把位置腾出来——
# 与 R2 在蜥蜴底座上刻意不写 `clawed` 是同一个手法。
# 底座与 R1 的差别**只有"删掉鳞的描述"这一处**，这样才归因得清。
# ---------------------------------------------------------------------------

FULL_SNAKE_CLEAN = FULL_SNAKE.replace("a blunt scaled head", "a blunt head").replace(
    ", keeled scales along a long muscular body", ", and a long smooth muscular body")

assert "scale" not in FULL_SNAKE_CLEAN, "R3: 底座还有鳞的描述，占位没腾出来"
assert FULL_SNAKE_CLEAN != FULL_SNAKE
assert "keeled scales" in FULL_SNAKE, "R3: 基线没变"

ROUNDS[3] = {
    "engine": "zimage",
    "size": (1024, 1024),
    "steps": 12,
    "seed": 4201,
    "note": "九似·第三期候选：鱼鳞 D6（把底座里鳞的描述删掉腾出占位）；含同轮底座对照",
    "shots": [
        {"name": "base-snake-clean", "seed": 4201,
         "prompt": f"{CN_FRAME}{FULL_SNAKE_CLEAN}. {MARSH} {PHOTO}"},
        {"name": "snake-fishscale", "seed": 4201,
         "prompt": _photo(FULL_SNAKE_CLEAN, [D_FISH_SCALE])},
        {"name": "snake-fishscale-antler", "seed": 4201,
         "prompt": _photo(FULL_SNAKE_CLEAN, [D_ANTLER, D_FISH_SCALE])},
    ],
}


# ---------------------------------------------------------------------------
# R4：合龙 —— 在**有四肢**的蜥蜴底座上叠多件（收官期）
#
# 到 R3 为止，九似里可行的部件是：角 D1（头）、耳 D9（头）、爪 D7（前肢）、掌 D8（后肢）。
# 合龙要把它们叠到同一个体上，于是正好压住规律 59 的边界：
#   头部 2 处（角+耳）✅ 允许；前肢 1 处、后肢 1 处 ✅
# 两个变体分别测 3 处（头 1 + 四肢 2）与 4 处（头 2 + 四肢 2），看叠加极限在哪。
#
# 底座沿用 R2 的蜥蜴（有四肢、且**没描述爪**），所以两个变体只差"叠了几件"。
# ---------------------------------------------------------------------------

D_DRAGON_3 = [D_ANTLER, D_EAGLE_CLAW_FRONT, D_TIGER_PAW_HIND]
D_DRAGON_4 = [D_ANTLER, D_OX_EAR, D_EAGLE_CLAW_FRONT, D_TIGER_PAW_HIND]

assert len(D_DRAGON_3) == 3 and len(D_DRAGON_4) == 4
# 区域分布守卫：头部不超过 2 处（规律 59）
assert sum("antler" in p or "ox's ear" in p for p in D_DRAGON_4) == 2, "R4: 头部超过 2 处"

ROUNDS[4] = {
    "engine": "zimage",
    "size": (1024, 1024),
    "steps": 12,
    "seed": 4201,
    "note": "九似·第四期候选【合龙】：蜥蜴底座 + 3 处 / 4 处部件叠加；含同轮底座对照",
    "shots": [
        {"name": "base-lizard", "seed": 4201,
         "prompt": f"{CN_FRAME}{FULL_LIZARD}. {MARSH} {PHOTO}"},
        {"name": "dragon-3parts", "seed": 4201, "prompt": _photo(FULL_LIZARD, D_DRAGON_3)},
        {"name": "dragon-4parts", "seed": 4201, "prompt": _photo(FULL_LIZARD, D_DRAGON_4)},
    ],
}


# ---------------------------------------------------------------------------
# R5–R7：把"期"做出各自的**特点**（定稿轮）
#
# 问题：R1–R4 四期的**生境 / 光线 / 机位 / 画布**完全相同，只有移植件在变 ——
# 于是四期读起来像"同一张照片加了不同的件"，没有各自的身份。
#
# 原因是我把**期内对照**的纪律（层恒定）错用到了**跨期**上。正确分工：
#   期内恒定 → 保证该期的 A/B（移植 vs 底座对照）可比
#   期间各异 → 让每期有自己的身份
#
# 所以 R5–R7 保持各期的底座与移植件**不变**（机制结论照旧成立），
# 只把呈现层换成该期专属，而且**按主体选机位**：
#
#   期 01（鹿角）  晨雾芦苇 · 黎明柔光 · 平视 600mm · 方 1024²  ← R1 已是这个look，保留
#   期 02（鹰爪）  **卵石河滩雨后 · 低机位贴地、聚焦前足 · 竖 1024×1280**  ← 爪是主角
#   期 03（鱼鳞）  **林下枯叶 · 斑驳林间光 · 侧俯贴体、鳞列满画 · 方**      ← 鳞是主角
#   期 04（合龙）  **雨中岩石 · 黄昏逆光 + 雨丝 · 广角低机位 · 横 1280×1024** ← 气势
#
# 机位不是随便挑的：期 02/03 的主体（爪、鳞）正是前两轮**只到"部分成立"**的部位，
# 把镜头对准它们，既给了期身份，也顺带提高这些部位的可读性。
# ---------------------------------------------------------------------------

PHOTO_BASE = ("fine surface detail, slight film grain, no digital sharpening, "
              "no text, no watermark")


def _styled(base: str, parts: list[str], *, pose: str, scene: str, light: str, lens: str,
            frame: str = CN_FRAME) -> str:
    """期专属呈现：{CN 取景句}{姿态}{底座 with 部位}. {生境} {光线} {镜头} {摄影底子}

    ``frame`` 默认是全身像取景；**特写期必须覆盖它**——否则 CN 层说"全身像"、
    摄影层说"tight close-up"，两句互相打架。
    """
    head, _, rest = base.partition(" with ")
    joined = " and ".join(parts) if parts else ""
    core = f"{head} with {joined}, {rest}" if parts else base
    return (f"{frame}{pose}{core}. {scene}. {light}. "
            f"Wildlife photograph, {lens}, {PHOTO_BASE}.")


# 期 02 定稿（R5）：卵石河滩 · 雨后侧逆光 · 低机位聚焦前足 · 竖幅
S2 = dict(pose="它以后肢撑起上身、两前足抬起张开：",
          scene="on a wet pebble riverbank just after rain, water still sheeting over the stones",
          light="wet overcast light with a soft backlight rimming its body",
          lens="a low ground-level camera angle, 85mm lens at f/3.2, very shallow depth of field")
# 期 03 定稿（R6）：林下枯叶 · 斑驳林光 · 侧俯贴体 · 方向
S3 = dict(pose="它把身体平铺在地、整个背脊朝向镜头：",
          scene="on damp leaf litter deep on a forest floor",
          light="dappled light falling through the canopy",
          lens="100mm macro lens, side view from slightly above, f/5.6, the whole length of the body in focus")
# 期 04 定稿（R7）：雨中岩石 · 黄昏逆光 + 雨丝 · 广角低机位 · 横幅
S4 = dict(pose="它昂首挺立、四肢张开、全身展开：",
          scene="on a rain-slicked rock outcrop",
          light="dusk backlight through falling rain, water beading along its back",
          lens="a wide-angle 35mm lens at a low angle, f/4")

ROUNDS[5] = {
    "engine": "zimage", "size": (1024, 1280), "steps": 12, "seed": 4201,
    "note": "期 02 定稿【卵石河滩·低机位聚焦前足】：蜥蜴底座 + 鹰爪 D7（+虎掌 D8）",
    "shots": [
        {"name": "base-lizard", "seed": 4201, "prompt": _styled(FULL_LIZARD, [], **S2)},
        {"name": "lizard-talons", "seed": 4201,
         "prompt": _styled(FULL_LIZARD, [D_EAGLE_CLAW_FRONT], **S2)},
        {"name": "lizard-talons-paws", "seed": 4201,
         "prompt": _styled(FULL_LIZARD, [D_EAGLE_CLAW_FRONT, D_TIGER_PAW_HIND], **S2)},
    ],
}

ROUNDS[6] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 4201,
    "note": "期 03 定稿【林下枯叶·侧俯贴体看鳞】：蛇底座（腾出鳞占位）+ 鱼鳞 D6（+鹿角 D1）",
    "shots": [
        {"name": "base-snake", "seed": 4201, "prompt": _styled(FULL_SNAKE_CLEAN, [], **S3)},
        {"name": "snake-fishscale", "seed": 4201,
         "prompt": _styled(FULL_SNAKE_CLEAN, [D_FISH_SCALE], **S3)},
        {"name": "snake-fishscale-antler", "seed": 4201,
         "prompt": _styled(FULL_SNAKE_CLEAN, [D_ANTLER, D_FISH_SCALE], **S3)},
    ],
}

ROUNDS[7] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 4201,
    "note": "期 04 定稿【雨中岩石·黄昏逆光】合龙：蜥蜴底座 + 角/耳/爪/掌",
    "shots": [
        {"name": "base-lizard", "seed": 4201, "prompt": _styled(FULL_LIZARD, [], **S4)},
        {"name": "dragon-3parts", "seed": 4201,
         "prompt": _styled(FULL_LIZARD, D_DRAGON_3, **S4)},
        {"name": "dragon-4parts", "seed": 4201,
         "prompt": _styled(FULL_LIZARD, D_DRAGON_4, **S4)},
    ],
}


# ---------------------------------------------------------------------------
# R8：期 05 收官【九似小成】—— 头似驼 D2 + 眼似兔 D3
#
# 先纠正一处**规划时的误判**：PLAN.md 把 D3 兔眼当作"空位新增 → 易"，
# 但底座 FULL_SNAKE 里写明了 `dark lidless eyes`——**眼位是被占住的**，
# 与 D6 鳞同属"腾出占位"。
#
# 于是本轮要同时腾出两处（头形 + 眼），而这正是收官期该测的东西：
#   D2 驼头 = **头是整体名词位**（规律 57 里最危险的一类），预期最难
#   D3 兔眼 = 腾出占位的小部件，识别度低
#   两件都落在**头部** → 头部正好 2 处，压在规律 59 的上限（规律 68：数区域不数件数）
#
# 为了能归因，本轮做成 2×2 消融：
#   base-snake-open   底座腾出两处后长什么样（对照）
#   snake-camelhead   只加 D2  → 测驼头单独能否落地
#   snake-rabbiteyes  只加 D3  → 测兔眼单独能否落地
#   dragon-head-eyes  D2 + D3  → 测"头 + 眼"同区域两件是否互相挤掉
#
# 底座与 FULL_SNAKE 的差别**只有删掉这两处描述**，其余一字不动。
# ---------------------------------------------------------------------------

FULL_SNAKE_OPEN = (FULL_SNAKE.replace("a blunt scaled head, ", "")
                   .replace("dark lidless eyes, ", "")
                   .replace("its head raised", "its neck lifted"))

assert "scaled head" not in FULL_SNAKE_OPEN and "lidless" not in FULL_SNAKE_OPEN
assert "its head raised" not in FULL_SNAKE_OPEN, "R8: 头部的名词也要腾掉"
assert "a flickering forked tongue" in FULL_SNAKE_OPEN, "R8: 除头眼外不该动到别的描述"

# 期 05 呈现：晨雾芦苇 · 侧逆光勾轮廓 · **贴面特写** · 方
# 生境与期 01 同为芦苇湿地，但身份由**机位**（贴面特写）与**光线**（侧逆光勾边）承担：
# 特写下背景化成一团灰，与期 01 的平视全身像不会读串。
# 注意 frame 必须跟着改成"头部特写"——CN 取景句与摄影层不能一句说全身一句说特写。
S5 = dict(frame="头部特写，一只动物独自占据画面：",
          pose="它昂起头颈、正面朝向镜头：",
          scene="at the edge of a misty marsh before sunrise, the far bank lost in grey",
          light="low side-backlight from the first light, rimming the outline of the head",
          lens="a tight close-up portrait of the head and neck, 200mm lens at f/4, "
               "the background dissolved into soft grey")

ROUNDS[8] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 4201,
    "note": "期 05 收官【九似小成】：蛇底座（腾出头+眼占位）+ 驼头 D2 / 兔眼 D3（2×2 消融）",
    "shots": [
        {"name": "base-snake-open", "seed": 4201,
         "prompt": _styled(FULL_SNAKE_OPEN, [], **S5)},
        {"name": "snake-camelhead", "seed": 4201,
         "prompt": _styled(FULL_SNAKE_OPEN, [D_CAMEL_HEAD], **S5)},
        {"name": "snake-rabbiteyes", "seed": 4201,
         "prompt": _styled(FULL_SNAKE_OPEN, [D_RABBIT_EYE], **S5)},
        {"name": "dragon-head-eyes", "seed": 4201,
         "prompt": _styled(FULL_SNAKE_OPEN, [D_CAMEL_HEAD, D_RABBIT_EYE], **S5)},
    ],
}


# ---------------------------------------------------------------------------
# R9：R8 全军覆没后的追问 —— **底座的物种名词本身就是一个占位**
#
# R8 实测：把头形与眼的描述都从底座里删掉（腾出占位）、再写 D2 驼头 / D3 兔眼，
# **一件都没落地**——四张全是同一条蛇，而且是眼镜蛇（比底座原文还"蛇"）。
# 说明腾出占位在这里无效：模型回退到了它自己的蛇先验。
#
# 假设：占位的来源不只是**描述该部位的词**，还有**底座的物种名词本身**。
# `a large wild snake ...` 里的 `snake` 一词携带了整个蛇形先验（含头形与眼），
# 只要这个词还在，头部腾得再干净也会被它填回去。
#
# 这是规律 57（危险的是整体名词点名）的**镜像**：
#   移植件点名整只动物 → 拖出整只供体（已知）
#   底座点名整只动物   → 拖出整个底座物种的典范形态（本轮要测的）
#
# 测法：底座**不写物种名**，只描述可观察的部位（长躯干 + 鳞 + 分叉舌），
# 看 D2 驼头能不能在"无先验"底座上落地。
#
# 同轮另出期 05 的备选定稿：既然 D2/D3 走不通，收官期改用**已实测成立**的
# 头部件排一组龙首特写（角 D1 + 耳 D9 [+ 鳞 D6]），头部 2 处（规律 59/68）。
# ---------------------------------------------------------------------------

FULL_NOSPECIES = "a long muscular low body with keeled scales and a flickering forked tongue"

assert "snake" not in FULL_NOSPECIES and "lizard" not in FULL_NOSPECIES
assert " with " in FULL_NOSPECIES, "_styled 依赖「X with ...」结构"
assert "head" not in FULL_NOSPECIES and "eye" not in FULL_NOSPECIES, "R9: 无先验底座不许提头眼"

D_DRAGON_HEAD = [D_ANTLER, D_OX_EAR]                      # 头部 2 处
D_DRAGON_HEAD_SCALE = [D_ANTLER, D_OX_EAR, D_FISH_SCALE]  # 头 2 + 体 1

assert sum("antler" in p or "ox's ear" in p for p in D_DRAGON_HEAD_SCALE) == 2

ROUNDS[9] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 4201,
    "note": "期 05 候选【龙首特写】：测「底座物种名词=占位」；另出角/耳/鳞的龙首特写",
    "shots": [
        {"name": "base-nospecies", "seed": 4201,
         "prompt": _styled(FULL_NOSPECIES, [], **S5)},
        {"name": "nospecies-camelhead", "seed": 4201,
         "prompt": _styled(FULL_NOSPECIES, [D_CAMEL_HEAD], **S5)},
        {"name": "nospecies-camelhead-eye", "seed": 4201,
         "prompt": _styled(FULL_NOSPECIES, [D_CAMEL_HEAD, D_RABBIT_EYE], **S5)},
        {"name": "snake-antler-oxear", "seed": 4201,
         "prompt": _styled(FULL_SNAKE, D_DRAGON_HEAD, **S5)},
        {"name": "snake-antler-oxear-scale", "seed": 4201,
         "prompt": _styled(FULL_SNAKE_CLEAN, D_DRAGON_HEAD_SCALE, **S5)},
    ],
}


# ---------------------------------------------------------------------------
# R10：期 05 定稿【龙首特写】—— 只把 R9 验证过的组合补齐**同轮底座对照**
#
# R9 的第 4/5 张（角+耳 / 角+耳+鳞）已经成立，但那一轮的同轮对照是
# `base-nospecies`——与它们用的底座（FULL_SNAKE / FULL_SNAKE_CLEAN）不是同一个，
# 所以客观指标对这两张不可用（项目纪律：每轮必须有同轮、同 seed、同句式的底座对照）。
# 本轮补上这个对照，其余一字不动。
# ---------------------------------------------------------------------------

ROUNDS[10] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 4201,
    "note": "期 05 定稿【龙首特写】：蛇底座（特写）+ 角 D1 / 耳 D9（+鳞 D6）；含同轮底座对照",
    "shots": [
        {"name": "base-snake", "seed": 4201,
         "prompt": _styled(FULL_SNAKE, [], **S5)},
        {"name": "dragon-head", "seed": 4201,
         "prompt": _styled(FULL_SNAKE, D_DRAGON_HEAD, **S5)},
        {"name": "dragon-head-scale", "seed": 4201,
         "prompt": _styled(FULL_SNAKE_CLEAN, D_DRAGON_HEAD_SCALE, **S5)},
    ],
}
