#!/usr/bin/env python3
"""Offline self-test for the image-edit-comfyui skill.

Starts a mock ComfyUI (including /upload/image) and exercises:

  1. workflow conversion: bypass node dropped + rewired, control-image interface
     reconnected, every profile parameter applied, no dangling links
  2. pre-scale node enable/disable and preprocessor bypass
  3. full HTTP roundtrip: upload -> /prompt -> /history -> /view download
  4. prompt preservation (<prefix>.api.json + requests.jsonl)

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
import _shared  # noqa: E402

_shared.ensure()

import comfyui_convert as cc  # noqa: E402
import comfyui_edit as ce  # noqa: E402

WORKFLOW = ce.DEFAULT_WORKFLOW
PROFILE = cc.load_profile(ce.DEFAULT_PROFILE)
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
)


class Handler(BaseHTTPRequestHandler):
    submitted: dict = {}
    uploads: list = []

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
            return self._json({"system": {"comfyui_version": "mock"}})
        if self.path.startswith("/history/"):
            pid = self.path.rsplit("/", 1)[-1]
            if pid not in Handler.submitted:
                return self._json({})
            return self._json({pid: {
                "status": {"status_str": "success"},
                "outputs": {"9": {"images": [
                    {"filename": f"mock_{pid[:8]}_.png", "subfolder": "", "type": "output"}
                ]}},
            }})
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
        if self.path.startswith("/upload/image"):
            Handler.uploads.append(raw)
            return self._json({"name": "uploaded-ref.png", "subfolder": "", "type": "input"})
        if self.path.startswith("/prompt"):
            payload = json.loads(raw or b"{}")
            Handler.submitted["mock-edit-id"] = payload
            return self._json({"prompt_id": "mock-edit-id", "number": 1, "node_errors": {}})
        self.send_response(404)
        self.end_headers()


def start_mock():
    server = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host, port = server.server_address
    return server, f"http://{host}:{port}"


def _fresh():
    return json.load(open(WORKFLOW, encoding="utf-8"))


def _dangling(api: dict) -> list:
    ids = set(api)
    return [
        (k, n) for k, v in api.items() for n, val in v["inputs"].items()
        if isinstance(val, list) and val and val[0] not in ids
    ]


def check_conversion() -> list[str]:
    failures: list[str] = []

    # ---- defaults: bypassed pre-scale drops out, control image wired to Canny
    api, save_id, warns = cc.convert_ex(_fresh(), {"image": "ref.png"}, PROFILE)
    if save_id != "9":
        failures.append(f"SaveImage expected node 9, got {save_id}")
    if "62" in api:
        failures.append("bypassed ImageScaleToMaxDimension (62) leaked into the API graph")
    if "MarkdownNote" in json.dumps(api, ensure_ascii=False):
        failures.append("UI-only nodes leaked into the API graph")
    if api.get("57", {}).get("inputs", {}).get("image") != ["58", 0]:
        failures.append(f"Canny should read the raw image via bypass rewire: {api.get('57')}")
    if api.get("60", {}).get("inputs", {}).get("image") != ["57", 0]:
        failures.append(f"ControlNet should read the Canny output: {api.get('60')}")
    if api.get("58", {}).get("inputs", {}).get("image") != "ref.png":
        failures.append(f"LoadImage not pointed at the uploaded file: {api.get('58')}")
    if failures:
        return failures + _dangling(api)

    # ---- every profile parameter reaches the graph
    api, _, warns = cc.convert_ex(_fresh(), {
        "image": "ref.png", "prompt": "unit edit prompt", "seed": 4242,
        "steps": 5, "cfg": 2.5, "sampler": "euler", "scheduler": "karras",
        "denoise": 0.8, "shift": 4.5, "control_strength": 0.4,
        "control_start": 0.1, "control_end": 0.9, "canny_low": 0.02, "canny_high": 0.2,
        "batch_size": 3, "filename_prefix": "unit-prefix",
        "width": 640, "height": 896,
        "unet_name": "u.safetensors", "clip_name": "c.safetensors",
        "vae_name": "v.safetensors", "controlnet_name": "p.safetensors",
    }, PROFILE)
    expect = [
        (api["45"]["inputs"], "text", "unit edit prompt", "prompt"),
        (api["44"]["inputs"], "seed", 4242, "seed"),
        (api["44"]["inputs"], "steps", 5, "steps"),
        (api["44"]["inputs"], "cfg", 2.5, "cfg"),
        (api["44"]["inputs"], "sampler_name", "euler", "sampler"),
        (api["44"]["inputs"], "scheduler", "karras", "scheduler"),
        (api["44"]["inputs"], "denoise", 0.8, "denoise"),
        (api["47"]["inputs"], "shift", 4.5, "shift"),
        (api["60"]["inputs"], "strength", 0.4, "control_strength"),
        (api["60"]["inputs"], "start_percent", 0.1, "control_start"),
        (api["60"]["inputs"], "end_percent", 0.9, "control_end"),
        (api["57"]["inputs"], "low_threshold", 0.02, "canny_low"),
        (api["57"]["inputs"], "high_threshold", 0.2, "canny_high"),
        (api["41"]["inputs"], "width", 640, "width"),
        (api["41"]["inputs"], "height", 896, "height"),
        (api["41"]["inputs"], "batch_size", 3, "batch_size"),
        (api["9"]["inputs"], "filename_prefix", "unit-prefix", "filename_prefix"),
        (api["46"]["inputs"], "unet_name", "u.safetensors", "unet_name"),
        (api["39"]["inputs"], "clip_name", "c.safetensors", "clip_name"),
        (api["40"]["inputs"], "vae_name", "v.safetensors", "vae_name"),
        (api["64"]["inputs"], "name", "p.safetensors", "controlnet_name"),
    ]
    for inputs, field, want, label in expect:
        if inputs.get(field) != want:
            failures.append(f"{label}: expected {field}={want!r}, got {inputs.get(field)!r}")
    # forced size must cut the GetImageSize link
    if isinstance(api["41"]["inputs"].get("height"), list):
        failures.append("height stayed linked to GetImageSize despite force=true")

    # ---- enabling the pre-scale node puts it back, in front of Canny
    api2, _, _ = cc.convert_ex(_fresh(), {"image": "ref.png", "max_dimension": 512}, PROFILE)
    if "62" not in api2:
        failures.append("max_dimension did not enable the pre-scale node")
    else:
        if api2["62"]["inputs"].get("largest_size") != 512:
            failures.append(f"largest_size not applied: {api2['62']['inputs']}")
        if api2["57"]["inputs"].get("image") != ["62", 0]:
            failures.append(f"Canny should read the pre-scaled image: {api2.get('57')}")

    # ---- bypassing the preprocessor wires ControlNet straight to LoadImage
    api3, _, _ = cc.convert_ex(_fresh(), {"image": "ref.png"}, PROFILE, {"Canny": 4})
    if "57" in api3:
        failures.append("--no-preprocessor left the Canny node in the graph")
    if api3.get("60", {}).get("inputs", {}).get("image") != ["58", 0]:
        failures.append(f"ControlNet should read LoadImage when Canny is bypassed: {api3.get('60')}")

    for label, graph in (("full", api), ("pre-scale", api2), ("no-preprocessor", api3)):
        bad = _dangling(graph)
        if bad:
            failures.append(f"{label}: dangling links {bad}")

    # ---- an override that lands nowhere must be loud, not silently ignored
    try:
        cc.convert_ex(_fresh(), {"image": "ref.png", "widht": 640}, PROFILE, strict=True)
        failures.append("strict convert_ex accepted an unapplied override")
    except cc.UnappliedOverrideError:
        pass
    report: dict = {}
    cc.convert_ex(_fresh(), {"image": "ref.png", "widht": 640}, PROFILE,
                  strict=False, report=report)
    if report.get("unapplied") != {"widht": 640} or "image" not in (report.get("applied") or []):
        failures.append(f"report did not separate applied/unapplied: {report}")

    # ---- every declared profile parameter must reach the graph
    every = {k: (s.get("default") if s.get("default") is not None else 1)
             for k, s in PROFILE["parameters"].items()}
    every.update({"image": "ref.png", "prompt": "p"})
    full: dict = {}
    cc.convert_ex(_fresh(), every, PROFILE, strict=False, report=full)
    if full.get("unapplied"):
        failures.append(f"declared profile parameters not applied: {full['unapplied']}")
    if len(full.get("applied", [])) != len(every):
        failures.append(f"applied {len(full.get('applied', []))} of {len(every)} requested")

    # ---- drift: a profile entry whose node class is absent from the workflow
    drifted = json.loads(json.dumps(PROFILE))
    drifted["parameters"]["ghost"] = {"node": "NoSuchNodeClass", "field": "x", "force": True}
    try:
        cc.convert_ex(_fresh(), {"image": "ref.png", "ghost": 1}, drifted, strict=True)
        failures.append("a profile entry with no node was silently dropped")
    except cc.UnappliedOverrideError:
        pass
    return failures


def check_roundtrip(tmp: str) -> list[str]:
    failures: list[str] = []
    server, url = start_mock()
    ref = os.path.join(tmp, "ref.png")
    with open(ref, "wb") as fh:
        fh.write(PNG)
    try:
        result = ce.generate(
            server=url, image=ref, prompt="mock edit", filename_prefix="edit-rec",
            out_dir=tmp, timeout=30, poll=0.2, quiet=True, record=True,
        )
        if not result["local_paths"]:
            failures.append("no image downloaded")
        if not Handler.uploads:
            failures.append("/upload/image was never called")
        else:
            body = Handler.uploads[-1]
            if b'name="image"' not in body or b"filename=\"ref.png\"" not in body:
                failures.append("upload body is not well-formed multipart")
        sent = Handler.submitted.get("mock-edit-id", {}).get("prompt", {})
        if sent.get("58", {}).get("inputs", {}).get("image") != "uploaded-ref.png":
            failures.append(f"submitted graph does not use the uploaded file: {sent.get('58')}")
        if sent.get("45", {}).get("inputs", {}).get("text") != "mock edit":
            failures.append("submitted graph does not carry the prompt")
        if "62" in sent or "57" not in sent:
            failures.append("submitted graph has wrong node set (bypass not handled)")

        api_file = os.path.join(tmp, "edit-rec.api.json")
        ledger = os.path.join(tmp, "requests.jsonl")
        if not os.path.exists(api_file):
            failures.append("no <prefix>.api.json written")
        else:
            saved = json.load(open(api_file, encoding="utf-8"))
            if saved.get("58", {}).get("inputs", {}).get("image") != "uploaded-ref.png":
                failures.append("api.json does not record the control image")
        if not os.path.exists(ledger):
            failures.append("no requests.jsonl written")
        else:
            rows = [json.loads(l) for l in open(ledger, encoding="utf-8") if l.strip()]
            if not rows or rows[-1].get("control_image") != "uploaded-ref.png":
                failures.append("requests.jsonl missing control_image")
            if rows[-1].get("engine") != "z-image-turbo-fun-controlnet":
                failures.append("requests.jsonl missing the engine name")
            if rows[-1].get("unapplied") != {}:
                failures.append(f"clean run recorded unapplied={rows[-1].get('unapplied')}")
            if "unapplied" not in rows[-1]:
                failures.append("requests.jsonl lacks the unapplied field")

        ce.generate(server=url, image=ref, prompt="no record", filename_prefix="edit-off",
                    out_dir=tmp, timeout=30, poll=0.2, quiet=True, record=False)
        if os.path.exists(os.path.join(tmp, "edit-off.api.json")):
            failures.append("record=False still wrote an api.json")
    finally:
        server.shutdown()
    return failures


def main() -> int:
    failures = check_conversion()
    print(f"conversion: {'OK' if not failures else 'FAIL'}")
    with tempfile.TemporaryDirectory() as tmp:
        rt = check_roundtrip(tmp)
    failures += rt
    print(f"mock roundtrip: {'OK' if not rt else 'FAIL'}")
    for f in failures:
        print("  -", f)
    print("RESULT:", "PASS" if not failures else "FAIL")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
