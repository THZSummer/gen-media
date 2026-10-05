#!/usr/bin/env python3
"""Z-Image-Turbo Fun Union ControlNet image-to-image / editing engine.

Uploads a control image to ComfyUI, runs the control-to-image workflow from
``assets/`` with an optional parameter profile, downloads the results and
records the exact submitted graph (prompt preservation, shared with the
text-to-image skill).

Usage:
  python3 comfyui_edit.py --image ./ref.png --prompt "realistic photo, ..." --out-dir out/
  python3 comfyui_edit.py --image ./ref.png --steps 12 --control-strength 0.7 \
      --canny-low 0.05 --canny-high 0.25 --seed 42 --out-dir out/
  python3 comfyui_edit.py --image ./big.png --max-dimension 1024   # enable the pre-scale node
  python3 comfyui_edit.py --image ./ref.png --no-preprocessor      # feed the raw image to ControlNet
  python3 comfyui_edit.py --list                                   # show every parameter
  python3 comfyui_edit.py --check                                  # verify models on the server
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared  # noqa: E402

_shared.ensure()

from comfyui_convert import (  # noqa: E402
    UnappliedOverrideError,
    convert_ex,
    load_profile,
    resolve_params,
)
from comfyui_gen import (  # noqa: E402
    DEFAULT_SERVER,
    _request,
    collect_images,
    download_image,
    list_models,
    queue_prompt,
    record_request,
    wait_for_history,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))
DEFAULT_WORKFLOW = os.path.join(ASSETS, "z-image-turbo-fun-union-controlnet.json")
DEFAULT_PROFILE = os.path.join(ASSETS, "z-image-turbo-fun-union-controlnet.profile.json")

REQUIRED_MODELS = [
    ("diffusion_models", "z_image_turbo_bf16.safetensors"),
    ("text_encoders", "qwen_3_4b.safetensors"),
    ("vae", "ae.safetensors"),
    ("model_patches", "Z-Image-Turbo-Fun-Controlnet-Union.safetensors"),
]


# --------------------------------------------------------------------------- upload
def upload_image(server: str, path: str, timeout: float = 120.0) -> str:
    """POST a local file to /upload/image and return the widget value to use."""
    with open(path, "rb") as fh:
        data = fh.read()
    boundary = "----dsh" + uuid.uuid4().hex
    name = os.path.basename(path)
    parts = []
    parts.append(f"--{boundary}\r\n".encode())
    parts.append(
        f'Content-Disposition: form-data; name="image"; filename="{name}"\r\n'.encode()
    )
    parts.append(b"Content-Type: application/octet-stream\r\n\r\n")
    parts.append(data)
    parts.append(f"\r\n--{boundary}\r\n".encode())
    parts.append(b'Content-Disposition: form-data; name="overwrite"\r\n\r\n1')
    parts.append(f"\r\n--{boundary}\r\n".encode())
    parts.append(b'Content-Disposition: form-data; name="type"\r\n\r\ninput')
    parts.append(f"\r\n--{boundary}--\r\n".encode())
    body = b"".join(parts)
    raw = _request(
        f"{server.rstrip('/')}/upload/image",
        data=body,
        method="POST",
        timeout=timeout,
        content_type=f"multipart/form-data; boundary={boundary}",
    )
    payload = json.loads(raw.decode("utf-8"))
    sub = payload.get("subfolder") or ""
    return f"{sub}/{payload['name']}" if sub else payload["name"]


# --------------------------------------------------------------------------- engine
def build_overrides(
    prompt=None, negative=None, image_name=None, seed=None, steps=None, cfg=None,
    sampler=None, scheduler=None, denoise=None, shift=None, sampling=None,
    control_strength=None, control_start=None, control_end=None,
    canny_low=None, canny_high=None, width=None, height=None, batch_size=None,
    filename_prefix=None, max_dimension=None, scale_method=None,
    unet_name=None, clip_name=None, vae_name=None, controlnet_name=None,
) -> dict:
    """Collect CLI values into the profile's parameter keys (None = keep default)."""
    return {
        "image": image_name,
        "prompt": prompt,
        "seed": seed,
        "steps": steps,
        "cfg": cfg,
        "sampler": sampler,
        "scheduler": scheduler,
        "denoise": denoise,
        "shift": shift,
        "sampling": sampling,
        "control_strength": control_strength,
        "control_start": control_start,
        "control_end": control_end,
        "canny_low": canny_low,
        "canny_high": canny_high,
        "width": width,
        "height": height,
        "batch_size": batch_size,
        "filename_prefix": filename_prefix,
        "max_dimension": max_dimension,
        "scale_method": scale_method,
        "unet_name": unet_name,
        "clip_name": clip_name,
        "vae_name": vae_name,
        "controlnet_name": controlnet_name,
    }


def generate(
    server: str = DEFAULT_SERVER,
    workflow: str = DEFAULT_WORKFLOW,
    profile: str | dict | None = DEFAULT_PROFILE,
    image: str | None = None,
    image_name: str | None = None,
    disable_nodes: list[str] | None = None,
    out_dir: str = "out",
    timeout: float = 900.0,
    poll: float = 2.0,
    quiet: bool = False,
    record: bool = True,
    strict: bool = True,
    **params,
) -> dict:
    """Run one control-to-image generation.

    ``image``      local file to upload (preferred)
    ``image_name`` an existing file in the server's input directory
    ``strict``     fail when a requested parameter has no input to land on
                   (default), instead of running with it silently ignored
    """
    prof = load_profile(profile) if isinstance(profile, str) else profile
    if image and not image_name:
        image_name = upload_image(server, image)
        if not quiet:
            print(f"   uploaded: {image_name}", flush=True)
    if not image_name:
        raise ValueError("no control image: pass image=<local path> or image_name=<server file>")

    overrides = build_overrides(image_name=image_name, **params)
    ui = json.load(open(workflow, encoding="utf-8"))
    node_modes = {cls: 4 for cls in (disable_nodes or [])}
    convert_report: dict = {}
    api_prompt, save_id, warnings = convert_ex(
        ui, overrides, prof, node_modes, strict=strict, report=convert_report
    )
    unapplied = convert_report.get("unapplied") or {}
    if warnings and not quiet:
        for warning in warnings:
            print(f"   warning: {warning}", file=sys.stderr)
    if save_id is None:
        raise RuntimeError("workflow has no SaveImage node; cannot locate outputs")

    prefix = params.get("filename_prefix") or "z-image-turbo-fun"
    if not quiet:
        print(
            f"-> control-to-image @ {server}  image={image_name}  "
            f"steps={overrides.get('steps')} cfg={overrides.get('cfg')} seed={overrides.get('seed')}",
            flush=True,
        )
    prompt_id = queue_prompt(server, api_prompt, f"dsh-edit-{os.getpid()}", timeout=120.0)
    if not quiet:
        print(f"   queued: {prompt_id}", flush=True)
    entry = wait_for_history(server, prompt_id, timeout=timeout, poll=poll, quiet=quiet)
    images = collect_images(entry, only_node=save_id)
    paths = [download_image(server, img, out_dir) for img in images if img.get("filename")]
    if not quiet:
        for path in paths:
            print(f"   saved: {path} ({os.path.getsize(path)} bytes)", flush=True)

    if record:
        record_request(
            out_dir=out_dir,
            prefix=prefix,
            engine="z-image-turbo-fun-controlnet",
            server=server,
            params={
                "control_image": image_name,
                "control_image_local": image,
                "prompt": params.get("prompt"),
                "negative": None,
                "workflow": os.path.basename(workflow),
                "profile": os.path.basename(profile) if isinstance(profile, str) else None,
                "disabled_nodes": sorted(disable_nodes or []),
                **{
                    k: v
                    for k, v in overrides.items()
                    if k not in ("image", "prompt") and v is not None
                },
                "warnings": warnings,
                "unapplied": unapplied,
            },
            prompt_id=prompt_id,
            graph=api_prompt,
            files=paths,
        )
    return {
        "prompt_id": prompt_id,
        "images": images,
        "local_paths": paths,
        "status": (entry.get("status") or {}).get("status_str"),
        "warnings": warnings,
        "unapplied": unapplied,
        "control_image": image_name,
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=DEFAULT_SERVER)
    ap.add_argument("--workflow", default=DEFAULT_WORKFLOW)
    ap.add_argument("--profile", default=DEFAULT_PROFILE)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--image", help="local control image to upload")
    g.add_argument("--image-name", help="control image already in the server's input/ dir")

    ap.add_argument("--prompt")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--steps", type=int)
    ap.add_argument("--cfg", type=float)
    ap.add_argument("--sampler")
    ap.add_argument("--scheduler")
    ap.add_argument("--denoise", type=float)
    ap.add_argument("--shift", type=float)
    ap.add_argument("--sampling", choices=["flow", "img_to_img_velocity"])
    ap.add_argument("--control-strength", type=float)
    ap.add_argument("--control-start", type=float)
    ap.add_argument("--control-end", type=float)
    ap.add_argument("--canny-low", type=float)
    ap.add_argument("--canny-high", type=float)
    ap.add_argument("--width", type=int, help="force latent width (cuts the GetImageSize link)")
    ap.add_argument("--height", type=int, help="force latent height (cuts the GetImageSize link)")
    ap.add_argument("--batch", "--batch-size", dest="batch_size", type=int)
    ap.add_argument("--filename-prefix")
    ap.add_argument("--max-dimension", type=int, help="enable the pre-scale node for this largest size")
    ap.add_argument("--scale-method", help="pre-scale resample filter (enables the pre-scale node)")
    ap.add_argument("--no-preprocessor", action="store_true",
                    help="bypass the Canny node and feed the raw image to ControlNet")
    ap.add_argument("--disable-node", action="append", default=[], metavar="CLASS",
                    help="bypass an arbitrary node class (repeatable)")
    ap.add_argument("--unet-name")
    ap.add_argument("--clip-name")
    ap.add_argument("--vae-name")
    ap.add_argument("--controlnet-name")
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--timeout", type=float, default=900.0)
    ap.add_argument("--poll", type=float, default=2.0)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-record", dest="record", action="store_false")
    ap.add_argument("--list", action="store_true", help="print the workflow's parameters and defaults")
    ap.add_argument("--check", action="store_true", help="verify the required models exist on the server")
    ap.add_argument("--allow-unapplied", action="store_true",
                    help="do not fail when a parameter has no node/field to land on")
    args = ap.parse_args(argv)

    if args.check:
        missing = check_models(args.server)
        print(json.dumps({"ok": not missing, "missing": missing}, ensure_ascii=False, indent=2))
        return 0 if not missing else 2
    if args.list:
        ui = json.load(open(args.workflow, encoding="utf-8"))
        prof = load_profile(args.profile)
        print(json.dumps(
            {"interface_defaults": resolve_params(ui),
             "profile_parameters": sorted(prof.get("parameters", {})),
             "defaults": prof.get("defaults", {})},
            ensure_ascii=False, indent=2))
        return 0
    if not (args.image or args.image_name):
        ap.error("--image or --image-name is required")

    disable = list(args.disable_node)
    if args.no_preprocessor:
        disable.append("Canny")

    cli_overrides = build_overrides(
        prompt=args.prompt, seed=args.seed, steps=args.steps, cfg=args.cfg,
        sampler=args.sampler, scheduler=args.scheduler, denoise=args.denoise,
        shift=args.shift, sampling=args.sampling,
        control_strength=args.control_strength, control_start=args.control_start,
        control_end=args.control_end, canny_low=args.canny_low, canny_high=args.canny_high,
        width=args.width, height=args.height, batch_size=args.batch_size,
        filename_prefix=args.filename_prefix, max_dimension=args.max_dimension,
        scale_method=args.scale_method, unet_name=args.unet_name, clip_name=args.clip_name,
        vae_name=args.vae_name, controlnet_name=args.controlnet_name,
    )
    cli_overrides.pop("image", None)  # the image comes from --image/--image-name
    try:
        result = generate(
            server=args.server,
            workflow=args.workflow,
            profile=args.profile,
            image=args.image,
            image_name=args.image_name,
            disable_nodes=disable,
            out_dir=args.out_dir,
            timeout=args.timeout,
            poll=args.poll,
            quiet=args.quiet,
            record=args.record,
            strict=not args.allow_unapplied,
            **cli_overrides,
        )
    except UnappliedOverrideError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["local_paths"] else 1


if __name__ == "__main__":
    sys.exit(main())
