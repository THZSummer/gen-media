#!/usr/bin/env python3
"""Self-test for the image-tools skill.

Entirely offline: no ComfyUI, no model, no network.  ffmpeg and numpy are
required (that is the point of this skill), so a missing tool is reported as a
failure with the install hint rather than a traceback.

Run:
  python3 scripts/test_skill.py
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import contact_sheet  # noqa: E402
import ffkit  # noqa: E402
import pngdiff  # noqa: E402


def _pattern(w: int, h: int, fn) -> np.ndarray:
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            arr[y, x] = fn(x, y)
    return arr


def _write_with_text(path: str, w: int, h: int, colour, text: str) -> None:
    """Write a PNG carrying a tEXt chunk (ffmpeg never writes one itself)."""
    import struct
    import zlib
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    arr[:, :] = colour
    raw = bytearray()
    for _ in range(h):
        raw.append(0)
        raw += bytes(colour) * w

    def chunk(tag: bytes, body: bytes) -> bytes:
        return (struct.pack(">I", len(body)) + tag + body
                + struct.pack(">I", zlib.crc32(tag + body) & 0xFFFFFFFF))

    data = bytearray(ffkit.PNG_SIGNATURE)
    data += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    data += chunk(b"tEXt", b"workflow\x00" + text.encode())
    data += chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    data += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(bytes(data))


def check_ffkit(tmp: str) -> list[str]:
    failures: list[str] = []
    try:
        ffkit.require_ffmpeg()
    except ffkit.ToolError as exc:
        return [f"ffmpeg missing: {exc}"]

    # ---- encode/decode round trip is exact, for RGB and RGBA
    src = _pattern(37, 21, lambda x, y: ((x * 7) % 256, (y * 11) % 256, (x * y) % 256))
    a = os.path.join(tmp, "a.png")
    ffkit.encode(a, src)
    back = ffkit.decode(a)
    if back.shape != src.shape or not np.array_equal(back, src):
        failures.append(f"round trip mismatch: {back.shape} vs {src.shape}")
    if ffkit.png_chunks(a) != ["IHDR", "IDAT", "IEND"]:
        failures.append(f"unexpected chunks: {ffkit.png_chunks(a)}")
    rgba = np.dstack([src, np.full((21, 37), 128, dtype=np.uint8)])
    a4 = os.path.join(tmp, "a4.png")
    ffkit.encode(a4, rgba)
    if ffkit.decode(a4).shape[2] != 3:
        failures.append("rgb24 decode of an RGBA file did not flatten to 3 channels")
    if ffkit.decode(a4, pix_fmt="rgba").shape[2] != 4:
        failures.append("rgba decode did not keep the alpha channel")

    # ---- JPEG output (by extension) is deterministic, smaller, and decodable
    # 合并图/审计图用 JPEG（体积约为 PNG 的 1/8）；成品与对照仍必须用 PNG，
    # 因为 JPEG 的块效应会给「区域差 < 1.5 = 空操作」这条判据加约 1.2 的噪声底。
    jq = os.path.join(tmp, "a.jpg")
    ffkit.encode(jq, src, quality=2)
    jq2 = os.path.join(tmp, "a2.jpg")
    ffkit.encode(jq2, src, quality=2)
    if open(jq, "rb").read() != open(jq2, "rb").read():
        failures.append("JPEG encode is not deterministic")
    if ffkit.decode(jq).shape != src.shape:
        failures.append(f"JPEG round trip shape mismatch: {ffkit.decode(jq).shape}")
    # 体积：合成图案上 PNG 反而更小（PNG 很会压渐变），所以这里只验证
    # 「quality 数值越大 → 文件越小」这条单调性；真实照片上的实测收益见 SKILL.md
    # （一张 1.4MB 的成品 PNG → q2 的 JPEG 只有 164KB）。
    q2 = os.path.join(tmp, "q2.jpg")
    q10 = os.path.join(tmp, "q10.jpg")
    ffkit.encode(q2, src, quality=2)
    ffkit.encode(q10, src, quality=10)
    if os.path.getsize(q10) > os.path.getsize(q2):
        failures.append("JPEG quality is not monotonic in file size")

    # ---- probe reports geometry and the absence of ComfyUI metadata
    meta = ffkit.probe(a)
    if (meta["width"], meta["height"], meta["codec"]) != (37, 21, "png"):
        failures.append(f"probe geometry/codec wrong: {meta}")
    if meta["has_workflow_metadata"]:
        failures.append("probe claims tEXt metadata on a file that has none")
    if ffkit.probe(a4).get("pix_fmt") not in ("rgba", "rgb32", "rgba64be"):
        failures.append(f"probe pix_fmt unexpected: {ffkit.probe(a4).get('pix_fmt')}")

    # ---- box downscale averages exactly (4x4 -> 2x2, factor 2)
    grid = _pattern(4, 4, lambda x, y: (x * 10, y * 10, 0))
    small = ffkit.box_downscale(grid, 2)
    if small.shape != (2, 2, 3):
        failures.append(f"box_downscale shape wrong: {small.shape}")
    else:
        expect = [[[5, 5, 0], [25, 5, 0]], [[5, 25, 0], [25, 25, 0]]]
        if small.tolist() != expect:
            failures.append(f"box_downscale averaged wrong: {small.tolist()} != {expect}")
    if ffkit.box_downscale(grid, 8) is not grid:
        failures.append("box_downscale copied although within max_edge")

    # ---- crop clips; scale replicates
    piece = ffkit.crop(grid, 1, 2, 10, 10)
    if piece.shape != (2, 3, 3) or tuple(piece[0, 0]) != (10, 20, 0):
        failures.append(f"crop wrong: {piece.shape} {tuple(piece[0, 0])}")
    up = ffkit.scale_to(np.array([[[0, 0, 0], [100, 0, 0]]], dtype=np.uint8), 3)
    if up.shape != (3, 6, 3) or tuple(up[1, 3]) != (100, 0, 0):
        failures.append(f"scale_to wrong: {up.shape}")

    # ---- strip must drop metadata and keep pixels
    withmeta = os.path.join(tmp, "meta.png")
    _write_with_text(withmeta, 4, 4, (10, 20, 30), "workflow: {...}")
    if "tEXt" not in ffkit.png_chunks(withmeta):
        failures.append("fixture is wrong: no tEXt chunk to strip")
    stripped = os.path.join(tmp, "stripped.png")
    report = ffkit.strip_metadata(withmeta, stripped)
    if "tEXt" in ffkit.png_chunks(stripped):
        failures.append("strip left the tEXt chunk behind")
    if not pngdiff.compare(withmeta, stripped).same:
        failures.append("strip changed the pixels")
    if report.get("saved", 0) <= 0:
        failures.append(f"strip did not shrink the file: {report}")

    # ---- a non-integer ratio still lands within the cap
    wide = ffkit.box_downscale(_pattern(130, 71, lambda x, y: (x % 256, y % 256, 0)), 32)
    if max(wide.shape[:2]) > 32:
        failures.append(f"downscale exceeded the cap: {wide.shape}")
    return failures


def check_pngdiff(tmp: str) -> list[str]:
    failures: list[str] = []
    base_arr = np.full((32, 32, 3), 100, dtype=np.uint8)
    base = os.path.join(tmp, "d0.png")
    ffkit.encode(base, base_arr)

    # ---- metadata-only difference: bytes differ, pixels identical
    withmeta = os.path.join(tmp, "d1.png")
    _write_with_text(withmeta, 32, 32, (100, 100, 100), "workflow: {...}")
    if open(base, "rb").read() == open(withmeta, "rb").read():
        failures.append("fixture is wrong: a tEXt-only change kept the bytes equal")
    same, detail = pngdiff.pixels_equal(base, withmeta)
    if not same:
        failures.append(f"pixel compare should ignore tEXt-only differences: {detail}")

    # ---- a one-step change is detected with the right counts and metrics
    one = os.path.join(tmp, "d2.png")
    ffkit.encode(one, base_arr + 1)
    diff = pngdiff.compare(base, one)
    if diff.same or diff.differing != 1024 or diff.max_diff != 1:
        failures.append(f"1-LSB change mishandled: {diff}")
    if abs(diff.mean_abs_diff - 1.0) > 1e-9:
        failures.append(f"mean_abs_diff wrong: {diff.mean_abs_diff}")
    if abs(diff.psnr - 48.13) > 0.05:
        failures.append(f"psnr wrong: {diff.psnr}")
    if abs(diff.ssim - 1.0) > 1e-2:
        failures.append(f"ssim should stay high for a uniform 1-step shift: {diff.ssim}")

    # ---- metrics behave on the textbook cases
    if pngdiff.psnr(base_arr, base_arr) != float("inf"):
        failures.append("psnr of identical images is not inf")
    if abs(pngdiff.ssim(base_arr, base_arr) - 1.0) > 1e-9:
        failures.append("ssim of identical images is not 1")
    rng = np.random.default_rng(7)
    noise = rng.integers(0, 256, (32, 32, 3), dtype=np.uint8)
    if not (pngdiff.ssim(base_arr, noise) < 0.2 < pngdiff.ssim(base_arr, base_arr + 10)):
        failures.append("ssim does not order dissimilar < similar")
    if not (pngdiff.psnr(base_arr, base_arr + 1) > pngdiff.psnr(base_arr, base_arr + 20)):
        failures.append("psnr does not fall as the error grows")
    try:
        pngdiff.ssim(base_arr, base_arr[:16])
        failures.append("ssim accepted mismatched shapes")
    except ValueError:
        pass

    # ---- tolerance suppresses small deltas but keeps the statistics
    tol = pngdiff.compare(base, one, tolerance=1)
    if not tol.same or tol.max_diff != 1:
        failures.append(f"tolerance mishandled: {tol}")

    # ---- geometry mismatch is reported, not silently zero
    small = os.path.join(tmp, "d3.png")
    ffkit.encode(small, base_arr[:16, :16])
    geo = pngdiff.compare(base, small)
    if geo.same or "geometry differs" not in geo.detail:
        failures.append(f"geometry mismatch mishandled: {geo.detail}")

    # ---- a non-image must fail loudly, not crash
    junk = os.path.join(tmp, "junk.bin")
    open(junk, "wb").write(b"not an image at all")
    ok, detail = pngdiff.pixels_equal(base, junk)
    if ok or "cannot compare" not in detail:
        failures.append(f"non-image mishandled: {detail}")
    return failures


def check_contact_sheet(tmp: str) -> list[str]:
    failures: list[str] = []
    red = os.path.join(tmp, "s0-red_00001_.png")
    green = os.path.join(tmp, "s1-green_00001_.png")
    ffkit.encode(red, np.full((64, 64, 3), (200, 20, 20), dtype=np.uint8))
    ffkit.encode(green, np.full((64, 64, 3), (20, 200, 20), dtype=np.uint8))

    sheet = os.path.join(tmp, "sheet.png")
    man = contact_sheet.build_sheet([red, green, "-"], sheet, cols=3, cell=32,
                                    title="UNIT TEST")
    info = ffkit.probe(sheet)
    expect_w = contact_sheet.PAD + 3 * (32 + contact_sheet.PAD)
    if info["width"] != expect_w:
        failures.append(f"sheet width {info['width']} != {expect_w}")
    if man["rows"] != 1 or len(man["tiles"]) != 3:
        failures.append(f"manifest layout wrong: {man['rows']} rows, {len(man['tiles'])} tiles")
    if man["tile"] != [32, 32]:
        failures.append(f"tile was not downscaled to the cap: {man['tile']}")

    img = ffkit.decode(sheet)
    t0, t1, t2 = man["tiles"]
    if tuple(img[t0["y"] + 16, t0["x"] + 16]) != (200, 20, 20):
        failures.append(f"first tile is not red: {tuple(img[t0['y'] + 16, t0['x'] + 16])}")
    if tuple(img[t1["y"] + 16, t1["x"] + 16]) != (20, 200, 20):
        failures.append("second tile is not green")
    if tuple(img[t2["y"] + 16, t2["x"] + 16]) != contact_sheet.BLANK:
        failures.append("blank cell was not drawn blank")

    # ---- labels were really drawn (ink under the first tile, if drawtext exists)
    if man["labels_drawn"]:
        band = img[t0["y"] + t0["h"] + 4:t0["y"] + t0["h"] + 26, t0["x"]:t0["x"] + t0["w"]]
        ink = int(np.count_nonzero(np.any(band != np.array(contact_sheet.BG), axis=2)))
        if ink < 20:
            failures.append(f"no label ink found under the first tile (found {ink} px)")

    # ---- mixed aspect ratios: the smaller tile must be centred, not top-left
    tall = os.path.join(tmp, "tall_00001_.png")
    ffkit.encode(tall, np.full((64, 32, 3), (30, 30, 200), dtype=np.uint8))
    mixed = os.path.join(tmp, "mixed.png")
    man_mixed = contact_sheet.build_sheet([red, tall], mixed, cols=2, cell=32,
                                          labels=["a", "b"])
    img_mixed = ffkit.decode(mixed)
    tb = man_mixed["tiles"][1]           # 32x16 的方块放在 32x32 的格子里
    # 竖图 64x32 → 受 max_edge=32 限制后为 16x32（限制的是**最长边**）
    if tb["w"] != 16 or tb["h"] != 32:
        failures.append(f"mixed-aspect tile size wrong: {tb['w']}x{tb['h']}")
    else:
        # 第 2 格的**格子原点** = PAD + 1*(tw+PAD)；居中后图块应再内缩 (32-16)/2 = 8
        cell_x = contact_sheet.PAD + 1 * (man_mixed["tile"][0] + contact_sheet.PAD)
        left = tb["x"] - cell_x
        if not 6 <= left <= 10:
            failures.append(f"tile not centred horizontally: left margin {left}px "
                            f"(cell origin {cell_x}, tile x {tb['x']})")
        if tb["y"] != man_mixed["tiles"][0]["y"]:
            failures.append(f"tile not aligned to the cell top: y {tb['y']}")

    # ---- labels come from the filename, without ComfyUI's counter
    if contact_sheet._label_for("os-r1-owl-seam_00001_.png", "name") != "os-r1-owl-seam":
        failures.append("label_mode=name did not strip the ComfyUI counter")
    if contact_sheet._label_for("os-r1-owl-seam_00001_.png", "file") != "os-r1-owl-seam_00001_":
        failures.append("label_mode=file changed the stem")
    if contact_sheet._label_for("plain.png", "name") != "plain":
        failures.append("label_mode=name mangled a name without a counter")

    # ---- adversarial labels must not break the filtergraph
    if man["labels_drawn"]:
        nasty = ["a:b", "it's", "50%x", "a,b", "[x]", "p=q", "back\\slash", "骨瓷·公主"]
        try:
            contact_sheet.build_sheet([red] * len(nasty), os.path.join(tmp, "nasty.png"),
                                      cols=4, cell=24, labels=nasty, title="对抗性标题：测试")
        except ffkit.ToolError as exc:
            failures.append(f"adversarial labels broke drawtext: {exc}")

    # ---- CJK must render when a CJK font is present
    font = contact_sheet.default_font() or ""
    if "Noto" in font or "CJK" in font:
        cjk_sheet = os.path.join(tmp, "cjk.png")
        man_cjk = contact_sheet.build_sheet([red], cjk_sheet, cols=1, cell=32, title="骨瓷国公主")
        if not man_cjk["labels_drawn"]:
            failures.append("CJK title was silently dropped")

    # ---- --round mode reads a project round.json and flags unapplied params
    rj = os.path.join(tmp, "round.json")
    json.dump({"round": 7, "engine": "qwen",
               "shots": [{"name": "cat", "seed": 4201, "file": red, "unapplied": {}},
                         {"name": "owl", "seed": 4201, "file": green, "unapplied": {}}]},
              open(rj, "w"))
    paths, labels, title = contact_sheet._load_round(rj)
    if paths != [red, green] or labels != ["cat · seed 4201", "owl · seed 4201"]:
        failures.append(f"round mode wrong: {paths} {labels}")
    if title != "R7 · qwen · seed 4201":
        failures.append(f"round title wrong: {title!r}")
    json.dump({"round": 8, "engine": "qwen", "shots": [
        {"name": "x", "seed": 1, "file": red, "unapplied": {"width": 512}}]}, open(rj, "w"))
    if "UNAPPLIED" not in contact_sheet._load_round(rj)[2]:
        failures.append("round mode missed a non-empty unapplied field")
    json.dump({"round": 9, "engine": "qwen", "shots": [
        {"name": "y", "seed": 1, "file": None}]}, open(rj, "w"))
    if contact_sheet._load_round(rj)[0] != ["-"]:
        failures.append("round mode did not turn a missing file into a blank cell")

    # ---- a stale absolute path must fall back to the file beside round.json
    #      (projects get reorganised; round.json keeps the historical path)
    json.dump({"round": 10, "engine": "zimage", "shots": [
        {"name": "moved", "seed": 1,
         "file": os.path.join(tmp, "some-old-location", os.path.basename(red)),
         "unapplied": {}}]}, open(rj, "w"))
    moved_paths = contact_sheet._load_round(rj)[0]
    if moved_paths != [red]:
        failures.append(f"stale path not resolved to the sibling file: {moved_paths}")
    man_moved = contact_sheet.build_sheet(moved_paths, os.path.join(tmp, "moved.png"),
                                          cols=1, cell=16)
    if man_moved["tiles"][0]["w"] != 16:
        failures.append("sheet from a stale round.json did not render")

    # ---- a missing file must fail loudly
    try:
        contact_sheet.build_sheet([os.path.join(tmp, "nope.png")], sheet, cols=1)
        failures.append("build_sheet accepted a missing file")
    except (OSError, ffkit.ToolError):
        pass
    return failures


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.parse_args(argv)
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        for name, fn in (("ffkit", check_ffkit), ("pngdiff", check_pngdiff),
                         ("contact_sheet", check_contact_sheet)):
            got = fn(tmp)
            print(f"{name}: {'OK' if not got else 'FAIL'}")
            failures += got
    for f in failures:
        print("  -", f)
    print("RESULT:", "PASS" if not failures else "FAIL")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
