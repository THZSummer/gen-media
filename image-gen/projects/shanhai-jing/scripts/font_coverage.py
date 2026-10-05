#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查一个字库到底覆盖哪些字符（直接解析 TTF 的 cmap，不依赖 fontTools）。

为什么需要它
------------
印章要用**真篆字**（见 PLAN.md「印章」一节）。但开源篆体字库往往只映射
Unicode 新增的「小篆区」，**未必覆盖常规汉字码位**——渲染出来可能是一堆
替代方块，而肉眼在一张图里很难分辨"这是篆书"还是"这是缺字方块"。

所以把"字库能不能打出这几个字"变成一条可证伪的机械检查。

用法
----
    python3 scripts/font_coverage.py --font assets/fonts/LXGWSeal-Regular.ttf --text 九尾狐
    python3 scripts/font_coverage.py --font F.ttf --text 青丘 --json
退出码：0 = 全部覆盖；1 = 有缺字（缺哪些会逐字列出）
"""

import argparse
import json
import struct
import sys


def sfnt_base(data: bytes) -> int:
    """返回第一个 sfnt 表的起始偏移。TTC（.ttc 集合）要先跳过 ttcf 头。

    注意：TTC 的**表目录**偏移相对 sfnt 起点，但目录里记录的表偏移是
    相对**文件开头**的绝对偏移，所以只有表目录位置需要这个 base。
    """
    if data[:4] == b"ttcf":
        n = struct.unpack_from(">I", data, 8)[0]
        if n < 1:
            raise SystemExit("TTC 集合里没有字体")
        return struct.unpack_from(">I", data, 12)[0]
    return 0


def read_tables(data: bytes) -> dict:
    base = sfnt_base(data)
    num = struct.unpack_from(">H", data, base + 4)[0]
    tables = {}
    for i in range(num):
        off = base + 12 + i * 16
        tag = data[off:off + 4].decode("latin-1")
        toff, tlen = struct.unpack_from(">II", data, off + 8)
        tables[tag] = (toff, tlen)
    return tables


def parse_format4(data: bytes, off: int) -> set:
    seg = struct.unpack_from(">H", data, off + 6)[0] // 2
    end_off = off + 14
    ends = struct.unpack_from(">%dH" % seg, data, end_off)
    start_off = end_off + seg * 2 + 2
    starts = struct.unpack_from(">%dH" % seg, data, start_off)
    delta_off = start_off + seg * 2
    deltas = struct.unpack_from(">%dh" % seg, data, delta_off)
    range_off = delta_off + seg * 2
    ranges = struct.unpack_from(">%dH" % seg, data, range_off)
    out = set()
    for i in range(seg):
        s, e = starts[i], ends[i]
        if s == 0xFFFF or e < s:
            continue
        for c in range(s, e + 1):
            if ranges[i] == 0:
                g = (c + deltas[i]) & 0xFFFF
            else:
                gi = range_off + i * 2 + ranges[i] + (c - s) * 2
                if gi + 2 > len(data):
                    continue
                g = struct.unpack_from(">H", data, gi)[0]
                if g:
                    g = (g + deltas[i]) & 0xFFFF
            if g:
                out.add(c)
    return out


def parse_format12(data: bytes, off: int) -> set:
    n = struct.unpack_from(">I", data, off + 12)[0]
    out = set()
    for i in range(n):
        p = off + 16 + i * 12
        s, e, _g = struct.unpack_from(">III", data, p)
        if e - s > 0x20000:          # 防御异常巨段
            continue
        out.update(range(s, e + 1))
    return out


def font_charset(path: str) -> set:
    """返回该字库 cmap 覆盖的全部码位集合（合并所有子表）。"""
    with open(path, "rb") as fh:
        data = fh.read()
    tables = read_tables(data)
    if "cmap" not in tables:
        raise SystemExit(f"不是有效 TTF：缺少 cmap 表（{path}）")
    coff, _clen = tables["cmap"]
    n = struct.unpack_from(">H", data, coff + 2)[0]
    charset = set()
    for i in range(n):
        p = coff + 4 + i * 8
        _plat, _enc, sub = struct.unpack_from(">HHI", data, p)
        soff = coff + sub
        fmt = struct.unpack_from(">H", data, soff)[0]
        try:
            if fmt == 4:
                charset |= parse_format4(data, soff)
            elif fmt == 12:
                charset |= parse_format12(data, soff)
        except struct.error:
            continue
    return charset


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="检查字库对指定文本的覆盖情况（解析 cmap）")
    ap.add_argument("--font", required=True)
    ap.add_argument("--text", required=True, help="要检查的文本")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    cs = font_charset(args.font)
    missing = [ch for ch in args.text if ord(ch) not in cs]
    ok = not missing

    if args.json:
        print(json.dumps({"font": args.font, "text": args.text,
                          "charset_size": len(cs),
                          "missing": missing, "ok": ok}, ensure_ascii=False))
    else:
        print(f"font          : {args.font}")
        print(f"charset_size  : {len(cs)} 个码位")
        print(f"text          : {args.text}")
        print(f"missing       : {''.join(missing) if missing else '（无）'}")
        for ch in args.text:
            mark = "✅" if ord(ch) in cs else "❌"
            print(f"  {mark} {ch}  U+{ord(ch):04X}")
        print("OK: 全部覆盖" if ok else f"FAIL: 缺 {len(missing)} 字，印章不能用这个字库")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
