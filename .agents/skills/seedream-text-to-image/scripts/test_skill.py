#!/usr/bin/env python3
"""seedream-text-to-image 的离线自检：不花钱、不联网、不需要凭据。

覆盖三块：

  1. **转换**：UI 工作流 -> API 图的形状（带点输入名、伪 widget 不进图、连线正确、
     与真机实测接受的那张图逐字节一致）；
  2. **参数面**：按 schema 判"这个模型到底支不支持这个参数"——支持的要落进图，
     不支持的必须报错而不是被静默丢掉；尺寸三种写法、Custom 边界、保存格式切换；
  3. **往返**：内置 mock ComfyUI 跑完 /prompt -> /history -> /view，
     并分别验证"带凭据/不带凭据"的 payload、鉴权失败/节点报错/被拒/超时的分类。

Run:
  python3 scripts/test_skill.py
"""
from __future__ import annotations

import base64
import json
import os
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import seedream_api as sa  # noqa: E402
import seedream_gen as sg  # noqa: E402

PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
)
FIXTURE = sa.load_node_info(sa.DEFAULT_NODE_INFO)
# 真机实测被服务器接受的那张图（POST /prompt -> 200 + prompt_id），逐字节比对用
ACCEPTED_GRAPH = {
    "2": {"class_type": "SaveImageAdvanced", "inputs": {
        "images": ["3", 0], "filename_prefix": "Seedream5.0_Pro_T2I", "format": "png",
        "format.bit_depth": "8-bit", "format.input_color_space": "sRGB"}},
    "3": {"class_type": "ByteDanceSeedreamNodeV3", "inputs": {
        "prompt": "九尾狐 素描 线稿", "model": "seedream 5.0 pro",
        "model.size_preset": "(1K) 1024x1024 (1:1)", "model.width": 2048, "model.height": 2048,
        "model.prompt_optimization": "standard", "model.seed": 1766827367,
        "model.watermark": False, "model.thinking": True}},
}


def _strip_meta(api: dict) -> dict:
    return {nid: {"class_type": n["class_type"], "inputs": n["inputs"]} for nid, n in api.items()}


# --------------------------------------------------------------------------
# mock ComfyUI
# --------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    submitted: list = []
    mode = "ok"          # ok | unauth | node_error
    answer = True        # False -> /history 永远空（测超时）
    reject = False       # True -> /prompt 返回 400

    def log_message(self, *args):
        pass

    def _json(self, payload, code=200):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/system_stats"):
            return self._json({"system": {"comfyui_version": "mock-0.38.0"}})
        if self.path.startswith("/object_info/"):
            cls = self.path.rsplit("/", 1)[-1]
            if cls in FIXTURE["nodes"]:
                return self._json({cls: FIXTURE["nodes"][cls]})
            return self._json({}, 404)
        if self.path.startswith("/history/"):
            pid = self.path.rsplit("/", 1)[-1]
            if not Handler.answer:
                return self._json({})
            status = {"status_str": "success", "completed": True, "messages": [
                ["execution_start", {"prompt_id": pid}],
                ["execution_cached", {"nodes": ["2", "3"], "prompt_id": pid}]]}
            if Handler.mode == "unauth":
                status = {"status_str": "error", "completed": False, "messages": [
                    ["execution_error", {"node_id": "3", "node_type": "ByteDanceSeedreamNodeV3",
                                         "exception_message": "Unauthorized: Please login first"
                                                              " to use this node.\n"}]]}
            elif Handler.mode == "node_error":
                status = {"status_str": "error", "completed": False, "messages": [
                    ["execution_error", {"node_id": "3", "node_type": "ByteDanceSeedreamNodeV3",
                                         "exception_message": "prompt rejected by safety"}]]}
            return self._json({pid: {"status": status, "outputs": {
                "2": {"images": [{"filename": f"mock_{pid[:8]}_.png", "subfolder": "",
                                  "type": "output"}]}}}})
        if self.path.startswith("/view?"):
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", str(len(PNG)))
            self.end_headers()
            self.wfile.write(PNG)
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        if self.path.startswith("/prompt"):
            if Handler.reject:
                return self._json({"error": {"type": "prompt_outputs_failed_validation",
                                             "message": "Required input is missing: model.height"}},
                                  400)
            payload = json.loads(raw or b"{}")
            Handler.submitted.append(payload)
            return self._json({"prompt_id": "mock-seedream-id", "number": 1, "node_errors": {}})
        self.send_response(404)
        self.end_headers()


def start_mock():
    server = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host, port = server.server_address
    return server, f"http://{host}:{port}"


def _reset(mode="ok", answer=True, reject=False):
    Handler.mode, Handler.answer, Handler.reject = mode, answer, reject
    Handler.submitted.clear()


# --------------------------------------------------------------------------
# 1) 转换
# --------------------------------------------------------------------------
def check_conversion() -> list[str]:
    failures: list[str] = []
    ui = sa.load_workflow(sa.DEFAULT_WORKFLOW)
    api, save_id = sa.build_api_graph(ui)
    if save_id != "2":
        failures.append(f"保存节点应为 2，得到 {save_id}")
    got = _strip_meta(api)
    if got != ACCEPTED_GRAPH:
        failures.append("转换结果与真机实测接受的那张图不一致：\n"
                        f"    got  = {json.dumps(got, ensure_ascii=False, sort_keys=True)}\n"
                        f"    want = {json.dumps(ACCEPTED_GRAPH, ensure_ascii=False, sort_keys=True)}")
    dumped = json.dumps(api, ensure_ascii=False)
    if "control_after_generate" in dumped:
        failures.append("前端伪 widget control_after_generate 进了 API 图")
    if not failures:
        # 幂等：同样的输入必须给出逐字节相同的图
        again, _ = sa.build_api_graph(sa.load_workflow(sa.DEFAULT_WORKFLOW))
        if json.dumps(again, sort_keys=True) != json.dumps(api, sort_keys=True):
            failures.append("同一个工作流转两次得到的 API 图不同")
    problems = sa.validate_graph(api, FIXTURE)
    if problems:
        failures.append(f"自带工作流没过本地 schema 校验：{problems}")
    # mute/bypass 的节点要消失
    muted = json.loads(json.dumps(ui))
    muted["nodes"][0]["mode"] = 4
    api_muted, save_muted = sa.build_api_graph(muted)
    if save_muted is not None or len(api_muted) != 1:
        failures.append("bypass 的保存节点没有被丢掉")
    return failures


# --------------------------------------------------------------------------
# 2) 参数面
# --------------------------------------------------------------------------
def _apply(params, expect_error=None, strict=True):
    api, _ = sa.build_api_graph(sa.load_workflow(sa.DEFAULT_WORKFLOW))
    try:
        new, report = sa.apply_params(api, params, FIXTURE, strict=strict)
    except (sa.UnappliedOverrideError, sa.UnknownModelError, sa.InvalidValueError) as exc:
        if expect_error is None:
            raise AssertionError(f"不该报错却报错：{type(exc).__name__}: {exc}") from exc
        if not isinstance(exc, expect_error):
            raise AssertionError(f"期望 {expect_error.__name__}，得到 {type(exc).__name__}: {exc}")
        return None, str(exc)
    if expect_error is not None:
        raise AssertionError(f"期望 {expect_error.__name__}，但没有报错")
    return new, report


def check_params() -> list[str]:
    failures: list[str] = []

    # ---- 各模型参数面（真机 schema 快照）
    expect_support = {
        "seedream 5.0 pro": {"prompt_optimization": True, "thinking": True, "max_images": False},
        "seedream 5.0 flash": {"prompt_optimization": False, "thinking": False, "max_images": False},
        "seedream 5.0 lite": {"prompt_optimization": False, "thinking": True, "max_images": True},
        "seedream-4-5-251128": {"thinking": True, "max_images": True},
        "seedream-4-0-250828": {"thinking": True, "max_images": True},
    }
    if set(expect_support) - set(sa.model_keys(FIXTURE)):
        failures.append("schema 快照里少了模型：" f"{set(expect_support) - set(sa.model_keys(FIXTURE))}")
    for model, checks in expect_support.items():
        for param, supported in checks.items():
            value = {"max_images": 3, "prompt_optimization": "fast", "thinking": False}[param]
            api, _ = sa.build_api_graph(sa.load_workflow(sa.DEFAULT_WORKFLOW))
            try:
                sa.apply_params(api, {"model": model, param: value}, FIXTURE)
                ok = True
            except sa.UnappliedOverrideError:
                ok = False
            if ok != supported:
                failures.append(f"{model} 的 {param}：期望{'支持' if supported else '不支持'}，"
                                f"实际{'支持' if ok else '不支持'}")

    # ---- 支持的参数必须真的落进图
    graph, report = _apply({"prompt": "单元测试", "seed": 4242, "thinking": False,
                            "watermark": True, "prompt_optimization": "fast",
                            "filename_prefix": "unit-prefix"})
    seed_node = graph[sa.find_node(graph, sa.SEEDREAM_CLASS)]["inputs"]
    save_node = graph[sa.find_node(graph, sa.SAVE_CLASS)]["inputs"]
    for name, want in (("prompt", "单元测试"), ("model.seed", 4242), ("model.thinking", False),
                       ("model.watermark", True), ("model.prompt_optimization", "fast")):
        if seed_node.get(name) != want:
            failures.append(f"{name} 没落进图：{seed_node.get(name)!r} != {want!r}")
    if save_node.get("filename_prefix") != "unit-prefix":
        failures.append("filename_prefix 没落进保存节点")
    if sorted(report["applied"]) != sorted(["prompt", "seed", "thinking", "watermark",
                                            "prompt_optimization", "filename_prefix"]):
        failures.append(f"applied 清单不对：{report['applied']}")
    if sa.validate_graph(graph, FIXTURE):
        failures.append(f"覆盖后的图没过校验：{sa.validate_graph(graph, FIXTURE)}")

    # ---- 尺寸：预设原文 / WxH 命中预设 / WxH 落 Custom / 比例 / 非法 / 越界
    cases = [
        ("(2K) 2048x2048 (1:1)", {"model.size_preset": "(2K) 2048x2048 (1:1)"}),
        ("1024x1024", {"model.size_preset": "(1K) 1024x1024 (1:1)"}),
        ("1:1", {"model.size_preset": "(1K) 1024x1024 (1:1)"}),
        ("1440x2560", {"model.size_preset": "Custom", "model.width": 1440, "model.height": 2560}),
    ]
    for value, want in cases:
        got = sa.parse_size(value, FIXTURE, "seedream 5.0 pro")
        if got != want:
            failures.append(f"--size {value} 解析成 {got}，期望 {want}")
    for bad, why in (("4000x4000x2", "格式"), ("16:10", "比例"), ("nonsense", "无法解析"),
                     ("900x900", "越界")):
        try:
            got = sa.parse_size(bad, FIXTURE, "seedream 5.0 pro")
            failures.append(f"--size {bad} 本该因{why}被拒，却解析成 {got}")
        except sa.InvalidValueError:
            pass
    _apply({"size": "Custom"}, sa.InvalidValueError)

    # ---- 不支持的参数：默认报错，--allow-unapplied 才放行并如实记录
    _apply({"model": "seedream 5.0 flash", "thinking": True}, sa.UnappliedOverrideError)
    _apply({"model": "seedream 5.0 pro", "max_images": 4}, sa.UnappliedOverrideError)
    _apply({"no_such_param": 1}, sa.UnappliedOverrideError)
    _apply({"model": "seedream 9.9"}, sa.UnknownModelError)
    graph, report = _apply({"max_images": 3}, None, strict=False)
    if report["unapplied"] != {"max_images": 3}:
        failures.append(f"strict=False 没有如实记录被丢掉的参数：{report}")
    if report["applied"]:
        failures.append(f"strict=False 把没落地的参数当成 applied：{report['applied']}")
    graph, report = _apply({"model": "seedream 5.0 lite", "max_images": 3, "fail_on_partial": False})
    if graph[sa.find_node(graph, sa.SEEDREAM_CLASS)]["inputs"].get("model.max_images") != 3:
        failures.append("lite 的 max_images 没落进图")

    # ---- 保存格式是第二个动态下拉框：换格式要换子输入集合
    graph, _ = _apply({"format": "exr"})
    save_inputs = graph[sa.find_node(graph, sa.SAVE_CLASS)]["inputs"]
    if save_inputs.get("format.bit_depth") != "16-bit float":
        failures.append(f"换 exr 后没有补上该格式的默认 bit_depth：{save_inputs}")
    _apply({"format": "exr", "bit_depth": "8-bit"}, sa.InvalidValueError)
    _apply({"format": "jpeg"}, sa.InvalidValueError)

    # ---- 纯文生图：参考图输入是采集式的，不给不算缺（真机实测服务器接受）
    api, _ = sa.build_api_graph(sa.load_workflow(sa.DEFAULT_WORKFLOW))
    if "model.images.image_1" in json.dumps(api):
        failures.append("文生图工作流里不该出现参考图输入")
    if "缺少必填输入 model.images" in " ".join(sa.validate_graph(api, FIXTURE)):
        failures.append("把采集式输入 model.images 当成了必填")

    # ---- schema 漂移检测
    live = json.loads(json.dumps(FIXTURE))
    live["nodes"][sa.SEEDREAM_CLASS]["input"]["required"]["model"][1]["options"].append(
        {"key": "seedream 6.0", "inputs": {"required": {}}})
    drift = sa.diff_schema(FIXTURE, live)
    if drift["models_added"] != ["seedream 6.0"]:
        failures.append(f"漂移检测漏掉了新模型：{drift}")
    if sa.diff_schema(FIXTURE, FIXTURE)["params"]:
        failures.append("自己和自己对账出现了参数漂移")
    return failures


# --------------------------------------------------------------------------
# 3) 往返
# --------------------------------------------------------------------------
def check_roundtrip(tmp: str) -> list[str]:
    failures: list[str] = []
    server, url = start_mock()
    try:
        # --check：节点在、模型列表在、无凭据时明确提示
        _reset()
        result, code = sg.run_check(url)
        if code != sg.EXIT_OK or not result["reachable"]:
            failures.append(f"--check 应通过：{result}")
        if result["nodes"][sa.SEEDREAM_CLASS] is not True:
            failures.append("--check 没认出 Seedream 节点")
        if result["schema_drift"] != "none":
            failures.append(f"--check 报出了不该有的 schema 漂移：{result['schema_drift']}")
        if result["credential"]["present"]:
            failures.append("--check 凭空认为有凭据")
        if "hint" not in result["credential"]:
            failures.append("--check 在缺凭据时没有给提示")

        # 不带凭据：payload 里不能有 extra_data
        _reset()
        out = sg.generate(server=url, prompt="mock t2i", out_dir=tmp, filename_prefix="nokey",
                          timeout=30, poll=0.2, quiet=True)
        if out["local_paths"] and open(out["local_paths"][0], "rb").read() != PNG:
            failures.append("下载到的字节与服务器给的不一致")
        sent = Handler.submitted[-1]
        if "extra_data" in sent:
            failures.append(f"没给凭据时却发了 extra_data：{sent.get('extra_data')}")

        # 带凭据：必须走 official channel extra_data.api_key_comfy_org
        _reset()
        key = "comfyui-UNIT-TEST-KEY"
        out = sg.generate(server=url, prompt="mock t2i keyed", out_dir=tmp,
                          filename_prefix="withkey", api_key=key, timeout=30, poll=0.2,
                          quiet=True)
        sent = Handler.submitted[-1]
        if sent.get("extra_data", {}).get("api_key_comfy_org") != key:
            failures.append(f"凭据没走 extra_data.api_key_comfy_org：{sent.get('extra_data')}")
        if sent["prompt"][sa.find_node(sent["prompt"], sa.SEEDREAM_CLASS)][
                "inputs"]["prompt"] != "mock t2i keyed":
            failures.append("提交的图里没有这次请求的 prompt")

        # 留档：api.json 复现得出来；requests.jsonl 只记来源、不记 key
        api_file = os.path.join(tmp, "withkey.api.json")
        ledger = os.path.join(tmp, "requests.jsonl")
        if not os.path.exists(api_file):
            failures.append("没有写 <prefix>.api.json")
        if not os.path.exists(ledger):
            failures.append("没有写 requests.jsonl")
        rows = [json.loads(line) for line in open(ledger, encoding="utf-8") if line.strip()]
        if len(rows) != 2:
            failures.append(f"requests.jsonl 应有 2 行，得到 {len(rows)}")
        last = rows[-1]
        if (last.get("credential_channel") != "api_key"
                or last.get("credential_source") != "cli:--api-key"):
            failures.append(f"requests.jsonl 没有如实记录凭据来源：{last}")
        if key in json.dumps(rows):
            failures.append("requests.jsonl 里出现了凭据明文（绝不允许）")
        if last.get("unapplied") != {} or last.get("engine") != sg.ENGINE:
            failures.append(f"requests.jsonl 字段不对：{last}")
        if not out["local_paths"]:
            failures.append("带凭据那轮没有下载到图")
        if out.get("cached_nodes") != ["2", "3"]:
            failures.append(f"没有把 ComfyUI 的缓存命中解析出来：{out.get('cached_nodes')}")

        # 第二通道：浏览器登录态的 Bearer token；两个通道不能同时发
        _reset()
        token = "unit-test-bearer-token"
        sg.generate(server=url, prompt="mock t2i token", out_dir=tmp, filename_prefix="tokenrun",
                    auth_token=token, timeout=30, poll=0.2, quiet=True)
        sent = Handler.submitted[-1]
        if sent.get("extra_data") != {"auth_token_comfy_org": token}:
            failures.append(f"auth_token 通道没走 extra_data.auth_token_comfy_org："
                            f"{sent.get('extra_data')}")
        if sg.resolve_credential(api_key="k", auth_token="t")["channel"] != "api_key":
            failures.append("两个通道同时给时没有优先用 api_key")
        if sg.resolve_credential()["present"]:
            failures.append("什么都没给却认为有凭据")

        # 分类：鉴权失败 / 节点报错 / 被服务器拒 / 超时
        _reset(mode="unauth")
        try:
            sg.generate(server=url, prompt="x", out_dir=tmp, timeout=30, poll=0.2, quiet=True)
            failures.append("Unauthorized 没有被识别成鉴权错误")
        except sg.AuthError as exc:
            if "api_key_comfy_org" not in str(exc) or "platform.comfy.org" not in str(exc):
                failures.append(f"鉴权错误里没有给出可操作的修法：{exc}")
        _reset(mode="node_error")
        try:
            sg.generate(server=url, prompt="x", out_dir=tmp, timeout=30, poll=0.2, quiet=True)
            failures.append("节点报错没有被抛出")
        except sg.NodeError as exc:
            if "safety" not in str(exc):
                failures.append(f"节点报错信息被吞了：{exc}")
        _reset(reject=True)
        try:
            sg.generate(server=url, prompt="x", out_dir=tmp, timeout=30, poll=0.2, quiet=True)
            failures.append("400 被拒没有被抛出")
        except sg.RejectedError as exc:
            if "model.height" not in str(exc):
                failures.append(f"服务器给的校验明细被吞了：{exc}")
        _reset(answer=False)
        try:
            sg.generate(server=url, prompt="x", out_dir=tmp, timeout=0.4, poll=0.2, quiet=True)
            failures.append("超时没有被抛出")
        except TimeoutError:
            pass
    finally:
        _reset()
        server.shutdown()
    return failures


def check_unreachable() -> list[str]:
    result, code = sg.run_check("http://127.0.0.1:1")
    if code != sg.EXIT_UNREACHABLE or result["reachable"]:
        return [f"不可达的服务器没有给出 EXIT_UNREACHABLE：{code} {result}"]
    return []


def main() -> int:
    failures = check_conversion()
    print(f"conversion: {'OK' if not failures else 'FAIL'}")
    param_failures = check_params()
    failures += param_failures
    print(f"params: {'OK' if not param_failures else 'FAIL'}")
    with tempfile.TemporaryDirectory() as tmp:
        rt = check_roundtrip(tmp)
    failures += rt
    print(f"mock roundtrip: {'OK' if not rt else 'FAIL'}")
    unreach = check_unreachable()
    failures += unreach
    print(f"unreachable server: {'OK' if not unreach else 'FAIL'}")
    for item in failures:
        print("  -", item)
    print("RESULT:", "PASS" if not failures else "FAIL")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
