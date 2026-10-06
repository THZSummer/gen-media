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

# R5 抑印措辞实验：**不动形态句（v5）**，只动"介质与版面"那一句，一次只改一个变量。
#   为什么换思路：R3 已证伪「no seal / no stamp / no writing」这套否定式（9 张全无效）；
#   印是"装裱过的旧画"这个先验带来的——那就改写先验本身，而不是叫模型别画。
#   s1 同轮底座对照（逐字复用现骨法句，量 seed 方差与印面基线）
#   s2 变量＝媒介名词：album leaf（册页）→ a single unmounted sheet of xuan paper（未装裱单片）
#   s3 变量＝版面：画面占满整张纸、不留空边（印章没有栖身的空白）
#   s4 变量＝纸龄：aged paper（陈年纸本）→ plain white paper（素白纸，去掉"旧画"先验）
#   四个骨法句与九尾狐 R9 逐字相同 —— 换兽不换实验设计，结论才能互相印证。
SUBJECT_V5 = ("A horse of Chinese mythology with a pure white head, a body covered in bold black "
              "tiger stripes; only its long tail is cinnabar red, its mane and legs stay white. "
              "It is called the lu-shu and stands in profile on a rocky ledge.")
STYLE_MEDIUM = ("Painted on a single unmounted sheet of xuan paper, fine ink brushwork, "
                "delicate fur strokes, ink and pale colour on aged paper.")
STYLE_FILLED = ("Painted in the manner of a traditional Chinese album leaf, fine ink brushwork, "
                "delicate fur strokes, ink and pale colour on aged paper. The subject and the "
                "ground fill the sheet out to all four edges, leaving no empty margin.")
STYLE_NEWPAPER = ("Painted in the manner of a traditional Chinese album leaf, fine ink brushwork, "
                  "delicate fur strokes, ink and pale colour on plain white paper.")

SUPPRESS_VARIANTS = {
    "s1": SUBJECT_V5 + " " + STYLE,
    "s2": SUBJECT_V5 + " " + STYLE_MEDIUM,
    "s3": SUBJECT_V5 + " " + STYLE_FILLED,
    "s4": SUBJECT_V5 + " " + STYLE_NEWPAPER,
}
SUPPRESS_SEEDS = (1811, 1922, 2033)

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
    # R5 抑印措辞实验（免费，本地 Z-Image）：不改形态、只改"介质与版面"
    5: {
        "note": ("R5 抑印措辞实验：同形态句（v5）× 四种骨法句（s1 底座对照 / s2 换媒介名词 / "
                 "s3 画面占满 / s4 换素白纸），每式 3 seed，看印面命中率能不能被措辞改写。"
                 "**结果：12/12 仍有印（措辞抑印证伪）；浓虎纹候选加权 4.38 < 定稿 4.60，不换代** "
                 "—— 见 rounds/r05-review.md"),
        "shots": [
            {"id": f"{v}-{s}", "variant": v, "prompt": p, "seed": s,
             "width": CANVAS["width"], "height": CANVAS["height"], "steps": STEPS}
            for v, p in SUPPRESS_VARIANTS.items() for s in SUPPRESS_SEEDS
        ],
    },
}
