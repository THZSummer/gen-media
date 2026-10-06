#!/usr/bin/env python3
"""MiniMax Music 3 text-to-music on ComfyUI (caption + lyrics -> audio).

Runs the ComfyUI "Text to Music (MiniMax Music 3)" subgraph template over the
HTTP API: convert the UI workflow to API format (shared converter, which also
flattens ``definitions.subgraphs``) -> POST /prompt -> poll /history -> GET /view
to pull the .mp3 down.

Usage:
  # 1) is the server able to run this at all? (models + nodes)
  python3 comfyui_music.py --check

  # 2) what parameters does the workflow expose, and what are the defaults?
  python3 comfyui_music.py --list

  # 3) build the exact graph without submitting (free, no GPU) -- always do this first
  python3 comfyui_music.py --caption-file bgm.txt --instrumental --duration 20 --plan

  # 4) generate (SLOW -- see the cost note below)
  python3 comfyui_music.py --caption-file bgm.txt --instrumental --duration 20 \
      --seed 42 --filename-prefix audio/jwh-bgm --out-dir out/

  # escape hatch for any node field the profile does not name
  python3 comfyui_music.py --caption "..." --set KSampler.denoise=0.9

COST (measured on the 192.168.3.5 box, RTX 4060 Ti 8 GB, fp16 DiT + 30 steps):
  **60 s of audio took ~1000 s of wall time** (~16.7 s per audio second).
  A 20 s BGM loop therefore costs ~5-6 minutes; 120 s costs ~35 minutes.
  ``--eta`` (on by default) prints the estimate before queueing. Ask for the
  shortest duration that still loops for your edit.

Notes:
  * caption is REQUIRED on purpose: a run is expensive, so there is no
    accidental "generate the template demo song" default.
  * duration is a single knob: it is set on MiniMaxMusic3TextEncode.max_duration
    and flows to EmptyMiniMaxMusic3LatentAudio.seconds through the template's
    FLOAT link, so both stay in sync (no second place to set it).
  * ``--instrumental`` only rewrites the *lyrics* field to a minimal tag script;
    whether the model returns vocals anyway is a model behaviour, not a
    guarantee -- verify by ear before shipping.
  * the tiled VAE decode switch (``--tiled``) trades a little quality and speed
    for a lot of VRAM; the template ships with it ON.
  * model licence: the weights are open-weight under the MiniMax-Music3
    community licence -- read it before any commercial use.
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
    download_image,
    list_models,
    queue_prompt,
    record_request,
    wait_for_history,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))
DEFAULT_WORKFLOW = os.path.join(ASSETS, "audio_minimax_music_3.json")
DEFAULT_PROFILE = os.path.join(ASSETS, "audio_minimax_music_3.profile.json")

# The three weights the template ships with (fp16 DiT; an int8 variant exists).
REQUIRED_MODELS = [
    ("diffusion_models", "minimax_music3_dit_fp16.safetensors"),
    ("text_encoders", "minimax_music3_text_encoder_pruned_int8_convrot.safetensors"),
    ("vae", "minimax_music3_dav.safetensors"),
]

# Nodes the graph cannot run without; the subgraph ones are MiniMax-Music3 specific.
REQUIRED_NODES = [
    "MiniMaxMusic3TextEncode",
    "EmptyMiniMaxMusic3LatentAudio",
    "VAEDecodeAudio",
    "VAEDecodeAudioTiled",
    "ComfySwitchNode",
    "SeedNode",
    "SaveAudioAdvanced",
]

# Wall-clock cost per audio second, measured on the reference box (see module docstring).
SECONDS_PER_AUDIO_SECOND = 16.7

# Media keys a Save*/Preview node may put its file descriptors under.
MEDIA_KEYS = ("audio", "images", "gifs", "videos", "files")

INSTRUMENTAL_LYRICS = "[intro]\n[instrumental]\n[outro]"


# --------------------------------------------------------------------------- helpers
def estimate_wall(duration: float | None) -> float | None:
    """Rough wall-clock estimate in seconds for ``duration`` seconds of audio."""
    if not duration:
        return None
    return round(float(duration) * SECONDS_PER_AUDIO_SECOND, 1)


def _parse_value(raw: str):
    """JSON-ish scalar parsing for --set values (falls back to the raw string)."""
    try:
        return json.loads(raw)
    except ValueError:
        return raw


def inject_sets(profile: dict, pairs: list[str] | None) -> tuple[dict, dict]:
    """Turn ``--set CLASS.FIELD=VALUE`` into profile entries + overrides."""
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
    caption=None, lyrics=None, duration=None, seed=None, steps=None,
    cfg_scale=None, top_k=None, sampler_cfg=None, sampler=None, scheduler=None,
    denoise=None, tiled_decode=None, tile_size=None, overlap=None,
    filename_prefix=None, unet_name=None, clip_name=None, vae_name=None,
) -> dict:
    """Collect CLI values into the profile's parameter keys (None = keep default).

    ``cfg_scale`` (text encoder guidance) and ``sampler_cfg`` (KSampler cfg) are
    separate fields in the graph but are meant to move together, so an explicit
    ``cfg_scale`` without ``sampler_cfg`` also pins the sampler.
    """
    if cfg_scale is not None and sampler_cfg is None:
        sampler_cfg = cfg_scale
    return {
        "caption": caption,
        "lyrics": lyrics,
        "duration": duration,
        "seed": seed,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "top_k": top_k,
        "sampler_cfg": sampler_cfg,
        "sampler": sampler,
        "scheduler": scheduler,
        "denoise": denoise,
        "tiled_decode": tiled_decode,
        "tile_size": tile_size,
        "overlap": overlap,
        "filename_prefix": filename_prefix,
        "unet_name": unet_name,
        "clip_name": clip_name,
        "vae_name": vae_name,
    }


def build_graph(workflow: str = DEFAULT_WORKFLOW, profile: str | dict = DEFAULT_PROFILE,
                overrides: dict | None = None, set_pairs=None, report: dict | None = None):
    """Convert the UI workflow into (api_graph, output_node_id, warnings, profile, merged)."""
    prof = load_profile(profile) if isinstance(profile, str) else dict(profile or {})
    prof, extra = inject_sets(prof, set_pairs)
    merged = {k: v for k, v in {**(overrides or {}), **extra}.items() if v is not None}
    ui = json.load(open(workflow, encoding="utf-8"))
    api, out_id, warnings = convert_ex(ui, merged, prof, report=report)
    return api, out_id, warnings, prof, merged


def collect_media(history_entry: dict, only_node: str | None = None) -> list[dict]:
    """Flatten a history entry's outputs into downloadable descriptors.

    Unlike the image helper this also looks at the ``audio`` key written by
    SaveAudioAdvanced (and the other media keys, so a swapped save node still works).
    """
    found: list[dict] = []
    for node_id, node_out in (history_entry.get("outputs") or {}).items():
        if only_node is not None and str(node_id) != str(only_node):
            continue
        for key in MEDIA_KEYS:
            for item in node_out.get(key) or []:
                if isinstance(item, dict) and item.get("filename"):
                    found.append({
                        "node_id": str(node_id),
                        "kind": key,
                        "filename": item.get("filename"),
                        "subfolder": item.get("subfolder", ""),
                        "type": item.get("type", "output"),
                    })
    return found


def probe_audio(path: str) -> dict | None:
    """Best-effort ffprobe summary of a produced audio file (None when unavailable)."""
    exe = shutil.which("ffprobe")
    if not exe:
        return None
    try:
        out = subprocess.run(
            [exe, "-v", "error", "-show_entries",
             "stream=codec_name,sample_rate,channels,bit_rate",
             "-show_entries", "format=duration,size,bit_rate", "-of", "json", path],
            capture_output=True, text=True, timeout=60,
        )
        if out.returncode != 0:
            return None
        data = json.loads(out.stdout)
        stream = (data.get("streams") or [{}])[0]
        fmt = data.get("format") or {}
        return {
            "codec": stream.get("codec_name"),
            "sample_rate": int(stream["sample_rate"]) if stream.get("sample_rate") else None,
            "channels": stream.get("channels"),
            "duration": float(fmt["duration"]) if fmt.get("duration") else None,
            "bytes": int(fmt["size"]) if fmt.get("size") else None,
            "bit_rate": int(fmt["bit_rate"]) if fmt.get("bit_rate") else None,
        }
    except Exception:  # noqa: BLE001 - purely informational
        return None


def workflow_model_names(workflow: str = DEFAULT_WORKFLOW) -> dict:
    """Model filenames the workflow hard-codes, keyed by loader class.

    Loaders live *inside* the subgraph in these templates, so both the top level
    and every ``definitions.subgraphs[*].nodes`` list is walked.
    """
    ui = json.load(open(workflow, encoding="utf-8"))
    nodes = list(ui.get("nodes", []))
    for sub in (ui.get("definitions") or {}).get("subgraphs", []) or []:
        nodes.extend(sub.get("nodes", []) or [])
    out: dict[str, str] = {}
    for node in nodes:
        cls = node.get("type")
        if cls in ("UNETLoader", "CLIPLoader", "VAELoader"):
            widgets = node.get("widgets_values") or []
            if widgets:
                out[cls] = widgets[0]
    return out


def workflow_clip_type(workflow: str = DEFAULT_WORKFLOW) -> str | None:
    """The CLIPLoader ``type`` widget (``minimax`` for this model) if present."""
    ui = json.load(open(workflow, encoding="utf-8"))
    nodes = list(ui.get("nodes", []))
    for sub in (ui.get("definitions") or {}).get("subgraphs", []) or []:
        nodes.extend(sub.get("nodes", []) or [])
    for node in nodes:
        if node.get("type") == "CLIPLoader":
            widgets = node.get("widgets_values") or []
            if len(widgets) > 1:
                return widgets[1]
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
            "the MiniMax-Music3 nodes ship with recent ComfyUI (frontend 1.53+/0.38+);"
            " update ComfyUI if a node is missing"
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
    timeout: float = 7200.0,
    poll: float = 10.0,
    quiet: bool = False,
    record: bool = True,
    **params,
) -> dict:
    """Run one text-to-music generation and download the produced audio."""
    overrides = build_overrides(**params)
    report: dict = {}
    api_prompt, out_id, warnings, _prof, merged = build_graph(
        workflow, profile, overrides, set_pairs, report=report
    )
    if warnings and not quiet:
        for warning in warnings:
            print(f"   warning: {warning}", file=sys.stderr)
    if out_id is None:
        raise RuntimeError("workflow has no SaveAudio node; cannot locate outputs")

    raw_prefix = str(params.get("filename_prefix") or "minimax-music3")
    prefix = os.path.basename(raw_prefix.rstrip("/")) or "minimax-music3"
    duration = params.get("duration")
    eta = estimate_wall(duration)
    if not quiet:
        print(f"-> minimax-music3 @ {server}  duration={duration}s seed={merged.get('seed')} "
              f"steps={merged.get('steps')} tiled={merged.get('tiled_decode')}", flush=True)
        if eta:
            print(f"   ETA ~{eta:.0f}s (measured {SECONDS_PER_AUDIO_SECOND} s wall per audio s)", flush=True)

    started = time.time()
    prompt_id = queue_prompt(server, api_prompt, f"dsh-music-{os.getpid()}", timeout=120.0)
    if not quiet:
        print(f"   queued: {prompt_id}", flush=True)
    entry = wait_for_history(server, prompt_id, timeout=timeout, poll=poll, quiet=quiet)
    media_items = collect_media(entry, only_node=out_id)
    paths = [download_image(server, item, out_dir) for item in media_items]
    elapsed = time.time() - started
    audio = probe_audio(paths[0]) if paths else None
    if not quiet:
        for path in paths:
            print(f"   saved: {path} ({os.path.getsize(path)} bytes)", flush=True)
        print(f"   elapsed: {elapsed:.1f}s" + (f"  audio: {audio}" if audio else ""), flush=True)

    if record:
        record_request(
            out_dir=out_dir,
            prefix=prefix,
            engine="minimax-music3-t2m",
            server=server,
            params={
                "caption": params.get("caption"),
                "lyrics": params.get("lyrics"),
                "workflow": os.path.basename(workflow),
                "profile": os.path.basename(profile) if isinstance(profile, str) else None,
                "elapsed_s": round(elapsed, 1),
                "eta_s": eta,
                "audio": audio,
                **{k: v for k, v in merged.items() if k not in ("caption", "lyrics")},
            },
            prompt_id=prompt_id,
            graph=api_prompt,
            files=paths,
        )
    return {
        "prompt_id": prompt_id,
        "outputs": media_items,
        "local_paths": paths,
        "audio": audio,
        "elapsed_s": round(elapsed, 1),
        "eta_s": eta,
        "status": (entry.get("status") or {}).get("status_str"),
        "warnings": warnings,
        "unapplied_overrides": report.get("unapplied") or {},
        "output_node": out_id,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=DEFAULT_SERVER)
    ap.add_argument("--workflow", default=DEFAULT_WORKFLOW)
    ap.add_argument("--profile", default=DEFAULT_PROFILE)

    src = ap.add_mutually_exclusive_group()
    src.add_argument("--caption", help="structured music description (long: prefer --caption-file)")
    src.add_argument("--caption-file", help="read the caption from a UTF-8 file")

    lyr = ap.add_mutually_exclusive_group()
    lyr.add_argument("--lyrics", help="lyrics with [verse]/[chorus] section tags")
    lyr.add_argument("--lyrics-file", help="read the lyrics from a UTF-8 file")
    lyr.add_argument("--instrumental", action="store_true",
                     help=f"no vocals: sets lyrics to {INSTRUMENTAL_LYRICS!r} (verify by ear)")

    ap.add_argument("--duration", "--seconds", dest="duration", type=float,
                    help="target length in seconds (max ~300; cost scales linearly)")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--steps", type=int, help="KSampler steps (template default 30)")
    ap.add_argument("--cfg-scale", type=float, help="MiniMaxMusic3TextEncode guidance (also pins sampler cfg)")
    ap.add_argument("--top-k", type=int, help="MiniMaxMusic3TextEncode top_k")
    ap.add_argument("--sampler-cfg", type=float, help="KSampler cfg on its own")
    ap.add_argument("--sampler", help="KSampler sampler_name (template default euler)")
    ap.add_argument("--scheduler", help="KSampler scheduler (template default simple)")
    ap.add_argument("--denoise", type=float)
    tiled = ap.add_mutually_exclusive_group()
    tiled.add_argument("--tiled", dest="tiled_decode", action="store_true", default=None,
                       help="tiled audio VAE decode (low VRAM; template default ON)")
    tiled.add_argument("--no-tiled", dest="tiled_decode", action="store_false",
                       help="full decode (best quality, needs more VRAM)")
    ap.add_argument("--tile-size", type=int, help="VAEDecodeAudioTiled tile_size (default 1536 in this workflow)")
    ap.add_argument("--overlap", type=int, help="VAEDecodeAudioTiled overlap (default 64)")
    ap.add_argument("--filename-prefix", help='server-side prefix (template default audio/audio_minimax_music3)')
    ap.add_argument("--unet-name")
    ap.add_argument("--clip-name")
    ap.add_argument("--vae-name")
    ap.add_argument("--set", dest="set_pairs", action="append", default=[], metavar="CLASS.FIELD=VALUE",
                    help="set any node field the profile does not name (repeatable)")
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--timeout", type=float, default=7200.0, help="seconds to wait for the job")
    ap.add_argument("--poll", type=float, default=10.0)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-record", dest="record", action="store_false")
    ap.add_argument("--check", action="store_true", help="verify required models and nodes on the server")
    ap.add_argument("--list", action="store_true", help="print the workflow's parameters and defaults")
    ap.add_argument("--plan", action="store_true", help="build and print the API graph without submitting")
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
             "workflow_models": workflow_model_names(args.workflow),
             "profile_parameters": sorted(prof.get("parameters", {})),
             "seconds_per_audio_second": SECONDS_PER_AUDIO_SECOND},
            ensure_ascii=False, indent=2))
        return 0

    caption = args.caption
    if args.caption_file:
        with open(args.caption_file, encoding="utf-8") as fh:
            caption = fh.read().strip()
    if not caption:
        ap.error("--caption or --caption-file is required (a run is expensive; there is no default)")

    lyrics = INSTRUMENTAL_LYRICS if args.instrumental else args.lyrics
    if args.lyrics_file:
        with open(args.lyrics_file, encoding="utf-8") as fh:
            lyrics = fh.read().strip()

    overrides = build_overrides(
        caption=caption, lyrics=lyrics, duration=args.duration, seed=args.seed,
        steps=args.steps, cfg_scale=args.cfg_scale, top_k=args.top_k,
        sampler_cfg=args.sampler_cfg, sampler=args.sampler, scheduler=args.scheduler,
        denoise=args.denoise, tiled_decode=args.tiled_decode, tile_size=args.tile_size,
        overlap=args.overlap, filename_prefix=args.filename_prefix,
        unet_name=args.unet_name, clip_name=args.clip_name, vae_name=args.vae_name,
    )

    if args.plan:
        report: dict = {}
        api_prompt, out_id, warnings, _prof, merged = build_graph(
            args.workflow, args.profile, overrides, args.set_pairs, report=report
        )
        print(json.dumps({
            "output_node": out_id,
            "nodes": len(api_prompt),
            "warnings": warnings,
            "unapplied_overrides": report.get("unapplied") or {},
            "overrides_entering_graph": {
                k: (v if k not in ("caption", "lyrics") else f"<{len(str(v))} chars>")
                for k, v in merged.items()
            },
            "eta_s": estimate_wall(args.duration),
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
