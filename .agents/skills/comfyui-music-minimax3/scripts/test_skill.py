#!/usr/bin/env python3
"""Offline self-test for the comfyui-music-minimax3 skill.

No GPU and no real ComfyUI: starts a mock server on localhost and exercises

  1. workflow conversion -- every profile parameter reaches the right node
     field, the duration knob lands on MiniMaxMusic3TextEncode.max_duration and
     stays wired to EmptyMiniMaxMusic3LatentAudio.seconds, the tiled-decode
     switch flips, UI-only notes never reach the API graph, and the asset's
     interface list still matches this script's expectations
  2. full HTTP roundtrip -- POST /prompt -> poll /history -> GET /view for the
     .mp3 under SaveAudioAdvanced's ``audio`` key (the key collect_images()
     ignores), plus prompt preservation (``<prefix>.api.json`` + ``requests.jsonl``)

Run:
  python3 scripts/test_skill.py
Exit code 0 = every check passed.
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
import comfyui_music as cm  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []

# The template's subgraph interface names; a workflow edit that renames one of
# these silently breaks every profile parameter, so it is pinned here.
EXPECTED_INTERFACES = [
    "caption", "lyrics", "max_duration", "seed",
    "unet_name", "clip_name", "vae_name", "switch",
]


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(ok), "" if ok else str(detail)))


def graph(**kw):
    set_pairs = kw.pop("set_pairs", None)
    overrides = {k: v for k, v in cm.build_overrides(**kw).items() if v is not None}
    report: dict = {}
    api, out_id, warnings, _prof, merged = cm.build_graph(
        cm.DEFAULT_WORKFLOW, cm.DEFAULT_PROFILE, overrides, set_pairs, report=report
    )
    return api, out_id, warnings, merged, report


def _find(api: dict, class_type: str) -> dict:
    for node in api.values():
        if node.get("class_type") == class_type:
            return node
    return {}


# --------------------------------------------------------------------------- 1
def test_conversion() -> None:
    ui = json.load(open(cm.DEFAULT_WORKFLOW, encoding="utf-8"))
    sub = (ui.get("definitions") or {}).get("subgraphs") or []
    check("workflow has a definitions.subgraphs entry", len(sub) == 1, f"got {len(sub)}")
    iface = [i.get("name") for i in (sub[0].get("inputs") or [])] if sub else []
    check("subgraph interface names unchanged", iface == EXPECTED_INTERFACES, f"got {iface}")

    # every asset file the profile points at really exists next to the workflow
    check("profile next to workflow", os.path.isfile(cm.DEFAULT_PROFILE))
    prof = cm.load_profile(cm.DEFAULT_PROFILE)
    check("profile declares the 8 interfaces + node fields",
          len(prof.get("parameters", {})) >= 15, f"got {len(prof.get('parameters', {}))}")

    # required models must be exactly what the workflow hard-codes (no drift)
    names = cm.workflow_model_names(cm.DEFAULT_WORKFLOW)
    declared = {name for _folder, name in cm.REQUIRED_MODELS}
    check("REQUIRED_MODELS matches the workflow's loaders",
          set(names.values()) == declared, f"workflow={sorted(names.values())} declared={sorted(declared)}")
    check("CLIPLoader type is minimax", cm.workflow_clip_type(cm.DEFAULT_WORKFLOW) == "minimax",
          cm.workflow_clip_type(cm.DEFAULT_WORKFLOW))

    api, out_id, warnings, merged, report = graph(
        caption="solo guqin, 66 BPM", lyrics=None, duration=20.0, seed=42,
        tiled_decode=True, tile_size=1024, filename_prefix="audio/test-bgm",
    )
    check("no conversion warnings", not warnings, warnings)
    check("every override applied", report.get("unapplied") == {}, report.get("unapplied"))
    check("output node is the audio saver",
          api.get(str(out_id), {}).get("class_type") == "SaveAudioAdvanced", out_id)
    check("graph has no UI-only note nodes",
          not any(n.get("class_type") in ("MarkdownNote", "Note") for n in api.values()))

    enc = _find(api, "MiniMaxMusic3TextEncode")
    check("caption reaches the text encoder", enc["inputs"].get("caption") == "solo guqin, 66 BPM",
          enc["inputs"].get("caption"))
    check("duration lands on max_duration", enc["inputs"].get("max_duration") == 20.0,
          enc["inputs"].get("max_duration"))
    empty = _find(api, "EmptyMiniMaxMusic3LatentAudio")
    check("latent seconds stays link-driven (single duration knob)",
          isinstance(empty["inputs"].get("seconds"), list), empty["inputs"])
    check("latent link points at the text encoder's FLOAT output",
          empty["inputs"].get("seconds") == [enc_node_id(api), 1], empty["inputs"].get("seconds"))
    seed_node = _find(api, "SeedNode")
    check("seed reaches SeedNode", seed_node["inputs"].get("seed") == 42, seed_node["inputs"])
    check("seed node still links into the sampler",
          isinstance(_find(api, "KSampler")["inputs"].get("seed"), list))
    check("tiled decode switch flipped on", _find(api, "ComfySwitchNode")["inputs"].get("switch") is True)
    check("tile_size applied", _find(api, "VAEDecodeAudioTiled")["inputs"].get("tile_size") == 1024)
    check("filename_prefix applied",
          _find(api, "SaveAudioAdvanced")["inputs"].get("filename_prefix") == "audio/test-bgm")

    # defaults must survive when a knob is not passed
    api2, _o2, _w2, _m2, _r2 = graph(caption="x", duration=12.0)
    check("mp3/V0 saver defaults survive the conversion",
          _find(api2, "SaveAudioAdvanced")["inputs"].get("format") == "mp3"
          and _find(api2, "SaveAudioAdvanced")["inputs"].get("format.quality") == "V0")
    check("template sampler defaults are euler/simple/30",
          _find(api2, "KSampler")["inputs"].get("sampler_name") == "euler"
          and _find(api2, "KSampler")["inputs"].get("scheduler") == "simple"
          and _find(api2, "KSampler")["inputs"].get("steps") == 30)

    # --instrumental only rewrites lyrics; --set is the escape hatch
    api3, _o3, _w3, _m3, _r3 = graph(caption="x", lyrics=cm.INSTRUMENTAL_LYRICS, duration=8.0,
                                     set_pairs=["KSampler.denoise=0.9"])
    check("instrumental lyric script applied",
          _find(api3, "MiniMaxMusic3TextEncode")["inputs"].get("lyrics") == cm.INSTRUMENTAL_LYRICS)
    check("--set escape hatch reaches an unnamed field",
          _find(api3, "KSampler")["inputs"].get("denoise") == 0.9)
    check("instrumental script carries the [instrumental] tag",
          "[instrumental]" in cm.INSTRUMENTAL_LYRICS)

    # cfg_scale pins both guidance fields unless sampler_cfg is given explicitly
    api4, _o4, _w4, _m4, _r4 = graph(caption="x", duration=8.0, cfg_scale=2.5)
    check("cfg_scale pins the text encoder",
          _find(api4, "MiniMaxMusic3TextEncode")["inputs"].get("cfg_scale") == 2.5)
    check("cfg_scale also pins the sampler cfg",
          _find(api4, "KSampler")["inputs"].get("cfg") == 2.5)
    api5, _o5, _w5, _m5, _r5 = graph(caption="x", duration=8.0, cfg_scale=2.5, sampler_cfg=1.1)
    check("explicit sampler_cfg wins over the shared default",
          _find(api5, "KSampler")["inputs"].get("cfg") == 1.1)

    # cost model: the measured 1000 s for 60 s must stay encoded
    check("ETA is ~16.7x the audio duration",
          cm.estimate_wall(60) == 1002.0 and cm.estimate_wall(None) is None,
          cm.estimate_wall(60))

    # collect_media must see the audio key (unlike the image collector)
    entry = {"outputs": {"35": {"audio": [{"filename": "a_00001_.mp3", "subfolder": "audio"}]},
                         "9": {"images": [{"filename": "decoy.png", "subfolder": ""}]}}}
    got = cm.collect_media(entry, only_node="35")
    check("collect_media picks up the audio key", len(got) == 1 and got[0]["filename"] == "a_00001_.mp3", got)
    check("collect_media honours only_node", all(g["node_id"] == "35" for g in got), got)
    check("collect_media would find images/other keys too",
          cm.collect_media(entry, only_node="9")[0]["filename"] == "decoy.png")

    # a missing caption is a hard error (a run is expensive)
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            cm.main([])
            code = 0
        except SystemExit as exc:  # argparse error path
            code = exc.code
    check("no caption -> argparse refuses to submit", code == 2, f"exit={code}")


def enc_node_id(api: dict) -> str:
    for nid, node in api.items():
        if node.get("class_type") == "MiniMaxMusic3TextEncode":
            return str(nid)
    return ""


# --------------------------------------------------------------------------- 2
class _Handler(BaseHTTPRequestHandler):
    audio = b"ID3\x03\x00\x00\x00\x00\x00\x00fake-mp3-payload"
    prompt_id = "mock-music-1"

    def log_message(self, *_args):  # keep the test output clean
        return

    def _send(self, payload: bytes, ctype="application/json"):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(length) or b"{}")
        type(self).last_prompt = body.get("prompt") or {}
        self._send(json.dumps({"prompt_id": self.prompt_id}).encode())

    def do_GET(self):  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/view":
            return self._send(type(self).audio, "audio/mpeg")
        if parsed.path.startswith("/history/"):
            entry = {
                self.prompt_id: {
                    "status": {"status_str": "success", "completed": True},
                    "outputs": {
                        "35": {"audio": [{"filename": "test-bgm_00001_.mp3",
                                          "subfolder": "audio", "type": "output"}]},
                        "9": {"images": [{"filename": "preview_00001_.png",
                                          "subfolder": "temp", "type": "temp"}]},
                    },
                }
            }
            return self._send(json.dumps(entry).encode())
        self.send_response(404)
        self.end_headers()


def test_roundtrip() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    out_dir = tempfile.mkdtemp(prefix="music-skill-")
    try:
        result = cm.generate(
            server=base, out_dir=out_dir, quiet=True, poll=0.2, timeout=20.0,
            caption="solo guqin, sparse, 66 BPM", lyrics=cm.INSTRUMENTAL_LYRICS,
            duration=6.0, seed=7, filename_prefix="audio/test-bgm",
        )
        check("roundtrip downloaded exactly the audio output",
              len(result["local_paths"]) == 1, result["local_paths"])
        path = result["local_paths"][0] if result["local_paths"] else ""
        check("downloaded file is the saver's mp3",
              os.path.basename(path) == "test-bgm_00001_.mp3", os.path.basename(path))
        check("audio bytes match the mock payload",
              os.path.isfile(path) and open(path, "rb").read() == _Handler.audio)
        check("temp preview was NOT downloaded",
              not any(p.endswith(".png") for p in result["local_paths"]))
        check("status reported success", result["status"] == "success", result["status"])
        check("unapplied overrides empty on the real path",
              result["unapplied_overrides"] == {}, result["unapplied_overrides"])

        api_path = os.path.join(out_dir, "test-bgm.api.json")
        check("api graph archived", os.path.isfile(api_path))
        if os.path.isfile(api_path):
            archived = json.load(open(api_path, encoding="utf-8"))
            check("archived graph is the submitted graph",
                  archived == _Handler.last_prompt, "archived != submitted")
        jsonl = os.path.join(out_dir, "requests.jsonl")
        check("requests.jsonl written", os.path.isfile(jsonl))
        if os.path.isfile(jsonl):
            row = json.loads(open(jsonl, encoding="utf-8").read().strip().splitlines()[-1])
            check("request row records engine/caption/eta",
                  row.get("engine") == "minimax-music3-t2m"
                  and row.get("caption") == "solo guqin, sparse, 66 BPM"
                  and row.get("eta_s") == cm.estimate_wall(6.0),
                  {k: row.get(k) for k in ("engine", "caption", "eta_s")})
        check("workflow asset hash pinned",
              hashlib.sha256(open(cm.DEFAULT_WORKFLOW, "rb").read()).hexdigest()[:12]
              == "841b9320ec6e",
              hashlib.sha256(open(cm.DEFAULT_WORKFLOW, "rb").read()).hexdigest()[:12])
    finally:
        server.shutdown()
        shutil.rmtree(out_dir, ignore_errors=True)


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
