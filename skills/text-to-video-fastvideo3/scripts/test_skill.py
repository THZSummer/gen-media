#!/usr/bin/env python3
"""Offline self-test for the text-to-video-fastvideo3 skill.

No GPU and no real ComfyUI: starts a mock server on localhost and exercises

  1. workflow conversion -- every profile parameter reaches the right node
     field, ResolutionSelector keeps driving width/height, the ``force``
     parameters cut their incoming link, the frame-grid math matches the
     workflow's Math Expression, and the API graph has no dangling links
  2. full HTTP roundtrip -- POST /prompt -> poll /history -> GET /view for the
     .mp4, including a decoy preview output that must NOT be downloaded, plus
     prompt preservation (``<prefix>.api.json`` + ``requests.jsonl``)

Run:
  python3 scripts/test_skill.py
Exit code 0 = every check passed.
"""
from __future__ import annotations

import contextlib
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
import comfyui_video as cv  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(ok), "" if ok else str(detail)))


def graph(**kw):
    set_pairs = kw.pop("set_pairs", None)
    overrides = {k: v for k, v in cv.build_overrides(**kw).items() if v is not None}
    api, out_id, warnings, _prof, merged = cv.build_graph(
        cv.DEFAULT_WORKFLOW, cv.DEFAULT_PROFILE, overrides, set_pairs
    )
    return api, out_id, warnings, merged


# --------------------------------------------------------------------------- 1
def test_conversion() -> None:
    api, out_id, warnings, _ = graph()
    check("output node is SaveVideo (92)", out_id == "92", out_id)
    check("clean t2v run has no warnings", warnings == [], warnings)
    check("ResolutionSelector ships 1:1 / 0.4MP / 32",
          api["143"]["inputs"] == {"aspect_ratio": "1:1 (Square)", "megapixels": 0.4, "multiple": 32},
          api["143"]["inputs"])
    check("width/height follow the ResolutionSelector link (not a literal)",
          api["104"]["inputs"]["width"] == ["143", 0] and api["104"]["inputs"]["height"] == ["143", 1],
          api["104"]["inputs"])
    check("duration lives on PrimitiveFloat", api["111"]["inputs"]["value"] == 5)
    check("length is fed by the math node", api["104"]["inputs"]["length"] == ["107", 1])
    check("drop_inputs removed the frontend-only control_after_generate",
          "control_after_generate" not in api["15"]["inputs"], api["15"]["inputs"])

    api, _, warnings, _ = graph(
        prompt="P", duration=9, aspect_ratio="16:9 (Widescreen)", megapixels=0.8, multiple=64,
        seed=42, steps=8, sampler="euler", scheduler="karras", denoise=0.9, fps=30,
        shift_video=7, shift_audio=2, attention="pytorch attention", sparse_selection="sla",
        sparse_keep_percent=25, sparse_min_tokens=4096, filename_prefix="video/T",
        unet_name="U.safetensors", clip_name="C.safetensors", vae_name="V.safetensors",
        audio_vae_name="A.safetensors", video_codec="h264", video_format="mp4",
    )
    check("no warnings with every parameter set", warnings == [], warnings)
    for label, got, want in [
        ("prompt -> MiniMaxH3ImageToVideo", api["104"]["inputs"]["prompt"], "P"),
        ("aspect_ratio -> ResolutionSelector", api["143"]["inputs"]["aspect_ratio"], "16:9 (Widescreen)"),
        ("megapixels", api["143"]["inputs"]["megapixels"], 0.8),
        ("multiple", api["143"]["inputs"]["multiple"], 64),
        ("seed -> RandomNoise", api["15"]["inputs"]["noise_seed"], 42),
        ("sampler -> KSamplerSelect", api["17"]["inputs"]["sampler_name"], "euler"),
        ("scheduler -> BasicScheduler", api["9"]["inputs"]["scheduler"], "karras"),
        ("steps", api["9"]["inputs"]["steps"], 8),
        ("denoise", api["9"]["inputs"]["denoise"], 0.9),
        ("fps -> CreateVideo", api["91"]["inputs"]["fps"], 30),
        ("video_codec -> CreateVideo.codec", api["91"]["inputs"]["codec"], "h264"),
        ("video_format -> SaveVideo.format", api["92"]["inputs"]["format"], "mp4"),
        ("filename_prefix -> SaveVideo", api["92"]["inputs"]["filename_prefix"], "video/T"),
        ("shift_video", api["148"]["inputs"]["shift_video"], 7),
        ("shift_audio", api["148"]["inputs"]["shift_audio"], 2),
        ("attention -> ModelAttentionBackend", api["128"]["inputs"]["attention"], "pytorch attention"),
        ("sparse selection", api["127"]["inputs"]["selection"], "sla"),
        ("sparse keep_percent (dotted field)", api["127"]["inputs"]["selection.keep_percent"], 25),
        ("sparse min_tokens", api["127"]["inputs"]["min_tokens"], 4096),
        ("unet_name -> UNETLoader", api["6"]["inputs"]["unet_name"], "U.safetensors"),
        ("clip_name -> CLIPLoader", api["13"]["inputs"]["clip_name"], "C.safetensors"),
        ("vae_name -> video VAELoader", api["11"]["inputs"]["vae_name"], "V.safetensors"),
        ("audio_vae_name -> audio VAELoader", api["24"]["inputs"]["vae_name"], "A.safetensors"),
    ]:
        check(label, got == want, f"got {got!r} want {want!r}")

    api, _, _, _ = graph(prompt="P", width=768, height=1344, length=124)
    check("width/height FORCE cut the ResolutionSelector link",
          api["104"]["inputs"]["width"] == 768 and api["104"]["inputs"]["height"] == 1344,
          api["104"]["inputs"])
    check("length FORCE cuts the duration math link", api["104"]["inputs"]["length"] == 124)

    api, _, _, _ = graph(prompt="P", set_pairs=["BlockSparseAttention.tau=1.3",
                                                "MiniMaxH3SigmaShift.shift_video=6"])
    check("--set escape hatch reaches an unnamed field", api["127"]["inputs"].get("tau") == 1.3)
    check("--set can also retarget a named field", api["148"]["inputs"]["shift_video"] == 6)

    check("frame grid: 5s -> 124 frames (5.167s)", cv.predicted_frames(5) == 124, cv.predicted_frames(5))
    check("frame grid: 1s -> 39 frames", cv.predicted_frames(1) == 39, cv.predicted_frames(1))
    check("frame grid: 2s -> 56 frames", cv.predicted_frames(2) == 56, cv.predicted_frames(2))

    # no dangling link may survive the flattening
    ids = set(api)
    dangling = []
    for nid, node in api.items():
        for field, value in node["inputs"].items():
            if isinstance(value, list) and len(value) == 2 and isinstance(value[0], str):
                if value[0] not in ids:
                    dangling.append(f"{nid}.{field} -> {value}")
    check("no dangling links in the API graph", not dangling, dangling)
    check("every node has a class_type and inputs",
          all(n.get("class_type") and "inputs" in n for n in api.values()))


# --------------------------------------------------------------------------- 2
VIDEO_BYTES = b"\x00\x00\x00\x18ftypmp42" + b"mock-video-payload" * 32


class MockComfy:
    """Minimal ComfyUI: /prompt, /history, /view, /models, /object_info."""

    def __init__(self) -> None:
        self.submitted: dict | None = None
        self.polls = 0
        self.viewed: list[str] = []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *a):  # silence
                pass

            def _send(self, payload, ctype="application/json"):
                body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self):
                if self.path != "/prompt":
                    self.send_error(404)
                    return
                raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
                outer.submitted = json.loads(raw.decode())["prompt"]
                self._send({"prompt_id": "mock-pid"})

            def do_GET(self):
                url = urllib.parse.urlparse(self.path)
                if url.path == "/system_stats":
                    self._send({"system": {"comfyui_version": "mock"}})
                elif url.path.startswith("/history/"):
                    outer.polls += 1
                    if outer.polls < 2:
                        self._send({})  # not finished yet: exercises polling
                        return
                    self._send({"mock-pid": {
                        "status": {"status_str": "success"},
                        "outputs": {
                            "92": {"images": [{"filename": "Mock_00001_.mp4",
                                               "subfolder": "video", "type": "output"}],
                                   "animated": [True]},
                            # decoy: a temp preview that must never be downloaded
                            "93": {"images": [{"filename": "ComfyUI_temp_abc_00001_.mp4",
                                               "subfolder": "", "type": "temp"}]},
                        },
                    }})
                elif url.path == "/view":
                    q = urllib.parse.parse_qs(url.query)
                    outer.viewed.append(q.get("filename", [""])[0])
                    self._send(VIDEO_BYTES, ctype="video/mp4")
                elif url.path.startswith("/models/"):
                    self._send(["fastvideo_fasth3_8step_v2_pruned_int8_convrot.safetensors",
                                "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors",
                                "minimax_h3_video_vae_int8_convrot.safetensors",
                                "minimax_h3_audio_vae_fp32.safetensors"])
                elif url.path.startswith("/object_info/"):
                    cls = url.path.rsplit("/", 1)[-1]
                    self._send({cls: {}} if cls in cv.REQUIRED_NODES else {})
                else:
                    self.send_error(404)

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.server.server_address[1]}"

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *exc):
        self.server.shutdown()
        self.server.server_close()


def test_roundtrip() -> None:
    out_dir = tempfile.mkdtemp(prefix="fastvideo-test-")
    try:
        with MockComfy() as mock:
            check("--check passes against the mock", cv.check_server(mock.url)["ok"],
                  cv.check_server(mock.url))
            result = cv.generate(
                server=mock.url, prompt="a test shot", duration=5, seed=7,
                filename_prefix="rt", out_dir=out_dir, poll=0.05, quiet=True, timeout=20,
            )
            check("roundtrip produced a local file", len(result["local_paths"]) == 1, result["local_paths"])
            path = result["local_paths"][0] if result["local_paths"] else ""
            check("downloaded file is the SaveVideo mp4",
                  os.path.basename(path) == "Mock_00001_.mp4", path)
            check("mp4 content matches /view bytes",
                  os.path.exists(path) and open(path, "rb").read() == VIDEO_BYTES)
            check("the temp preview decoy was NOT downloaded",
                  mock.viewed == ["Mock_00001_.mp4"], mock.viewed)
            check("polling retried until history was ready", mock.polls >= 2, mock.polls)
            check("reported the output node", result["output_node"] == "92", result["output_node"])
            check("elapsed time recorded", isinstance(result["elapsed_s"], float), result["elapsed_s"])

            api_path = os.path.join(out_dir, "rt.api.json")
            check("prompt archive <prefix>.api.json written", os.path.exists(api_path))
            if os.path.exists(api_path):
                saved = json.load(open(api_path, encoding="utf-8"))
                check("archived graph == the graph actually submitted", saved == mock.submitted)
                check("archived graph carries the prompt",
                      saved["104"]["inputs"]["prompt"] == "a test shot")
                check("archived graph dropped control_after_generate",
                      "control_after_generate" not in saved["15"]["inputs"])

            jsonl = os.path.join(out_dir, "requests.jsonl")
            check("requests.jsonl written", os.path.exists(jsonl))
            if os.path.exists(jsonl):
                entry = json.loads(open(jsonl, encoding="utf-8").read().strip().splitlines()[-1])
                check("requests.jsonl records engine/prompt_id",
                      entry.get("engine") == "fastvideo-fasth3-t2v" and entry.get("prompt_id") == "mock-pid",
                      {k: entry.get(k) for k in ("engine", "prompt_id")})
                check("requests.jsonl records duration + seeded run",
                      entry.get("duration") == 5 and entry.get("seed") == 7,
                      {k: entry.get(k) for k in ("duration", "seed")})
                check("requests.jsonl records elapsed_s", "elapsed_s" in entry)

            # plan mode must not submit anything
            before = mock.submitted
            with contextlib.redirect_stdout(io.StringIO()):  # --plan is chatty
                rc = cv.main(["--server", mock.url, "--prompt", "p", "--duration", "2", "--plan"])
            check("--plan exits 0 without submitting", rc == 0 and mock.submitted == before)

            # the shipped default prefix carries a server-side subdirectory
            nested = tempfile.mkdtemp(prefix="fastvideo-nested-")
            try:
                cv.generate(server=mock.url, prompt="p", filename_prefix="video/MiniMax_H3",
                            out_dir=nested, poll=0.05, quiet=True, timeout=20)
                check("nested filename_prefix still archives on the flat out_dir",
                      os.path.exists(os.path.join(nested, "MiniMax_H3.api.json")),
                      os.listdir(nested))
                check("nested filename_prefix does not create a bogus local subdir",
                      not os.path.isdir(os.path.join(nested, "video")), os.listdir(nested))
                check("nested filename_prefix reaches the graph intact",
                      json.load(open(os.path.join(nested, "MiniMax_H3.api.json"), encoding="utf-8"))
                      ["92"]["inputs"]["filename_prefix"] == "video/MiniMax_H3")
            finally:
                shutil.rmtree(nested, ignore_errors=True)
    finally:
        shutil.rmtree(out_dir, ignore_errors=True)


def main() -> int:
    test_conversion()
    print("conversion: OK" if all(ok for _, ok, _ in RESULTS) else "conversion: FAILED")
    before = len(RESULTS)
    test_roundtrip()
    roundtrip_ok = all(ok for _, ok, _ in RESULTS[before:])
    print("mock roundtrip: OK" if roundtrip_ok else "mock roundtrip: FAILED")

    failed = [(n, d) for n, ok, d in RESULTS if not ok]
    for name, detail in failed:
        print(f"  FAIL: {name}" + (f"  -> {detail}" if detail else ""))
    print(f"{len(RESULTS) - len(failed)}/{len(RESULTS)} checks passed")
    print("RESULT: " + ("PASS" if not failed else "FAIL"))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
