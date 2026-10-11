#!/usr/bin/env python3
"""comfyui-server —— 把"服务器本身"当对象来查：状态、权重、节点、模板、历史、队列。

设计边界（一句话判据）：**"这个功能在完全没有 prompt 的情况下还有意义吗？"**
有 → 归本技能；没有 → 归生成技能（text-to-image / image-edit / *-fastvideo3 /
music-minimax3）。所以这里**一步生成都不做**，只做探查与运维。

用法::

    python3 comfyui_server.py --check                 # 自检：探活 + 目录/队列摘要
    python3 comfyui_server.py status                  # 版本 / 显存 / 队列 一屏看完
    python3 comfyui_server.py models --search wan     # 本机有哪些权重（跨目录搜）
    python3 comfyui_server.py nodes --search upscale  # 有哪些节点类
    python3 comfyui_server.py nodes --class KSampler  # 某个节点吃哪些参数/枚举值
    python3 comfyui_server.py templates --type audio  # 官方模板目录（598 个）
    python3 comfyui_server.py templates --pull audio_minimax_music_3 --audit
    python3 comfyui_server.py audit --template video_wan2_2_14B_i2v
    python3 comfyui_server.py audit --workflow assets/my.json
    python3 comfyui_server.py workflows               # 本机已存的 UI 工作流
    python3 comfyui_server.py history --limit 10      # 最近的运行记录
    python3 comfyui_server.py history --download <id> --out-dir out/
    python3 comfyui_server.py queue                   # 现在在跑什么、排了多少
    python3 comfyui_server.py interrupt --yes         # 打断当前任务
    python3 comfyui_server.py free --yes              # 释放显存（不动权重）
    python3 comfyui_server.py free --yes --unload-models   # 卸载权重（下次生成会重载，慢）
    python3 comfyui_server.py clear-queue --yes       # 清空排队中的任务
    python3 comfyui_server.py upload --file ref.png   # 上传到服务器 input/

退出码：0 正常 / 1 失败（含服务器不可达）/ 2 用法错误 / 3 需要 --yes 的写操作被拦下。
输出：默认 JSON（`--format text` 给人看）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

DEFAULT_SERVER = os.environ.get("COMFYUI_SERVER", "http://192.168.3.5:18000")

# 前端专有节点：服务器上没有这些类，但它不占权重、也不影响执行（转换时剔掉即可）
UI_ONLY_CLASSES = ("MarkdownNote", "Note", "PrimitiveNode", "Reroute", "GroupNode")

# 认得出"哪个 widget 值其实是权重文件名"——`audit` 全靠它
MODEL_FILE_RE = re.compile(
    r"[\w\-.()+ ]+\.(?:safetensors|ckpt|pt|pth|gguf|bin|sft)$"
)

EXIT_OK, EXIT_FAIL, EXIT_USAGE, EXIT_NEEDS_YES = 0, 1, 2, 3

TEMPLATE_TYPES = ("image", "video", "audio", "3d", "llm")


# --------------------------------------------------------------------------- HTTP
class ServerUnreachable(RuntimeError):
    """探活失败：服务器没起来 / 端口没放通 / 地址写错。"""


class ServerError(RuntimeError):
    """连上了，但接口返回非 2xx。"""


def _request(
    server: str,
    path: str,
    *,
    data: bytes | None = None,
    method: str = "GET",
    timeout: float = 30.0,
    content_type: str | None = None,
) -> bytes:
    req = urllib.request.Request(server.rstrip("/") + path, data=data, method=method)
    if content_type:
        req.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:  # 连上了，接口报错
        body = exc.read()[:400].decode("utf-8", "replace")
        raise ServerError(f"{method} {path} -> HTTP {exc.code}: {body}") from None
    except urllib.error.URLError as exc:  # 连不上
        raise ServerUnreachable(
            f"服务器不可达：{server}（{exc.reason}）——"
            "先确认 ComfyUI 已启动、--listen 已开、防火墙放通端口"
        ) from None
    except OSError as exc:  # 超时 / 连接中断
        raise ServerUnreachable(f"{method} {path} 失败：{exc}") from None


def get_json(server: str, path: str, timeout: float = 30.0):
    return json.loads(_request(server, path, timeout=timeout) or b"null")


def post_json(server: str, path: str, payload: dict | None = None, timeout: float = 30.0):
    body = json.dumps(payload or {}).encode("utf-8")
    raw = _request(
        server, path, data=body, method="POST", timeout=timeout,
        content_type="application/json",
    )
    return json.loads(raw or b"null")


def probe(server: str, timeout: float = 10.0) -> dict:
    """先探活再干活：不可达就立刻抛，别让调用方提交完再长等。"""
    stats = get_json(server, "/system_stats", timeout=timeout)
    if not isinstance(stats, dict) or "system" not in stats:
        raise ServerError(f"/system_stats 返回了意外的结构：{str(stats)[:200]}")
    return stats


# --------------------------------------------------------------------- 只读采集
def model_folders(server: str, timeout: float = 30.0) -> list[str]:
    data = get_json(server, "/api/models", timeout=timeout)
    return data if isinstance(data, list) else []


def model_files(server: str, folder: str, timeout: float = 30.0) -> list[str]:
    data = get_json(server, f"/api/models/{urllib.parse.quote(folder)}", timeout=timeout)
    return data if isinstance(data, list) else []


def object_info(server: str, timeout: float = 120.0) -> dict:
    data = get_json(server, "/api/object_info", timeout=timeout)
    return data if isinstance(data, dict) else {}


def queue_state(server: str, timeout: float = 15.0) -> dict:
    data = get_json(server, "/queue", timeout=timeout)
    return data if isinstance(data, dict) else {}


def template_index(server: str, timeout: float = 60.0) -> list[dict]:
    """官方模板目录。注意 `/api/workflow_templates` 在本机版本上返回 `{}`，别用它。"""
    data = get_json(server, "/templates/index.json", timeout=timeout)
    rows: list[dict] = []
    for module in data if isinstance(data, list) else []:
        for item in module.get("templates") or []:
            rows.append(
                {
                    "name": item.get("name"),
                    "title": item.get("title"),
                    "type": item.get("type"),
                    "category": module.get("category"),
                    "module": module.get("moduleName"),
                    "description": item.get("description") or "",
                }
            )
    return rows


def history_entries(server: str, limit: int = 20, timeout: float = 30.0) -> list[dict]:
    data = get_json(server, f"/history?max_items={int(limit)}", timeout=timeout)
    if not isinstance(data, dict):
        return []
    rows = []
    for prompt_id, entry in data.items():
        status = (entry or {}).get("status") or {}
        rows.append(
            {
                "prompt_id": prompt_id,
                "status": status.get("status_str"),
                "completed": bool(status.get("completed")),
                "files": [_file_of(item) for item in _iter_outputs(entry)],
            }
        )
    rows.reverse()  # /history 是旧→新，这里给"最近的在前"
    return rows


def _iter_outputs(entry: dict | None):
    for node_output in ((entry or {}).get("outputs") or {}).values():
        if not isinstance(node_output, dict):
            continue
        for kind, items in node_output.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and item.get("filename"):
                        yield {**item, "kind": kind}


def _file_of(item: dict) -> dict:
    return {
        "filename": item.get("filename"),
        "subfolder": item.get("subfolder") or "",
        "type": item.get("type") or "output",
        "kind": item.get("kind"),
    }


def download_view(server: str, item: dict, out_dir: str, timeout: float = 180.0) -> str:
    query = urllib.parse.urlencode(
        {
            "filename": item["filename"],
            "subfolder": item.get("subfolder") or "",
            "type": item.get("type") or "output",
        }
    )
    raw = _request(server, f"/view?{query}", timeout=timeout)
    rel = os.path.join(item.get("subfolder") or "", os.path.basename(item["filename"]))
    dest = os.path.join(out_dir, rel)
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    with open(dest, "wb") as fh:
        fh.write(raw)
    return dest


# ------------------------------------------------------------------ 工作流审计
def _walk_nodes(obj):
    """深度遍历 UI 工作流（含 definitions.subgraphs 里的节点）。"""
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            if isinstance(cur.get("nodes"), list):
                for node in cur["nodes"]:
                    if isinstance(node, dict):
                        yield node
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)


def referenced_models(ui: dict) -> dict:
    """把工作流引用的权重文件名分成 active / inactive（mute 或 bypass）。

    这一步是 `audit` 的关键：模板里常备着"另一条分支"的权重（例如 int8 与非 int8
    两套、或换 LoRA 的备选），默认是 bypass 状态。不区分 mode 就会把能跑的模板
    误判成"缺权重"（实测：Z-Image Fun ControlNet 官方模板会被误判）。
    """
    active: set[str] = set()
    inactive: set[str] = set()
    for node in _walk_nodes(ui):
        bucket = inactive if node.get("mode") in (2, 4) else active
        for value in node.get("widgets_values") or []:
            if isinstance(value, str):
                text = value.strip()
                if MODEL_FILE_RE.match(text):
                    bucket.add(text)
    return {"active": sorted(active), "inactive": sorted(inactive)}


def referenced_nodes(ui: dict) -> tuple[set[str], set[str]]:
    """返回 (用到的节点类, 子图定义的 id/name——它们不是服务器上的类)。"""
    classes: set[str] = set()
    subs: set[str] = set()
    for sub in (ui.get("definitions") or {}).get("subgraphs") or []:
        if isinstance(sub, dict):
            subs |= {sub.get("id"), sub.get("name")}
    for node in _walk_nodes(ui):
        if node.get("mode") in (2, 4) or not isinstance(node.get("type"), str):
            continue
        if node["type"] in subs or node["type"].startswith("workflow>"):
            continue
        classes.add(node["type"])
    return classes, {s for s in subs if s}


def audit_workflow(
    ui: dict,
    *,
    server: str,
    installed_models: set[str] | None = None,
    installed_classes: set[str] | None = None,
    timeout: float = 120.0,
) -> dict:
    refs = referenced_models(ui)
    if installed_models is None:
        installed_models = set()
        for folder in model_folders(server, timeout=timeout):
            installed_models |= set(model_files(server, folder, timeout=timeout))
    if installed_classes is None:
        installed_classes = set(object_info(server, timeout=timeout))

    missing_models = [m for m in refs["active"] if m not in installed_models]
    used, _subs = referenced_nodes(ui)
    missing_nodes = sorted(c for c in used if c not in installed_classes)
    ui_only = sorted(c for c in missing_nodes if c in UI_ONLY_CLASSES)
    blocking_nodes = [c for c in missing_nodes if c not in UI_ONLY_CLASSES]

    outputs = sorted(
        {
            node.get("type")
            for node in _walk_nodes(ui)
            if node.get("mode") not in (2, 4)
            and isinstance(node.get("type"), str)
            and node["type"].startswith(("Save", "Preview"))
        }
    )
    return {
        "node_count": sum(1 for _ in _walk_nodes(ui)),
        "output_nodes": outputs,
        "active_models": refs["active"],
        "bypassed_models": refs["inactive"],
        "missing_models": missing_models,
        "missing_nodes": blocking_nodes,
        "ui_only_nodes": ui_only,
        # True 只代表"权重与节点都有"，不代表参数语义正确——最终仍要真机跑一次
        "runnable": not missing_models and not blocking_nodes,
    }


# --------------------------------------------------------------------- 输出格式
def emit(payload: dict, fmt: str = "json", *, items_key: str = "items",
         columns: list[str] | None = None) -> None:
    if fmt != "text":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    rows = payload.get(items_key) or []
    for key, value in payload.items():
        if key == items_key or isinstance(value, (list, dict)):
            continue
        print(f"{key}: {value}")
    if rows and columns:
        print("  ".join(columns))
        for row in rows:
            print("  ".join(str(row.get(c, "")) for c in columns))
    print(f"{items_key}: {len(rows)}")


def _fail(message: str, fmt: str) -> int:
    emit({"ok": False, "error": message, "hint": None}, fmt)
    return EXIT_FAIL


# -------------------------------------------------------------------------- 动词
def cmd_check(args) -> int:
    try:
        stats = probe(args.server, timeout=args.timeout)
        folders = model_folders(args.server, timeout=args.timeout)
        counts = {f: len(model_files(args.server, f, timeout=args.timeout)) for f in folders}
        q = queue_state(args.server, timeout=args.timeout)
    except (ServerUnreachable, ServerError) as exc:
        return _fail(str(exc), args.format)
    system = stats.get("system") or {}
    devices = stats.get("devices") or []
    payload = {
        "ok": True,
        "server": args.server,
        "comfyui_version": system.get("comfyui_version"),
        "required_frontend_version": system.get("required_frontend_version"),
        "installed_templates_version": system.get("installed_templates_version"),
        "device": (devices[0] or {}).get("name") if devices else None,
        "vram_free_gb": _gb((devices[0] or {}).get("vram_free")) if devices else None,
        "model_files_total": sum(counts.values()),
        "model_folders": {k: v for k, v in counts.items() if v},
        "queue": {"running": len(q.get("queue_running") or []),
                  "pending": len(q.get("queue_pending") or [])},
        "hint": None,
    }
    emit(payload, args.format)
    return EXIT_OK


def _gb(num) -> float | None:
    try:
        return round(int(num) / 1024 ** 3, 2)
    except (TypeError, ValueError):
        return None


def cmd_status(args) -> int:
    try:
        stats = probe(args.server, timeout=args.timeout)
        q = queue_state(args.server, timeout=args.timeout)
    except (ServerUnreachable, ServerError) as exc:
        return _fail(str(exc), args.format)
    system = stats.get("system") or {}
    devices = []
    for dev in stats.get("devices") or []:
        devices.append(
            {
                "name": dev.get("name"),
                "type": dev.get("type"),
                "vram_total_gb": _gb(dev.get("vram_total")),
                "vram_free_gb": _gb(dev.get("vram_free")),
                "torch_vram_free_gb": _gb(dev.get("torch_vram_free")),
            }
        )
    emit(
        {
            "server": args.server,
            "comfyui_version": system.get("comfyui_version"),
            "frontend": {
                "installed": (system.get("comfy_package_versions") or [{}])[0].get("version")
                if system.get("comfy_package_versions") else None,
                "required": system.get("required_frontend_version"),
            },
            "templates_version": system.get("installed_templates_version"),
            "python": system.get("python_version"),
            "os": system.get("os"),
            "ram_total_gb": _gb(system.get("ram_total")),
            "ram_free_gb": _gb(system.get("ram_free")),
            "devices": devices,
            "queue": {
                "running": len(q.get("queue_running") or []),
                "pending": len(q.get("queue_pending") or []),
                "running_ids": [str(i[1]) for i in (q.get("queue_running") or []) if len(i) > 1],
            },
        },
        args.format,
    )
    return EXIT_OK


def cmd_models(args) -> int:
    try:
        folders = [args.folder] if args.folder else model_folders(args.server, timeout=args.timeout)
        rows = []
        for folder in folders:
            for name in model_files(args.server, folder, timeout=args.timeout):
                if args.search and args.search.lower() not in name.lower():
                    continue
                rows.append({"folder": folder, "name": name})
    except (ServerUnreachable, ServerError) as exc:
        return _fail(str(exc), args.format)
    rows.sort(key=lambda r: (r["folder"], r["name"]))
    emit(
        {"server": args.server, "count": len(rows), "items": rows},
        args.format, columns=["folder", "name"],
    )
    return EXIT_OK


def cmd_nodes(args) -> int:
    try:
        info = object_info(args.server, timeout=max(args.timeout, 120.0))
    except (ServerUnreachable, ServerError) as exc:
        return _fail(str(exc), args.format)
    if args.class_name:
        node = info.get(args.class_name)
        if node is None:
            near = [c for c in sorted(info) if args.class_name.lower() in c.lower()][:10]
            emit(
                {"ok": False, "error": f"没有这个节点类：{args.class_name}",
                 "did_you_mean": near},
                args.format,
            )
            return EXIT_FAIL
        inp = node.get("input") or {}
        emit(
            {
                "ok": True,
                "class": args.class_name,
                "category": node.get("category"),
                "python_module": node.get("python_module"),
                "deprecated": bool(node.get("deprecated")),
                "required": {k: _input_spec(v) for k, v in (inp.get("required") or {}).items()},
                "optional": {k: _input_spec(v) for k, v in (inp.get("optional") or {}).items()},
                "outputs": node.get("output") or [],
                "output_names": node.get("output_name") or [],
            },
            args.format,
        )
        return EXIT_OK
    names = sorted(info)
    if args.search:
        names = [n for n in names if args.search.lower() in n.lower()]
    rows = [{"class": n, "category": (info[n] or {}).get("category")} for n in names]
    emit(
        {"server": args.server, "total_classes": len(info), "count": len(rows), "items": rows},
        args.format, columns=["class", "category"],
    )
    return EXIT_OK


def _input_spec(spec) -> dict:
    out: dict = {}
    if not isinstance(spec, list) or not spec:
        return {"type": None}
    head = spec[0]
    if isinstance(head, list):
        out["type"] = "CHOICE"
        out["choices"] = head
    else:
        out["type"] = head
    if len(spec) > 1 and isinstance(spec[1], dict):
        for key in ("default", "min", "max", "step", "multiline"):
            if key in spec[1]:
                out[key] = spec[1][key]
    return out


def cmd_templates(args) -> int:
    try:
        index = template_index(args.server, timeout=max(args.timeout, 60.0))
    except (ServerUnreachable, ServerError) as exc:
        return _fail(str(exc), args.format)
    if args.pull:
        return _pull_template(args, index)
    rows = index
    if args.type:
        rows = [t for t in rows if t["type"] == args.type]
    if args.search:
        needle = args.search.lower()
        rows = [
            t for t in rows
            if needle in (t["name"] or "").lower()
            or needle in (t["title"] or "").lower()
            or needle in (t["description"] or "").lower()
        ]
    if args.limit:
        rows = rows[: args.limit]
    by_type: dict[str, int] = {}
    for t in index:
        by_type[t["type"]] = by_type.get(t["type"], 0) + 1
    emit(
        {
            "server": args.server,
            "total": len(index),
            "by_type": by_type,
            "count": len(rows),
            "items": rows,
            "hint": "拉一个下来：templates --pull <name> --audit（本机缺什么权重一并报出）",
        },
        args.format, columns=["type", "name", "title"],
    )
    return EXIT_OK


def _pull_template(args, index: list[dict]) -> int:
    known = {t["name"] for t in index}
    if args.pull not in known:
        near = [n for n in sorted(known) if args.pull.lower() in n.lower()][:10]
        emit({"ok": False, "error": f"目录里没有模板 {args.pull}", "did_you_mean": near},
             args.format)
        return EXIT_FAIL
    out_dir = args.out_dir or "out/templates"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{args.pull}.json")
    try:
        raw = _request(args.server, f"/templates/{urllib.parse.quote(args.pull)}.json",
                       timeout=max(args.timeout, 60.0))
        ui = json.loads(raw)
    except (ServerUnreachable, ServerError, ValueError) as exc:
        return _fail(f"拉取模板失败：{exc}", args.format)
    if not isinstance(ui, dict) or "nodes" not in ui:
        return _fail(f"{args.pull} 不是 UI 工作流（缺 nodes 字段）", args.format)
    with open(path, "wb") as fh:
        fh.write(raw)

    report = audit_workflow(ui, server=args.server) if args.audit else None
    meta = {
        "source": f"{args.server.rstrip('/')}/templates/{args.pull}.json",
        "name": args.pull,
        "sha256": _sha256(raw),
        "bytes": len(raw),
        "node_count": sum(1 for _ in _walk_nodes(ui)),
        "output_nodes": sorted(
            {n.get("type") for n in _walk_nodes(ui)
             if isinstance(n.get("type"), str)
             and n["type"].startswith(("Save", "Preview"))}
        ),
        "fetched_via": "comfyui-server",
    }
    if report:
        meta["audit"] = report
    with open(os.path.join(out_dir, f"{args.pull}.meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    emit({"ok": True, "path": path, "meta_path": os.path.join(out_dir, f"{args.pull}.meta.json"),
          **meta}, args.format)
    return EXIT_OK


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def cmd_audit(args) -> int:
    if args.template:
        try:
            raw = _request(args.server, f"/templates/{urllib.parse.quote(args.template)}.json",
                           timeout=max(args.timeout, 60.0))
            ui = json.loads(raw)
        except (ServerUnreachable, ServerError, ValueError) as exc:
            return _fail(f"拉取模板失败：{exc}", args.format)
        source = args.template
    else:
        if not os.path.isfile(args.workflow or ""):
            return _fail(f"找不到工作流文件：{args.workflow}", args.format)
        try:
            ui = json.load(open(args.workflow, encoding="utf-8"))
        except ValueError as exc:
            return _fail(f"不是合法 JSON：{exc}", args.format)
        source = args.workflow
    try:
        probe(args.server, timeout=args.timeout)
        report = audit_workflow(ui, server=args.server, timeout=max(args.timeout, 120.0))
    except (ServerUnreachable, ServerError) as exc:
        return _fail(str(exc), args.format)
    emit(
        {
            "ok": report["runnable"],
            "server": args.server,
            "source": source,
            **report,
            "hint": None if report["runnable"]
            else "缺权重就去 /api/models 对一遍名字；缺节点类说明该自定义节点没装",
        },
        args.format,
    )
    return EXIT_OK if report["runnable"] else EXIT_FAIL


def cmd_workflows(args) -> int:
    try:
        data = get_json(
            args.server,
            f"/api/userdata?dir={urllib.parse.quote(args.dir)}",
            timeout=args.timeout,
        )
    except (ServerUnreachable, ServerError) as exc:
        return _fail(str(exc), args.format)
    names = data if isinstance(data, list) else []
    rows = [{"name": n} for n in names if isinstance(n, str)]
    if args.search:
        rows = [r for r in rows if args.search.lower() in r["name"].lower()]
    emit(
        {"server": args.server, "dir": args.dir, "count": len(rows), "items": rows},
        args.format, columns=["name"],
    )
    return EXIT_OK


def cmd_history(args) -> int:
    try:
        if args.download:
            entry = get_json(args.server, f"/history/{urllib.parse.quote(args.download)}",
                             timeout=args.timeout)
            if not isinstance(entry, dict) or not entry:
                return _fail(f"历史里没有 {args.download}", args.format)
            node = next(iter(entry.values()))
            out_dir = args.out_dir or "out/history"
            os.makedirs(out_dir, exist_ok=True)
            saved, skipped = [], []
            for item in _iter_outputs(node):
                if item.get("type") == "temp" and not args.include_temp:
                    skipped.append(_file_of(item))
                    continue
                saved.append(download_view(args.server, item, out_dir))
            emit(
                {"ok": True, "prompt_id": args.download, "out_dir": out_dir,
                 "local_paths": saved, "skipped_temp": skipped},
                args.format,
            )
            return EXIT_OK
        rows = history_entries(args.server, limit=args.limit, timeout=args.timeout)
    except (ServerUnreachable, ServerError) as exc:
        return _fail(str(exc), args.format)
    for row in rows:
        row["file_count"] = len(row.get("files") or [])
    emit(
        {"server": args.server, "count": len(rows), "items": rows,
         "hint": "下载某次的产物：history --download <prompt_id> --out-dir out/"},
        args.format, columns=["prompt_id", "status", "file_count"],
    )
    return EXIT_OK


def cmd_queue(args) -> int:
    try:
        q = queue_state(args.server, timeout=args.timeout)
    except (ServerUnreachable, ServerError) as exc:
        return _fail(str(exc), args.format)
    rows = []
    for state, key in (("running", "queue_running"), ("pending", "queue_pending")):
        for item in q.get(key) or []:
            rows.append(
                {
                    "state": state,
                    "number": item[0] if len(item) > 0 else None,
                    "prompt_id": item[1] if len(item) > 1 else None,
                }
            )
    emit(
        {"server": args.server,
         "running": len(q.get("queue_running") or []),
         "pending": len(q.get("queue_pending") or []),
         "items": rows},
        args.format, columns=["state", "number", "prompt_id"],
    )
    return EXIT_OK


def _guard(args, what: str, plan: dict) -> bool:
    if getattr(args, "yes", False):
        return True
    payload = {"ok": False, "blocked": what,
               "error": f"{what} 是写操作，需要 --yes 才执行",
               "plan": plan}
    emit(payload, args.format)
    return False


def cmd_interrupt(args) -> int:
    if not _guard(args, "打断当前任务（interrupt）", {"POST": "/interrupt"}):
        return EXIT_NEEDS_YES
    try:
        probe(args.server, timeout=args.timeout)
        q = queue_state(args.server, timeout=args.timeout)
        running = len(q.get("queue_running") or [])
        post_json(args.server, "/interrupt", {}, timeout=args.timeout)
    except (ServerUnreachable, ServerError) as exc:
        return _fail(str(exc), args.format)
    emit({"ok": True, "interrupted_running": running,
          "note": "队列里没有正在跑的任务时，这是无副作用的空操作"}, args.format)
    return EXIT_OK


def cmd_free(args) -> int:
    plan = {"unload_models": bool(args.unload_models), "free_memory": True}
    if not _guard(args, "释放显存（free）", {"POST": "/free", **plan}):
        return EXIT_NEEDS_YES
    try:
        probe(args.server, timeout=args.timeout)
        post_json(args.server, "/free", plan, timeout=args.timeout)
    except (ServerUnreachable, ServerError) as exc:
        return _fail(str(exc), args.format)
    emit({"ok": True, **plan,
          "note": "unload_models=false 只回收缓存；true 会把权重也卸掉，下一次生成要重载（慢）"},
         args.format)
    return EXIT_OK


def cmd_clear_queue(args) -> int:
    if not _guard(args, "清空排队任务（clear-queue）", {"POST": "/queue", "clear": True}):
        return EXIT_NEEDS_YES
    try:
        probe(args.server, timeout=args.timeout)
        before = len(queue_state(args.server, timeout=args.timeout).get("queue_pending") or [])
        post_json(args.server, "/queue", {"clear": True}, timeout=args.timeout)
    except (ServerUnreachable, ServerError) as exc:
        return _fail(str(exc), args.format)
    emit({"ok": True, "cleared_pending": before}, args.format)
    return EXIT_OK


def cmd_upload(args) -> int:
    if not os.path.isfile(args.file):
        return _fail(f"找不到文件：{args.file}", args.format)
    try:
        probe(args.server, timeout=args.timeout)
        name = upload_file(args.server, args.file, subfolder=args.subfolder,
                           timeout=max(args.timeout, 120.0))
    except (ServerUnreachable, ServerError) as exc:
        return _fail(str(exc), args.format)
    emit({"ok": True, "uploaded": name,
          "widget_value": name,
          "note": "把这个值填进 LoadImage.image（或同名字段）即可引用"}, args.format)
    return EXIT_OK


def upload_file(server: str, path: str, *, subfolder: str = "", timeout: float = 120.0) -> str:
    """POST /upload/image。字段名对图片/音频/视频都一样是 `image`。"""
    with open(path, "rb") as fh:
        data = fh.read()
    boundary = "----dsh" + uuid.uuid4().hex
    parts = [
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="image"; filename="{os.path.basename(path)}"\r\n'.encode(),
        b"Content-Type: application/octet-stream\r\n\r\n",
        data,
        f"\r\n--{boundary}\r\n".encode(),
        b'Content-Disposition: form-data; name="overwrite"\r\n\r\n1',
        f"\r\n--{boundary}\r\n".encode(),
        b'Content-Disposition: form-data; name="type"\r\n\r\ninput',
    ]
    if subfolder:
        parts += [
            f"\r\n--{boundary}\r\n".encode(),
            b'Content-Disposition: form-data; name="subfolder"\r\n\r\n',
            subfolder.encode(),
        ]
    parts.append(f"\r\n--{boundary}--\r\n".encode())
    raw = _request(
        server, "/upload/image", data=b"".join(parts), method="POST", timeout=timeout,
        content_type=f"multipart/form-data; boundary={boundary}",
    )
    payload = json.loads(raw or b"{}")
    sub = payload.get("subfolder") or ""
    return f"{sub}/{payload.get('name')}" if sub else payload.get("name", "")


# --------------------------------------------------------------------------- CLI
def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--server", default=DEFAULT_SERVER,
                        help=f"ComfyUI 地址（默认 {DEFAULT_SERVER}，或 $COMFYUI_SERVER）")
    common.add_argument("--timeout", type=float, default=30.0, help="单次请求超时秒数")
    common.add_argument("--format", choices=("json", "text"), default="json")

    ap = argparse.ArgumentParser(
        prog="comfyui_server.py",
        description="查 ComfyUI 服务器本身：状态 / 权重 / 节点 / 模板 / 历史 / 队列（不做生成）",
        parents=[common],
    )
    ap.add_argument("--check", action="store_true",
                    help="等价于 `check` 子命令（自检）")
    sub = ap.add_subparsers(dest="verb")

    sub.add_parser("check", parents=[common], help="探活 + 目录/队列摘要")

    sub.add_parser("status", parents=[common], help="版本 / 显存 / 队列")

    p = sub.add_parser("models", parents=[common], help="本机有哪些权重文件")
    p.add_argument("--folder", help="只列某个目录（diffusion_models / loras / vae …）")
    p.add_argument("--search", help="按文件名子串过滤")

    p = sub.add_parser("nodes", parents=[common], help="有哪些节点类 / 某个节点的参数")
    p.add_argument("--search", help="按类名子串过滤")
    p.add_argument("--class", dest="class_name", help="打印这个类的输入输出 schema")

    p = sub.add_parser("templates", parents=[common], help="官方模板目录（浏览 / 拉取）")
    p.add_argument("--search", help="按 name/title/description 过滤")
    p.add_argument("--type", choices=TEMPLATE_TYPES, help="只看某一类")
    p.add_argument("--limit", type=int, help="最多返回几条")
    p.add_argument("--pull", metavar="NAME", help="下载这个模板的 UI 工作流 JSON")
    p.add_argument("--audit", action="store_true", help="拉取时顺带审计本机缺哪些权重/节点")
    p.add_argument("--out-dir", default="out/templates", help="落盘目录（默认 out/templates）")

    p = sub.add_parser("audit", parents=[common], help="某模板/工作流在本机能不能跑")
    p.add_argument("--template", help="模板名（先从服务器拉）")
    p.add_argument("--workflow", help="本地 UI 工作流 JSON 路径")

    p = sub.add_parser("workflows", parents=[common], help="本机已存的 UI 工作流")
    p.add_argument("--dir", default="workflows", help="userdata 子目录（默认 workflows）")
    p.add_argument("--search", help="按文件名子串过滤")

    p = sub.add_parser("history", parents=[common], help="运行记录 / 下载某次产物")
    p.add_argument("--limit", type=int, default=20, help="最多几条（默认 20）")
    p.add_argument("--download", metavar="PROMPT_ID", help="下载这一次的全部产物")
    p.add_argument("--out-dir", default="out/history", help="落盘目录（默认 out/history）")
    p.add_argument("--include-temp", action="store_true", help="连 temp 中间产物一起下")

    sub.add_parser("queue", parents=[common], help="正在跑什么、排了多少")

    p = sub.add_parser("interrupt", parents=[common], help="打断当前任务（要 --yes）")
    p.add_argument("--yes", action="store_true")

    p = sub.add_parser("free", parents=[common], help="释放显存（要 --yes）")
    p.add_argument("--yes", action="store_true")
    p.add_argument("--unload-models", action="store_true",
                   help="连权重一起卸掉（下次生成要重载，慢）")

    p = sub.add_parser("clear-queue", parents=[common], help="清空排队任务（要 --yes）")
    p.add_argument("--yes", action="store_true")

    p = sub.add_parser("upload", parents=[common], help="上传文件到服务器 input/")
    p.add_argument("--file", required=True)
    p.add_argument("--subfolder", default="")

    return ap


COMMANDS = {
    "check": cmd_check,
    "status": cmd_status,
    "models": cmd_models,
    "nodes": cmd_nodes,
    "templates": cmd_templates,
    "audit": cmd_audit,
    "workflows": cmd_workflows,
    "history": cmd_history,
    "queue": cmd_queue,
    "interrupt": cmd_interrupt,
    "free": cmd_free,
    "clear-queue": cmd_clear_queue,
    "upload": cmd_upload,
}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "--check":  # 与其它技能的 `--check` 习惯对齐
        argv[0] = "check"
    args = build_parser().parse_args(argv)
    if getattr(args, "check", False) and not args.verb:
        args.verb = "check"
    if not args.verb:
        build_parser().print_help()
        return EXIT_USAGE
    if args.verb == "audit" and not (args.template or args.workflow):
        emit({"ok": False, "error": "audit 需要 --template 或 --workflow"}, args.format)
        return EXIT_USAGE
    try:
        return COMMANDS[args.verb](args)
    except KeyboardInterrupt:
        return EXIT_FAIL


if __name__ == "__main__":
    sys.exit(main())
