#!/usr/bin/env python3
"""一张图 → 8 个不同角度（Qwen-Image-Edit 2511 + Multiple-Angles LoRA，本地模型）。

把 ComfyUI 官方模板 "1 Click Multiple Character Angles" 跑成可脚本化的管线：
上传一张参考图 → 展开**嵌套子图**（父图里 8 个 "Image Edit (Qwen-Image 2511 with
LoRA)" 实例，各带一句角度提示词）→ 提交 → 轮询 /history → 把 8 张图按**角度名**
落盘并留档。

用法::

    python3 comfyui_angles.py --list                 # 看 8 个角度、模型、快/慢档（离线）
    python3 comfyui_angles.py --check                # 真机：5 个模型 + 12 个节点类在不在
    python3 comfyui_angles.py --image ref.png --plan # 免费：只验证图与接线，不提交、不上传
    python3 comfyui_angles.py --image ref.png --only 45_right,90_right   # 只出 2 个角度（省时间）
    python3 comfyui_angles.py --image ref.png --out-dir out/            # 全 8 个角度

**成本**：本机免费、可重复跑，但**慢**——用户实测 1080p 输入、8 张不同角度 ≈ **5 分钟**
（快档 4 步）；只出 2 个角度约 1 分半。脚本在提交前打印 ETA。

退出码：0 正常 / 1 没有产物 / 2 参数问题 / 3 服务器不可达 / 4 缺节点 / 5 超时。
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from typing import Any

import _shared

_shared.ensure()
import comfyui_convert as C  # noqa: E402
import comfyui_gen as G  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_WORKFLOW = os.path.normpath(
    os.path.join(HERE, "..", "assets", "qwen-2511-batch-angles-ui.json"))
DEFAULT_SERVER = os.environ.get("COMFYUI_SERVER", G.DEFAULT_SERVER)

ENGINE = "qwen-2511-multi-angle"
PARENT_NAME = "Qwen-Image 2511: Batch Angle Generation"
EDIT_NAME = "Image Edit (Qwen-Image 2511 with LoRA)"
SAVE_CLASS = "SaveImage"
LOAD_CLASS = "LoadImage"

# 实测成本（2026-10-12 真机）：8 张 1024×1024 / 快档 4 步 = 285.8 s → 单张 35.7 s
SECONDS_PER_ANGLE_FAST = 36.0
SECONDS_PER_ANGLE_SLOW = 576.0  # 慢档实测（2026-10-12 真机）：单张 576.5 s（服务端执行窗口 572.2 s）

REQUIRED_MODELS: tuple[tuple[str, str], ...] = (
    ("diffusion_models", "qwen_image_edit_2511_bf16.safetensors"),
    ("text_encoders", "qwen_2.5_vl_7b_fp8_scaled.safetensors"),
    ("vae", "qwen_image_vae.safetensors"),
    ("loras", "Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors"),
    ("loras", "qwen-image-edit-2511-multiple-angles-lora.safetensors"),
)

REQUIRED_NODES: tuple[str, ...] = (
    "UNETLoader", "CLIPLoader", "VAELoader", "LoraLoaderModelOnly", "KSampler",
    "SaveImage", "LoadImage", "TextEncodeQwenImageEditPlus", "FluxKontextImageScale",
    "FluxKontextMultiReferenceLatentMethod", "ModelSamplingAuraFlow", "CFGNorm",
    "ComfySwitchNode",
)

# 父图实例上可覆盖的下拉/开关（API 名 → 说明）
MODEL_INTERFACES = ("unet_name", "clip_name", "vae_name", "lora_name", "lora_name_1")

EXIT_OK, EXIT_NO_OUTPUT, EXIT_BAD_PARAMS, EXIT_UNREACHABLE, EXIT_NO_NODE, EXIT_TIMEOUT = 0, 1, 2, 3, 4, 5


# --------------------------------------------------------------------------
# 工作流解剖：角度表
# --------------------------------------------------------------------------
def parent_instance(ui: dict) -> dict:
    """顶层那个父图实例（"Batch Angle Generation"）。"""
    cands = [n for n in ui.get("nodes") or [] if n.get("type") in _subgraph_ids(ui)]
    for n in cands:
        sg = _subgraph(ui, n["type"])
        if sg and sg.get("name") == PARENT_NAME:
            return n
    raise ValueError(f"工作流里找不到父图实例 {PARENT_NAME!r}")


def _subgraph_ids(ui: dict) -> set:
    return {s.get("id") for s in (ui.get("definitions") or {}).get("subgraphs") or []}


def _subgraph(ui: dict, sid: str) -> dict | None:
    for s in (ui.get("definitions") or {}).get("subgraphs") or []:
        if s.get("id") == sid:
            return s
    return None


def _top_links(ui: dict) -> dict:
    out = {}
    for l in ui.get("links") or []:
        if isinstance(l, list):
            out[l[0]] = (l[1], l[2], l[3], l[4])
        elif isinstance(l, dict):
            out[l.get("id")] = (l.get("origin_id"), l.get("origin_slot"),
                                l.get("target_id"), l.get("target_slot"))
    return out


def _parent_links(sg: dict) -> dict:
    out = {}
    for l in sg.get("links") or []:
        if isinstance(l, dict):
            out[l.get("id")] = (l.get("origin_id"), l.get("origin_slot"),
                                l.get("target_id"), l.get("target_slot"))
    return out


def _prefix_of(ui: dict, save_id: Any) -> str:
    for n in ui.get("nodes") or []:
        if n.get("id") == save_id:
            named = n.get("widgets_values_named") or {}
            return named.get("filename_prefix") or (n.get("widgets_values") or [""])[0]
    return ""


def angle_table(ui: dict) -> list[dict]:
    """8 个角度：槽位 → 角度名(key) / 提示词 / 子图实例 id / SaveImage 节点 id。

    **槽位顺序**取自父图 `outputs` 的声明顺序（= /prompt 里的输出顺序），
    不是 JSON 文件里节点的排列顺序 —— 官方模板里两者不同，按文件顺序会张冠李戴。
    """
    inst = parent_instance(ui)
    sg = _subgraph(ui, inst["type"]) or {}
    plinks = _parent_links(sg)
    tlinks = _top_links(ui)
    byid = {n.get("id"): n for n in ui.get("nodes") or []}
    rows: list[dict] = []
    for slot, out in enumerate(sg.get("outputs") or []):
        child_id = None
        for lid in (out.get("linkIds") or []):
            src = plinks.get(lid)
            if src:
                child_id = src[0]
        prompt = ""
        for n in sg.get("nodes") or []:
            if n.get("id") == child_id:
                prompt = (n.get("widgets_values_named") or {}).get("prompt") or (
                    n.get("widgets_values") or [""])[0]
        save_id = None
        for o in (inst.get("outputs") or [])[slot:slot + 1] or []:
            for lid in (o.get("links") or []):
                tgt = tlinks.get(lid)
                if tgt:
                    save_id = tgt[2]
        prefix = _prefix_of(ui, save_id)
        rows.append({"slot": slot, "key": prefix.replace("ComfyUI-", ""), "prompt": (prompt or "").strip(),
                     "child_id": child_id, "save_id": save_id, "prefix": prefix,
                     "save_class": (byid.get(save_id) or {}).get("type")})
    return rows


# --------------------------------------------------------------------------
# UI 层改写（在转换之前做，目标明确、可报告）
# --------------------------------------------------------------------------
def _set_child_prompt(sg: dict, child_id: Any, text: str) -> bool:
    for n in sg.get("nodes") or []:
        if n.get("id") == child_id:
            w = n.get("widgets_values")
            if isinstance(w, list) and w:
                w[0] = text
            elif isinstance(w, list):
                w.append(text)
            (n.setdefault("widgets_values_named", {}))["prompt"] = text
            return True
    return False


def apply_angle_prompts(ui: dict, table: list[dict], overrides: dict[str, str],
                        *, prefix: str = "", suffix: str = "") -> list[str]:
    """改写角度提示词（`--angle`）+ 统一前后缀（`--prompt-prefix/--prompt-suffix`）。"""
    inst = parent_instance(ui)
    sg = _subgraph(ui, inst["type"]) or {}
    applied: list[str] = []
    for row in table:
        text = overrides.get(row["key"], row["prompt"])
        if prefix:
            text = prefix.rstrip() + " " + text.lstrip()
        if suffix:
            text = text.rstrip() + " " + suffix.lstrip()
        if text != row["prompt"] or overrides.get(row["key"]):
            if _set_child_prompt(sg, row["child_id"], text):
                applied.append(row["key"])
        row["prompt"] = text
    return applied


def apply_output_prefix(ui: dict, table: list[dict], base: str) -> None:
    """把 8 个 SaveImage 的前缀改成 `<base>/<角度名>`（便于一次跑出一组有名字的文件）。"""
    byid = {n.get("id"): n for n in ui.get("nodes") or []}
    for row in table:
        n = byid.get(row["save_id"])
        if not n:
            continue
        new = f"{(base or '').strip('/')}/{row['key']}" if base else row["prefix"]
        n.setdefault("widgets_values", [new])
        if n.get("widgets_values"):
            n["widgets_values"][0] = new
        else:
            n["widgets_values"] = [new]
        (n.setdefault("widgets_values_named", {}))["filename_prefix"] = new
        row["prefix"] = new


def set_load_image(ui: dict, name: str) -> str | None:
    """把唯一的 LoadImage 指到上传后的文件名。"""
    for n in ui.get("nodes") or []:
        if n.get("type") == LOAD_CLASS:
            n.setdefault("widgets_values", [name])
            if n["widgets_values"]:
                n["widgets_values"][0] = name
            else:
                n["widgets_values"] = [name]
            (n.setdefault("widgets_values_named", {}))["image"] = name
            return name
    return None


def upload_image(server: str, path: str, timeout: float = 300.0) -> str:
    """POST /upload/image，返回服务器 input 目录里的名字。"""
    with open(path, "rb") as fh:
        blob = fh.read()
    boundary = "----dsh" + uuid.uuid4().hex
    name = os.path.basename(path)
    parts = [
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="image"; filename="{name}"\r\n'.encode(),
        b"Content-Type: application/octet-stream\r\n\r\n",
        blob,
        f"\r\n--{boundary}\r\n".encode(),
        b'Content-Disposition: form-data; name="overwrite"\r\n\r\n1',
        f"\r\n--{boundary}\r\n".encode(),
        b'Content-Disposition: form-data; name="type"\r\n\r\ninput',
        f"\r\n--{boundary}\r\n".encode(),
        b'Content-Disposition: form-data; name="subfolder"\r\n\r\n',
        b"",
        f"\r\n--{boundary}--\r\n".encode(),
    ]
    req = urllib.request.Request(f"{server.rstrip('/')}/upload/image", data=b"".join(parts))
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise ValueError(f"上传 {path} 失败（HTTP {exc.code}）：{detail[:400]}") from exc
    sub = payload.get("subfolder") or ""
    return f"{sub}/{payload['name']}" if sub else payload["name"]


# --------------------------------------------------------------------------
# 转换 + 图级校验
# --------------------------------------------------------------------------
def set_fast_mode(ui: dict, fast: bool) -> list[str]:
    """在 8 个子图**实例**上把 `value`（enable_turbo_mode）设成 `fast`。

    ⚠️ **实测结论（两次对照）**：这条开关的取值**只认子图实例上的 widget**：
      * 改父图实例的 `value` → 转换出的图**逐字节相同**（转换器不透传实例接口值，`convert_ex` 记为 unapplied）
      * 改子图**定义**里的 `PrimitiveBoolean` → 也**无效**（实例 widget 覆盖定义）
      * 改子图**实例**的 `value` widget → ✅ 图里 8 个 `PrimitiveBoolean` 全部跟着变
    所以这里改实例；顺手把父图实例的 `value` 同步成同一个值，免得 UI 上读数自相矛盾。
    """
    inst = parent_instance(ui)
    sg = _subgraph(ui, inst["type"]) or {}
    touched: list[str] = []
    for n in sg.get("nodes") or []:
        if n.get("type") not in _subgraph_ids(ui):
            continue
        named = n.setdefault("widgets_values_named", {})
        named["value"] = fast
        w = n.get("widgets_values")
        if isinstance(w, list):
            keys = list(named)
            idx = keys.index("value") if "value" in keys else 1
            if idx < len(w):
                w[idx] = fast
        touched.append(str(n.get("id")))
    if isinstance(inst.get("widgets_values"), list) and inst["widgets_values"]:
        inst["widgets_values"][0] = fast
    (inst.setdefault("widgets_values_named", {}))["value"] = fast
    return touched


def apply_only(ui: dict, table: list[dict], selected: list[str]) -> list[str]:
    """把未选中角度的 SaveImage 标成 **bypass(mode=4)**，转换时它们会被丢掉。

    ⚠️ `convert_ex(node_modes=...)` 是**按类名**生效的（`{"SaveImage": 4}` 会旁路掉
    **全部** SaveImage），所以要精确旁路就必须在 UI 上按**节点 id** 设 `mode`。
    """
    keep = set(selected)
    bypassed: list[str] = []
    for n in ui.get("nodes") or []:
        if n.get("type") == SAVE_CLASS and n.get("id") is not None:
            row = next((r for r in table if r["save_id"] == n["id"]), None)
            if row and row["key"] not in keep:
                n["mode"] = 4
                bypassed.append(row["key"])
    return bypassed


def build_api(ui: dict, *, models: dict[str, str] | None = None,
              node_modes: dict[str, int] | None = None) -> tuple[dict, list[str], dict]:
    overrides: dict[str, Any] = {}
    for k, v in (models or {}).items():
        if v:
            overrides[k] = v
    report: dict[str, Any] = {}
    api, _out, warnings = C.convert_ex(copy.deepcopy(ui), overrides, None, node_modes,
                                       strict=True, report=report)
    return api, warnings, report


def save_pairs(api: dict) -> list[tuple[str, str]]:
    """(SaveImage 节点 id, 前缀) —— 按节点 id 数值排序，稳定可测。"""
    rows = [(nid, str(n["inputs"].get("filename_prefix") or ""))
            for nid, n in api.items() if n.get("class_type") == SAVE_CLASS]
    rows.sort(key=lambda r: int(r[0]) if str(r[0]).isdigit() else 1 << 30)
    return rows


def flatten_parent(ui: dict) -> dict:
    """把"父图"这一层摊平：8 个子图实例提到顶层，父图实例从顶层移除。

    ⚠️ **为什么必须这么做（实测）**：这份模板是**两级嵌套**（顶层 → 父图 → 8 个子图），
    而共享转换器只可靠地处理**一级**子图。直接转换会同时坏两头：

      * **输入侧**：子图内部的 `FluxKontextImageScale.image` 变成 `None` —— 参考图**根本没进模型**
      * **输出侧**：8 个 `SaveImage.images` 指向父图内部实例 id（如 `['221', 0]`），那些 id
        **不在展开后的图里** → 提交必失败

    摊平后：顶层 = `LoadImage` + 8 个子图实例 + 8 个 `SaveImage`（**一级嵌套**，正是转换器与
    兄弟技能验证过的形态）。子图实例自己的 widget（角度提示词 / value 开关 / 模型名）原样保留，
    父图接口里**真正是连线**的那几个（这里是 `image`）改接到真实上游节点。
    """
    ui = copy.deepcopy(ui)
    inst = parent_instance(ui)
    sg = _subgraph(ui, inst["type"]) or {}
    top_nodes = ui.get("nodes") or []
    links = ui.get("links") or []
    top_links = _top_links(ui)
    names = [i.get("name") for i in sg.get("inputs") or []]

    # 父图接口 → 真实上游（顶层连线指向父图实例的那些槽）
    iface_src: dict[str, list] = {}
    for lid, (o, osl, tnode, tslot) in top_links.items():
        if str(tnode) == str(inst.get("id")) and isinstance(tslot, int) and tslot < len(names):
            iface_src[names[tslot]] = [str(o), osl]

    # 父图内部：接口 / 兄弟输出 → 子图实例的输入槽
    # 实测：父图内部连到接口的线用 **虚拟输入节点 -10** 表示，`origin_slot` 就是**接口下标**；
    # 连到父图输出的线用 **-20**。所以这里要按下标查名字，而不是按接口 UUID。
    plinks = _parent_links(sg)
    child_src: dict[tuple[str, int], Any] = {}
    for lid, (o, osl, tnode, tslot) in plinks.items():
        src = None
        if o is not None and int(o) == -10:               # 来自某个父图接口
            name = names[osl] if isinstance(osl, int) and osl < len(names) else None
            src = iface_src.get(name)
        elif o is not None and int(o) != -20:             # 来自兄弟子图实例的输出
            src = [str(o), osl]
        if src is not None and tnode is not None:
            child_src[(str(tnode), tslot)] = src

    # 新顶层：把 8 个子图实例搬上来（新 id，避免与顶层已有 id 冲突）
    used = {int(n["id"]) for n in top_nodes if str(n.get("id", "")).isdigit()}
    for _l in (ui.get("links") or []):
        if isinstance(_l, list) and _l and str(_l[0]).isdigit():
            used.add(int(_l[0]))
    nxt = (max(used) + 1) if used else 1
    link_id = max([l.get("id", 0) if isinstance(l, dict) else l[0] for l in links] or [0]) + 1
    new_nodes, new_links, remap = [], [], {}
    for child in sg.get("nodes") or []:
        if child.get("type") not in _subgraph_ids(ui):
            continue
        nid = nxt
        nxt += 1
        remap[str(child.get("id"))] = str(nid)
        node = {k: copy.deepcopy(v) for k, v in child.items() if k not in ("inputs", "outputs", "order")}
        node["id"] = nid
        node["inputs"] = []
        node["outputs"] = []
        new_nodes.append(node)

    # 连线：上游 → 子图实例输入
    for child in sg.get("nodes") or []:
        if child.get("type") not in _subgraph_ids(ui):
            continue
        nid = int(remap[str(child.get("id"))])
        for slot, decl in enumerate(child.get("inputs") or []):
            src = child_src.get((str(child.get("id")), slot))
            if not src:
                continue
            new_links.append([link_id, int(src[0]) if str(src[0]).isdigit() else src[0],
                              src[1], nid, slot, decl.get("type")])
            node = next(n for n in new_nodes if n["id"] == nid)
            node["inputs"].append({"name": decl.get("name"), "type": decl.get("type"),
                                   "link": link_id})
            link_id += 1

    # 连线：子图实例输出 → 顶层 SaveImage（按父图 outputs 声明顺序）
    saves_by_slot = {}
    for slot, out in enumerate(sg.get("outputs") or []):
        for lid in (out.get("linkIds") or []):
            src = plinks.get(lid)
            if src:
                saves_by_slot[slot] = str(src[0])
    for n in top_nodes:
        if n.get("type") != SAVE_CLASS:
            continue
        for slot, child_id in saves_by_slot.items():
            tgt = top_links.get((n.get("inputs") or [{}])[0].get("link"))
        # 用实例的输出连线来定 SaveImage：inst.outputs[slot].links → 顶层 link → SaveImage
    save_of_slot = {}
    for slot, o in enumerate(inst.get("outputs") or []):
        for lid in (o.get("links") or []):
            t = top_links.get(lid)
            if t:
                save_of_slot[slot] = t[2]
    for slot, save_id in save_of_slot.items():
        child_id = saves_by_slot.get(slot)
        if child_id is None or str(save_id) not in {str(n["id"]) for n in top_nodes}:
            continue
        new_id = int(remap[str(child_id)])
        new_links.append([link_id, new_id, 0, save_id, 0, "IMAGE"])
        snode = next(n for n in top_nodes if str(n["id"]) == str(save_id))
        snode["inputs"] = [{"name": "images", "type": "IMAGE", "link": link_id}]
        node = next(n for n in new_nodes if n["id"] == new_id)
        node["outputs"].append({"name": "IMAGE", "type": "IMAGE", "links": [link_id]})
        link_id += 1

    kept = [n for n in top_nodes if str(n.get("id")) != str(inst.get("id"))] + new_nodes
    kept_links = [l for l in links if not _targets(l, inst.get("id"))]
    ui["nodes"] = kept
    ui["links"] = kept_links + new_links
    return ui


def _targets(link: Any, node_id: Any) -> bool:
    if isinstance(link, dict):
        return str(link.get("target_id")) == str(node_id)
    return len(link) > 3 and str(link[3]) == str(node_id)


def dangling_links(api: dict) -> list[str]:
    """指向"不在图里的节点"的连线（提交前必须为空）。"""
    bad: list[str] = []
    for nid, node in api.items():
        for key, val in (node.get("inputs") or {}).items():
            if (isinstance(val, list) and len(val) == 2 and isinstance(val[0], (str, int))
                    and str(val[0]) not in api):
                bad.append(f"#{nid}.{key} → {val}（节点不在图里）")
    return bad


def prune_unreachable(api: dict) -> list[str]:
    """删掉没有任何输出依赖的节点（`--only` 之后那些未选角度的子图仍在图里）。

    ComfyUI 的执行器本来也只会跑输出所需的部分，但把死节点删掉有两层好处：
    提交的图更小、`--only` 到底省了什么一眼可见（也便于测试断言）。
    """
    roots = [nid for nid, n in api.items() if n.get("class_type") == SAVE_CLASS]
    keep: set[str] = set()
    stack = list(roots)
    while stack:
        nid = stack.pop()
        if nid in keep or nid not in api:
            continue
        keep.add(nid)
        for v in (api[nid].get("inputs") or {}).values():
            if isinstance(v, list) and v and str(v[0]) in api:
                stack.append(str(v[0]))
    gone = [nid for nid in api if nid not in keep]
    for nid in gone:
        api.pop(nid, None)
    return gone


def set_seeds(api: dict, base: int) -> list[int]:
    """给 8 个 KSampler 设确定性种子（base, base+1, …，按节点 id 排序）。"""
    ids = sorted((nid for nid, n in api.items() if n.get("class_type") == "KSampler"),
                 key=lambda x: int(x) if str(x).isdigit() else 1 << 30)
    seeds = []
    for i, nid in enumerate(ids):
        seed = (base + i) % (2 ** 31)
        api[nid]["inputs"]["seed"] = seed
        seeds.append(seed)
    return seeds


def validate(api: dict, expected: int, report: dict) -> list[str]:
    problems: list[str] = []
    if report.get("unapplied"):
        problems.append(f"有参数没落图：{report['unapplied']}")
    pairs = save_pairs(api)
    if len(pairs) != expected:
        problems.append(f"输出节点数 {len(pairs)} ≠ 期望 {expected}（--only 会旁路掉未选角度）")
    if len({p for _, p in pairs}) != len(pairs):
        problems.append(f"输出前缀有重名：{[p for _, p in pairs]}")
    ks = [n for n in api.values() if n.get("class_type") == "KSampler"]
    if len(ks) != expected:
        problems.append(f"KSampler 数 {len(ks)} ≠ 期望 {expected}")
    pos = [n for n in api.values() if n.get("class_type") == "TextEncodeQwenImageEditPlus"
           and isinstance(n["inputs"].get("prompt"), str) and n["inputs"]["prompt"].strip()]
    if len(pos) != expected:
        problems.append(f"带提示词的正向编码节点 {len(pos)} ≠ 期望 {expected}")
    for nm, v in [("LoadImage", LOAD_CLASS)]:
        if not any(n.get("class_type") == v for n in api.values()):
            problems.append(f"图里没有 {nm}")
    dangling = dangling_links(api)
    if dangling:
        problems.append(f"有 {len(dangling)} 条连线指向图外的节点（提交必失败）：{dangling[:3]}")
    return problems


# --------------------------------------------------------------------------
# --list / --check
# --------------------------------------------------------------------------
def describe(ui: dict) -> dict:
    table = angle_table(ui)
    inst = parent_instance(ui)
    named = inst.get("widgets_values_named") or {}
    fast = named.get("value")
    return {
        "engine": ENGINE,
        "workflow": os.path.relpath(DEFAULT_WORKFLOW, HERE),
        "parent_subgraph": PARENT_NAME,
        "angles": [{k: r[k] for k in ("slot", "key", "prompt", "save_id", "prefix")} for r in table],
        "angle_count": len(table),
        "models": [{"folder": f, "name": n} for f, n in REQUIRED_MODELS],
        "switch": {
            "interface": "value（enable_turbo_mode）",
            "current": fast,
            "true": "快档：4 步 + cfg 1 + Lightning LoRA（模板默认）",
            "false": ("慢档：40 步 + cfg 4，不走 Lightning —— **实测单张 576.5 s（9 分 37 秒）**，"
                      "比快档慢 16×；8 个角度线性外推 ≈ 76 分钟"),
            "where": ("UI 链：实例 value → 父图接口 → 子图实例 → 子图内 PrimitiveBoolean → 三个 ComfySwitchNode；"
                      "但转换器不透传实例接口值，所以脚本直接改 8 个子图里的 PrimitiveBoolean（--fast/--no-fast）"),
        },
        "input": "一张参考图（LoadImage）；子图内另有 image2/image3 但父图未接线（模板如此，属可选输入）",
        "output_names": "每个角度一个 SaveImage，前缀即角度名（已修正官方模板里两处错名/重名）",
        "eta_fast_s": round(SECONDS_PER_ANGLE_FAST * len(table)),
        "eta_slow_s": round(SECONDS_PER_ANGLE_SLOW * len(table)),
        "server_default": DEFAULT_SERVER,
    }


def run_check(server: str) -> tuple[dict, int]:
    result: dict[str, Any] = {"server": server, "engine": ENGINE}
    health = G.check_server(server)
    result["reachable"] = health["reachable"]
    if not health["reachable"]:
        result["error"] = health["error"]
        result["hint"] = "服务器不可达：先确认 ComfyUI 已启动、--listen 已开、防火墙放通端口"
        return result, EXIT_UNREACHABLE
    result["comfyui_version"] = (health["stats"].get("system") or {}).get("comfyui_version")

    missing_models: list[str] = []
    for folder, name in REQUIRED_MODELS:
        try:
            have = G.list_models(server, folder)
        except Exception as exc:  # noqa: BLE001
            result.setdefault("errors", []).append(f"{folder}: {exc}")
            continue
        if name not in have:
            missing_models.append(f"{folder}/{name}")
    result["missing_models"] = missing_models

    missing_nodes: list[str] = []
    for cls in REQUIRED_NODES:
        try:
            G._get_json(f"{server.rstrip('/')}/object_info/{cls}", timeout=20.0)
        except Exception:  # noqa: BLE001 - 404 或异常都算缺
            missing_nodes.append(cls)
    result["missing_nodes"] = missing_nodes
    result["ok"] = not missing_models and not missing_nodes
    result["eta_fast_s"] = round(SECONDS_PER_ANGLE_FAST * 8)
    if missing_models:
        result["hint"] = "缺模型文件：按 assets 工作流里的 MarkdownNote 链接下载到对应目录"
    elif missing_nodes:
        result["hint"] = "缺节点类：ComfyUI 版本偏旧，或启动参数带了 --disable-* 开关"
    return result, (EXIT_OK if result["ok"] else EXIT_NO_NODE)


# --------------------------------------------------------------------------
# 生成
# --------------------------------------------------------------------------
def generate(
    server: str = DEFAULT_SERVER,
    workflow: str = DEFAULT_WORKFLOW,
    image: str | None = None,
    image_name: str | None = None,
    only: list[str] | None = None,
    angles: dict[str, str] | None = None,
    prompt_prefix: str = "",
    prompt_suffix: str = "",
    output_prefix: str = "",
    fast: bool | None = None,
    seed: int | None = None,
    models: dict[str, str] | None = None,
    out_dir: str = "out",
    timeout: float = 3600.0,
    poll: float = 5.0,
    quiet: bool = False,
    record: bool = True,
    plan: bool = False,
) -> dict:
    """跑一次多角度批量生成，返回可 JSON 序列化的摘要。"""
    ui = json.load(open(workflow, encoding="utf-8"))
    table = angle_table(ui)
    by_key = {r["key"]: r for r in table}
    selected = list(by_key) if not only else [k.strip() for k in only if k.strip()]
    bad = [k for k in selected if k not in by_key]
    if bad:
        raise ValueError(f"没有这些角度：{bad}；可用：{sorted(by_key)}")

    overrides = {k: v for k, v in (angles or {}).items() if k in by_key}
    unknown = [k for k in (angles or {}) if k not in by_key]
    if unknown:
        raise ValueError(f"--angle 指定了不存在的角度：{unknown}；可用：{sorted(by_key)}")

    uploaded: str | None = None
    src_name = image_name
    if image:
        if plan:
            src_name = f"<plan:{os.path.basename(image)}>"
        else:
            uploaded = upload_image(server, image, timeout=min(timeout, 300.0))
            src_name = uploaded
    if not src_name:
        raise ValueError("要给一张参考图：--image <本地图> 或 --image-name <服务器上已有图>")
    if not set_load_image(ui, src_name):
        raise RuntimeError("工作流里没有 LoadImage")

    apply_angle_prompts(ui, table, overrides, prefix=prompt_prefix, suffix=prompt_suffix)
    if output_prefix:
        apply_output_prefix(ui, table, output_prefix)

    bypassed = apply_only(ui, table, selected)
    fast_touched = set_fast_mode(ui, fast) if fast is not None else []
    # ⚠️ 必须先摊平父图这一层（两级嵌套转换器处理不了：参考图会丢、输出连线会悬空）
    flat = flatten_parent(ui)
    api, warnings, report = build_api(flat, models=models)
    dangling_before = dangling_links(api)   # 摊平后应为 0（否则说明还有未解析的子图跳）
    pruned = prune_unreachable(api)
    seeds = set_seeds(api, seed) if seed is not None else []

    # 角度名以**工作流里的输出节点 id** 为准（不要从前缀反推：--output-prefix 会改写前缀）
    prefix_of_save = dict(save_pairs(api))
    key_of_save = {str(r["save_id"]): r["key"] for r in table}
    pairs = [(key_of_save.get(nid, pfx), nid) for nid, pfx in save_pairs(api)]
    want = set(selected)
    kept = [(k, nid) for k, nid in pairs if k in want]
    if len(kept) != len(selected):
        raise ValueError(f"选中的角度与图里的输出对不上：选中 {sorted(want)}，图里 {sorted(k for k, _ in pairs)}")
    problems = validate(api, len(selected), report)

    summary: dict[str, Any] = {
        "engine": ENGINE, "server": server, "plan": plan, "input_image": src_name,
        "uploaded": uploaded, "angles_requested": selected, "angles_in_graph": [k for k, _ in pairs],
        "outputs": {k: nid for k, nid in kept},
        "output_prefixes": {k: prefix_of_save.get(nid, "") for k, nid in kept}, "seeds": seeds, "applied": report.get("applied"),
        "unapplied": report.get("unapplied"), "warnings": warnings,
        "fast": fast, "fast_switches_set": fast_touched, "bypassed_angles": bypassed,
        "eta_s": round((SECONDS_PER_ANGLE_FAST if fast is not False else SECONDS_PER_ANGLE_SLOW)
                       * len(selected)),
        "nodes": len(api), "pruned_nodes": len(pruned),
        "dangling_links_after_flatten": dangling_before, "dangling_links": dangling_links(api),
        "graph": api,
    }
    if problems:
        summary["problems"] = problems
        raise ValueError("API 图校验不过：\n  - " + "\n  - ".join(problems))
    if plan:
        summary["next"] = "确认无误后去掉 --plan 真跑（8 张约 5 分钟；--only 可以只出几个角度）"
        return summary

    started = time.time()
    prompt_id = G.queue_prompt(server, api, f"dsh-angles-{os.getpid()}", timeout=120.0)
    if not quiet:
        print(f"-> qwen-2511 multi-angle @ {server}  角度={len(selected)}  ETA≈{summary['eta_s']}s  "
              f"prompt_id={prompt_id}", flush=True)
    entry = G.wait_for_history(server, prompt_id, timeout=timeout, poll=poll, quiet=quiet)
    elapsed = time.time() - started

    local: dict[str, str] = {}
    for key, nid in kept:
        items = G.collect_images(entry, only_node=nid)
        for i, item in enumerate(items):
            suffix = "" if len(items) == 1 else f"_{i + 1}"
            dest = os.path.join(out_dir, f"{key}{suffix}.png")
            os.makedirs(out_dir, exist_ok=True)
            with open(dest, "wb") as fh:
                fh.write(G._request(
                    f"{server.rstrip('/')}/view?" + urllib.parse.urlencode(
                        {"filename": item["filename"], "subfolder": item.get("subfolder", ""),
                         "type": item.get("type", "output")}), timeout=600.0))
            local[key] = dest
    summary.update({"prompt_id": prompt_id, "elapsed_s": round(elapsed, 1),
                    "status": (entry.get("status") or {}).get("status_str"),
                    "local_paths": local, "per_angle_s": round(elapsed / max(len(selected), 1), 1)})
    if record:
        prefix = f"multi-angle-{len(selected)}" + (f"-{output_prefix}" if output_prefix else "")
        summary["record"] = G.record_request(
            out_dir, prefix.replace("/", "_"), ENGINE, server,
            {k: v for k, v in summary.items() if k not in ("graph", "local_paths")},
            prompt_id, api, list(local.values()))
    return summary


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def _parse_kv(pairs: list[str] | None, what: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in pairs or []:
        if "=" not in p:
            raise ValueError(f"{what} 要写成 KEY=VALUE，收到 {p!r}")
        k, v = p.split("=", 1)
        out[k.strip()] = v
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=DEFAULT_SERVER, help=f"ComfyUI 地址（默认 {DEFAULT_SERVER}）")
    ap.add_argument("--workflow", default=DEFAULT_WORKFLOW, help="UI 工作流 JSON")
    ap.add_argument("--image", help="本地参考图（会被上传）")
    ap.add_argument("--image-name", help="服务器 input 里已有的图（免上传）")
    ap.add_argument("--only", help="只出这些角度（逗号分隔，键见 --list），其余旁路")
    ap.add_argument("--angle", action="append", metavar="KEY=TEXT",
                    help="改写某个角度的提示词（可重复）")
    ap.add_argument("--prompt-prefix", default="", help="给 8 条角度提示词统一加前缀")
    ap.add_argument("--prompt-suffix", default="", help="统一加后缀（如保持人物一致性的约束）")
    ap.add_argument("--output-prefix", default="", help="输出前缀改成 <此值>/<角度名>")
    ap.add_argument("--fast", dest="fast", action="store_true", default=None,
                    help="快档：4 步 + cfg 1 + Lightning LoRA（模板默认）")
    ap.add_argument("--no-fast", dest="fast", action="store_false",
                    help="慢档：40 步 + cfg 4，不走 Lightning")
    ap.add_argument("--seed", type=int, help="确定性种子（8 个角度依次用 seed, seed+1, …）")
    ap.add_argument("--unet-name"), ap.add_argument("--clip-name")
    ap.add_argument("--vae-name"), ap.add_argument("--lora-name")
    ap.add_argument("--lora-name-1")
    ap.add_argument("--out-dir", default="out", help="产物与留档目录（默认 out）")
    ap.add_argument("--timeout", type=float, default=3600.0, help="等成品的最长秒数")
    ap.add_argument("--poll", type=float, default=5.0)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-record", dest="record", action="store_false", default=True)
    ap.add_argument("--plan", action="store_true",
                    help="只验证参数与接线（**不提交、不上传**）")
    ap.add_argument("--list", dest="list_params", action="store_true", help="列出角度/模型/快慢档")
    ap.add_argument("--check", action="store_true", help="真机：模型与节点类是否在位")
    args = ap.parse_args(argv)

    def emit(payload) -> None:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    try:
        if args.list_params:
            emit(describe(json.load(open(args.workflow, encoding="utf-8"))))
            return EXIT_OK
        if args.check:
            result, code = run_check(args.server)
            emit(result)
            return code
        models = {"unet_name": args.unet_name, "clip_name": args.clip_name,
                  "vae_name": args.vae_name, "lora_name": args.lora_name,
                  "lora_name_1": args.lora_name_1}
        summary = generate(
            server=args.server, workflow=args.workflow, image=args.image,
            image_name=args.image_name,
            only=args.only.split(",") if args.only else None,
            angles=_parse_kv(args.angle, "--angle"),
            prompt_prefix=args.prompt_prefix, prompt_suffix=args.prompt_suffix,
            output_prefix=args.output_prefix, fast=args.fast, seed=args.seed,
            models={k: v for k, v in models.items() if v},
            out_dir=args.out_dir, timeout=args.timeout, poll=args.poll,
            quiet=args.quiet, record=args.record, plan=args.plan)
        emit(summary)
        if args.plan:
            return EXIT_OK
        return EXIT_OK if summary.get("local_paths") else EXIT_NO_OUTPUT
    except ValueError as exc:
        emit({"ok": False, "error": str(exc), "kind": "bad_params"})
        return EXIT_BAD_PARAMS
    except TimeoutError as exc:
        emit({"ok": False, "error": str(exc), "kind": "timeout"})
        return EXIT_TIMEOUT
    except KeyboardInterrupt:
        return EXIT_BAD_PARAMS


if __name__ == "__main__":
    sys.exit(main())
