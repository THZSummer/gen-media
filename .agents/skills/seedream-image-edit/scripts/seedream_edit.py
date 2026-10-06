#!/usr/bin/env python3
"""把 Seedream 图片编辑工作流提交到 ComfyUI，轮询 /history，下载成品。

与姊妹技能 `seedream-text-to-image` 的关系：**同一个付费 partner 节点**
（`ByteDanceSeedreamNodeV3`），推理同样在 ByteDance 云端、按张计费、本机零权重。
本技能补的是"给参考图"那一半：底图（+ 可选标注）上传 → 接进 `model.images.image_N`
→ 按提示词改图。凭据、schema、排队、留档全部复用姊妹技能的引擎（见 `_shared.py`），
这里只多三件事：**上传**参考图、**改造**图（参考图接线 / 删前端节点）、**按底图比例**
挑尺寸预设。

Examples:
  python3 seedream_edit.py --check
  python3 seedream_edit.py --list
  python3 seedream_edit.py --image base.png --prompt "女主换成男主" --dry-run
  python3 seedream_edit.py --image base.png --prompt "背景换成纯白" --seed 7 --out-dir out/
  python3 seedream_edit.py --image a.png --image b.png --prompt "把两张图里的动物并排画在一起" \\
      --size "(2K) 2048x2048 (1:1)" --api-key-file ../../../work/comfy_api_key
  python3 seedream_edit.py --image base.png --annotate marks.png --prompt "把红框区域改成纯黑"
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared  # noqa: E402

_shared.ensure()
import seedream_api as A  # noqa: E402
import seedream_gen as G  # noqa: E402
from seedream_edit_graph import (  # noqa: E402
    HEADLESS_DROP, auto_size, build_edit_graph, default_model, image_size, max_refs,
    supports_thinking,
)

DEFAULT_WORKFLOW = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets",
                 "seedream-5.0-pro-image-edit-ui.json"))
DEFAULT_NODE_INFO = A.DEFAULT_NODE_INFO  # 与姊妹技能共用同一份 schema 快照
DEFAULT_PREFIX = "seedream-edit"
SERVER = G.DEFAULT_SERVER

EXIT_OK = G.EXIT_OK
EXIT_NO_IMAGE = G.EXIT_NO_IMAGE
EXIT_UNREACHABLE = G.EXIT_UNREACHABLE
EXIT_NO_NODE = G.EXIT_NO_NODE
EXIT_AUTH = G.EXIT_AUTH
EXIT_REJECTED = G.EXIT_REJECTED
EXIT_NODE_ERROR = G.EXIT_NODE_ERROR
EXIT_TIMEOUT = G.EXIT_TIMEOUT
EXIT_BAD_PARAMS = G.EXIT_BAD_PARAMS

SEEDREAM_CLASS = A.SEEDREAM_CLASS


# --------------------------------------------------------------------------
# 上传
# --------------------------------------------------------------------------
def upload_image(server: str, path: str, timeout: float = 300.0) -> str:
    """POST 到 /upload/image，返回服务器 input 目录里的文件名（Painter 也吃这个名字）。"""
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
    body = b"".join(parts)
    req = G.urllib.request.Request(f"{server.rstrip('/')}/upload/image", data=body)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with G.urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except G.urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise A.InvalidValueError(
            f"上传 {path} 失败（HTTP {exc.code}）：{detail[:400]}") from exc
    sub = payload.get("subfolder") or ""
    return f"{sub}/{payload['name']}" if sub else payload["name"]


def download_composite(server: str, img: dict, out_dir: str, prefix: str) -> str:
    """下载 Painter 的合成结果并改个可读的名字（/view 的 filename 必须用服务器原名）。"""
    raw = G.download_image(server, img, out_dir)
    dest = os.path.join(out_dir, f"{prefix}-composite-{os.path.basename(raw)}")
    os.replace(raw, dest)
    return dest


# --------------------------------------------------------------------------
# 出图
# --------------------------------------------------------------------------
def generate(
    server: str = SERVER,
    workflow: str = DEFAULT_WORKFLOW,
    node_info: str = DEFAULT_NODE_INFO,
    images: list[str] | None = None,
    annotate: str | None = None,
    prompt: str | None = None,
    model: str | None = None,
    size: str | None = None,
    tier: str | None = None,
    width: int | None = None,
    height: int | None = None,
    seed: int | None = None,
    thinking: bool | None = None,
    watermark: bool | None = None,
    prompt_optimization: str | None = None,
    max_images: int | None = None,
    fail_on_partial: bool | None = None,
    filename_prefix: str | None = None,
    image_format: str | None = None,
    out_dir: str = "out",
    timeout: float = 900.0,
    poll: float = 3.0,
    quiet: bool = False,
    record: bool = True,
    dry_run: bool = False,
    keep_preview: bool = False,
    api_key: str | None = None,
    key_file: str | None = None,
    auth_token: str | None = None,
    allow_unapplied: bool = False,
) -> dict:
    """跑一次 Seedream 图片编辑，返回可 JSON 序列化的摘要。"""
    info = A.load_node_info(node_info)
    ui = A.load_workflow(workflow)
    prefix = filename_prefix or DEFAULT_PREFIX
    images = list(images or [])
    if not images:
        raise A.InvalidValueError(
            "至少要给一张参考图（--image）。纯文生图请用姊妹技能 seedream-text-to-image")
    for path in images + ([annotate] if annotate else []):
        if not os.path.isfile(path):
            raise A.InvalidValueError(f"找不到图片：{path}")

    # 模型先定下来：参考图上限、thinking 支持与否都跟它有关
    model_key = str(model or default_model(ui) or "")
    if model_key not in A.model_keys(info):
        raise A.UnknownModelError(
            f"未知模型 {model_key!r}；这台服务器上可用的模型：\n  "
            + "\n  ".join(A.model_keys(info)))
    limit = max_refs(info, model_key)
    if limit is not None and len(images) > limit:
        raise A.InvalidValueError(
            f"{model_key} 最多收 {limit} 张参考图，这次给了 {len(images)} 张")

    # 尺寸：默认 auto = 按第 1 张底图的比例挑预设；也可以给预设原文 / 1024x1024 / 1:1
    size_note: dict[str, Any] = {}
    if size is None or str(size).strip().lower() == "auto":
        ref_w, ref_h = image_size(images[0])
        auto = auto_size(info, model_key, ref_w, ref_h, tier)
        size = auto["preset"]
        size_note = {"size_mode": "auto", **auto}
    elif str(size).strip() == "Custom":
        if width is None or height is None:
            raise A.InvalidValueError("--size Custom 需要同时给 --width 和 --height")
        size = f"{width}x{height}"
    elif width is not None or height is not None:
        if width is None or height is None:
            raise A.InvalidValueError("--width/--height 要成对给（或直接用 --size 1024x1024）")
        size = f"{width}x{height}"

    if not quiet:
        print(f"-> {server}  参考图 {len(images)} 张  model={model_key!r} size={size!r}"
              + (f"（{size_note['size_mode']}：底图 {size_note['ref_size'][0]}x"
                 f"{size_note['ref_size'][1]} 比例 {size_note['want_aspect']} → "
                 f"{size_note['tier']} 档）" if size_note else ""), flush=True)

    # 有参考图时 thinking 不能关（服务器原话见 references/api-node.md §3）；本地先拦
    if thinking is False and supports_thinking(info, model_key):
        raise A.InvalidValueError(
            "有参考图时 thinking 不能关：服务器会拒（\"'thinking' can only be disabled "
            "for text-to-image; enable it when using reference images.\"）；"
            "要去掉 --no-thinking，纯文生图才允许关")

    # 上传：参考图 + 标注层（--dry-run 不上传，用本地文件名占位，只看接线与参数）
    ref_names: list[str] = []
    annotate_name = None
    if dry_run:
        ref_names = [os.path.basename(path) for path in images]
        annotate_name = os.path.basename(annotate) if annotate else None
    else:
        for path in images:
            ref_names.append(upload_image(server, path))
            if not quiet:
                print(f"   uploaded: {path} -> {ref_names[-1]}", flush=True)
        if annotate:
            annotate_name = upload_image(server, annotate)
            if not quiet:
                print(f"   uploaded: {annotate} -> {annotate_name}"
                      "（Painter 会按 alpha 合成到底图）", flush=True)

    base_size = image_size(images[0])
    api, save_id, meta = build_edit_graph(ui, ref_names, annotate_name, base_size=base_size,
                                          drop_preview=not keep_preview)
    seed_id = meta["seed_node"]
    if save_id is None:
        raise RuntimeError("工作流里没有 SaveImageAdvanced；找不到产物")
    if meta["dropped"] and not quiet:
        print("   剔除的界面节点：" + "；".join(
            f"{d['class']}(#{d['id']}) {d['why']}" for d in meta["dropped"]), flush=True)

    api, report = A.apply_params(api, {
        "prompt": prompt, "model": model, "size": size, "seed": seed, "thinking": thinking,
        "watermark": watermark, "prompt_optimization": prompt_optimization,
        "max_images": max_images, "fail_on_partial": fail_on_partial,
        "filename_prefix": prefix, "format": image_format,
    }, info, strict=not allow_unapplied)

    ref_keys = [k for k in api[seed_id]["inputs"] if k.startswith("model.images.")]
    problems = A.validate_graph(api, info)
    if problems:
        raise RuntimeError("本地 schema 校验没过（这张图不该发出去）：\n  - "
                           + "\n  - ".join(problems))

    if dry_run:
        return {"dry_run": True, "api": api, "save_node": save_id, "meta": meta,
                "ref_keys": sorted(ref_keys), "applied": report["applied"],
                "unapplied": report["unapplied"], **size_note}
    key = G.resolve_credential(api_key, key_file, auth_token)
    if not key["present"] and not quiet:
        print("!! 没有凭据（--api-key / --api-key-file / $COMFYUI_API_KEY / --auth-token）；"
              "付费节点通常会被拒。继续试一次。", file=sys.stderr, flush=True)

    prompt_id = G.queue_prompt(server, api, f"dsh-seedream-edit-{os.getpid()}", key)
    if not quiet:
        print(f"   queued: {prompt_id}", flush=True)
    entry = G.wait_for_history(server, prompt_id, timeout=timeout, poll=poll, quiet=quiet)
    G.raise_for_status(entry, prompt_id)

    local_paths: list[str] = []
    for img in G.collect_images(entry, only_node=save_id):
        if img.get("filename"):
            local_paths.append(G.download_image(server, img, out_dir))
    # 标注层的合成结果：Painter 是中间节点，但它的输出也在 /history 里 —— 正好当"标注真的
    # 进了图"的证据留档（只有 --annotate 时才有）
    composite: list[str] = []
    if meta.get("composite_node"):
        for img in G.collect_images(entry, only_node=meta["composite_node"]):
            if img.get("filename"):
                composite.append(download_composite(server, img, out_dir, prefix))
    if not quiet:
        for path in local_paths + composite:
            print(f"   saved: {path} ({os.path.getsize(path)} bytes)", flush=True)

    params = {"prompt": prompt, "model": model_key,
              "size": api[seed_id]["inputs"].get("model.size_preset"),
              "custom_width": api[seed_id]["inputs"].get("model.width"),
              "custom_height": api[seed_id]["inputs"].get("model.height"),
              "seed": api[seed_id]["inputs"].get("model.seed"),
              "thinking": api[seed_id]["inputs"].get("model.thinking"),
              "watermark": api[seed_id]["inputs"].get("model.watermark"),
              "ref_keys": sorted(ref_keys), "local_refs": images,
              "server_refs": ref_names, "annotate": annotate, "annotate_server": annotate_name,
              "composite": composite, **size_note,
              "workflow": os.path.basename(workflow),
              "applied": report["applied"], "unapplied": report["unapplied"]}
    if record:
        G.record_request(out_dir, prefix, server, params, prompt_id, api,
                         local_paths + composite, key)
    return {"prompt_id": prompt_id, "images": G.collect_images(entry, only_node=save_id),
            "local_paths": local_paths, "composite_paths": composite, "model": model_key,
            "credential_channel": key.get("channel"), "cached_nodes": G.cached_nodes(entry),
            "ref_keys": sorted(ref_keys), "annotate_node": meta.get("annotate_node"),
            "dropped": meta["dropped"], **size_note,
            "status": (entry.get("status") or {}).get("status_str"),
            "applied": report["applied"], "unapplied": report["unapplied"]}


# --------------------------------------------------------------------------
# 自检 / 清单
# --------------------------------------------------------------------------
def run_check(server: str, node_info: str = DEFAULT_NODE_INFO, api_key: str | None = None,
              key_file: str | None = None, auth_token: str | None = None) -> tuple[dict, int]:
    result: dict[str, Any] = {"server": server}
    health = G.check_server(server)
    result["reachable"] = health["reachable"]
    if not health["reachable"]:
        result["error"] = health["error"]
        result["hint"] = "服务器不可达：先确认 ComfyUI Desktop 已启动、--listen 已开、防火墙放通端口"
        return result, EXIT_UNREACHABLE
    result["comfyui_version"] = (health["stats"].get("system") or {}).get("comfyui_version")

    # 编辑图要用到的每个节点都问一遍真机（不下载整份 /object_info）
    needed = [SEEDREAM_CLASS, A.SAVE_CLASS, "LoadImage", "Painter"]
    result["nodes"] = {cls: G.fetch_node_info(server, cls) is not None for cls in needed}
    if not result["nodes"][SEEDREAM_CLASS]:
        result["hint"] = (f"服务器上没有 {SEEDREAM_CLASS}：ComfyUI 太旧，或启动参数带了 "
                          "--disable-partner-nodes / --offline")
        return result, EXIT_NO_NODE
    if not result["nodes"]["LoadImage"]:
        result["hint"] = "服务器上没有 LoadImage：工作流没法读底图"
        return result, EXIT_NO_NODE
    result["painter_note"] = ("Painter 在位，--annotate 可用" if result["nodes"]["Painter"]
                              else "没有 Painter：只能用 --image（不标注）")

    fixture = A.load_node_info(node_info)
    live_seed = G.fetch_node_info(server, SEEDREAM_CLASS)
    live_save = G.fetch_node_info(server, A.SAVE_CLASS)
    result["models"] = A.model_keys({"nodes": {SEEDREAM_CLASS: live_seed}})
    result["max_refs"] = {m: max_refs({"nodes": {SEEDREAM_CLASS: live_seed}}, m)
                          for m in result["models"]}
    result["api_node"] = bool(live_seed.get("api_node"))
    result["paid"] = True
    result["schema_drift"] = A.diff_schema(
        fixture, {"nodes": {SEEDREAM_CLASS: live_seed, A.SAVE_CLASS: live_save or {}}})
    if not any(result["schema_drift"].values()):
        result["schema_drift"] = "none"
    result["model_files_needed"] = []  # 模型在云端：本机没有、也不需要权重

    # 工作流里的节点类是不是都能在真机上跑（前端专有节点会被剔除，这里只报事实）
    api, _save, meta = build_edit_graph(A.load_workflow(DEFAULT_WORKFLOW), ["<check>"],
                                        "<check>" if result["nodes"]["Painter"] else None)
    result["workflow_classes"] = sorted({n["class_type"] for n in api.values()})
    result["headless_dropped"] = sorted({d["class"] for d in meta["dropped"]})
    result["headless_drop_note"] = (
        "这些是界面上有、服务器上没有的节点（" + "、".join(HEADLESS_DROP) +
        " 是无头不需要的预览节点），提交前已剔除")

    key = G.resolve_credential(api_key, key_file, auth_token)
    result["credential"] = {"present": key["present"], "channel": key["channel"],
                            "source": key["source"], "masked": key["masked"]}
    if not key["present"]:
        result["credential"]["hint"] = (
            "没有凭据：付费节点会在执行阶段报 Unauthorized（用 --api-key-file 或 "
            "$COMFYUI_API_KEY 给 ComfyUI 账号 API Key）。--check 不花钱，也证明不了能出图。")
    result["next"] = ("python3 seedream_edit.py --image <底图> --prompt-file <prompt.txt> "
                      "--out-dir out/")
    return result, EXIT_OK


def describe(info: dict) -> dict:
    base = A.describe(info)
    models = {}
    for key in A.model_keys(info):
        models[key] = {**base["models"][key], "max_refs": max_refs(info, key),
                       "thinking_switchable": supports_thinking(info, key)}
    return {
        "models": models,
        "save": base["save"],
        "_sizes_note": ("默认 --size auto：按第 1 张底图的比例挑同档里最小的预设；"
                        "也接受预设原文 / 1024x1024 / 1:1 / Custom+--width/--height"),
        "_ref_note": ("参考图按顺序接进 model.images.image_1 / image_2 …；"
                      "第 1 张是底图（--annotate 时先被 Painter 合成标注层）"),
        "_thinking_note": "有参考图时 thinking 不能关（服务器会拒）；纯文生图才能关",
        "_t2i_note": "纯文生图用姊妹技能 seedream-text-to-image/scripts/seedream_gen.py",
    }


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=SERVER, help=f"ComfyUI 地址（默认 {SERVER}）")
    ap.add_argument("--workflow", default=DEFAULT_WORKFLOW, help="UI 工作流 JSON")
    ap.add_argument("--node-info", default=DEFAULT_NODE_INFO, help="节点 schema 快照")
    ap.add_argument("--image", action="append", dest="images", metavar="PATH",
                    help="参考图（可重复；第 1 张是底图）")
    ap.add_argument("--annotate", metavar="PATH",
                    help="RGBA 标注层（alpha = 笔迹）：Painter 会按 alpha 合成到底图上再送去编辑")
    ap.add_argument("--prompt", help="编辑指令")
    ap.add_argument("--prompt-file", help="从文件读编辑指令（与 --prompt 二选一）")
    ap.add_argument("--model", help="模型键（默认取工作流里的 seedream 5.0 pro）")
    ap.add_argument("--size", help="auto（默认，按底图比例）/ 预设原文 / 1024x1024 / 1:1 / Custom")
    ap.add_argument("--size-tier", dest="tier", help="--size auto 用哪一档（1K / 1.5K / 2K / 3K / 4K）")
    ap.add_argument("--width", type=int, help="仅 --size Custom 时有意义")
    ap.add_argument("--height", type=int)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--thinking", dest="thinking", action="store_true", default=None,
                    help="开 thinking（有参考图时**必须**开，这是默认）")
    ap.add_argument("--no-thinking", dest="thinking", action="store_false",
                    help="关 thinking —— 有参考图时会被本地拦住（服务器也会拒）")
    ap.add_argument("--watermark", dest="watermark", action="store_true", default=None,
                    help='加 "AI generated" 水印')
    ap.add_argument("--no-watermark", dest="watermark", action="store_false")
    ap.add_argument("--prompt-optimization", choices=["standard", "fast"],
                    help="仅 seedream 5.0 pro 有（给参考图时才有意义）")
    ap.add_argument("--max-images", type=int, help="仅 lite/4.5/4.0：一次要几张关联图")
    ap.add_argument("--fail-on-partial", dest="fail_on_partial", action="store_true",
                    default=None, help="缺图即失败（仅 lite/4.5/4.0）")
    ap.add_argument("--no-fail-on-partial", dest="fail_on_partial", action="store_false")
    ap.add_argument("--filename-prefix", help=f"输出前缀（也是留档名，默认 {DEFAULT_PREFIX}）")
    ap.add_argument("--format", dest="image_format", help="保存格式（png / jpeg / webp / exr…）")
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--timeout", type=float, default=900.0,
                    help="等待秒数（有参考图时 thinking 强制开，pro 可能几分钟）")
    ap.add_argument("--poll", type=float, default=3.0)
    ap.add_argument("--keep-preview", action="store_true",
                    help="保留工作流里的 PreviewImage（默认剔除：无头没人看，还多存一张临时图）")
    ap.add_argument("--api-key", help="ComfyUI 账号 API Key（也可用 $COMFYUI_API_KEY）")
    ap.add_argument("--api-key-file", help="从文件读 API Key（首行/整文件）")
    ap.add_argument("--auth-token", help="改用浏览器登录态 Bearer token 通道（会过期，一般不推荐）")
    ap.add_argument("--allow-unapplied", action="store_true",
                    help="参数对所选模型不存在时不报错（默认报错）")
    ap.add_argument("--dry-run", action="store_true", help="只打印 API 图，不提交（不上传参考图）")
    ap.add_argument("--no-record", dest="record", action="store_false",
                    help="不写 <prefix>.api.json / requests.jsonl")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--check", action="store_true", help="探活 + 节点 + schema 对账 + 凭据（不花钱）")
    ap.add_argument("--list", action="store_true", help="列出模型、参数、尺寸与参考图上限")
    args = ap.parse_args(argv)

    if args.check:
        result, code = run_check(args.server, args.node_info, args.api_key, args.api_key_file,
                                 args.auth_token)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return code
    if args.list:
        print(json.dumps(describe(A.load_node_info(args.node_info)), ensure_ascii=False, indent=2))
        return EXIT_OK

    prompt = args.prompt
    if args.prompt_file:
        with open(args.prompt_file, encoding="utf-8") as fh:
            prompt = fh.read().strip()
    if not args.images:
        ap.error("--image 必须至少给一张（--check / --list 除外）")
    if not prompt:
        ap.error("--prompt 或 --prompt-file 必须给一个（--check / --list 除外）")

    try:
        result = generate(
            server=args.server, workflow=args.workflow, node_info=args.node_info,
            images=args.images, annotate=args.annotate, prompt=prompt, model=args.model,
            size=args.size, tier=args.tier, width=args.width, height=args.height,
            seed=args.seed, thinking=args.thinking, watermark=args.watermark,
            prompt_optimization=args.prompt_optimization, max_images=args.max_images,
            fail_on_partial=args.fail_on_partial, filename_prefix=args.filename_prefix,
            image_format=args.image_format, out_dir=args.out_dir, timeout=args.timeout,
            poll=args.poll, quiet=args.quiet, record=args.record,
            dry_run=args.dry_run, keep_preview=args.keep_preview,
            api_key=args.api_key, key_file=args.api_key_file, auth_token=args.auth_token,
            allow_unapplied=args.allow_unapplied,
        )
    except (A.UnappliedOverrideError, A.UnknownModelError, A.InvalidValueError, ValueError) as exc:
        print(f"参数不成立：{exc}", file=sys.stderr)
        return EXIT_BAD_PARAMS
    except G.RejectedError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_REJECTED
    except G.AuthError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_AUTH
    except G.NodeError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_NODE_ERROR
    except TimeoutError as exc:
        print(f"{exc}（付费任务可能仍在跑；调大 --timeout 或去 ComfyUI 队列里看）", file=sys.stderr)
        return EXIT_TIMEOUT
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_BAD_PARAMS

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("dry_run"):
        return EXIT_OK
    return EXIT_OK if result["local_paths"] else EXIT_NO_IMAGE


if __name__ == "__main__":
    sys.exit(main())
