#!/usr/bin/env python3
"""FastVideo FastH3 text-to-video (video + synchronized audio) on ComfyUI.

Runs the ComfyUI "Fast Video FastH3" template over the HTTP API: a MiniMax-H3
graph with the FastVideo FastH3 8-Step V2 DMD2-distilled checkpoint, so a
5-second 24fps clip with audio lands in 8 sampling steps.

Pipeline: convert the UI workflow to API format (shared converter) -> POST
/prompt -> poll /history -> GET /view to pull the .mp4 down.

Usage:
  # 1) is the server able to run this at all? (models + nodes)
  python3 comfyui_video.py --check

  # 2) what parameters does the workflow expose, and what are the defaults?
  python3 comfyui_video.py --list

  # 3) build the exact graph without submitting (free, no GPU) -- always do this first
  python3 comfyui_video.py --prompt-file shot.txt --duration 5 --plan

  # 4) generate (slow: 35 GB of weights on an 8 GB card)
  python3 comfyui_video.py --prompt-file shot.txt --duration 5 --aspect-ratio "16:9 (Widescreen)" \
      --megapixels 0.4 --seed 42 --out-dir out/

  # escape hatch for any node field the profile does not name
  python3 comfyui_video.py --prompt-file shot.txt --set "BlockSparseAttention.tau=1.3"

Notes:
  * prompt is REQUIRED on purpose: this workflow ships with a long demo prompt and
    a run is expensive, so there is no accidental "generate the template" default.
  * t2va only -- the distilled checkpoint was not trained for first/last-frame or
    multi-reference conditioning (the node's image inputs stay unconnected).
  * there is no negative prompt: MiniMaxH3ImageToVideo takes a single prompt.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared  # noqa: E402

_shared.ensure()

from comfyui_convert import convert_ex, load_profile, resolve_params  # noqa: E402
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

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))
DEFAULT_WORKFLOW = os.path.join(ASSETS, "video_fastvideo_fasth3_t2v.json")
DEFAULT_PROFILE = os.path.join(ASSETS, "video_fastvideo_fasth3_t2v.profile.json")

# The distilled checkpoint and its two VAEs, exactly as the template ships.
REQUIRED_MODELS = [
    ("diffusion_models", "fastvideo_fasth3_8step_v2_pruned_int8_convrot.safetensors"),
    ("text_encoders", "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors"),
    ("vae", "minimax_h3_video_vae_int8_convrot.safetensors"),
    ("vae", "minimax_h3_audio_vae_fp32.safetensors"),
]

# Nodes the graph cannot run without; video support needs a recent ComfyUI.
REQUIRED_NODES = [
    "MiniMaxH3ImageToVideo",
    "MiniMaxH3SigmaShift",
    "BlockSparseAttention",
    "ModelAttentionBackend",
    "ResolutionSelector",
    "ComfyMathExpression",
    "CreateVideo",
    "SaveVideo",
    "VAEDecodeAudio",
]

H3_FPS = 24.0
FRAME_GRID = 17  # H3 emits 17k+5 frames


# --------------------------------------------------------------------------- helpers
def predicted_frames(duration: float, fps: float = H3_FPS) -> int:
    """Frame count the workflow's Math Expression snaps ``duration`` up to.

    Mirrors ``max(5, round(a*fps)) + (5 - (max(5, round(a*fps)) % 17)) % 17``:
    5 s -> 124 frames -> 5.167 s, not 5.000 s.
    """
    base = max(5, round(duration * fps))
    return base + (5 - base % FRAME_GRID) % FRAME_GRID


def _parse_value(raw: str):
    """JSON-ish scalar parsing for --set values (falls back to the raw string)."""
    try:
        return json.loads(raw)
    except ValueError:
        return raw


def inject_sets(profile: dict, pairs: list[str] | None) -> tuple[dict, dict]:
    """Turn ``--set CLASS.FIELD=VALUE`` into profile entries + overrides.

    Reuses the profile machinery instead of a second code path, so an escape-hatch
    parameter behaves exactly like a declared one.
    """
    prof = json.loads(json.dumps(profile or {}))
    overrides: dict = {}
    for item in pairs or []:
        if "=" not in item:
            raise SystemExit(f"--set expects CLASS.FIELD=VALUE, got {item!r}")
        lhs, raw = item.split("=", 1)
        if "." not in lhs:
            raise SystemExit(f"--set expects CLASS.FIELD=VALUE, got {item!r}")
        cls, field = lhs.split(".", 1)
        key = f"set_{cls}_{field}"
        prof.setdefault("parameters", {})[key] = {"node": cls, "field": field}
        overrides[key] = _parse_value(raw)
    return prof, overrides


def build_overrides(
    prompt=None, duration=None, length=None, seed=None, steps=None,
    sampler=None, scheduler=None, denoise=None, aspect_ratio=None,
    megapixels=None, multiple=None, width=None, height=None, fps=None,
    shift_video=None, shift_audio=None, attention=None, sparse_selection=None,
    sparse_keep_percent=None, sparse_tau=None, sparse_start_percent=None,
    sparse_end_percent=None, sparse_min_tokens=None, sparse_extra_tokens=None,
    sparse_dense_blocks=None, sparse_sink=None, bit_depth=None, color_space=None,
    video_codec=None, video_format=None, filename_prefix=None, unet_name=None,
    clip_name=None, vae_name=None, audio_vae_name=None,
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
        "aspect_ratio": aspect_ratio,
        "megapixels": megapixels,
        "multiple": multiple,
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


def build_graph(workflow: str, profile: str | dict, overrides: dict, set_pairs=None):
    """Convert the UI workflow into (api_graph, output_node_id, warnings)."""
    prof = load_profile(profile) if isinstance(profile, str) else dict(profile or {})
    prof, extra = inject_sets(prof, set_pairs)
    merged = {k: v for k, v in {**overrides, **extra}.items() if v is not None}
    ui = json.load(open(workflow, encoding="utf-8"))
    return (*convert_ex(ui, merged, prof), prof, merged)


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
    set_pairs: list[str] | None = None,
    out_dir: str = "out",
    timeout: float = 3600.0,
    poll: float = 10.0,
    quiet: bool = False,
    record: bool = True,
    **params,
) -> dict:
    """Run one text-to-video generation and download the produced media."""
    overrides = build_overrides(**params)
    api_prompt, out_id, warnings, _prof, merged = build_graph(
        workflow, profile, overrides, set_pairs
    )
    if warnings and not quiet:
        for warning in warnings:
            print(f"   warning: {warning}", file=sys.stderr)
    if out_id is None:
        raise RuntimeError("workflow has no SaveVideo/SaveImage node; cannot locate outputs")

    # filename_prefix may carry a server-side subdirectory ("video/MiniMax_H3").
    # Keep it for the server, but archive locally under the bare basename --
    # otherwise "<prefix>.api.json" would need a directory that does not exist.
    raw_prefix = str(params.get("filename_prefix") or "fastvideo-fasth3")
    prefix = os.path.basename(raw_prefix.rstrip("/")) or "fastvideo-fasth3"
    duration = params.get("duration")
    if duration and not params.get("length"):
        frames = predicted_frames(float(duration), float(params.get("fps") or H3_FPS))
        if not quiet:
            print(f"   duration {duration}s -> length {frames} frames "
                  f"({frames / (params.get('fps') or H3_FPS):.3f}s, {FRAME_GRID}k+5 grid)")
    if not quiet:
        print(f"-> fastvideo-fasth3 t2v @ {server}  seed={merged.get('seed')} "
              f"steps={merged.get('steps')} ratio={merged.get('aspect_ratio')} "
              f"mp={merged.get('megapixels')}", flush=True)

    started = time.time()
    prompt_id = queue_prompt(server, api_prompt, f"dsh-video-{os.getpid()}", timeout=120.0)
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
            engine="fastvideo-fasth3-t2v",
            server=server,
            params={
                "prompt": params.get("prompt"),
                "negative": None,
                "workflow": os.path.basename(workflow),
                "profile": os.path.basename(profile) if isinstance(profile, str) else None,
                "elapsed_s": round(elapsed, 1),
                "media": media,
                **{k: v for k, v in merged.items() if k != "prompt"},
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
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=DEFAULT_SERVER)
    ap.add_argument("--workflow", default=DEFAULT_WORKFLOW)
    ap.add_argument("--profile", default=DEFAULT_PROFILE)

    src = ap.add_mutually_exclusive_group()
    src.add_argument("--prompt", help="the prompt string (long: prefer --prompt-file)")
    src.add_argument("--prompt-file", help="read the prompt from a UTF-8 file")

    ap.add_argument("--duration", "--seconds", dest="duration", type=float,
                    help="clip length in seconds (snapped up to the 17k+5 frame grid)")
    ap.add_argument("--length", type=int, help="force frame count directly (cuts the duration math)")
    ap.add_argument("--aspect-ratio", help='e.g. "1:1 (Square)", "16:9 (Widescreen)"')
    ap.add_argument("--megapixels", type=float, help="ResolutionSelector target megapixels")
    ap.add_argument("--multiple", type=int, help="round the canvas to a multiple of N (default 32)")
    ap.add_argument("--width", type=int, help="force canvas width (cuts the ResolutionSelector link)")
    ap.add_argument("--height", type=int, help="force canvas height (cuts the ResolutionSelector link)")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--steps", type=int, help="the distilled checkpoint is trained for 8")
    ap.add_argument("--sampler")
    ap.add_argument("--scheduler")
    ap.add_argument("--denoise", type=float)
    ap.add_argument("--fps", type=float, help="container fps (the duration math assumes 24)")
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
    ap.add_argument("--timeout", type=float, default=3600.0, help="seconds to wait for the job")
    ap.add_argument("--poll", type=float, default=10.0)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-record", dest="record", action="store_false")
    ap.add_argument("--check", action="store_true", help="verify required models and nodes on the server")
    ap.add_argument("--list", action="store_true", help="print the workflow's parameters and defaults")
    ap.add_argument("--plan", action="store_true", help="build and print the API graph without submitting")
    ap.add_argument("--show-default-prompt", action="store_true",
                    help="print the long prompt the workflow ships with (a real t2va specimen)")
    args = ap.parse_args(argv)

    if args.show_default_prompt:
        ui = json.load(open(args.workflow, encoding="utf-8"))
        for node in ui.get("nodes", []):
            named = node.get("widgets_values_named") or {}
            if named.get("prompt"):
                print(named["prompt"])
                return 0
        print("no default prompt found in the workflow", file=sys.stderr)
        return 1

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

    prompt = args.prompt
    if args.prompt_file:
        with open(args.prompt_file, encoding="utf-8") as fh:
            prompt = fh.read().strip()
    if not prompt:
        ap.error("--prompt or --prompt-file is required (a run is expensive; there is no default)")

    overrides = build_overrides(
        prompt=prompt, duration=args.duration, length=args.length, seed=args.seed,
        steps=args.steps, sampler=args.sampler, scheduler=args.scheduler,
        denoise=args.denoise, aspect_ratio=args.aspect_ratio, megapixels=args.megapixels,
        multiple=args.multiple, width=args.width, height=args.height, fps=args.fps,
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
            args.workflow, args.profile, overrides, args.set_pairs
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
        set_pairs=args.set_pairs, out_dir=args.out_dir, timeout=args.timeout,
        poll=args.poll, quiet=args.quiet, record=args.record, **overrides,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["local_paths"] else 1


if __name__ == "__main__":
    sys.exit(main())
