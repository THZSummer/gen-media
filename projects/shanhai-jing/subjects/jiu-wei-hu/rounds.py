"""九尾狐（山海經 · 南山經 · 青丘之山）—— 考据记录与轮次 prompt 定义。

底本：郭璞注本《山海經》卷一 · 南山經（識典古籍 SK2098，与鹿蜀同期核对）
原文（逐字核对，异体字保留底本写法）：

    又東三百里，曰青丘之山。其陽多玉，其陰多青䨼。有獸焉，其狀如狐而九尾，
    其音如嬰兒，能食人。食者不蠱。

可验特征（验收硬指标）：
  1. 九尾 —— 「其狀如狐而九尾」：读作九尾即可，**目视点数，非机械确证**
     （R5 已证：「可机械确证」当硬门槛只会逼出机械的图）

骨法（期内恒定，与鹿蜀定稿同一句）：赭石设色工笔 / 册页、淡彩陈年纸本。

轮次存档说明
------------
R1–R6、R8 是临时敲命令跑的，逐字 prompt 未留档（见 README v0.4）。
本文件先把 **R7 定稿那一条**从 period-01/manifest.json 追认回来（可复跑），
再定义 R9 的抑印措辞实验——把 prompt 定义放回仓库，跑之前能 `--dry` 看逐字 prompt。
"""

SLUG = "jiu-wei-hu"
NAME_ZH = "九尾狐"
NAME_EN = "nine-tailed fox"
VOLUME = "山海經 · 南山經"
VOLUME_EN = "Shan Hai Jing · Nan Shan Jing"
PLACE = "青丘之山"
PASSAGE = ("又東三百里，曰青丘之山。其陽多玉，其陰多青䨼。"
           "有獸焉，其狀如狐而九尾，其音如嬰兒，能食人。食者不蠱。")
COVER_LINE = "其狀如狐而九尾"

CANVAS = {"width": 1024, "height": 1360}   # 与鹿蜀同画布，系列一致
STEPS = 20
ENGINE = "z-image-turbo"

# 点名式形态句（R7 定案：点名神话生物 8/8 出九尾；描述式仅 1/6）
SUBJECT_R7 = ("The nine-tailed fox of Chinese mythology, standing on a rocky outcrop and looking "
              "back over its shoulder. Its nine long tails spread out behind it, thick and full of fur.")

# 骨法句（现用，R7 定案）—— 与鹿蜀 rounds.py 的 STYLE 逐字相同
STYLE = ("Painted in the manner of a traditional Chinese album leaf, fine ink brushwork, "
         "delicate fur strokes, ink and pale colour on aged paper.")

# R9 抑印措辞实验：**不动形态句**，只动"介质与版面"那一句，一次只改一个变量。
#   为什么换思路：R3 已证伪「no seal / no stamp / no writing」这套否定式（9 张全无效）；
#   印是"装裱过的旧画"这个先验带来的——那就改写先验本身，而不是叫模型别画。
#   s1 同轮底座对照（逐字复用现骨法句，用来量 seed 方差与印面基线）
#   s2 变量＝媒介名词：album leaf（册页）→ a single unmounted sheet of xuan paper（未装裱单片）
#   s3 变量＝版面：画面占满整张纸、不留空边（印章没有栖身的空白）
#   s4 变量＝纸龄：aged paper（陈年纸本）→ plain white paper（素白纸，去掉"旧画"先验）
STYLE_MEDIUM = ("Painted on a single unmounted sheet of xuan paper, fine ink brushwork, "
                "delicate fur strokes, ink and pale colour on aged paper.")
STYLE_FILLED = ("Painted in the manner of a traditional Chinese album leaf, fine ink brushwork, "
                "delicate fur strokes, ink and pale colour on aged paper. The subject and the "
                "ground fill the sheet out to all four edges, leaving no empty margin.")
STYLE_NEWPAPER = ("Painted in the manner of a traditional Chinese album leaf, fine ink brushwork, "
                  "delicate fur strokes, ink and pale colour on plain white paper.")

SUPPRESS_VARIANTS = {
    "s1": SUBJECT_R7 + " " + STYLE,
    "s2": SUBJECT_R7 + " " + STYLE_MEDIUM,
    "s3": SUBJECT_R7 + " " + STYLE_FILLED,
    "s4": SUBJECT_R7 + " " + STYLE_NEWPAPER,
}
SUPPRESS_SEEDS = (1811, 1922, 2033)

ROUNDS = {
    # R7 是定稿轮（临时命令跑的），这里按 manifest 的原文追认，便于复跑与对照
    7: {
        "note": "R7 定稿轮（追认存档）：点名式 prompt + 赭石设色骨法，seed 202 那张即 period-01 的画心",
        "shots": [
            {"id": "m202", "variant": "r7", "prompt": SUBJECT_R7 + " " + STYLE, "seed": 202,
             "width": CANVAS["width"], "height": CANVAS["height"], "steps": STEPS},
        ],
    },
    # R9：不改形态、只改"介质与版面"的抑印实验（免费，本地 Z-Image）
    9: {
        "note": ("R9 抑印措辞实验：同形态句 × 四种骨法句（s1 底座对照 / s2 换媒介名词 / "
                 "s3 画面占满 / s4 换素白纸），每式 3 seed，看印面命中率能不能被措辞改写。"
                 "**结果：12/12 仍有印（措辞抑印证伪）；最优候选加权 4.63 < 定稿 4.80，不换代** "
                 "—— 见 rounds/r09-review.md"),
        "shots": [
            {"id": f"{v}-{s}", "variant": v, "prompt": p, "seed": s,
             "width": CANVAS["width"], "height": CANVAS["height"], "steps": STEPS}
            for v, p in SUPPRESS_VARIANTS.items() for s in SUPPRESS_SEEDS
        ],
    },
}
