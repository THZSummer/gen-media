#!/usr/bin/env python3
"""Live parameter-matrix check for the ComfyUI text-to-image skill.

Runs a real generation for every workflow parameter and proves the change
actually reached the sampler by comparing **decoded pixels**.

Why pixels and not file hashes: ComfyUI embeds the executed graph in the PNG's
``tEXt`` chunk, so anything that alters the graph -- including the
``filename_prefix`` this skill sets per run -- changes the file hash while the
image stays bit-identical.  A sha256 "is this reproducible?" check therefore
reports failures that are not failures; see ``pngdiff.py`` for the measured case.

Usage:
  python3 scripts/verify_params.py                      # default server
  python3 scripts/verify_params.py --server http://192.168.3.5:18000 --out-dir out/verify
  python3 scripts/verify_params.py --quick              # 4 generations instead of 7
  python3 scripts/verify_params.py --tolerance 2        # ignore tiny channel deltas

Exit code 0 = every checked parameter took effect.
"""
from __future__ import annotations

import argparse
import json
import os
import struct
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Deterministic image tooling (pixel diff, contact sheets, PNG encode/decode)
# lives in the sibling `image-tools` skill -- the AI-free layer this skill
# depends on, not the other way round.
_TOOLS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "image-tools", "scripts"))
if os.path.isdir(_TOOLS) and _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
import comfyui_convert as cc  # noqa: E402
import comfyui_gen as cg  # noqa: E402
import pngdiff  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
WORKFLOW = os.path.join(HERE, "..", "assets", "z-image-turbo-ui.json")
DEFAULT_SERVER = cg.DEFAULT_SERVER


def png_size(path: str) -> tuple[int, int]:
    with open(path, "rb") as fh:
        head = fh.read(24)
    return struct.unpack(">II", head[16:24])


def changed(a: str, b: str, tolerance: int = 0) -> tuple[bool, str]:
    """True when the two images really differ, with the pixel-level detail."""
    diff = pngdiff.compare(a, b, tolerance)
    return (not diff.same), diff.detail


def same_pixels(a: str, b: str, tolerance: int = 0) -> tuple[bool, str]:
    return pngdiff.pixels_equal(a, b, tolerance)


def run(server: str, out_dir: str, timeout: float, **params) -> tuple[dict, float]:
    t0 = time.time()
    result = cg.generate(
        server=server,
        workflow=WORKFLOW,
        out_dir=out_dir,
        timeout=timeout,
        poll=2.0,
        quiet=True,
        **params,
    )
    return result, time.time() - t0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=DEFAULT_SERVER)
    ap.add_argument("--out-dir", default=os.path.join(HERE, "..", "out", "verify"))
    ap.add_argument("--timeout", type=float, default=900.0)
    ap.add_argument("--quick", action="store_true", help="4 generations instead of the full matrix")
    ap.add_argument("--tolerance", type=int, default=0,
                    help="max per-channel delta still counted as identical (default 0)")
    args = ap.parse_args(argv)

    results: list[tuple[str, bool, str]] = []
    skipped: list[str] = []

    # Fail fast: without this the matrix blocks for the full --timeout on a dead
    # server and reports it as a "baseline produced no image" mystery.
    probe = cg.check_server(args.server, timeout=10.0)
    if not probe["reachable"]:
        print(f"server {args.server} unreachable: {probe['error']}", file=sys.stderr)
        print("see references/server-192.168.3.5.md for the network triage", file=sys.stderr)
        return 2
    print(f"server {args.server} reachable"
          + (f" (ComfyUI {probe['stats'].get('system', {}).get('comfyui_version')})"
             if isinstance(probe.get("stats"), dict) else ""), flush=True)

    def record(name: str, ok: bool, detail: str) -> None:
        results.append((name, ok, detail))
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)

    def skip(name: str) -> None:
        skipped.append(name)
        print(f"[SKIP] {name}: --quick", flush=True)

    # ---------------------------------------------------------------- base
    base_prompt = "a red fox in fresh snow, cinematic close-up"
    base, t_base = run(args.server, args.out_dir, args.timeout, prompt=base_prompt,
                       width=768, height=768, steps=6, seed=11)
    if not base["local_paths"]:
        print("base generation produced no image; aborting")
        return 1
    base_path = base["local_paths"][0]
    record("baseline", True, f"{os.path.basename(base_path)} {png_size(base_path)} {t_base:.1f}s")

    # ------------------------------------------------- 1. prompt takes effect
    r, _ = run(args.server, args.out_dir, args.timeout, prompt="a blue whale in the sky, surreal",
               width=768, height=768, steps=6, seed=11)
    other_prompt = r["local_paths"][0]
    diff, detail = changed(base_path, other_prompt, args.tolerance)
    record("--prompt", diff, f"changed image {os.path.basename(other_prompt)}: {detail}")

    # ---------------------------------------------- 2. width/height take effect
    r, _ = run(args.server, args.out_dir, args.timeout, prompt=base_prompt,
               width=768, height=1152, steps=6, seed=11)
    tall = r["local_paths"][0]
    size = png_size(tall)
    record("--width/--height", size == (768, 1152), f"output size {size} (expected (768, 1152))")

    # ------------------------------------- 3. seed reproducibility (pixel-based)
    r, _ = run(args.server, args.out_dir, args.timeout, prompt=base_prompt,
               width=768, height=768, steps=6, seed=11)
    rerun = r["local_paths"][0]
    same, detail = same_pixels(base_path, rerun, args.tolerance)
    bytes_same = open(base_path, "rb").read() == open(rerun, "rb").read()
    record("--seed reproducible", same,
           f"seed 11 twice -> {detail}; file bytes {'identical' if bytes_same else 'differ (PNG tEXt)'}")

    if args.quick:
        for name in ("--seed changes output", "--steps", "--filename-prefix"):
            skip(name)
    else:
        # ------------------------------------------------ 4. seed takes effect
        r, _ = run(args.server, args.out_dir, args.timeout, prompt=base_prompt,
                   width=768, height=768, steps=6, seed=99)
        seed99 = r["local_paths"][0]
        diff, detail = changed(base_path, seed99, args.tolerance)
        record("--seed changes output", diff, f"seed 99 vs 11: {detail}")

        # ---------------------------------------------- 5. steps takes effect
        r, _ = run(args.server, args.out_dir, args.timeout, prompt=base_prompt,
                   width=768, height=768, steps=3, seed=11)
        steps3 = r["local_paths"][0]
        diff, detail = changed(base_path, steps3, args.tolerance)
        record("--steps", diff, f"steps 3 vs 6: {detail}")

        # ----------------------------------------- 6. filename_prefix applied
        r, _ = run(args.server, args.out_dir, args.timeout, prompt=base_prompt, width=768, height=768,
                   steps=6, seed=11, filename_prefix="paramcheck")
        prefixed = r["local_paths"][0]
        record("--filename-prefix", os.path.basename(prefixed).startswith("paramcheck"),
               os.path.basename(prefixed))

    # -------------------------------------- 7. model overrides are really sent
    ui = json.load(open(WORKFLOW, encoding="utf-8"))
    api, _ = cc.convert(ui, {
        "unet_name": "UNET_UNDER_TEST.safetensors",
        "clip_name": "CLIP_UNDER_TEST.safetensors",
        "vae_name": "VAE_UNDER_TEST.safetensors",
    })
    sent = (api["28"]["inputs"]["unet_name"], api["30"]["inputs"]["clip_name"], api["29"]["inputs"]["vae_name"])
    record("--unet/clip/vae-name (payload)", sent == (
        "UNET_UNDER_TEST.safetensors", "CLIP_UNDER_TEST.safetensors", "VAE_UNDER_TEST.safetensors"),
        f"sent {sent}")

    # -------------------------- 8. server validates those names (rejects junk)
    try:
        cg.queue_prompt(args.server, cc.convert(
            ui, {"prompt": "x", "unet_name": "definitely_not_a_model.safetensors"})[0], "verify-params")
        record("server rejects bad --unet-name", False, "invalid model was accepted")
    except Exception as exc:  # noqa: BLE001
        record("server rejects bad --unet-name", True, f"rejected: {str(exc)[:90]}")

    # ------------------------------- 9. a typo'd parameter must not be silent
    from comfyui_convert import UnappliedOverrideError
    report: dict = {}
    try:
        cc.convert(ui, {"widht": 1536})
        record("typo'd parameter is rejected", False, "'widht' was silently accepted")
    except UnappliedOverrideError as exc:
        record("typo'd parameter is rejected", True, f"raised: {str(exc)[:70]}")
    cc.convert_ex(ui, {"widht": 1536, "width": 512}, report=report)
    record("unapplied keys are reported", report.get("unapplied") == {"widht": 1536},
           f"report {report}")

    # ------------------------------------------------------------ summary
    print()
    failed = [r for r in results if not r[1]]
    print(f"{len(results) - len(failed)}/{len(results)} checks passed"
          + (f" ({len(skipped)} skipped)" if skipped else ""))
    for name, _, detail in failed:
        print(f"  FAILED {name}: {detail}")
    if not args.quick:
        print("\nartifacts:")
        for path in sorted(os.listdir(args.out_dir)):
            print("  ", os.path.join(args.out_dir, path))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
