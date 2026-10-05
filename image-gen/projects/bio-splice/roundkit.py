#!/usr/bin/env python3
"""轮次驱动的通用机械：跑轮、存档、分句换行。

**与子主题无关的东西都在这里**；每个子主题把自己的 prompt 与 ROUNDS 放在
`subjects/<子主题>/rounds.py`，由本模块按需加载。

为什么要分开：prompt 是子主题的（猫+鹰 与 龙·九似 的锚点毫无关系），
而"跑一轮 → 落档 → 打印逐字 prompt"的流程是项目级的。
第一个子主题时把两者写在一个文件里没关系，第二个子主题就必须拆——
否则每加一个子主题都要复制一遍分句换行与存档逻辑。

用法（入口在项目根 `run_round.py`）：
  python3 run_round.py 6
  python3 run_round.py --subject dragon-nines 1
  python3 run_round.py 6 --dry
  python3 run_round.py --subject dragon-nines --prompts
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_SCRIPTS = os.path.normpath(
    os.path.join(HERE, "..", "..", "skills", "text-to-image-comfyui", "scripts")
)
sys.path.insert(0, SKILL_SCRIPTS)
import comfyui_gen as cg  # noqa: E402
import comfyui_qwen as qw  # noqa: E402

SERVER = os.environ.get("COMFYUI_SERVER", cg.DEFAULT_SERVER)
WORKFLOW = os.path.normpath(
    os.path.join(HERE, "..", "..", "skills", "text-to-image-comfyui", "assets", "z-image-turbo-ui.json")
)
SUBJECTS_DIR = os.path.join(HERE, "subjects")


def load_subject(name: str):
    """按目录名加载子主题模块（目录名含连字符，不能用普通 import）。"""
    path = os.path.join(SUBJECTS_DIR, name, "rounds.py")
    if not os.path.exists(path):
        avail = sorted(d for d in os.listdir(SUBJECTS_DIR)
                       if os.path.exists(os.path.join(SUBJECTS_DIR, d, "rounds.py")))
        raise SystemExit(f"FATAL: unknown subject {name!r}; available: {available}")
    spec = importlib.util.spec_from_file_location("rounds_" + name.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Prompt 存档：分句换行，便于查阅与逐轮对照
# 还原规则见 docs/prompts-all.md 抬头；生成时逐条断言「还原 == 原文」。
# ---------------------------------------------------------------------------

ARCHIVE_WIDTH = 100
_ARCHIVE_SEP = re.compile(r"(。|！|？|\. |, |; |: |，|；|、|：)")
_ARCHIVE_STRONG = ("。", "！", "？", ". ")  # 句末：即使没到宽度也断行
_ARCHIVE_PUNCT = ("，", "；", "、", "：")  # 中文子句：断行处原文无空格


def _cols(s: str) -> int:
    """Display width, counting CJK/fullwidth characters as 2 columns."""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def _tight(c: str) -> bool:
    """True for a printable ASCII char (the only place a space can sit)."""
    return bool(c) and ord(c) < 128 and not c.isspace()


def _hard_wrap(line: str, width: int) -> list[str]:
    """Fallback split for a single clause that is itself wider than ``width``."""
    out: list[str] = []
    rest = line
    while _cols(rest) > width:
        space_cut = cjk_cut = -1
        for i, ch in enumerate(rest):
            if _cols(rest[:i + 1]) > width:
                break
            nxt = rest[i + 1] if i + 1 < len(rest) else ""
            if ch == " " and _tight(nxt):
                space_cut = i
            elif nxt and not _tight(ch) and not _tight(nxt):
                cjk_cut = i + 1
        if space_cut > 0:
            out.append(rest[:space_cut])
            rest = rest[space_cut + 1:]
        elif cjk_cut > 0:
            out.append(rest[:cjk_cut])
            rest = rest[cjk_cut:]
        else:
            return out + [rest]  # nothing safe to split on: leave it long
    if rest:
        out.append(rest)
    return out


def wrap_prompt(text: str, width: int = ARCHIVE_WIDTH) -> str:
    """Break a prompt string into clause-level lines for reading/comparison."""
    parts = _ARCHIVE_SEP.split(text)
    # split() with one capture group yields [text, sep, text, sep, ..., text];
    # pair each text with the separator that follows it.
    units = [(parts[i], parts[i + 1] if i + 1 < len(parts) else "")
             for i in range(0, len(parts), 2)]
    if not units[-1][0] and not units[-1][1]:
        units.pop()

    def breakable(i: int) -> bool:
        """May a line break be placed immediately after unit ``i``?"""
        if i < 0 or i >= len(units) - 1:
            return False
        sep = units[i][1]
        nxt = units[i + 1][0][:1]
        if sep in _ARCHIVE_PUNCT:
            return True  # 中文标点后断开是纯插入，与下一字符无关
        # 英文 ", " / ". " 断开 = 用换行替代那个空格，只有下一字符是 ASCII
        # 时才能被 unwrap_prompt 无歧义地还原。
        return _tight(nxt)

    lines: list[str] = []
    cur = ""
    for i, (txt, sep) in enumerate(units):
        if cur and breakable(i - 1) and (
            units[i - 1][1] in _ARCHIVE_STRONG or _cols(cur + txt + sep) > width
        ):
            lines.append(cur)
            cur = ""
        cur += txt + sep
    if cur:
        lines.append(cur)

    out: list[str] = []
    for line in lines:
        out.extend(_hard_wrap(line, width) if _cols(line) > width else [line])
    # Drop the space a break replaced; safe because breakable() guarantees the
    # next line starts with an ASCII char whenever the break ate a space.
    return "\n".join(
        ln[:-1] if ln.endswith(" ") and i + 1 < len(out) else ln
        for i, ln in enumerate(out)
    )


def unwrap_prompt(wrapped: str) -> str:
    """Inverse of :func:`wrap_prompt`: restore the byte-exact one-line string."""
    ls = wrapped.split("\n")
    text = ls[0]
    for prev, cur in zip(ls, ls[1:]):
        text += (" " if _tight(prev[-1:]) and _tight(cur[:1]) else "") + cur
    return text


def _wrap_checked(text: str, label: str) -> str:
    """Wrap ``text``, asserting the wrap is lossless (otherwise fail loudly)."""
    wrapped = wrap_prompt(text)
    if unwrap_prompt(wrapped) != text:
        raise SystemExit(f"FATAL: prompt wrapping is not lossless for {label}")
    return wrapped


def emit_prompt_archive(rounds: dict, subject, out_path: str) -> int:
    """Write every round's prompt text, wrapped for reading (losslessly)."""
    lines: list[str] = [
        "# 全部轮次原始 Prompt 存档",
        "",
        "> 本文件由 `python3 run_round.py --prompts` 自动生成，内容 = **实际提交给 ComfyUI 的字符串**。",
        "> 为便于查阅与逐轮对照，代码块内已按分句换行；**换行符不属于 prompt，仅排版**。",
        "> 还原规则：行尾是 ASCII 字符时，该换行等于一个空格；否则换行处原本没有字符。",
        "> `run_round.py` 的 `unwrap_prompt()` 就是这条规则，生成时会逐条断言「还原 == 原文」。",
        "> 逐字原文（单行）见 `run_round.py` 的常量（`python3 run_round.py <N> --dry` 可直接打印）",
        "> 与 `work/rN/round.json`；最终依据是服务器 `GET /history/{prompt_id}`。",
        "> 修改 prompt 请改 `subjects/<子主题>/rounds.py`，然后重新生成本文件。",
        "> 返回[子主题首页](../README.md) ｜ [项目首页](../../../README.md)",
        "",
        "## 记录在哪（三层）",
        "",
        "| 层 | 位置 | 内容 |",
        "|----|------|------|",
        "| 权威源 | `subjects/<子主题>/rounds.py` | 逐字 prompt（真正发出去的，单行） |",
        "| 可读文档 | 本文件 / `docs/rN.md` | 分句换行的 prompt 全文；每轮改动与自检 |",
        "| 机器记录 | `work/rN/round.json` | 文件名 / seed / prompt_id / 引擎 / 参数 / **prompt 原文** |",
        "| 服务器侧 | `GET /history/{prompt_id}` | ComfyUI 实际执行的完整图（最终依据） |",
        "",
    ]
    for n in sorted(rounds):
        spec = rounds[n]
        lines += [
            f"## R{n} · {spec['note']}",
            "",
            f"- 引擎：`{spec.get('engine', 'zimage')}`　尺寸：{spec['size'][0]}×{spec['size'][1]}　"
            f"steps：{spec['steps']}　共用 seed：{spec.get('seed')}",
            f"- 张数：{len(spec['shots'])}（每张独立请求）",
            "",
            "**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）",
            "",
            "```text",
            _wrap_checked(subject.ARCHIVE_LAYERS, f"R{n} shared layers"),
            "```",
            "",
        ]
        if spec.get("negative"):
            lines += ["**负向 prompt（全轮共用）**", "", "```text",
                      _wrap_checked(spec["negative"], f"R{n} negative"), "```", ""]
        for shot in spec["shots"]:
            over = []
            if "size" in shot:
                over.append(f"{shot['size'][0]}×{shot['size'][1]}")
            if "steps" in shot:
                over.append(f"steps {shot['steps']}")
            override = f"　（覆盖：{' · '.join(over)}）" if over else ""
            lines += [
                f"### {shot['name']}　seed {shot['seed']}{override}",
                "",
                "```text",
                _wrap_checked(shot["prompt"], f"R{n}/{shot['name']}"),
                "```",
                "",
            ]
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    shots = sum(len(rounds[n]["shots"]) for n in rounds)
    print(f"wrote {out_path}: {len(rounds)} round(s), {shots} prompt block(s)")
    return 0

def run_round(subject, subject_name: str, spec: dict, round_no: int, server: str) -> int:
    """跑一轮：逐镜头生成，最后把 round.json 写到 work/<子主题>/rN/。"""
    engine = spec.get("engine", "zimage")
    shots = spec["shots"]
    # 轮号是**子主题内**的编号，所以目录必须带子主题名，否则两个子主题的第 1 轮会撞车
    out_dir = os.path.join(HERE, "work", subject_name, f"r{round_no}")
    os.makedirs(out_dir, exist_ok=True)

    log = []
    for i, shot in enumerate(shots, start=1):
        prefix = f"{subject.PREFIX}-r{round_no}-{shot['name']}"
        # 每个镜头可以覆盖尺寸/步数/cfg/超时/负向，用来在一轮内做消融
        size = tuple(shot.get("size", spec["size"]))
        steps = shot.get("steps", spec["steps"])
        cfg = shot.get("cfg", spec.get("cfg", 3.0))
        timeout = shot.get("timeout", 2400)
        negative = shot.get("negative", spec.get("negative", ""))
        seed = shot["seed"]
        print(f"[{i}/{len(shots)}] {prefix} seed={seed} engine={engine} "
              f"{size[0]}x{size[1]} steps={steps}", flush=True)
        common = dict(server=server, prompt=shot["prompt"], width=size[0], height=size[1],
                      steps=steps, seed=seed, filename_prefix=prefix, out_dir=out_dir,
                      timeout=timeout, quiet=True)
        if engine == "qwen":
            result = qw.generate(negative=negative, cfg=cfg, **common)
        else:
            result = cg.generate(workflow=WORKFLOW, **common)
        log.append({
            "file": result["local_paths"][0] if result["local_paths"] else None,
            "seed": seed, "name": shot["name"], "engine": engine,
            "prompt_id": result["prompt_id"], "status": result["status"],
            "unapplied": result.get("unapplied") or {},
            "prompt": shot["prompt"], "negative": negative,
            "width": size[0], "height": size[1], "steps": steps,
        })
        print(f"      -> {log[-1]['file']}", flush=True)

    with open(os.path.join(out_dir, "round.json"), "w", encoding="utf-8") as fh:
        json.dump({"round": round_no, "subject": subject.PREFIX, "engine": engine,
                   "note": spec["note"], "shots": log}, fh, ensure_ascii=False, indent=2)
    print(json.dumps(log, ensure_ascii=False, indent=2))
    return 0 if all(item["file"] for item in log) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("round", type=int, nargs="?", help="轮号（用 --prompts 时可省略）")
    ap.add_argument("--subject", default="cat-eagle", help="子主题目录名（默认 cat-eagle）")
    ap.add_argument("--server", default=SERVER)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--prompts", nargs="?", const="", metavar="OUT.md",
                    help="把该子主题全部轮次的逐字 prompt 写成 Markdown"
                         "（默认 subjects/<子主题>/rounds/prompts-all.md）")
    args = ap.parse_args(argv)

    subject = load_subject(args.subject)
    rounds = subject.ROUNDS

    if args.prompts is not None:
        out = args.prompts or os.path.join("subjects", args.subject, "rounds", "prompts-all.md")
        return emit_prompt_archive(rounds, subject, out)
    if args.round is None:
        ap.error("a round number is required (or use --prompts)")
    if args.round not in rounds:
        ap.error(f"round {args.round} is not defined for {args.subject} "
                 f"(have: {sorted(rounds)})")

    spec = rounds[args.round]
    if args.dry:
        for shot in spec["shots"]:
            print(f"--- {shot['name']} (seed {shot['seed']}) ---\n{shot['prompt']}\n")
        return 0
    return run_round(subject, args.subject, spec, args.round, args.server)


if __name__ == "__main__":
    sys.exit(main())
