#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""山海经项目的轮次驱动：按 `subjects/<子主题>/rounds.py` 的定义出图。

为什么要有这个脚本
  九尾狐的 R6–R8 是临时敲命令跑的，结果**轮次记录缺了 R6–R8 的存档**，
  "哪一句 prompt 得到哪张图"只能从 manifest 反推。这个驱动把 prompt 定义放进仓库
  （`subjects/<子主题>/rounds.py`），跑之前能 `--dry` 看逐字 prompt，
  跑完产物与 requests.jsonl 落在 `work/shanhai-jing/<子主题>/rNN/`（**不进仓库**）。

用法
----
    python3 scripts/run_round.py --subject lu-shu 1 --dry          # 只打印逐字 prompt
    python3 scripts/run_round.py --subject lu-shu 1                # Z-Image-Turbo 出图
    python3 scripts/run_round.py --subject lu-shu 1 --engine seedream   # 同 prompt 走 Seedream（付费）
    python3 scripts/run_round.py --subject lu-shu 1 --sheet        # 出完拼一张速览图

出图引擎是仓库里的技能脚本，本驱动不重复实现 HTTP：
  * `z-image-turbo` → ../../.agents/skills/text-to-image-comfyui/scripts/comfyui_gen.py
  * `seedream`      → ../../.agents/skills/seedream-text-to-image/scripts/seedream_gen.py（付费，需凭据）
"""

import argparse
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(PROJ))
WORK = os.path.join(REPO, "work", "shanhai-jing")

T2I = os.path.join(REPO, ".agents", "skills", "text-to-image-comfyui", "scripts", "comfyui_gen.py")
SEEDREAM = os.path.join(REPO, ".agents", "skills", "seedream-text-to-image", "scripts", "seedream_gen.py")
CONTACT = os.path.join(REPO, ".agents", "skills", "image-tools", "scripts", "contact_sheet.py")


def load_rounds(subject: str):
    path = os.path.join(PROJ, "subjects", subject, "rounds.py")
    if not os.path.exists(path):
        raise SystemExit(f"找不到 {path}")
    spec = importlib.util.spec_from_file_location(f"rounds_{subject.replace('-', '_')}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def shots_of(mod, round_no: int) -> list:
    if round_no not in mod.ROUNDS:
        raise SystemExit(f"rounds.py 里没有 R{round_no}（现有：{sorted(mod.ROUNDS)}）")
    return mod.ROUNDS[round_no]["shots"]


def print_dry(mod, round_no: int) -> None:
    shots = shots_of(mod, round_no)
    print(f"# {mod.NAME_ZH}（{mod.SLUG}）R{round_no}  ·  {len(shots)} 张  ·  "
          f"画布 {mod.CANVAS['width']}x{mod.CANVAS['height']} / steps {mod.STEPS}")
    print(f"# 原文：{mod.PASSAGE}")
    for s in shots:
        print(f"\n--- {s['id']}  seed={s['seed']}  {s['width']}x{s['height']} steps={s['steps']}")
        print(s["prompt"])


def run_shot(mod, round_no: int, shot: dict, out_dir: str, engine: str,
             api_key_file: str | None, timeout: float) -> dict:
    prefix = f"shj-{mod.SLUG}-r{round_no}-{shot['id']}"
    if engine == "z-image-turbo":
        cmd = [sys.executable, T2I, "--prompt", shot["prompt"], "--seed", str(shot["seed"]),
               "--width", str(shot["width"]), "--height", str(shot["height"]),
               "--steps", str(shot["steps"]), "--filename-prefix", prefix,
               "--out-dir", out_dir]
    elif engine == "seedream":
        cmd = [sys.executable, SEEDREAM, "--prompt", shot["prompt"], "--seed", str(shot["seed"]),
               "--size", f"{shot['width']}x{shot['height']}", "--filename-prefix", prefix,
               "--out-dir", out_dir, "--timeout", str(int(timeout))]
        if api_key_file:
            cmd += ["--api-key-file", api_key_file]
    else:
        raise SystemExit(f"未知引擎 {engine}")
    print(f"-> {shot['id']}  seed={shot['seed']}", flush=True)
    res = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if res.returncode != 0:
        print(res.stdout[-2000:], file=sys.stderr)
        raise SystemExit(f"{shot['id']} 出图失败（退出码 {res.returncode}）")
    try:
        payload = json.loads(res.stdout[res.stdout.index("{"):])
    except (ValueError, json.JSONDecodeError):
        payload = {}
    files = payload.get("local_paths") or []
    print(f"   {'saved: ' + files[0] if files else res.stdout.strip().splitlines()[-1]}")
    return {"id": shot["id"], "seed": shot["seed"], "prompt": shot["prompt"],
            "prompt_id": payload.get("prompt_id"), "files": files}


def make_sheet(out_dir: str, round_no: int, subject: str) -> str:
    pngs = sorted(f for f in os.listdir(out_dir) if f.endswith(".png"))
    if not pngs:
        raise SystemExit("目录里没有 png，无法拼速览图")
    sheet = os.path.join(out_dir, f"sheet-r{round_no:02d}.jpg")
    cmd = [sys.executable, CONTACT, "-o", sheet, "--cols", "3", "--cell", "420",
           "--label-mode", "name", "--title", f"{subject} R{round_no}"] + \
        [os.path.join(out_dir, f) for f in pngs]
    subprocess.run(cmd, check=True)
    return sheet


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="山海经轮次驱动")
    ap.add_argument("round", type=int, help="轮次号")
    ap.add_argument("--subject", default="jiu-wei-hu")
    ap.add_argument("--engine", default="z-image-turbo",
                    choices=["z-image-turbo", "seedream"])
    ap.add_argument("--dry", action="store_true", help="只打印逐字 prompt，不出图")
    ap.add_argument("--sheet", action="store_true", help="跑完拼速览图")
    ap.add_argument("--only", help="只跑指定 shot id（逗号分隔）")
    ap.add_argument("--api-key-file", help="seedream 引擎的凭据文件")
    ap.add_argument("--timeout", type=float, default=900.0)
    args = ap.parse_args(argv)

    mod = load_rounds(args.subject)
    if args.dry:
        print_dry(mod, args.round)
        return 0

    shots = shots_of(mod, args.round)
    if args.only:
        want = {x.strip() for x in args.only.split(",") if x.strip()}
        shots = [s for s in shots if s["id"] in want]
        if not shots:
            raise SystemExit(f"--only 没匹配到任何 shot：{sorted(want)}")

    out_dir = os.path.join(WORK, args.subject, f"r{args.round:02d}")
    os.makedirs(out_dir, exist_ok=True)
    done = []
    for shot in shots:
        done.append(run_shot(mod, args.round, shot, out_dir, args.engine,
                             args.api_key_file, args.timeout))
    ledger = os.path.join(out_dir, f"round-r{args.round:02d}-{args.engine}.json")
    with open(ledger, "w", encoding="utf-8") as fh:
        json.dump({"subject": args.subject, "round": args.round, "engine": args.engine,
                   "canvas": mod.CANVAS, "steps": mod.STEPS, "shots": done},
                  fh, ensure_ascii=False, indent=1)
    print(f"\n{len(done)} 张已出图 → {os.path.relpath(out_dir)}")
    print(f"轮次存档       → {os.path.relpath(ledger)}")
    if args.sheet:
        print(f"速览图         → {os.path.relpath(make_sheet(out_dir, args.round, args.subject))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
