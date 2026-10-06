#!/usr/bin/env python3
"""把 ByteDance Seedream 文生图工作流提交到 ComfyUI，轮询 /history，下载成品。

与 `text-to-image-comfyui` 的根本区别：**模型不在本机**。这份工作流用的是 ComfyUI 的付费
partner 节点 `ByteDanceSeedreamNodeV3`，推理在 ByteDance 云端、按张计费，本机既没有权重、
也没有 `models/` 里那份文件可查。于是三件事变了：

  * `--check` 不再查模型文件，改查"节点在不在 + 模型列表 + schema 有没有漂移 + 凭据有没有"；
  * 提交要给凭据：`POST /prompt` 的 `extra_data.api_key_comfy_org`（ComfyUI 账号 API Key）；
  * 出图有成本、耗时按秒~分钟计，所以默认先 `--dry-run` 看逐字 API 图，再真出。

Examples:
  python3 seedream_gen.py --check
  python3 seedream_gen.py --list
  python3 seedream_gen.py --prompt "九尾狐 素描 线稿" --dry-run
  python3 seedream_gen.py --prompt "九尾狐 素描 线稿" --seed 42 --out-dir out/
  python3 seedream_gen.py --prompt-file p.txt --size 1440x2560 --model "seedream 5.0 lite" \\
      --api-key-file ../../../work/comfy_api_key --out-dir out/
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedream_api import (  # noqa: E402
    DEFAULT_NODE_INFO, DEFAULT_WORKFLOW, SAVE_CLASS, SEEDREAM_CLASS,
    InvalidValueError, UnappliedOverrideError, UnknownModelError, apply_params,
    build_api_graph, describe, diff_schema, load_node_info, load_workflow, model_keys,
    validate_graph,
)

DEFAULT_SERVER = os.environ.get("COMFYUI_SERVER", "http://192.168.3.5:18000")
KEY_ENV_VARS = ("COMFYUI_API_KEY", "COMFY_API_KEY")
KEY_FILE_ENV = "COMFYUI_API_KEY_FILE"
# 第二个通道：浏览器/OAuth 登录态的 Bearer token（ComfyUI 的 hidden.auth_token_comfy_org）。
# 桌面端界面点 Run 走的就是它 —— 所以"界面能出图"不代表无头能出图。
TOKEN_ENV_VARS = ("COMFYUI_AUTH_TOKEN", "COMFY_AUTH_TOKEN")
# extra_data 里两个通道的键名，取自 ComfyUI comfy_api_nodes/util/_helpers.py
CHANNEL_FIELDS = {"api_key": "api_key_comfy_org", "auth_token": "auth_token_comfy_org"}
ENGINE = "seedream"

EXIT_OK, EXIT_NO_IMAGE, EXIT_UNREACHABLE, EXIT_NO_NODE = 0, 1, 2, 3
EXIT_AUTH, EXIT_REJECTED, EXIT_NODE_ERROR, EXIT_TIMEOUT, EXIT_BAD_PARAMS = 4, 5, 6, 7, 8


class AuthError(RuntimeError):
    """付费节点要求 ComfyUI 账号凭据，而这次请求没有（或无效）。"""


class NodeError(RuntimeError):
    """节点执行报错（非鉴权类）。"""


class RejectedError(RuntimeError):
    """服务器在 /prompt 阶段就拒了这张 API 图。"""


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------
def _request(url: str, data: bytes | None = None, timeout: float = 30.0) -> bytes:
    req = urllib.request.Request(url, data=data)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _get_json(url: str, timeout: float = 30.0) -> Any:
    return json.loads(_request(url, timeout=timeout).decode("utf-8"))


def check_server(server: str, timeout: float = 10.0) -> dict:
    out: dict[str, Any] = {"reachable": False, "stats": None, "error": None}
    try:
        out["stats"] = _get_json(f"{server.rstrip('/')}/system_stats", timeout=timeout)
        out["reachable"] = True
    except Exception as exc:  # noqa: BLE001 - 原样报给用户
        out["error"] = f"{type(exc).__name__}: {exc}"
    return out


def fetch_node_info(server: str, cls: str, timeout: float = 15.0) -> dict | None:
    try:
        payload = _get_json(f"{server.rstrip('/')}/object_info/{urllib.parse.quote(cls)}",
                            timeout=timeout)
    except Exception:  # noqa: BLE001 - 探活失败按"没有这个节点"处理
        return None
    return payload.get(cls) if isinstance(payload, dict) else None


# --------------------------------------------------------------------------
# 凭据
# --------------------------------------------------------------------------
def resolve_credential(api_key: str | None = None, key_file: str | None = None,
                       auth_token: str | None = None) -> dict:
    """按 --api-key > --api-key-file > $COMFYUI_API_KEY_FILE > $COMFYUI_API_KEY/$COMFY_API_KEY
    > --auth-token > $COMFYUI_AUTH_TOKEN 找凭据。

    两个通道对应 ComfyUI 的两种登录方式（见 references/api-node.md §2）：
      * `api_key`    -> `extra_data.api_key_comfy_org`（Comfy 账号 API Key，推荐）
      * `auth_token` -> `extra_data.auth_token_comfy_org`（浏览器/OAuth 的 Bearer token，会过期）

    只回报来源和掩码，**绝不把凭据写进留档或日志**。
    """
    out: dict[str, Any] = {"present": False, "channel": None, "source": None,
                           "masked": None, "value": None}
    value = source = None
    if api_key:
        value, source = api_key.strip(), "cli:--api-key"
    if value is None:
        path = key_file or os.environ.get(KEY_FILE_ENV)
        if path:
            with open(os.path.expanduser(path), encoding="utf-8") as fh:
                value, source = fh.read().strip(), f"file:{path}"
    channel = "api_key" if value else None
    if value is None:
        for var in KEY_ENV_VARS:
            if os.environ.get(var):
                value, source, channel = os.environ[var].strip(), f"env:{var}", "api_key"
                break
    if value is None:
        if auth_token:
            value, source, channel = auth_token.strip(), "cli:--auth-token", "auth_token"
        else:
            for var in TOKEN_ENV_VARS:
                if os.environ.get(var):
                    value, source, channel = os.environ[var].strip(), f"env:{var}", "auth_token"
                    break
    if value:
        out.update(present=True, channel=channel, source=source, value=value,
                   masked=value[:10] + "…" + f"（{len(value)} 字符）")
    return out


# --------------------------------------------------------------------------
# 提交 / 轮询 / 下载
# --------------------------------------------------------------------------
def queue_prompt(server: str, api_prompt: dict, client_id: str,
                 credential: dict | None = None, timeout: float = 60.0) -> str:
    payload: dict[str, Any] = {"prompt": api_prompt, "client_id": client_id}
    if credential and credential.get("present"):
        # 无头/自建前端调用付费节点的官方通道（二选一，见 resolve_credential）
        payload["extra_data"] = {CHANNEL_FIELDS[credential["channel"]]: credential["value"]}
    body = json.dumps(payload).encode("utf-8")
    try:
        raw = _request(f"{server.rstrip('/')}/prompt", data=body, timeout=timeout)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise RejectedError(f"服务器拒绝这张 API 图（HTTP {exc.code}）：{detail}") from exc
    data = json.loads(raw.decode("utf-8"))
    if "prompt_id" not in data:
        raise RejectedError(f"/prompt 返回异常：{data}")
    return data["prompt_id"]


def wait_for_history(server: str, prompt_id: str, timeout: float = 900.0, poll: float = 3.0,
                     quiet: bool = False) -> dict:
    url = f"{server.rstrip('/')}/history/{urllib.parse.quote(prompt_id)}"
    deadline = time.time() + timeout
    last_note = 0.0
    while True:
        payload = _get_json(url, timeout=30.0)
        if prompt_id in payload:
            return payload[prompt_id]
        if time.time() > deadline:
            raise TimeoutError(f"prompt {prompt_id} 在 {timeout:.0f}s 内没有结束")
        if not quiet and time.time() - last_note > 20:
            print(f"  ...等待 {prompt_id}", flush=True)
            last_note = time.time()
        time.sleep(poll)


def execution_errors(entry: dict) -> list[dict]:
    return [m[1] for m in (entry.get("status") or {}).get("messages", []) or []
            if m and m[0] == "execution_error"]


def cached_nodes(entry: dict) -> list[str]:
    """这次执行里被 ComfyUI 缓存复用的节点 —— 缓存命中意味着**没有**真的再调一次云端。

    这一条对"同 seed 能不能复现"很关键：图逐像素一致可能只是节点缓存，不是远端模型确定性。
    """
    out: set[str] = set()
    for msg in (entry.get("status") or {}).get("messages", []) or []:
        if msg and msg[0] == "execution_cached":
            out.update(str(n) for n in (msg[1] or {}).get("nodes", []) or [])
    return sorted(out)


def raise_for_status(entry: dict, prompt_id: str) -> None:
    errs = execution_errors(entry)
    if not errs:
        return
    first = errs[0]
    msg = str(first.get("exception_message") or "").strip()
    node = f"{first.get('node_type')}(#{first.get('node_id')})"
    low = msg.lower()
    if "unauthor" in low or "please login" in low:
        raise AuthError(
            f"{node} 拒绝执行：{msg}\n"
            "  付费 partner 节点要 ComfyUI 账号凭据，而这次请求没带（或无效）。三条路：\n"
            "   1) 拿 platform.comfy.org 的 ComfyUI Account API Key（账号里要有 credits），\n"
            "      用 --api-key-file / --api-key / $COMFYUI_API_KEY 传进来（脚本走\n"
            "      extra_data.api_key_comfy_org）；\n"
            "   2) 在 ComfyUI 里 Settings → User 填同一个 API Key（服务端会替无头请求带上）；\n"
            "   3) 只在桌面端界面点 Run —— 但那样就不能脚本化、不能留档。\n"
            "  注意：在桌面端用邮箱/浏览器登录**不足以**让无头请求通过，实测仍报 Unauthorized。"
        )
    raise NodeError(f"{node} 执行失败：{msg}")


def collect_images(entry: dict, only_node: str | None = None) -> list[dict]:
    images: list[dict] = []
    for node_id, node_out in (entry.get("outputs") or {}).items():
        if only_node is not None and str(node_id) != str(only_node):
            continue
        for img in node_out.get("images", []) or []:
            images.append({"node_id": str(node_id), "filename": img.get("filename"),
                           "subfolder": img.get("subfolder", ""),
                           "type": img.get("type", "output")})
    return images


def download_image(server: str, img: dict, out_dir: str, timeout: float = 300.0) -> str:
    query = urllib.parse.urlencode({"filename": img["filename"],
                                    "subfolder": img.get("subfolder", ""),
                                    "type": img.get("type", "output")})
    os.makedirs(out_dir, exist_ok=True)
    local_path = os.path.join(out_dir, os.path.basename(img["filename"]))
    with open(local_path, "wb") as fh:
        fh.write(_request(f"{server.rstrip('/')}/view?{query}", timeout=timeout))
    return local_path


def record_request(out_dir: str, prefix: str, server: str, params: dict, prompt_id: str,
                   graph: dict, files: list[str], key: dict) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    api_name = f"{prefix}.api.json"
    with open(os.path.join(out_dir, api_name), "w", encoding="utf-8") as fh:
        json.dump(graph, fh, ensure_ascii=False, indent=2)
    entry = {"time": time.strftime("%Y-%m-%dT%H:%M:%S"), "engine": ENGINE, "server": server,
             "prompt_id": prompt_id, "prefix": prefix, "api_file": api_name, "files": files,
             # 只记"用没用凭据、走的哪条通道"，不记凭据本身
             "credential_channel": key.get("channel"), "credential_source": key.get("source")}
    entry.update(params)
    with open(os.path.join(out_dir, "requests.jsonl"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


# --------------------------------------------------------------------------
# 生成
# --------------------------------------------------------------------------
def generate(
    server: str = DEFAULT_SERVER,
    workflow: str = DEFAULT_WORKFLOW,
    node_info: str = DEFAULT_NODE_INFO,
    prompt: str | None = None,
    model: str | None = None,
    size: str | None = None,
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
    api_key: str | None = None,
    key_file: str | None = None,
    auth_token: str | None = None,
    allow_unapplied: bool = False,
) -> dict:
    """跑一次 Seedream 文生图，返回可 JSON 序列化的摘要。"""
    info = load_node_info(node_info)
    ui = load_workflow(workflow)
    api, save_id = build_api_graph(ui)
    if save_id is None:
        raise RuntimeError("工作流里没有 SaveImageAdvanced；找不到产物")

    # 尺寸：预设原文 / 1024x1024 / 1:1；Custom 必须配 --width/--height
    if str(size or "").strip() == "Custom":
        if width is None or height is None:
            raise InvalidValueError("--size Custom 需要同时给 --width 和 --height")
        size = f"{width}x{height}"
    elif size is None and (width is not None or height is not None):
        if width is None or height is None:
            raise InvalidValueError("--width/--height 要成对给（或直接用 --size 1024x1024）")
        size = f"{width}x{height}"

    api, report = apply_params(api, {
        "prompt": prompt, "model": model, "size": size, "seed": seed, "thinking": thinking,
        "watermark": watermark, "prompt_optimization": prompt_optimization,
        "max_images": max_images, "fail_on_partial": fail_on_partial,
        "filename_prefix": filename_prefix, "format": image_format,
    }, info, strict=not allow_unapplied)

    problems = validate_graph(api, info)
    if problems:
        raise RuntimeError("本地 schema 校验没过（这张图不该发出去）：\n  - "
                           + "\n  - ".join(problems))

    seed_nid = find_seedream(api)
    model_used = api[seed_nid]["inputs"].get("model")
    size_used = api[seed_nid]["inputs"].get("model.size_preset")
    if not quiet:
        print(f"-> {server}  model={model_used!r} size={size_used!r} "
              f"seed={api[seed_nid]['inputs'].get('model.seed')}", flush=True)
    if dry_run:
        return {"dry_run": True, "api": api, "applied": report["applied"],
                "unapplied": report["unapplied"], "save_node": save_id}

    key = resolve_credential(api_key, key_file, auth_token)
    if not key["present"] and not quiet:
        print("!! 没有凭据（--api-key / --api-key-file / $COMFYUI_API_KEY / --auth-token）；"
              "付费节点通常会被拒。继续试一次。", file=sys.stderr, flush=True)

    prompt_id = queue_prompt(server, api, f"dsh-seedream-{os.getpid()}", key)
    if not quiet:
        print(f"   queued: {prompt_id}", flush=True)
    entry = wait_for_history(server, prompt_id, timeout=timeout, poll=poll, quiet=quiet)
    raise_for_status(entry, prompt_id)

    local_paths: list[str] = []
    for img in collect_images(entry, only_node=save_id):
        if img.get("filename"):
            local_paths.append(download_image(server, img, out_dir))
    if not quiet:
        for path in local_paths:
            print(f"   saved: {path} ({os.path.getsize(path)} bytes)", flush=True)

    params = {"prompt": prompt, "model": model_used, "size": size_used,
              # 只在 size_preset=Custom 时才有意义，故不叫 width/height
              "custom_width": api[seed_nid]["inputs"].get("model.width"),
              "custom_height": api[seed_nid]["inputs"].get("model.height"),
              "seed": api[seed_nid]["inputs"].get("model.seed"),
              "thinking": api[seed_nid]["inputs"].get("model.thinking"),
              "watermark": api[seed_nid]["inputs"].get("model.watermark"),
              "workflow": os.path.basename(workflow),
              "applied": report["applied"], "unapplied": report["unapplied"]}
    if record:
        record_request(out_dir, filename_prefix or "seedream", server, params, prompt_id,
                       api, local_paths, key)
    return {"prompt_id": prompt_id, "images": collect_images(entry, only_node=save_id),
            "local_paths": local_paths, "credential_channel": key.get("channel"),
            "cached_nodes": cached_nodes(entry),
            "status": (entry.get("status") or {}).get("status_str"),
            "applied": report["applied"], "unapplied": report["unapplied"]}


def find_seedream(api: dict) -> str:
    for nid, node in api.items():
        if node.get("class_type") == SEEDREAM_CLASS:
            return nid
    raise KeyError(f"API 图里没有 {SEEDREAM_CLASS}")


# --------------------------------------------------------------------------
# 自检
# --------------------------------------------------------------------------
def run_check(server: str, node_info: str = DEFAULT_NODE_INFO, api_key: str | None = None,
              key_file: str | None = None, auth_token: str | None = None) -> tuple[dict, int]:
    result: dict[str, Any] = {"server": server}
    health = check_server(server)
    result["reachable"] = health["reachable"]
    if not health["reachable"]:
        result["error"] = health["error"]
        result["hint"] = "服务器不可达：先确认 ComfyUI Desktop 已启动、--listen 已开、防火墙放通端口"
        return result, EXIT_UNREACHABLE
    result["comfyui_version"] = (health["stats"].get("system") or {}).get("comfyui_version")

    live_seed = fetch_node_info(server, SEEDREAM_CLASS)
    live_save = fetch_node_info(server, SAVE_CLASS)
    result["nodes"] = {SEEDREAM_CLASS: live_seed is not None, SAVE_CLASS: live_save is not None}
    if live_seed is None:
        result["hint"] = (f"服务器上没有 {SEEDREAM_CLASS}：ComfyUI 太旧，或启动参数带了 "
                          "--disable-partner-nodes / --offline")
        return result, EXIT_NO_NODE

    fixture = load_node_info(node_info)
    result["models"] = model_keys({"nodes": {SEEDREAM_CLASS: live_seed}})
    result["api_node"] = bool(live_seed.get("api_node"))
    result["paid"] = True
    result["schema_drift"] = diff_schema(fixture, {"nodes": {SEEDREAM_CLASS: live_seed,
                                                            SAVE_CLASS: live_save or {}}})
    if not any(result["schema_drift"].values()):
        result["schema_drift"] = "none"
    result["model_files_needed"] = []  # 模型在云端：本机没有、也不需要权重
    key = resolve_credential(api_key, key_file, auth_token)
    result["credential"] = {"present": key["present"], "channel": key["channel"],
                            "source": key["source"], "masked": key["masked"]}
    if not key["present"]:
        result["credential"]["hint"] = (
            "没有凭据：付费节点会在执行阶段报 Unauthorized（用 --api-key-file 或 "
            "$COMFYUI_API_KEY 给 ComfyUI 账号 API Key）。--check 只能证明图能过校验，"
            "证明不了能出图。")
    result["next"] = ("python3 seedream_gen.py --prompt-file <prompt.txt> --size 1024x1024 "
                      "--out-dir out/")
    return result, EXIT_OK


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=DEFAULT_SERVER, help=f"ComfyUI 地址（默认 {DEFAULT_SERVER}）")
    ap.add_argument("--workflow", default=DEFAULT_WORKFLOW, help="UI 工作流 JSON")
    ap.add_argument("--node-info", default=DEFAULT_NODE_INFO, help="节点 schema 快照")
    ap.add_argument("--prompt", help="提示词")
    ap.add_argument("--prompt-file", help="从文件读提示词（与 --prompt 二选一）")
    ap.add_argument("--model", help="模型键（默认取工作流里的）")
    ap.add_argument("--size", help="尺寸预设原文 / 1024x1024 / 1:1")
    ap.add_argument("--width", type=int, help="仅 --size 为 Custom 时有意义")
    ap.add_argument("--height", type=int)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--thinking", dest="thinking", action="store_true", default=None,
                    help="开 thinking（pro/lite/4.5/4.0 支持；更慢、遵循度更好）")
    ap.add_argument("--no-thinking", dest="thinking", action="store_false")
    ap.add_argument("--watermark", dest="watermark", action="store_true", default=None,
                    help='加 "AI generated" 水印')
    ap.add_argument("--no-watermark", dest="watermark", action="store_false")
    ap.add_argument("--prompt-optimization", choices=["standard", "fast"],
                    help="仅 seedream 5.0 pro 有")
    ap.add_argument("--max-images", type=int, help="仅 lite/4.5/4.0：一次要几张关联图")
    ap.add_argument("--fail-on-partial", dest="fail_on_partial", action="store_true",
                    default=None, help="缺图即失败（仅 lite/4.5/4.0）")
    ap.add_argument("--no-fail-on-partial", dest="fail_on_partial", action="store_false")
    ap.add_argument("--filename-prefix", help="输出前缀（也是留档名，默认 seedream）")
    ap.add_argument("--format", dest="image_format", help="保存格式（png / jpeg / webp / exr…）")
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--timeout", type=float, default=900.0,
                    help="等待秒数（thinking + pro 可能几分钟，默认 900）")
    ap.add_argument("--poll", type=float, default=3.0)
    ap.add_argument("--api-key", help="ComfyUI 账号 API Key（也可用 $COMFYUI_API_KEY）")
    ap.add_argument("--api-key-file", help="从文件读 API Key（首行/整文件）")
    ap.add_argument("--auth-token", help="改用浏览器登录态 Bearer token 通道（会过期，一般不推荐）")
    ap.add_argument("--allow-unapplied", action="store_true",
                    help="参数对所选模型不存在时不报错（默认报错）")
    ap.add_argument("--dry-run", action="store_true", help="只打印 API 图，不提交")
    ap.add_argument("--no-record", dest="record", action="store_false",
                    help="不写 <prefix>.api.json / requests.jsonl")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--check", action="store_true", help="探活 + 节点 + schema 对账 + 凭据")
    ap.add_argument("--list", action="store_true", help="列出模型与各模型支持的参数")
    args = ap.parse_args(argv)

    if args.check:
        result, code = run_check(args.server, args.node_info, args.api_key, args.api_key_file,
                                 args.auth_token)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return code
    if args.list:
        print(json.dumps(describe(load_node_info(args.node_info)), ensure_ascii=False, indent=2))
        return EXIT_OK

    prompt = args.prompt
    if args.prompt_file:
        with open(args.prompt_file, encoding="utf-8") as fh:
            prompt = fh.read().strip()
    if not prompt:
        ap.error("--prompt 或 --prompt-file 必须给一个（--check / --list 除外）")

    try:
        result = generate(
            server=args.server, workflow=args.workflow, node_info=args.node_info, prompt=prompt,
            model=args.model, size=args.size, width=args.width, height=args.height,
            seed=args.seed, thinking=args.thinking, watermark=args.watermark,
            prompt_optimization=args.prompt_optimization, max_images=args.max_images,
            fail_on_partial=args.fail_on_partial, filename_prefix=args.filename_prefix,
            image_format=args.image_format, out_dir=args.out_dir, timeout=args.timeout,
            poll=args.poll, quiet=args.quiet, record=args.record, dry_run=args.dry_run,
            api_key=args.api_key, key_file=args.api_key_file, auth_token=args.auth_token,
            allow_unapplied=args.allow_unapplied,
        )
    except (UnappliedOverrideError, UnknownModelError, ValueError) as exc:
        print(f"参数不成立：{exc}", file=sys.stderr)
        return EXIT_BAD_PARAMS
    except RejectedError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_REJECTED
    except AuthError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_AUTH
    except NodeError as exc:
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
