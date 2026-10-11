#!/usr/bin/env python3
"""comfyui-server 的离线自检：起一个 mock ComfyUI，把每个 verb 都跑一遍。

不需要 GPU、不需要真服务器，覆盖：

  1. 探查类 —— check / status / models / nodes / templates / workflows / history / queue
     的解析与过滤，以及"服务器不可达"的报错路径（不吐 traceback）
  2. 审计类 —— `audit` 必须**按 node.mode 区分 active / bypass**：模板里常备着另一条
     分支的权重（bypass 状态），不区分就会把能跑的模板误判成缺权重（真机踩过：
     Z-Image Fun ControlNet 官方模板）
  3. 写操作 ——`interrupt` / `free` / `clear-queue` 没有 `--yes` 时**一个请求都不许发**，
     退出码 3；`upload` 的 multipart 形状

用法：
  python3 scripts/test_skill.py
退出码 0 = 全部通过。
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import comfyui_server as cs  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []

STATS = {
    "system": {
        "os": "nt", "comfyui_version": "1.2.3-test",
        "required_frontend_version": "9.9.9", "installed_templates_version": "0.0.1-test",
        "python_version": "3.12.test", "ram_total": 64 * 1024 ** 3, "ram_free": 32 * 1024 ** 3,
    },
    "devices": [{"name": "mock-gpu", "type": "cuda", "vram_total": 8 * 1024 ** 3,
                 "vram_free": 6 * 1024 ** 3, "torch_vram_free": 5 * 1024 ** 3}],
}
MODELS = {
    "diffusion_models": ["z_image_turbo_bf16.safetensors", "qwen_image_2512_fp8_e4m3fn.safetensors"],
    "loras": ["pixel_art_style_z_image_turbo.safetensors"],
    "vae": ["ae.safetensors"],
    "upscale_models": ["RealESRGAN_x4plus.pth"],
}
OBJECT_INFO = {
    "KSampler": {
        "category": "sampling", "python_module": "nodes",
        "input": {
            "required": {
                "seed": ["INT", {"default": 0, "min": 0, "max": 18446744073709551615}],
                "sampler_name": [["euler", "dpmpp_2m"]],
                "steps": ["INT", {"default": 20, "min": 1, "max": 10000}],
            },
            "optional": {"denoise": ["FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0}]},
        },
        "output": ["LATENT"], "output_name": ["LATENT"],
    },
    "UNETLoader": {"category": "loaders", "input": {"required": {"unet_name": [["z_image_turbo_bf16.safetensors"]]}}},
    "VAELoader": {"category": "loaders", "input": {"required": {"vae_name": [["ae.safetensors"]]}}},
    "SaveImage": {"category": "image", "input": {"required": {}}},
    "SubgraphOutputs": {"category": "subgraph"},
}
TEMPLATES = [
    {"moduleName": "default", "category": "Foundation", "templates": [
        {"name": "image_z_image_turbo", "title": "Z-Image-Turbo: Text to Image",
         "type": "image", "description": "fast t2i"},
        {"name": "audio_minimax_music_3", "title": "MiniMax Music 3: Text to Music",
         "type": "audio", "description": "caption to music"},
    ]},
    {"moduleName": "extra", "category": "Applied", "templates": [
        {"name": "video_fastvideo_fasth3_i2v", "title": "FastVideo FastH3: Image to Video",
         "type": "video", "description": "i2v with audio"},
    ]},
]

# 审计夹具：一个 bypass 分支引用了本机没有的权重（不该报缺），一个活跃分支真的缺
UI_WORKFLOW = {
    "nodes": [
        {"id": 1, "type": "UNETLoader", "mode": 0, "widgets_values": ["z_image_turbo_bf16.safetensors", "default"]},
        {"id": 2, "type": "UNETLoader", "mode": 4, "widgets_values": ["bypassed_alt_model.safetensors", "default"]},
        {"id": 3, "type": "UNETLoader", "mode": 0, "widgets_values": ["active_missing_model.safetensors", "default"]},
        {"id": 4, "type": "SaveImage", "mode": 0, "widgets_values": ["out/audit"]},
        {"id": 5, "type": "MarkdownNote", "mode": 0, "widgets_values": ["点击这里看说明"]},
        {"id": 6, "type": "SomeMissingCustomNode", "mode": 0, "widgets_values": [1]},
    ],
    "definitions": {"subgraphs": [
        {"id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "name": "My Subgraph", "nodes": [
            {"id": 7, "type": "VAELoader", "mode": 0, "widgets_values": ["ae.safetensors"]},
        ]},
    ]},
}
UI_OK_WORKFLOW = {
    "nodes": [
        {"id": 1, "type": "UNETLoader", "mode": 0, "widgets_values": ["z_image_turbo_bf16.safetensors", "default"]},
        {"id": 2, "type": "SaveImage", "mode": 0, "widgets_values": ["out/ok"]},
        {"id": 3, "type": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "mode": 0, "widgets_values": []},
        {"id": 4, "type": "MarkdownNote", "mode": 0, "widgets_values": ["note"]},
    ],
    # 真机上子图实例就是用子图的 UUID 当 `type`（实测 audio_minimax_music_3 /
    # image_z_image_turbo / video_minimax_h3_i2v 三个官方模板都是如此），
    # 所以审计必须先收 definitions.subgraphs 的 id，否则会把实例当成"缺节点类"
    "definitions": {"subgraphs": [
        {"id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "name": "Text to Image (mock)", "nodes": [
            {"id": 8, "type": "VAELoader", "mode": 0, "widgets_values": ["ae.safetensors"]},
        ]},
    ]},
}


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(ok), "" if ok else str(detail)))


def run(argv: list[str]) -> tuple[int, dict]:
    """跑一次 CLI，捕获 stdout 里的 JSON。"""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = cs.main(argv)
    text = buf.getvalue().strip()
    try:
        payload = json.loads(text) if text else {}
    except ValueError:
        payload = {"_raw": text}
    return code, payload


class _Handler(BaseHTTPRequestHandler):
    posts: list[tuple[str, dict]] = []
    uploads: list[bytes] = []

    def log_message(self, *a):  # 静音
        pass

    def _send(self, payload: bytes, ctype="application/json"):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        path, query = parsed.path, urllib.parse.parse_qs(parsed.query)
        if path == "/system_stats":
            return self._send(json.dumps(STATS).encode())
        if path == "/api/models":
            return self._send(json.dumps(sorted(MODELS)).encode())
        if path.startswith("/api/models/"):
            folder = urllib.parse.unquote(path.split("/api/models/", 1)[1])
            if folder not in MODELS:
                return self._not_found()
            return self._send(json.dumps(MODELS[folder]).encode())
        if path == "/api/object_info":
            return self._send(json.dumps(OBJECT_INFO).encode())
        if path == "/templates/index.json":
            return self._send(json.dumps(TEMPLATES).encode())
        if path.startswith("/templates/"):
            name = urllib.parse.unquote(path.split("/templates/", 1)[1])[:-len(".json")]
            if name == "image_z_image_turbo":
                return self._send(json.dumps(UI_OK_WORKFLOW).encode())
            if name == "audio_minimax_music_3":
                return self._send(json.dumps(UI_WORKFLOW).encode())
            return self._not_found()
        if path == "/api/userdata":
            return self._send(json.dumps(["image_z_image_turbo.json", "audio_minimax_music_3.json"]).encode())
        if path == "/history":
            limit = int((query.get("max_items") or ["20"])[0])
            entries = {}
            for i in range(min(limit, 3)):
                entries[f"pid-{i}"] = {
                    "status": {"status_str": "success", "completed": True},
                    "outputs": {
                        "9": {"images": [{"filename": f"shot_{i:05d}_.png", "subfolder": "img", "type": "output"}]},
                        "10": {"images": [{"filename": f"temp_{i:05d}_.png", "subfolder": "", "type": "temp"}]},
                    },
                }
            return self._send(json.dumps(entries).encode())
        if path.startswith("/history/"):
            pid = path.split("/history/", 1)[1]
            if pid != "pid-0":
                return self._not_found()
            return self._send(json.dumps({"pid-0": {
                "status": {"status_str": "success", "completed": True},
                "outputs": {
                    "9": {"images": [{"filename": "shot_00000_.png", "subfolder": "img", "type": "output"}]},
                    "10": {"images": [{"filename": "temp_00000_.png", "subfolder": "", "type": "temp"}]},
                    "11": {"audio": [{"filename": "bgm_00001_.mp3", "subfolder": "audio", "type": "output"}]},
                },
            }}).encode())
        if path == "/view":
            name = (query.get("filename") or [""])[0]
            return self._send(f"BYTES:{name}".encode(), "application/octet-stream")
        if path == "/queue":
            return self._send(json.dumps({
                "queue_running": [[0, "pid-running", {}, {}]],
                "queue_pending": [[1, "pid-pending", {}, {}]],
            }).encode())
        return self._not_found()

    def do_POST(self):  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length)
        if parsed.path == "/upload/image":
            type(self).uploads.append(body)
            return self._send(json.dumps({"name": "ref.png", "subfolder": "sub", "type": "input"}).encode())
        try:
            payload = json.loads(body or b"{}")
        except ValueError:
            payload = {}
        type(self).posts.append((parsed.path, payload))
        return self._send(b"{}")

    def _not_found(self):
        self.send_response(404)
        self.end_headers()


def _reset():
    _Handler.posts = []
    _Handler.uploads = []


# --------------------------------------------------------------------------- 测试
def test_readonly(base: str) -> None:
    code, p = run(["--check", "--server", base])
    check("--check 走通并报 ok", code == 0 and p.get("ok") is True, p)
    check("--check 报版本与模板版本",
          p.get("comfyui_version") == "1.2.3-test" and p.get("installed_templates_version") == "0.0.1-test", p)
    check("--check 汇总模型文件数与目录",
          p.get("model_files_total") == 5 and p.get("model_folders", {}).get("loras") == 1, p)
    check("--check 报显存与队列", p.get("vram_free_gb") == 6.0 and p.get("queue") == {"running": 1, "pending": 1}, p)

    code, s = run(["status", "--server", base])
    check("status 报设备与显存换算",
          code == 0 and s["devices"][0]["vram_free_gb"] == 6.0 and s["devices"][0]["torch_vram_free_gb"] == 5.0, s)
    check("status 报 RAM 换算与运行中 id",
          s["ram_total_gb"] == 64.0 and s["queue"]["running_ids"] == ["pid-running"], s)

    code, m = run(["models", "--server", base])
    check("models 跨目录列全部文件", code == 0 and m["count"] == 5, m)
    code, m = run(["models", "--folder", "loras", "--server", base])
    check("models --folder 只列该目录", m["count"] == 1 and m["items"][0]["folder"] == "loras", m)
    code, m = run(["models", "--search", "Z_IMAGE", "--server", base])
    check("models --search 大小写不敏感", m["count"] == 2, m)

    code, n = run(["nodes", "--server", base])
    check("nodes 列类名与总数", code == 0 and n["total_classes"] == 5 and n["count"] == 5, n)
    code, n = run(["nodes", "--search", "sampler", "--server", base])
    check("nodes --search 过滤", n["count"] == 1 and n["items"][0]["class"] == "KSampler", n)
    code, n = run(["nodes", "--class", "KSampler", "--server", base])
    check("nodes --class 出 required/optional 与默认值",
          n["required"]["steps"] == {"type": "INT", "default": 20, "min": 1, "max": 10000}, n.get("required"))
    check("nodes --class 把枚举摊成 choices",
          n["required"]["sampler_name"]["type"] == "CHOICE"
          and n["required"]["sampler_name"]["choices"] == ["euler", "dpmpp_2m"], n["required"])
    check("nodes --class 保留 outputs", n["outputs"] == ["LATENT"], n.get("outputs"))
    code, n = run(["nodes", "--class", "KSampl", "--server", base])
    check("nodes --class 打错一半 -> 退出 1 + 猜你想找",
          code == 1 and n["ok"] is False and n["did_you_mean"] == ["KSampler"], n)
    code, n = run(["nodes", "--class", "NoSuchNode", "--server", base])
    check("nodes --class 完全不认识 -> 退出 1 且建议列表为空",
          code == 1 and n["ok"] is False and n["did_you_mean"] == [], n)

    code, t = run(["templates", "--server", base])
    check("templates 摊平目录并统计 type", code == 0 and t["total"] == 3 and t["by_type"]["audio"] == 1, t)
    code, t = run(["templates", "--type", "video", "--server", base])
    check("templates --type 过滤", t["count"] == 1 and t["items"][0]["type"] == "video", t)
    code, t = run(["templates", "--search", "fastvideo", "--server", base])
    check("templates --search 命中 name", t["count"] == 1, t)
    code, t = run(["templates", "--search", "caption to music", "--server", base])
    check("templates --search 也搜 description", t["count"] == 1, t)
    code, t = run(["templates", "--limit", "1", "--server", base])
    check("templates --limit 生效", t["count"] == 1 and t["total"] == 3, t)

    code, w = run(["workflows", "--server", base])
    check("workflows 列 userdata", code == 0 and w["count"] == 2, w)
    code, w = run(["workflows", "--search", "audio", "--server", base])
    check("workflows --search 过滤", w["count"] == 1, w)

    code, h = run(["history", "--limit", "3", "--server", base])
    check("history 最近的在前", code == 0 and [r["prompt_id"] for r in h["items"]] == ["pid-2", "pid-1", "pid-0"], h)
    check("history 报每条产物数", h["items"][0]["file_count"] == 2, h)

    code, q = run(["queue", "--server", base])
    check("queue 分开报 running / pending",
          code == 0 and q["running"] == 1 and q["pending"] == 1 and len(q["items"]) == 2, q)


def test_history_download(base: str) -> None:
    out_dir = tempfile.mkdtemp(prefix="server-skill-")
    try:
        code, d = run(["history", "--download", "pid-0", "--out-dir", out_dir, "--server", base])
        names = sorted(os.path.basename(p) for p in d.get("local_paths", []))
        check("history --download 存下产出的字节",
              code == 0 and names == ["bgm_00001_.mp3", "shot_00000_.png"], d.get("local_paths"))
        check("history --download 默认跳过 temp",
              len(d.get("skipped_temp", [])) == 1 and d["skipped_temp"][0]["filename"] == "temp_00000_.png", d)
        png = os.path.join(out_dir, "img", "shot_00000_.png")
        check("history --download 保留 subfolder 结构",
              os.path.isfile(png) and open(png, "rb").read() == b"BYTES:shot_00000_.png")

        code, d = run(["history", "--download", "pid-0", "--out-dir", out_dir,
                       "--include-temp", "--server", base])
        check("history --download --include-temp 连 temp 一起下",
              any(p.endswith("temp_00000_.png") for p in d.get("local_paths", [])), d.get("local_paths"))

        code, d = run(["history", "--download", "nope", "--server", base])
        check("history --download 未知 id -> 退出 1", code == 1 and d["ok"] is False, d)
    finally:
        shutil.rmtree(out_dir, ignore_errors=True)


def test_templates_pull(base: str) -> None:
    out_dir = tempfile.mkdtemp(prefix="server-skill-")
    try:
        code, t = run(["templates", "--pull", "image_z_image_turbo", "--out-dir", out_dir, "--server", base])
        path = t.get("path", "")
        check("templates --pull 落盘 UI 工作流", code == 0 and os.path.isfile(path), t)
        check("templates --pull 报 sha256 与字节数",
              t.get("sha256") == hashlib.sha256(open(path, "rb").read()).hexdigest() and t.get("bytes") > 0, t)
        meta = t.get("meta_path", "")
        check("templates --pull 写 meta 并存来源 URL",
              os.path.isfile(meta) and json.load(open(meta, encoding="utf-8"))["source"].endswith(
                  "/templates/image_z_image_turbo.json"), meta)
        check("templates --pull 报输出节点", t.get("output_nodes") == ["SaveImage"], t.get("output_nodes"))

        code, t = run(["templates", "--pull", "no_such_template", "--server", base])
        check("templates --pull 未知名字 -> 退出 1 + 猜你想找",
              code == 1 and t["ok"] is False and t["did_you_mean"] == [], t)

        code, t = run(["templates", "--pull", "audio_minimax_music_3", "--audit",
                       "--out-dir", out_dir, "--server", base])
        check("templates --pull --audit 顺带审计（bypass 的权重不算缺）",
              code == 0 and t["audit"]["missing_models"] == ["active_missing_model.safetensors"], t.get("audit"))
    finally:
        shutil.rmtree(out_dir, ignore_errors=True)


def test_audit(base: str) -> None:
    code, a = run(["audit", "--template", "audio_minimax_music_3", "--server", base])
    check("audit --template：bypass 分支引用的权重不进 missing_models",
          a["missing_models"] == ["active_missing_model.safetensors"], a.get("missing_models"))
    check("audit --template：bypass 引用的权重单独列出",
          a["bypassed_models"] == ["bypassed_alt_model.safetensors"], a.get("bypassed_models"))
    check("audit --template：子图内节点也被扫到（ae.safetensors 在 active）",
          "ae.safetensors" in a["active_models"], a.get("active_models"))
    check("audit --template：缺的自定义节点算 blocking",
          a["missing_nodes"] == ["SomeMissingCustomNode"], a.get("missing_nodes"))
    check("audit --template：UI 专有节点单列、不算 blocking",
          a["ui_only_nodes"] == ["MarkdownNote"], a.get("ui_only_nodes"))
    check("audit --template：runnable=False -> 退出 1", code == 1 and a["ok"] is False, a)
    check("audit --template：报输出节点", a["output_nodes"] == ["SaveImage"], a.get("output_nodes"))

    path = os.path.join(tempfile.mkdtemp(prefix="server-skill-"), "ok.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(UI_OK_WORKFLOW, open(path, "w", encoding="utf-8"))
    code, a = run(["audit", "--workflow", path, "--server", base])
    check("audit --workflow：权重/节点齐 -> runnable=True、退出 0",
          code == 0 and a["ok"] is True and a["missing_models"] == [] and a["missing_nodes"] == [], a)
    check("audit --workflow：子图定义 node 不当成缺失类",
          a["missing_nodes"] == [], a.get("missing_nodes"))

    code, a = run(["audit", "--workflow", "/no/such/file.json", "--server", base])
    check("audit --workflow 文件不存在 -> 退出 1", code == 1 and a["ok"] is False, a)
    code, a = run(["audit", "--server", base])
    check("audit 不给目标 -> 用法错误退出 2", code == 2, a)


def test_write_guards(base: str) -> None:
    for verb, argv in (("interrupt", []), ("free", []), ("clear-queue", [])):
        _reset()
        code, p = run([verb, "--server", base, *argv])
        check(f"{verb} 没有 --yes -> 退出 3 且不发请求",
              code == 3 and p.get("blocked") and not _Handler.posts, (code, p, _Handler.posts))
    _reset()
    code, p = run(["free", "--yes", "--server", base])
    check("free --yes 只回收缓存（默认不卸权重）",
          code == 0 and _Handler.posts == [("/free", {"unload_models": False, "free_memory": True})],
          _Handler.posts)
    _reset()
    code, p = run(["free", "--yes", "--unload-models", "--server", base])
    check("free --yes --unload-models 带上卸载开关",
          _Handler.posts == [("/free", {"unload_models": True, "free_memory": True})], _Handler.posts)
    _reset()
    code, p = run(["clear-queue", "--yes", "--server", base])
    check("clear-queue --yes 发 {clear: true} 并报清了几条",
          _Handler.posts == [("/queue", {"clear": True})] and p.get("cleared_pending") == 1, (p, _Handler.posts))
    _reset()
    code, p = run(["interrupt", "--yes", "--server", base])
    check("interrupt --yes 报打断了几条在跑的",
          _Handler.posts == [("/interrupt", {})] and p.get("interrupted_running") == 1, (p, _Handler.posts))
    _reset()
    code, p = run(["interrupt", "--server", base, "--format", "text"])
    check("--format text 的拦截提示也是可读文本", code == 3, p)


def test_upload(base: str) -> None:
    _reset()
    tmp = tempfile.mkdtemp(prefix="server-skill-")
    src = os.path.join(tmp, "ref.png")
    open(src, "wb").write(b"\x89PNG\r\n\x1a\nfake")
    try:
        code, p = run(["upload", "--file", src, "--subfolder", "sub", "--server", base])
        check("upload 回报带 subfolder 的 widget 值",
              code == 0 and p.get("uploaded") == "sub/ref.png" and p.get("widget_value") == "sub/ref.png", p)
        body = _Handler.uploads[-1] if _Handler.uploads else b""
        check("upload body 是合法 multipart", b'name="image"' in body and b'filename="ref.png"' in body
              and body.endswith(b"--\r\n"), body[:80])
        check("upload body 带上 overwrite=1 / type=input / subfolder",
              b'name="overwrite"' in body and b"input" in body and b'name="subfolder"' in body, "")
        code, p = run(["upload", "--file", "/no/such.png", "--server", base])
        check("upload 文件不存在 -> 退出 1", code == 1 and p["ok"] is False, p)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_formats_and_errors(base: str) -> None:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = cs.main(["models", "--folder", "loras", "--server", base, "--format", "text"])
    out = buf.getvalue()
    check("--format text 出表格（含表头与计数）",
          code == 0 and "folder" in out and "loras" in out and "items: 1" in out, out)

    code, p = run(["status", "--server", "http://127.0.0.1:1"])
    check("服务器不可达 -> ok=false、退出 1、带排查提示",
          code == 1 and p["ok"] is False and "不可达" in p["error"], p)
    code, p = run(["nodes", "--class", "KSampler", "--server", "http://127.0.0.1:1"])
    check("不可达时报错不吐 traceback", code == 1 and isinstance(p.get("error"), str), p)

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = cs.main([])
    check("没有子命令 -> 打印帮助并返回 2", code == 2 and "usage" in buf.getvalue().lower(), code)


def main() -> int:
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        groups = [("readonly", test_readonly), ("history/download", test_history_download),
                  ("templates/pull", test_templates_pull), ("audit", test_audit),
                  ("写操作护栏", test_write_guards), ("upload", test_upload),
                  ("格式与报错", test_formats_and_errors)]
        for label, fn in groups:
            before = len(RESULTS)
            fn(base)
            ok = all(ok for _, ok, _ in RESULTS[before:])
            print(f"{label}: {'OK' if ok else 'FAILED'}")
    finally:
        server.shutdown()

    failed = [(n, d) for n, ok, d in RESULTS if not ok]
    for name, detail in failed:
        print(f"  FAIL: {name}" + (f"  -> {detail}" if detail else ""))
    print(f"{len(RESULTS) - len(failed)}/{len(RESULTS)} checks passed")
    print("RESULT: " + ("PASS" if not failed else "FAIL"))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
