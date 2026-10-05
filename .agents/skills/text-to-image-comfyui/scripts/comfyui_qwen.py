#!/usr/bin/env python3
"""Qwen-Image text-to-image engine for the ComfyUI skill.

Z-Image-Turbo (see comfyui_gen.py) is fast but stylized; Qwen-Image renders far
finer surface detail and, unlike the z-image workflow, supports a real negative
prompt. Both talk to the same server.

Graph:
  UNETLoader(qwen_image) -> ModelSamplingAuraFlow(shift) -> KSampler
  CLIPLoader(qwen_2.5_vl, type=qwen_image) -> CLIPTextEncode (positive/negative)
  EmptySD3LatentImage -> KSampler(euler/simple, cfg) -> VAEDecode -> SaveImage

Usage:
  python3 comfyui_qwen.py --prompt "..." --negative "..." \
      --width 1024 --height 1360 --steps 24 --cfg 3.0 --seed 7 --out-dir out/
  python3 comfyui_qwen.py --check        # verify the three model files exist
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comfyui_gen import (  # noqa: E402
    DEFAULT_SERVER,
    _get_json,
    collect_images,
    download_image,
    list_models,
    queue_prompt,
    record_request,
    wait_for_history,
)

DEFAULTS = {
    "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors",
    "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
    "vae_name": "qwen_image_vae.safetensors",
    "clip_type": "qwen_image",
    "shift": 3.0,
    "sampler": "euler",
    "scheduler": "simple",
}
REQUIRED_MODELS = [
    ("diffusion_models", DEFAULTS["unet_name"]),
    ("text_encoders", DEFAULTS["clip_name"]),
    ("vae", DEFAULTS["vae_name"]),
]

# Every key build_graph() understands as a keyword.  The graph is assembled in
# Python rather than converted from a UI JSON, so an unrecognised key would
# otherwise be swallowed by **overrides and the run would silently use a default
# -- the same silent-no-op failure mode the converter now rejects.
OVERRIDE_KEYS: tuple[str, ...] = (
    "unet_name",
    "clip_name",
    "vae_name",
    "clip_type",
    "shift",
    "sampler",
    "scheduler",
)


def _reject_unknown_overrides(overrides: dict) -> dict:
    unknown = sorted(set(overrides) - set(OVERRIDE_KEYS))
    if unknown:
        raise ValueError(
            f"unknown Qwen parameter(s): {', '.join(unknown)} "
            f"(known: {', '.join(OVERRIDE_KEYS)})"
        )
    return overrides


def build_graph(
    prompt: str,
    negative: str = "",
    width: int = 1024,
    height: int = 1360,
    steps: int = 24,
    cfg: float = 3.0,
    seed: int = 0,
    batch_size: int = 1,
    prefix: str = "qwen",
    **overrides,
) -> dict:
    _reject_unknown_overrides(overrides)
    unet = overrides.get("unet_name") or DEFAULTS["unet_name"]
    clip = overrides.get("clip_name") or DEFAULTS["clip_name"]
    vae = overrides.get("vae_name") or DEFAULTS["vae_name"]
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": unet, "weight_dtype": "default"}},
        "2": {
            "class_type": "ModelSamplingAuraFlow",
            "inputs": {"model": ["1", 0], "shift": overrides.get("shift", DEFAULTS["shift"])},
        },
        "3": {
            "class_type": "CLIPLoader",
            "inputs": {
                "clip_name": clip,
                "type": overrides.get("clip_type", DEFAULTS["clip_type"]),
                "device": "default",
            },
        },
        "4": {"class_type": "VAELoader", "inputs": {"vae_name": vae}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["3", 0], "text": prompt}},
        "6": {
            "class_type": "EmptySD3LatentImage",
            "inputs": {"width": width, "height": height, "batch_size": batch_size},
        },
        "7": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["2", 0],
                "positive": ["5", 0],
                "negative": ["8", 0],
                "latent_image": ["6", 0],
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": overrides.get("sampler", DEFAULTS["sampler"]),
                "scheduler": overrides.get("scheduler", DEFAULTS["scheduler"]),
                "denoise": 1.0,
            },
        },
        "8": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["3", 0], "text": negative}},
        "9": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["4", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": prefix}},
    }


def check_models(server: str) -> list[str]:
    missing: list[str] = []
    for folder, name in REQUIRED_MODELS:
        try:
            files = list_models(server, folder)
        except Exception as exc:  # noqa: BLE001
            missing.append(f"{folder}: cannot list ({exc})")
            continue
        if name not in files:
            missing.append(f"{folder}/{name} not found")
    return missing


def generate(
    server: str = DEFAULT_SERVER,
    prompt: str = "",
    negative: str = "",
    width: int = 1024,
    height: int = 1360,
    steps: int = 24,
    cfg: float = 3.0,
    seed: int = 0,
    batch_size: int = 1,
    filename_prefix: str = "qwen",
    out_dir: str = "out",
    timeout: float = 1800.0,
    poll: float = 3.0,
    quiet: bool = False,
    record: bool = True,
    **overrides,
) -> dict:
    graph = build_graph(
        prompt, negative, width, height, steps, cfg, seed, batch_size, filename_prefix, **overrides
    )
    if not quiet:
        print(f"-> qwen-image @ {server}  {width}x{height} steps={steps} cfg={cfg} seed={seed}", flush=True)
    prompt_id = queue_prompt(server, graph, f"dsh-qwen-{os.getpid()}", timeout=120.0)
    if not quiet:
        print(f"   queued: {prompt_id}", flush=True)
    entry = wait_for_history(server, prompt_id, timeout=timeout, poll=poll, quiet=quiet)
    images = collect_images(entry, only_node="10")
    paths = [download_image(server, img, out_dir) for img in images if img.get("filename")]
    if not quiet:
        for path in paths:
            print(f"   saved: {path} ({os.path.getsize(path)} bytes)", flush=True)
    if record:
        record_request(
            out_dir=out_dir,
            prefix=filename_prefix,
            engine="qwen-image",
            server=server,
            params={
                "prompt": prompt,
                "negative": negative,
                "width": width,
                "height": height,
                "steps": steps,
                "cfg": cfg,
                "seed": seed,
                "batch_size": batch_size,
                "filename_prefix": filename_prefix,
                "unet_name": overrides.get("unet_name") or DEFAULTS["unet_name"],
                "clip_name": overrides.get("clip_name") or DEFAULTS["clip_name"],
                "vae_name": overrides.get("vae_name") or DEFAULTS["vae_name"],
                "sampler": overrides.get("sampler", DEFAULTS["sampler"]),
                "scheduler": overrides.get("scheduler", DEFAULTS["scheduler"]),
                "shift": overrides.get("shift", DEFAULTS["shift"]),
                # always empty: an unknown key raises in build_graph instead of
                # being dropped.  Kept for archive symmetry with comfyui_gen.
                "unapplied": {},
            },
            prompt_id=prompt_id,
            graph=graph,
            files=paths,
        )
    return {
        "prompt_id": prompt_id,
        "images": images,
        "local_paths": paths,
        "status": (entry.get("status") or {}).get("status_str"),
        "unapplied": {},
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=DEFAULT_SERVER)
    ap.add_argument("--prompt")
    ap.add_argument("--negative", default="")
    ap.add_argument("--width", type=int, default=1024)
    ap.add_argument("--height", type=int, default=1360)
    ap.add_argument("--steps", type=int, default=24)
    ap.add_argument("--cfg", type=float, default=3.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--batch", "--batch-size", dest="batch_size", type=int, default=1)
    ap.add_argument("--filename-prefix", default="qwen")
    ap.add_argument("--unet-name")
    ap.add_argument("--clip-name")
    ap.add_argument("--vae-name")
    ap.add_argument("--shift", type=float)
    ap.add_argument("--sampler")
    ap.add_argument("--scheduler")
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--timeout", type=float, default=1800.0)
    ap.add_argument("--poll", type=float, default=3.0)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-record", dest="record", action="store_false",
                    help="do not write <prefix>.api.json / requests.jsonl next to the outputs")
    ap.add_argument("--check", action="store_true", help="verify the Qwen model files exist")
    args = ap.parse_args(argv)

    if args.check:
        missing = check_models(args.server)
        print(json.dumps({"ok": not missing, "missing": missing}, ensure_ascii=False, indent=2))
        return 0 if not missing else 2
    if not args.prompt:
        ap.error("--prompt is required unless --check is used")

    result = generate(
        server=args.server,
        prompt=args.prompt,
        negative=args.negative,
        width=args.width,
        height=args.height,
        steps=args.steps,
        cfg=args.cfg,
        seed=args.seed,
        batch_size=args.batch_size,
        filename_prefix=args.filename_prefix,
        out_dir=args.out_dir,
        timeout=args.timeout,
        poll=args.poll,
        quiet=args.quiet,
        record=args.record,
        **{
            k: v
            for k, v in {
                "unet_name": args.unet_name,
                "clip_name": args.clip_name,
                "vae_name": args.vae_name,
                "shift": args.shift,
                "sampler": args.sampler,
                "scheduler": args.scheduler,
            }.items()
            if v is not None
        },
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["local_paths"] else 1


if __name__ == "__main__":
    sys.exit(main())
