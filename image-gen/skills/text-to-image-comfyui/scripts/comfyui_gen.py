#!/usr/bin/env python3
"""Submit the Z-Image-Turbo text-to-image workflow to a ComfyUI server and
download the resulting image(s).

Pipeline:
  1. read the UI workflow JSON, convert it to API format (see comfyui_convert)
  2. POST /prompt                      -> prompt_id
  3. poll /history/{prompt_id}         -> outputs
  4. GET /view?...                     -> save every produced image locally

Examples:
  python3 comfyui_gen.py --server http://192.168.3.5:18000 \
      --prompt "a red fox in snow, cinematic" --width 1024 --height 1024 \
      --steps 8 --seed 42 --out-dir out/

  # check the server before spending time on generation
  python3 comfyui_gen.py --server http://192.168.3.5:18000 --check

  # block up to 20 minutes, quiet progress
  python3 comfyui_gen.py --prompt "..." --timeout 1200 --quiet
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comfyui_convert import convert, load_node_info  # noqa: E402

DEFAULT_SERVER = os.environ.get("COMFYUI_SERVER", "http://192.168.3.5:18000")
DEFAULT_WORKFLOW = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "assets", "z-image-turbo-ui.json"
)
DAYONE_NODE_INFO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "references", "node-info.json"
)


def _load_node_info(path: str) -> bool:
    """Load a cached /object_info subset; returns True when usable.

    A real ComfyUI export is a dict of class names; a hand-written day-one
    placeholder carries a "note" key and is ignored in favour of built-ins.
    """
    if not path or not os.path.exists(path):
        return False
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return False
    if not isinstance(data, dict) or not data:
        return False
    if any(k in ("note", "$schema", "_comment") for k in data):
        return False
    load_node_info(path)
    return True



def record_request(
    out_dir: str,
    prefix: str,
    engine: str,
    server: str,
    params: dict,
    prompt_id: str,
    graph: dict,
    files: list[str],
) -> dict:
    """Persist everything needed to reproduce a generation.

    Writes two artifacts next to the images:
      * ``<prefix>.api.json``  - the exact API graph that was submitted
      * ``requests.jsonl``     - one appended line per request (params + files)
    """
    os.makedirs(out_dir, exist_ok=True)
    api_name = f"{prefix}.api.json"
    with open(os.path.join(out_dir, api_name), "w", encoding="utf-8") as fh:
        json.dump(graph, fh, ensure_ascii=False, indent=2)
    entry = {
        "time": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "engine": engine,
        "server": server,
        "prompt_id": prompt_id,
        "prefix": prefix,
        "api_file": api_name,
        "files": files,
    }
    entry.update(params)
    with open(os.path.join(out_dir, "requests.jsonl"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def _request(
    url: str,
    data: bytes | None = None,
    method: str | None = None,
    timeout: float = 30.0,
    content_type: str | None = None,
):
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", content_type or "application/json")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _get_json(url: str, timeout: float = 30.0):
    return json.loads(_request(url, timeout=timeout).decode("utf-8"))


def check_server(server: str, timeout: float = 10.0) -> dict:
    """Return {'reachable', 'stats', 'error'} without raising."""
    out: dict = {"reachable": False, "stats": None, "error": None}
    try:
        out["stats"] = _get_json(f"{server.rstrip('/')}/system_stats", timeout=timeout)
        out["reachable"] = True
    except Exception as exc:  # noqa: BLE001 - reported to the user as-is
        out["error"] = f"{type(exc).__name__}: {exc}"
    return out


def list_models(server: str, folder: str, timeout: float = 15.0) -> list[str]:
    """List model files for a ComfyUI folder (e.g. diffusion_models, vae)."""
    data = _get_json(f"{server.rstrip('/')}/models/{urllib.parse.quote(folder)}", timeout=timeout)
    return list(data) if isinstance(data, list) else []


def queue_prompt(server: str, api_prompt: dict, client_id: str, timeout: float = 60.0) -> str:
    body = json.dumps({"prompt": api_prompt, "client_id": client_id}).encode("utf-8")
    payload = json.loads(_request(f"{server.rstrip('/')}/prompt", data=body, timeout=timeout).decode("utf-8"))
    if "prompt_id" not in payload:
        raise RuntimeError(f"unexpected /prompt response: {payload}")
    return payload["prompt_id"]


def wait_for_history(
    server: str,
    prompt_id: str,
    timeout: float = 600.0,
    poll: float = 2.0,
    quiet: bool = False,
) -> dict:
    """Poll /history until our prompt shows up (ComfyUI only records finished jobs)."""
    url = f"{server.rstrip('/')}/history/{urllib.parse.quote(prompt_id)}"
    deadline = time.time() + timeout
    last_note = 0.0
    while True:
        payload = _get_json(url, timeout=30.0)
        if prompt_id in payload:
            return payload[prompt_id]
        if time.time() > deadline:
            raise TimeoutError(f"prompt {prompt_id} not finished within {timeout:.0f}s")
        if not quiet and time.time() - last_note > 15:
            print(f"  ...waiting for {prompt_id}", flush=True)
            last_note = time.time()
        time.sleep(poll)


def collect_images(history_entry: dict, only_node: str | None = None) -> list[dict]:
    """Flatten a history entry's outputs into downloadable image descriptors.

    ``only_node`` restricts the result to one node's outputs, which matters when
    the graph also contains PreviewImage (it writes ComfyUI_temp_* previews that
    would otherwise be downloaded instead of the real SaveImage result).
    """
    images: list[dict] = []
    for node_id, node_out in (history_entry.get("outputs") or {}).items():
        if only_node is not None and str(node_id) != str(only_node):
            continue
        for img in node_out.get("images", []) or []:
            images.append(
                {
                    "node_id": str(node_id),
                    "filename": img.get("filename"),
                    "subfolder": img.get("subfolder", ""),
                    "type": img.get("type", "output"),
                }
            )
    return images


def download_image(server: str, img: dict, out_dir: str, timeout: float = 120.0) -> str:
    query = urllib.parse.urlencode(
        {
            "filename": img["filename"],
            "subfolder": img.get("subfolder", ""),
            "type": img.get("type", "output"),
        }
    )
    os.makedirs(out_dir, exist_ok=True)
    local_name = os.path.basename(img["filename"])
    local_path = os.path.join(out_dir, local_name)
    data = _request(f"{server.rstrip('/')}/view?{query}", timeout=timeout)
    with open(local_path, "wb") as fh:
        fh.write(data)
    return local_path


def generate(
    server: str = DEFAULT_SERVER,
    workflow: str = DEFAULT_WORKFLOW,
    prompt: str | None = None,
    width: int | None = None,
    height: int | None = None,
    seed: int | None = None,
    steps: int | None = None,
    unet_name: str | None = None,
    clip_name: str | None = None,
    vae_name: str | None = None,
    filename_prefix: str | None = None,
    batch_size: int | None = None,
    negative: str | None = None,
    out_dir: str = "out",
    timeout: float = 600.0,
    poll: float = 2.0,
    quiet: bool = False,
    record: bool = True,
    node_info: str | None = DAYONE_NODE_INFO,
    allow_unapplied: bool = False,
) -> dict:
    """Run one text-to-image generation; returns a JSON-serialisable summary."""
    if negative:
        print(
            "WARNING: this workflow has no negative encoder (ConditioningZeroOut);"
            " --negative is ignored.",
            file=sys.stderr,
        )
    _load_node_info(node_info or "")
    ui = json.load(open(workflow, encoding="utf-8"))
    convert_report: dict = {}
    api_prompt, save_id = convert(
        ui,
        {
            "prompt": prompt,
            "width": width,
            "height": height,
            "seed": seed,
            "steps": steps,
            "unet_name": unet_name,
            "clip_name": clip_name,
            "vae_name": vae_name,
            "filename_prefix": filename_prefix,
            "batch_size": batch_size,
        },
        strict=not allow_unapplied,
        report=convert_report,
    )
    unapplied = convert_report.get("unapplied") or {}
    if unapplied:
        print(
            f"WARNING: these parameters never reached the graph: {unapplied}",
            file=sys.stderr,
        )
    if save_id is None:
        raise RuntimeError("workflow has no SaveImage node; cannot locate outputs")

    client_id = f"dsh-image-gen-{os.getpid()}"
    if not quiet:
        print(f"-> {server}  prompt={prompt!r} {width}x{height} steps={steps} seed={seed}", flush=True)
    prompt_id = queue_prompt(server, api_prompt, client_id)
    if not quiet:
        print(f"   queued: {prompt_id}", flush=True)
    entry = wait_for_history(server, prompt_id, timeout=timeout, poll=poll, quiet=quiet)
    images = collect_images(entry, only_node=save_id)
    local_paths = []
    for img in images:
        if img.get("filename"):
            local_paths.append(download_image(server, img, out_dir))
    if not quiet:
        for path in local_paths:
            print(f"   saved: {path} ({os.path.getsize(path)} bytes)", flush=True)
    if record:
        record_request(
            out_dir=out_dir,
            prefix=(filename_prefix or "z-image-turbo"),
            engine="z-image-turbo",
            server=server,
            params={
                "prompt": prompt,
                "negative": None,
                "workflow": os.path.basename(workflow),
                "width": width,
                "height": height,
                "steps": steps,
                "seed": seed,
                "filename_prefix": filename_prefix,
                "unet_name": unet_name,
                "clip_name": clip_name,
                "vae_name": vae_name,
                "unapplied": unapplied,
            },
            prompt_id=prompt_id,
            graph=api_prompt,
            files=local_paths,
        )
    return {
        "prompt_id": prompt_id,
        "images": images,
        "local_paths": local_paths,
        "status": (entry.get("status") or {}).get("status_str"),
        "unapplied": unapplied,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=DEFAULT_SERVER, help=f"ComfyUI base URL (default {DEFAULT_SERVER})")
    ap.add_argument("--workflow", default=DEFAULT_WORKFLOW, help="UI workflow JSON")
    ap.add_argument("--node-info", default=DAYONE_NODE_INFO, help="cached /object_info subset (optional)")
    ap.add_argument("--prompt", help="text prompt")
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--steps", type=int)
    ap.add_argument("--unet-name")
    ap.add_argument("--clip-name")
    ap.add_argument("--vae-name")
    ap.add_argument("--filename-prefix", help="SaveImage filename prefix (default z-image-turbo)")
    ap.add_argument("--batch", "--batch-size", dest="batch_size", type=int, help="images per request (default 1)")
    ap.add_argument("--negative", help="NOT supported by this workflow (no negative encoder); warns and ignores")
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--timeout", type=float, default=600.0, help="seconds to wait for the job")
    ap.add_argument("--poll", type=float, default=2.0)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-record", dest="record", action="store_false",
                    help="do not write <prefix>.api.json / requests.jsonl next to the outputs")
    ap.add_argument("--check", action="store_true", help="probe the server and exit")
    ap.add_argument("--list-models", metavar="FOLDER", help="list model files in a ComfyUI folder")
    ap.add_argument("--allow-unapplied", action="store_true",
                    help="do not fail when a parameter has no matching input in the workflow")
    args = ap.parse_args(argv)

    if args.check:
        result = check_server(args.server)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["reachable"] else 2
    if args.list_models:
        print(json.dumps(list_models(args.server, args.list_models), ensure_ascii=False, indent=2))
        return 0
    if not args.prompt:
        ap.error("--prompt is required unless --check / --list-models is used")

    result = generate(
        server=args.server,
        workflow=args.workflow,
        prompt=args.prompt,
        width=args.width,
        height=args.height,
        seed=args.seed,
        steps=args.steps,
        unet_name=args.unet_name,
        clip_name=args.clip_name,
        vae_name=args.vae_name,
        filename_prefix=args.filename_prefix,
        batch_size=args.batch_size,
        negative=args.negative,
        out_dir=args.out_dir,
        timeout=args.timeout,
        poll=args.poll,
        quiet=args.quiet,
        record=args.record,
        node_info=args.node_info,
        allow_unapplied=args.allow_unapplied,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["local_paths"] else 1


if __name__ == "__main__":
    sys.exit(main())
