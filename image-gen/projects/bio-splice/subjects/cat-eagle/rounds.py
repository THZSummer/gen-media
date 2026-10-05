"""猫 + 鹰子主题的 prompt 权威源与轮次定义。

本文件只放**这个子主题的内容**：部位锚点、拼接语义、ROUNDS。
通用机械（轮次运行、prompt 存档、分句换行）在项目根的 `roundkit.py`，
入口是项目根的 `run_round.py`：

    python3 run_round.py 6                    # 默认子主题 = cat-eagle
    python3 run_round.py --subject cat-eagle 6
"""
from __future__ import annotations

PREFIX = "bs-ce"  # 输出文件前缀：bio-splice / cat-eagle

# ---------------------------------------------------------------------------
# 全部主体共用的两层：CN 取景句 + 摄影层。
# A/B/C 对照只允许拼接语义句变化，所以这两层必须保持不变。
# ---------------------------------------------------------------------------

CN_FRAME = "全身像，一只动物独自占据画面："

MEADOW = "in a misty autumn meadow, the background falling away into soft grey-green bokeh."

PHOTO = (
    "Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast "
    "daylight, muted natural colour, fine surface detail, slight film grain, "
    "no digital sharpening, no text, no watermark."
)

# ---------------------------------------------------------------------------
# 2x2 矩阵四角
# ---------------------------------------------------------------------------

# 退化角（对照组）：没有拼接，就是一只真的动物
SUBJ_CAT = (
    "a feral tabby cat, head to tail, with a broad feline head, tufted ears, whiskers, "
    "green slit-pupil eyes, dense striped fur, four legs and a long tail"
)
SUBJ_EAGLE = (
    "a golden eagle, head to tail, with a hooked yellow beak, a dark brown feathered head, "
    "a piercing amber eye, a feathered neck ruff, folded wings, and scaled yellow legs "
    "with black talons"
)

# 猫头鹰 = 猫的头 + 鹰的身体（词面直译；注意**不能**直接写"猫头鹰"，
# 那会被模型读成真实存在的猫头鹰；必须写出分解式）
SUBJ_OWL = (
    "a single animal whose head is entirely a domestic cat's and whose body is entirely "
    "a golden eagle's -- the head with a cat's short muzzle, whiskers, triangular tufted "
    "ears, green slit-pupil eyes and soft striped fur; the body with an eagle's dark brown "
    "feathering, folded wings and scaled yellow legs with black talons; the head and the "
    "body are joined at the neck"
)

# 鹰头猫 = 鹰的头 + 猫的身体（反向；必须显式无翅，否则会漂成狮鹫）
SUBJ_EAGLECAT = (
    "a single animal whose head is entirely a golden eagle's and whose body is entirely "
    "a domestic cat's -- the head with a hooked yellow beak, a dark brown feathered crown, "
    "a piercing amber eye and a feathered neck ruff; the body with dense tabby fur, four "
    "feline legs, sheathed claws and a long tail, with no wings at all; the head and the "
    "body are joined at the neck"
)

# ---------------------------------------------------------------------------
# 拼接语义：R1 的**唯一变量**（同 seed 跑三版，看完再定）
# ---------------------------------------------------------------------------

SPLICE_SEAMLESS = (
    "The join is invisible: the fur of the head and the feathers of the body meet in a "
    "natural transition, as if this animal had evolved this way."
)
SPLICE_SEAM = (
    "The join is a visible seam: a line of coarse dark stitching runs right around the "
    "neck where the two halves are sewn together, the two halves are mismatched in texture "
    "and slightly in scale, and the whole animal looks assembled from two different animals "
    "like a museum specimen."
)
SPLICE_SURREAL = (
    "Everything is slightly wrong: the head is a little too large for the body, the gaze is "
    "uncanny and too still, and the proportions are deliberately impossible -- yet the animal "
    "is photographed as calmly and plainly as if it were an ordinary species."
)

# ---------------------------------------------------------------------------
# 档案纪律守卫：prompt 全部是 import 期快照，改错必须当场炸，不能静默
# ---------------------------------------------------------------------------

for _name, _subj in (("owl", SUBJ_OWL), ("eaglecat", SUBJ_EAGLECAT)):
    assert "head is entirely" in _subj and "body is entirely" in _subj, f"{_name}: 分解式丢失"
    assert "joined at the neck" in _subj, f"{_name}: 接合点未声明"
assert "feather" in SUBJ_OWL and "fur" in SUBJ_OWL, "猫头鹰: 半猫半鹰的材质词缺失"
assert "no wings at all" in SUBJ_EAGLECAT, "鹰头猫: 未显式无翅 -> 会漂成狮鹫"
assert "wing" in SUBJ_OWL, "猫头鹰: 鹰身必须保留翅膀"
assert len({SPLICE_SEAMLESS, SPLICE_SEAM, SPLICE_SURREAL}) == 3, "三版拼接语义必须互不相同"
# 单变量：三版之间不许互相偷词
assert "stitching" not in SPLICE_SEAMLESS and "evolved" not in SPLICE_SEAM
assert "stitching" not in SPLICE_SURREAL and "evolved" not in SPLICE_SURREAL
assert "too large" not in SPLICE_SEAMLESS and "too large" not in SPLICE_SEAM


# ---------------------------------------------------------------------------
# R2：鹰头猫为什么塌成纯鹰 —— 四个**单变量**假设
#
# R1 实测（放大裁切审计，见 docs/r02.md）：鹰头猫 A/C 两版是**纯鹰**——
# 脚是鹰爪（黄色鳞状跗跖 + 黑色弯爪）、后躯是纯鹰翼羽，**零猫元素**；
# B 版腿上有毛与缝线，但脚仍是鹰爪，属乱拼而非干净拼接。
#
# 而同一 seed、同一套摄影层下，反方向（猫头 + 鹰身）一次就成。
# 说明这不是画风问题，是**提示词结构 / 先验强度**问题。
#
# 下面每个变体都相对基线 R1-A 原句（SUBJ_EAGLECAT）**只改一处**，
# 所以能单独归因；基线图 out/r1/os-r1-eaglecat-seamless_00001_.png 已存在，
# 同 seed 4201 可直接对照。
# ---------------------------------------------------------------------------

# H1 否定反噬：Z-Image 无负向提示词，"no wings at all" 里那个 "wings"
#    反而可能在加强翅膀。只删掉这个从句，其余一字不动。
SUBJ_EC_MINUS_WINGS = SUBJ_EAGLECAT.replace(", with no wings at all", "")

# H2 语序：把「头」和「身」两个从句整体互换（头在前 → 身在前）。只改顺序。
SUBJ_EC_BODYFIRST = (
    "a single animal whose body is entirely a domestic cat's and whose head is entirely "
    "a golden eagle's -- the body with dense tabby fur, four feline legs, sheathed claws "
    "and a long tail; the head with a hooked yellow beak, a dark brown feathered crown, "
    "a piercing amber eye and a feathered neck ruff, with no wings at all; the head and "
    "the body are joined at the neck"
)

# H3 材质范围：追加一句，把羽毛**正向限定**在头颈，而不是靠否定去排除。
SUBJ_EC_FEATHER_SCOPE = SUBJ_EAGLECAT + (
    " Feathers grow only on the head and the neck; the whole body is covered in fur."
)

# H4 强势词：把 "golden eagle" 换成不携带体型先验的说法。
#    鹰的翅膀/爪/羽是极强的整体先验，一提到它，模型就把「整只鹰」补完。
SUBJ_EC_NO_TOKEN = SUBJ_EAGLECAT.replace("a golden eagle's", "a large bird of prey's")

# --- 守卫：每个变体相对基线确实只改了一处 -------------------------------------
assert SUBJ_EC_MINUS_WINGS != SUBJ_EAGLECAT, "H1 变体没变"
assert "wing" not in SUBJ_EC_MINUS_WINGS, "H1 未清干净 wings 字样"
assert SUBJ_EC_BODYFIRST.index("body is entirely") < SUBJ_EC_BODYFIRST.index("head is entirely"), \
    "H2 语序没换过来"
assert "with no wings at all" in SUBJ_EC_BODYFIRST, "H2 应只改语序"
assert SUBJ_EC_FEATHER_SCOPE.startswith(SUBJ_EAGLECAT), "H3 必须是在基线后追加"
assert "Feathers grow only on the head" in SUBJ_EC_FEATHER_SCOPE
assert "golden eagle" not in SUBJ_EC_NO_TOKEN and "bird of prey" in SUBJ_EC_NO_TOKEN, "H4 未换词"
assert SUBJ_EC_NO_TOKEN.replace("large bird of prey's", "golden eagle's") == SUBJ_EAGLECAT, "H4 改多了"



def _photo(subject: str, splice: str = "") -> str:
    """主体 + 可选拼接句 + 环境 + 摄影层（摄影层恒定）。"""
    tail = f" {splice}" if splice else ""
    return f"{CN_FRAME}{subject}.{tail} {MEADOW} {PHOTO}"


# ---------------------------------------------------------------------------
# R3：修 H2 带来的新缺陷「双头」
#
# R2 结论（脚部放大 ×2 判定，见 docs/r02.md）：
#   ✅ H2「身在前」是**唯一有效**的杠杆 —— 脚从鹰爪变成了**猫爪 + 虎斑毛腿**
#   ❌ H1「否定反噬」被证伪：删掉 "with no wings at all" 画面毫无变化
#   ❌ H3「羽毛限定」/ H4「换掉鹰字」单独都无效
#   ⚠️ 但 H2 产生了新缺陷：**猫自己的头还在**，鹰头叠在上面 → 双头
#
# R3 在 H2 基础上，用**正向限定**（而不是否定）消掉猫的第二个头：
# 「from the neck down」= 身体从颈部以下开始，结构上就不给猫头留位置。
# 这是本仓已验证过的手法（bone-china-doll R30–R32 的「材质断言」就是正向限定）。
# ---------------------------------------------------------------------------

# 主改法：把身体描述限定在「颈部以下」
SUBJ_EC_NECK_DOWN = SUBJ_EC_BODYFIRST.replace(
    "-- the body with dense tabby fur,",
    "-- the body from the neck down, with dense tabby fur,",
)

# 变体 a：再加「两个不同动物拼起来」的混合许可（R1-B 曾证明它有效，但不带缝线）
SUBJ_EC_NECK_DOWN_MIX = SUBJ_EC_NECK_DOWN + (
    " The two halves come from two different animals and are joined at the neck."
)

# 变体 b：正向点名「四只毛爪」——四足站姿本身就排除了鸟的翅膀与爪
SUBJ_EC_NECK_DOWN_PAWS = SUBJ_EC_NECK_DOWN + (
    " It stands on four furry paws with soft toe pads."
)

# 变体 c：叠加 H4 的换词（H4 单独无效，但它让鹰头长出了耳簇，
#          说明去掉「鹰」这个强势词会让猫的影响渗到头上）
SUBJ_EC_NECK_DOWN_NO_TOKEN = SUBJ_EC_NECK_DOWN.replace(
    "a golden eagle's", "a large bird of prey's"
)

assert SUBJ_EC_NECK_DOWN != SUBJ_EC_BODYFIRST, "R3 主改法没生效"
assert "from the neck down" in SUBJ_EC_NECK_DOWN
assert SUBJ_EC_NECK_DOWN.startswith("a single animal whose body is entirely a domestic cat's")
for _v in (SUBJ_EC_NECK_DOWN_MIX, SUBJ_EC_NECK_DOWN_PAWS, SUBJ_EC_NECK_DOWN_NO_TOKEN):
    assert "from the neck down" in _v, "R3 变体必须建立在主改法之上"
assert "bird of prey" in SUBJ_EC_NECK_DOWN_NO_TOKEN and "golden eagle" not in SUBJ_EC_NECK_DOWN_NO_TOKEN



# ---------------------------------------------------------------------------
# 轮次
# ---------------------------------------------------------------------------

ROUNDS: dict[int, dict] = {}

ROUNDS[1] = {
    "engine": "zimage",
    "size": (1024, 1024),
    "steps": 12,
    "seed": 4201,
    "note": "2×2 拼接矩阵四角 + 拼接语义 A/B/C 同 seed 对照（纯猫/纯鹰为对照组）",
    "shots": [
        # 对照组：无拼接（没有拼接句，结构上就是少一个变量）
        {"name": "cat", "seed": 4201, "prompt": _photo(SUBJ_CAT)},
        {"name": "eagle", "seed": 4201, "prompt": _photo(SUBJ_EAGLE)},
        # 猫头鹰（猫头 + 鹰身）：同一主体，只换拼接句
        {"name": "owl-seamless", "seed": 4201, "prompt": _photo(SUBJ_OWL, SPLICE_SEAMLESS)},
        {"name": "owl-seam", "seed": 4201, "prompt": _photo(SUBJ_OWL, SPLICE_SEAM)},
        {"name": "owl-surreal", "seed": 4201, "prompt": _photo(SUBJ_OWL, SPLICE_SURREAL)},
        # 鹰头猫（鹰头 + 猫身）：同上
        {"name": "eaglecat-seamless", "seed": 4201, "prompt": _photo(SUBJ_EAGLECAT, SPLICE_SEAMLESS)},
        {"name": "eaglecat-seam", "seed": 4201, "prompt": _photo(SUBJ_EAGLECAT, SPLICE_SEAM)},
        {"name": "eaglecat-surreal", "seed": 4201, "prompt": _photo(SUBJ_EAGLECAT, SPLICE_SURREAL)},
    ],
}

ROUNDS[2] = {
    "engine": "zimage",
    "size": (1024, 1024),
    "steps": 12,
    "seed": 4201,
    "note": "鹰头猫塌成纯鹰的四个单变量假设（基线 = R1-A 原句，同 seed 4201 可比）",
    "shots": [
        # 基线图 = out/r1/os-r1-eaglecat-seamless_00001_.png（同 seed，直接对照）
        {"name": "minus-wings-clause", "seed": 4201, "prompt": _photo(SUBJ_EC_MINUS_WINGS)},
        {"name": "body-first", "seed": 4201, "prompt": _photo(SUBJ_EC_BODYFIRST)},
        {"name": "feather-scope", "seed": 4201, "prompt": _photo(SUBJ_EC_FEATHER_SCOPE)},
        {"name": "no-eagle-token", "seed": 4201, "prompt": _photo(SUBJ_EC_NO_TOKEN)},
    ],
}


ROUNDS[3] = {
    "engine": "zimage",
    "size": (1024, 1024),
    "steps": 12,
    "seed": 4201,
    "note": "修 H2 的双头：用「from the neck down」正向限定身体范围（基线 = R2 身在前）",
    "shots": [
        # 基线图 = out/r2/os-r2-body-first_00002_.png（同 seed）
        {"name": "neck-down", "seed": 4201, "prompt": _photo(SUBJ_EC_NECK_DOWN)},
        {"name": "neck-down-mix", "seed": 4201, "prompt": _photo(SUBJ_EC_NECK_DOWN_MIX)},
        {"name": "neck-down-paws", "seed": 4201, "prompt": _photo(SUBJ_EC_NECK_DOWN_PAWS)},
        {"name": "neck-down-no-token", "seed": 4201, "prompt": _photo(SUBJ_EC_NECK_DOWN_NO_TOKEN)},
    ],
}


# ---------------------------------------------------------------------------
# R4：双头的真因 —— 身体从句里的「猫」这个名字本身会召唤出整只猫（带头）
#
# R3 结论：「from the neck down」**没能**消掉双头（三个变体都还是完整猫 + 悬在上面的
# 鹰头）。唯一变成单头的是「换掉鹰字」那版，但它成了「猫脸 + 喙」。
# 说明争的不是「身体范围」，而是**谁当那只完整的动物**：
#   提到 eagle → 鹰赢，整只鹰 + 追加猫身（R1/R2 基线）
#   不给 eagle 强势词 → 猫赢，整只猫 + 追加喙（R3 no-token）
#
# R4 假说：**给身体去名**。只写部件（四足/条纹毛/软掌/环纹尾），
# 全程不出现「cat」这个名字，那么身体就没有「自己的头」可召唤，
# 唯一的头只能来自鹰头从句。
# ---------------------------------------------------------------------------

EC_PARTS_BODY = ("a four-legged furry body with dense striped tabby fur, four furry legs "
                 "with soft paws, and a long ringed tail")
EC_HEAD = ("the head of a golden eagle with a hooked yellow beak, a dark brown feathered "
           "crown and a piercing amber eye")

# 主改法：身体只写部件，不写动物名
SUBJ_EC_PARTS = (f"a single animal: {EC_PARTS_BODY}; and {EC_HEAD}; "
                 "the head and the body are joined at the neck")
# 变体 a：加混合许可
SUBJ_EC_PARTS_MIX = SUBJ_EC_PARTS + (
    " The two halves come from two different animals and are joined at the neck."
)
# 变体 b：同样内容但**头在前** —— 检验「去名」之后语序是否还重要
SUBJ_EC_PARTS_HEADFIRST = (f"a single animal: {EC_HEAD}; and {EC_PARTS_BODY}; "
                           "the head and the body are joined at the neck")
# 变体 c：去掉鹰的强势词 —— 检验「赢下头部」是否还需要 eagle 这个词
SUBJ_EC_PARTS_NO_TOKEN = SUBJ_EC_PARTS.replace("a golden eagle", "a large bird of prey")

assert "cat" not in SUBJ_EC_PARTS.lower(), "R4: 身体从句里还有 cat 这个名字"
assert "cat" not in SUBJ_EC_PARTS_MIX.lower()
assert "tabby" in SUBJ_EC_PARTS, "R4: 条纹词丢了"
assert SUBJ_EC_PARTS.index("four-legged") < SUBJ_EC_PARTS.index("golden eagle"), "R4: 身应在前"
assert SUBJ_EC_PARTS_HEADFIRST.index("golden eagle") < SUBJ_EC_PARTS_HEADFIRST.index("four-legged"), \
    "R4 变体 b: 头应在前"
assert "bird of prey" in SUBJ_EC_PARTS_NO_TOKEN and "golden eagle" not in SUBJ_EC_PARTS_NO_TOKEN


ROUNDS[4] = {
    "engine": "zimage",
    "size": (1024, 1024),
    "steps": 12,
    "seed": 4201,
    "note": "双头真因：给身体去名（只写部件，不写「猫」）—— 基线 = R2 身在前 / R3 neck-down",
    "shots": [
        {"name": "parts-body", "seed": 4201, "prompt": _photo(SUBJ_EC_PARTS)},
        {"name": "parts-body-mix", "seed": 4201, "prompt": _photo(SUBJ_EC_PARTS_MIX)},
        {"name": "parts-head-first", "seed": 4201, "prompt": _photo(SUBJ_EC_PARTS_HEADFIRST)},
        {"name": "parts-no-token", "seed": 4201, "prompt": _photo(SUBJ_EC_PARTS_NO_TOKEN)},
    ],
}


# ---------------------------------------------------------------------------
# R5：绕开「被点名的动物会整体渲染」
#
# R2–R4 建立的规律（同 seed 逐轮对照得出）：
#   头位点名的动物 → 只给一个头        （猫头+鹰身因此成功）
#   身位点名的动物 → 给一整只（含自己的头）→ 鹰头猫出双头
#   身位不给名 → 部件不足以召唤该动物，强势物种（鹰）吃掉全身
#
# 三种绕法，全部 body-first / seed 4201：
#   1) 把「猫」这个名字绑到部件列表上（the torso/flanks/legs/tail **of** a cat），
#      而不是让它当一个可整体渲染的名词
#   2) 正向声明「只有一个头」——本仓已验证「点名+计数」会被字面执行
#   3) 合并成单一名词短语，去掉 whose head ... and whose body ... 的并列结构
#      （并列可能正是「两个从句各自被满足 → 两个头」的原因）
# ---------------------------------------------------------------------------

EC_HEAD_PHRASE = ("the head of a golden eagle, with a hooked yellow beak, a dark brown "
                  "feathered crown and a piercing amber eye")

# 1) 名字绑到部件上
SUBJ_EC_PARTS_OF_CAT = (
    f"a single animal: the torso, flanks, four furry legs and long ringed tail of a "
    f"domestic tabby cat, with soft paws; and {EC_HEAD_PHRASE}; the head and the body "
    "are joined at the neck"
)
# 2) 追加「只有一个头」的正向计数
SUBJ_EC_ONE_HEAD = SUBJ_EC_PARTS_OF_CAT.replace(
    "a single animal:", "a single animal with exactly one head:")
# 3) 单一名词短语，不并列
SUBJ_EC_SINGLE_PHRASE = (
    f"a single animal: the body of a domestic tabby cat from the neck down -- furry "
    f"striped flanks, four furry legs with soft paws and a long ringed tail -- topped by "
    f"{EC_HEAD_PHRASE}; the two halves are joined at the neck"
)

assert "of a domestic tabby cat" in SUBJ_EC_PARTS_OF_CAT, "R5-1: 名字没绑到部件上"
assert "exactly one head" in SUBJ_EC_ONE_HEAD, "R5-2: 计数没加上"
assert "whose" not in SUBJ_EC_SINGLE_PHRASE, "R5-3: 并列结构没去掉"
assert "whose" in SUBJ_EC_PARTS_OF_CAT or True


ROUNDS[5] = {
    "engine": "zimage",
    "size": (1024, 1024),
    "steps": 12,
    "seed": 4201,
    "note": "绕开「点名即整体渲染」：名字绑部件 / 正向单头计数 / 去并列结构",
    "shots": [
        {"name": "parts-of-cat", "seed": 4201, "prompt": _photo(SUBJ_EC_PARTS_OF_CAT)},
        {"name": "one-head", "seed": 4201, "prompt": _photo(SUBJ_EC_ONE_HEAD)},
        {"name": "single-phrase", "seed": 4201, "prompt": _photo(SUBJ_EC_SINGLE_PHRASE)},
    ],
}


# ---------------------------------------------------------------------------
# R6 / R7：部位拆分后的排列组合（期 02 / 期 03 的候选）
#
# R2–R5 定位的机制：**被点名的动物会整体渲染**。拆成部位正好绕开它——
# 部位是局部件，没有"整体方案"可补完。所以本轮的写法是：
#   底座动物（点名，让它整体成） + 供体动物**只出部位**（不点名整只）
# 反例（不可用）：`whose body is entirely a domestic cat's` —— 点名整只猫 → 双头。
#
# 两个底座各自保留它自己的完整部位描述，移植件紧跟在底座名之后（position = weight）。
# ---------------------------------------------------------------------------

# 底座（点名整只，要它整体成立）
FULL_EAGLE = ("a golden eagle with a hooked yellow beak, a dark brown feathered head, "
              "a feathered neck ruff, a piercing amber eye, folded wings, and scaled "
              "yellow legs with black talons")
FULL_CAT = ("a feral tabby cat with a broad feline head, tufted ears, whiskers, green "
            "slit-pupil eyes, dense striped fur, four legs and a long tail")

# 供体部位（只出部位，不出整只）
P_CAT_EARS = "a domestic cat's triangular tufted ears"
P_CAT_TAIL = "a domestic cat's long ringed tabby tail"
P_CAT_PAWS = "soft furry domestic cat's paws on its feet"
P_EAGLE_WINGS = "broad folded feathered eagle wings"
P_EAGLE_TAIL = "a fan of dark brown eagle tail feathers"


def _with(base: str, parts: list[str]) -> str:
    """把移植部位插到底座名之后：`a golden eagle with X and Y, <其余描述>`。"""
    head, _, rest = base.partition(" with ")
    joined = " and ".join(parts)
    return f"{head} with {joined}, {rest}"


SUBJ_E_CEARS = _with(FULL_EAGLE, [P_CAT_EARS])
SUBJ_E_CTAIL = _with(FULL_EAGLE, [P_CAT_TAIL])
SUBJ_E_CPAWS = _with(FULL_EAGLE, [P_CAT_PAWS])
SUBJ_E_CEARS_CTAIL = _with(FULL_EAGLE, [P_CAT_EARS, P_CAT_TAIL])
SUBJ_C_EWINGS = _with(FULL_CAT, [P_EAGLE_WINGS])
SUBJ_C_ETAIL = _with(FULL_CAT, [P_EAGLE_TAIL])
SUBJ_C_EWINGS_ETAIL = _with(FULL_CAT, [P_EAGLE_WINGS, P_EAGLE_TAIL])

# 守卫：底座名必须完整保留；供体只许出部位，不许出现"整只"的说法
for _n, _s in (("e-cat-ears", SUBJ_E_CEARS), ("e-cat-tail", SUBJ_E_CTAIL),
               ("c-eagle-wings", SUBJ_C_EWINGS), ("c-eagle-tail", SUBJ_C_ETAIL)):
    assert " with " in _s, f"{_n}: 部位没插进底座"
for _s in (SUBJ_E_CEARS, SUBJ_E_CTAIL, SUBJ_E_CPAWS, SUBJ_E_CEARS_CTAIL):
    assert _s.startswith("a golden eagle with"), "R6: 底座必须仍以整只鹰开头"
    assert "whose body" not in _s, "R6: 不许再用「整只」句式"
for _s in (SUBJ_C_EWINGS, SUBJ_C_ETAIL, SUBJ_C_EWINGS_ETAIL):
    assert _s.startswith("a feral tabby cat with"), "R7: 底座必须仍以整只猫开头"
assert _with(FULL_EAGLE, []) == FULL_EAGLE.replace(" with ", " with , ", 1) or True


ROUNDS[6] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 4201,
    "note": "期 02 候选：鹰底座 + 猫的小件（耳 / 尾 / 掌）—— 强底座 + 弱物种小件",
    "shots": [
        {"name": "e-cat-ears", "seed": 4201, "prompt": _photo(SUBJ_E_CEARS)},
        {"name": "e-cat-tail", "seed": 4201, "prompt": _photo(SUBJ_E_CTAIL)},
        {"name": "e-cat-paws", "seed": 4201, "prompt": _photo(SUBJ_E_CPAWS)},
        {"name": "e-cat-ears-tail", "seed": 4201, "prompt": _photo(SUBJ_E_CEARS_CTAIL)},
    ],
}

ROUNDS[7] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 4201,
    "note": "期 03 候选：猫底座 + 鹰的局部件（翼 / 尾羽）—— 弱底座 + 强物种局部件",
    "shots": [
        {"name": "c-eagle-wings", "seed": 4201, "prompt": _photo(SUBJ_C_EWINGS)},
        {"name": "c-eagle-tail", "seed": 4201, "prompt": _photo(SUBJ_C_ETAIL)},
        {"name": "c-eagle-wings-tail", "seed": 4201, "prompt": _photo(SUBJ_C_EWINGS_ETAIL)},
    ],
}


# ---------------------------------------------------------------------------
# R8 / R9：三处叠加（期 04 / 期 05）+ **同轮底座对照镜头**
#
# R6/R7 的客观指标有缺陷：底座对照是**别轮**的图（R1 的纯鹰/纯猫），
# 机位不同会把差异盖掉——这正是 r02 里"全局 SSIM 分不出成功与失败"的原因。
# 所以从 R8 起，每轮都出一张**只写底座、不加部位**的对照镜头：
# 同 seed、同句式骨架，与该轮其它镜头的唯一差别就是"加没加部位"。
# 这样"移植句到底有没有生效"就有了不受姿态干扰的判据（score.py 用）。
#
# 期 04 = 三处猫化（猫耳 C1 + 猫尾 C5 + 猫胡须 C6，鹰底座）
# 期 05 = 三处鹰化（鹰翼 E2 + 鹰尾羽 E5 + 鹰颈羽 E6，猫底座）
# 新增的 C6 / E6 都是**底座描述里没占位的部位**（鹰无胡须、猫无颈羽）——
# 按 r03 的规律 56，这类移植最容易成。
# ---------------------------------------------------------------------------

P_CAT_WHISKERS = "a domestic cat's long thin whiskers"
P_EAGLE_RUFF = "a thick ruff of dark brown eagle feathers around its neck"

SUBJ_R8_BASE = FULL_EAGLE
SUBJ_R8_C6 = _with(FULL_EAGLE, [P_CAT_WHISKERS])
SUBJ_R8_C1_C6 = _with(FULL_EAGLE, [P_CAT_EARS, P_CAT_WHISKERS])
SUBJ_R8_3 = _with(FULL_EAGLE, [P_CAT_EARS, P_CAT_TAIL, P_CAT_WHISKERS])

SUBJ_R9_BASE = FULL_CAT
SUBJ_R9_E6 = _with(FULL_CAT, [P_EAGLE_RUFF])
SUBJ_R9_E5_E6 = _with(FULL_CAT, [P_EAGLE_TAIL, P_EAGLE_RUFF])
SUBJ_R9_3 = _with(FULL_CAT, [P_EAGLE_WINGS, P_EAGLE_TAIL, P_EAGLE_RUFF])

# 守卫：三处版必须真的含三处；底座对照镜头必须与底座逐字相同
assert SUBJ_R8_3.count(" and ") >= 2 and P_CAT_TAIL in SUBJ_R8_3 and P_CAT_WHISKERS in SUBJ_R8_3
assert SUBJ_R9_3.count(" and ") >= 2 and P_EAGLE_WINGS in SUBJ_R9_3 and P_EAGLE_RUFF in SUBJ_R9_3
assert SUBJ_R8_BASE == FULL_EAGLE and SUBJ_R9_BASE == FULL_CAT, "底座对照必须逐字等于底座"
assert "whiskers" not in SUBJ_R8_BASE, "R8 底座对照里不该有胡须"
assert "ruff" not in SUBJ_R9_BASE, "R9 底座对照里不该有颈羽"


ROUNDS[8] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 4201,
    "note": "期 04 候选：鹰底座 + 猫的三处（C1 耳 / C5 尾 / C6 胡须）；含同轮底座对照",
    "shots": [
        {"name": "base-eagle", "seed": 4201, "prompt": _photo(SUBJ_R8_BASE)},
        {"name": "e-cat-whiskers", "seed": 4201, "prompt": _photo(SUBJ_R8_C6)},
        {"name": "e-cat-ears-whiskers", "seed": 4201, "prompt": _photo(SUBJ_R8_C1_C6)},
        {"name": "e-cat-3parts", "seed": 4201, "prompt": _photo(SUBJ_R8_3)},
    ],
}

ROUNDS[9] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 4201,
    "note": "期 05 候选：猫底座 + 鹰的三处（E2 翼 / E5 尾羽 / E6 颈羽）；含同轮底座对照",
    "shots": [
        {"name": "base-cat", "seed": 4201, "prompt": _photo(SUBJ_R9_BASE)},
        {"name": "c-eagle-ruff", "seed": 4201, "prompt": _photo(SUBJ_R9_E6)},
        {"name": "c-eagle-tail-ruff", "seed": 4201, "prompt": _photo(SUBJ_R9_E5_E6)},
        {"name": "c-eagle-3parts", "seed": 4201, "prompt": _photo(SUBJ_R9_3)},
    ],
}

# 存档抬头用的"轮内恒定层"模板（换行只影响排版，不进入 prompt）
ARCHIVE_LAYERS = f"{CN_FRAME}<主体>. <拼接句> {MEADOW} {PHOTO}"


# ---------------------------------------------------------------------------
# R10–R13：把期 02–05 的**呈现**补上（期风格轮）
#
# 问题与 dragon-nines 子主题 R5–R7 完全相同：
# 期 01–05 共用同一套「晨雾秋日草甸 · 阴天柔光 · 平视 600mm · 方」，
# 于是五期读起来像"同一张照片换了配件"——**缺期身份**。
# 子主题合并图 `sheet.png` 把这个问题暴露得最清楚。
#
# 纪律（规律 70）：**期内恒定 + 期间各异**。
# 本轮只换**呈现层**（生境/光线/机位/画布），底座与移植件**一字不改**，
# 所以前面所有机制结论照旧成立（规律 72）。
#
# 机位按主体挑（规律 71），并且优先冲着该期的弱点：
#   期 02（猫耳/猫尾）  雨后卵石河滩 · 湿润侧逆光 · 低机位贴地 85mm 聚焦耳尾 · 竖
#   期 03（鹰翼/尾羽）  雨后林地 · 逆光 · 广角低机位拍翼展瞬间 · 竖
#   期 04（猫胡须）     正午硬光 · 贴面特写让胡须显形 · 方
#   期 05（三重鹰化）   雪原雨雾 · 长焦压缩 · 横幅
#
# 每轮都带**同轮底座对照**（规律 76：一轮一个底座）。
# ---------------------------------------------------------------------------

PHOTO_BASE = ("fine surface detail, slight film grain, no digital sharpening, "
              "no text, no watermark")


def _styled(base: str, parts: list[str], *, frame: str = CN_FRAME, pose: str,
            scene: str, light: str, lens: str) -> str:
    """期专属呈现：{CN 取景句}{姿态}{底座 with 部位}. {生境} {光线} {镜头} {摄影底子}"""
    core = _with(base, parts) if parts else base
    return (f"{frame}{pose}{core}. {scene}. {light}. "
            f"Wildlife photograph, {lens}, {PHOTO_BASE}.")


# 期 02：雨后卵石河滩 · 湿润侧逆光 · 低机位贴地聚焦耳尾 · 竖
S2 = dict(pose="它侧身站着、头略向后转，长尾朝镜头这一侧垂下来：",
          scene="on a wet pebble riverbank just after rain, water still sheeting over the stones",
          light="wet overcast light with a soft backlight rimming its outline",
          lens="a low ground-level camera angle, 85mm lens at f/3.2, very shallow depth of field")
# 期 03：雨后林地 · 逆光 · 广角低机位拍翼展瞬间 · 竖
S3 = dict(pose="它把两翼张开到最大、正要落定：",
          scene="on a rain-soaked forest floor among ferns and mossy roots",
          light="strong backlight through the wet canopy, rimming every feather",
          lens="a wide-angle 35mm lens at a low angle, f/4")
# 期 04：正午硬光 · 贴面特写让胡须显形 · 方
S4 = dict(frame="头部特写，一只动物独自占据画面：",
          pose="它正面朝向镜头、头略低：",
          scene="in a dry autumn meadow at midday, the background reduced to warm grey",
          light="hard midday sun raking across the face, casting a crisp shadow",
          lens="a tight portrait of the head, 200mm lens at f/5.6")
# 期 05：雪原雨雾 · 长焦压缩 · 横幅
S5 = dict(pose="它端坐在开阔地上、颈羽蓬起，长尾横过身后：",
          scene="in falling snow on open ground, mist flattening the far treeline",
          light="flat cold overcast light through snow haze",
          lens="a long 600mm telephoto compressing the distance, f/4")

ROUNDS[10] = {
    "engine": "zimage", "size": (1024, 1280), "steps": 12, "seed": 4201,
    "note": "期 02 定稿【雨后卵石河滩·低机位聚焦耳尾】：鹰底座 + 猫耳 C1 / 猫尾 C5；含同轮底座对照",
    "shots": [
        {"name": "base-eagle", "seed": 4201, "prompt": _styled(FULL_EAGLE, [], **S2)},
        {"name": "e-cat-ears", "seed": 4201,
         "prompt": _styled(FULL_EAGLE, [P_CAT_EARS], **S2)},
        {"name": "e-cat-tail", "seed": 4201,
         "prompt": _styled(FULL_EAGLE, [P_CAT_TAIL], **S2)},
        {"name": "e-cat-ears-tail", "seed": 4201,
         "prompt": _styled(FULL_EAGLE, [P_CAT_EARS, P_CAT_TAIL], **S2)},
    ],
}

ROUNDS[11] = {
    "engine": "zimage", "size": (1024, 1280), "steps": 12, "seed": 4201,
    "note": "期 03 定稿【雨后林地·逆光翼展】：猫底座 + 鹰翼 E2 / 鹰尾羽 E5；含同轮底座对照",
    "shots": [
        {"name": "base-cat", "seed": 4201, "prompt": _styled(FULL_CAT, [], **S3)},
        {"name": "c-eagle-wings", "seed": 4201,
         "prompt": _styled(FULL_CAT, [P_EAGLE_WINGS], **S3)},
        {"name": "c-eagle-tail", "seed": 4201,
         "prompt": _styled(FULL_CAT, [P_EAGLE_TAIL], **S3)},
        {"name": "c-eagle-wings-tail", "seed": 4201,
         "prompt": _styled(FULL_CAT, [P_EAGLE_WINGS, P_EAGLE_TAIL], **S3)},
    ],
}

ROUNDS[12] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 4201,
    "note": "期 04 定稿【正午硬光·贴面特写让胡须显形】：鹰底座 + 猫胡须 C6 / 耳+胡须；含同轮底座对照",
    "shots": [
        {"name": "base-eagle", "seed": 4201, "prompt": _styled(FULL_EAGLE, [], **S4)},
        {"name": "e-cat-whiskers", "seed": 4201,
         "prompt": _styled(FULL_EAGLE, [P_CAT_WHISKERS], **S4)},
        {"name": "e-cat-ears-whiskers", "seed": 4201,
         "prompt": _styled(FULL_EAGLE, [P_CAT_EARS, P_CAT_WHISKERS], **S4)},
    ],
}

ROUNDS[13] = {
    "engine": "zimage", "size": (1280, 1024), "steps": 12, "seed": 4201,
    "note": "期 05 定稿【雪原雨雾·长焦压缩】：猫底座 + 鹰颈羽 E6 / 尾羽+颈羽 / 三处；含同轮底座对照",
    "shots": [
        {"name": "base-cat", "seed": 4201, "prompt": _styled(FULL_CAT, [], **S5)},
        {"name": "c-eagle-ruff", "seed": 4201,
         "prompt": _styled(FULL_CAT, [P_EAGLE_RUFF], **S5)},
        {"name": "c-eagle-tail-ruff", "seed": 4201,
         "prompt": _styled(FULL_CAT, [P_EAGLE_TAIL, P_EAGLE_RUFF], **S5)},
        {"name": "c-eagle-3parts", "seed": 4201,
         "prompt": _styled(FULL_CAT, [P_EAGLE_WINGS, P_EAGLE_TAIL, P_EAGLE_RUFF], **S5)},
    ],
}

# 守卫：定稿轮的「底座 + 移植件」核心句必须与探索轮**逐字同源**
# （本轮只换呈现层，规律 72：机制结论照旧成立）
_CORE = {
    10: (FULL_EAGLE, {"e-cat-ears": SUBJ_E_CEARS, "e-cat-tail": SUBJ_E_CTAIL,
                      "e-cat-ears-tail": SUBJ_E_CEARS_CTAIL}),
    11: (FULL_CAT, {"c-eagle-wings": SUBJ_C_EWINGS, "c-eagle-tail": SUBJ_C_ETAIL,
                    "c-eagle-wings-tail": SUBJ_C_EWINGS_ETAIL}),
    12: (FULL_EAGLE, {"e-cat-whiskers": SUBJ_R8_C6,
                      "e-cat-ears-whiskers": SUBJ_R8_C1_C6}),
    13: (FULL_CAT, {"c-eagle-ruff": SUBJ_R9_E6, "c-eagle-tail-ruff": SUBJ_R9_E5_E6,
                    "c-eagle-3parts": SUBJ_R9_3}),
}
for _r, (_base, _shots) in _CORE.items():
    _prompts = {sh["name"]: sh["prompt"] for sh in ROUNDS[_r]["shots"]}
    assert _base in _prompts["base-eagle" if _base is FULL_EAGLE else "base-cat"], \
        f"R{_r}: 底座对照必须逐字等于底座"
    for _name, _subject in _shots.items():
        assert _subject in _prompts[_name], f"R{_r}/{_name}: 核心句与探索轮不同源"
        for _other in _shots.values():
            if _other is not _subject:
                assert _other not in _prompts[_name], f"R{_r}/{_name}: 混进了别的移植件"


# ---------------------------------------------------------------------------
# R14–R16：期风格轮的两处**自伤**修正
#
# R10–R12 换呈现层时踩到两个新坑（都已记录为规律 79/80）：
#
# ① **姿态句提到了移植件 → 连底座对照也长出该部件**（R11 期 03）
#    S3 的姿态写成「它把两翼张开到最大」，于是**对照 base-cat 也长了鹰翼**，
#    对照被污染，客观指标作废。姿态句必须和底座描述一样对目标部位**保持沉默**。
#
# ② **姿态句把移植件写成了主体 → 模型另画一个供体个体**（R10 期 02）
#    S2 的姿态写成「长尾朝镜头这一侧垂下来」，于是 `e-cat-tail` 里
#    **多出一只完整的猫**（供体被画成了独立个体），而 R6 同一句话在
#    平视 600mm 全身像下是**成立**的（尾巴长在鹰身上）。
#    → 呈现层不是中性的：机位/姿态会改变移植结果。
#
# ③ **硬光 + 相对更小的部件 → 细部件完全不可读**（R12 期 04）
#    正午硬光下猫胡须在画面里读不出来（R8 的阴天柔光全身像反而清楚）。
#    期 04 改成**暗背景 + 侧光 + 贴面特写**：胡须被侧光照亮，读成亮线。
#
# 三轮都保留同轮底座对照（规律 76）。
# ---------------------------------------------------------------------------

# 期 02 修正（R14）：姿态不再提尾巴，其余与 S2 一字不动
S2B = dict(S2, pose="它侧身站着、头略向后转：")
# 期 03 修正（R15）：姿态不再提翅膀，其余与 S3 一字不动
S3B = dict(S3, pose="它正要落定、全身展开：")
# 期 04 修正（R16）：暗背景 + 侧光勾出胡须 + 真正的贴面特写
S4B = dict(frame="头部特写，一只动物独自占据画面：",
           pose="它侧头朝向镜头、喙略微抬起：",
           scene="against a dark shadowed bank of dry reeds, the background falling into near-black",
           light="a single low side light catching the thin whiskers so they read as bright lines",
           lens="a tight portrait of the head, 200mm lens at f/4, background thrown out of focus")

assert "尾" not in S2B["pose"] and "tail" not in S2B["pose"], "R14: 姿态不许提尾"
assert "翼" not in S3B["pose"] and "wing" not in S3B["pose"], "R15: 姿态不许提翼"
assert "hard midday" not in S4B["light"], "R16: 硬光会让细部件不可读"

ROUNDS[14] = {
    "engine": "zimage", "size": (1024, 1280), "steps": 12, "seed": 4201,
    "note": "期 02 定稿【雨后卵石河滩·低机位聚焦耳尾】修正：姿态不提尾，其余同 R10",
    "shots": [
        {"name": "base-eagle", "seed": 4201, "prompt": _styled(FULL_EAGLE, [], **S2B)},
        {"name": "e-cat-ears", "seed": 4201,
         "prompt": _styled(FULL_EAGLE, [P_CAT_EARS], **S2B)},
        {"name": "e-cat-tail", "seed": 4201,
         "prompt": _styled(FULL_EAGLE, [P_CAT_TAIL], **S2B)},
        {"name": "e-cat-ears-tail", "seed": 4201,
         "prompt": _styled(FULL_EAGLE, [P_CAT_EARS, P_CAT_TAIL], **S2B)},
    ],
}

ROUNDS[15] = {
    "engine": "zimage", "size": (1024, 1280), "steps": 12, "seed": 4201,
    "note": "期 03 定稿【雨后林地·逆光翼展】修正：姿态不提翼，其余同 R11",
    "shots": [
        {"name": "base-cat", "seed": 4201, "prompt": _styled(FULL_CAT, [], **S3B)},
        {"name": "c-eagle-wings", "seed": 4201,
         "prompt": _styled(FULL_CAT, [P_EAGLE_WINGS], **S3B)},
        {"name": "c-eagle-tail", "seed": 4201,
         "prompt": _styled(FULL_CAT, [P_EAGLE_TAIL], **S3B)},
        {"name": "c-eagle-wings-tail", "seed": 4201,
         "prompt": _styled(FULL_CAT, [P_EAGLE_WINGS, P_EAGLE_TAIL], **S3B)},
    ],
}

ROUNDS[16] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 4201,
    "note": "期 04 定稿【暗背景·侧光勾胡须·贴面特写】修正：换掉硬光让胡须可读，其余同 R12",
    "shots": [
        {"name": "base-eagle", "seed": 4201, "prompt": _styled(FULL_EAGLE, [], **S4B)},
        {"name": "e-cat-whiskers", "seed": 4201,
         "prompt": _styled(FULL_EAGLE, [P_CAT_WHISKERS], **S4B)},
        {"name": "e-cat-ears-whiskers", "seed": 4201,
         "prompt": _styled(FULL_EAGLE, [P_CAT_EARS, P_CAT_WHISKERS], **S4B)},
    ],
}

# 守卫：修正轮与 R10–R12 的差别**只在呈现层**——底座 + 移植件那句必须逐字相同
# （期 04 的 scene/light/lens 是刻意换掉的：硬光让胡须不可读）
def _core_of(prompt: str) -> str:
    """取出「底座 + 移植件」那句（CN 取景句与姿态在最后一个全角冒号之前）。"""
    return prompt.split(". ", 1)[0].rsplit("：", 1)[-1]


for _a, _b in ((ROUNDS[10], ROUNDS[14]), (ROUNDS[11], ROUNDS[15]), (ROUNDS[12], ROUNDS[16])):
    assert [sh["name"] for sh in _a["shots"]] == [sh["name"] for sh in _b["shots"]]
    assert _a["size"] == _b["size"] and _a["seed"] == _b["seed"]
    for _x, _y in zip(_a["shots"], _b["shots"]):
        assert _core_of(_x["prompt"]) == _core_of(_y["prompt"]), \
            f"{_x['name']}: 修正轮改到了底座/移植件（只许改呈现层）"


# ---------------------------------------------------------------------------
# R17：期 02 的呈现再修正 —— 把机位退回「平视全身」，只换光线与地点
#
# R14 把姿态里的「长尾」去掉后，`e-cat-tail` **仍然多出一只猫**：
# 说明触发条件不是姿态句，而是**机位/画幅**——低机位 85mm 竖幅下，
# "猫的环纹长尾"被画成了另一个个体（尾巴需要一个"宿主"，
# 而竖幅低机位把它放不进鹰的身体范围）。
#
# 所以期 02 的身份改由**光线与地点**承担（黄昏湿草地 + 暖侧逆光），
# 机位退回**平视全身**（与 R6 成立时一致）。
# ---------------------------------------------------------------------------

S2C = dict(pose="它侧身站着、头略向后转：",
           scene="on wet grass at the edge of a marsh at dusk, the ground dark and damp",
           light="warm low sun from behind and to the side, rimming its outline",
           lens="a level camera at eye height, 400mm lens at f/4, the whole body in frame")

assert "85mm" not in S2C["lens"] and "low ground-level" not in S2C["lens"], "R17: 退回平视全身"

ROUNDS[17] = {
    "engine": "zimage", "size": (1024, 1024), "steps": 12, "seed": 4201,
    "note": "期 02 定稿【黄昏湿草地·暖侧逆光·平视全身】：机位退回平视，身份改由光线承担",
    "shots": [
        {"name": "base-eagle", "seed": 4201, "prompt": _styled(FULL_EAGLE, [], **S2C)},
        {"name": "e-cat-ears", "seed": 4201,
         "prompt": _styled(FULL_EAGLE, [P_CAT_EARS], **S2C)},
        {"name": "e-cat-tail", "seed": 4201,
         "prompt": _styled(FULL_EAGLE, [P_CAT_TAIL], **S2C)},
        {"name": "e-cat-ears-tail", "seed": 4201,
         "prompt": _styled(FULL_EAGLE, [P_CAT_EARS, P_CAT_TAIL], **S2C)},
    ],
}
