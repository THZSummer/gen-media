#!/usr/bin/env python3
"""真机付费矩阵：把"参考图这条路"的每一环实跑一遍，用**解码后的像素**当判据。

这是付费验证（默认 4 张图，都取 1K 预设 = 最小成本）。没有凭据就直接退出（exit 2），
不会假装通过。四条支路各一张：

  edit      单参考：把背景改成纯白 —— 证明"编辑指令真的落到了图上"（边缘纸色变白）
  annotate  单参考 + 标注层：证明 Painter 的合成结果真的进了图（合成图与底图**只在标注框内**
            不同 —— 这条是确定性判据，跟模型听不听话无关），并记录模型对标注区的响应
  refs2     两张参考图：证明 `model.images.image_2` 这条采集式输入真的能用
  flash     换模型（seedream 5.0 flash）+ 参考图：证明模型切换后编辑照跑

判据纪律与仓库其它技能一致：**看像素，不看文件哈希**；尺寸看 PNG 头解出来的真实宽高。
模型"听不听话"的部分（标注区有没有变黑）作为观察项如实记录，不跟接线判据混在一起。

Examples:
  python3 scripts/verify_edits.py --yes
  python3 scripts/verify_edits.py --yes --steps edit,refs2
  python3 scripts/verify_edits.py --api-key-file ../../../work/comfy_api_key --yes
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _shared  # noqa: E402

_shared.ensure()
import seedream_gen as G  # noqa: E402
import seedream_edit as E  # noqa: E402

REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
DEFAULT_OUT = os.path.normpath(os.path.join(HERE, "..", ".verify", "edit"))
DEFAULT_REF1 = os.path.join(REPO, "projects", "shanhai-jing", "subjects", "lu-shu",
                            "period-01", "01-lu-shu.png")
DEFAULT_REF2 = os.path.join(REPO, "projects", "shanhai-jing", "subjects", "jiu-wei-hu",
                            "period-01", "01-jiu-wei-hu.png")
# 标注框（x, y, w, h）：盖在鹿蜀身上，方便肉眼复核
BOX = (300, 420, 320, 280)
STEPS = ("edit", "annotate", "refs2", "flash")


# --------------------------------------------------------------------------
# 像素工具（ffmpeg + numpy，不用 Pillow）
# --------------------------------------------------------------------------
def decode_rgb(path: str):
    import numpy as np
    meta = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "csv=p=0", path],
        capture_output=True, check=True).stdout.decode().strip().splitlines()[0]
    width, height = (int(v) for v in meta.split(",")[:2])
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(height, width, 3).astype(int)


def png_size(path: str) -> tuple[int, int]:
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} 不是 PNG，无法从头部读尺寸")
    return struct.unpack(">II", head[16:24])


def preset_size(preset: str) -> tuple[int, int] | None:
    hit = re.search(r"(\d+)x(\d+)", preset or "")
    return (int(hit.group(1)), int(hit.group(2))) if hit else None


def pixel_digest(path: str) -> str:
    """解码成 raw RGB24 再哈希 —— 与文件哈希无关，只看像素。"""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True, check=True).stdout
    return hashlib.sha256(raw).hexdigest()[:16]


def edge_white_fraction(arr, band: float = 0.06) -> float:
    """四边各取 band 宽的带，算"接近纯白"的像素占比（min(RGB) >= 235）。"""
    height, width = arr.shape[:2]
    step = max(1, int(min(height, width) * band))
    edges = [arr[:step, :], arr[-step:, :], arr[:, :step], arr[:, -step:]]
    import numpy as np
    total = sum(e.reshape(-1, 3).shape[0] for e in edges)
    white = sum(int((e.reshape(-1, 3).min(axis=1) >= 235).sum()) for e in edges)
    return white / total


def region_luma(arr, box) -> float:
    x, y, w, h = box
    patch = arr[y:y + h, x:x + w]
    return float(patch.mean())


def make_overlay(path: str, size: tuple[int, int], box, colour=(220, 30, 30)) -> str:
    """造一张"透明底 + 一块不透明色块"的 RGBA 标注层（Painter 只认 alpha）。"""
    import numpy as np
    width, height = size
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    x, y, w, h = box
    canvas[y:y + h, x:x + w] = [*colour, 255]
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
         "-s", f"{width}x{height}", "-i", "-", "-frames:v", "1", path],
        input=canvas.tobytes(), check=True)
    return path


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
    prefix = f"verify-{name}"
    result = E.generate(server=kwargs.pop("server"), prompt=kwargs.pop("prompt"),
                        filename_prefix=prefix, **credential_kwargs(credential), **kwargs)
    if not result["local_paths"]:
        raise RuntimeError(f"{name}: 没有下载到图")
    if result.get("credential_channel") != credential["channel"]:
        raise RuntimeError(f"{name}: 提交时没用上凭据（channel={result.get('credential_channel')}）")
    path = result["local_paths"][0]
    return {"name": name, "file": os.path.basename(path), "path": path,
            "size": png_size(path), "digest": pixel_digest(path),
            "prompt_id": result["prompt_id"], "model": result.get("model"),
            "ref_keys": result.get("ref_keys"), "preset": result.get("preset"),
            "composite": [os.path.basename(p) for p in result.get("composite_paths") or []],
            "composite_path": (result.get("composite_paths") or [None])[0]}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=G.DEFAULT_SERVER)
    ap.add_argument("--api-key")
    ap.add_argument("--api-key-file")
    ap.add_argument("--auth-token", help="改用浏览器登录态 Bearer token 通道")
    ap.add_argument("--out-dir", default=DEFAULT_OUT)
    ap.add_argument("--ref1", default=DEFAULT_REF1, help="底图（默认仓库里的鹿蜀定稿）")
    ap.add_argument("--ref2", default=DEFAULT_REF2, help="第二张参考图（默认九尾狐定稿）")
    ap.add_argument("--timeout", type=float, default=1200.0)
    ap.add_argument("--steps", default=",".join(STEPS), help="逗号分隔：" + ",".join(STEPS))
    ap.add_argument("--yes", action="store_true", help="确认为这次真机验证付费")
    args = ap.parse_args(argv)

    key = G.resolve_credential(args.api_key, args.api_key_file, args.auth_token)
    if not key["present"]:
        print(json.dumps({
            "status": "SKIPPED_NO_CREDENTIAL",
            "why": "付费 partner 节点需要 ComfyUI 账号凭据；没有凭据就无从验证编辑出图",
            "how": "拿 platform.comfy.org 的 API Key，用 --api-key-file / $COMFYUI_API_KEY 传进来",
        }, ensure_ascii=False, indent=2))
        return 2

    steps = [s.strip() for s in args.steps.split(",") if s.strip()]
    unknown = [s for s in steps if s not in STEPS]
    if unknown:
        ap.error(f"不认识的步骤 {unknown}；可选：{', '.join(STEPS)}")
    if not args.yes:
        print(f"这会真出图（{len(steps)} 张，按 ComfyUI 账号额度计费）。确认后加 --yes。")
        return 2

    os.makedirs(args.out_dir, exist_ok=True)
    report: dict = {"server": args.server, "credential_channel": key["channel"],
                    "credential_source": key["source"], "steps": [], "checks": [],
                    "observations": [], "result": "PASS"}
    runs: dict[str, dict] = {}

    def add_check(label: str, ok: bool, detail: str = "") -> None:
        report["checks"].append({"check": label, "ok": bool(ok), "detail": detail})
        if not ok:
            report["result"] = "FAIL"

    def observe(label: str, detail: str) -> None:
        report["observations"].append({"observation": label, "detail": detail})

    def step(name: str, **kwargs) -> None:
        if name not in steps:
            return
        runs[name] = run_step(name, args.out_dir, key, server=args.server, **kwargs)
        report["steps"].append(runs[name])
        print(f"  {name}: {runs[name]['size']} digest={runs[name]['digest']} "
              f"refs={runs[name]['ref_keys']}", flush=True)

    overlay = make_overlay(os.path.join(args.out_dir, "annotate-overlay.png"),
                           E.image_size(args.ref1), BOX)
    base_arr = decode_rgb(args.ref1)
    base_edge_white = edge_white_fraction(base_arr)
    base_box_luma = region_luma(base_arr, BOX)
    report["baseline"] = {"source": os.path.basename(args.ref1),
                          "edge_white_fraction": round(base_edge_white, 4),
                          "box_luma": round(base_box_luma, 2)}

    try:
        step("edit", images=[args.ref1],
             prompt="把整幅画的背景改成纯白色，画里的动物保持不动")
        if "edit" in runs:
            size_ok = preset_size(runs["edit"]["preset"]) == runs["edit"]["size"]
            add_check("单参考：出的图就是请求的预设尺寸", size_ok,
                      f"preset={runs['edit']['preset']} 实际={runs['edit']['size']}")
            out = decode_rgb(runs["edit"]["path"])
            white = edge_white_fraction(out)
            report["edge_white_after"] = round(white, 4)
            add_check("单参考：背景改动真的落到边缘像素上（白占比上升 ≥0.25）",
                      white - base_edge_white >= 0.25,
                      f"底图 {base_edge_white:.3f} -> 出图 {white:.3f}")

        step("annotate", images=[args.ref1], annotate=overlay,
             prompt="把红框标出的整块区域改成纯黑色")
        if "annotate" in runs:
            composite = runs["annotate"]["composite_path"]
            add_check("带标注：Painter 的合成结果被下载留档", bool(composite),
                      str(runs["annotate"]["composite"]))
            if composite:
                comp = decode_rgb(composite)
                x, y, w, h = BOX
                inside = (abs(comp[y:y + h, x:x + w] - base_arr[y:y + h, x:x + w]).sum(axis=2) > 12)
                outside = (abs(comp - base_arr).sum(axis=2) > 12)
                inside_ratio = float(inside.mean())
                outside_ratio = float(outside.sum() - inside.sum()) / max(
                    1, outside.size - inside.size)
                add_check("带标注：合成图与底图只在标注框内不同（≥0.95 且框外 ≈ 0）",
                          inside_ratio >= 0.95 and outside_ratio <= 0.01,
                          f"框内 {inside_ratio:.3f}，框外 {outside_ratio:.5f}")
                add_check("带标注：合成图的尺寸与底图一致",
                          comp.shape == base_arr.shape,
                          f"{comp.shape[:2][::-1]} vs {base_arr.shape[:2][::-1]}")
            out = decode_rgb(runs["annotate"]["path"])
            after = region_luma(out, BOX)
            observe("标注区改成纯黑：模型响应（观察项，不是接线判据）",
                    f"标注框内平均亮度 {base_box_luma:.1f} -> {after:.1f}")

        step("refs2", images=[args.ref1, args.ref2],
             prompt="把两张参考图里的动物并排画在同一张画里，保留各自的颜色与花纹")
        if "refs2" in runs:
            add_check("双参考：两张图分别接到 image_1 / image_2",
                      runs["refs2"]["ref_keys"] == ["model.images.image_1",
                                                    "model.images.image_2"],
                      str(runs["refs2"]["ref_keys"]))
            add_check("双参考：出的图与底图不是同一张",
                      runs["refs2"]["digest"] != pixel_digest(args.ref1),
                      runs["refs2"]["digest"])

        step("flash", images=[args.ref1], model="seedream 5.0 flash",
             prompt="把整幅画的背景改成纯白色")
        if "flash" in runs:
            add_check("换模型 + 参考图照跑（seedream 5.0 flash）",
                      runs["flash"]["model"] == "seedream 5.0 flash"
                      and preset_size(runs["flash"]["preset"]) == runs["flash"]["size"],
                      f"model={runs['flash']['model']} preset={runs['flash']['preset']} "
                      f"实际={runs['flash']['size']}")
    except Exception as exc:  # noqa: BLE001 - 真机失败原因原样落进报告
        report["result"] = "FAIL"
        report["error"] = f"{type(exc).__name__}: {exc}"

    path = os.path.join(args.out_dir, "verify-report.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    print(json.dumps({"checks": report["checks"], "observations": report["observations"],
                      "result": report["result"], "report": path},
                     ensure_ascii=False, indent=2))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
