#!/usr/bin/env python3
"""Seedance 2.5 参考生视频（r2v）—— 走 ComfyUI 付费 partner 节点。

把 UI 工作流（`assets/seedance-2.5-reference-r2v-ui.json`，节点
`ByteDance2ReferenceNodeV2`）转成 /prompt API 图，按节点 schema 校验参数、
把参考图上传并接到 `model.reference_images.image_N`，带着 ComfyUI 账号凭据提交、
轮询 /history、从 /view 把 mp4 拉回来并留档。

用法::

    python3 seedance_r2v.py --list                     # 看模型、参数、参考图上限（离线）
    python3 seedance_r2v.py --check                    # 真机：节点在不在 + schema 对账 + 有没有凭据
    python3 seedance_r2v.py --show-default-prompt      # 看工作流里自带的那条 r2v 提示词样本
    python3 seedance_r2v.py --reference ref.png --prompt-file p.txt \\
        --resolution 1080p --ratio 9:16 --duration 5 --plan          # 免费：只验证参数落图
    python3 seedance_r2v.py --reference ref.png --prompt-file p.txt \\
        --resolution 1080p --ratio 9:16 --duration 5 --out-dir out/  # 真出片（**按次计费**）

⚠️ 这是**付费**云端节点（`partner/video/ByteDance`）：本机不需要权重，但每一跑都要花
ComfyUI 账号的 credits，而且**不做**任何离线自检兜底 —— 详见 SKILL.md 的"未验证声明"。

退出码沿用兄弟技能：0 正常 / 1 没有产物 / 2 服务器不可达 / 3 服务器没有该节点 /
4 凭据被拒 / 5 被 /prompt 拒绝 / 6 节点执行失败 / 7 超时 / 8 参数问题。
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any

import _shared

_shared.ensure()
import seedream_api as A  # noqa: E402
import seedream_gen as G  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_WORKFLOW = os.path.normpath(
    os.path.join(HERE, "..", "assets", "seedance-2.5-reference-r2v-ui.json"))
DEFAULT_NODE_INFO = os.path.normpath(
    os.path.join(HERE, "..", "references", "node-info.json"))
DEFAULT_SERVER = os.environ.get("COMFYUI_SERVER", "http://192.168.3.5:18000")

ENGINE = "seedance-2.5-r2v"
SEEDANCE_CLASS = "ByteDance2ReferenceNodeV2"
LOAD_CLASS = "LoadImage"
SAVE_CLASS = "SaveVideo"
DYNAMIC_COMBO = A.DYNAMIC_COMBO          # COMFY_DYNAMICCOMBO_V3
AUTOGROW = A.AUTOGROW                    # COMFY_AUTOGROW_V3

# 友好参数名 -> (节点类, API 输入名)。模型自身的子输入统一带 `model.` 前缀。
PARAM_TARGETS: dict[str, tuple[str, str]] = {
    "prompt": (SEEDANCE_CLASS, "model.prompt"),
    "model": (SEEDANCE_CLASS, "model"),
    "resolution": (SEEDANCE_CLASS, "model.resolution"),
    "ratio": (SEEDANCE_CLASS, "model.ratio"),
    "duration": (SEEDANCE_CLASS, "model.duration"),
    "generate_audio": (SEEDANCE_CLASS, "model.generate_audio"),
    "task_type": (SEEDANCE_CLASS, "model.task_type"),
    "output_format": (SEEDANCE_CLASS, "model.output_format"),
    "auto_downscale": (SEEDANCE_CLASS, "model.auto_downscale"),
    "auto_upscale": (SEEDANCE_CLASS, "model.auto_upscale"),
    "seed": (SEEDANCE_CLASS, "seed"),
    "watermark": (SEEDANCE_CLASS, "watermark"),
    "filename_prefix": (SAVE_CLASS, "filename_prefix"),
    "format": (SAVE_CLASS, "format"),
    "codec": (SAVE_CLASS, "codec"),
}

# 采集式（autogrow）输入：数量随图里接了几张变，不是"单个 widget"
AUTOGROW_FIELDS = ("model.reference_images", "model.reference_videos",
                   "model.reference_audios", "model.reference_assets")
# 本技能**只接参考图**：工作流里只有 LoadImage 这一个源节点（v1 的限制，见 SKILL.md）
REF_TEMPLATE = "model.reference_images.image_{}"

# task_type 里需要"参考视频/编辑目标"的那几档，光给图通常跑不动 —— 只警告不拦
TASK_TYPES_NEEDING_VIDEO = ("edit", "extend")


# --------------------------------------------------------------------------
# 小工具
# --------------------------------------------------------------------------
def _node_id_key(nid: str) -> int:
    return int(nid) if str(nid).isdigit() else 1 << 30


def _next_id(api: dict) -> str:
    used = [int(n) for n in api if str(n).isdigit()]
    return str(max(used) + 1 if used else 1)


def _spec_kind(spec: Any) -> str:
    return spec[0] if isinstance(spec, list) and spec and isinstance(spec[0], str) else (
        "CHOICE" if isinstance(spec, list) and spec and isinstance(spec[0], list) else "")


def _spec_opts(spec: Any) -> dict:
    if isinstance(spec, list) and len(spec) > 1 and isinstance(spec[1], dict):
        return spec[1]
    return {}


def _allowed_values(spec: Any) -> list | None:
    """枚举型输入的允许值：CHOICE 在 spec[0]，COMBO/dynamic combo 在 spec[1]['options']。"""
    if isinstance(spec, list) and spec and isinstance(spec[0], list):
        return [x if isinstance(x, str) else x.get("key") for x in spec[0]]
    opts = _spec_opts(spec).get("options")
    if isinstance(opts, list):
        return [x if isinstance(x, str) else x.get("key") for x in opts]
    return None


def _is_autogrow(spec: Any) -> bool:
    return _spec_kind(spec) == AUTOGROW


def check_value(name: str, value: Any, spec: Any) -> None:
    """值域检查（枚举 / 整型范围 / 布尔）。不合法就抛 InvalidValueError。

    真机一次出片是花钱的，宁可在这里炸掉。
    """
    if not spec:
        return
    allowed = _allowed_values(spec)
    if allowed:
        if value not in allowed:
            raise A.InvalidValueError(f"{name}={value!r} 不在允许值里：{allowed}")
        return
    kind = _spec_kind(spec)
    opts = _spec_opts(spec)
    if kind == "INT":
        if isinstance(value, bool) or not isinstance(value, int):
            raise A.InvalidValueError(f"{name} 要整数，拿到 {value!r}")
        lo, hi = opts.get("min"), opts.get("max")
        if lo is not None and value < lo:
            raise A.InvalidValueError(f"{name}={value} 小于下限 {lo}")
        if hi is not None and value > hi:
            raise A.InvalidValueError(f"{name}={value} 大于上限 {hi}")
    elif kind == "BOOLEAN" and not isinstance(value, bool):
        raise A.InvalidValueError(f"{name} 要 true/false，拿到 {value!r}")


def model_param_specs(info: dict, model: str) -> dict[str, Any]:
    """所选模型的全部子输入（键为 `model.xxx` 的 API 名，含 autogrow 项）。"""
    return A.dynamic_sub_inputs(info, SEEDANCE_CLASS, "model", model)


def reference_limits(info: dict, model: str) -> dict[str, int]:
    """该模型能接几个参考图/视频/音频/素材（autogrow 模板里的 names 数量）。"""
    specs = model_param_specs(info, model)
    out: dict[str, int] = {}
    for field in AUTOGROW_FIELDS:
        tpl = _spec_opts(specs.get(field, [])).get("template") or {}
        out[field.split(".")[-1]] = len(tpl.get("names") or [])
    return out


def default_model(ui: dict) -> str | None:
    for node in ui.get("nodes") or []:
        if node.get("type") == SEEDANCE_CLASS:
            named = node.get("widgets_values_named") or {}
            if named.get("model"):
                return named["model"]
            w = node.get("widgets_values") or []
            return w[0] if w else None
    return None


def canned_prompt(ui: dict) -> str:
    """工作流自带的那条提示词（只当格式样本，不会当默认值用）。"""
    for node in ui.get("nodes") or []:
        if node.get("type") == SEEDANCE_CLASS:
            return (node.get("widgets_values_named") or {}).get("model.prompt") or ""
    return ""


# --------------------------------------------------------------------------
# 参考图 -> 图
# --------------------------------------------------------------------------
def inject_reference_images(api: dict, names: list[str]) -> dict:
    """把参考图名接进 `model.reference_images.image_1..N`。

    工作流里本来就有一个 LoadImage 接在 image_1 上，所以这里：够用就改写它的
    `image`，不够就补 LoadImage 节点，多了就把没接线的 LoadImage 删掉
    （否则那个节点会去加载服务器上并不存在的图片名）。
    """
    sid = A.find_node(api, SEEDANCE_CLASS)
    if sid is None:
        raise RuntimeError(f"图里没有 {SEEDANCE_CLASS}")
    loads = sorted((nid for nid, n in api.items() if n.get("class_type") == LOAD_CLASS),
                   key=_node_id_key)
    added: list[str] = []
    while len(loads) < len(names):
        nid = _next_id(api)
        api[nid] = {"class_type": LOAD_CLASS,
                    "inputs": {"image": "", "upload": "image"},
                    "_meta": {"title": LOAD_CLASS}}
        loads.append(nid)
        added.append(nid)
    dropped: list[str] = []
    for nid in loads[len(names):]:
        api.pop(nid, None)
        dropped.append(nid)
    wired: dict[str, list] = {}
    for i, name in enumerate(names):
        nid = loads[i]
        api[nid]["inputs"]["image"] = name
        wired[REF_TEMPLATE.format(i + 1)] = [nid, 0]
    for key in list(api[sid]["inputs"]):
        if key.startswith("model.reference_images."):
            api[sid]["inputs"].pop(key)
    api[sid]["inputs"].update(wired)
    return {"loads": loads[: len(names)], "added": added, "dropped": dropped,
            "wired": sorted(wired)}


def prune_orphan_loads(api: dict) -> list[str]:
    """删掉没被任何输入引用的 LoadImage（例如 apply_params 之后留下的空壳）。"""
    referenced = {str(v[0]) for n in api.values() for v in n["inputs"].values()
                  if isinstance(v, list) and v}
    gone = [nid for nid, n in list(api.items())
            if n.get("class_type") == LOAD_CLASS and nid not in referenced]
    for nid in gone:
        api.pop(nid, None)
    return gone


# --------------------------------------------------------------------------
# 参数落图 / 校验
# --------------------------------------------------------------------------
def apply_params(api: dict, params: dict[str, Any], info: dict, *,
                 strict: bool = True) -> tuple[dict, dict[str, Any]]:
    """把友好参数写进 API 图；对所选模型不存在的参数默认报错（静默丢弃会毁掉一轮实验）。

    返回 (新图, report)，report = {"applied": [...], "unapplied": {...}, "warnings": [...]}。
    """
    api = copy.deepcopy(api)
    report: dict[str, Any] = {"applied": [], "unapplied": {}, "warnings": []}
    sid = A.find_node(api, SEEDANCE_CLASS)
    if sid is None:
        raise RuntimeError(f"图里没有 {SEEDANCE_CLASS}")
    model = params.get("model") or api[sid]["inputs"].get("model")
    specs = model_param_specs(info, model)

    for name, value in params.items():
        if value is None:
            continue
        target = PARAM_TARGETS.get(name)
        if target is None:
            report["unapplied"][name] = value
            if strict:
                raise A.UnappliedOverrideError(
                    f"未知参数 {name!r}；可用：{sorted(PARAM_TARGETS)}")
            continue
        cls, field = target
        tid = A.find_node(api, cls)
        if tid is None:
            report["unapplied"][name] = value
            if strict:
                raise A.UnappliedOverrideError(f"{name}：图里没有 {cls} 节点")
            continue
        spec = specs.get(field) if field.startswith("model.") else None
        if field.startswith("model.") and field not in specs:
            report["unapplied"][name] = value
            if strict:
                raise A.UnappliedOverrideError(
                    f"{name}（{field}）对模型 {model!r} 不存在。"
                    f"该模型认的输入：{sorted(specs)}")
            continue
        check_value(name, value, spec)
        api[tid]["inputs"][field] = value
        report["applied"].append({"param": name, "field": field, "value": value})

    task = api[sid]["inputs"].get("model.task_type")
    if task in TASK_TYPES_NEEDING_VIDEO:
        report["warnings"].append(
            f"task_type={task!r} 通常要参考视频/被编辑的视频，而本工作流只接了参考图"
            f"（v1 只支持 --reference 图片）—— 大概率会失败或被云端忽略。")
    return api, report


def validate_graph(api: dict, info: dict, model: str) -> list[str]:
    """API 图是否能满足所选模型的必填输入（离线，不连服务器）。"""
    problems: list[str] = []
    sid = A.find_node(api, SEEDANCE_CLASS)
    if sid is None:
        return [f"缺少 {SEEDANCE_CLASS} 节点"]
    save = A.find_node(api, SAVE_CLASS)
    if save is None:
        problems.append(f"缺少 {SAVE_CLASS} 节点：找不到产物落点")
    inputs = api[sid]["inputs"]
    if not inputs.get("model"):
        problems.append("model 为空")
    elif inputs["model"] != model:
        problems.append(f"图里的 model={inputs['model']!r} 与请求的 {model!r} 不一致")

    specs = model_param_specs(info, model)
    if not specs:
        problems.append(f"schema 快照里没有模型 {model!r}（--list 看有哪些）")
    for field, spec in specs.items():
        if _is_autogrow(spec):
            continue
        if field not in inputs:
            problems.append(f"缺必填输入 {field}（模型 {model}）")
            continue
        try:
            check_value(field, inputs[field], spec)
        except A.InvalidValueError as exc:
            problems.append(str(exc))
    if not str(inputs.get("model.prompt") or "").strip():
        problems.append("model.prompt 为空：付费节点不给默认提示词")
    for field in ("seed", "watermark"):
        if field not in inputs:
            problems.append(f"缺 {field}")
    # 连线完整性
    for name, value in inputs.items():
        if isinstance(value, list) and value and str(value[0]) not in api:
            problems.append(f"{name} 指向的节点 {value[0]} 不在图里")
    return problems


# --------------------------------------------------------------------------
# 上传
# --------------------------------------------------------------------------
def upload_image(server: str, path: str, timeout: float = 300.0) -> str:
    """POST /upload/image，返回服务器 input 目录里的名字（可含 subfolder）。"""
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
        f"\r\n--{boundary}--\r\n".encode(),
    ]
    req = urllib.request.Request(f"{server.rstrip('/')}/upload/image",
                                 data=b"".join(parts))
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise A.InvalidValueError(
            f"上传 {path} 失败（HTTP {exc.code}）：{detail[:400]}") from exc
    sub = payload.get("subfolder") or ""
    return f"{sub}/{payload['name']}" if sub else payload["name"]


# --------------------------------------------------------------------------
# 留档
# --------------------------------------------------------------------------
def record_request(out_dir: str, prefix: str, server: str, params: dict, prompt_id: str,
                   graph: dict, files: list[str], key: dict, elapsed: float | None) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    api_name = f"{prefix}.api.json"
    with open(os.path.join(out_dir, api_name), "w", encoding="utf-8") as fh:
        json.dump(graph, fh, ensure_ascii=False, indent=2)
    prompt = str(params.get("prompt") or "")
    entry = {
        "time": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "engine": ENGINE, "server": server, "prompt_id": prompt_id, "prefix": prefix,
        "api_file": api_name, "files": files, "elapsed_s": round(elapsed, 1) if elapsed else None,
        # 提示词全文在 <prefix>.api.json 里；这里只记指纹，免得 requests.jsonl 被长文撑爆
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16] if prompt else None,
        "prompt_chars": len(prompt) if prompt else 0,
        # 只记"用没用凭据、走的哪条通道"，不记凭据本身
        "credential_channel": key.get("channel"), "credential_source": key.get("source"),
    }
    for k, v in params.items():
        if k not in ("prompt", "reference_blobs"):
            entry[k] = v
    with open(os.path.join(out_dir, "requests.jsonl"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


# --------------------------------------------------------------------------
# --check / --list
# --------------------------------------------------------------------------
def run_check(server: str, node_info: str = DEFAULT_NODE_INFO, api_key: str | None = None,
              key_file: str | None = None, auth_token: str | None = None) -> tuple[dict, int]:
    result: dict[str, Any] = {"server": server, "engine": ENGINE, "verified": False}
    health = G.check_server(server)
    result["reachable"] = health["reachable"]
    if not health["reachable"]:
        result["error"] = health["error"]
        result["hint"] = "服务器不可达：先确认 ComfyUI 已启动、--listen 已开、防火墙放通端口"
        return result, G.EXIT_UNREACHABLE
    result["comfyui_version"] = (health["stats"].get("system") or {}).get("comfyui_version")

    live_seed = G.fetch_node_info(server, SEEDANCE_CLASS)
    live_save = G.fetch_node_info(server, SAVE_CLASS)
    live_load = G.fetch_node_info(server, LOAD_CLASS)
    result["nodes"] = {SEEDANCE_CLASS: live_seed is not None, SAVE_CLASS: live_save is not None,
                       LOAD_CLASS: live_load is not None}
    if live_seed is None:
        result["hint"] = (f"服务器上没有 {SEEDANCE_CLASS}：ComfyUI 太旧，或启动参数带了 "
                          "--disable-partner-nodes / --offline")
        return result, G.EXIT_NO_NODE

    fixture = A.load_node_info(node_info)
    result["models"] = A.model_keys({"nodes": {SEEDANCE_CLASS: live_seed}}, SEEDANCE_CLASS)
    result["reference_limits"] = {m: reference_limits(fixture, m) for m in result["models"]}
    result["api_node"] = bool(live_seed.get("api_node"))
    result["paid"] = True
    result["model_files_needed"] = []          # 模型在云端：本机没有、也不需要权重
    result["schema_drift"] = A.diff_schema(
        fixture, {"nodes": {SEEDANCE_CLASS: live_seed, SAVE_CLASS: live_save or {},
                            LOAD_CLASS: live_load or {}}})
    if not any(result["schema_drift"].values()):
        result["schema_drift"] = "none"
    key = G.resolve_credential(api_key, key_file, auth_token)
    result["credential"] = {"present": key["present"], "channel": key["channel"],
                            "source": key["source"], "masked": key["masked"]}
    if not key["present"]:
        result["credential"]["hint"] = (
            "没有凭据：付费节点会在执行阶段报 Unauthorized。用 --api-key-file / "
            "$COMFYUI_API_KEY 给 ComfyUI 账号 API Key（脚本走 extra_data.api_key_comfy_org）。"
            "--check 只能证明图能过校验，证明不了能出片。")
    result["note"] = ("本技能交付时**未做任何验证**（无离线自检、无真机出片记录）："
                      "--check 通过只代表节点在、schema 对得上、凭据通道找得到。")
    result["next"] = ("python3 seedance_r2v.py --reference ref.png --prompt-file p.txt "
                      "--resolution 1080p --ratio 9:16 --duration 5 --plan")
    return result, G.EXIT_OK


def describe(info: dict, workflow: str) -> dict:
    ui = A.load_workflow(workflow)
    models = A.model_keys(info, SEEDANCE_CLASS)
    catalog = {}
    for m in models:
        subs = {}
        for field, spec in model_param_specs(info, m).items():
            entry: dict[str, Any] = {"type": _spec_kind(spec)}
            allowed = _allowed_values(spec)
            if allowed:
                entry["choices"] = allowed
            opts = _spec_opts(spec)
            for k in ("default", "min", "max", "step"):
                if k in opts:
                    entry[k] = opts[k]
            if _is_autogrow(spec):
                entry["autogrow"] = True
                entry["max_items"] = len((opts.get("template") or {}).get("names") or [])
            subs[field] = entry
        catalog[m] = subs
    return {
        "engine": ENGINE,
        "node": SEEDANCE_CLASS,
        "server_default": DEFAULT_SERVER,
        "workflow": os.path.relpath(workflow, HERE),
        "workflow_default_model": default_model(ui),
        "workflow_default_prompt_chars": len(canned_prompt(ui)),
        "models": models,
        "params_by_model": catalog,
        "friendly_params": {k: v[1] for k, v in PARAM_TARGETS.items()},
        "reference_images_only": True,
        "save": {k: _spec_kind(v) for k, v in
                 (A.node_schema(info, SAVE_CLASS)["input"]["required"] or {}).items()},
        "snapshot": {k: v for k, v in (info.get("_source") or {}).items()},
        "cost": "付费 partner 节点：按次计费，本技能不含价格表、也没有实测过（见 SKILL.md）",
        "verified": False,
    }


# --------------------------------------------------------------------------
# 生成
# --------------------------------------------------------------------------
def generate(
    server: str = DEFAULT_SERVER,
    workflow: str = DEFAULT_WORKFLOW,
    node_info: str = DEFAULT_NODE_INFO,
    prompt: str | None = None,
    model: str | None = None,
    resolution: str | None = None,
    ratio: str | None = None,
    duration: int | None = None,
    generate_audio: bool | None = None,
    task_type: str | None = None,
    output_format: str | None = None,
    auto_downscale: bool | None = None,
    auto_upscale: bool | None = None,
    seed: int | None = None,
    watermark: bool | None = None,
    references: list[str] | None = None,
    reference_names: list[str] | None = None,
    filename_prefix: str | None = None,
    video_format: str | None = None,
    set_pairs: list[str] | None = None,
    out_dir: str = "out",
    timeout: float = 3600.0,
    poll: float = 5.0,
    quiet: bool = False,
    record: bool = True,
    plan: bool = False,
    api_key: str | None = None,
    key_file: str | None = None,
    auth_token: str | None = None,
    allow_unapplied: bool = False,
) -> dict:
    """跑一次 Seedance 2.5 参考生视频，返回可 JSON 序列化的摘要。"""
    info = A.load_node_info(node_info)
    ui = A.load_workflow(workflow)
    api, save_id = A.build_api_graph(ui)
    if save_id is None:
        raise RuntimeError(f"工作流里没有 {SAVE_CLASS}；找不到产物落点")

    model = model or default_model(ui)
    if not model:
        raise A.InvalidValueError("没给 --model，工作流里也没有默认模型")
    if model not in A.model_keys(info, SEEDANCE_CLASS):
        raise A.UnknownModelError(
            f"模型 {model!r} 不在 schema 快照里：{A.model_keys(info, SEEDANCE_CLASS)}")

    ref_names = list(reference_names or [])
    ref_paths = list(references or [])
    if not ref_names and not ref_paths:
        raise A.InvalidValueError(
            "参考生视频至少要一张参考图：--reference <本地图> 或 --reference-name <服务器上已有图>。"
            "要纯文生视频请用 text-to-video-fastvideo3 或官方 t2v 模板。")
    limit = reference_limits(info, model).get("images")
    if limit is not None and len(ref_names) + len(ref_paths) > limit:
        raise A.InvalidValueError(
            f"{model} 最多接 {limit} 张参考图，这次给了 {len(ref_names) + len(ref_paths)} 张")

    params: dict[str, Any] = {
        "prompt": prompt, "model": model, "resolution": resolution, "ratio": ratio,
        "duration": duration, "generate_audio": generate_audio, "task_type": task_type,
        "output_format": output_format, "auto_downscale": auto_downscale,
        "auto_upscale": auto_upscale, "seed": seed, "watermark": watermark,
        "filename_prefix": filename_prefix,
    }
    if video_format:
        params["format"] = video_format
    api, report = apply_params(api, params, info, strict=not allow_unapplied)

    # --set CLASS.FIELD=VALUE 兜底（兄弟技能的同一个习惯）
    for pair in set_pairs or []:
        if "=" not in pair:
            raise A.InvalidValueError(f"--set 要写成 CLASS.FIELD=VALUE，收到 {pair!r}")
        left, value = pair.split("=", 1)
        cls, _, field = left.partition(".")
        nid = A.find_node(api, cls)
        if nid is None:
            raise A.UnappliedOverrideError(f"--set {pair}：图里没有 {cls}")
        try:
            parsed = json.loads(value)
        except ValueError:
            parsed = value
        api[nid]["inputs"][field] = parsed
        report["applied"].append({"param": f"set:{left}", "field": f"{cls}.{field}",
                                  "value": parsed})

    uploaded: list[str] = []
    if ref_paths:
        if plan:
            # 免费路径：不碰服务器、不上传，只报告"会传什么、接到哪"
            uploaded = [f"<plan:{os.path.basename(p)}>" for p in ref_paths]
        else:
            for path in ref_paths:
                uploaded.append(upload_image(server, path, timeout=min(timeout, 300.0)))
    names = ref_names + uploaded
    if names:
        wire = inject_reference_images(api, names)
    else:
        wire = {"loads": [], "added": [], "dropped": [], "wired": []}
    pruned = A.prune_ui_only(api)[1]
    orphan = prune_orphan_loads(api)

    problems = validate_graph(api, info, model)
    if problems:
        raise A.InvalidValueError("API 图校验不过：\n  - " + "\n  - ".join(problems))

    summary: dict[str, Any] = {
        "engine": ENGINE, "server": server, "model": model, "plan": plan,
        "output_node": save_id, "nodes": len(api), "references": names,
        "reference_wiring": wire, "dropped_ui_nodes": [d.get("class_type") for d in pruned],
        "dropped_orphan_loads": orphan, "applied": report["applied"],
        "unapplied_overrides": report["unapplied"], "warnings": report["warnings"],
        "predicted": {"resolution": api[A.find_node(api, SEEDANCE_CLASS)]["inputs"].get("model.resolution"),
                      "ratio": api[A.find_node(api, SEEDANCE_CLASS)]["inputs"].get("model.ratio"),
                      "duration": api[A.find_node(api, SEEDANCE_CLASS)]["inputs"].get("model.duration")},
        "paid": True, "verified": False,
        "graph": api,
    }
    if plan:
        summary["next"] = ("确认无误后去掉 --plan 真跑；**这一步是按次计费的**，"
                           "建议先用 --duration 4 最短档试一条。")
        return summary

    key = G.resolve_credential(api_key, key_file, auth_token)
    summary["credential"] = {"present": key["present"], "channel": key["channel"],
                             "source": key["source"], "masked": key["masked"]}
    started = time.time()
    prompt_id = G.queue_prompt(server, api, f"dsh-seedance-{os.getpid()}", key, timeout=120.0)
    if not quiet:
        print(f"-> seedance r2v @ {server}  model={model}  refs={len(names)}  "
              f"prompt_id={prompt_id}", flush=True)
    entry = G.wait_for_history(server, prompt_id, timeout=timeout, poll=poll, quiet=quiet)
    G.raise_for_status(entry, prompt_id)
    elapsed = time.time() - started

    files = G.collect_images(entry, only_node=save_id)
    local_paths = [G.download_image(server, item, out_dir, timeout=600.0) for item in files]
    # 留档名取 SaveVideo 前缀的基名（默认 video/Seedance2.5_r2v → Seedance2.5_r2v）
    raw_prefix = str(api[save_id]["inputs"].get("filename_prefix") or ENGINE)
    prefix = os.path.basename(raw_prefix.rstrip("/")) or ENGINE
    summary.update({"prompt_id": prompt_id, "status": (entry.get("status") or {}).get("status_str"),
                    "elapsed_s": round(elapsed, 1), "files": files,
                    "local_paths": local_paths})
    if not local_paths:
        summary["warnings"] = summary["warnings"] + [
            "这次没有下载到任何产物：检查 SaveVideo 的 filename_prefix 与 /history 的 outputs"]
    if record:
        summary["record"] = record_request(out_dir, prefix, server,
                                           {**{k: v for k, v in params.items() if v is not None},
                                            "references": names},
                                           prompt_id, api, local_paths, key, elapsed)
    return summary


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=DEFAULT_SERVER, help=f"ComfyUI 地址（默认 {DEFAULT_SERVER}）")
    ap.add_argument("--workflow", default=DEFAULT_WORKFLOW, help="UI 工作流 JSON")
    ap.add_argument("--node-info", default=DEFAULT_NODE_INFO, help="节点 schema 快照")
    ap.add_argument("--prompt", help="提示词（r2v 写法见 references/api-node.md）")
    ap.add_argument("--prompt-file", help="从文件读提示词（与 --prompt 二选一）")
    ap.add_argument("--model", help="模型键（默认取工作流里的：Seedance 2.5）")
    ap.add_argument("--resolution", help="分辨率：480p / 720p / 1080p（Seedance 2.0 另有 4k）")
    ap.add_argument("--ratio", help="画幅：16:9 / 4:3 / 1:1 / 3:4 / 9:16 / 21:9 / adaptive")
    ap.add_argument("--duration", type=int, help="时长秒数（Seedance 2.5：4–30）")
    ap.add_argument("--audio", dest="generate_audio", action="store_true", default=None,
                    help="生成同步音频（工作流默认开）")
    ap.add_argument("--no-audio", dest="generate_audio", action="store_false",
                    help="不要音频")
    ap.add_argument("--task-type", help="auto / reference / edit / extend（仅 Seedance 2.5 有）")
    ap.add_argument("--output-format", help="输出容器（模板里是 mp4）")
    ap.add_argument("--auto-downscale", dest="auto_downscale", action="store_true", default=None)
    ap.add_argument("--no-auto-downscale", dest="auto_downscale", action="store_false")
    ap.add_argument("--auto-upscale", dest="auto_upscale", action="store_true", default=None)
    ap.add_argument("--no-auto-upscale", dest="auto_upscale", action="store_false")
    ap.add_argument("--seed", type=int, help="种子（云端结果本身是非确定性的）")
    ap.add_argument("--watermark", dest="watermark", action="store_true", default=None)
    ap.add_argument("--no-watermark", dest="watermark", action="store_false")
    ap.add_argument("--reference", action="append", metavar="PATH",
                    help="参考图本地路径（可重复；会被上传）")
    ap.add_argument("--reference-name", action="append", metavar="NAME",
                    help="服务器 input 里已有的参考图名（可重复，免上传）")
    ap.add_argument("--filename-prefix", help='SaveVideo 前缀（默认 video/Seedance2.5_r2v）')
    ap.add_argument("--video-format", help="容器：auto / mp4 / mkv / webm（SaveVideo.format）")
    ap.add_argument("--set", dest="set_pairs", action="append", metavar="CLASS.FIELD=VALUE",
                    help="兜底：改任何 profile 没命名的字段（可重复）")
    ap.add_argument("--out-dir", default="out", help="产物与留档目录（默认 out）")
    ap.add_argument("--timeout", type=float, default=3600.0, help="等成品的最长秒数")
    ap.add_argument("--poll", type=float, default=5.0, help="轮询间隔秒")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-record", dest="record", action="store_false", default=True,
                    help="不写 <prefix>.api.json / requests.jsonl")
    ap.add_argument("--plan", action="store_true",
                    help="只验证参数真的落图（**不提交、不上传、不花钱**）")
    ap.add_argument("--api-key", help="ComfyUI 账号 API Key")
    ap.add_argument("--api-key-file", help="从文件读 API Key")
    ap.add_argument("--auth-token", help="OAuth Bearer token（会过期，次选）")
    ap.add_argument("--allow-unapplied", action="store_true",
                    help="允许参数没落图也不报错（默认报错）")
    ap.add_argument("--check", action="store_true", help="真机：节点 + schema 对账 + 凭据")
    ap.add_argument("--list", dest="list_params", action="store_true",
                    help="列出模型、参数、参考图上限（离线）")
    ap.add_argument("--show-default-prompt", action="store_true",
                    help="打印工作流自带的那条提示词样本")
    args = ap.parse_args(argv)

    def emit(payload: dict) -> None:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    try:
        if args.list_params:
            emit(describe(A.load_node_info(args.node_info), args.workflow))
            return G.EXIT_OK
        if args.show_default_prompt:
            text = canned_prompt(A.load_workflow(args.workflow))
            if not text:
                emit({"ok": False, "error": "工作流里没有自带提示词"})
                return G.EXIT_BAD_PARAMS
            print(text)
            return G.EXIT_OK
        if args.check:
            result, code = run_check(args.server, args.node_info, args.api_key,
                                     args.api_key_file, args.auth_token)
            emit(result)
            return code

        prompt = args.prompt
        if args.prompt_file:
            with open(args.prompt_file, encoding="utf-8") as fh:
                prompt = fh.read()
        if not prompt or not prompt.strip():
            emit({"ok": False,
                  "error": "--prompt / --prompt-file 必填（付费节点不给默认提示词；"
                           "工作流里那条只是样本，可看 --show-default-prompt）"})
            return G.EXIT_BAD_PARAMS

        summary = generate(
            server=args.server, workflow=args.workflow, node_info=args.node_info,
            prompt=prompt, model=args.model, resolution=args.resolution, ratio=args.ratio,
            duration=args.duration, generate_audio=args.generate_audio,
            task_type=args.task_type, output_format=args.output_format,
            auto_downscale=args.auto_downscale, auto_upscale=args.auto_upscale,
            seed=args.seed, watermark=args.watermark, references=args.reference,
            reference_names=args.reference_name, filename_prefix=args.filename_prefix,
            video_format=args.video_format, set_pairs=args.set_pairs, out_dir=args.out_dir,
            timeout=args.timeout, poll=args.poll, quiet=args.quiet, record=args.record,
            plan=args.plan, api_key=args.api_key, key_file=args.api_key_file,
            auth_token=args.auth_token, allow_unapplied=args.allow_unapplied)
        emit(summary)
        return G.EXIT_OK if (summary.get("local_paths") or args.plan) else G.EXIT_NO_IMAGE
    except A.UnappliedOverrideError as exc:
        emit({"ok": False, "error": str(exc), "kind": "unapplied"})
        return G.EXIT_BAD_PARAMS
    except (A.UnknownModelError, A.InvalidValueError, ValueError) as exc:
        emit({"ok": False, "error": str(exc), "kind": "bad_params"})
        return G.EXIT_BAD_PARAMS
    except G.AuthError as exc:
        emit({"ok": False, "error": str(exc), "kind": "auth"})
        return G.EXIT_AUTH
    except G.RejectedError as exc:
        emit({"ok": False, "error": str(exc), "kind": "rejected"})
        return G.EXIT_REJECTED
    except G.NodeError as exc:
        emit({"ok": False, "error": str(exc), "kind": "node_error"})
        return G.EXIT_NODE_ERROR
    except TimeoutError as exc:
        emit({"ok": False, "error": str(exc), "kind": "timeout"})
        return G.EXIT_TIMEOUT
    except KeyboardInterrupt:
        return G.EXIT_BAD_PARAMS


if __name__ == "__main__":
    sys.exit(main())
