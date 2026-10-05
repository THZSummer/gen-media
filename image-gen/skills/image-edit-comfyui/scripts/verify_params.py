#!/usr/bin/env python3
"""Live parameter verification for the image-edit-comfyui skill.

Generates synthetic control images (no third-party deps), runs the real
workflow on the ComfyUI server for every option, and proves each change
actually reached the sampler graph by comparing output pixels.

  python3 scripts/verify_params.py                 # full matrix
  python3 scripts/verify_params.py --server URL    # custom server
Exit code 0 = every parameter took effect.
"""
from __future__ import annotations

import argparse
import json
import os
import struct
import sys
import time
import urllib.error
import urllib.request
import zlib  # for the local PNG fixture writer below

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _shared  # noqa: E402

_shared.ensure()

import comfyui_convert as cc  # noqa: E402
import comfyui_edit as ce  # noqa: E402
import pngdiff  # noqa: E402  (shared tool; lives in the sibling skill)

VERIFY_DIR = os.path.normpath(os.path.join(HERE, "..", ".verify"))


# ------------------------------------------------------------------ PNG writer
def write_png(path: str, width: int, height: int, pixel) -> str:
    """Minimal RGB PNG writer; pixel(x, y) -> (r, g, b)."""
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter: none
        for x in range(width):
            raw.extend(pixel(x, y))
    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data)) + tag + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)
    return path


def blocks_pattern(seed: int = 0):
    """Hard-edged geometric pattern: gives Canny plenty of structure."""
    def pixel(x: int, y: int, _s=seed):
        if (x // 64 + y // 64 + _s) % 2 == 0:
            return (240, 235, 225)
        if abs(x - y) < 12:
            return (30, 40, 60)
        if (x % 128) < 10 or (y % 128) < 10:
            return (120, 90, 60)
        return (90, 110, 130)
    return pixel


def circles_pattern(shift: int = 0):
    def pixel(x: int, y: int, _s=shift):
        cx, cy = 256 + _s, 256
        d = int(((x - cx) ** 2 + (y - cy) ** 2) ** 0.5)
        return (255 - d % 255, 128, (d * 3) % 255)
    return pixel


# ------------------------------------------------------------------ helpers
# Pixel comparison lives in the shared engine skill (text-to-image-comfyui)
# so both skills apply exactly one criterion: decoded pixels, never file bytes.

pixels_equal = pngdiff.pixels_equal


def png_size(path: str) -> tuple[int, int]:
    head = open(path, "rb").read(24)
    return struct.unpack(">II", head[16:24])


def payload_for(image_name: str, profile: dict, **params) -> dict:
    """Build the API graph without submitting (payload-level assertions)."""
    ui = json.load(open(ce.DEFAULT_WORKFLOW, encoding="utf-8"))
    overrides = ce.build_overrides(image_name=image_name, **params)
    graph, _save, _warn = cc.convert_ex(ui, overrides, profile)
    return graph


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=ce.DEFAULT_SERVER)
    ap.add_argument("--timeout", type=float, default=600.0)
    args = ap.parse_args(argv)

    os.makedirs(VERIFY_DIR, exist_ok=True)
    ref = write_png(os.path.join(VERIFY_DIR, "ctrl-512.png"), 512, 512, blocks_pattern())
    ref2 = write_png(os.path.join(VERIFY_DIR, "ctrl-512b.png"), 512, 512, circles_pattern())
    big = write_png(os.path.join(VERIFY_DIR, "ctrl-640.png"), 640, 640, blocks_pattern(1))

    profile = cc.load_profile(ce.DEFAULT_PROFILE)
    results: list[tuple[str, bool, str]] = []

    def record(name: str, ok: bool, detail: str) -> None:
        results.append((name, ok, detail))
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)

    run_dir = os.path.join(VERIFY_DIR, "out")
    runs: dict[str, dict] = {}

    def run(tag: str, image: str = ref, **params) -> dict:
        t0 = time.time()
        res = ce.generate(
            server=args.server, image=image, out_dir=os.path.join(run_dir, tag),
            filename_prefix=f"v-{tag}", timeout=args.timeout, quiet=True, **params
        )
        res["seconds"] = time.time() - t0
        runs[tag] = res
        if not res["local_paths"]:
            record(f"run:{tag}", False, "no image produced")
        return res

    # ---------------------------------------------------------------- baseline
    base = run("base", prompt="realistic photo of a porcelain doll, studio light", seed=11, steps=8)
    if not base["local_paths"]:
        print("baseline failed; aborting")
        return 1
    base_path = base["local_paths"][0]
    base_size = png_size(base_path)
    record("baseline", True, f"{os.path.basename(base_path)} {base_size} in {base['seconds']:.1f}s")

    # ------------------------------------------------------- control image size
    record("output follows control image", base_size == (512, 512), f"size={base_size} (control 512x512)")

    # ------------------------------------------------------------- each option
    def differs(tag: str, detail: str, **params) -> None:
        res = run(tag, **params)
        if res["local_paths"]:
            diff = pngdiff.compare(base_path, res["local_paths"][0])
            record(tag, not diff.same, f"{detail} -- {diff.detail}")

    differs("prompt", "different prompt -> different image",
            prompt="an oil painting of a castle at sunset", seed=11, steps=8)
    differs("seed", "different seed -> different image", seed=99, steps=8)
    r_repro = run("seed-repro", prompt="realistic photo of a porcelain doll, studio light", seed=11, steps=8)
    if r_repro["local_paths"]:
        same, detail = pixels_equal(base_path, r_repro["local_paths"][0])
        record("seed reproducible", same, f"same seed -> {detail} (ComfyUI embeds the graph in PNG tEXt, so bytes differ)")
    if base["local_paths"]:
        # the UI-only "upload" combo must never reach the API graph
        first_graph = json.load(open(os.path.join(run_dir, "base", "v-base.api.json"), encoding="utf-8"))
        load_inputs = first_graph["58"]["inputs"]
        record("UI-only fields dropped",
               load_inputs == {"image": runs["base"]["control_image"]},
               f"LoadImage inputs={load_inputs}")
    differs("steps", "steps 4 != steps 8", seed=11, steps=4)
    differs("cfg", "cfg 2.0 != cfg 1.0", seed=11, steps=8, cfg=2.0)
    differs("sampler", "euler != res_multistep", seed=11, steps=8, sampler="euler")
    differs("scheduler", "normal != simple", seed=11, steps=8, scheduler="normal")
    differs("denoise", "denoise 0.6 != 1.0", seed=11, steps=8, denoise=0.6)
    differs("shift", "shift 1.5 != 3.0", seed=11, steps=8, shift=1.5)
    differs("control-strength", "strength 0.2 != 1.0", seed=11, steps=8, control_strength=0.2)
    differs("control-window", "start/end 0.2/0.8 != 0/1", seed=11, steps=8, control_start=0.2, control_end=0.8)
    differs("canny-thresholds", "low/high 0.4/0.8 != 0.1/0.32", seed=11, steps=8, canny_low=0.4, canny_high=0.8)

    # ------------------------------------------------------------- forced size
    r_size = run("forced-size", prompt="realistic photo of a porcelain doll, studio light",
                 seed=11, steps=8, width=640, height=640)
    if r_size["local_paths"]:
        got = png_size(r_size["local_paths"][0])
        record("width/height force", got == (640, 640), f"size={got} (expected (640,640))")

    # ------------------------------------------------------------------ batch
    r_batch = run("batch", prompt="realistic photo of a porcelain doll, studio light",
                  seed=11, steps=8, batch_size=2)
    record("batch_size", len(r_batch["local_paths"]) == 2, f"{len(r_batch['local_paths'])} images")

    # --------------------------------------------------------- filename_prefix
    if r_batch["local_paths"]:
        ok = all(os.path.basename(p).startswith("v-batch") for p in r_batch["local_paths"])
        record("filename_prefix", ok, os.path.basename(r_batch["local_paths"][0]))

    # ------------------------------------ pre-scale node (bypassed by default)
    r_prescale = run("max-dimension", image=big, prompt="realistic photo of a porcelain doll",
                     seed=11, steps=8, max_dimension=256)
    if r_prescale["local_paths"]:
        got = png_size(r_prescale["local_paths"][0])
        record("max_dimension enables pre-scale", max(got) <= 256, f"size={got} (control 640, cap 256)")

    # ------------------------------------------------------- preprocessor off
    r_nopre = run("no-preprocessor", prompt="realistic photo of a porcelain doll",
                  seed=11, steps=8, disable_nodes=["Canny"])
    if r_nopre["local_paths"]:
        graph = json.load(open(os.path.join(run_dir, "no-preprocessor", "v-no-preprocessor.api.json"),
                              encoding="utf-8"))
        record("no-preprocessor", "57" not in graph, f"Canny absent, ControlNet reads {graph['60']['inputs']['image']}")

    # ------------------------------------------------- server-side image reuse
    first_name = runs["base"]["control_image"]
    r_reuse = ce.generate(server=args.server, image_name=first_name,
                          out_dir=os.path.join(run_dir, "image-name"), filename_prefix="v-image-name",
                          prompt="realistic photo of a porcelain doll, studio light", seed=11, steps=8,
                          timeout=args.timeout, quiet=True)
    record("image_name (no re-upload)", bool(r_reuse["local_paths"]), f"reused {first_name}")

    # --------------------------------------------------- second control image
    r_alt = run("second-image", image=ref2, prompt="realistic photo of a porcelain doll, studio light",
                seed=11, steps=8)
    if r_alt["local_paths"]:
        diff = pngdiff.compare(base_path, r_alt["local_paths"][0])
        record("second control image", not diff.same, f"different control -> {diff.detail}")

    # ------------------------------------------- unapplied parameters are loud
    # The exposure for this skill is a profile/workflow drift (a parameter whose
    # node is gone), not a CLI typo -- argparse and build_overrides reject those
    # before the converter ever sees them.  All of this is payload-level: free.
    wf = json.load(open(ce.DEFAULT_WORKFLOW, encoding="utf-8"))
    try:
        cc.convert_ex(wf, {"image": "ref.png", "prompt": "p", "widht": 512}, profile, strict=True)
        record("unknown parameter is rejected", False, "'widht' was silently accepted")
    except cc.UnappliedOverrideError as exc:
        record("unknown parameter is rejected", True, f"raised: {str(exc)[:60]}")
    probe: dict = {}
    _api, _id, warns = cc.convert_ex(wf, {"image": "ref.png", "prompt": "p", "widht": 512}, profile,
                                     strict=False, report=probe)
    record("strict=False still reports the key",
           probe.get("unapplied") == {"widht": 512} and any("unapplied" in w for w in warns),
           f"unapplied={probe.get('unapplied')}")

    # every declared profile parameter must land, or the skill says so
    every = {k: (s.get("default") if s.get("default") is not None else 1)
             for k, s in profile["parameters"].items()}
    every.update({"image": "ref.png", "prompt": "p"})
    full: dict = {}
    cc.convert_ex(wf, every, profile, strict=False, report=full)
    record("no silent drops on the real profile", full.get("unapplied") == {},
           f"{len(full.get('applied', []))}/{len(every)} params applied, unapplied {full.get('unapplied')}")

    # a parameter whose node class vanished from the workflow must be reported
    drifted = json.loads(json.dumps(profile))
    drifted["parameters"]["ghost_param"] = {"node": "NoSuchNodeClass", "field": "x", "force": True}
    ghost: dict = {}
    try:
        cc.convert_ex(wf, {"image": "ref.png", "prompt": "p", "ghost_param": 1}, drifted,
                      strict=True, report=ghost)
        record("workflow/node drift is rejected", False, "ghost_param was silently dropped")
    except cc.UnappliedOverrideError:
        record("workflow/node drift is rejected", True, f"raised (applied={ghost.get('applied')})")

    # ------------------------------------------------------ payload assertions
    graph = payload_for("ref.png", profile, prompt="p", steps=3, cfg=2.0, sampler="euler",
                        scheduler="karras", denoise=0.7, shift=2.0, control_strength=0.5,
                        control_start=0.1, control_end=0.9, canny_low=0.02, canny_high=0.2,
                        width=600, height=600, batch_size=4, filename_prefix="pfx",
                        unet_name="U.safetensors", clip_name="C.safetensors",
                        vae_name="V.safetensors", controlnet_name="P.safetensors")
    checks = {
        "steps": graph["44"]["inputs"].get("steps") == 3,
        "cfg": graph["44"]["inputs"].get("cfg") == 2.0,
        "sampler": graph["44"]["inputs"].get("sampler_name") == "euler",
        "scheduler": graph["44"]["inputs"].get("scheduler") == "karras",
        "denoise": graph["44"]["inputs"].get("denoise") == 0.7,
        "shift": graph["47"]["inputs"].get("shift") == 2.0,
        "control": (graph["60"]["inputs"].get("strength") == 0.5
                    and graph["60"]["inputs"].get("start_percent") == 0.1
                    and graph["60"]["inputs"].get("end_percent") == 0.9),
        "canny": (graph["57"]["inputs"].get("low_threshold") == 0.02
                  and graph["57"]["inputs"].get("high_threshold") == 0.2),
        "latent": (graph["41"]["inputs"].get("width") == 600
                   and graph["41"]["inputs"].get("height") == 600
                   and graph["41"]["inputs"].get("batch_size") == 4),
        "models": (graph["46"]["inputs"].get("unet_name") == "U.safetensors"
                   and graph["39"]["inputs"].get("clip_name") == "C.safetensors"
                   and graph["40"]["inputs"].get("vae_name") == "V.safetensors"
                   and graph["64"]["inputs"].get("name") == "P.safetensors"),
        "save_prefix": graph["9"]["inputs"].get("filename_prefix") == "pfx",
    }
    bad = [k for k, v in checks.items() if not v]
    record("payload: all params present", not bad, "all present" if not bad else f"missing/incorrect: {bad}")

    # ------------------------------------------- server-side model validation
    bad_graph = payload_for("ref.png", profile, prompt="p", controlnet_name="nope-not-a-model.safetensors")
    body = json.dumps({"prompt": bad_graph, "client_id": "verify"}).encode()
    req = urllib.request.Request(f"{args.server.rstrip('/')}/prompt", data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp.read()
        record("invalid controlnet rejected", False, "server accepted a bogus patch model")
    except urllib.error.HTTPError as exc:
        record("invalid controlnet rejected", exc.code == 400, f"HTTP {exc.code}")

    print()
    failed = [r for r in results if not r[1]]
    print(f"{len(results) - len(failed)}/{len(results)} checks passed")
    for name, _, detail in failed:
        print(f"  FAILED {name}: {detail}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
