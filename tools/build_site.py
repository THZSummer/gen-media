#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 manifest / 评分复核 / README / 目录结构生成站点数据（site/data/*.json）。

设计原则：
  * 只读——不改动任何图片或既有文件
  * 幂等——同样的输入产出完全相同的 JSON（无时间戳、排序稳定）
  * 零依赖——只用标准库，随仓库本身一起工作

数据契约（**流媒体式前端**要的东西）：每个有内容的项目导出一份 `<pid>.json`，
核心是 `reels[]`（一"卷"= 可连续上下滑的一组作品）+ 每卷里的 `items[]`（一帧 = 一张图
或一段视频）。**文字全部挂在帧上**（标签 / 说明 / 提示词 / 评分），前端只负责渲染，
不再自己拼文案、也不再按项目名硬编码渲染器。

    {id, kind, title, desc, readme, summary, plan, rubric, stats,
     reels: [{id, title, desc, poster, count, period_refs, text_ref,
              items: [{kind, src, thumb, size, role, period, label, note,
                       shot, round, engine, seed, sha256, prompt, scores}]}]}

首页只读 `index.json`：项目卡片里带一条 `strip`（首页横向行的卡片），
所以**首屏不需要拉任何项目数据**。

用法：
    python3 tools/build_site.py            # 生成并打印统计
    python3 tools/build_site.py --quiet    # 只生成
    python3 tools/build_site.py --no-thumbs  # 跳过缩略图（网格直出原图）
"""

import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "site", "data")

BIO = "projects/bio-splice"

# ── 缩略图 ──────────────────────────────────────────────────────────────────
# 网格若直出原图，bio-splice 单页要加载 266 张、合计 306 MB（均值 1.47 MB）。
# 所以 build 时生成 site/thumbs/：**卡片与占位用缩略图，详情页当前帧才用原图**。
# 命名镜像源路径、扩展名改 .jpg，便于排查对应关系。
THUMB_DIR = os.path.join("site", "thumbs")
THUMB_MAX = 480          # 最长边（px）
THUMB_Q = 4              # ffmpeg -q:v：2 最好 / 31 最差
THUMB_STATE = {"enabled": True, "made": 0, "skipped": 0, "failed": 0}
_FFMPEG = None


def ffmpeg_bin():
    global _FFMPEG
    if _FFMPEG is None:
        _FFMPEG = shutil.which("ffmpeg") or ""
        if not _FFMPEG:
            print("⚠️  找不到 ffmpeg —— 缩略图退化为原图，页面会变重", file=sys.stderr)
    return _FFMPEG


def thumb_of(src):
    """返回 src 的缩略图（仓库相对路径），必要时生成。

    ⚠️ 三个必须守住的约束（**都实际踩过**）：

    1. `src` 可能是**绝对路径**。直接 `os.path.join(THUMB_DIR, src)` 会丢掉 `THUMB_DIR`
       前缀（`os.path.join` 遇到绝对分量会丢弃前面的），把缩略图写进源目录。
       → 一律先用 `os.path.relpath(src, ROOT)` 归一。
    2. 源本身是 `.jpg` 时，上面那个 bug 会让输出路径**正好等于源路径**，
       `ffmpeg -y` 会直接把原图覆盖成 480px 缩略图（不可逆的素材损毁）。
       → 显式断言：输出必须落在 `THUMB_DIR` 内，且不等于源。
    3. **已经是缩略图**的路径不能再缩一遍（会生成 `site/thumbs/site/thumbs/...` 套娃）。
       → 命中 `THUMB_DIR` 前缀就直接返回。

    另：**增量**（存在且不比源旧就跳过，保证 build 幂等）；**优雅退化**（没有 ffmpeg 时返回原图）。
    """
    if not src or not os.path.isfile(src):
        return None
    # 归一为仓库相对路径（CWD == 仓库根 是本脚本的既有前提）
    srcrel = os.path.relpath(src, ROOT) if os.path.isabs(src) else src
    srcrel = srcrel.replace(os.sep, "/")
    if os.path.normpath(srcrel).startswith(os.path.normpath(THUMB_DIR) + os.sep):
        return srcrel
    if not THUMB_STATE["enabled"]:
        return srcrel
    exe = ffmpeg_bin()
    if not exe:
        THUMB_STATE["failed"] += 1
        return srcrel
    out = os.path.join(THUMB_DIR, os.path.splitext(srcrel)[0] + ".jpg").replace(os.sep, "/")
    if os.path.normpath(out) == os.path.normpath(srcrel):
        raise RuntimeError("缩略图输出会覆盖源文件，已中止：%s" % srcrel)
    if not os.path.normpath(out).startswith(os.path.normpath(THUMB_DIR) + os.sep):
        raise RuntimeError("缩略图输出越出 %s，已中止：%s" % (THUMB_DIR, out))
    if os.path.isfile(out) and os.path.getmtime(out) >= os.path.getmtime(src):
        THUMB_STATE["skipped"] += 1
        return out
    os.makedirs(os.path.dirname(out), exist_ok=True)
    vf = (f"scale='min({THUMB_MAX},iw)':'min({THUMB_MAX},ih)'"
          f":force_original_aspect_ratio=decrease")
    r = subprocess.run([exe, "-v", "error", "-y", "-i", srcrel, "-vf", vf,
                        "-q:v", str(THUMB_Q), out],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if r.returncode != 0 or not os.path.isfile(out):
        THUMB_STATE["failed"] += 1
        return srcrel
    THUMB_STATE["made"] += 1
    return out


# ── 文字工具 ────────────────────────────────────────────────────────────────
MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")


def plain(s):
    """把 README 里的一小段 markdown 还原成能直接上屏的纯文本。

    仓库文档里的说明句常带 `**加粗**`、`「」`、行内代码与链接；直接塞进 JSON
    会在页面上露出星号。这里只做去噪，不改写内容。
    """
    if not s:
        return ""
    s = MD_LINK.sub(r"\1", s)
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"(?<!\*)\*(?!\*)", "", s)
    s = s.replace("<br>", " ").replace("\\", "")
    return re.sub(r"[ \t]+", " ", s).strip()


def first_para(readme):
    """取 README 的第一段正文，作为说明文字的兜底（中英同文，取自中文文档）。

    跳过标题 / 引用块（`>`）/ 代码围栏 / 表格 / 图片行，取到第一段连续正文为止。
    """
    if not readme or not os.path.isfile(readme):
        return ""
    para = []
    with open(readme, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not para:
                if (not line or line.startswith(("#", ">", "```", "|", "!", "---"))
                        or line.startswith("<!--")):
                    continue
                para.append(line)
            else:
                if not line or line.startswith(("#", "```", "|", "---")):
                    break
                para.append(line)
    return plain(" ".join(para))


def en_mate(p):
    """`X.md` → `X.en.md`（本仓库的双语命名约定）。"""
    return re.sub(r"\.md$", ".en.md", p) if p and p.endswith(".md") else None


def read_para(path):
    """一段文档的中英说明：中文取 `X.md`，英文取 `X.en.md`；英文缺件时退回中文。"""
    zh = first_para(path)
    en = first_para(en_mate(path)) if path else ""
    return {"zh": zh, "en": en or zh}


H1 = re.compile(r"^#\s+(.*)$")
PERIOD_PREFIX = re.compile(r"^(?:第\s*[0-9一二三四五六七八九十]+\s*(?:期|部分)\s*·\s*|Period\s*\d+\s*·\s*|Part\s*\d+\s*·\s*)",
                           re.I)


def read_h1(path, strip_prefix=False):
    """README 的一级标题（期标题常写成「第一期 · 猫头鹰」，可去掉序号前缀）。"""
    if not path or not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = H1.match(line.strip())
            if m:
                t = plain(m.group(1))
                return PERIOD_PREFIX.sub("", t) if strip_prefix else t
    return ""


# ── 双语标题（人工维护一次；其余文案从仓库里现成的文档取原文） ──────────────
SUBJECT_TITLES = {
    "cat-eagle":     ("猫 + 鹰", "Cat + Eagle"),
    "dragon-nines":  ("龙 · 九似", "Dragon · Nine Resemblances"),
    "turtle-snake":  ("龟 + 蛇（玄武）", "Turtle + Snake (Black Tortoise)"),
    "fish-bird":     ("鱼 + 鸟（鲲鹏）", "Fish + Bird (Kunpeng)"),
    "deer-crane":    ("鹿 + 鹤（鹿鹤同春）", "Deer + Crane"),
    "lichen":        ("地衣 = 真菌 + 藻", "Lichen = Fungus + Alga"),
    "cordyceps":     ("冬虫夏草 = 菌 + 虫", "Cordyceps = Fungus + Insect"),
    "flytrap-fang":  ("捕蝇草 + 动物器官", "Venus Flytrap + Animal Parts"),
    "flower-bird":   ("花 + 鸟", "Flower + Bird"),
    "tree-beast":    ("树 + 兽", "Tree + Beast"),
    "wing-atlas":    ("翅 · 图鉴", "Wing Atlas"),
    "horn-atlas":    ("角 · 图鉴", "Horn Atlas"),
    # 山海经（没有 SUMMARY.md，标题靠这张表；缺失时退回目录名）
    "jiu-wei-hu":    ("九尾狐", "Nine-Tailed Fox"),
    "lu-shu":        ("鹿蜀", "Lu-Shu"),
    "bo-yi":         ("猼訑", "Bo-Yi"),
}

GROUPS = {
    "甲": ("同界跨界（动物 × 动物）", "Cross-species (animal × animal)"),
    "乙": ("跨域拼接（动物 × 植物 × 菌）", "Cross-kingdom (animal × plant × fungus)"),
    "丙": ("部件图鉴（同一底座轮换器官）", "Part atlas (same base, rotating organs)"),
}

PROJECTS = {
    "bio-splice":        ("生物拼接", "Bio Splice"),
    "bone-china-doll":   ("骨瓷人偶", "Bone-China Doll"),
    "character-lookbook": ("角色设定图库", "Character Lookbook"),
    "shanhai-jing":      ("山海经 · 图赞", "Shan Hai Jing · Illustrated Verses"),
    "video-projects":    ("视频项目", "Video Projects"),
}

DOCS = {
    "bio-splice": (
        "跨物种、跨界的“部位移植”图像实验：12 个子主题 × 5 期，135 件成品，"
        "每轮带同轮底座对照，成品全部经五维评分过关。",
        "Cross-species / cross-kingdom part-transplant studies: 12 sub-themes × 5 periods, "
        "135 curated finals, each round paired with a same-round base control.",
    ),
    "bone-china-doll": (
        "以「骨瓷」质感为统一材质约束的人偶形象系列，逐轮做 A/B 消融对照。",
        "A doll series under one material constraint (bone china), developed with round-by-round A/B ablations.",
    ),
    "character-lookbook": (
        "角色多角度设定图库（示例项目）：正面锚点 → 补视角 → 换场景 → 换装。",
        "Multi-angle character lookbook (example project): front anchor → more views → scenes → outfits.",
    ),
    "shanhai-jing": (
        "以《山海经》原文为纲的图赞连载：一兽一期，标注卷次 + 原文 + 郭璞注，"
        "面向小红书竖版；出图到制版的完整过程（含失败迭代）都留档。",
        "Illustrated-verse series driven by the verbatim Shan Hai Jing: one creature per period with "
        "volume, original passage and commentary; the full generate-to-typeset process is recorded.",
    ),
    "video-projects": (
        "图生视频 / 文生视频的成片与方法手册，图片项目的产物在这里被消费。",
        "Image-to-video / text-to-video films and method notes; image projects feed in here.",
    ),
}

# 项目卡片目录：**扫描式收录**（新增项目放进 projects/ 即自动进画廊）。
# 之前这里硬编码项目清单，导致新建的 shanhai-jing 一直没进画廊。
PROJECTS_DIR = "projects"

# 封面显式覆写；未列出的走自动挑选（见 pick_cover）
COVERS = {
    # 图赞主图（成品卡片）比白描画心更适合当画廊封面
    "shanhai-jing": "projects/shanhai-jing/subjects/jiu-wei-hu/period-01/02-jiu-wei-hu-zan.png",
}

# 各项目的评分维度（**逐项目**，不要写进 app.js）：
#   bio-splice 用 A–E 五维；shanhai-jing 用 A–F 六维（多一个「气韵生动」）。
# 未登记的项目不带 rubric，前端就不渲染那一行。
RUBRICS = {
    "bio-splice": {
        "zh": "A 移植到位 .30 ｜ B 底座完整 .20 ｜ C 解剖可信 .20 ｜ D 摄影统一 .15 ｜ E 概念可读 .15",
        "en": "A transplant fidelity .30 | B base integrity .20 | C anatomy .20 | "
              "D photographic unity .15 | E concept readability .15",
    },
    "shanhai-jing": {
        "zh": "A 考据准确 .25 ｜ F 气韵生动 .25 ｜ B 骨法纯正 .15 ｜ C 制式完整 .15 ｜ "
              "D 辨识度 .10 ｜ E 系列一致 .10",
        "en": "A sourcing accuracy .25 | F vitality of brushwork .25 | B bone purity .15 | "
              "C format completeness .15 | D legibility .10 | E series consistency .10",
    },
}

# 视频项目的一句话说明（**双语**，与 projects/README.md 的项目表同源）。
VIDEO_DOCS = {
    "giant-kingdom": (
        "穿越到巨人女儿国：体型反差的视觉奇观（巨手遮天 / 掌心如地 / 一肩一世界）。",
        "Into the giant kingdom: a body-scale contrast spectacle (a hand blotting out the sky, "
        "a palm for ground, a shoulder for a world).",
    ),
    "step-scenery": (
        "移步换景：少女穿越时空，一步一世界（茶室 → 竹林 → 沙漠 → 赛博 → 星空 → 雪原 → 茶室闭环）。",
        "Step scenery: a girl crossing time, one step one world "
        "(tea room → bamboo → desert → cyber → starfield → snow → back to the tea room).",
    ),
    "step-scenery-v2": (
        "移步换景 v2：同故事，seedance-2.0 原生音频版（每镜自带场景音效）。",
        "Step scenery v2: same story, seedance-2.0 native-audio version, each shot with its own ambience.",
    ),
    "survival-island": (
        "荒岛求生：6 镜 30s 剧情短片，18 岁东方少女 × 极致反差（荒岛不荒、人更惨）。",
        "Survival island: a 6-shot 30s narrative short — an 18-year-old Eastern girl and extreme contrast.",
    ),
    "tea-shake-dance": (
        "来杯好茶摇一摇：艺术舞蹈短片，以「摇一摇」为动作母题，茶文化跳成现代舞（6 镜逐镜详解）。",
        "Tea shake dance: an art-dance short built on the \"shake\" motif, turning tea culture into "
        "modern dance (all 6 shots detailed).",
    ),
}

# 视频项目的双语名（中文取自各项目 README 的一级标题）
VIDEO_TITLES = {
    "giant-kingdom":   ("蝴蝶女大冒险", "Butterfly Girl"),
    "step-scenery":    ("移步换景", "Step Scenery"),
    "step-scenery-v2": ("移步换景 v2", "Step Scenery v2"),
    "survival-island": ("荒岛求生", "Survival Island"),
    "tea-shake-dance": ("来杯好茶摇一摇", "Tea Shake Dance"),
}

# 图集项目（无 manifest）的**卷**：目录 → 阶段标题（全部取自各项目 README 的阶段划分）
GALLERY_REELS = {
    "bone-china-doll": {
        "out":             ("定稿单图", "Final stills"),
        "final-set":       ("第二阶段定稿", "Phase 2 finals"),
        "final-set-east":  ("三阶段 · 东方古典公主", "Phase 3 · Classical Eastern princess"),
        "final-set-gauze": ("四阶段 · 半纱半瓷", "Phase 4 · Half gauze, half porcelain"),
        "final-set-life":  ("五阶段 · 起居瞬间", "Phase 5 · Living moments"),
    },
}

# 图集项目的逐帧标签：文件名（去扩展名）→ 双语短语。
# 这些名字来自文件命名与 README 里已有的中文说法，不是新编的内容描述。
GALLERY_FILE_LABELS = {
    "hero": "主图 / Hero",
    "portrait": "肖像 / Portrait",
    "seated": "坐姿 / Seated",
    "full-figure": "全身 / Full figure",
    "tang-portrait": "唐装肖像 / Tang-style portrait",
    "airy-turn": "轻纱转身 / Airy turn",
    "gauze-macro": "轻纱微距 / Gauze macro",
    "skin-macro": "肤质微距 / Skin macro",
    "macro-wrist": "手腕微距 / Wrist macro",
    "macro-chest": "胸前微距 / Chest macro",
    "macro-hairpin": "发簪微距 / Hairpin macro",
    "macro-necklace": "项链微距 / Necklace macro",
    "macro-slipper": "绣鞋微距 / Slipper macro",
    "macro-tiara": "冠饰微距 / Tiara macro",
    "doze": "伏案打盹 / Dozing",
    "mat-by-window": "窗边矮榻 / Mat by the window",
    "prone": "伏卧 / Prone",
    "recline": "侧卧 / Reclining",
    "detail-study-joint-hand": "关节手部研究 / Jointed hand study",
    "final-bone-china-princess": "定稿 · 公主 / Final · Princess",
    "final-bone-china-princess-v2": "定稿 · v2 / Final · v2",
    "final-bone-china-princess-east": "定稿 · 东方古典 / Final · Classical East",
    "final-bone-china-princess-gauze": "定稿 · 半纱半瓷 / Final · Gauze porcelain",
    "final-bone-china-princess-life": "定稿 · 起居瞬间 / Final · Living moment",
}

# 帧的角色（前端按 role 上徽标与配色；这里只定义**取值**，文案在 app.js 的 T 里）
ROLE_FINAL = "final"

VERDICT_OK = "✅"


def rel(p):
    """仓库内相对路径。

    存相对路径而不是站点绝对路径，是为了兼容两种部署：
      * 本地预览：站点根 = 仓库根
      * GitHub Pages：站点根 = /gen-media/
    前端用 location.pathname 推出站点前缀再拼接（见 site/app.js 的 BASE）。
    """
    return p.replace(os.sep, "/")


def walk_files(sub):
    out = []
    for base, _dirs, files in os.walk(sub):
        for f in files:
            out.append(os.path.join(base, f))
    return sorted(out)


def maybe_path(p):
    return rel(p) if os.path.isfile(p) else None


IMG_RE = re.compile(r"\.(png|jpe?g|webp)$", re.I)


# ── SUMMARY.md 交付清单表 ────────────────────────────────────────────────────
ROW = re.compile(
    r"^\|\s*\[([a-z0-9\-]+)\]\(subjects/[^)]+\)\s*(.*?)\s*\|\s*([甲乙丙])\s*\|"
    r"\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\d.]+|\*\*[\d.]+\*\*)\s*\|"
)


def parse_summary(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = ROW.match(line.rstrip("\n"))
            if not m:
                continue
            sid, title, group, periods, finals, controls, mean = m.groups()
            rows.append({
                "id": sid,
                "zh_title": title.strip(),
                "group": group,
                "periods": int(periods),
                "finals": int(finals),
                "controls": int(controls),
                "mean": float(mean.strip("*")),
            })
    return rows


# ── rounds/rNN-review.md 的评分表 ───────────────────────────────────────────
SCORE_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|(.+)\|\s*$")

# 轮次文件名不统一，实测有三种写法，用「可选前缀 + 不补零」一次覆盖：
#   cat-eagle     r01-review.md        （补零、无前缀）
#   turtle-snake  ts-r3-review.md      （子主题缩写前缀）
#   flower-bird   fb2-r1-review.md · dragon-nines dn-r10-review.md（多字符前缀 / 两位数轮次）
ROUND_FILE = re.compile(r"^(?:[A-Za-z0-9]+-)?r(\d+)-(review|audit)\.(md|jpg)$")


def index_rounds(sdir):
    """按轮次索引复核文件：({round: review.md}, {round: audit.jpg})"""
    reviews, audits = {}, {}
    rdir = os.path.join(sdir, "rounds")
    if not os.path.isdir(rdir):
        return reviews, audits
    for f in sorted(os.listdir(rdir)):
        m = ROUND_FILE.match(f)
        if not m:
            continue
        n, kind = int(m.group(1)), m.group(2).lower()
        target = reviews if kind == "review" else audits
        target.setdefault(n, os.path.join(rdir, f))
    return reviews, audits


def parse_review(path):
    """返回 {shot: {A..E, total, verdict, global_diff, region_diff}}"""
    scores = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = SCORE_ROW.match(line.rstrip("\n"))
            if not m:
                continue
            shot, rest = m.group(1), m.group(2)
            cells = [c.strip() for c in rest.split("|")]
            if len(cells) < 8:
                continue
            try:
                a, b, c, d, e = (int(x) for x in cells[:5])
                total = float(cells[5].strip("*"))
            except ValueError:
                continue
            row = {
                "A": a, "B": b, "C": c, "D": d, "E": e,
                "total": total,
                "verdict": cells[6],
                "global_diff": cells[7],
                "region_diff": cells[8] if len(cells) > 8 else "",
            }
            old = scores.get(shot)
            # 同一镜头多次出现时，优先保留判定为成品的那一行
            if old is None or (VERDICT_OK in row["verdict"] and VERDICT_OK not in old["verdict"]):
                scores[shot] = row
    return scores


# ── 期 README 的「成品表」→ 逐帧短标签 ──────────────────────────────────────
# 表头形如 `| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |`，第三列就是
# 「这张画的是什么」。实测有 8 种列布局（移植部位 / 拼接语义 / 叠加 / 只有评分），
# 所以只认「第二列是指向本目录图片的 Markdown 链接」的行，取第三列；第三列长得像
# 分数就丢弃。取不到就留空——前端会退回期级说明。实测覆盖率约 46%，
# 剩下的一半是「只有评分」的布局，宁缺毋滥。
SCORE_LIKE = re.compile(r"^\*{0,2}[\d.]+")


def read_captions(pdir):
    """{文件名: {zh, en}}：期 README 成品表第三列的逐帧短标签。"""
    out = {}
    for lang, fn in (("zh", "README.md"), ("en", "README.en.md")):
        p = os.path.join(pdir, fn)
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as fh:
            for line in fh:
                if not line.startswith("|"):
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) < 3:
                    continue
                m = MD_LINK.search(cells[1])
                if not m or not IMG_RE.search(m.group(2)):
                    continue
                cap = plain(cells[2])
                if not cap or SCORE_LIKE.match(cap):
                    continue
                out.setdefault(os.path.basename(m.group(2)), {})[lang] = cap
    return {k: {"zh": v.get("zh", v.get("en", "")), "en": v.get("en", v.get("zh", ""))}
            for k, v in out.items()}


def frame_label(caps, filename, note, ekind=""):
    """逐帧标签 → (label|None, note 正文)。

    取值顺序：README 成品表的短标签 > manifest note 的抬头 > manifest `kind`（画心/卡片）。
    都没有就返回 None——前端退回 role 的名字（定稿 / 对照 / 合图），**不硬翻、不留空**。
    """
    head, rest = split_note(note)
    c = caps.get(filename)
    if c and c.get("zh"):
        label = {"zh": c["zh"], "en": c.get("en") or LABEL_EN.get(c["zh"], "")}
    elif head:
        label = {"zh": head["zh"], "en": LABEL_EN.get(head["zh"], "")}
    elif ekind in FRAME_KIND_LABELS:
        zh, en = FRAME_KIND_LABELS[ekind]
        label = {"zh": zh, "en": en}
    else:
        label = None
    return label, rest


def split_note(note):
    """把 manifest 的 `note` 拆成（短标签, 余下正文）。

    shanhai-jing 的 note 写成「图赞主图：卷次 + 榜题 + 画心 + 点睛句 + 出處」，
    冒号前那截正好是这张图的类型（抬头上限 12 字，避免把整句当标题）；
    没有冒号时退一步认「白描画心（供制版使用）」这种「短语（限定）」写法。
    """
    note = plain(note)
    if "：" in note:
        head, rest = note.split("：", 1)
        if 0 < len(head) <= 12:
            return {"zh": head, "en": ""}, rest.strip()
    m = re.match(r"^([^（）()]{2,12})[（(]([^）)]*)[）)]\s*$", note)
    if m:
        return {"zh": m.group(1).strip(), "en": ""}, m.group(2).strip()
    return None, note


# manifest 里 `kind` 字段的双语名（区分画心与制版卡；没有更具体的标签时用它）
# 默认画心名跟着**当前骨法**走：山海经 2026-10-06 起骨法是赭石设色（R7 定案），
# 白描只是 R7 之前的路线；真要用白描，在 manifest 的 note 里显式写标签即可。
FRAME_KIND_LABELS = {
    "plate": ("设色画心", "Coloured plate"),
    "card": ("图赞卡片", "Verse card"),
}

# note 抬头只有中文、但英文界面也需要一个能读的标题时，用这张小表；查不到就留空，
# 前端会退回 role 的名字（定稿 / 对照 / 合图）——**不硬翻、不留空**。
LABEL_EN = {
    "白描画心": "Ink plate",
    "设色画心": "Coloured plate",
    "跨引擎对照": "Cross-engine",
    "同轮底座对照（写法维度）": "Same-round control (wording)",
    "形态最强但有印（已退役）": "Strongest, but sealed (retired)",
    "图赞主图": "Illustrated verse",
    "原文卡": "Source-text card",
    "第 1 轮审计": "Round 1 audit",
    "擦除前原样": "Before erasure",
    "更浓的虎纹（有印）": "Bolder stripes (sealed)",
    "更浓的尾巴（有印）": "Stronger tails (sealed)",
    "旧引擎对照": "Old engine",
    "中文直述对照": "Chinese direct",
    "设色代价": "Cost of colour",
}


# ── 帧（feed 的一屏）────────────────────────────────────────────────────────
def image_frame(src, role, *, label=None, note="", period="", **meta):
    """一张图 = 详情页里的一帧。src 为仓库相对路径。"""
    abspath = os.path.join(ROOT, src)
    return {
        "kind": "image",
        "file": os.path.basename(src),
        "src": rel(src),
        "thumb": thumb_of(abspath),
        "size": os.path.getsize(abspath) if os.path.isfile(abspath) else 0,
        "role": role,
        "period": period,
        "label": label,
        "note": note,
        **meta,
    }


def prettify(stem):
    return re.sub(r"[_\-]+", " ", stem).strip()


def gallery_label(file):
    stem = os.path.splitext(file)[0]
    if stem in GALLERY_FILE_LABELS:
        zh, _, en = GALLERY_FILE_LABELS[stem].partition(" / ")
        return {"zh": zh, "en": en or zh}
    return {"zh": prettify(stem), "en": prettify(stem)}


# ── 卷（reel = 可连续上下滑的一组作品）──────────────────────────────────────
def reel(rid, title, desc, items, *, poster=None, periods=None, text_ref=None, doc=None):
    items = [it for it in items if it]
    return {
        "id": rid,
        "title": title,
        "desc": desc,
        "poster": poster or next((it.get("thumb") or it.get("src") for it in items), None),
        "cover": next((it.get("src") for it in items), None),
        "count": len(items),
        # 成品数单列一份：卷的总数里混着合图/对照/审计，卡片上写"36 件"会虚高
        "finals": sum(1 for it in items if it.get("role") == ROLE_FINAL),
        "bytes": sum(it.get("size") or 0 for it in items),
        "periods": periods or [],
        "text_ref": text_ref,
        "doc": doc,
        "items": items,
    }


def build_subject_reel(sid, meta, proot):
    """装配一个「期结构」子主题：成品在前，合图 / 对照 / 轮次审计在后。

    顺序是刻意的——**正文与过程件分开**：一进来滑到的都是定稿；
    继续往下才是同轮对照、本期合图、轮次审计（每帧都带 role 徽标与配色）。
    """
    sdir = os.path.join(proot, "subjects", sid)
    if not os.path.isdir(sdir):
        return None
    zh, en = SUBJECT_TITLES.get(sid, (meta.get("zh_title") or sid, sid))

    reviews, audit_files = index_rounds(sdir)
    cache = {}

    def scores_for(round_no, shot):
        if round_no not in reviews:
            return None
        if round_no not in cache:
            cache[round_no] = parse_review(reviews[round_no])
        return cache[round_no].get(shot)

    finals, extras, periods, text_ref = [], [], [], None
    for name in sorted(os.listdir(sdir)):
        if not re.fullmatch(r"period-\d+", name):
            continue
        pdir = os.path.join(sdir, name)
        mpath = os.path.join(pdir, "manifest.json")
        if not os.path.isfile(mpath):
            continue
        with open(mpath, encoding="utf-8") as fh:
            man = json.load(fh)

        caps = read_captions(pdir)
        note = plain(man.get("note", ""))
        ptitle = read_h1(os.path.join(pdir, "README.md"), strip_prefix=True)
        ptitle_en = read_h1(os.path.join(pdir, "README.en.md"), strip_prefix=True)
        # 期标题来自期 README 的一级标题；没有 README（shanhai-jing）就留空，
        # 前端会用「第 N 期」的界面标签兜底——**不要把目录名 period-01 当标题**
        period_title = {"zh": ptitle, "en": ptitle_en}
        periods.append({
            "id": name,
            "title": period_title,
            "note": note,
            "doc": maybe_path(os.path.join(pdir, "README.md")),
        })
        text_ref = text_ref or man.get("text_ref")

        period_finals, period_extras = [], []
        for ent in man.get("entries", []):
            fn = ent.get("final")
            if not fn:
                continue
            src = rel(os.path.join(pdir, fn))
            if not os.path.isfile(os.path.join(ROOT, src)):
                continue
            role = ent.get("role", ROLE_FINAL)
            label, note_body = frame_label(caps, os.path.basename(fn),
                                           ent.get("note", ""), ent.get("kind", ""))
            frame = image_frame(
                src, role,
                label=label,
                note=note_body,
                period=name,
                shot=ent.get("source_shot", ""),
                round=ent.get("source_round"),
                engine=ent.get("source_engine", "") or ent.get("source", ""),
                seed=ent.get("seed"),
                sha256=ent.get("sha256", ""),
                prompt=ent.get("prompt", ""),
            )
            if role == ROLE_FINAL and frame["round"]:
                frame["scores"] = scores_for(frame["round"], frame["shot"])
            (period_finals if role == ROLE_FINAL else period_extras).append(frame)

        # 本期合图（把本期的成品拼在一张上）——放在本期成品之后
        sheet = os.path.join(pdir, "sheet.jpg")
        if os.path.isfile(sheet):
            period_extras.insert(0, image_frame(
                rel(sheet), "sheet", period=name,
                label={"zh": "本期合图", "en": "Period contact sheet"},
                note=note))
        finals += period_finals
        extras += period_extras

    if not finals and not extras:
        return None

    # 子主题总览合图与轮次审计图排在最后
    for p in (os.path.join(sdir, "sheet.jpg"),):
        if os.path.isfile(p):
            extras.append(image_frame(rel(p), "sheet",
                                      label={"zh": "全套合图", "en": "All-periods contact sheet"},
                                      note=read_para(os.path.join(sdir, "README.md"))["zh"]))
    for n, p in sorted(audit_files.items()):
        extras.append(image_frame(rel(p), "audit", round=n,
                                  label={"zh": "第 %d 轮审计" % n, "en": "Round %d audit" % n},
                                  note=""))

    desc = read_para(os.path.join(sdir, "README.md"))
    if not desc["zh"]:
        # 子主题没有自己的 README（shanhai-jing）：拿本期 manifest 的 note 当卷说明——
        # 那句话本来就是这个子主题最完整的交代，不必再编一段。
        desc = {"zh": periods[0]["note"] if periods else "",
                "en": periods[0]["note"] if periods else ""}
    # 子主题自带的 sheet-thumb.jpg 本来就是缩略图 → 直接当卡面，**不要再缩一遍**
    # （缩一遍只会多出一堆 site/thumbs/…/sheet-thumb.jpg 套娃文件）
    st = os.path.join(sdir, "sheet-thumb.jpg")
    poster = rel(st) if os.path.isfile(st) else None
    return reel(sid, {"zh": zh, "en": en}, desc, finals + extras,
                poster=poster,
                periods=periods,
                text_ref=text_ref,
                doc=maybe_path(os.path.join(sdir, "README.md")))


def build_gallery_reels(pid, pdir):
    """图集项目：**按目录分卷**（每个阶段一卷），成品在前、其余按目录名排序。"""
    imgs = [p for p in walk_files(pdir) if IMG_RE.search(p)]
    imgs = [p for p in imgs if not GALLERY_SKIP.search(rel(p))]
    if not imgs:
        return []
    labels = GALLERY_REELS.get(pid, {})
    buckets = {}
    for p in imgs:
        buckets.setdefault(os.path.basename(os.path.dirname(p)), []).append(p)

    def order(d):
        return (0 if d == "out" else 1, d)

    reels = []
    for d in sorted(buckets, key=order):
        paths = buckets[d]
        finals = sorted(p for p in paths if os.path.basename(p).lower().startswith("final"))
        rest = sorted(p for p in paths if p not in finals)
        items = []
        for p in finals + rest:
            f = os.path.basename(p)
            items.append(image_frame(rel(p), ROLE_FINAL if p in finals else "image",
                                     label=gallery_label(f)))
        zh, en = labels.get(d, (d, d))
        # 卷说明：第一段用项目简介（双语、已人工校过），其余阶段用阶段名——都比
        # 「README 第一段」稳，后者抓到的常是 markdown 项目符号清单。
        if d == "out":
            desc = {"zh": DOCS.get(pid, ("", ""))[0], "en": DOCS.get(pid, ("", ""))[1]}
        else:
            desc = {"zh": zh, "en": en}
        reels.append(reel(d, {"zh": zh, "en": en}, desc, items))
    return reels


def build_video_reels():
    """视频项目：**每个子项目一卷**，卷里是它的成片。"""
    vroot = "projects"
    reels = []
    if not os.path.isdir(vroot):
        return reels
    for pid in sorted(os.listdir(vroot)):
        pdir = os.path.join(vroot, pid)
        if not os.path.isdir(pdir) or pid.startswith("_"):
            continue
        clips = [p for p in walk_files(pdir) if p.lower().endswith(".mp4")]
        clips = [p for p in clips if not SKIP_VIDEO.search(p)]
        if not clips:
            continue
        imgs = [p for p in walk_files(pdir) if re.search(r"\.(jpg|jpeg|png)$", p, re.I)]

        def pick_poster(clip):
            # 先在同目录附近的图片里按偏好挑，退化为项目内第一张图
            for pat in POSTER_PREF:
                for img in imgs:
                    if pat.search(img):
                        return img
            return None

        items = []
        for clip in sorted(clips):
            poster = pick_poster(clip)
            stem = os.path.splitext(os.path.basename(clip))[0]
            items.append({
                "kind": "video",
                "file": os.path.basename(clip),
                "src": rel(clip),
                "thumb": thumb_of(os.path.join(ROOT, poster)) if poster else None,
                "poster": rel(poster) if poster else None,
                "size": os.path.getsize(clip),
                "role": "video",
                "period": "",
                "label": {"zh": "成片" if len(clips) == 1 else prettify(stem),
                          "en": "Film" if len(clips) == 1 else prettify(stem)},
                "note": "",
            })
        rp = os.path.join(pdir, "README.md")
        zh, en = VIDEO_TITLES.get(pid, (read_h1(rp) or pid, pid))
        reels.append(reel(pid, {"zh": zh, "en": en}, video_desc(pid, rp), items,
                          doc=maybe_path(rp)))
    return reels


def video_desc(pid, readme):
    """视频项目说明：登记过的用双语一句话，未登记的退化为 README 首段（中英同文）。"""
    if pid in VIDEO_DOCS:
        zh, en = VIDEO_DOCS[pid]
        return {"zh": zh, "en": en}
    p = first_para(readme)
    return {"zh": p, "en": p}


SKIP_VIDEO = re.compile(r"(^|/)(api_|test_|shot_|chain_shot)", re.I)
POSTER_PREF = [
    re.compile(r"storyboard/shot1_final\.(jpg|jpeg|png)$", re.I),
    re.compile(r"storyboard/shot1.*\.(jpg|jpeg|png)$", re.I),
    re.compile(r"keyframes/shot1.*\.(jpg|jpeg|png)$", re.I),
    re.compile(r"storyboard/.*\.(jpg|jpeg|png)$", re.I),
    re.compile(r".*\.(jpg|jpeg|png)$", re.I),
]

# 扁平图集项目：排除中间件 / 对照 / 审计 / 微距消融板
GALLERY_SKIP = re.compile(r"(^|/)(controls?|audit|macro|refs?|storyboard|frame)", re.I)


def discover_subjects(pdir):
    """**没有 SUMMARY.md 的项目**：扫 `subjects/*/period-*/manifest.json` 自建子主题元数据。

    bio-splice 的交付清单表写在 SUMMARY.md 里；shanhai-jing 这类新项目没有那份表，
    但目录结构与 manifest 完全同构，所以照样能装配——**不该因为没有 SUMMARY 就没有详情页**。
    """
    sroot = os.path.join(pdir, "subjects")
    rows = []
    if not os.path.isdir(sroot):
        return rows
    for sid in sorted(os.listdir(sroot)):
        sdir = os.path.join(sroot, sid)
        if not os.path.isdir(sdir):
            continue
        periods, finals, controls = [], 0, 0
        for name in sorted(os.listdir(sdir)):
            if not re.fullmatch(r"period-\d+", name):
                continue
            mpath = os.path.join(sdir, name, "manifest.json")
            if not os.path.isfile(mpath):
                continue
            periods.append(name)
            try:
                with open(mpath, encoding="utf-8") as fh:
                    man = json.load(fh)
            except ValueError:
                continue
            for e in man.get("entries", []):
                if e.get("role") == ROLE_FINAL:
                    finals += 1
                else:
                    controls += 1
        if not periods:
            continue
        rows.append({
            "id": sid, "zh_title": sid, "group": "",
            "periods": len(periods), "finals": finals, "controls": controls, "mean": 0.0,
        })
    return rows


def pick_cover(pid, pdir):
    """挑项目封面：显式覆写 → `final-*` → 期目录首图 → 项目首图。

    优先级是"确定性"的（walk_files 已排序），所以同输入永远同一张封面。
    """
    if pid in COVERS:
        p = COVERS[pid]
        return rel(p) if p and os.path.isfile(p) else None
    imgs = [p for p in walk_files(pdir) if IMG_RE.search(p)]
    # 排除对照图/审计图：它们是过程件，不代表项目观感
    imgs = [p for p in imgs if "/controls/" not in p and "audit" not in os.path.basename(p).lower()]
    for pat in (r"/final[-_]", r"/period-\d+/0?1-", r"/sheet-thumb\."):
        for p in imgs:
            if re.search(pat, p, re.I):
                return rel(p)
    return rel(imgs[0]) if imgs else None


def kind_of_reel(pid, pdir):
    """项目归类：periods（有期 manifest）/ videos（有 mp4）/ gallery（有图）/ empty。"""
    if discover_subjects(pdir):
        return "periods"
    if any(p.lower().endswith(".mp4") for p in walk_files(pdir)):
        return "videos"
    if any(IMG_RE.search(p) for p in walk_files(pdir)):
        return "gallery"
    return "empty"


def strip_of(kind, pid, reels, cap=12):
    """首页横向行的卡片（**写进 index.json**，首页因此不必拉任何项目数据）。

    1. 有多个卷（子主题 / 阶段 / 视频项目）→ 每卷一张卡，点进该卷的第一帧；
    2. 只有一个卷 → 直接摊开这一卷的帧（最多 12 张），点进那一帧。
    """
    cards = []
    if len(reels) > 1:
        for r in reels[:cap]:
            n = r["finals"] or r["count"]
            cards.append({
                "title": r["title"], "poster": r["poster"],
                "route": "w/%s/r/%s" % (pid, r["id"]),
                "count": n,
                "unit": {"zh": "件成品" if kind != "videos" else "段成片",
                         "en": "finals" if kind != "videos" else "films"},
            })
        return cards
    for r in reels:
        for i, it in enumerate(r["items"][:cap], 1):
            cards.append({
                "title": it.get("label") or r["title"],
                "poster": it.get("thumb") or it.get("src"),
                "route": "w/%s/r/%s/%d" % (pid, r["id"], i),
                "count": None, "unit": None,
            })
    return cards


def project_doc(pid, kind, pdir, reels, *, cover=None, plan=None, summary=None, rubric=None):
    """装配项目文档与首页卡片（两者的关系：卡片带 strip，文档带 reels）。"""
    title = PROJECTS.get(pid, (pid, pid))
    desc = DOCS.get(pid, ("", ""))
    total = sum(r["count"] for r in reels)
    n_final = sum(1 for r in reels for it in r["items"] if it.get("role") == ROLE_FINAL)
    n_control = sum(1 for r in reels for it in r["items"]
                    if it.get("role") in ("control", "retired-control"))
    if kind == "videos":
        stats = {"projects": len(reels), "clips": total}
    elif kind == "periods":
        stats = {"reels": len(reels), "periods": sum(len(r["periods"]) for r in reels),
                 "finals": n_final, "controls": n_control}
    else:
        stats = {"reels": len(reels), "images": total, "finals": n_final}
    if cover is None:
        cover = pick_cover(pid, pdir)
    poster = cover if cover and cover.startswith(THUMB_DIR + "/") else (
        thumb_of(os.path.join(ROOT, cover)) if cover else None)
    doc = {
        "id": pid, "kind": kind,
        "title": {"zh": title[0], "en": title[1]},
        "desc": {"zh": desc[0], "en": desc[1]},
        "readme": maybe_path(os.path.join(pdir, "README.md")),
        "summary": summary,
        "plan": plan,
        "rubric": rubric,
        "data": pid + ".json",
        "stats": stats,
        "reels": reels,
    }
    card = {
        "id": pid, "kind": kind,
        "title": doc["title"], "desc": doc["desc"],
        "cover": poster,
        "readme": doc["readme"],
        "summary": summary,
        "plan": plan,
        "data": pid + ".json",
        "stats": stats,
        "reel_count": len(reels),
        "strip": strip_of(kind, pid, reels),
    }
    return card, doc


def build_periods_project(pid, pdir):
    """「期结构」项目：一卷 = 一个子主题。子主题元数据有 SUMMARY.md 就用，没有就自动发现。"""
    summary = os.path.join(pdir, "SUMMARY.md")
    rows = parse_summary(summary) if os.path.isfile(summary) else discover_subjects(pdir)
    reels = [r for r in (build_subject_reel(m["id"], m, pdir) for m in rows) if r]
    if not reels:
        return None, None

    def gkey(r):
        m = next((x for x in rows if x["id"] == r["id"]), {})
        return ({"甲": 0, "乙": 1, "丙": 2}.get(m.get("group", ""), 9),
                -m.get("mean", 0.0))
    reels.sort(key=gkey)
    return project_doc(pid, "periods", pdir, reels,
                       plan=maybe_path(os.path.join(pdir, "PLAN.md")),
                       summary=maybe_path(summary),
                       rubric=RUBRICS.get(pid))


def build_gallery_project(pid, pdir):
    """「图集」项目：一卷 = 一个阶段目录（bone-china-doll 这种没有 manifest 的项目）。"""
    reels = build_gallery_reels(pid, pdir)
    if not reels:
        return None, None
    return project_doc(pid, "gallery", pdir, reels)


def build_video_project():
    """视频汇总项目：一卷 = 一个视频子项目。

    `pdir` 传 `projects/`（README 就是项目索引），封面直接用第一卷首帧的缩略图，
    免得为了挑封面去 walk 整个仓库。
    """
    reels = build_video_reels()
    if not reels:
        return None, None
    cover = None
    for r in reels:
        for it in r["items"]:
            cover = it.get("thumb") or it.get("poster")
            break
        if cover:
            break
    return project_doc("video-projects", "videos", PROJECTS_DIR, reels, cover=cover)


def build_other_projects():
    """**扫描 `projects/` 自动收录**项目卡片。

    口径（与 kind_of_reel 一致）：
      * `_` 开头（_template）跳过
      * 含 `.mp4` 的归视频汇总（kind=videos）
      * 有 `subjects/*/period-*/manifest.json` 的走期结构（kind=periods）
      * 有图的走图集（kind=gallery）
      * 都没有的（character-lookbook）仍外链 README
    返回 (cards, data_files)：data_files 是 {文件名: 对象}，由 main 落盘。
    """
    cards, data_files = [], {}
    if not os.path.isdir(PROJECTS_DIR):
        return cards, data_files
    for pid in sorted(os.listdir(PROJECTS_DIR)):
        pdir = os.path.join(PROJECTS_DIR, pid)
        if not os.path.isdir(pdir) or pid.startswith("_"):
            continue
        if pid == "bio-splice":
            continue          # 旗舰项目单独装配（页首大图固定用 horn-atlas，见 main）
        kind = kind_of_reel(pid, pdir)
        if kind == "videos":
            continue                              # 视频 → 汇总项目
        if kind == "periods":
            card, doc = build_periods_project(pid, pdir)
        elif kind == "gallery":
            card, doc = build_gallery_project(pid, pdir)
        else:
            card, doc = None, None
        if card:
            cards.append(card)
            data_files[card["data"]] = doc
            continue
        # 无内容：保留外链卡片，明确显示"暂无成品"
        title = PROJECTS.get(pid, (pid, pid))
        desc = DOCS.get(pid, ("", ""))
        cards.append({
            "id": pid, "kind": "project",
            "title": {"zh": title[0], "en": title[1]},
            "desc": {"zh": desc[0], "en": desc[1]},
            "cover": None,
            "readme": maybe_path(os.path.join(pdir, "README.md")),
            "stats": {},
            "strip": [],
        })
    return cards, data_files


def main():
    quiet = "--quiet" in sys.argv
    # `--no-thumbs`：跳过缩略图（卡片直出原图）。给"只想看数据"或没有 ffmpeg 的环境用。
    THUMB_STATE["enabled"] = "--no-thumbs" not in sys.argv
    os.makedirs(OUT_DIR, exist_ok=True)

    # bio-splice 也走**通用的「期结构」装配**，不再内联特写——
    # 这样 shanhai-jing 这类同构项目自动获得同样的详情页。
    bio_card, bio = build_periods_project("bio-splice", BIO)
    bio_reels = bio["reels"]
    subjects = len(bio_reels)
    periods = sum(len(r["periods"]) for r in bio_reels)
    finals = sum(1 for r in bio_reels for it in r["items"] if it["role"] == ROLE_FINAL)
    controls = sum(1 for r in bio_reels for it in r["items"] if it["role"] == "control")
    scored = sum(1 for r in bio_reels for it in r["items"] if it.get("scores"))
    total_bytes = sum(r["bytes"] for r in bio_reels)
    # bio 的页首大图固定用 horn-atlas（封面与合图都从它取，保持既有观感）
    horn = os.path.join(BIO, "subjects", "horn-atlas", "sheet.jpg")
    if os.path.isfile(horn):
        bio["cover"] = rel(horn)
        bio["cover_thumb"] = thumb_of(horn)
        bio_card["cover"] = bio["cover_thumb"]

    video_card, video_doc = build_video_project()
    others, other_data = build_other_projects()

    index = {
        "counts": {
            "subjects": subjects,
            "periods": periods,
            "finals": finals,
            "controls": controls,
            "scored": scored,
            "videos": (video_card or {}).get("stats", {}).get("clips", 0),
            "video_bytes": sum(r["bytes"] for r in video_doc["reels"]) if video_doc else 0,
        },
        "projects": [bio_card] + ([video_card] if video_card else []) + others,
    }

    def dump(name, obj):
        p = os.path.join(OUT_DIR, name)
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=1, sort_keys=False)
            fh.write("\n")
        return os.path.getsize(p)

    # 每个有内容的项目各存一份 `<pid>.json`（前端按 #/p/<pid> · #/w/... 懒加载）
    project_files = dict(other_data)
    project_files[bio["data"]] = bio
    if video_doc:
        project_files[video_doc["data"]] = video_doc

    sizes = [("index.json", dump("index.json", index))]
    sizes += [(n, dump(n, o)) for n, o in sorted(project_files.items())]

    if not quiet:
        print("生成完毕 → site/data/")
        for n, s in sizes:
            print("  %-22s %7.1f KB" % (n, s / 1024))
        print()
        print("  卷 %d ｜ 期 %d ｜ 成品 %d ｜ 对照 %d ｜ 有评分 %d ｜ 成品合计 %.1f MB"
              % (subjects, periods, finals, controls, scored, total_bytes / 1048576))
        vc = index["counts"]
        print("  视频 %d 个 / %.1f MB ｜ 其它项目 %d 个"
              % (vc["videos"], vc["video_bytes"] / 1048576, len(others)))
        t = THUMB_STATE
        if not t["enabled"]:
            print("  缩略图：已禁用（--no-thumbs），卡片直出原图")
        elif t["failed"] and not ffmpeg_bin():
            print("  缩略图：⚠️  %d 张退化为原图（缺 ffmpeg）" % t["failed"])
        else:
            print("  缩略图：新生成 %d ｜ 命中缓存 %d ｜ 失败 %d（最长边 %dpx）"
                  % (t["made"], t["skipped"], t["failed"], THUMB_MAX))

    # 交付基线校验（与 SUMMARY.md 的合计数对齐）
    want = {"subjects": 12, "periods": 60, "finals": 135, "controls": 59}
    got = {"subjects": subjects, "periods": periods, "finals": finals, "controls": controls}
    if got != want:
        print("\n⚠️  与 SUMMARY.md 基线不一致：期望 %s，实际 %s" % (want, got), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
