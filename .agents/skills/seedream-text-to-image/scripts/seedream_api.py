#!/usr/bin/env python3
"""把 ComfyUI 的 UI 版工作流（V3 命名 widget 格式）转成 /prompt API 图，并按节点 schema 校验。

为什么本技能自带一个转换器，而不复用 `text-to-image-comfyui/scripts/comfyui_convert.py`：

  1. 那份转换器面向 `definitions.subgraphs` 子图工作流，对**扁平的两节点工作流**直接抛
     "no subgraph node found"；
  2. Seedream 节点用的是 V3 动态下拉框（`COMFY_DYNAMICCOMBO_V3`），它的子输入在 API 格式里
     **带前缀**（`model.size_preset`、`model.thinking`、`format.bit_depth`），而
     `widgets_values_named` 正好就是这个形状 —— 照抄即可，重新推断反而容易错；
  3. 付费节点必须在提交前就知道"这个参数对所选模型到底存不存在"，这要靠 schema，不靠猜。

核心事实（真机实测，证据见 references/api-node.md）：

  * API 输入名 = `widgets_values_named` 的键（带点）。把 `model.height` 写成 `height` 会被
    服务器判 `Required input is missing`。
  * `control_after_generate` / `control_after_generate#1` 是前端伪 widget，不能进 API 图。
  * `model.images`（COMFY_AUTOGROW_V3）在 schema 里挂在 required 下，但**不给也能过校验**：
    它是采集式可选输入。纯文生图不给；图生图才用（本技能不做，见 SKILL.md）。
  * 每个模型支持的参数不同：pro 有 `prompt_optimization`，flash 连 `thinking` 都没有，
    lite/4.5/4.0 有 `max_images` + `fail_on_partial` 而 pro/flash 没有。
  * 导出的 UI 图里可能有**前端专有节点**（`MarkdownNote` 等）：服务器上不存在，
    提交前必须 `prune_ui_only()`，否则 /prompt 直接 400 `missing_node_type`。

Importable:
  from seedream_api import load_workflow, build_api_graph, apply_params, validate_graph
"""
from __future__ import annotations

import copy
import json
import os
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_WORKFLOW = os.path.normpath(
    os.path.join(HERE, "..", "assets", "seedream-5.0-pro-t2i-ui.json")
)
DEFAULT_NODE_INFO = os.path.normpath(os.path.join(HERE, "..", "references", "node-info.json"))

SEEDREAM_CLASS = "ByteDanceSeedreamNodeV3"
SAVE_CLASS = "SaveImageAdvanced"
SAVE_FALLBACKS = ("SaveImageAdvanced", "SaveImage")
DYNAMIC_COMBO = "COMFY_DYNAMICCOMBO_V3"
AUTOGROW = "COMFY_AUTOGROW_V3"

# 前端伪 widget：只控制界面上"生成后如何变化"，不是节点输入。
PSEUDO_WIDGETS = ("control_after_generate",)

# 前端专有节点：只存在于界面画布上，服务器上没有实现，原样提交会被 /prompt 判
# `missing_node_type`（真机实测：带 MarkdownNote 的导出图 400，见
# seedream-image-edit/references/api-node.md §2）。
UI_ONLY_CLASSES = ("MarkdownNote", "Note", "PrimitiveNode", "Reroute", "GroupNode")

# 友好参数名 -> (节点类, API 输入名)。size 另走 parse_size。
PARAM_TARGETS: dict[str, tuple[str, str]] = {
    "prompt": (SEEDREAM_CLASS, "prompt"),
    "model": (SEEDREAM_CLASS, "model"),
    "width": (SEEDREAM_CLASS, "model.width"),
    "height": (SEEDREAM_CLASS, "model.height"),
    "seed": (SEEDREAM_CLASS, "model.seed"),
    "thinking": (SEEDREAM_CLASS, "model.thinking"),
    "watermark": (SEEDREAM_CLASS, "model.watermark"),
    "prompt_optimization": (SEEDREAM_CLASS, "model.prompt_optimization"),
    "max_images": (SEEDREAM_CLASS, "model.max_images"),
    "fail_on_partial": (SEEDREAM_CLASS, "model.fail_on_partial"),
    "filename_prefix": (SAVE_CLASS, "filename_prefix"),
    "format": (SAVE_CLASS, "format"),
    "bit_depth": (SAVE_CLASS, "format.bit_depth"),
    "color_space": (SAVE_CLASS, "format.input_color_space"),
}
# 始终存在的输入，不作为"该模型额外支持什么"的提示项
ALWAYS_ON = {"prompt", "model", "model.width", "model.height", "model.size_preset"}


class UnappliedOverrideError(RuntimeError):
    """请求的参数对所选模型不存在 —— 静默丢掉会毁掉一整轮实验，所以直接报错。"""


class UnknownModelError(ValueError):
    pass


class InvalidValueError(ValueError):
    pass


# --------------------------------------------------------------------------
# schema
# --------------------------------------------------------------------------
def load_node_info(path: str = DEFAULT_NODE_INFO) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def node_schema(info: dict, cls: str) -> dict:
    nodes = info.get("nodes") or info
    if cls not in nodes:
        raise KeyError(f"schema 里没有节点 {cls}；可用：{sorted(nodes)}")
    return nodes[cls]


def _spec_kind(spec: Any) -> str:
    """节点 schema 里一个输入声明的类型名（列表首项）。"""
    if isinstance(spec, list) and spec:
        return spec[0] if isinstance(spec[0], str) else str(spec[0])
    return ""


def _spec_opts(spec: Any) -> dict:
    if isinstance(spec, list) and len(spec) > 1 and isinstance(spec[1], dict):
        return spec[1]
    return {}


def model_keys(info: dict, cls: str = SEEDREAM_CLASS) -> list[str]:
    spec = node_schema(info, cls)["input"]["required"]["model"]
    return [o["key"] for o in _spec_opts(spec).get("options", [])]


def dynamic_options(info: dict, cls: str, input_name: str) -> list[dict]:
    spec = node_schema(info, cls)["input"]["required"].get(input_name)
    if not spec or _spec_kind(spec) != DYNAMIC_COMBO:
        return []
    return list(_spec_opts(spec).get("options") or [])


def dynamic_sub_inputs(info: dict, cls: str, input_name: str, key: str) -> dict[str, Any]:
    """动态下拉框某个选项下的子输入 -> 规格，键是 API 格式的带点名字。"""
    for opt in dynamic_options(info, cls, input_name):
        if opt.get("key") == key:
            ins = opt.get("inputs") or {}
            out: dict[str, Any] = {}
            for section in ("required", "optional"):
                for name, spec in (ins.get(section) or {}).items():
                    out[f"{input_name}.{name}"] = spec
            return out
    return {}


def model_param_names(info: dict, key: str) -> dict[str, Any]:
    """所选模型在 API 图里认的全部输入（含 prompt / model 自身）。"""
    required = node_schema(info, SEEDREAM_CLASS)["input"]["required"]
    names = {"prompt": required["prompt"], "model": required["model"]}
    names.update(dynamic_sub_inputs(info, SEEDREAM_CLASS, "model", key))
    return names


def save_param_names(info: dict, fmt: str | None = None) -> dict[str, Any]:
    """保存节点在 API 图里认的输入；`format` 是动态下拉框，子输入随格式变。"""
    required = node_schema(info, SAVE_CLASS)["input"]["required"]
    names = {k: v for k, v in required.items() if k in ("images", "filename_prefix", "format")}
    if fmt is None:
        fmt = _spec_opts(required.get("format", [])).get("default")
        if fmt is None:
            options = dynamic_options(info, SAVE_CLASS, "format")
            fmt = options[0]["key"] if options else None
    if fmt:
        names.update(dynamic_sub_inputs(info, SAVE_CLASS, "format", fmt))
    return names


def size_presets(info: dict, model: str) -> list[str]:
    subs = dynamic_sub_inputs(info, SEEDREAM_CLASS, "model", model)
    return list(_spec_opts(subs.get("model.size_preset", [])).get("options") or [])


# --------------------------------------------------------------------------
# 工作流 -> API 图
# --------------------------------------------------------------------------
def load_workflow(path: str = DEFAULT_WORKFLOW) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _link_index(ui: dict) -> dict[tuple[Any, int], list]:
    """(目标节点, 目标槽) -> [源节点字符串, 源槽]。兼容 list / dict 两种 links 形状。"""
    index: dict[tuple[Any, int], list] = {}
    for link in ui.get("links") or []:
        if isinstance(link, dict):
            origin, oslot = link.get("origin_id"), link.get("origin_slot")
            target, tslot = link.get("target_id"), link.get("target_slot")
        else:
            origin, oslot, target, tslot = link[1], link[2], link[3], link[4]
        if target is None or tslot is None:
            continue
        index[(target, tslot)] = [str(origin), oslot]
    return index


def build_api_graph(ui: dict) -> tuple[dict, str | None]:
    """UI 工作流 -> (API 图, 保存节点 id)。mute/bypass 的节点直接丢弃。"""
    links = _link_index(ui)
    api: dict[str, Any] = {}
    save_ids: list[str] = []
    for node in ui.get("nodes") or []:
        if node.get("mode", 0) != 0:
            continue  # 2 = mute，4 = bypass
        cls = node.get("type")
        if not cls:
            continue
        inputs: dict[str, Any] = {}
        for slot, declared in enumerate(node.get("inputs") or []):
            origin = links.get((node["id"], slot))
            if origin is not None:
                inputs[declared.get("name")] = origin
        for name, value in (node.get("widgets_values_named") or {}).items():
            if any(name == p or name.startswith(p + "#") for p in PSEUDO_WIDGETS):
                continue
            if value is None:
                continue
            inputs[name] = value
        nid = str(node["id"])
        api[nid] = {"class_type": cls, "inputs": inputs,
                    "_meta": {"title": node.get("title") or cls}}
        if cls in SAVE_FALLBACKS:
            save_ids.append(nid)

    def _rank(nid: str) -> int:
        return SAVE_FALLBACKS.index(api[nid]["class_type"])

    save_id = min(save_ids, key=_rank) if save_ids else None
    return api, save_id


def find_node(api: dict, cls: str) -> str | None:
    for nid, node in api.items():
        if node.get("class_type") == cls:
            return nid
    return None


def prune_ui_only(
    api: dict,
    known_classes: set[str] | None = None,
    drop: tuple[str, ...] = UI_ONLY_CLASSES,
) -> tuple[dict, list[dict]]:
    """删掉服务器上没有的节点，并清掉指向它们的连线。

    `known_classes` 给了就按"真机 /object_info 里没有的都删"（最稳），没给就按
    `UI_ONLY_CLASSES` 这份已知的前端专有节点名单删。返回 (新图, 删掉的节点列表)，
    删掉的节点里带 `_dropped_class` 便于回报。

    注意是**原地改**再返回同一个 dict（调用方通常紧接着就要用）。
    """
    dropped: list[dict] = []
    for nid in list(api):
        cls = api[nid].get("class_type")
        hit = (cls not in known_classes) if known_classes is not None else (cls in drop)
        if hit:
            node = api.pop(nid)
            node["_dropped_class"] = cls
            node["_dropped_id"] = nid
            dropped.append(node)
    if dropped:
        gone = {n["_dropped_id"] for n in dropped}
        for node in api.values():
            for name, value in list(node["inputs"].items()):
                if isinstance(value, list) and value and str(value[0]) in gone:
                    node["inputs"].pop(name)
    return api, dropped


# --------------------------------------------------------------------------
# 参数覆盖
# --------------------------------------------------------------------------
def _preset_pixels(preset: str) -> int:
    """从 `(2K) 2048x2048 (1:1)` 里取出 2048*2048；取不到就当无穷大（排在最后）。"""
    for token in preset.replace("(", " ").replace(")", " ").split():
        if "x" in token.lower():
            try:
                width, height = (int(v) for v in token.lower().split("x", 1))
            except ValueError:
                continue
            return width * height
    return 1 << 62


def parse_size(value: str, info: dict, model: str) -> dict[str, Any]:
    """`--size` -> {'model.size_preset': ...} 或 {'model.size_preset': 'Custom', width/height}。

    接受三种写法：预设原文（`(2K) 2048x2048 (1:1)`）、"2048x2048"、比例 "1:1"。
    同比例有多档时取**像素最小**的那一档（服务器给的顺序未必稳定，别依赖顺序）。
    """
    presets = size_presets(info, model)
    raw = str(value).strip()
    if raw == "Custom":
        # "Custom" 本身也在预设列表里，但它必须配 width/height 才有意义
        raise InvalidValueError("--size Custom 要配合 --width/--height；只给 Custom 无法出图")
    if raw in presets:
        return {"model.size_preset": raw}
    if ":" in raw and "x" not in raw.lower():
        want = raw.replace(" ", "")
        hits = [p for p in presets if p.endswith(f"({want})")]
        if hits:
            return {"model.size_preset": min(hits, key=_preset_pixels)}
        raise InvalidValueError(
            f"{model} 没有 {want} 这个比例；可用预设：\n  " + "\n  ".join(presets))
    if "x" in raw.lower():
        try:
            width, height = (int(v) for v in raw.lower().split("x", 1))
        except ValueError as exc:
            raise InvalidValueError(f"--size 解析失败：{raw!r}（写法：1024x1024 或 1:1）") from exc
        for preset in presets:
            if f"{width}x{height}" in preset:
                return {"model.size_preset": preset}
        subs = dynamic_sub_inputs(info, SEEDREAM_CLASS, "model", model)
        for name, val, label in ((("model.width"), width, "宽"), ("model.height", height, "高")):
            spec = _spec_opts(subs.get(name, []))
            lo, hi = spec.get("min"), spec.get("max")
            if (lo is not None and val < lo) or (hi is not None and val > hi):
                raise InvalidValueError(
                    f"{model} 的{label}度 {val} 超出范围 [{lo}, {hi}]；"
                    "要用预设尺寸可写：\n  " + "\n  ".join(presets))
        return {"model.size_preset": "Custom", "model.width": width, "model.height": height}
    raise InvalidValueError(
        f"--size 无法解析：{raw!r}；可用预设：\n  " + "\n  ".join(presets))


def _check_value(label: str, value: Any, spec: Any) -> None:
    kind, opts = _spec_kind(spec), _spec_opts(spec)
    if kind == DYNAMIC_COMBO:
        keys = [o.get("key") for o in opts.get("options") or [] if isinstance(o, dict)]
        if keys and value not in keys:
            raise InvalidValueError(f"{label} 的取值 {value!r} 不在节点允许的集合里：{keys}")
    elif kind == "COMBO":
        choices = opts.get("options")
        if isinstance(choices, list) and choices and isinstance(choices[0], str):
            if value not in choices:
                raise InvalidValueError(
                    f"{label} 的取值 {value!r} 不在节点允许的集合里：{choices}")
    elif kind == "INT":
        if not isinstance(value, int) or isinstance(value, bool):
            raise InvalidValueError(f"{label} 需要整数，收到 {value!r}")
        lo, hi = opts.get("min"), opts.get("max")
        if (lo is not None and value < lo) or (hi is not None and value > hi):
            raise InvalidValueError(f"{label}={value} 超出 [{lo}, {hi}]")
    elif kind == "BOOLEAN":
        if not isinstance(value, bool):
            raise InvalidValueError(f"{label} 需要 true/false，收到 {value!r}")
    elif kind == "STRING":
        if not isinstance(value, str):
            raise InvalidValueError(f"{label} 需要字符串，收到 {value!r}")


def apply_params(
    api: dict,
    params: dict[str, Any],
    info: dict,
    *,
    strict: bool = True,
) -> tuple[dict, dict[str, Any]]:
    """把友好参数写进 API 图；对所选模型不存在的参数默认报错。

    返回 (新图, report)，report = {"applied": [...], "unapplied": {name: value}}。
    """
    api = copy.deepcopy(api)
    report: dict[str, Any] = {"applied": [], "unapplied": {}}
    seed_nid, save_nid = find_node(api, SEEDREAM_CLASS), find_node(api, SAVE_CLASS)
    if seed_nid is None:
        raise KeyError(f"API 图里没有 {SEEDREAM_CLASS} 节点")
    if save_nid is None:
        raise KeyError(f"API 图里没有 {SAVE_CLASS} 节点")

    model = str(params.get("model") or api[seed_nid]["inputs"].get("model") or "")
    keys = model_keys(info)
    if model not in keys:
        raise UnknownModelError(
            f"未知模型 {model!r}；这台服务器上可用的模型：\n  " + "\n  ".join(keys))
    # 模型侧的输入 + 保存节点侧的输入（保存格式用当前图里的值解析，换格式时由下面重算）
    allowed = dict(model_param_names(info, model))
    allowed.update(save_param_names(info, api[save_nid]["inputs"].get("format")))

    # API 输入名 -> (节点 id, 友好名, 值)
    writes: dict[str, tuple[str, str, Any]] = {}
    if params.get("size") is not None:
        for name, value in parse_size(str(params["size"]), info, model).items():
            writes[name] = (seed_nid, "size", value)
    for friendly, value in params.items():
        if value is None or friendly == "size":
            continue
        if friendly not in PARAM_TARGETS:
            report["unapplied"][friendly] = value
            if strict:
                raise UnappliedOverrideError(
                    f"没有 {friendly} 这个参数；可用：{', '.join(sorted(PARAM_TARGETS))}")
            continue
        cls, name = PARAM_TARGETS[friendly]
        writes[name] = (seed_nid if cls == SEEDREAM_CLASS else save_nid, friendly, value)

    # 先落 format：它是动态下拉框，换了格式，允许的子输入集合也跟着换
    fmt_write = writes.pop("format", None)
    if fmt_write is not None:
        nid, friendly, value = fmt_write
        if "format" not in allowed:
            report["unapplied"][friendly] = value
            if strict:
                raise UnappliedOverrideError(f"保存节点不接受 format={value!r}")
        else:
            _check_value("format", value, allowed["format"])
            api[nid]["inputs"]["format"] = value
            report["applied"].append("format")
            allowed = dict(model_param_names(info, model))
            allowed.update(save_param_names(info, value))
            subs = dynamic_sub_inputs(info, SAVE_CLASS, "format", value)
            for name in list(api[nid]["inputs"]):
                if name.startswith("format.") and name not in subs:
                    api[nid]["inputs"].pop(name)
            for name, spec in subs.items():
                default = _spec_opts(spec).get("default")
                current = api[nid]["inputs"].get(name)
                if current is None:
                    if default is not None:
                        api[nid]["inputs"][name] = default
                    continue
                # 旧格式留下的值对新格式可能非法（如 png 的 8-bit 之于 exr）→ 回到该格式的默认
                try:
                    _check_value(name, current, spec)
                except InvalidValueError:
                    if default is None:
                        api[nid]["inputs"].pop(name)
                    else:
                        api[nid]["inputs"][name] = default

    for name, (nid, friendly, value) in writes.items():
        if name not in allowed:
            hint = "、".join(sorted(
                n for _c, n in PARAM_TARGETS.values() if n in allowed and n not in ALWAYS_ON))
            report["unapplied"][friendly] = value
            if strict:
                raise UnappliedOverrideError(
                    f"{model} 不支持 {friendly}（{name}）；该模型额外支持：{hint}")
            continue
        _check_value(f"{friendly}（{name}）", value, allowed[name])
        api[nid]["inputs"][name] = value
        if friendly not in report["applied"]:
            report["applied"].append(friendly)
    return api, report


def validate_graph(api: dict, info: dict | None = None) -> list[str]:
    """本地事前校验：必填齐不齐、值合不合法、连线有没有断。返回问题列表（空 = 通过）。"""
    problems: list[str] = []
    ids = set(api)
    for nid, node in api.items():
        for name, value in node["inputs"].items():
            if isinstance(value, list) and value and str(value[0]) not in ids:
                problems.append(f"节点 {nid} 的 {name} 指向不存在的节点 {value[0]}")
    seed_nid = find_node(api, SEEDREAM_CLASS)
    if seed_nid is None:
        problems.append(f"缺少 {SEEDREAM_CLASS} 节点")
        return problems
    if find_node(api, SAVE_CLASS) is None and find_node(api, "SaveImage") is None:
        problems.append("缺少保存节点（SaveImageAdvanced / SaveImage）")
    if info is None:
        return problems
    inputs = api[seed_nid]["inputs"]
    model = inputs.get("model")
    if model not in model_keys(info):
        problems.append(f"模型 {model!r} 不在服务器可用列表里")
        return problems
    allowed = model_param_names(info, model)
    for name, spec in allowed.items():
        if name.startswith("model.") and _spec_kind(spec) == AUTOGROW:
            continue  # 采集式输入：纯文生图可以不给（真机实测服务器接受）
        if name not in inputs:
            problems.append(f"缺少必填输入 {name}")
    for name, value in inputs.items():
        if name in allowed:
            try:
                _check_value(name, value, allowed[name])
            except InvalidValueError as exc:
                problems.append(str(exc))

    save_nid = find_node(api, SAVE_CLASS)
    if save_nid is not None:
        save_inputs = api[save_nid]["inputs"]
        save_allowed = save_param_names(info, save_inputs.get("format"))
        for name, spec in save_allowed.items():
            if name == "images":
                continue
            if name not in save_inputs:
                problems.append(f"保存节点缺少必填输入 {name}")
        for name, value in save_inputs.items():
            if name in save_allowed and name != "images":
                try:
                    _check_value(name, value, save_allowed[name])
                except InvalidValueError as exc:
                    problems.append(str(exc))
    return problems


def describe(info: dict) -> dict:
    """给 `--list` / `--check` 用：模型 -> 支持的可调参数 + 尺寸预设，另附保存节点参数。"""
    models: dict[str, Any] = {}
    for key in model_keys(info):
        allowed = model_param_names(info, key)
        models[key] = {
            "params": sorted(f for f, (_c, n) in PARAM_TARGETS.items()
                             if n in allowed and n not in ALWAYS_ON),
            "size_presets": size_presets(info, key),
        }
    formats = [o["key"] for o in dynamic_options(info, SAVE_CLASS, "format")]
    save_allowed = save_param_names(info)
    return {
        "models": models,
        "save": {
            "formats": formats,
            "params": sorted(f for f, (_c, n) in PARAM_TARGETS.items()
                             if n in save_allowed and n not in ("images",)),
        },
        "_sizes_note": ("也接受 1024x1024 / 1:1；不在预设里就走 Custom"
                        "（受该模型的 min/max 约束）"),
        "_image_input_note": ("节点还有 model.images（采集式参考图）输入，本技能只做文生图，"
                              "不接参考图"),
    }


def diff_schema(fixture: dict, live: dict) -> dict:
    """离线快照 vs 真机 /object_info：模型增删 + 每个模型的参数增删 + 保存格式增删。"""
    fi, li = model_keys(fixture), model_keys(live)
    drift: dict[str, Any] = {
        "models_added": sorted(set(li) - set(fi)),
        "models_removed": sorted(set(fi) - set(li)),
        "params": {},
    }
    for key in sorted(set(fi) & set(li)):
        fp = sorted(model_param_names(fixture, key))
        lp = sorted(model_param_names(live, key))
        if fp != lp:
            drift["params"][key] = {"added": sorted(set(lp) - set(fp)),
                                    "removed": sorted(set(fp) - set(lp))}
    try:
        ff = [o["key"] for o in dynamic_options(fixture, SAVE_CLASS, "format")]
        lf = [o["key"] for o in dynamic_options(live, SAVE_CLASS, "format")]
    except KeyError:
        ff = lf = []
    if set(ff) != set(lf):
        drift["save_formats"] = {"added": sorted(set(lf) - set(ff)),
                                 "removed": sorted(set(ff) - set(lf))}
    return drift
