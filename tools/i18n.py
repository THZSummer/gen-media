#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双语文档流水线：给每个中文 `X.md` 配一份英文 `X.en.md`。

约定（本仓库的 i18n 规范）：
  * 中文版是 `X.md`（默认），英文版是同名 `X.en.md`
  * 两份文件顶部各有一行语言切换：中文版 `> 🌐 语言：**中文** ｜ [English](X.en.md)`
  * 英文版内部的相对链接指向 `.en.md`；目标没有英文版时仍指向中文版
  * 排除 `.agents/skills/**` 与 `.agents/skills/**`（技能文档只留中文）

用法：
    python3 tools/i18n.py status            # 覆盖率报告（哪些缺英文版）
    python3 tools/i18n.py switch            # 写入/更新两侧的语言切换行（幂等）
    python3 tools/i18n.py links             # 把英文版里的相对链接改指 .en.md
    python3 tools/i18n.py check             # 体检：缺件 / 未翻译 / 断链
    python3 tools/i18n.py check --strict    # 有任一问题即退出码 1

判定「未翻译」用的是相对指标：英文版的中日韩字符数若超过中文版的 50%，
基本可以断定是原文照抄（阈值可用 --ratio 调）。
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN_SUFFIX = ".en.md"
# 技能文档只写中文：.agents/skills 是仓库技能根（含 dev-guide 与 5 个执行技能）
SKIP_PREFIXES = (".agents/skills/",)

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3000-\u303f\uff01-\uff60]")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
SWITCH_RE = re.compile(r"^>\s*🌐")
H1_RE = re.compile(r"^#\s+\S")
FRONTMATTER_RE = re.compile(r"^---\s*$")

# 「本地保留、不入库」的中间产物：文档里指向它们是预期行为，不算断链
LOCAL_ARTIFACT_RE = re.compile(r"(^|/)(work|out/r\d+)(/|$)")


def is_local_artifact(path: str) -> bool:
    return bool(LOCAL_ARTIFACT_RE.search(path.replace("\\", "/")))


def in_scope(rel: str) -> bool:
    if not rel.endswith(".md"):
        return False
    if rel.endswith(EN_SUFFIX):
        return False
    if rel.startswith(SKIP_PREFIXES):
        return False
    return True


def walk_md() -> list[str]:
    out = []
    for base, dirs, files in os.walk(ROOT):
        # work/ 与 .verify/ 都是 gitignore 的中间产物，不是仓库文档，必须排除
        dirs[:] = [d for d in dirs
                   if d not in (".git", "node_modules", "__pycache__", "work", ".verify")]
        for f in files:
            rel = os.path.relpath(os.path.join(base, f), ROOT)
            if in_scope(rel):
                out.append(rel)
    return sorted(out)


def zh_of(rel: str) -> str:
    """英文版路径 → 对应的中文版路径（README.en.md → README.md）"""
    if rel.endswith(EN_SUFFIX):
        return rel[: -len(EN_SUFFIX)] + ".md"
    return rel


def en_of(rel: str) -> str:
    return rel if rel.endswith(EN_SUFFIX) else rel[: -len(".md")] + EN_SUFFIX


def read(rel: str) -> str:
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def write(rel: str, text: str) -> None:
    with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as fh:
        fh.write(text)


def cjk_count(text: str) -> int:
    return len(CJK_RE.findall(text))


def cjk_outside_fence(text: str) -> int:
    """只数围栏代码块之外的汉字。

    判「是否真的翻译了」必须用这个口径：prompt 存档之类的文件，正文大段中文位于代码块内
    （prompt 原文 = 内容，按规范逐字保留），用全文口径会把它们误判成「未翻译」。
    """
    total = 0
    in_fence = False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            total += len(CJK_RE.findall(line))
    return total


# ── switch：语言切换行 ──────────────────────────────────────────────────────
def switch_line(rel: str, english: bool) -> str:
    base = os.path.basename(rel)
    if english:
        zh = os.path.basename(zh_of(rel))
        return f"> 🌐 Language: **English** | [中文]({zh})"
    return f"> 🌐 语言：**中文** ｜ [English]({base[: -len('.md')]}{EN_SUFFIX})"


def apply_switch(rel: str, english: bool) -> bool:
    """写入或更新切换行；返回是否发生变化。"""
    path = os.path.join(ROOT, rel)
    if not os.path.isfile(path):
        return False
    text = read(rel)
    lines = text.split("\n")
    want = switch_line(rel, english)

    # 已有则原位替换
    for i, line in enumerate(lines[:25]):
        if SWITCH_RE.match(line):
            if line == want:
                return False
            lines[i] = want
            write(rel, "\n".join(lines))
            return True

    # 没有则插到 YAML frontmatter 之后、H1 之后（都没有就放最前）
    insert_at = 0
    if lines and FRONTMATTER_RE.match(lines[0]):
        for i in range(1, len(lines)):
            if FRONTMATTER_RE.match(lines[i]):
                insert_at = i + 1
                break
    for i in range(insert_at, min(len(lines), insert_at + 40)):
        if H1_RE.match(lines[i]):
            insert_at = i + 1
            break
    block = ["", want]
    lines[insert_at:insert_at] = block
    write(rel, "\n".join(lines))
    return True


# ── links：英文版内部链接指向 .en.md ────────────────────────────────────────
def remap_links(rel: str) -> int:
    text = read(rel)
    base_dir = os.path.dirname(rel)
    changed = 0

    def repl(m: re.Match) -> str:
        nonlocal changed
        target = m.group(1)
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        path, _, anchor = target.partition("#")
        if not path or path.endswith(EN_SUFFIX):
            return m.group(0)
        candidate = os.path.normpath(os.path.join(base_dir, path))
        if not candidate.endswith(".md"):
            return m.group(0)
        # 语言切换行指向本文件的中文对应版，不能重定向（否则会指向自己）
        if candidate == os.path.normpath(zh_of(rel)):
            return m.group(0)
        if os.path.isfile(os.path.join(ROOT, en_of(candidate))):
            changed += 1
            new = en_of(path)
            return "](" + new + (("#" + anchor) if anchor else "") + ")"
        return m.group(0)

    new_text = LINK_RE.sub(repl, text)
    if changed:
        write(rel, new_text)
    return changed


# ── 命令 ────────────────────────────────────────────────────────────────────
def cmd_status(_args) -> int:
    zh = walk_md()
    have = [r for r in zh if os.path.isfile(os.path.join(ROOT, en_of(r)))]
    missing = [r for r in zh if r not in have]
    by_dir = Counter(os.path.dirname(r) or "." for r in missing)

    print(f"范围内中文文档：{len(zh)}")
    print(f"已有英文版：    {len(have)}")
    print(f"缺英文版：      {len(missing)}")
    if missing:
        print("\n缺件最多的目录：")
        for d, n in by_dir.most_common(12):
            print(f"  {n:4d}  {d}")
    return 0


def cmd_switch(_args) -> int:
    zh = walk_md()
    n = 0
    for rel in zh:
        if os.path.isfile(os.path.join(ROOT, en_of(rel))):
            n += apply_switch(rel, english=False)
            n += apply_switch(en_of(rel), english=True)
    print(f"语言切换行：更新 {n} 处")
    return 0


def cmd_links(_args) -> int:
    zh = walk_md()
    total = files = 0
    for rel in zh:
        en = en_of(rel)
        if os.path.isfile(os.path.join(ROOT, en)):
            c = remap_links(en)
            if c:
                files += 1
                total += c
    print(f"英文版链接重定向：{files} 个文件，{total} 条链接")
    return 0


def cmd_check(args) -> int:
    zh = walk_md()
    problems = []

    missing = [r for r in zh if not os.path.isfile(os.path.join(ROOT, en_of(r)))]
    for r in missing:
        problems.append(("缺英文版", r, ""))

    # 未翻译检测（相对指标，只数围栏块外的汉字）：英文版的正文汉字数 / 中文版正文汉字数
    untranslated = []
    for rel in zh:
        en = en_of(rel)
        if not os.path.isfile(os.path.join(ROOT, en)):
            continue
        z = cjk_outside_fence(read(rel))
        e = cjk_outside_fence(read(en))
        if z >= 40 and e / max(z, 1) > args.ratio:
            untranslated.append((rel, z, e, e / max(z, 1)))
    for rel, z, e, ratio in sorted(untranslated, key=lambda x: -x[3]):
        problems.append(("疑似未翻译", rel, f"中文 {z} 字 / 英文版仍含 {e} 字（{ratio:.0%}）"))

    # 英文版里的相对链接是否都指得到
    broken = []
    local_only = 0
    for rel in zh:
        en = en_of(rel)
        if not os.path.isfile(os.path.join(ROOT, en)):
            continue
        base_dir = os.path.dirname(en)
        for m in LINK_RE.finditer(read(en)):
            t = m.group(1)
            if t.startswith(("http://", "https://", "mailto:", "#")):
                continue
            p = t.split("#")[0]
            if not p:
                continue
            if is_local_artifact(p):
                # 指向 work/ 或 out/r*/ 这类「本地保留、不入库」的中间产物，属预期
                local_only += 1
                continue
            # 指向被排除目录（skills）的中文文件是允许的
            if not os.path.exists(os.path.join(ROOT, os.path.normpath(os.path.join(base_dir, p)))):
                broken.append((en, t))
    for rel, t in broken[:20]:
        problems.append(("英文版断链", rel, t))

    print(f"范围内中文文档 {len(zh)}；缺英文版 {len(missing)}；疑似未翻译 {len(untranslated)}；"
          f"英文版断链 {len(broken)}（另有 {local_only} 条指向本地中间产物，符合预期）")
    for kind, rel, extra in problems[:40]:
        print(f"  [{kind}] {rel} {extra}")
    if len(problems) > 40:
        print(f"  … 另有 {len(problems) - 40} 条")
    if not problems:
        print("✅ 全部通过")
    return 1 if (problems and args.strict) else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="双语文档流水线")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sub.add_parser("switch").set_defaults(func=cmd_switch)
    sub.add_parser("links").set_defaults(func=cmd_links)
    p = sub.add_parser("check")
    p.add_argument("--strict", action="store_true", help="有问题时退出码 1")
    p.add_argument("--ratio", type=float, default=0.5, help="未翻译判定阈值（默认 0.5）")
    p.set_defaults(func=cmd_check)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
