#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 manifest / 评分复核 / 目录结构生成站点数据（site/data/*.json）。

设计原则：
  * 只读——不改动任何图片或既有文件
  * 幂等——同样的输入产出完全相同的 JSON（无时间戳、排序稳定）
  * 零依赖——只用标准库，随仓库本身一起工作

用法：
    python3 tools/build_site.py            # 生成并打印统计
    python3 tools/build_site.py --quiet    # 只生成

数据来源：
    projects/bio-splice/SUMMARY.md             交付清单表（子主题/组/期/成品/对照/均分）
    projects/bio-splice/subjects/*/period-*/manifest.json   每个成品的元数据
    projects/bio-splice/subjects/*/rounds/rNN-review.md     每个镜头的 A–E 评分
    projects/*/                                  项目封面与说明（扁平化后图片与视频项目同处一处）
"""

import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "site", "data")

BIO = "projects/bio-splice"

# ── 缩略图 ──────────────────────────────────────────────────────────────────
# 网格若直出原图，bio-splice 单页要加载 266 张、合计 306 MB（均值 1.47 MB）。
# 所以 build 时生成 site/thumbs/：**网格与封面用缩略图，灯箱仍用原图**。
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

    ⚠️ 两个必须守住的约束（**都实际踩过**）：

    1. `src` 可能是**绝对路径**。直接 `os.path.join(THUMB_DIR, src)` 会丢掉 `THUMB_DIR`
       前缀（`os.path.join` 遇到绝对分量会丢弃前面的），把缩略图写进源目录。
       → 一律先用 `os.path.relpath(src, ROOT)` 归一。
    2. 源本身是 `.jpg` 时，上面那个 bug 会让输出路径**正好等于源路径**，
       `ffmpeg -y` 会直接把原图覆盖成 480px 缩略图（不可逆的素材损毁）。
       → 显式断言：输出必须落在 `THUMB_DIR` 内，且不等于源。

    另：**增量**（存在且不比源旧就跳过，保证 build 幂等）；**优雅退化**（没有 ffmpeg 时返回原图）。
    """
    if not src or not os.path.isfile(src):
        return None
    # 归一为仓库相对路径（CWD == 仓库根 是本脚本的既有前提）
    srcrel = os.path.relpath(src, ROOT) if os.path.isabs(src) else src
    srcrel = srcrel.replace(os.sep, "/")
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

# ── 双语标题（人工维护一次；其余文案从仓库里现成的中文文档取原文） ──────────────
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
}

# 视频项目的一句话说明（**双语**，与 projects/README.md 的项目表同源）。
# 以前 videos.json 的 desc 是空字符串；若改成抓 README 首段，抓到的是副标题而不是正文，
# 而且中英同文。登记过的用这里，未登记的才退回 README 首段。
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


def build_subject(sid, meta):
    sdir = os.path.join(BIO, "subjects", sid)
    if not os.path.isdir(sdir):
        return None
    zh, en = SUBJECT_TITLES.get(sid, (meta["zh_title"] or sid, sid))

    reviews, audit_files = index_rounds(sdir)
    cache = {}

    def scores_for(round_no, shot):
        if round_no not in reviews:
            return None
        if round_no not in cache:
            cache[round_no] = parse_review(reviews[round_no])
        return cache[round_no].get(shot)

    periods = []
    for name in sorted(os.listdir(sdir)):
        if not re.fullmatch(r"period-\d+", name):
            continue
        pdir = os.path.join(sdir, name)
        mpath = os.path.join(pdir, "manifest.json")
        if not os.path.isfile(mpath):
            continue
        with open(mpath, encoding="utf-8") as fh:
            man = json.load(fh)

        entries = []
        for ent in man.get("entries", []):
            fn = ent.get("final")
            if not fn:
                continue
            item = {
                "file": fn,
                "path": rel(os.path.join(pdir, fn)),
                "thumb": thumb_of(os.path.join(pdir, fn)),
                "size": os.path.getsize(os.path.join(pdir, fn)),
                "role": ent.get("role", "final"),
                "shot": ent.get("source_shot", ""),
                "round": ent.get("source_round"),
                "engine": ent.get("source_engine", ""),
                "seed": ent.get("seed"),
                "sha256": ent.get("sha256", ""),
                "prompt": ent.get("prompt", ""),
            }
            if item["role"] == "final" and item["round"]:
                item["scores"] = scores_for(item["round"], item["shot"])
            entries.append(item)

        periods.append({
            "id": name,
            "note": man.get("note", ""),
            "sheet": rel(os.path.join(pdir, "sheet.jpg")) if os.path.isfile(os.path.join(pdir, "sheet.jpg")) else None,
            "thumb": thumb_of(os.path.join(pdir, "sheet.jpg")),
            "readme": rel(os.path.join(pdir, "README.md")) if os.path.isfile(os.path.join(pdir, "README.md")) else None,
            "bytes": sum(e["size"] for e in entries),
            "entries": entries,
        })

    audits = [{"round": n, "path": rel(p), "thumb": thumb_of(p)}
              for n, p in sorted(audit_files.items())]

    def maybe(relpath):
        return rel(relpath) if os.path.isfile(relpath) else None

    return {
        "id": sid,
        "title": {"zh": zh, "en": en},
        "group": meta["group"],
        "stats": {
            "periods": meta["periods"],
            "finals": meta["finals"],
            "controls": meta["controls"],
            "mean": meta["mean"],
            "bytes": sum(p["bytes"] for p in periods),
        },
        "thumb": maybe(os.path.join(sdir, "sheet-thumb.jpg")),
        "sheet": maybe(os.path.join(sdir, "sheet.jpg")),
        "readme": maybe(os.path.join(sdir, "README.md")),
        "parts": maybe(os.path.join(sdir, "parts.md")),
        "audits": audits,
        "periods": periods,
    }


IMG_RE = re.compile(r"\.(png|jpe?g|webp)$", re.I)


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


def count_finals(pdir):
    """数成品：优先读 manifest.json 里 role=final 的条目，退化到文件名含 final。"""
    n = 0
    for p in walk_files(pdir):
        if not p.endswith("manifest.json"):
            continue
        try:
            with open(p, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            continue
        for e in data.get("entries", []):
            if e.get("role") == "final":
                n += 1
    return n


def build_other_projects():
    """**扫描 `projects/` 自动收录**项目卡片。

    以前这里硬编码 bone-china-doll / character-lookbook 两个项目，新建的项目
    （shanhai-jing）建好后不会出现在画廊里。改为扫描后，新增项目放进 `projects/`
    就自动进画廊；标题/说明/封面可用 PROJECTS / DOCS / COVERS 覆写。

    口径：
      * `_` 开头（_template）跳过
      * `bio-splice` 单独成卡（kind=periods，见 build_bio）
      * **含 `.mp4` 的项目归视频汇总卡**（kind=videos，见 build_videos）
      * 其余各成一卡（kind=project，点击在新标签打开它的 README）
    """
    items = []
    if not os.path.isdir(PROJECTS_DIR):
        return items
    for pid in sorted(os.listdir(PROJECTS_DIR)):
        pdir = os.path.join(PROJECTS_DIR, pid)
        if not os.path.isdir(pdir) or pid.startswith("_"):
            continue
        if pid == "bio-splice":
            continue
        if any(p.lower().endswith(".mp4") for p in walk_files(pdir)):
            continue                              # 视频项目 → 汇总卡
        title = PROJECTS.get(pid, (pid, pid))
        desc = DOCS.get(pid, ("", ""))
        finals = count_finals(pdir)
        cover = pick_cover(pid, pdir)
        items.append({
            "id": pid, "kind": "project",
            "title": {"zh": title[0], "en": title[1]},
            "desc": {"zh": desc[0], "en": desc[1]},
            # 卡片用缩略图（首页封面曾合计 5.3 MB，bone-china-doll 单张就 3.89 MB）
            "cover": thumb_of(os.path.join(ROOT, cover)) if cover else None,
            "readme": maybe_path(os.path.join(pdir, "README.md")),
            "stats": {"finals": finals} if finals else {},
        })
    return items


def maybe_path(p):
    return rel(p) if os.path.isfile(p) else None


# ── 视频 ────────────────────────────────────────────────────────────────────
SKIP_VIDEO = re.compile(r"(^|/)(api_|test_|shot_|chain_shot)", re.I)
POSTER_PREF = [
    re.compile(r"storyboard/shot1_final\.(jpg|jpeg|png)$", re.I),
    re.compile(r"storyboard/shot1.*\.(jpg|jpeg|png)$", re.I),
    re.compile(r"keyframes/shot1.*\.(jpg|jpeg|png)$", re.I),
    re.compile(r"storyboard/.*\.(jpg|jpeg|png)$", re.I),
    re.compile(r".*\.(jpg|jpeg|png)$", re.I),
]


def build_videos():
    # 扁平化后图片与视频项目同在 projects/；图片项目里没有 .mp4，
    # 下面的 `if not clips: continue` 自然把它们排除，无需另列白名单。
    vroot = "projects"
    projects = []
    total = 0
    if not os.path.isdir(vroot):
        return {"projects": [], "clips": 0}
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
                        return rel(img)
            return None

        items = []
        for clip in sorted(clips):
            size = os.path.getsize(clip)
            total += size
            poster = pick_poster(clip)
            items.append({
                "file": os.path.basename(clip),
                "path": rel(clip),
                "size": size,
                "poster": poster,
                "thumb": thumb_of(os.path.join(ROOT, poster)) if poster else None,
            })

        zh, en = pid, pid
        # 项目 README 第一行标题（形如 "# 巨人的国度 —— ..."）
        title_zh = pid
        rp = os.path.join(pdir, "README.md")
        if os.path.isfile(rp):
            with open(rp, encoding="utf-8") as fh:
                for line in fh:
                    if line.startswith("# "):
                        title_zh = line[2:].strip()
                        break
        projects.append({
            "id": pid,
            "title": {"zh": title_zh, "en": pid},
            # 说明：登记过的取双语一句话，未登记的退回 README 首段
            "desc": video_desc(pid, rp),
            "readme": maybe_path(rp),
            "clips": items,
            "poster": items[0]["poster"] if items else None,
            "size": sum(c["size"] for c in items),
            "count": len(items),
        })
    return {"projects": projects, "clips": total}


def video_desc(pid, readme):
    """视频项目说明：登记过的用双语一句话，未登记的退化为 README 首段（中英同文）。"""
    if pid in VIDEO_DOCS:
        zh, en = VIDEO_DOCS[pid]
        return {"zh": zh, "en": en}
    return first_para(readme)


def first_para(readme):
    """取 README 的第一段正文，作为双语说明的兜底（中英同文，取自中文文档）。

    跳过标题 / 引用块（`>`）/ 代码围栏 / 表格 / 图片行，取到第一段连续正文为止。
    """
    if not os.path.isfile(readme):
        return {"zh": "", "en": ""}
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
    text = " ".join(para).strip()
    return {"zh": text, "en": text}


def main():
    quiet = "--quiet" in sys.argv
    # `--no-thumbs`：跳过缩略图（网格直出原图）。给"只想看数据"或没有 ffmpeg 的环境用。
    THUMB_STATE["enabled"] = "--no-thumbs" not in sys.argv
    os.makedirs(OUT_DIR, exist_ok=True)

    summary_path = os.path.join(BIO, "SUMMARY.md")
    rows = parse_summary(summary_path)

    subjects = []
    for meta in rows:
        s = build_subject(meta["id"], meta)
        if s:
            subjects.append(s)

    subjects.sort(key=lambda s: ({"甲": 0, "乙": 1, "丙": 2}[s["group"]], -s["stats"]["mean"]))

    groups = []
    for g in ("甲", "乙", "丙"):
        members = [s["id"] for s in subjects if s["group"] == g]
        if members:
            groups.append({"id": g, "title": {"zh": GROUPS[g][0], "en": GROUPS[g][1]}, "subjects": members})

    finals = sum(1 for s in subjects for p in s["periods"] for e in p["entries"] if e["role"] == "final")
    controls = sum(1 for s in subjects for p in s["periods"] for e in p["entries"] if e["role"] == "control")
    periods = sum(len(s["periods"]) for s in subjects)
    scored = sum(1 for s in subjects for p in s["periods"] for e in p["entries"] if e.get("scores"))

    videos = build_videos()
    others = build_other_projects()

    zh, en = PROJECTS["bio-splice"]
    bio_card = {
        "id": "bio-splice", "kind": "periods",
        "title": {"zh": zh, "en": en},
        "desc": {"zh": DOCS["bio-splice"][0], "en": DOCS["bio-splice"][1]},
        "cover": rel(os.path.join(BIO, "subjects", "horn-atlas", "sheet-thumb.jpg")),
        "readme": maybe_path(os.path.join(BIO, "README.md")),
        "summary": maybe_path(os.path.join(BIO, "SUMMARY.md")),
        "stats": {"subjects": len(subjects), "periods": periods, "finals": finals, "controls": controls},
        "groups": [g["id"] for g in groups],
    }

    vz, ve = PROJECTS["video-projects"]
    video_card = {
        "id": "video-projects", "kind": "videos",
        "title": {"zh": vz, "en": ve},
        "desc": {"zh": DOCS["video-projects"][0], "en": DOCS["video-projects"][1]},
        # 缩略图挂在 clip 上（poster 是 .jpg，且可能被多个 clip 共用，故取首个 clip 的 thumb）
        "cover": ((videos["projects"][0]["clips"][0].get("thumb")
                   or videos["projects"][0].get("poster")) if videos["projects"] else None),
        # 指向项目索引（原 video-gen/README.md 已随扁平化合并删除）
        "readme": maybe_path(os.path.join(PROJECTS_DIR, "README.md")),
        "stats": {"projects": len(videos["projects"]), "clips": sum(p["count"] for p in videos["projects"])},
    }

    index = {
        "counts": {
            "subjects": len(subjects),
            "periods": periods,
            "finals": finals,
            "controls": controls,
            "scored": scored,
            "videos": sum(p["count"] for p in videos["projects"]),
            "video_bytes": videos["clips"],
        },
        "projects": [bio_card, video_card] + others,
    }

    bio = {
        "id": "bio-splice",
        "title": {"zh": zh, "en": en},
        "desc": {"zh": DOCS["bio-splice"][0], "en": DOCS["bio-splice"][1]},
        "readme": bio_card["readme"],
        "summary": bio_card["summary"],
        "plan": maybe_path(os.path.join(BIO, "PLAN.md")),
        "sheet": rel(os.path.join(BIO, "subjects", "horn-atlas", "sheet.jpg")),
        # 首个子主题合图的缩略图（8.1 MB 的子主题合图不该直接进首屏）
        "sheet_thumb": thumb_of(os.path.join(BIO, "subjects", "horn-atlas", "sheet.jpg")),
        # 评分维度随项目走：bio-splice 是 A–E 五维，shanhai-jing 是 A–F 六维。
        # 写死在 app.js 里的话，第二个项目的期详情页就会说错。
        "rubric": RUBRICS.get("bio-splice"),
        "groups": groups,
        "subjects": subjects,
    }

    def dump(name, obj):
        p = os.path.join(OUT_DIR, name)
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=1, sort_keys=False)
            fh.write("\n")
        return os.path.getsize(p)

    sizes = [
        ("index.json", dump("index.json", index)),
        ("bio-splice.json", dump("bio-splice.json", bio)),
        ("videos.json", dump("videos.json", videos)),
    ]

    if not quiet:
        print("生成完毕 → site/data/")
        for n, s in sizes:
            print("  %-18s %7.1f KB" % (n, s / 1024))
        print()
        print("  子主题 %d ｜ 期 %d ｜ 成品 %d ｜ 对照 %d ｜ 有评分 %d"
              % (len(subjects), periods, finals, controls, scored))
        print("  视频 %d 个 / %.1f MB ｜ 其它项目 %d 个"
              % (index["counts"]["videos"], videos["clips"] / 1048576, len(others)))
        t = THUMB_STATE
        if not t["enabled"]:
            print("  缩略图：已禁用（--no-thumbs），网格直出原图")
        elif t["failed"] and not ffmpeg_bin():
            print("  缩略图：⚠️  %d 张退化为原图（缺 ffmpeg）" % t["failed"])
        else:
            print("  缩略图：新生成 %d ｜ 命中缓存 %d ｜ 失败 %d（最长边 %dpx）"
                  % (t["made"], t["skipped"], t["failed"], THUMB_MAX))

    # 交付基线校验（与 SUMMARY.md 的合计数对齐）
    want = {"subjects": 12, "periods": 60, "finals": 135, "controls": 59}
    got = {"subjects": len(subjects), "periods": periods, "finals": finals, "controls": controls}
    if got != want:
        print("\n⚠️  与 SUMMARY.md 基线不一致：期望 %s，实际 %s" % (want, got), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
