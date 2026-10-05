#!/usr/bin/env python3
"""FastVideo FastH3 image-to-video (fl2va, video + synchronized audio) on ComfyUI.

First-frame driven companion to ``text-to-video-fastvideo3``: uploads a still,
sizes the canvas from that still, and generates the motion (plus audio) between
the optional keyframes with the same FastH3 8-Step V2 distilled checkpoint.

Canvas comes from the image, not from a resolution widget:

    LoadImage -> ImageScaleToTotalPixels(megapixels, resolution_steps)
              -> GetImageSize -> MiniMaxH3ImageToVideo.width/height

Usage:
  python3 scripts/comfyui_i2v.py --check
  python3 scripts/comfyui_i2v.py --list
  python3 scripts/comfyui_i2v.py --image ref.png --prompt-file shot.txt --duration 5 --plan
  python3 scripts/comfyui_i2v.py --image ref.png --prompt-file shot.txt --duration 5 --out-dir out/
  python3 scripts/comfyui_i2v.py --image first.png --last-frame last.png --prompt-file shot.txt --out-dir out/

Notes:
  * the prompt is REQUIRED: a run is expensive and the shipped demo prompt is not yours.
  * --last-frame is a script-level capability (it injects a LoadImage); the shipped
    workflow wires only the first frame.
  * no negative prompt: MiniMaxH3ImageToVideo takes a single prompt.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared  # noqa: E402

_shared.ensure()

from comfyui_convert import convert_ex, load_profile, resolve_params  # noqa: E402
from comfyui_gen import (  # noqa: E402
    DEFAULT_SERVER,
    _get_json,
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
DEFAULT_WORKFLOW = os.path.join(ASSETS, "video_fastvideo_fasth3_i2v.json")
DEFAULT_PROFILE = os.path.join(ASSETS, "video_fastvideo_fasth3_i2v.profile.json")

REQUIRED_MODELS = [
    ("diffusion_models", "fastvideo_fasth3_8step_v2_pruned_int8_convrot.safetensors"),
    ("text_encoders", "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors"),
    ("vae", "minimax_h3_video_vae_int8_convrot.safetensors"),
    ("vae", "minimax_h3_audio_vae_fp32.safetensors"),
]

REQUIRED_NODES = [
    "MiniMaxH3ImageToVideo",
    "MiniMaxH3SigmaShift",
    "BlockSparseAttention",
    "ModelAttentionBackend",
    "ImageScaleToTotalPixels",
    "GetImageSize",
    "LoadImage",
    "ComfyMathExpression",
    "CreateVideo",
    "SaveVideo",
    "VAEDecodeAudio",
]

H3_FPS = 24.0
FRAME_GRID = 17  # H3 emits 17k+5 frames


# --------------------------------------------------------------------------- helpers
def predicted_frames(duration: float, fps: float = H3_FPS) -> int:
    """Frame count the workflow's Math Expression snaps ``duration`` up to."""
    base = max(5, round(duration * fps))
    return base + (5 - base % FRAME_GRID) % FRAME_GRID


def _parse_value(raw: str):
    try:
        return json.loads(raw)
    except ValueError:
        return raw


def inject_sets(profile: dict, pairs: list[str] | None) -> tuple[dict, dict]:
    """Turn ``--set CLASS.FIELD=VALUE`` into profile entries + overrides."""
    prof = json.loads(json.dumps(profile or {}))
    overrides: dict = {}
    for item in pairs or []:
        if "=" not in item or "." not in item.split("=", 1)[0]:
            raise SystemExit(f"--set expects CLASS.FIELD=VALUE, got {item!r}")
        lhs, raw = item.split("=", 1)
        cls, field = lhs.split(".", 1)
        key = f"set_{cls}_{field}"
        prof.setdefault("parameters", {})[key] = {"node": cls, "field": field}
        overrides[key] = _parse_value(raw)
    return prof, overrides


def upload_image(server: str, path: str, timeout: float = 180.0) -> str:
    """POST a local file to /upload/image and return the widget value to use."""
    with open(path, "rb") as fh:
        data = fh.read()
    boundary = "----dsh" + uuid.uuid4().hex
    name = os.path.basename(path)
    parts = [
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="image"; filename="{name}"\r\n'.encode(),
        b"Content-Type: application/octet-stream\r\n\r\n",
        data,
        f"\r\n--{boundary}\r\n".encode(),
        b'Content-Disposition: form-data; name="overwrite"\r\n\r\n1',
        f"\r\n--{boundary}\r\n".encode(),
        b'Content-Disposition: form-data; name="type"\r\n\r\ninput',
        f"\r\n--{boundary}--\r\n".encode(),
    ]
    raw = _request(
        f"{server.rstrip('/')}/upload/image",
        data=b"".join(parts),
        method="POST",
        timeout=timeout,
        content_type=f"multipart/form-data; boundary={boundary}",
    )
    payload = json.loads(raw.decode("utf-8"))
    sub = payload.get("subfolder") or ""
    return f"{sub}/{payload['name']}" if sub else payload["name"]


def attach_last_frame(api: dict, image_name: str, target_class: str = "MiniMaxH3ImageToVideo") -> str:
    """Wire an uploaded image into a workflow input that ships unconnected.

    ``last_frame`` is an *optional node input*, not a subgraph interface parameter,
    so it cannot go through the profile (that would put a bare string where the
    API format requires a ``[node_id, slot]`` link).  Instead add a LoadImage and
    point the consumer at it.
    """
    targets = [nid for nid, node in api.items() if node.get("class_type") == target_class]
    if not targets:
        raise RuntimeError(f"no {target_class} node in the converted graph")
    numeric = [int(k) for k in api if str(k).isdigit()]
    new_id = str(max(numeric) + 1 if numeric else 1)
    api[new_id] = {"class_type": "LoadImage", "inputs": {"image": image_name}}
    api[targets[0]]["inputs"]["last_frame"] = [new_id, 0]
    return new_id


def build_overrides(
    prompt=None, duration=None, length=None, seed=None, steps=None, sampler=None,
    scheduler=None, denoise=None, megapixels=None, resolution_steps=None,
    scale_method=None, width=None, height=None, fps=None, shift_video=None,
    shift_audio=None, attention=None, sparse_selection=None, sparse_keep_percent=None,
    sparse_tau=None, sparse_start_percent=None, sparse_end_percent=None,
    sparse_min_tokens=None, sparse_extra_tokens=None, sparse_dense_blocks=None,
    sparse_sink=None, bit_depth=None, color_space=None, video_codec=None,
    video_format=None, filename_prefix=None, unet_name=None, clip_name=None,
    vae_name=None, audio_vae_name=None,
) -> dict:
    """Collect CLI values into the profile's parameter keys (None = keep default)."""
    return {
        "prompt": prompt,
        "duration": duration,
        "length": length,
        "seed": seed,
        "steps": steps,
        "sampler": sampler,
        "scheduler": scheduler,
        "denoise": denoise,
        "megapixels": megapixels,
        "resolution_steps": resolution_steps,
        "scale_method": scale_method,
        "width": width,
        "height": height,
        "fps": fps,
        "shift_video": shift_video,
        "shift_audio": shift_audio,
        "attention": attention,
        "sparse_selection": sparse_selection,
        "sparse_keep_percent": sparse_keep_percent,
        "sparse_tau": sparse_tau,
        "sparse_start_percent": sparse_start_percent,
        "sparse_end_percent": sparse_end_percent,
        "sparse_min_tokens": sparse_min_tokens,
        "sparse_extra_tokens": sparse_extra_tokens,
        "sparse_dense_blocks": sparse_dense_blocks,
        "sparse_sink": sparse_sink,
        "bit_depth": bit_depth,
        "color_space": color_space,
        "video_codec": video_codec,
        "video_format": video_format,
        "filename_prefix": filename_prefix,
        "unet_name": unet_name,
        "clip_name": clip_name,
        "vae_name": vae_name,
        "audio_vae_name": audio_vae_name,
    }


def build_graph(
    workflow: str,
    profile: str | dict,
    overrides: dict,
    image_name: str | None = None,
    last_frame_name: str | None = None,
    set_pairs=None,
):
    """Convert the UI workflow into (api_graph, output_node_id, warnings, profile, merged)."""
    prof = load_profile(profile) if isinstance(profile, str) else dict(profile or {})
    prof, extra = inject_sets(prof, set_pairs)
    merged = {k: v for k, v in {**overrides, **extra}.items() if v is not None}
    if image_name:
        merged["image"] = image_name
    ui = json.load(open(workflow, encoding="utf-8"))
    api, out_id, warnings = convert_ex(ui, merged, prof)
    if last_frame_name:
        attach_last_frame(api, last_frame_name)
    return api, out_id, warnings, prof, merged


def probe_media(path: str) -> dict | None:
    """Best-effort ffprobe summary of a produced video (None when unavailable)."""
    exe = shutil.which("ffprobe")
    if not exe:
        return None
    try:
        out = subprocess.run(
            [exe, "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height,r_frame_rate",
             "-show_entries", "format=duration,size", "-of", "json", path],
            capture_output=True, text=True, timeout=30,
        )
        if out.returncode != 0:
            return None
        data = json.loads(out.stdout)
        stream = (data.get("streams") or [{}])[0]
        fmt = data.get("format") or {}
        return {
            "width": stream.get("width"),
            "height": stream.get("height"),
            "r_frame_rate": stream.get("r_frame_rate"),
            "duration": float(fmt["duration"]) if fmt.get("duration") else None,
            "bytes": int(fmt["size"]) if fmt.get("size") else None,
        }
    except Exception:  # noqa: BLE001 - purely informational
        return None


# --------------------------------------------------------------------------- server
def check_server(server: str) -> dict:
    """Verify every required model file and node class exists on the server."""
    missing_models: list[str] = []
    for folder, name in REQUIRED_MODELS:
        try:
            files = list_models(server, folder)
        except Exception as exc:  # noqa: BLE001
            missing_models.append(f"{folder}: cannot list ({exc})")
            continue
        if name not in files:
            missing_models.append(f"{folder}/{name}")
    missing_nodes: list[str] = []
    for cls in REQUIRED_NODES:
        try:
            if cls not in _get_json(f"{server.rstrip('/')}/object_info/{cls}", timeout=10):
                missing_nodes.append(cls)
        except Exception:  # noqa: BLE001
            missing_nodes.append(f"{cls} (probe failed)")
    return {
        "ok": not missing_models and not missing_nodes,
        "missing_models": missing_models,
        "missing_nodes": missing_nodes,
        "hint": (
            "video nodes are newer than the image ones -- update ComfyUI if a node is missing"
            if missing_nodes else None
        ),
    }


# --------------------------------------------------------------------------- engine
def generate(
    server: str = DEFAULT_SERVER,
    workflow: str = DEFAULT_WORKFLOW,
    profile: str | dict = DEFAULT_PROFILE,
    image: str | None = None,
    image_name: str | None = None,
    last_frame: str | None = None,
    last_frame_name: str | None = None,
    set_pairs: list[str] | None = None,
    out_dir: str = "out",
    timeout: float = 3600.0,
    poll: float = 10.0,
    quiet: bool = False,
    record: bool = True,
    **params,
) -> dict:
    """Run one image-to-video generation and download the produced media."""
    if image and not image_name:
        image_name = upload_image(server, image)
        if not quiet:
            print(f"   uploaded first frame: {image_name}", flush=True)
    if last_frame and not last_frame_name:
        last_frame_name = upload_image(server, last_frame)
        if not quiet:
            print(f"   uploaded last frame: {last_frame_name}", flush=True)
    if not image_name:
        raise ValueError("no input image: pass image=<local path> or image_name=<server file>")

    overrides = build_overrides(**params)
    api_prompt, out_id, warnings, _prof, merged = build_graph(
        workflow, profile, overrides, image_name=image_name,
        last_frame_name=last_frame_name, set_pairs=set_pairs,
    )
    if warnings and not quiet:
        for warning in warnings:
            print(f"   warning: {warning}", file=sys.stderr)
    if out_id is None:
        raise RuntimeError("workflow has no SaveVideo/SaveImage node; cannot locate outputs")

    raw_prefix = str(params.get("filename_prefix") or "fastvideo-fasth3-i2v")
    prefix = os.path.basename(raw_prefix.rstrip("/")) or "fastvideo-fasth3-i2v"
    duration = params.get("duration")
    if duration and not params.get("length"):
        frames = predicted_frames(float(duration), float(params.get("fps") or H3_FPS))
        if not quiet:
            print(f"   duration {duration}s -> length {frames} frames "
                  f"({frames / (params.get('fps') or H3_FPS):.3f}s, {FRAME_GRID}k+5 grid)")
    if not quiet:
        print(f"-> fastvideo-fasth3 i2v @ {server}  image={image_name} "
              f"last_frame={last_frame_name}  seed={merged.get('seed')} "
              f"steps={merged.get('steps')} mp={merged.get('megapixels')}", flush=True)

    started = time.time()
    prompt_id = queue_prompt(server, api_prompt, f"dsh-i2v-{os.getpid()}", timeout=120.0)
    if not quiet:
        print(f"   queued: {prompt_id}", flush=True)
    entry = wait_for_history(server, prompt_id, timeout=timeout, poll=poll, quiet=quiet)
    outputs = collect_images(entry, only_node=out_id)
    paths = [download_image(server, item, out_dir) for item in outputs if item.get("filename")]
    elapsed = time.time() - started
    media = probe_media(paths[0]) if paths else None
    if not quiet:
        for path in paths:
            print(f"   saved: {path} ({os.path.getsize(path)} bytes)", flush=True)
        print(f"   elapsed: {elapsed:.1f}s" + (f"  media: {media}" if media else ""), flush=True)

    if record:
        record_request(
            out_dir=out_dir,
            prefix=prefix,
            engine="fastvideo-fasth3-i2v",
            server=server,
            params={
                "prompt": params.get("prompt"),
                "negative": None,
                "input_image": image_name,
                "input_image_local": image,
                "last_frame_image": last_frame_name,
                "last_frame_local": last_frame,
                "workflow": os.path.basename(workflow),
                "profile": os.path.basename(profile) if isinstance(profile, str) else None,
                "elapsed_s": round(elapsed, 1),
                "media": media,
                **{k: v for k, v in merged.items() if k not in ("prompt", "image")},
            },
            prompt_id=prompt_id,
            graph=api_prompt,
            files=paths,
        )
    return {
        "prompt_id": prompt_id,
        "outputs": outputs,
        "images": outputs,
        "local_paths": paths,
        "media": media,
        "elapsed_s": round(elapsed, 1),
        "status": (entry.get("status") or {}).get("status_str"),
        "warnings": warnings,
        "output_node": out_id,
        "input_image": image_name,
        "last_frame_image": last_frame_name,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=DEFAULT_SERVER)
    ap.add_argument("--workflow", default=DEFAULT_WORKFLOW)
    ap.add_argument("--profile", default=DEFAULT_PROFILE)

    g = ap.add_mutually_exclusive_group()
    g.add_argument("--image", help="local first-frame image to upload")
    g.add_argument("--image-name", help="first frame already in the server's input/ dir")
    g2 = ap.add_mutually_exclusive_group()
    g2.add_argument("--last-frame", help="optional local last-frame image to upload")
    g2.add_argument("--last-frame-name", help="optional last frame already on the server")

    src = ap.add_mutually_exclusive_group()
    src.add_argument("--prompt", help="the prompt string (long: prefer --prompt-file)")
    src.add_argument("--prompt-file", help="read the prompt from a UTF-8 file")

    ap.add_argument("--duration", "--seconds", dest="duration", type=float,
                    help="clip length in seconds (snapped up to the 17k+5 frame grid)")
    ap.add_argument("--length", type=int, help="force frame count directly (cuts the duration math)")
    ap.add_argument("--megapixels", type=float,
                    help="scale the input image to this many megapixels to decide the canvas")
    ap.add_argument("--resolution-steps", type=int, help="canvas rounding step (workflow default 32)")
    ap.add_argument("--scale-method", help="resample filter used for the size estimate")
    ap.add_argument("--width", type=int, help="force canvas width (cuts the GetImageSize link)")
    ap.add_argument("--height", type=int, help="force canvas height (cuts the GetImageSize link)")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--steps", type=int, help="the distilled checkpoint is trained for 8")
    ap.add_argument("--sampler")
    ap.add_argument("--scheduler")
    ap.add_argument("--denoise", type=float)
    ap.add_argument("--fps", type=float)
    ap.add_argument("--shift-video", type=float)
    ap.add_argument("--shift-audio", type=float)
    ap.add_argument("--attention", help='"comfy kitchen attention" or "pytorch attention"')
    ap.add_argument("--sparse-selection", help="vsa (default) / sla / sol-attn")
    ap.add_argument("--sparse-keep-percent", type=float)
    ap.add_argument("--sparse-tau", type=float, help="only for selection=sol-attn")
    ap.add_argument("--sparse-start", dest="sparse_start_percent", type=float)
    ap.add_argument("--sparse-end", dest="sparse_end_percent", type=float)
    ap.add_argument("--sparse-min-tokens", type=int)
    ap.add_argument("--sparse-extra-tokens", type=int)
    ap.add_argument("--sparse-dense-blocks")
    ap.add_argument("--sparse-sink", help="exact_kv / exact_kv_and_rows / off")
    ap.add_argument("--bit-depth")
    ap.add_argument("--color-space")
    ap.add_argument("--video-codec", help="CreateVideo codec: none / auto / h264 / av1")
    ap.add_argument("--video-format", help="container written by SaveVideo: auto / mp4 / mkv / webm")
    ap.add_argument("--filename-prefix", help='SaveVideo prefix (default video/MiniMax_H3)')
    ap.add_argument("--unet-name")
    ap.add_argument("--clip-name")
    ap.add_argument("--vae-name", dest="vae_name", help="video VAE")
    ap.add_argument("--audio-vae-name")
    ap.add_argument("--set", dest="set_pairs", action="append", default=[], metavar="CLASS.FIELD=VALUE",
                    help="set any node field the profile does not name (repeatable)")
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--timeout", type=float, default=3600.0)
    ap.add_argument("--poll", type=float, default=10.0)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-record", dest="record", action="store_false")
    ap.add_argument("--check", action="store_true", help="verify required models and nodes on the server")
    ap.add_argument("--list", action="store_true", help="print the workflow's parameters and defaults")
    ap.add_argument("--plan", action="store_true", help="build and print the API graph without submitting")
    ap.add_argument("--show-default-prompt", action="store_true",
                    help="print the long prompt the workflow ships with (a real fl2va specimen)")
    args = ap.parse_args(argv)

    if args.check:
        result = check_server(args.server)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 2
    if args.list:
        ui = json.load(open(args.workflow, encoding="utf-8"))
        prof = load_profile(args.profile)
        print(json.dumps(
            {"interface_defaults": resolve_params(ui),
             "profile_parameters": sorted(prof.get("parameters", {})),
             "defaults": prof.get("defaults", {}),
             "expected_unconnected": prof.get("expected_unconnected", [])},
            ensure_ascii=False, indent=2))
        return 0
    if args.show_default_prompt:
        ui = json.load(open(args.workflow, encoding="utf-8"))
        for node in ui.get("nodes", []):
            named = node.get("widgets_values_named") or {}
            if named.get("prompt"):
                print(named["prompt"])
                return 0
        print("no default prompt found in the workflow", file=sys.stderr)
        return 1

    prompt = args.prompt
    if args.prompt_file:
        with open(args.prompt_file, encoding="utf-8") as fh:
            prompt = fh.read().strip()
    if not prompt:
        ap.error("--prompt or --prompt-file is required (a run is expensive; there is no default)")
    if not (args.image or args.image_name) and not args.plan:
        ap.error("--image or --image-name is required")

    overrides = build_overrides(
        prompt=prompt, duration=args.duration, length=args.length, seed=args.seed,
        steps=args.steps, sampler=args.sampler, scheduler=args.scheduler,
        denoise=args.denoise, megapixels=args.megapixels,
        resolution_steps=args.resolution_steps, scale_method=args.scale_method,
        width=args.width, height=args.height, fps=args.fps,
        shift_video=args.shift_video, shift_audio=args.shift_audio, attention=args.attention,
        sparse_selection=args.sparse_selection, sparse_keep_percent=args.sparse_keep_percent,
        sparse_tau=args.sparse_tau, sparse_start_percent=args.sparse_start_percent,
        sparse_end_percent=args.sparse_end_percent, sparse_min_tokens=args.sparse_min_tokens,
        sparse_extra_tokens=args.sparse_extra_tokens, sparse_dense_blocks=args.sparse_dense_blocks,
        sparse_sink=args.sparse_sink, bit_depth=args.bit_depth, color_space=args.color_space,
        video_codec=args.video_codec, video_format=args.video_format,
        filename_prefix=args.filename_prefix, unet_name=args.unet_name,
        clip_name=args.clip_name, vae_name=args.vae_name, audio_vae_name=args.audio_vae_name,
    )

    if args.plan:
        api_prompt, out_id, warnings, prof, merged = build_graph(
            args.workflow, args.profile, overrides,
            image_name=args.image_name or (os.path.basename(args.image) if args.image else "<uploaded>"),
            last_frame_name=args.last_frame_name or (os.path.basename(args.last_frame) if args.last_frame else None),
            set_pairs=args.set_pairs,
        )
        frames = None
        if args.duration and not args.length:
            frames = predicted_frames(args.duration, args.fps or H3_FPS)
        print(json.dumps({
            "output_node": out_id,
            "nodes": len(api_prompt),
            "warnings": warnings,
            "overrides_entering_graph": {k: v for k, v in merged.items() if k != "prompt"},
            "predicted_length_frames": frames,
            "predicted_seconds": (frames / (args.fps or H3_FPS)) if frames else None,
            "graph": api_prompt,
        }, ensure_ascii=False, indent=2))
        return 0

    result = generate(
        server=args.server, workflow=args.workflow, profile=args.profile,
        image=args.image, image_name=args.image_name,
        last_frame=args.last_frame, last_frame_name=args.last_frame_name,
        set_pairs=args.set_pairs, out_dir=args.out_dir, timeout=args.timeout,
        poll=args.poll, quiet=args.quiet, record=args.record, **overrides,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["local_paths"] else 1


if __name__ == "__main__":
    sys.exit(main())
