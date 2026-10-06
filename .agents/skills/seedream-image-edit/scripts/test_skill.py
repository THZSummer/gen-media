#!/usr/bin/env python3
"""seedream-image-edit 的离线自检：不花钱、不联网、不需要凭据。

覆盖四块：

  1. **转换**：UI 工作流（带 `MarkdownNote` + `Painter` + `PreviewImage`）-> API 图的形状，
     并与"真机实测接受过的那张图"（references/accepted-api-graph.json）逐字节比对；
  2. **接线**：单参考 / 双参考 / 带标注 / 不带标注四条支路的 `model.images.image_N` 落点；
  3. **参数面**：`--size auto`（按底图比例挑预设）、PNG/JPEG 读尺寸、参考图上限、
     "有参考图不能关 thinking"这条服务器事实要在本地就被拦住；
  4. **往返**：内置 mock ComfyUI 跑完 上传 -> /prompt -> /history -> /view，
     验证上传的 multipart、参考图接线、合成结果下载与留档不含明文凭据。

Run:
  python3 scripts/test_skill.py
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _shared  # noqa: E402

_shared.ensure()
import seedream_api as A  # noqa: E402
import seedream_gen as G  # noqa: E402
import seedream_edit as E  # noqa: E402
from seedream_edit_graph import (  # noqa: E402
    auto_size, build_edit_graph, default_model, image_size, jpeg_size, max_refs, png_size,
    supports_thinking,
)

FIXTURE_PATH = os.path.normpath(os.path.join(HERE, "..", "references",
                                             "accepted-api-graph.json"))
INFO = A.load_node_info(A.DEFAULT_NODE_INFO)
UI = A.load_workflow(E.DEFAULT_WORKFLOW)
FIXTURE = json.load(open(FIXTURE_PATH, encoding="utf-8"))
PROBE = FIXTURE["_probe"]

# 1x1 PNG / 3x2 JPEG（离线造图，不依赖 Pillow）
PNG_1x1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
)
JPEG_3x2 = base64.b64decode(
    "/9j/4AAQSkZJRgABAgAAAQABAAD//gAQTGF2YzYyLjExLjEwMAD/2wBDAAgEBAQEBAUFBQUFBQYGBgYG"
    "BgYGBgYGBgYHBwcICAgHBwcGBgcHCAgICAkJCQgICAgJCQoKCgwMCwsODg4RERT/xABMAAEBAAAAAAAA"
    "AAAAAAAAAAAABgEBAQAAAAAAAAAAAAAAAAAABgcQAQAAAAAAAAAAAAAAAAAAAAARAQAAAAAAAAAAAAAA"
    "AAAAAAD/wAARCAACAAMDASIAAhEAAxEA/9oADAMBAAIRAxEAPwCLAE1/f//Z"
)


def _graph(api: dict) -> dict:
    """整节点比对：fixture 就是当初提交上去的那张图（`_meta` 也在内）。"""
    return api


def _link_ids(api: dict) -> set[str]:
    return {str(v[0]) for node in api.values() for v in node["inputs"].values()
            if isinstance(v, list) and v}


def _write_png(path: str) -> str:
    with open(path, "wb") as fh:
        fh.write(PNG_1x1)
    return path


# --------------------------------------------------------------------------
# 1. 转换 + 与真机接受的图逐字节比对
# --------------------------------------------------------------------------
def check_conversion() -> list[str]:
    bad: list[str] = []
    asset = os.path.join(HERE, "..", "assets", "seedream-5.0-pro-image-edit-ui.json")
    digest = hashlib.sha256(open(asset, "rb").read()).hexdigest()
    if digest != PROBE["workflow_sha256"]:
        bad.append(f"工作流资产变了（sha256 {digest[:12]}… != fixture 记录的 "
                   f"{PROBE['workflow_sha256'][:12]}…）：要重录 fixture")

    if default_model(UI) != "seedream 5.0 pro":
        bad.append(f"default_model 读到的不是 seedream 5.0 pro：{default_model(UI)!r}")

    api, save_id, meta = build_edit_graph(
        UI, [PROBE["uploaded"]["ref"]], PROBE["uploaded"]["annotate"],
        base_size=tuple(PROBE["ref_size"]))
    api, _report = A.apply_params(api, {
        "prompt": PROBE["prompt"], "size": PROBE["size_auto"], "filename_prefix": PROBE["prefix"],
    }, INFO)
    if save_id != FIXTURE["graph"][meta["save_node"]]["class_type"] and save_id is None:
        bad.append("找不到保存节点")
    built, accepted = _graph(api), FIXTURE["graph"]
    if built != accepted:
        only_built = sorted(set(built) - set(accepted))
        only_acc = sorted(set(accepted) - set(built))
        diff = [nid for nid in set(built) & set(accepted) if built[nid] != accepted[nid]]
        bad.append(f"生成的 API 图与真机接受的图不一致：多节点{only_built} 少节点{only_acc} "
                   f"内容不同{diff}")

    if set(_link_ids(api)) - set(api):
        bad.append("图里有指向不存在节点的连线")
    if A.validate_graph(api, INFO):
        bad.append(f"本地 schema 校验没过：{A.validate_graph(api, INFO)}")
    if meta["composite_node"] != meta["annotate_node"]:
        bad.append("标注支路的 Painter 节点没有同时被当成合成结果来源")
    return bad


# --------------------------------------------------------------------------
# 2. 四条接线
# --------------------------------------------------------------------------
def check_wiring() -> list[str]:
    bad: list[str] = []
    base = (1024, 1360)

    # 不带标注：Painter 必须整条删掉，image_1 直接吃 LoadImage
    api, _save, meta = build_edit_graph(UI, ["a.png"], None, base_size=base)
    classes = {n["class_type"] for n in api.values()}
    if "Painter" in classes or "PreviewImage" in classes or "MarkdownNote" in classes:
        bad.append(f"不带标注时还留着界面节点：{classes}")
    seed_id = meta["seed_node"]
    if api[seed_id]["inputs"].get("model.images.image_1") != [meta["ref_nodes"][0], 0]:
        bad.append("image_1 没有直接接到 LoadImage")
    if not any(d["class"] == "Painter" for d in meta["dropped"]):
        bad.append("删掉的 Painter 没有出现在 dropped 报告里")

    # 带标注：LoadImage -> Painter -> image_1，Painter 画布 = 底图尺寸
    api, _save, meta = build_edit_graph(UI, ["a.png"], "marks.png", base_size=base)
    painter = meta["annotate_node"]
    if painter is None or api[painter]["class_type"] != "Painter":
        bad.append("带标注时没有留下 Painter")
    else:
        inputs = api[painter]["inputs"]
        if inputs.get("mask") != "marks.png":
            bad.append(f"Painter.mask 不是标注层：{inputs.get('mask')!r}")
        if (inputs.get("width"), inputs.get("height")) != base:
            bad.append(f"Painter 画布不是底图尺寸：{inputs.get('width')}x{inputs.get('height')}")
        if inputs.get("image") != [meta["ref_nodes"][0], 0]:
            bad.append("Painter 没有吃到 LoadImage 的底图")
        if api[meta["seed_node"]]["inputs"].get("model.images.image_1") != [painter, 0]:
            bad.append("image_1 没有接到 Painter")

    # 双参考：image_2 接到新 LoadImage，且没有撞 id
    api, _save, meta = build_edit_graph(UI, ["a.png", "b.png"], None, base_size=base)
    if len(meta["ref_nodes"]) != 2 or len(set(meta["ref_nodes"])) != 2:
        bad.append(f"两张参考图没有各自一个 LoadImage：{meta['ref_nodes']}")
    if meta["ref_keys"] != ["model.images.image_1", "model.images.image_2"]:
        bad.append(f"参考图键名不对：{meta['ref_keys']}")
    second = api[meta["seed_node"]]["inputs"].get("model.images.image_2")
    if not second or api[second[0]]["class_type"] != "LoadImage":
        bad.append("image_2 没有接到第二个 LoadImage")
    if api[second[0]]["inputs"]["image"] != "b.png":
        bad.append("第二个 LoadImage 吃错了文件")

    # 带标注 + 保留预览：PreviewImage 留着，图仍然合法
    api, _save, _meta = build_edit_graph(UI, ["a.png"], "marks.png", base_size=base,
                                        drop_preview=False)
    if "PreviewImage" not in {n["class_type"] for n in api.values()}:
        bad.append("annotate + drop_preview=False 时 PreviewImage 不该被删")
    if A.validate_graph(api, INFO):
        bad.append(f"保留 PreviewImage 的图没过本地校验：{A.validate_graph(api, INFO)}")

    # 不带标注 + 保留预览：Painter 被删，它的下游 PreviewImage 只能级联删掉（否则断线）
    api, _save, meta = build_edit_graph(UI, ["a.png"], None, base_size=base,
                                        drop_preview=False)
    if "PreviewImage" in {n["class_type"] for n in api.values()}:
        bad.append("删掉 Painter 后 PreviewImage 还在：它会变成一张断线的图")
    if set(_link_ids(api)) - set(api):
        bad.append("删 Painter 后留下了断线")
    if not any(d["why"].startswith("上游被删") for d in meta["dropped"]):
        bad.append(f"级联删除没有出现在 dropped 报告里：{meta['dropped']}")

    # 没有参考图 -> 必须报错并指向姊妹技能
    try:
        build_edit_graph(UI, [], None)
        bad.append("不给参考图竟然建了图")
    except A.InvalidValueError as exc:
        if "seedream-text-to-image" not in str(exc):
            bad.append("不给参考图的报错没有指向姊妹技能")
    return bad


# --------------------------------------------------------------------------
# 3. 参数面
# --------------------------------------------------------------------------
def check_params() -> list[str]:
    bad: list[str] = []

    # --size auto：按底图比例挑预设
    cases = [
        ("seedream 5.0 pro", 1024, 1360, None, "(1K) 864x1152 (3:4)"),
        ("seedream 5.0 pro", 1024, 1024, None, "(1K) 1024x1024 (1:1)"),
        ("seedream 5.0 pro", 1024, 1024, "2K", "(2K) 2048x2048 (1:1)"),
        ("seedream 5.0 lite", 1024, 1360, None, "(2K) 1728x2304 (3:4)"),
    ]
    for model, width, height, tier, want in cases:
        got = auto_size(INFO, model, width, height, tier)["preset"]
        if got != want:
            bad.append(f"auto_size({model}, {width}x{height}, tier={tier}) = {got!r}，应为 {want!r}")
    try:
        auto_size(INFO, "seedream 5.0 pro", 1024, 1024, "9K")
        bad.append("不存在的档位没有被拦下")
    except A.InvalidValueError:
        pass

    # 参考图上限 / thinking 开关：从 schema 的 tooltip 与选项里读
    if max_refs(INFO, "seedream 5.0 pro") != 10:
        bad.append(f"pro 的参考图上限读成了 {max_refs(INFO, 'seedream 5.0 pro')}")
    if max_refs(INFO, "seedream 5.0 lite") != 14:
        bad.append(f"lite 的参考图上限读成了 {max_refs(INFO, 'seedream 5.0 lite')}")
    if not supports_thinking(INFO, "seedream 5.0 pro"):
        bad.append("pro 应当有 thinking")
    if supports_thinking(INFO, "seedream 5.0 flash"):
        bad.append("flash 不该有 thinking")

    # 读尺寸：PNG 走 IHDR，JPEG 扫 SOF，认不出的要报错
    with tempfile.TemporaryDirectory() as tmp:
        png = _write_png(os.path.join(tmp, "p.png"))
        jpg = os.path.join(tmp, "j.jpg")
        with open(jpg, "wb") as fh:
            fh.write(JPEG_3x2)
        if png_size(png) != (1, 1) or image_size(png) != (1, 1):
            bad.append(f"PNG 尺寸读成了 {image_size(png)}，应为 (1, 1)")
        if jpeg_size(jpg) != (3, 2) or image_size(jpg) != (3, 2):
            bad.append(f"JPEG 尺寸读成了 {image_size(jpg)}，应为 (3, 2)")
        weird = os.path.join(tmp, "w.bmp")
        with open(weird, "wb") as fh:
            fh.write(b"BM" + b"\x00" * 40)
        try:
            image_size(weird)
            bad.append("不认得的格式没有被拦下")
        except A.InvalidValueError:
            pass

        # 服务器事实：有参考图不能关 thinking —— 本地就要拦住（不联网，上传之前就报）
        try:
            E.generate(images=[png], prompt="x", thinking=False, quiet=True)
            bad.append("有参考图 + --no-thinking 没有被拦住")
        except A.InvalidValueError as exc:
            if "thinking" not in str(exc):
                bad.append(f"thinking 的报错信息没提 thinking：{exc}")
        # 未知模型
        try:
            E.generate(images=[png], prompt="x", model="seedream 9.9", quiet=True)
            bad.append("未知模型没有被拦住")
        except A.UnknownModelError:
            pass
        # 超过参考图上限
        try:
            E.generate(images=[png] * 11, prompt="x", quiet=True)
            bad.append("11 张参考图（pro 上限 10）没有被拦住")
        except A.InvalidValueError as exc:
            if "10" not in str(exc):
                bad.append(f"参考图超限的报错没提上限：{exc}")
        # 文件不存在
        try:
            E.generate(images=[os.path.join(tmp, "nope.png")], prompt="x", quiet=True)
            bad.append("不存在的参考图没有被拦住")
        except A.InvalidValueError:
            pass
    return bad


def check_prune() -> list[str]:
    """前端专有节点：静态名单与实际 /object_info 两条判据都要能剔干净。"""
    bad: list[str] = []
    api = {
        "1": {"class_type": "LoadImage", "inputs": {"image": "a.png"},
              "_meta": {"title": "LoadImage"}},
        "2": {"class_type": "MarkdownNote", "inputs": {"text": "note"},
              "_meta": {"title": "note"}},
    }
    pruned, dropped = A.prune_ui_only(api)
    if "2" in pruned or len(dropped) != 1:
        bad.append(f"静态名单没有剔掉 MarkdownNote：{pruned} {dropped}")
    api = {
        "1": {"class_type": "LoadImage", "inputs": {"image": "a.png"},
              "_meta": {"title": "LoadImage"}},
        "2": {"class_type": "SomeFrontendThing", "inputs": {},
              "_meta": {"title": "x"}},
    }
    pruned, dropped = A.prune_ui_only(api, known_classes={"LoadImage"})
    if "2" in pruned:
        bad.append("按真机类名名单没有剔掉未知节点")
    # 断线要清掉：被删节点的下游输入不能留
    api = {
        "1": {"class_type": "PreviewImage", "inputs": {"images": ["2", 0]},
              "_meta": {"title": "p"}},
        "2": {"class_type": "MarkdownNote", "inputs": {}, "_meta": {"title": "n"}},
    }
    pruned, _dropped = A.prune_ui_only(api)
    if pruned["1"]["inputs"]:
        bad.append(f"删掉上游后还留着断线输入：{pruned['1']['inputs']}")
    return bad


# --------------------------------------------------------------------------
# 4. mock ComfyUI 往返
# --------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    submitted: list = []
    uploads: list = []

    def log_message(self, *_args):  # noqa: D102 - 静音
        pass

    def _json(self, payload, code=200):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length)
        if self.path.startswith("/upload/image"):
            body = raw.decode("utf-8", "replace")
            name = body.split('filename="')[1].split('"')[0]
            Handler.uploads.append(name)
            return self._json({"name": f"up-{name}", "subfolder": "", "type": "input"})
        if self.path.startswith("/prompt"):
            Handler.submitted.append(json.loads(raw.decode()))
            return self._json({"prompt_id": "p1"})
        return self._json({"error": "no"}, 404)

    def do_GET(self):  # noqa: N802
        if self.path.startswith("/history/p1"):
            return self._json({"p1": {
                "status": {"status_str": "success",
                           "messages": [["execution_success", {}]]},
                "outputs": {
                    "2": {"images": [{"filename": "edited_00001_.png", "subfolder": "",
                                      "type": "output"}]},
                    "7": {"images": [{"filename": "composite_00001_.png", "subfolder": "",
                                      "type": "temp"}]},
                }}})
        if self.path.startswith("/view"):
            body = PNG_1x1
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        return self._json({"error": "no"}, 404)


def check_roundtrip(tmp: str) -> list[str]:
    bad: list[str] = []
    Handler.submitted, Handler.uploads = [], []
    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}"
    try:
        base = _write_png(os.path.join(tmp, "base.png"))
        marks = _write_png(os.path.join(tmp, "marks.png"))
        out = os.path.join(tmp, "out")
        result = E.generate(server=url, images=[base], annotate=marks, prompt="改成纯黑",
                            api_key="test-key-123", key_file=None, out_dir=out,
                            quiet=True, timeout=30)
        payload = Handler.submitted[0]
        if payload["extra_data"] != {"api_key_comfy_org": "test-key-123"}:
            bad.append(f"凭据通道不对：{payload.get('extra_data')}")
        graph = payload["prompt"]
        seed_id = next(nid for nid, n in graph.items()
                       if n["class_type"] == A.SEEDREAM_CLASS)
        painter_id = next(nid for nid, n in graph.items() if n["class_type"] == "Painter")
        if graph[seed_id]["inputs"]["model.images.image_1"] != [painter_id, 0]:
            bad.append("提交的图里 image_1 没接到 Painter")
        if graph[painter_id]["inputs"]["mask"] != "up-marks.png":
            bad.append(f"Painter.mask 不是上传后的名字：{graph[painter_id]['inputs']['mask']!r}")
        if graph["3"]["inputs"]["image"] != "up-base.png":
            bad.append(f"LoadImage 没吃到上传后的名字：{graph['3']['inputs']['image']!r}")
        if result["credential_channel"] != "api_key":
            bad.append(f"摘要里的凭据通道不对：{result['credential_channel']}")
        if len(result["local_paths"]) != 1:
            bad.append(f"成品下载数量不对：{result['local_paths']}")
        if len(result["composite_paths"]) != 1 or "composite" not in os.path.basename(
                result["composite_paths"][0]):
            bad.append(f"合成结果没有下载/改名：{result['composite_paths']}")
        # 留档里不能出现明文凭据
        with open(os.path.join(out, "requests.jsonl"), encoding="utf-8") as fh:
            blob = fh.read()
        if "test-key-123" in blob or "test-key-123" in json.dumps(graph):
            bad.append("留档里出现了明文凭据")
        for entry in (json.loads(line) for line in blob.splitlines() if line.strip()):
            if entry.get("credential_channel") != "api_key":
                bad.append(f"requests.jsonl 的凭据通道不对：{entry.get('credential_channel')}")
            if entry.get("ref_keys") != ["model.images.image_1"]:
                bad.append(f"requests.jsonl 没记参考图接线：{entry.get('ref_keys')}")
        # --dry-run 不联网（mock 服务器的上传计数不应当再涨）
        before = len(Handler.uploads)
        dry = E.generate(server="http://127.0.0.1:1", images=[base], prompt="x",
                         dry_run=True, quiet=True)
        if not dry.get("dry_run") or len(Handler.uploads) != before:
            bad.append("--dry-run 竟然联网了")
    finally:
        server.shutdown()
        server.server_close()
    return bad


def check_check_command() -> list[str]:
    bad: list[str] = []
    result, code = E.run_check("http://127.0.0.1:1")
    if code != E.EXIT_UNREACHABLE or result["reachable"]:
        bad.append(f"不可达的服务器没有给出 EXIT_UNREACHABLE：{code}")
    return bad


def main() -> int:
    failures = check_conversion()
    print(f"conversion（与真机接受的图逐字节比对）: {'OK' if not failures else 'FAIL'}")
    wiring = check_wiring()
    failures += wiring
    print(f"wiring（单/双参考 · 带/不带标注）: {'OK' if not wiring else 'FAIL'}")
    params = check_params()
    failures += params
    print(f"params（auto 尺寸 / 上限 / thinking / 格式）: {'OK' if not params else 'FAIL'}")
    prune = check_prune()
    failures += prune
    print(f"prune（前端专有节点）: {'OK' if not prune else 'FAIL'}")
    with tempfile.TemporaryDirectory() as tmp:
        roundtrip = check_roundtrip(tmp)
    failures += roundtrip
    print(f"mock roundtrip（上传 -> 排队 -> 下载）: {'OK' if not roundtrip else 'FAIL'}")
    check = check_check_command()
    failures += check
    print(f"unreachable server: {'OK' if not check else 'FAIL'}")
    for item in failures:
        print("  -", item)
    print("RESULT:", "PASS" if not failures else "FAIL")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
