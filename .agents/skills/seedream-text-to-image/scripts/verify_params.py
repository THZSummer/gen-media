#!/usr/bin/env python3
"""真机参数矩阵：每个可调参数实跑一次，用**解码后的像素**证明它真的落到了图上。

这是付费验证：默认矩阵 6 张图（都取 1K 预设，最小成本）。没有凭据就**直接退出**（exit 2），
不会假装通过。判据与仓库其它技能一致——

  * "参数生效"看像素差，不看文件哈希（PNG 里嵌了执行图，换个前缀哈希就变）；
  * 尺寸看 PNG 头解出来的真实宽高，不看命令行回了什么；
  * 同一个 seed 重跑是否逐像素一致，**如实记录**：远端模型的复现性不能假设，
    这项只报告不判定（不同 seed 必须不同 —— 那才证明 seed 真的传到了模型）。

Examples:
  python3 scripts/verify_params.py --yes                    # 跑默认 6 步矩阵
  python3 scripts/verify_params.py --yes --steps size,seed   # 只跑指定步骤
  python3 scripts/verify_params.py --api-key-file ../../../work/comfy_api_key --yes
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import seedream_gen as sg  # noqa: E402

DEFAULT_OUT = os.path.join(HERE, "..", ".verify", "seedream")
PROMPT = "九尾狐 素描 线稿"


def png_size(path: str) -> tuple[int, int]:
    """从 PNG 头读真实宽高（IHDR 固定在第 16..24 字节）。"""
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} 不是 PNG，无法从头部读尺寸")
    return struct.unpack(">II", head[16:24])


def pixel_digest(path: str) -> str:
    """解码成 raw RGB24 再哈希 —— 与文件哈希无关，只看像素。"""
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True, check=True).stdout
    return hashlib.sha256(out).hexdigest()[:16]


def credential_kwargs(credential: dict) -> dict:
    """把查到的凭据转成 generate() 的参数 —— 漏传这一步就会白跑一轮并报 Unauthorized。"""
    if not credential.get("present"):
        return {}
    field = "api_key" if credential["channel"] == "api_key" else "auth_token"
    return {field: credential["value"]}


def run_step(name: str, out_dir: str, credential: dict, **kwargs) -> dict:
    kwargs.setdefault("out_dir", out_dir)
    kwargs.setdefault("quiet", True)
    kwargs.setdefault("record", True)
    result = sg.generate(server=kwargs.pop("server"), prompt=kwargs.pop("prompt", PROMPT),
                         **credential_kwargs(credential), **kwargs)
    paths = result["local_paths"]
    if not paths:
        raise RuntimeError(f"{name}: 没有下载到图")
    if result.get("credential_channel") != credential["channel"]:
        raise RuntimeError(f"{name}: 提交时没用上凭据（channel={result.get('credential_channel')}）"
                           " —— 检查 run_step 有没有把凭据传下去")
    path = paths[0]
    cached = [n for n in result.get("cached_nodes", []) if n == "3"]
    return {"name": name, "file": os.path.basename(path), "size": png_size(path),
            "digest": pixel_digest(path), "prompt_id": result["prompt_id"],
            "seedream_node_cached": bool(cached)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=sg.DEFAULT_SERVER)
    ap.add_argument("--api-key")
    ap.add_argument("--api-key-file")
    ap.add_argument("--auth-token", help="改用浏览器登录态 Bearer token 通道")
    ap.add_argument("--out-dir", default=DEFAULT_OUT)
    ap.add_argument("--seed", type=int, default=424242)
    ap.add_argument("--timeout", type=float, default=1200.0)
    ap.add_argument("--steps", default="baseline,repeat,seed,size,thinking,model",
                    help="逗号分隔：baseline,repeat,seed,size,thinking,model")
    ap.add_argument("--yes", action="store_true", help="确认为这次真机验证付费")
    args = ap.parse_args(argv)

    key = sg.resolve_credential(args.api_key, args.api_key_file, args.auth_token)
    if not key["present"]:
        print(json.dumps({
            "status": "SKIPPED_NO_CREDENTIAL",
            "why": "付费 partner 节点需要 ComfyUI 账号凭据；没有凭据就无从验证出图",
            "how": "拿 platform.comfy.org 的 API Key，用 --api-key-file / $COMFYUI_API_KEY 传进来",
        }, ensure_ascii=False, indent=2))
        return 2

    steps = [s.strip() for s in args.steps.split(",") if s.strip()]
    os.makedirs(args.out_dir, exist_ok=True)
    if not args.yes:
        print(f"这会真出图（{len(steps)} 张，按 ComfyUI 账号额度计费）。确认后加 --yes。")
        return 2

    report: dict = {"server": args.server, "credential_channel": key["channel"],
                    "credential_source": key["source"], "steps": [], "checks": [],
                    "result": "PASS"}
    runs: dict[str, dict] = {}

    def add_check(label: str, ok: bool, detail: str = "") -> None:
        report["checks"].append({"check": label, "ok": bool(ok), "detail": detail})
        if not ok:
            report["result"] = "FAIL"

    def step(name: str, **kwargs) -> None:
        if name not in steps:
            return
        runs[name] = run_step(name, args.out_dir, key, server=args.server, **kwargs)
        report["steps"].append(runs[name])
        print(f"  {name}: {runs[name]['size']} digest={runs[name]['digest']}", flush=True)

    try:
        step("baseline", seed=args.seed, size="1024x1024")
        if "baseline" in runs:
            add_check("1K 预设出的是 1024x1024", runs["baseline"]["size"] == (1024, 1024),
                      str(runs["baseline"]["size"]))

        step("repeat", seed=args.seed, size="1024x1024")
        if "baseline" in runs and "repeat" in runs:
            same = runs["baseline"]["digest"] == runs["repeat"]["digest"]
            cached = runs["repeat"]["seedream_node_cached"]
            report["same_seed_digest_identical"] = same
            report["repeat_seedream_node_cached"] = cached
            report["same_seed_reproducible"] = bool(same) and not cached
            add_check("同 seed 重跑尺寸一致",
                      runs["baseline"]["size"] == runs["repeat"]["size"],
                      "digest 一致" if same else "digest 不同")
            if cached:
                report["same_seed_note"] = (
                    "这轮 Seedream 节点被 ComfyUI 缓存命中（history 里 execution_cached 含节点 3）——"
                    "图一致只证明缓存语义，**不能**当成远端模型的复现性；要真测请让服务器带 "
                    "--cache-none 重启后再跑")

        step("seed", seed=args.seed + 1, size="1024x1024")
        if "baseline" in runs and "seed" in runs:
            add_check("换 seed 像素确实变了",
                      runs["baseline"]["digest"] != runs["seed"]["digest"],
                      "同 digest 说明 seed 没传到模型")

        step("size", seed=args.seed, size="1440x2560")
        if "size" in runs:
            add_check("--size 1440x2560 出的是 1440x2560", runs["size"]["size"] == (1440, 2560),
                      str(runs["size"]["size"]))

        step("thinking", seed=args.seed, size="1024x1024", thinking=False)
        if "thinking" in runs:
            add_check("--no-thinking 能出图", runs["thinking"]["size"] == (1024, 1024),
                      str(runs["thinking"]["size"]))

        step("model", seed=args.seed, size="1024x1024", model="seedream 5.0 flash")
        if "model" in runs:
            add_check("换模型（seedream 5.0 flash）能出图",
                      runs["model"]["size"] == (1024, 1024), str(runs["model"]["size"]))
    except Exception as exc:  # noqa: BLE001 - 真机失败原因原样落进报告
        report["result"] = "FAIL"
        report["error"] = f"{type(exc).__name__}: {exc}"

    path = os.path.join(args.out_dir, "verify-report.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    print(json.dumps({"checks": report["checks"], "result": report["result"],
                      "report": path}, ensure_ascii=False, indent=2))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
