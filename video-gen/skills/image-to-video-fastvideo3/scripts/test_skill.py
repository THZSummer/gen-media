#!/usr/bin/env python3
"""Offline self-test for the image-to-video-fastvideo3 skill.

No GPU and no real ComfyUI: starts a mock server on localhost and exercises

  1. workflow conversion -- the first frame lands on LoadImage, the canvas follows
     ImageScaleToTotalPixels -> GetImageSize, every profile parameter reaches its
     node field, ``force`` parameters cut their incoming link, the optional last
     frame is injected as a real link (never a bare string), and the API graph has
     no dangling links
  2. full HTTP roundtrip -- /upload/image -> POST /prompt -> poll /history ->
     GET /view for the .mp4, including a decoy preview output that must NOT be
     downloaded, plus prompt preservation

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
import comfyui_i2v as i2v  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(ok), "" if ok else str(detail)))


def graph(image="ref.png", last=None, **kw):
    set_pairs = kw.pop("set_pairs", None)
    overrides = {k: v for k, v in i2v.build_overrides(**kw).items() if v is not None}
    api, out_id, warnings, _prof, merged = i2v.build_graph(
        i2v.DEFAULT_WORKFLOW, i2v.DEFAULT_PROFILE, overrides,
        image_name=image, last_frame_name=last, set_pairs=set_pairs,
    )
    return api, out_id, warnings, merged


# --------------------------------------------------------------------------- 1
def test_conversion() -> None:
    api, out_id, warnings, _ = graph()
    check("output node is SaveVideo (92)", out_id == "92", out_id)
    check("default run has no warnings", warnings == [], warnings)
    check("first frame lands on LoadImage.image", api["136"]["inputs"] == {"image": "ref.png"},
          api["136"]["inputs"])
    check("LoadImage.upload (frontend-only) was dropped", "upload" not in api["136"]["inputs"])
    check("canvas follows ImageScaleToTotalPixels -> GetImageSize",
          api["142"]["inputs"]["image"] == ["136", 0] and api["141"]["inputs"]["image"] == ["142", 0],
          {"142": api["142"]["inputs"], "141": api["141"]["inputs"]})
    check("width/height come from GetImageSize, not a literal",
          api["104"]["inputs"]["width"] == ["141", 0] and api["104"]["inputs"]["height"] == ["141", 1],
          api["104"]["inputs"])
    check("first_frame is wired to the uploaded image",
          api["104"]["inputs"]["first_frame"] == ["136", 0], api["104"]["inputs"].get("first_frame"))
    check("last_frame absent when not requested", "last_frame" not in api["104"]["inputs"])
    check("duration lives on PrimitiveFloat", api["111"]["inputs"]["value"] == 5)
    check("length is fed by the math node", api["104"]["inputs"]["length"] == ["107", 1])
    check("drop_inputs removed the frontend-only control_after_generate",
          "control_after_generate" not in api["15"]["inputs"], api["15"]["inputs"])
    check("scale defaults ship from the workflow",
          api["142"]["inputs"]["megapixels"] == 0.4
          and api["142"]["inputs"]["resolution_steps"] == 32
          and api["142"]["inputs"]["upscale_method"] == "nearest-exact", api["142"]["inputs"])

    api, _, warnings, _ = graph(
        prompt="P", duration=9, megapixels=0.8, resolution_steps=64, scale_method="lanczos",
        seed=42, steps=8, sampler="euler", scheduler="karras", denoise=0.9, fps=30,
        shift_video=7, shift_audio=2, attention="pytorch attention", sparse_selection="sla",
        sparse_keep_percent=25, sparse_min_tokens=4096, filename_prefix="video/T",
        unet_name="U.safetensors", clip_name="C.safetensors", vae_name="V.safetensors",
        audio_vae_name="A.safetensors", video_codec="h264", video_format="mp4",
    )
    check("no warnings with every parameter set", warnings == [], warnings)
    for label, got, want in [
        ("prompt -> MiniMaxH3ImageToVideo", api["104"]["inputs"]["prompt"], "P"),
        ("image -> LoadImage", api["136"]["inputs"]["image"], "ref.png"),
        ("megapixels -> ImageScaleToTotalPixels", api["142"]["inputs"]["megapixels"], 0.8),
        ("resolution_steps", api["142"]["inputs"]["resolution_steps"], 64),
        ("scale_method", api["142"]["inputs"]["upscale_method"], "lanczos"),
        ("seed -> RandomNoise", api["15"]["inputs"]["noise_seed"], 42),
        ("sampler -> KSamplerSelect", api["17"]["inputs"]["sampler_name"], "euler"),
        ("scheduler -> BasicScheduler", api["9"]["inputs"]["scheduler"], "karras"),
        ("denoise", api["9"]["inputs"]["denoise"], 0.9),
        ("fps -> CreateVideo", api["91"]["inputs"]["fps"], 30),
        ("video_codec -> CreateVideo.codec", api["91"]["inputs"]["codec"], "h264"),
        ("video_format -> SaveVideo.format", api["92"]["inputs"]["format"], "mp4"),
        ("filename_prefix -> SaveVideo", api["92"]["inputs"]["filename_prefix"], "video/T"),
        ("shift_video", api["143"]["inputs"]["shift_video"], 7),
        ("attention -> ModelAttentionBackend", api["128"]["inputs"]["attention"], "pytorch attention"),
        ("sparse selection", api["127"]["inputs"]["selection"], "sla"),
        ("sparse keep_percent (dotted field)", api["127"]["inputs"]["selection.keep_percent"], 25),
        ("unet_name -> UNETLoader", api["6"]["inputs"]["unet_name"], "U.safetensors"),
        ("vae_name -> video VAELoader", api["11"]["inputs"]["vae_name"], "V.safetensors"),
        ("audio_vae_name -> audio VAELoader", api["24"]["inputs"]["vae_name"], "A.safetensors"),
    ]:
        check(label, got == want, f"got {got!r} want {want!r}")

    api, _, _, _ = graph(prompt="P", width=768, height=1344, length=124)
    check("width/height FORCE cut the GetImageSize link",
          api["104"]["inputs"]["width"] == 768 and api["104"]["inputs"]["height"] == 1344,
          api["104"]["inputs"])
    check("length FORCE cuts the duration math link", api["104"]["inputs"]["length"] == 124)

    # the injected last frame must be a real link, never a string
    api, _, warnings, _ = graph(prompt="P", last="last.png")
    check("no warnings when a last frame is supplied", warnings == [], warnings)
    new_ids = [k for k, v in api.items() if v["class_type"] == "LoadImage" and k != "136"]
    check("exactly one extra LoadImage was injected", len(new_ids) == 1, sorted(api))
    if new_ids:
        injected = new_ids[0]
        check("injected LoadImage carries only the image name",
              api[injected]["inputs"] == {"image": "last.png"}, api[injected]["inputs"])
        check("last_frame is a [node, slot] link, not a string",
              api["104"]["inputs"]["last_frame"] == [injected, 0], api["104"]["inputs"]["last_frame"])
        check("injected node id does not collide", injected not in ("92", "104", "136", "142"),
              injected)

    api, _, _, _ = graph(prompt="P", set_pairs=["BlockSparseAttention.tau=1.3"])
    check("--set escape hatch reaches an unnamed field", api["127"]["inputs"].get("tau") == 1.3)

    check("frame grid: 5s -> 124 frames (5.167s)", i2v.predicted_frames(5) == 124, i2v.predicted_frames(5))
    check("frame grid: 2s -> 56 frames", i2v.predicted_frames(2) == 56, i2v.predicted_frames(2))

    ids = set(api)
    dangling = [f"{nid}.{f} -> {v}" for nid, node in api.items() for f, v in node["inputs"].items()
                if isinstance(v, list) and len(v) == 2 and isinstance(v[0], str) and v[0] not in ids]
    check("no dangling links in the API graph", not dangling, dangling)


# --------------------------------------------------------------------------- 2
VIDEO_BYTES = b"\x00\x00\x00\x18ftypmp42" + b"mock-video-payload" * 32


class MockComfy:
    """Minimal ComfyUI: /upload/image, /prompt, /history, /view, /models, /object_info."""

    def __init__(self) -> None:
        self.submitted: dict | None = None
        self.uploads: list[str] = []
        self.polls = 0
        self.viewed: list[str] = []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _send(self, payload, ctype="application/json"):
                body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self):
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length)
                if self.path == "/prompt":
                    outer.submitted = json.loads(raw.decode())["prompt"]
                    self._send({"prompt_id": "mock-pid"})
                    return
                if self.path == "/upload/image":
                    # pull the filename out of the multipart body
                    marker = b'filename="'
                    start = raw.find(marker)
                    name = raw[start + len(marker):raw.find(b'"', start + len(marker))].decode() \
                        if start >= 0 else "unnamed"
                    outer.uploads.append(name)
                    self._send({"name": name, "subfolder": "", "type": "input"})
                    return
                self.send_error(404)

            def do_GET(self):
                url = urllib.parse.urlparse(self.path)
                if url.path == "/system_stats":
                    self._send({"system": {"comfyui_version": "mock"}})
                elif url.path.startswith("/history/"):
                    outer.polls += 1
                    if outer.polls < 2:
                        self._send({})
                        return
                    self._send({"mock-pid": {
                        "status": {"status_str": "success"},
                        "outputs": {
                            "92": {"images": [{"filename": "Mock_i2v_00001_.mp4",
                                               "subfolder": "video", "type": "output"}],
                                   "animated": [True]},
                            "93": {"images": [{"filename": "ComfyUI_temp_decoy.mp4",
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
                    self._send({cls: {}} if cls in i2v.REQUIRED_NODES else {})
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
    out_dir = tempfile.mkdtemp(prefix="fastvideo-i2v-")
    src_dir = tempfile.mkdtemp(prefix="fastvideo-i2v-src-")
    try:
        first = os.path.join(src_dir, "first.png")
        last = os.path.join(src_dir, "last.png")
        for p in (first, last):
            with open(p, "wb") as fh:
                fh.write(b"\x89PNG\r\n\x1a\n" + b"fake")

        with MockComfy() as mock:
            check("--check passes against the mock", i2v.check_server(mock.url)["ok"],
                  i2v.check_server(mock.url))
            result = i2v.generate(
                server=mock.url, prompt="a test shot", image=first, last_frame=last,
                duration=5, seed=7, filename_prefix="rt", out_dir=out_dir,
                poll=0.05, quiet=True, timeout=20,
            )
            check("both frames were uploaded", mock.uploads == ["first.png", "last.png"], mock.uploads)
            check("roundtrip produced a local file", len(result["local_paths"]) == 1, result["local_paths"])
            path = result["local_paths"][0] if result["local_paths"] else ""
            check("downloaded file is the SaveVideo mp4",
                  os.path.basename(path) == "Mock_i2v_00001_.mp4", path)
            check("mp4 content matches /view bytes",
                  os.path.exists(path) and open(path, "rb").read() == VIDEO_BYTES)
            check("the temp preview decoy was NOT downloaded",
                  mock.viewed == ["Mock_i2v_00001_.mp4"], mock.viewed)
            check("reported the input image names",
                  result["input_image"] == "first.png" and result["last_frame_image"] == "last.png",
                  (result["input_image"], result["last_frame_image"]))

            api_path = os.path.join(out_dir, "rt.api.json")
            check("prompt archive <prefix>.api.json written", os.path.exists(api_path))
            if os.path.exists(api_path):
                saved = json.load(open(api_path, encoding="utf-8"))
                check("archived graph == the graph actually submitted", saved == mock.submitted)
                check("archived graph carries the prompt",
                      saved["104"]["inputs"]["prompt"] == "a test shot")
                check("archived graph wires the uploaded first frame",
                      saved["136"]["inputs"]["image"] == "first.png")
                injected = [k for k, v in saved.items() if v["class_type"] == "LoadImage" and k != "136"]
                check("archived graph wires the uploaded last frame as a link",
                      len(injected) == 1 and saved["104"]["inputs"]["last_frame"] == [injected[0], 0],
                      saved["104"]["inputs"].get("last_frame"))
                check("archived graph dropped control_after_generate",
                      "control_after_generate" not in saved["15"]["inputs"])

            jsonl = os.path.join(out_dir, "requests.jsonl")
            check("requests.jsonl written", os.path.exists(jsonl))
            if os.path.exists(jsonl):
                entry = json.loads(open(jsonl, encoding="utf-8").read().strip().splitlines()[-1])
                check("requests.jsonl records engine/prompt_id",
                      entry.get("engine") == "fastvideo-fasth3-i2v" and entry.get("prompt_id") == "mock-pid",
                      {k: entry.get(k) for k in ("engine", "prompt_id")})
                check("requests.jsonl records both input images",
                      entry.get("input_image") == "first.png"
                      and entry.get("last_frame_image") == "last.png",
                      {k: entry.get(k) for k in ("input_image", "last_frame_image")})
                check("requests.jsonl records elapsed_s", "elapsed_s" in entry)

            # --plan must neither upload nor submit
            uploads_before, submitted_before = list(mock.uploads), mock.submitted
            with contextlib.redirect_stdout(io.StringIO()):
                rc = i2v.main(["--server", mock.url, "--image", first, "--prompt", "p",
                               "--duration", "2", "--plan"])
            check("--plan exits 0 without uploading or submitting",
                  rc == 0 and mock.uploads == uploads_before and mock.submitted == submitted_before,
                  (rc, mock.uploads))
    finally:
        shutil.rmtree(out_dir, ignore_errors=True)
        shutil.rmtree(src_dir, ignore_errors=True)


def main() -> int:
    test_conversion()
    print("conversion: OK" if all(ok for _, ok, _ in RESULTS) else "conversion: FAILED")
    before = len(RESULTS)
    test_roundtrip()
    print("mock roundtrip: OK" if all(ok for _, ok, _ in RESULTS[before:]) else "mock roundtrip: FAILED")

    failed = [(n, d) for n, ok, d in RESULTS if not ok]
    for name, detail in failed:
        print(f"  FAIL: {name}" + (f"  -> {detail}" if detail else ""))
    print(f"{len(RESULTS) - len(failed)}/{len(RESULTS)} checks passed")
    print("RESULT: " + ("PASS" if not failed else "FAIL"))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
