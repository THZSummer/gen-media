"""猼訑（山海經 · 南山經 · 基山）—— 考据记录与轮次 prompt 定义。

底本：郭璞注本《山海經》卷一 · 南山經（識典古籍 SK2098，四庫全書本，2026-10-06 核对）；
      另以四部叢刊本（SBCK099，郭璞注、黃丕烈校勘）复核，两本此段一致（仅标点小异）。
原文（逐字核对；繁体与底本标点照录）：

    又東三百里，曰基山。其陽多玉，其陰多怪木。有獸焉，其狀如羊，九尾四耳，
    其目在背，其名曰猼訑，佩之不畏。

  ▸ 紧接其后的「有鳥焉，其狀如雞，而三首六目、六足三翼，其名曰𪁺𩿧，食之無臥」
    写的是**基山上的鸟**，属另一件，**不入本件原文区**（原文区为从山名到猼訑句中连续的一段，
    不跳字、不加省略号）——与鹿蜀期把「旋龜」排除在外是同一条体例。
  ▸ 字形：識典古籍的简体排印把「訑」作「𫍙」（U+2B359，非 BMP／扩展 C），四部叢刊本同。
    本件从**通行繁体字形「訑」**（U+8A11）。理由两条：① 教育部《重編國語辭典》与《太平御覽》
    引文均作「訑」；② 𫍙 非 BMP，Noto Serif CJK 无字形，制版根本渲染不出（`font_coverage.py` 会拒）。
  ▸ 读音：郭璞注「博施二音。施一作陁」→ 旧读 bó shī；今通行读 **bó yí**（教育部辭典 ㄅㄛˊ ㄧˊ），
    slug 取 `bo-yi`。
  ▸ 校记（留档，不入成品）：《太平御覽》卷九一三引作「九尾四目」（四**目**），各本《山海經》作
    「四耳」→ 从底本作四耳。《山海經圖贊》：「猼訑似羊，眼乃在背。視之則奇，推之無怪。若欲不恐，
    厥皮可佩。」可作「目在背」的旁证。

可验特征（验收硬指标，逐项落地才拿 A 分）：
  1. 羊身 —— 其狀如羊
  2. 九尾 —— 九尾（**可数**：目视点数，读作九条即可）
  3. 四耳 —— 四耳（**可数**：四只耳朵，注意不是两只）
  4. 目在背 —— 其目在背（**反常识部位**：背上有眼睛；面部仍作羊脸，底本未说它无面目）

骨法（期内恒定，与九尾狐 / 鹿蜀定稿同一句）：赭石设色工笔 / 册页、淡彩陈年纸本。
"""

SLUG = "bo-yi"
NAME_ZH = "猼訑"
NAME_EN = "bo-yi"
VOLUME = "山海經 · 南山經"
VOLUME_EN = "Shan Hai Jing · Nan Shan Jing"
PLACE = "基山"
PASSAGE = ("又東三百里，曰基山。其陽多玉，其陰多怪木。"
           "有獸焉，其狀如羊，九尾四耳，其目在背，其名曰猼訑，佩之不畏。")
COVER_LINE = "佩之不畏"          # 点睛句（原文原字，不另作白话）

CANVAS = {"width": 1024, "height": 1360}   # 与九尾狐 / 鹿蜀同画布，系列一致
STEPS = 20
ENGINE = "z-image-turbo"

# 骨法句与九尾狐 R7、鹿蜀定稿逐字相同 —— 换兽不换骨法，才能评"系列一致"
STYLE = ("Painted in the manner of a traditional Chinese album leaf, fine ink brushwork, "
         "delicate fur strokes, ink and pale colour on aged paper.")

# R1 设计：写法扫描，三个变体 × 三个 seed（沿用前两件 R1 的 seed，便于横向比）
#   v1 英文点名（承 R7/R1 结论：点名才有该兽）
#   v2 特征逐项前置（把四条硬指标逐条写出，看计数特征与"目在背"能不能一起落地）
#   v3 中文直述（**同轮底座对照**：前两件两轮 6/6 失败，这里再验一次）
# 本轮要回答的问题：九尾 + 四耳 + 目在背 这三条能不能同时出现？模型会不会把"背上的眼睛"
# 抹掉、或误当成背上的斑纹/盾牌（这是它最容易失败的地方）。
VARIANTS = {
    "v1": ("The bo-yi of Chinese mythology, a sheep with nine tails, four ears and a pair of "
           "eyes on its back, standing in profile on a rocky ledge. " + STYLE),
    "v2": ("A sheep of Chinese mythology with nine long tails, four ears and a pair of eyes set "
           "in its back; it is called the bo-yi and stands in profile on a rocky ledge. " + STYLE),
    "v3": ("《山海經》異獸猼訑：羊的身子、九條尾巴、四隻耳朵，背上還長著眼睛；"
           "側身立於山石之上。中國傳統冊頁淡彩：工筆、赭石與墨、陳年紙本、大量留白。"),
}
SEEDS = {"v1": [101, 202, 303], "v2": [101, 202, 303], "v3": [101, 202, 303]}

# R2 设计：R1 的结论是**三条特征 0/9**（九张全是普通盘羊：一条短尾、两只耳、背上无眼）。
#   R1 的形态句用了 "a sheep with nine tails, four ears and a pair of eyes on its back" 这种
#   **介词短语**写法；而九尾狐能出九尾靠的是 "nine-tailed fox" 这种**复合形容词**写法 ——
#   那是一个训练数据里就有的固定说法。R2 就试三种"把计数塞进名词短语 / 明确对比"的写法：
#   w1 复合形容词当头（nine-tailed, four-eared …）
#   w2 明确对比 + 数词拼写（is no ordinary sheep: nine tails, four ears …）
#   w3 明确对比 + 阿拉伯数字（not an ordinary sheep: 9 tails, 4 ears …）—— Qwen3 文本编码器读数字
#   w4 中文对照（**同轮底座对照**，前两件的中文直述两轮 6/6 失败，这里再验一次）
#   seed 换新（404/505/606），避免与 R1 撞图。
VARIANTS_R2 = {
    "w1": ("The nine-tailed, four-eared bo-yi of Chinese mythology, a woolly sheep-like beast with "
           "a pair of eyes set in its back, standing in profile on a rocky ledge. " + STYLE),
    "w2": ("The bo-yi of Chinese mythology is no ordinary sheep: it has nine tails, four ears and "
           "two extra eyes on its back. It stands in profile on a rocky ledge. " + STYLE),
    "w3": ("The bo-yi of Chinese mythology is not an ordinary sheep: 9 tails, 4 ears and 2 eyes on "
           "its back. It stands in profile on a rocky ledge. " + STYLE),
    "w4": ("《山海經》異獸猼訑：不是普通的羊——九條尾巴、四隻耳朵，背上還有一雙眼睛；"
           "側身立於山石之上。中國傳統冊頁淡彩：工筆、赭石與墨、陳年紙本、大量留白。"),
}

# R3 设计：R2 的结论是「复合形容词写法**部分**起效」——w1（nine-tailed, four-eared …）
#   多画出了 2–3 条尾部羽状影，另三式仍是单尾；四耳与目在背**一张都没出现**。
#   本地另一条引擎 Qwen-Image 还没试：它的文本编码器是 Qwen2.5-VL（中文更强），而且
#   **支持真负向**（Z-Image 的负向是 ConditioningZeroOut，传了等于没传，cfg=1）。
#   所以 R3 把 R2 里最有效的两种写法搬过去，并加上"普通羊"的负向：
#   q1 复合形容词（R2 w1）+ 负向 / q2 明确对比 + 数词（R2 w2）+ 负向 / q3 中文新版 + 中文负向
#   seed 707 / 808，每式 2 张（Qwen-Image 单张比 Z-Image 慢，先看方向）
NEG_EN = ("an ordinary sheep, a single tail, two ears, no eyes on the back, "
          "photorealistic, 3d render, photograph")
NEG_ZH = "普通的羊，只有一条尾巴、两只耳朵，背上没有眼睛，照片，3D 渲染"
VARIANTS_R3 = {
    "q1": VARIANTS_R2["w1"],
    "q2": VARIANTS_R2["w2"],
    "q3": ("《山海經》異獸猼訑：**九條**尾巴、**四隻**耳朵，背上另有一雙眼睛；"
           "側身立於山石之上。中國傳統冊頁淡彩：工筆、赭石與墨、陳年紙本、大量留白。"),
}
NEGATIVES_R3 = {"q1": NEG_EN, "q2": NEG_EN, "q3": NEG_ZH}

# R4 设计：R3 的结论是「换引擎就成立了」——Qwen-Image + 复合形容词写法（q1）两张都拿到
#   羊身 / 多尾 / 多耳 / 背上眼，而且**四角机械筛 0 候选**（Z-Image 那套"必盖印"的先验
#   在 Qwen 上不成立）。但 q1/q2 都是**墨线（白描）**调子，与系列现用的**赭石设色**不是一个调，
#   E 系列一致要掉档。R4 只动"色"这一件事，两种写法各 3 seed：
#   c1 把骨法句改写成"墨线 + 赭石/暖褐/淡青罩染"（与 STYLE 同义、但显式点色）
#   c2 **保留 STYLE 逐字不动**，只在其后追加一句明确设色 —— 这样系列一致句仍然逐字相同
#   负向沿用 R3 的 NEG_EN（普通羊 / 单尾 / 两耳 / 背上无眼）。
STYLE_PIGMENT = ("Painted in the manner of a traditional Chinese album leaf: fine ink brushwork "
                 "washed with soft ochre, warm brown and pale green, delicate fur strokes, "
                 "on aged paper.")
VARIANTS_R4 = {
    "c1": ("The nine-tailed, four-eared bo-yi of Chinese mythology, a woolly sheep-like beast with "
           "a pair of eyes set in its back, standing in profile on a rocky ledge. " + STYLE_PIGMENT),
    "c2": (VARIANTS_R2["w1"] + " The ink lines are washed with soft ochre and warm brown."),
}

ROUNDS = {
    1: {
        "note": ("R1 写法扫描：英文点名 / 特征逐项前置 / 中文直述（同轮底座对照）× 3 seed，"
                 "看「羊身 + 九尾 + 四耳 + 目在背」四条能不能同时落地，以及背上的眼睛会不会被抹掉。"
                 "**结果：三条特征 0/9** —— 九张全是普通盘羊（一条短尾、两只耳、背上无眼）；"
                 "形态句写成介词短语（a sheep with nine tails）没用，见 R2"),
        "shots": [
            {"id": f"{v}-{s}", "variant": v, "prompt": p, "seed": s,
             "width": CANVAS["width"], "height": CANVAS["height"], "steps": STEPS}
            for v, p in VARIANTS.items() for s in SEEDS[v]
        ],
    },
    2: {
        "note": ("R2 计数写法轮：R1 三条特征 0/9（模型画的是普通盘羊）。本轮试三种把计数塞进"
                 "名词短语/明确对比的写法（复合形容词 / no ordinary sheep + 数词拼写 / + 阿拉伯数字）"
                 "＋中文同轮底座对照，每式 3 seed。**结果：仍 0/12 达标** —— "
                 "w1 复合形容词写法让模型多画了 2–3 条尾部羽状影（唯一有反应的一式），"
                 "四耳与目在背一张都没出现 → 换引擎（R3 Qwen-Image + 真负向）"),
        "shots": [
            {"id": f"{v}-{s}", "variant": v, "prompt": p, "seed": s,
             "width": CANVAS["width"], "height": CANVAS["height"], "steps": STEPS}
            for v, p in VARIANTS_R2.items() for s in (404, 505, 606)
        ],
    },
    # R3 换引擎：Qwen-Image（同机，免费；支持真负向）
    3: {
        "note": ("R3 换引擎轮（Qwen-Image）：把 R2 最有反应的复合形容词写法、明确对比写法，"
                 "以及中文新版，各配一条「普通羊／单尾／两耳／背上无眼」的负向，每式 2 seed。"
                 "**结果：英文两式成立（羊身 + 多尾 + 多耳 + 背上眼），中文那式画成了狐狸**"
                 "（模型把「異獸 + 九尾」联想成了九尾狐）；Qwen 出的四张机械筛 0 候选 → R4 补设色"),
        "shots": [
            {"id": f"{v}-{s}", "variant": v, "prompt": p, "negative": NEGATIVES_R3[v], "seed": s,
             "width": CANVAS["width"], "height": CANVAS["height"], "steps": STEPS}
            for v, p in VARIANTS_R3.items() for s in (707, 808)
        ],
    },
    # R4 补色：Qwen-Image 已成立，只把"墨线"补成系列的"赭石设色"
    4: {
        "note": ("R4 设色轮（Qwen-Image）：R3 的形态句成立但调子是白描墨线，本轮只动色 —— "
                 "c1 改写骨法句为墨线 + 赭石/暖褐/淡青罩染；c2 保留 STYLE 逐字不动、追加一句设色；"
                 "每式 3 seed，负向同 R3"),
        "shots": [
            {"id": f"{v}-{s}", "variant": v, "prompt": p, "negative": NEG_EN, "seed": s,
             "width": CANVAS["width"], "height": CANVAS["height"], "steps": STEPS}
            for v, p in VARIANTS_R4.items() for s in (909, 1010, 1111)
        ],
    },
}
