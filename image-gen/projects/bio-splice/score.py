#!/usr/bin/env python3
"""给一轮产物打分：客观指标（脚本算）+ 主观维度（人填），按门槛判定能否作为成品。

为什么要打分
------------
「每期只放成品」这条纪律如果只靠"我觉得行"，迟早会滑。所以拆成两部分：

* **客观**（本脚本算）：与**同轮同 seed 的底座对照图**的差异。
  区域差异是**单向判据**：
    - 区域几乎没变（< 1.5）→ 该部位**肯定没落地**（本仓多次踩到空操作句：`no wings at all`、`exactly one head`）
    - 区域变了 → **不能**证明是部位造成的（换词引起的姿态漂移也会让区域变），必须目视确认
  所以客观指标只用来**报警**，不用来给分。
* **主观**（人填，见 scores.json）：移植到位 / 底座完整 / 解剖可信 / 摄影统一 / 概念可读。

> 方法论补强：要拿到不受姿态干扰的客观判据，**每轮必须有一张只写底座、不加部位的对照镜头**
> （同 seed、同句式骨架）。没有它，与别轮的对照图比会被机位差异干扰——这正是 r02 里
> "全局 SSIM 分不出成功与失败"的原因。

用法
----
  python3 score.py --round work/r8/round.json \\
      --scores work/r8/scores.json \\
      --control base-eagle \\
      --base subjects/cat-eagle/period-01/controls/eagle.png \\
      --region head=280,30,460,420 --region rear=520,360,480,520 \\
      --audit-sheet subjects/cat-eagle/rounds/r08-audit.png \\
      -o subjects/cat-eagle/rounds/r08-review.md

`scores.json` 格式::

  {
    "base_label": "纯鹰底座（同轮 base-eagle 镜头）",
    "shots": {
      "e-cat-whiskers": {
        "A": 4, "B": 5, "C": 5, "D": 5, "E": 3,
        "good": ["胡须细而清晰", "鹰头与翼羽完好"],
        "bad":  ["胡须与颈羽有点混"],
        "fatal": []
      }
    }
  }

维度与权重（满分 5）：A 移植到位 .30 ｜ B 底座完整 .20 ｜ C 解剖可信 .20 ｜
D 摄影统一 .15 ｜ E 概念可读 .15

判定：
  * `fatal` 非空          → ❌ 不合格（一眼假：双头 / 穿模 / 拼贴突兀）
  * A < 3                 → ❌ 不合格（移植没到位）
  * B < 3                 → ❌ 不合格（底座被毁）
  * 总分 ≥ 4.0 且 A ≥ 4   → ✅ 成品（首选）
  * 总分 ≥ 3.5            → ✅ 成品
  * 其余                  → ⚠️ 备选（**不纳入成品**，与 ❌ 一样不进期目录）
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.normpath(os.path.join(HERE, "..", "..", "skills", "image-tools", "scripts"))
sys.path.insert(0, TOOLS)
import contact_sheet as cs  # noqa: E402
import ffkit  # noqa: E402
import pngdiff  # noqa: E402

WEIGHTS = {"A": 0.30, "B": 0.20, "C": 0.20, "D": 0.15, "E": 0.15}
LABELS = {
    "A": "移植到位", "B": "底座完整", "C": "解剖可信", "D": "摄影统一", "E": "概念可读",
}
# 区域几乎不变时提示"移植句空操作"的阈值（平均通道差）
NOOP_THRESHOLD = 1.5


def _shot_path(round_json: str, shot: dict) -> str | None:
    f = shot.get("file")
    if not f:
        return None
    base = os.path.dirname(os.path.abspath(round_json))
    beside = os.path.join(base, os.path.basename(f))
    return beside if os.path.exists(beside) else (f if os.path.isabs(f) else os.path.join(base, f))


def _region_diff(path_a: str, path_b: str, box: tuple[int, int, int, int]) -> float:
    """指定区域内的平均通道差（0–255）。"""
    a = ffkit.decode(path_a)[:, :, :3]
    b = ffkit.decode(path_b)[:, :, :3]
    ca = ffkit.crop(a, *box)
    cb = ffkit.crop(b, *box)
    h = min(ca.shape[0], cb.shape[0])
    w = min(ca.shape[1], cb.shape[1])
    d = abs(ca[:h, :w].astype("int16") - cb[:h, :w].astype("int16"))
    return float(d.mean())


def _parse_box(text: str) -> tuple[str, tuple[int, int, int, int]]:
    name, _, nums = text.partition("=")
    parts = [int(p) for p in nums.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("--region needs name=x,y,w,h")
    return name, (parts[0], parts[1], parts[2], parts[3])


def grade(marks: dict) -> tuple[float, str]:
    total = sum(WEIGHTS[k] * float(marks.get(k, 0)) for k in WEIGHTS)
    if marks.get("fatal"):
        return total, "❌ 不合格"
    if float(marks.get("A", 0)) < 3:
        return total, "❌ 不合格（移植没到位）"
    if float(marks.get("B", 0)) < 3:
        return total, "❌ 不合格（底座被毁）"
    if total >= 4.0 and float(marks.get("A", 0)) >= 4:
        return total, "✅ 成品（首选）"
    if total >= 3.5:
        return total, "✅ 成品"
    return total, "⚠️ 备选"



def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--round", required=True, help="work/rN/round.json")
    ap.add_argument("--scores", required=True, help="人工评分 JSON")
    ap.add_argument("--control", help="同轮的底座对照镜头名（推荐；没有则客观指标仅供参考）")
    ap.add_argument("--skip", action="append", default=[], metavar="SHOT",
                    help="跳过其它对照/参照镜头，不打分（可重复）")
    ap.add_argument("--base", help="底座对照图（用于区域变化的旁证）")
    ap.add_argument("--region", action="append", type=_parse_box, default=[],
                    help="部位落点区域 name=x,y,w,h（可重复）")
    ap.add_argument("--audit-sheet", help="把各区域放大 ×2 拼成一张审计图（评分依据）")
    ap.add_argument("--subject", default="cat-eagle", help="子主题名（写进抬头）")
    ap.add_argument("-o", "--out", required=True, help="输出 Markdown 复核报告")
    args = ap.parse_args(argv)

    rj = os.path.join(HERE, args.round)
    if not os.path.exists(rj):
        print(f"error: no such round.json: {rj}", file=sys.stderr)
        return 2
    rdata = json.load(open(rj, encoding="utf-8"))
    marks_all = json.load(open(os.path.join(HERE, args.scores), encoding="utf-8"))
    marks = marks_all.get("shots", {})
    shots = {s["name"]: s for s in rdata.get("shots", [])}

    control = args.control
    if control and control not in shots:
        print(f"error: --control {control!r} is not a shot in this round", file=sys.stderr)
        return 2
    base_path = None
    if control:
        base_path = _shot_path(rj, shots[control])
    elif args.base:
        base_path = os.path.join(HERE, args.base)

    rows, audit = [], []
    for name, shot in shots.items():
        if name == control or name in set(args.skip):
            continue
        path = _shot_path(rj, shot)
        m = marks.get(name)
        if not path or not os.path.exists(path):
            rows.append({"name": name, "path": None, "marks": m, "verdict": "❌ 无产物"})
            continue
        total, verdict = grade(m or {})
        entry = {"name": name, "path": path, "marks": m, "total": total, "verdict": verdict}
        if base_path and os.path.exists(base_path):
            entry["global"] = pngdiff.compare(base_path, path, metrics=False)
            entry["regions"] = {rn: _region_diff(base_path, path, box) for rn, box in args.region}
            noop = [rn for rn, v in entry["regions"].items() if v < NOOP_THRESHOLD]
            entry["noop_suspect"] = noop
        if args.base and not control:
            entry["vs_base"] = pngdiff.compare(os.path.join(HERE, args.base), path, metrics=False)
        rows.append(entry)
        for rn, box in args.region:
            arr = ffkit.decode(path)[:, :, :3]
            out = os.path.join(".scratch", "score", f"{name}-{rn}.png")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            ffkit.encode(out, ffkit.scale_to(ffkit.crop(arr, *box), 2))
            audit.append((out, f"{name} · {rn}"))

    rows.sort(key=lambda r: (-(r.get("total") or -1)))

    lines = [
        f"# 打分复核 · R{rdata.get('round')}（{args.subject}）",
        "",
        f"> 引擎：`{rdata.get('engine')}`　轮次说明：{rdata.get('note','')}",
        f"> 底座对照：**{marks_all.get('base_label', control or args.base or '（无）')}**"
        + (f"　未评分（对照/参照）：{'、'.join('`'+s+'`' for s in args.skip)}" if args.skip else "")
        + ("（同轮同 seed，客观指标不受姿态干扰）" if control else "（**非同一轮**，客观指标仅供参考）"),
        "> 评分维度：A 移植到位 .30 ｜ B 底座完整 .20 ｜ C 解剖可信 .20 ｜ D 摄影统一 .15 ｜ E 概念可读 .15",
        "> 门槛：`fatal` 非空 / A<3 / B<3 → 不合格；总分 ≥4.0 且 A≥4 → 首选成品；≥3.5 → 成品；其余为备选（**不纳入成品**）",
        "> 客观指标只用于报警（区域差 < 1.5 = 移植句空操作），不参与给分",
        "",
        "| 镜头 | A | B | C | D | E | 总分 | 判定 | 与底座全局差 | 区域差 |",
        "|------|---|---|---|---|---|------|------|--------------|--------|",
    ]
    for r in rows:
        m = r.get("marks") or {}
        cells = " | ".join(str(m.get(k, "–")) for k in "ABCDE")
        gdiff = f"{r['global'].mean_abs_diff:.2f}" if r.get("global") else "–"
        reg = " ".join(f"{k} {v:.1f}" for k, v in (r.get("regions") or {}).items()) or "–"
        total = f"{r['total']:.2f}" if r.get("total") is not None else "–"
        lines.append(f"| `{r['name']}` | {cells} | **{total}** | {r['verdict']} | {gdiff} | {reg} |")

    lines += ["", "## 逐条优缺点", ""]
    for r in rows:
        m = r.get("marks") or {}
        lines.append(f"### `{r['name']}` — {r.get('verdict')}"
                     + (f"（总分 {r['total']:.2f}）" if r.get("total") is not None else ""))
        for k in "ABCDE":
            if k in m:
                lines.append(f"- **{k} {LABELS[k]}**：{m[k]}/5")
        for g in m.get("good", []):
            lines.append(f"- 👍 {g}")
        for b in m.get("bad", []):
            lines.append(f"- 👎 {b}")
        for f in m.get("fatal", []):
            lines.append(f"- ⛔ **致命**：{f}")
        if r.get("noop_suspect"):
            lines.append(f"- ⚠️ 区域几乎未变（{', '.join(r['noop_suspect'])}）→ "
                         "该部位的移植句疑似**空操作**，请对照审计图确认")
        if not m:
            lines.append("- （未填评分）")
        lines.append("")

    keep = [r for r in rows if r.get("verdict", "").startswith("✅")]
    lines += [
        "## 结论",
        "",
        f"- 可纳入成品：**{len(keep)}** 张 —— "
        + ("、".join(f"`{r['name']}`" for r in keep) if keep else "（无）"),
        f"- 不合格：{sum(1 for r in rows if r.get('verdict','').startswith('❌'))} 张；"
        f"备选（同样不纳入成品）：{sum(1 for r in rows if r.get('verdict','').startswith('⚠️'))} 张",
        f"- 建议主图：`{keep[0]['name']}`" if keep else "- 建议主图：无（本轮无可交付成品）",
        "",
        "> 判定依据（局部放大审计图）见 "
        + (f"[`{os.path.relpath(os.path.join(HERE, args.audit_sheet), os.path.dirname(os.path.join(HERE, args.out)))}`]"
           f"({os.path.relpath(os.path.join(HERE, args.audit_sheet), os.path.dirname(os.path.join(HERE, args.out)))})"
           if args.audit_sheet else "（未生成）"),
        "",
    ]

    if args.audit_sheet and audit:
        cs.build_sheet([p for p, _ in audit], os.path.join(HERE, args.audit_sheet),
                       cols=len(args.region) or 1, cell=0, labels=[l for _, l in audit],
                       title=f"R{rdata.get('round')} 评分审计 · 区域放大 ×2")

    out_path = os.path.join(HERE, args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"wrote {args.out}")
    for r in rows:
        print(f"  {r['name']:28s} {r.get('verdict','–')}"
              + (f"  {r['total']:.2f}" if r.get("total") is not None else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
