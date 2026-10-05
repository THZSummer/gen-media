#!/usr/bin/env python3
"""Self-test for the text-to-image-comfyui skill.

Starts a mock ComfyUI server (no GPU, no models) and exercises the whole path:
workflow expansion -> API prompt -> POST /prompt -> /history -> /view download.

Run:
  python3 scripts/test_skill.py            # mock end-to-end test
  python3 scripts/test_skill.py --server http://192.168.3.5:18000   # probe a live server
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import struct
import sys
import tempfile
import threading
import zlib
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Deterministic image tooling (pixel diff, contact sheets, PNG encode/decode)
# lives in the sibling `image-tools` skill -- the AI-free layer this skill
# depends on, not the other way round.
_TOOLS = os.path.normpath(os.path.join(HERE, "..", "..", "image-tools", "scripts"))
if os.path.isdir(_TOOLS) and _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import comfyui_convert as cc  # noqa: E402
import comfyui_gen as cg  # noqa: E402
import comfyui_qwen as qw  # noqa: E402
import pngdiff  # noqa: E402

WORKFLOW = os.path.join(HERE, "..", "assets", "z-image-turbo-ui.json")


def _write_rgb_png(path: str, width: int, height: int, pixel, extra_text: str | None = None) -> str:
    """Minimal 8-bit RGB PNG writer, for the pixel-comparison tests."""
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter type 0
        for x in range(width):
            raw.extend(pixel(x, y))

    def chunk(tag: bytes, body: bytes) -> bytes:
        return (struct.pack(">I", len(body)) + tag + body
                + struct.pack(">I", zlib.crc32(tag + body) & 0xFFFFFFFF))

    out = bytearray(b"\x89PNG\r\n\x1a\n")
    out += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    if extra_text:
        out += chunk(b"tEXt", b"workflow\x00" + extra_text.encode())
    out += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    out += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(bytes(out))
    return path

# 1x1 transparent PNG
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
)

# ---------------------------------------------------------------- mock server
class Handler(BaseHTTPRequestHandler):
    submitted: dict = {}

    def log_message(self, *args):  # silence
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
            return self._json({"system": {"comfyui_version": "0.3.73"}, "devices": []})
        if self.path.startswith("/history/"):
            pid = self.path.rsplit("/", 1)[-1]
            entry = self.submitted.get(pid)
            if entry is None:
                return self._json({})
            return self._json(
                {
                    pid: {
                        "status": {"status_str": "success", "completed": True},
                        "outputs": {
                            "9": {
                                "images": [
                                    {
                                        "filename": f"mock_{pid[:8]}_00001_.png",
                                        "subfolder": "",
                                        "type": "output",
                                    }
                                ]
                            }
                        },
                    }
                }
            )
        if self.path.startswith("/view?"):
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", str(len(PNG)))
            self.end_headers()
            self.wfile.write(PNG)
            return
        if self.path.startswith("/models/"):
            return self._json(["z_image_turbo_bf16.safetensors"])
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length) or b"{}")
        if self.path.startswith("/prompt"):
            Handler.submitted["mock-prompt-id"] = {"request": payload}
            return self._json({"prompt_id": "mock-prompt-id", "number": 1, "node_errors": {}})
        self.send_response(404)
        self.end_headers()


def start_mock() -> tuple[HTTPServer, str]:
    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    return server, f"http://{host}:{port}"


# ------------------------------------------------------------------- checks
def _fresh_ui() -> dict:
    """convert() annotates nodes in place, so every case needs a clean copy."""
    return json.load(open(WORKFLOW, encoding="utf-8"))


def check_conversion() -> list[str]:
    failures: list[str] = []
    api, save_id = cc.convert(_fresh_ui(), {"prompt": "unit test prompt", "width": 640, "height": 640, "seed": 7, "steps": 4})
    ids = set(api)
    if save_id != "9":
        failures.append(f"SaveImage node expected 9, got {save_id}")
    for node_id in ("3", "8", "9", "11", "13", "27", "28", "29", "30", "33"):
        if node_id not in api:
            failures.append(f"missing node {node_id}")
    if "MarkdownNote" in json.dumps(api):
        failures.append("UI-only MarkdownNote leaked into the API prompt")
    if api.get("27", {}).get("inputs", {}).get("text") != "unit test prompt":
        failures.append("prompt override not applied to CLIPTextEncode")
    if api.get("13", {}).get("inputs", {}) != {"width": 640, "height": 640, "batch_size": 1}:
        failures.append(f"size override wrong: {api.get('13')}")
    ks = api.get("3", {}).get("inputs", {})
    if ks.get("seed") != 7 or ks.get("steps") != 4:
        failures.append(f"seed/steps override wrong: {ks}")
    if ks.get("sampler_name") != "res_multistep" or ks.get("scheduler") != "simple":
        failures.append(f"sampler defaults lost: {ks}")
    if api.get("9", {}).get("inputs", {}).get("images") != ["8", 0]:
        failures.append(f"SaveImage not wired to VAEDecode: {api.get('9')}")
    for node_id, node in api.items():
        for name, value in node.get("inputs", {}).items():
            if isinstance(value, list) and value and value[0] not in ids:
                failures.append(f"node {node_id}.{name} points at missing node {value[0]}")

    # every exposed parameter must be settable, and unset ones keep the defaults
    full, _ = cc.convert(
        _fresh_ui(),
        {
            "prompt": "p",
            "width": 512,
            "height": 768,
            "seed": 3,
            "steps": 9,
            "unet_name": "u.safetensors",
            "clip_name": "c.safetensors",
            "vae_name": "v.safetensors",
            "filename_prefix": "unit-prefix",
        },
    )
    if full["28"]["inputs"]["unet_name"] != "u.safetensors":
        failures.append("unet_name override not applied")
    if full["30"]["inputs"]["clip_name"] != "c.safetensors":
        failures.append("clip_name override not applied")
    if full["29"]["inputs"]["vae_name"] != "v.safetensors":
        failures.append("vae_name override not applied")
    if full["9"]["inputs"].get("filename_prefix") != "unit-prefix":
        failures.append(f"filename_prefix override not applied: {full['9']['inputs']}")
    defaults, _ = cc.convert(_fresh_ui(), {})
    if defaults["9"]["inputs"].get("filename_prefix") != "z-image-turbo":
        failures.append("filename_prefix default lost")
    if "fox" not in json.dumps(defaults) and "Latina" not in json.dumps(defaults):
        failures.append("workflow's own prompt default not preserved")
    if defaults["13"]["inputs"]["width"] != 1024:
        failures.append("workflow's own width default not preserved")
    batched, _ = cc.convert(_fresh_ui(), {"batch_size": 5, "prompt": "p"})
    if batched["13"]["inputs"].get("batch_size") != 5:
        failures.append(f"batch_size override not applied: {batched['13']['inputs']}")
    return failures


def check_mock_roundtrip(tmp: str) -> list[str]:
    failures: list[str] = []
    server, url = start_mock()
    try:
        result = cg.generate(
            server=url,
            workflow=WORKFLOW,
            prompt="mock roundtrip",
            width=512,
            height=512,
            seed=1,
            steps=2,
            out_dir=tmp,
            filename_prefix="z-rec",
            timeout=30,
            poll=0.2,
            quiet=True,
            node_info=None,
        )
        if not result["local_paths"]:
            failures.append("no local image written")
        else:
            path = result["local_paths"][0]
            if os.path.getsize(path) != len(PNG):
                failures.append(f"downloaded file size {os.path.getsize(path)} != {len(PNG)}")
        sent = Handler.submitted["mock-prompt-id"]["request"]["prompt"]
        if sent["27"]["inputs"]["text"] != "mock roundtrip":
            failures.append("mock server received the wrong prompt")
        if sent["13"]["inputs"]["width"] != 512:
            failures.append("mock server received the wrong width")

        # prompt preservation: exact graph + jsonl ledger
        api_file = os.path.join(tmp, "z-rec.api.json")
        ledger = os.path.join(tmp, "requests.jsonl")
        if not os.path.exists(api_file):
            failures.append("z-image run did not write <prefix>.api.json")
        else:
            saved = json.load(open(api_file, encoding="utf-8"))
            if saved.get("27", {}).get("inputs", {}).get("text") != "mock roundtrip":
                failures.append("<prefix>.api.json does not hold the submitted prompt")
        if not os.path.exists(ledger):
            failures.append("z-image run did not write requests.jsonl")
        else:
            rows = [json.loads(l) for l in open(ledger, encoding="utf-8") if l.strip()]
            if not rows or rows[-1].get("prompt") != "mock roundtrip":
                failures.append("requests.jsonl missing the prompt field")

        # optional recording must be switchable off
        cg.generate(server=url, workflow=WORKFLOW, prompt="no-record", out_dir=tmp,
                    filename_prefix="z-off", timeout=30, poll=0.2, quiet=True,
                    record=False, node_info=None)
        if os.path.exists(os.path.join(tmp, "z-off.api.json")):
            failures.append("record=False still wrote an api.json")

        # same guarantee for the Qwen engine
        qw.generate(server=url, prompt="qwen mock", negative="bad, ugly", width=512,
                    height=512, steps=4, cfg=3.0, seed=2, filename_prefix="q-rec",
                    out_dir=tmp, timeout=30, poll=0.2, quiet=True)
        qapi = os.path.join(tmp, "q-rec.api.json")
        if not os.path.exists(qapi):
            failures.append("qwen run did not write <prefix>.api.json")
        else:
            qsaved = json.load(open(qapi, encoding="utf-8"))
            if qsaved.get("5", {}).get("inputs", {}).get("text") != "qwen mock":
                failures.append("qwen api.json does not hold the positive prompt")
            if qsaved.get("8", {}).get("inputs", {}).get("text") != "bad, ugly":
                failures.append("qwen api.json does not hold the negative prompt")
        rows = [json.loads(l) for l in open(ledger, encoding="utf-8") if l.strip()]
        if not any(r.get("engine") == "qwen-image" and r.get("negative") == "bad, ugly" for r in rows):
            failures.append("requests.jsonl missing the qwen negative prompt")
        # both engines must record the unapplied field, even when it is empty
        for engine in ("z-image-turbo", "qwen-image"):
            entries = [r for r in rows if r.get("engine") == engine]
            if not entries:
                failures.append(f"requests.jsonl has no {engine} entry")
            elif not all("unapplied" in r for r in entries):
                failures.append(f"{engine} entries lack the unapplied field")
        if not all(r.get("unapplied") == {} for r in rows):
            failures.append(f"a clean run recorded non-empty unapplied: {rows}")
    finally:
        server.shutdown()
    return failures


def check_unapplied_and_pixels() -> list[str]:
    """A dropped parameter must be loud; reproducibility must compare pixels.

    Both cases are fallout from real project runs: a silently ignored
    ``--width`` once invalidated a whole comparison round, and a sha256
    reproducibility check false-fails the moment ``filename_prefix`` changes
    (ComfyUI embeds the graph in the PNG's tEXt chunk).
    """
    failures: list[str] = []

    # ---- convert() refuses to return a graph that ignored a parameter
    for bad in ({"widht": 1536}, {"aspect_ratio": "16:9"}):
        try:
            cc.convert(_fresh_ui(), bad)
            failures.append(f"convert() accepted {bad} without applying it")
        except cc.UnappliedOverrideError:
            pass

    # ---- unknown names are reported, not swallowed
    report: dict = {}
    _api, _id, warns = cc.convert_ex(_fresh_ui(), {"widht": 1536, "width": 512},
                                     strict=False, report=report)
    if report.get("unapplied") != {"widht": 1536}:
        failures.append(f"report did not list the dropped key: {report}")
    if "width" not in (report.get("applied") or []):
        failures.append(f"valid key not reported as applied: {report}")
    if not any("unapplied" in w for w in warns):
        failures.append("no warning mentioned the unapplied key")

    # ---- the real parameter set is fully applied (no false positives)
    full: dict = {}
    cc.convert(_fresh_ui(), {"prompt": "p", "width": 512, "height": 768, "seed": 3, "steps": 9,
                             "unet_name": "u", "clip_name": "c", "vae_name": "v",
                             "filename_prefix": "pfx", "batch_size": 2}, report=full)
    if full.get("unapplied"):
        failures.append(f"valid overrides reported as unapplied: {full['unapplied']}")

    # ---- the Qwen graph rejects unknown keywords instead of defaulting
    try:
        qw.build_graph("p", smapler="euler")
        failures.append("qwen build_graph accepted an unknown keyword")
    except ValueError:
        pass

    # ---- pixel comparison: identical pixels, different bytes
    with tempfile.TemporaryDirectory() as tmp:
        a = os.path.join(tmp, "a.png")
        b = os.path.join(tmp, "b.png")
        c = os.path.join(tmp, "c.png")
        _write_rgb_png(a, 8, 8, lambda x, y: (x * 30 % 256, y * 30 % 256, 128))
        # same pixels, one extra metadata chunk -> different file bytes
        _write_rgb_png(b, 8, 8, lambda x, y: (x * 30 % 256, y * 30 % 256, 128),
                       extra_text="workflow: {...}")
        _write_rgb_png(c, 8, 8, lambda x, y: (x * 30 % 256, y * 30 % 256, 129))
        if open(a, "rb").read() == open(b, "rb").read():
            failures.append("test fixture is wrong: metadata-only change kept the bytes equal")
        same, detail = pngdiff.pixels_equal(a, b)
        if not same:
            failures.append(f"pixel compare should ignore tEXt-only differences: {detail}")
        diff = pngdiff.compare(a, c)
        if diff.same or diff.differing != 64 or diff.max_diff != 1:
            failures.append(f"pixel compare missed a real change: {diff}")
        if pngdiff.compare(a, a).same is not True:
            failures.append("self-comparison reported a difference")
    return failures


def check_live(server: str) -> list[str]:
    probe = cg.check_server(server)
    print(json.dumps(probe, ensure_ascii=False, indent=2)[:800])
    if not probe["reachable"]:
        return [f"live server unreachable: {probe['error']}"]
    return []


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--server", help="also probe this live ComfyUI server")
    args = ap.parse_args(argv)

    failures = check_conversion()
    print(f"conversion: {'OK' if not failures else 'FAIL'}")
    up = check_unapplied_and_pixels()
    failures += up
    print(f"unapplied + pixel diff: {'OK' if not up else 'FAIL'}")
    with tempfile.TemporaryDirectory() as tmp:
        rt = check_mock_roundtrip(tmp)
    failures += rt
    print(f"mock roundtrip: {'OK' if not rt else 'FAIL'}")
    if args.server:
        live = check_live(args.server)
        failures += live
        print(f"live probe: {'OK' if not live else 'FAIL'}")

    for f in failures:
        print("  -", f)
    print("RESULT:", "PASS" if not failures else "FAIL")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
