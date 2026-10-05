#!/usr/bin/env python3
"""把 work/ 里的**成品**提升到 subjects/<子主题>/period-NN/，并留下出处。

为什么需要它
------------
项目纪律是「每期只放成品，不放半成品」。手工 cp 有两个问题：
  1. 分不清哪张是哪张——丢了 seed / prompt_id / prompt，事后无法复核
  2. 手一滑就把探索产物拷进交付目录

所以成品只能经由本脚本进入交付目录，并在期目录写一份 `manifest.json`
记录每个成品的来源轮次、镜头名、seed、prompt_id 与 prompt 原文。

用法
----
  python3 curate.py \
      --period subjects/cat-eagle/period-01 \
      --from work/r1/round.json \
      --pick owl-seamless=01-owl-seamless \
      --pick owl-seam=02-owl-seam \
      --control cat=controls/cat \
      --control eagle=controls/eagle

`--pick` 把某个镜头作为**成品**收进期目录根；`--control` 作为**对照**收进子目录
（对照不是该期的成品，是系列的参照系）。

退出码：0 成功；1 有镜头名在 round.json 里找不到；2 参数/路径错误。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _resolve(round_json: str, base: str, name: str) -> str | None:
    """Locate the image for a shot name.

    ``round.json`` records the path that was written at generation time, which
    goes stale as soon as the project is reorganised -- so the recorded path is
    only a hint; the file sitting next to ``round.json`` wins when it exists.
    """
    data = json.load(open(round_json, encoding="utf-8"))
    for shot in data.get("shots", []):
        if shot.get("name") != name:
            continue
        f = shot.get("file")
        if not f:
            return None
        beside = os.path.join(base, os.path.basename(f))
        if os.path.exists(beside):
            return beside
        return f if os.path.isabs(f) else os.path.join(base, f)
    return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--period", required=True, help="期目录，如 subjects/cat-eagle/period-01")
    ap.add_argument("--from", dest="round_json", required=True, help="来源 work/rN/round.json")
    ap.add_argument("--pick", action="append", default=[], metavar="SHOT=NAME",
                    help="收为成品（可重复）")
    ap.add_argument("--control", action="append", default=[], metavar="SHOT=PATH",
                    help="收为对照并复制进期目录（可重复）")
    ap.add_argument("--ref", action="append", default=[], metavar="NAME=PATH",
                    help="只登记引用、不复制：NAME 是期目录内的显示名，PATH 是已存在的"
                         "相对路径（相对期目录）。用于复用别期的基准图，避免重复存拷贝")
    ap.add_argument("--note", help="写进 manifest 的本期说明")
    ap.add_argument("--force", action="store_true", help="覆盖已存在的成品")
    args = ap.parse_args(argv)

    round_json = os.path.normpath(os.path.join(HERE, args.round_json))
    period = os.path.normpath(os.path.join(HERE, args.period))
    if not os.path.exists(round_json):
        print(f"error: no such round.json: {round_json}", file=sys.stderr)
        return 2
    if not os.path.isdir(period):
        print(f"error: no such period dir: {period} (create it first)", file=sys.stderr)
        return 2

    base = os.path.dirname(round_json)
    rdata = json.load(open(round_json, encoding="utf-8"))
    byname = {s.get("name"): s for s in rdata.get("shots", [])}

    entries: list[dict] = []
    missing: list[str] = []
    for spec, role in ([(p, "final") for p in args.pick]
                       + [(c, "control") for c in args.control]
                       + [(r, "reference") for r in args.ref]):
        if "=" not in spec:
            print(f"error: expected SHOT=NAME, got {spec!r}", file=sys.stderr)
            return 2
        shot_name, dest_name = spec.split("=", 1)
        if role == "reference":
            # 左边 = 期目录内的显示名；右边 = 真实的相对路径（相对期目录）
            display, real = shot_name, dest_name
            target = os.path.join(period, real)
            if not os.path.exists(target):
                print(f"error: reference target missing: {target}", file=sys.stderr)
                return 2
            entries.append({"final": display, "path": real, "role": role,
                            "note": "复用已有基准图，未复制", "sha256": _sha256(target)})
            continue
        src = _resolve(round_json, base, shot_name)
        if not src or not os.path.exists(src):
            missing.append(shot_name)
            continue
        dest = os.path.join(period, dest_name + ".png")
        if os.path.exists(dest) and not args.force:
            print(f"error: {dest} exists (use --force)", file=sys.stderr)
            return 2
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src, dest)
        shot = byname.get(shot_name, {})
        entries.append({
            "final": dest_name + ".png",
            "path": dest_name + ".png",
            "role": role,
            "source_round": rdata.get("round"),
            "source_engine": rdata.get("engine"),
            "source_shot": shot_name,
            "source_file": os.path.relpath(src, HERE),
            "seed": shot.get("seed"),
            "prompt_id": shot.get("prompt_id"),
            "prompt": shot.get("prompt"),
            "negative": shot.get("negative"),
            "unapplied": shot.get("unapplied") or {},
            "sha256": _sha256(dest),
        })

    if missing:
        print(f"error: shot(s) not found in {args.round_json}: {missing}", file=sys.stderr)
        return 1
    if not entries:
        print("error: nothing picked", file=sys.stderr)
        return 2

    manifest_path = os.path.join(period, "manifest.json")
    manifest = {"period": os.path.basename(period),
                "note": args.note,
                "from": os.path.relpath(round_json, HERE),
                "entries": entries}
    if os.path.exists(manifest_path):
        old = json.load(open(manifest_path, encoding="utf-8"))
        old_entries = old.get("entries", [])
        if args.force:
            # --force = **重写这一期的成品清单**：只保留显式登记的 reference 条目，
            # 其余的旧成品/对照都算被本次调用取代。
            # （曾经这里是"按文件名去重后合并"，于是改名重做时会留下旧文件 + 旧条目，
            #   期目录里就出现了两份同源成品 —— 2026-10-05 修。）
            kept = [e for e in old_entries if e.get("role") == "reference"]
            new_names = {n["final"] for n in entries}
            for e in old_entries:
                if e.get("role") == "reference" or e["final"] in new_names:
                    continue
                stale = os.path.join(period, e.get("path", e["final"]))
                if os.path.exists(stale):
                    os.remove(stale)
                    print(f"  removed stale {e['final']}")
        else:
            kept = [e for e in old_entries
                    if e["final"] not in {n["final"] for n in entries}
                    and e.get("role") != "reference"]
        manifest["entries"] = kept + entries
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)

    for e in entries:
        origin = e.get("source_file") or e.get("note", "")
        extra = f"  seed {e['seed']}" if "seed" in e else ""
        print(f"  {e['role']:9s} {e['final']:28s} ← {origin}{extra}  {e['sha256'][:12]}")
    print(f"{len(entries)} entr(ies) → {os.path.relpath(manifest_path, HERE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
