#!/usr/bin/env python3
"""comfyui-multi-angle 的离线自检（不需要服务器、不需要 GPU）。

这个模板有 498 KB、9 个子图、193 个展开节点，最大的风险是**接口漂移**（有人改了
子图接口名/角度提示词/输出前缀，脚本就静默错位）。所以这里把"事实"全部钉住：

  1. 工作流解剖：8 个角度（键 / 提示词 / 槽位顺序 / 输出节点）与父图、子图**接口名**
  2. `value` 开关的语义：on_true ← 4 步 / cfg 1，on_false ← 40 步 / cfg 4（快档 vs 慢档）
  3. 转换：8 个 SaveImage / 8 个 KSampler / 8 条正向提示词 / 193 个节点；`--only` 真旁路
  4. 参数落图：`--angle` 改对子图、前后缀应用到 8 条、`--output-prefix` 重写 8 个前缀且不重名
  5. 种子：8 个 KSampler 依次拿到 seed..seed+7；`validate()` 能抓出重名等故障（负向对照）

用法：python3 scripts/test_skill.py      （退出码 0 = 全部通过）
"""
from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import comfyui_angles as A  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []

EXPECTED_KEYS = ["close_up", "45_right", "aerial_view", "wide_shot",
                 "90_right", "low_angle", "90_left", "45_left"]
EXPECTED_PROMPTS = ["Turn the camera to a close-up.",
                    "Rotate the camera 45 degrees to the right.",
                    "Turn the camera to an aerial view.",
                    "Turn the camera to a wide-angle lens.",
                    "Rotate the camera 90 degrees to the right.",
                    "Turn the camera to a low-angle view.",
                    "Rotate the camera 90 degrees to the left.",
                    "Rotate the camera 45 degrees to the left."]
PARENT_INPUTS = ["image", "value", "unet_name", "clip_name", "vae_name",
                 "lora_name", "lora_name_1", "lora_name_1_1"]
CHILD_INPUTS = ["image", "image2", "image3", "prompt", "value", "unet_name",
                "clip_name", "vae_name", "lora_name", "lora_name_1"]
ASSET_SHA12 = "3552237b001d"


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(ok), "" if ok else str(detail)))


def load() -> dict:
    return json.load(open(A.DEFAULT_WORKFLOW, encoding="utf-8"))


def graph(*, only=None, fast=None, angles=None, prefix=None, output_prefix=None,
          image="ref.png", affix=None) -> tuple[dict, dict]:
    """走一遍与 generate() 相同的 UI 流水线（不联网），返回 (api, report)。"""
    ui = load()
    table = A.angle_table(ui)
    sel = list({r["key"] for r in table}) if only is None else only
    A.apply_angle_prompts(ui, table, angles or {},
                          prefix=(affix or ("", ""))[0], suffix=(affix or ("", ""))[1])
    if output_prefix:
        A.apply_output_prefix(ui, table, output_prefix)
    A.apply_only(ui, table, sel)
    if fast is not None:
        A.set_fast_mode(ui, fast)
    A.set_load_image(ui, image)
    flat = A.flatten_parent(ui)
    api, _w, rep = A.build_api(flat)
    A.prune_unreachable(api)
    return api, rep


# --------------------------------------------------------------------------- 1
def test_anatomy() -> None:
    raw = open(A.DEFAULT_WORKFLOW, "rb").read()
    check("资产 sha256 前缀固定（换了工作流必须同步改脚本与测试）",
          hashlib.sha256(raw).hexdigest().startswith(ASSET_SHA12),
          hashlib.sha256(raw).hexdigest()[:12])
    ui = load()
    table = A.angle_table(ui)
    check("角度表 8 行", len(table) == 8, len(table))
    check("角度键与顺序不变", [r["key"] for r in table] == EXPECTED_KEYS, [r["key"] for r in table])
    check("8 条角度提示词原文不变",
          [r["prompt"] for r in table] == EXPECTED_PROMPTS, [r["prompt"] for r in table])
    check("槽位即顺序（slot 0..7）", [r["slot"] for r in table] == list(range(8)), [r["slot"] for r in table])
    check("输出节点 8 个且互不相同",
          len({r["save_id"] for r in table}) == 8 and all(r["save_class"] == "SaveImage" for r in table))
    check("输出前缀唯一（官方模板里 45_right/90_right 曾是重名，本技能已修正）",
          len({r["prefix"] for r in table}) == 8, [r["prefix"] for r in table])

    inst = A.parent_instance(ui)
    sg = A._subgraph(ui, inst["type"]) or {}
    check("父图名不变", sg.get("name") == A.PARENT_NAME, sg.get("name"))
    check("父图接口名与顺序不变",
          [i.get("name") for i in (sg.get("inputs") or [])] == PARENT_INPUTS,
          [i.get("name") for i in (sg.get("inputs") or [])])
    kids = [n for n in sg.get("nodes") or [] if n.get("type") in A._subgraph_ids(ui)]
    check("父图内正好 8 个子图实例", len(kids) == 8, len(kids))
    kid_def = A._subgraph(ui, kids[0]["type"]) or {}
    check("子图名不变", kid_def.get("name") == A.EDIT_NAME, kid_def.get("name"))
    check("子图接口名与顺序不变",
          [i.get("name") for i in (kid_def.get("inputs") or [])] == CHILD_INPUTS,
          [i.get("name") for i in (kid_def.get("inputs") or [])])


def test_switch_semantics() -> None:
    """value=True = 快档（4 步 / cfg 1），False = 慢档（40 步 / cfg 4）。"""
    ui = load()
    inst = A.parent_instance(ui)
    check("模板默认 value=True（快档）",
          (inst.get("widgets_values_named") or {}).get("value") is True,
          (inst.get("widgets_values_named") or {}).get("value"))
    sg = A._subgraph(ui, inst["type"]) or {}
    kid_def = A._subgraph(ui, sg["nodes"][0]["type"]) or {}
    nodes = {n["id"]: n for n in kid_def["nodes"]}
    steps = [n for n in kid_def["nodes"] if n.get("type") == "ComfySwitchNode"
             and n.get("title") == "Switch (Steps)"]
    cfg = [n for n in kid_def["nodes"] if n.get("type") == "ComfySwitchNode"
           and n.get("title") == "Switch (CFG)"]
    check("子图里 Steps / CFG 各有一个开关", len(steps) == 1 and len(cfg) == 1)
    if steps and cfg:
        ints = {n["id"]: (n.get("widgets_values_named") or {}).get("value")
                for n in kid_def["nodes"] if n.get("type") == "PrimitiveInt"}
        floats = {n["id"]: (n.get("widgets_values_named") or {}).get("value")
                  for n in kid_def["nodes"] if n.get("type") == "PrimitiveFloat"}
        inl = {l.get("id"): l for l in kid_def.get("links") or [] if isinstance(l, dict)}

        def ends(sw):
            out = {}
            for inp in sw.get("inputs") or []:
                src = inl.get(inp.get("link"))
                if src:
                    out[inp.get("name")] = src.get("origin_id")
            return out
        se, ce = ends(steps[0]), ends(cfg[0])
        check("Steps: on_true=4 / on_false=40",
              ints.get(se.get("on_true")) == 4 and ints.get(se.get("on_false")) == 40,
              (ints.get(se.get("on_true")), ints.get(se.get("on_false"))))
        check("CFG: on_true=1 / on_false=4",
              floats.get(ce.get("on_true")) == 1 and floats.get(ce.get("on_false")) == 4,
              (floats.get(ce.get("on_true")), floats.get(ce.get("on_false"))))
        check("两个开关都有 switch 输入（由子图 value 接口驱动）",
              all(any(i.get("name") == "switch" for i in (n.get("inputs") or []))
                  for n in (steps[0], cfg[0])))
    check("子图内部 24 个节点不变", len(kid_def.get("nodes") or []) == 24, len(kid_def.get("nodes")))
    iface = [i for i in kid_def.get("inputs") or [] if i.get("name") == "value"]
    inl2 = {l.get("id"): l for l in kid_def.get("links") or [] if isinstance(l, dict)}
    tgt = None
    for lid in (iface[0].get("linkIds") or []) if iface else []:
        l = inl2.get(lid)
        if l:
            tgt = {n["id"]: n["type"] for n in kid_def["nodes"]}.get(l.get("target_id"))
    check("子图 value 接口在 UI 里确实接到 PrimitiveBoolean（链是通的）", tgt == "PrimitiveBoolean", tgt)

    # 钉住两个"必须摊平"的实测事实（否则整套图是坏的）
    naive, _w, _r = A.build_api(load())
    check("两级嵌套直接转换：8 条输出连线悬空（所以必须先摊平父图）",
          len(A.dangling_links(naive)) == 8, len(A.dangling_links(naive)))
    check("两级嵌套直接转换：参考图根本没进模型（FluxKontextImageScale.image 为 None）",
          all(n["inputs"].get("image") is None for n in naive.values()
              if n.get("class_type") == "FluxKontextImageScale"))


# --------------------------------------------------------------------------- 3
def test_conversion() -> None:
    api, rep = graph()
    check("摊平+转换：无未落图参数", rep.get("applied") == [] and rep.get("unapplied") == {}, rep)
    check("摊平+转换：193 个节点", len(api) == 193, len(api))
    check("摊平+转换：0 条悬空连线", A.dangling_links(api) == [], A.dangling_links(api)[:3])
    pairs = A.save_pairs(api)
    check("摊平+转换：8 个 SaveImage 且前缀唯一",
          len(pairs) == 8 and len({p for _, p in pairs}) == 8, pairs)
    check("摊平+转换：8 个 KSampler",
          sum(1 for n in api.values() if n.get("class_type") == "KSampler") == 8)
    prompts = [n["inputs"]["prompt"] for n in api.values()
               if n.get("class_type") == "TextEncodeQwenImageEditPlus"
               and isinstance(n["inputs"].get("prompt"), str) and n["inputs"]["prompt"].strip()]
    check("摊平+转换：8 条正向提示词", len(prompts) == 8, len(prompts))
    check("8 条提示词与角度表一致", sorted(p.strip() for p in prompts) == sorted(EXPECTED_PROMPTS))
    refs = [1 for n in api.values() for k, v in (n.get("inputs") or {}).items()
            if isinstance(v, list) and str(v[0]) == "25"]
    check("参考图（LoadImage #25）被 8 个角度各自引用", len(refs) == 8, len(refs))
    check("FluxKontextImageScale 的输入指向 LoadImage",
          all(n["inputs"].get("image") == ["25", 0] for n in api.values()
              if n.get("class_type") == "FluxKontextImageScale"))
    check("默认不带 image2/image3 输入（子图内为可选输入）",
          not any("image2" in n["inputs"] for n in api.values()
                  if n.get("class_type") == "TextEncodeQwenImageEditPlus"))
    lora = sorted({n["inputs"].get("lora_name") for n in api.values()
                   if n.get("class_type") == "LoraLoaderModelOnly"})
    check("两种 LoRA 各 8 份（Lightning + multiple-angles）",
          lora == sorted(["Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors",
                          "qwen-image-edit-2511-multiple-angles-lora.safetensors"]), lora)

    api2, _rep2 = graph(only=["45_right", "90_right"])
    check("--only 旁路：只剩 2 个输出", len(A.save_pairs(api2)) == 2, A.save_pairs(api2))
    check("--only：保留的正是选中的两个角度（按节点 id 认，不靠前缀）",
          sorted(p.replace("ComfyUI-", "") for _, p in A.save_pairs(api2)) == ["45_right", "90_right"],
          A.save_pairs(api2))
    check("--only：未选角度的分支被剪掉（真省时间）",
          sum(1 for n in api2.values() if n.get("class_type") == "KSampler") == 2
          and len(api2) < 60,
          (sum(1 for n in api2.values() if n.get("class_type") == "KSampler"), len(api2)))
    check("--only：仍然 0 悬空连线", A.dangling_links(api2) == [])

    # 快/慢档
    ui3 = load()
    touched = A.set_fast_mode(ui3, False)
    check("--no-fast 触及 8 个子图实例", len(touched) == 8, touched)
    flat3 = A.flatten_parent(ui3)
    api3, _w3, _r3 = A.build_api(flat3)
    pbs = [n["inputs"].get("value") for n in api3.values() if n.get("class_type") == "PrimitiveBoolean"]
    check("--no-fast 后 8 个 PrimitiveBoolean 全为 False", len(pbs) == 8 and set(pbs) == {False}, pbs)
    api4, _rep4 = graph(fast=True)
    pbs4 = [n["inputs"].get("value") for n in api4.values() if n.get("class_type") == "PrimitiveBoolean"]
    check("--fast 后 8 个 PrimitiveBoolean 全为 True", len(pbs4) == 8 and set(pbs4) == {True}, pbs4)
    check("快/慢两档真的产出不同的图",
          json.dumps(api3, sort_keys=True) != json.dumps(api4, sort_keys=True))


# --------------------------------------------------------------------------- 4
def test_param_landing() -> None:
    api, rep = graph()
    check("A. 无参数时提示词原样", rep.get("applied") == [])

    api2, _rep2 = graph(angles={"close_up": "Turn the camera to an extreme close-up."},
                        affix=("Keep the outfit identical.", "No distortion."))
    prompts = sorted(n["inputs"]["prompt"] for n in api2.values()
                     if n.get("class_type") == "TextEncodeQwenImageEditPlus"
                     and isinstance(n["inputs"].get("prompt"), str) and n["inputs"]["prompt"].strip())
    check("--angle 改写落到对应角度",
          "Keep the outfit identical. Turn the camera to an extreme close-up. No distortion." in prompts,
          prompts[:2])
    check("前后缀应用到全部 8 条",
          all(p.startswith("Keep the outfit identical.") and p.endswith("No distortion.")
              for p in prompts), prompts[:1])

    api3, _rep3 = graph(output_prefix="jwh/r1")
    pre = sorted(p for _, p in A.save_pairs(api3))
    check("--output-prefix 重写 8 个前缀", all(p.startswith("jwh/r1/") for p in pre), pre)
    check("重写后仍不重名", len(set(pre)) == 8, pre)

    api4, _rep4 = graph(image="uploaded-ref.png")
    imgs = [n["inputs"].get("image") for n in api4.values() if n.get("class_type") == "LoadImage"]
    check("LoadImage 指向新图", imgs == ["uploaded-ref.png"], imgs)

    seeds = A.set_seeds(api, 1000)
    check("8 个 KSampler 依次取 seed..seed+7", seeds == list(range(1000, 1008)), seeds)
    got = sorted(n["inputs"]["seed"] for n in api.values() if n.get("class_type") == "KSampler")
    check("种子确实写进图里", got == list(range(1000, 1008)), got)


# --------------------------------------------------------------------------- 5
def _raises(fn) -> bool:
    try:
        fn()
    except ValueError:
        return True
    except Exception:  # noqa: BLE001
        return False
    return False


def test_validation_negative_controls() -> None:
    api, rep = graph()
    check("正常图：validate 无问题", A.validate(api, 8, rep) == [], A.validate(api, 8, rep))
    check("期望值不符时报错", any("期望" in p for p in A.validate(api, 4, rep)),
          A.validate(api, 4, rep))

    dup = copy.deepcopy(api)
    saves = [nid for nid, n in dup.items() if n.get("class_type") == "SaveImage"]
    dup[saves[1]]["inputs"]["filename_prefix"] = dup[saves[0]]["inputs"]["filename_prefix"]
    check("输出重名会被抓出来", any("重名" in p for p in A.validate(dup, 8, {})),
          A.validate(dup, 8, {}))

    hang = copy.deepcopy(api)
    next(iter(hang.values()))["inputs"]["model"] = ["999999", 0]
    check("悬空连线会被抓出来（提交必失败的那类）",
          any("图外" in p for p in A.validate(hang, 8, {})), A.validate(hang, 8, {}))

    bad = copy.deepcopy(api)
    for n in bad.values():
        if n.get("class_type") == "TextEncodeQwenImageEditPlus" and n["inputs"].get("prompt", "").strip():
            n["inputs"]["prompt"] = "   "
    check("提示词被清空会被抓出来", any("正向编码" in p for p in A.validate(bad, 8, {})),
          A.validate(bad, 8, {}))

    check("--angle 里给不存在的角度会报错", _raises(lambda: A.generate(
        image_name="x.png", angles={"没这个角度": "x"}, plan=True)))
    check("--only 里给不存在的角度会报错", _raises(lambda: A.generate(
        image_name="x.png", only=["nope"], plan=True)))
    check("不给图会报错", _raises(lambda: A.generate(plan=True)))


# --------------------------------------------------------------------------- 6
def test_describe_and_cli() -> None:
    desc = A.describe(load())
    check("--list：8 个角度", desc["angle_count"] == 8 and len(desc["angles"]) == 8)
    check("--list：5 个模型文件（loras 两个不合并）", len(desc["models"]) == 5, desc["models"])
    check("--list：说明 value 开关的两档语义",
          "value" in desc["switch"]["interface"] and desc["switch"]["current"] is True
          and "where" in desc["switch"])
    check("--list：快档 ETA 按 8 张 ≈ 5 分钟给", 280 <= desc["eta_fast_s"] <= 320, desc["eta_fast_s"])
    check("--list：慢档 ETA 按实测 576 s/张 给（8 张 ≈ 76 分钟）",
          desc["eta_slow_s"] >= 4500, desc["eta_slow_s"])
    check("慢/快 ETA 比 ≈ 16×", 14 <= desc["eta_slow_s"] / desc["eta_fast_s"] <= 18,
          desc["eta_slow_s"] / desc["eta_fast_s"])

    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        code = A.main(["--list"])
    finally:
        sys.stdout = old
    out = json.loads(buf.getvalue())
    check("CLI --list 退出 0 且输出 JSON", code == 0 and out["angle_count"] == 8, out.get("angle_count"))

    buf = io.StringIO()
    sys.stdout = buf
    try:
        code = A.main(["--plan"])          # 不给图 → 参数错误
    finally:
        sys.stdout = old
    check("CLI 不给图 → 退出 2", code == A.EXIT_BAD_PARAMS, code)

    buf = io.StringIO()
    sys.stdout = buf
    try:
        code = A.main(["--image", "x.png", "--plan"])
        payload = json.loads(buf.getvalue())
    finally:
        sys.stdout = old
    check("CLI --plan 不出网也能给出 8 个输出与 ETA",
          code == 0 and len(payload["outputs"]) == 8 and payload["eta_s"] >= 280,
          (code, payload.get("eta_s")))
    check("--plan 明确不提交（无 prompt_id）", "prompt_id" not in payload)
    check("--plan 的输入图是占位符（没有真的上传）",
          payload["input_image"] == "<plan:x.png>", payload["input_image"])


def main() -> int:
    for label, fn in (("工作流解剖", test_anatomy), ("value 开关语义", test_switch_semantics),
                      ("转换（含 --only 旁路）", test_conversion), ("参数落图", test_param_landing),
                      ("校验负向对照", test_validation_negative_controls),
                      ("--list / CLI", test_describe_and_cli)):
        before = len(RESULTS)
        fn()
        print(f"{label}: {'OK' if all(ok for _, ok, _ in RESULTS[before:]) else 'FAILED'}")
    failed = [(n, d) for n, ok, d in RESULTS if not ok]
    for name, detail in failed:
        print(f"  FAIL: {name}" + (f"  -> {detail}" if detail else ""))
    print(f"{len(RESULTS) - len(failed)}/{len(RESULTS)} checks passed")
    print("RESULT: " + ("PASS" if not failed else "FAIL"))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
