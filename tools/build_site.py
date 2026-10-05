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
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "site", "data")

BIO = "projects/bio-splice"

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
    "video-gen":         ("视频生成", "Video Generation"),
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
    "video-gen": (
        "图生视频 / 文生视频的成片与方法手册，图片库的产物在这里被消费。",
        "Image-to-video / text-to-video films and method notes; the image library feeds in here.",
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
            "readme": rel(os.path.join(pdir, "README.md")) if os.path.isfile(os.path.join(pdir, "README.md")) else None,
            "bytes": sum(e["size"] for e in entries),
            "entries": entries,
        })

    audits = [{"round": n, "path": rel(p)} for n, p in sorted(audit_files.items())]

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


def build_other_projects():
    items = []

    # bone-china-doll：挑一张 final-* 当封面
    bdir = "projects/bone-china-doll"
    cover = None
    if os.path.isdir(bdir):
        cands = [p for p in walk_files(bdir) if os.path.basename(p).startswith("final") and p.endswith(".png")]
        cands.sort(key=lambda p: (0 if "east" in os.path.basename(p) else 1, len(p), p))
        if cands:
            cover = rel(cands[0])
        zh, en = PROJECTS["bone-china-doll"]
        items.append({
            "id": "bone-china-doll", "kind": "project",
            "title": {"zh": zh, "en": en},
            "desc": {"zh": DOCS["bone-china-doll"][0], "en": DOCS["bone-china-doll"][1]},
            "cover": cover,
            "readme": maybe_path(os.path.join(bdir, "README.md")),
            "stats": {},
        })

    # character-lookbook：示例项目，暂无成品图
    cdir = "projects/character-lookbook"
    if os.path.isdir(cdir):
        zh, en = PROJECTS["character-lookbook"]
        items.append({
            "id": "character-lookbook", "kind": "project",
            "title": {"zh": zh, "en": en},
            "desc": {"zh": DOCS["character-lookbook"][0], "en": DOCS["character-lookbook"][1]},
            "cover": None,
            "readme": maybe_path(os.path.join(cdir, "README.md")),
            "stats": {},
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
            items.append({
                "file": os.path.basename(clip),
                "path": rel(clip),
                "size": size,
                "poster": pick_poster(clip),
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
            "desc": {"zh": "", "en": ""},
            "readme": maybe_path(rp),
            "clips": items,
            "poster": items[0]["poster"] if items else None,
            "size": sum(c["size"] for c in items),
            "count": len(items),
        })
    return {"projects": projects, "clips": total}


def main():
    quiet = "--quiet" in sys.argv
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

    vz, ve = PROJECTS["video-gen"]
    video_card = {
        "id": "video-gen", "kind": "videos",
        "title": {"zh": vz, "en": ve},
        "desc": {"zh": DOCS["video-gen"][0], "en": DOCS["video-gen"][1]},
        "cover": videos["projects"][0]["poster"] if videos["projects"] else None,
        "readme": maybe_path("README.md"),
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

    # 交付基线校验（与 SUMMARY.md 的合计数对齐）
    want = {"subjects": 12, "periods": 60, "finals": 135, "controls": 59}
    got = {"subjects": len(subjects), "periods": periods, "finals": finals, "controls": controls}
    if got != want:
        print("\n⚠️  与 SUMMARY.md 基线不一致：期望 %s，实际 %s" % (want, got), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
