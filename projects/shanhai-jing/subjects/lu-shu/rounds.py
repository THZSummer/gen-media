"""鹿蜀（山海經 · 南山經 · 杻陽之山）—— 考据记录与轮次 prompt 定义。

底本：郭璞注本《山海經》卷一 · 南山經（識典古籍 SK2098，2026-10-06 核对）
原文（逐字核对，**异体字保留底本写法**；底本标点亦照录）：

    又東三百七十里曰杻陽之山。其陽多赤金，其陰多白金。有獸焉，其狀如馬而白首，
    其文如虎而赤尾，其音如謡，其名曰鹿蜀，佩之宜子孫。

  ▸ 紧接其后的「怪水出焉……其名曰旋龜……」写的是同一座山里的另一种生物（旋龜），
    属另一件，**不入本件原文区**（原文区为从山名到鹿蜀句中连续的一段，不跳字、不加省略号）。
  ▸ 「謡」按底本作謡（不作谣）；「杻」音 niǔ。

可验特征（验收硬指标，逐项落地才拿 A 分）：
  1. 馬身 —— 状如马
  2. 白首 —— 头是白的
  3. 虎紋 —— 身上有虎一样的斑纹
  4. 赤尾 —— 尾巴是赤红的

骨法（期内恒定，与九尾狐定稿同一句）：赭石设色工笔 / 册页、淡彩陈年纸本。
"""

SLUG = "lu-shu"
NAME_ZH = "鹿蜀"
NAME_EN = "lu-shu"
VOLUME = "山海經 · 南山經"
VOLUME_EN = "Shan Hai Jing · Nan Shan Jing"
PLACE = "杻陽之山"
PASSAGE = ("又東三百七十里曰杻陽之山。其陽多赤金，其陰多白金。"
           "有獸焉，其狀如馬而白首，其文如虎而赤尾，其音如謡，"
           "其名曰鹿蜀，佩之宜子孫。")
COVER_LINE = "佩之宜子孫"          # 点睛句（原文原字，不另作白话）

CANVAS = {"width": 1024, "height": 1360}   # 与九尾狐同画布，系列一致
STEPS = 20
ENGINE = "z-image-turbo"

# 骨法句与九尾狐 R7 定稿逐字相同 —— 换兽不换骨法，才能评"系列一致"
STYLE = ("Painted in the manner of a traditional Chinese album leaf, fine ink brushwork, "
         "delicate fur strokes, ink and pale colour on aged paper.")

# R1 设计：三个变体 × 三个 seed，先回答"名字 vs 特征列举 vs 中文直述 哪种写法把三特征都画对"
#   v1 点名式（承 R7 结论：点名才有该兽）
#   v2 特征前置逐项（把三条硬指标逐条写出，看能不能逼出全部落地）
#   v3 中文直述（Z-Image 的文本编码器是 Qwen3-4B，中文理解更强；同时看它会不会把汉字画进画面）
VARIANTS = {
    "v1": ("The lu-shu of Chinese mythology, a white-headed horse with tiger stripes on its "
           "body and a red tail, standing in profile on a rocky ledge. " + STYLE),
    "v2": ("A horse of Chinese mythology with a pure white head, a body covered in black tiger "
           "stripes and a long cinnabar-red tail; it is called the lu-shu and stands in profile "
           "on a rocky ledge. " + STYLE),
    "v3": ("《山海經》中的異獸鹿蜀：馬的身子、白色的頭、虎一樣的斑紋、赤紅的尾巴，"
           "側身立於山石之上。中國傳統冊頁畫法，工筆兼淡彩，赭石與墨，陳年紙本，留白充足。"),
}

SEEDS = {"v1": [101, 202, 303], "v2": [101, 202, 303], "v3": [101, 202, 303]}

# R2 设计：R1 的结论是「英文特征前置（v2）出得来虎纹与白首，中文直述（v3）丢了虎纹且色偏」。
#   R2 只动两个变量：① 赤色是否只落在尾巴上（v5 加了一句限定）；② 中文换一种写法再试一次（v6）。
#   v4 是 v2 的逐字复用（换 seed）——用来量 seed 方差，不是新写法。
VARIANTS_R2 = {
    "v4": VARIANTS["v2"],
    "v5": ("A horse of Chinese mythology with a pure white head, a body covered in bold black "
           "tiger stripes; only its long tail is cinnabar red, its mane and legs stay white. "
           "It is called the lu-shu and stands in profile on a rocky ledge. " + STYLE),
    "v6": ("《山海經》異獸鹿蜀：馬的身子、白色的頭，身上有清晰的黑色虎紋，"
           "只有尾巴是赤紅色；側身立於山石之上。中國傳統冊頁淡彩：工筆、赭石與墨、"
           "陳年紙本、大量留白。"),
}

# R3 设计：R1/R2 各 9 张里，**几乎每张的四角都被模型盖了乱码印/写了伪字**
#   （R1 8/9、R2 英文组 6/6，连已交付的九尾狐 R7 定稿也有淡淡的红印）。
#   这一轮只试「用 prompt 抑制印与字」这一条路（另一条路是工具擦除，见 R3 之后的处理）。
VARIANTS_R3 = {
    "w1": ("A horse of Chinese mythology with a pure white head, a body covered in bold black "
           "tiger stripes; only its long tail is cinnabar red, its mane and legs stay white. "
           "It is called the lu-shu and stands in profile on a rocky ledge. " + STYLE +
           " There is no red seal, no stamp and no writing anywhere in the painting."),
    "w2": ("A horse of Chinese mythology with a pure white head, a body covered in black tiger "
           "stripes and a long cinnabar-red tail; it is called the lu-shu and stands in profile "
           "on a rocky ledge. " + STYLE +
           " The paper stays blank: do not paint seals, stamps, calligraphy or any characters."),
    "w3": ("The lu-shu of Chinese mythology, a white-headed horse with bold black tiger stripes "
           "on its body and a red tail, standing in profile on a rocky ledge. " + STYLE +
           " without seal or inscription"),
}

ROUNDS = {
    1: {
        "note": "R1 变体扫描：写法（点名 / 特征前置 / 中文直述）× seed，先看三特征落地率与是否出现模型写的汉字",
        "shots": [
            {"id": f"{v}-{s}", "variant": v, "prompt": p, "seed": s,
             "width": CANVAS["width"], "height": CANVAS["height"], "steps": STEPS}
            for v, p in VARIANTS.items() for s in SEEDS[v]
        ],
    },
    2: {
        "note": "R2 收敛轮：以 R1 的 v2 写法为底，只试「赤色限定在尾部」与「中文改写」两个变量，3 seed 各跑一遍",
        "shots": [
            {"id": f"{v}-{s}", "variant": v, "prompt": p, "seed": s,
             "width": CANVAS["width"], "height": CANVAS["height"], "steps": STEPS}
            for v, p in VARIANTS_R2.items() for s in (404, 505, 606)
        ],
    },
    3: {
        "note": "R3 印面抑制轮：同一形态描述 + 三种「不要印/不要字」的写法，看 prompt 能不能压住乱码印",
        "shots": [
            {"id": f"{v}-{s}", "variant": v, "prompt": p, "seed": s,
             "width": CANVAS["width"], "height": CANVAS["height"], "steps": STEPS}
            for v, p in VARIANTS_R3.items() for s in (707, 808, 909)
        ],
    },
    # R4 跨引擎对照（**付费**，跑法：--engine seedream --api-key-file <key>）：
    # 同一段 prompt 交给 Seedream 5.0 Pro（远端模型），与 Z-Image-Turbo 比
    #   * 三特征（白首 / 虎纹 / 赤尾）落地率
    #   * 会不会同样在纸角盖乱码印（Z-Image 在本骨法下 23/24 命中）
    4: {
        "note": "R4 跨引擎对照：同一 prompt 走 Seedream 5.0 Pro，量「特征落地率」与「印面污染」（付费）",
        "shots": [
            {"id": f"{v}-{s}", "variant": v, "prompt": p, "seed": s,
             "width": CANVAS["width"], "height": CANVAS["height"], "steps": STEPS}
            for v, p in {"x1": VARIANTS["v1"], "x2": VARIANTS_R2["v5"]}.items()
            for s in (101, 202, 303)
        ],
    },
}
