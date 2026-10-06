#!/usr/bin/env python3
"""Seedream 图片编辑：把「底图（+ 可选标注）+ 提示词」变成 /prompt API 图。

和兄弟技能 `seedream-text-to-image` 用的是同一个付费 partner 节点
(`ByteDanceSeedreamNodeV3`)，区别只在**给不给参考图**。参考图接进来要处理四件事，
每一件都是真机实测出来的（证据见 references/api-node.md）：

  1. 参考图走 `model.images.image_1` / `image_2` …：这是 `COMFY_AUTOGROW_V3` 采集式
     输入，API 输入名带点，`image_2` 也真的被服务器接受（免费探针：HTTP 200）；
  2. 导出的 UI 图里有 `MarkdownNote`（前端专有节点）——原样提交会被 /prompt 判
     `missing_node_type`（实测 400），所以先过 `prune_ui_only()`；
  3. `Painter` 是"把 RGBA 标注层按 alpha 合成到底图"的**服务器**节点（实测：
     合成结果 = 底图 + 标注框，MASK 输出 = 标注层 alpha）——`--annotate` 时保留它，
     不标注时整条标注支路删掉；
  4. 有参考图时 `thinking` **不能关**：服务器会直接报
     `'thinking' can only be disabled for text-to-image; enable it when using
     reference images.`——本地就先拦住，省掉一次付费请求。

Importable:
    import _shared; _shared.ensure()
    from seedream_edit_graph import build_edit_graph, auto_size, image_size
"""
from __future__ import annotations

import math
import os
from typing import Any

import _shared

_shared.ensure()
import seedream_api as A  # noqa: E402

# 采集式参考图在 API 图里的键名模板
REF_KEY = "model.images.image_{}"
# 无头不需要的界面节点：预览图只是给人看的，去掉少存一张临时图
HEADLESS_DROP = ("PreviewImage",)
PAINTER_CLASS = "Painter"
LOAD_CLASS = "LoadImage"
NEW_ID_BASE = 1000


# --------------------------------------------------------------------------
# 图片尺寸（不依赖 Pillow：PNG 读 IHDR，JPEG 扫 SOF 段）
# --------------------------------------------------------------------------
def png_size(path: str) -> tuple[int, int]:
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise A.InvalidValueError(f"{path} 不是 PNG（magic 不对）")
    if head[12:16] != b"IHDR":
        raise A.InvalidValueError(f"{path} 的 PNG 第一块不是 IHDR，读不出尺寸")
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


def jpeg_size(path: str) -> tuple[int, int]:
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:2] != b"\xff\xd8":
        raise A.InvalidValueError(f"{path} 不是 JPEG（magic 不对）")
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seglen = int.from_bytes(data[i + 2:i + 4], "big")
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            height = int.from_bytes(data[i + 5:i + 7], "big")
            width = int.from_bytes(data[i + 7:i + 9], "big")
            return width, height
        i += 2 + seglen
    raise A.InvalidValueError(f"{path} 里找不到 JPEG 的 SOF 段，读不出尺寸")


def image_size(path: str) -> tuple[int, int]:
    """(宽, 高)。按扩展名/魔数选 PNG 或 JPEG；--size auto 需要它。"""
    if not os.path.isfile(path):
        raise A.InvalidValueError(f"找不到图片：{path}")
    ext = os.path.splitext(path)[1].lower()
    if ext == ".png":
        return png_size(path)
    if ext in (".jpg", ".jpeg"):
        return jpeg_size(path)
    with open(path, "rb") as fh:
        magic = fh.read(8)
    if magic.startswith(b"\x89PNG"):
        return png_size(path)
    if magic.startswith(b"\xff\xd8"):
        return jpeg_size(path)
    raise A.InvalidValueError(
        f"不认得的图片格式（{ext or '无扩展名'}）：{path}；"
        "--size auto 只支持 PNG / JPEG，其它格式请显式给 --size"
    )


# --------------------------------------------------------------------------
# 尺寸：按底图比例挑预设
# --------------------------------------------------------------------------
def preset_tier(preset: str) -> str:
    """`(2K) 2048x2048 (1:1)` -> `2K`；取不到就返回空串。"""
    head = preset.strip()
    if head.startswith("(") and ")" in head:
        return head[1:head.index(")")].strip()
    return ""


def preset_aspect(preset: str) -> float | None:
    for token in preset.replace("(", " ").replace(")", " ").split():
        if "x" in token.lower():
            try:
                width, height = (int(v) for v in token.lower().split("x", 1))
            except ValueError:
                continue
            return width / height if height else None
    return None


def auto_size(info: dict, model: str, width: int, height: int,
              tier: str | None = None) -> dict[str, Any]:
    """按底图宽高比挑一个预设：同比例里取**像素最小**的一档（便宜、够用）。

    Seedream 出图的尺寸由 `size_preset` 决定，**不会**自动跟随底图；编辑时底图比例
    跑掉了最容易被看出来，所以 `--size auto`（默认）走这里。
    `tier` 不给就取该模型最小的一档（pro/flash/4.0 = 1K；lite/4.5 = 2K）。
    """
    presets = A.size_presets(info, model)
    if not presets:
        raise A.InvalidValueError(f"{model} 没有尺寸预设")
    want = width / height if height else 1.0
    by_tier: dict[str, list[str]] = {}
    for preset in presets:
        by_tier.setdefault(preset_tier(preset) or "?", []).append(preset)
    tiers = [t for t in by_tier if t != "?"]
    if tier is None:
        tier = (min(tiers, key=lambda t: min(A._preset_pixels(p) for p in by_tier[t]))
                if tiers else "?")
    elif tier not in by_tier:
        raise A.InvalidValueError(
            f"{model} 没有 {tier} 档；可选：" + "、".join(sorted(by_tier)))
    pool = by_tier.get(tier) or presets
    best = min(pool, key=lambda p: (abs(math.log((preset_aspect(p) or want) / want)),
                                    A._preset_pixels(p)))
    # 注意：返回值里的 `preset` 是**预设原文**，直接当 `--size` 传下去即可
    return {"preset": best, "tier": tier, "ref_size": [width, height],
            "want_aspect": round(want, 4), "preset_aspect": round(preset_aspect(best) or 0, 4)}


# --------------------------------------------------------------------------
# 图的改造
# --------------------------------------------------------------------------
def _next_id(api: dict) -> str:
    numeric = [int(nid) for nid in api if str(nid).lstrip("-").isdigit()]
    return str(max([NEW_ID_BASE] + numeric) + 1)


def _drop_classes(api: dict, classes: tuple[str, ...]) -> list[dict]:
    gone = [{"id": nid, "class": api[nid].get("class_type")}
            for nid, node in api.items() if node.get("class_type") in classes]
    for item in gone:
        api.pop(item["id"], None)
    return gone


def _cascade(api: dict, removed: list[str]) -> list[str]:
    """把"输入指向已删节点"的节点也删掉（删 Painter 会带走它的下游）。

    只返回**额外**被带走的节点 id；传进来的那一批不算。
    """
    gone = {str(n) for n in removed}
    extra: list[str] = []
    while True:
        more = [nid for nid, node in api.items()
                if any(isinstance(v, list) and v and str(v[0]) in gone
                       for v in node["inputs"].values())]
        if not more:
            break
        for nid in more:
            api.pop(nid, None)
            gone.add(nid)
            extra.append(nid)
    return extra


def _load_nodes(api: dict) -> list[str]:
    return sorted((nid for nid, node in api.items() if node.get("class_type") == LOAD_CLASS),
                  key=lambda n: int(n) if str(n).isdigit() else 1 << 30)


def _add_load(api: dict, name: str) -> str:
    nid = _next_id(api)
    api[nid] = {"class_type": LOAD_CLASS,
                "inputs": {"image": name, "upload": "image"},
                "_meta": {"title": LOAD_CLASS}}
    return nid


def build_edit_graph(
    ui: dict,
    refs: list[str],
    annotate: str | None = None,
    *,
    base_size: tuple[int, int] | None = None,
    known_classes: set[str] | None = None,
    drop_preview: bool = True,
) -> tuple[dict, str | None, dict]:
    """UI 工作流 + 已上传的参考图名 -> (API 图, 保存节点 id, 说明)。

    `refs`     : 服务器 input 目录里的文件名（已上传），第 1 张是底图
    `annotate` : 标注层（RGBA PNG，alpha 就是笔迹）的文件名；给了才保留 Painter
    `base_size`: 底图像素尺寸，用来定 Painter 画布；不给就用工作流里的值
    `known_classes`: 真机 /object_info 的类名集合；给了就按它判"服务器上有没有"
    """
    if not refs:
        raise A.InvalidValueError(
            "图片编辑至少要给一张参考图（--image）；纯文生图请用姊妹技能 "
            "seedream-text-to-image 的 seedream_gen.py")

    api, save_id = A.build_api_graph(ui)
    dropped: list[dict] = []

    api, ui_nodes = A.prune_ui_only(api, known_classes=known_classes)
    dropped += [{"id": d.get("_dropped_id"), "class": d.get("_dropped_class"),
                 "why": "前端专有节点（服务器上没有）"} for d in ui_nodes]

    seed_id = A.find_node(api, A.SEEDREAM_CLASS)
    if seed_id is None:
        raise KeyError(f"API 图里没有 {A.SEEDREAM_CLASS}")

    removed: list[str] = []
    if drop_preview:
        preview = _drop_classes(api, HEADLESS_DROP)
        dropped += [{**d, "why": "无头不需要的预览节点"} for d in preview]
        removed += [d["id"] for d in preview]

    # 参考图：第 1 张复用工作流里的 LoadImage，其余按需新建
    loads = _load_nodes(api)
    if not loads:
        loads = [_add_load(api, refs[0])]
    api[loads[0]]["inputs"]["image"] = refs[0]
    ref_ids = [loads[0]]
    for extra in refs[1:]:
        ref_ids.append(_add_load(api, extra))

    # 标注支路
    painter_id = A.find_node(api, PAINTER_CLASS)
    if annotate:
        size = base_size
        if size is None and painter_id is not None:
            size = (api[painter_id]["inputs"].get("width", 1024),
                    api[painter_id]["inputs"].get("height", 1024))
        width, height = size or (1024, 1024)
        if painter_id is None:
            painter_id = _next_id(api)
            api[painter_id] = {"class_type": PAINTER_CLASS,
                               "inputs": {"bg_color": "#000000"},
                               "_meta": {"title": PAINTER_CLASS}}
        api[painter_id]["inputs"].update({
            "mask": annotate, "width": int(width), "height": int(height),
            "bg_color": api[painter_id]["inputs"].get("bg_color") or "#000000",
            "image": [ref_ids[0], 0],
        })
        api[seed_id]["inputs"][REF_KEY.format(1)] = [painter_id, 0]
    else:
        if painter_id is not None:
            api.pop(painter_id, None)
            removed.append(painter_id)
            dropped.append({"id": painter_id, "class": PAINTER_CLASS,
                            "why": "没给 --annotate：标注支路整条删掉"})
        api[seed_id]["inputs"][REF_KEY.format(1)] = [ref_ids[0], 0]

    for index, nid in enumerate(ref_ids[1:], start=2):
        api[seed_id]["inputs"][REF_KEY.format(index)] = [nid, 0]

    for nid in _cascade(api, removed):
        dropped.append({"id": nid, "class": "?", "why": "上游被删，连线断了，级联删除"})

    # 兜底：任何指向不存在节点的输入都清掉（宁可早报错，不要发一张坏图出去）
    ids = set(api)
    problems = [f"节点 {nid} 的 {name} 指向不存在的节点 {v[0]}"
                for nid, node in api.items() for name, v in node["inputs"].items()
                if isinstance(v, list) and v and str(v[0]) not in ids]
    if problems:
        raise RuntimeError("接线没接干净：\n  - " + "\n  - ".join(problems))

    meta = {
        "seed_node": seed_id,
        "save_node": save_id,
        "ref_nodes": ref_ids,
        "annotate_node": painter_id if annotate else None,
        "composite_node": painter_id if annotate else None,
        "dropped": dropped,
        "ref_keys": [REF_KEY.format(i) for i in range(1, len(ref_ids) + 1)],
    }
    return api, save_id, meta


def default_model(ui: dict) -> str | None:
    """工作流里 Seedream 节点上写的模型键（不建图，直接读 UI 的命名 widget）。"""
    for node in ui.get("nodes") or []:
        if node.get("type") == A.SEEDREAM_CLASS:
            named = node.get("widgets_values_named") or {}
            return named.get("model")
    return None


def max_refs(info: dict, model: str) -> int | None:
    """该模型能收几张参考图（从 `model.images` 的 tooltip "Up to N images." 里读）。"""
    import re
    subs = A.dynamic_sub_inputs(info, A.SEEDREAM_CLASS, "model", model)
    spec = subs.get("model.images")
    if not spec:
        return None
    tooltip = A._spec_opts(spec).get("tooltip") or ""
    hit = re.search(r"Up to (\d+) images", tooltip)
    return int(hit.group(1)) if hit else None


def supports_thinking(info: dict, model: str) -> bool:
    return "model.thinking" in A.dynamic_sub_inputs(info, A.SEEDREAM_CLASS, "model", model)
