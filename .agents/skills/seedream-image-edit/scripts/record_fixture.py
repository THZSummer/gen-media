#!/usr/bin/env python3
"""重新录制"真机接受的 API 图"（references/accepted-api-graph.json）—— 不花钱。

为什么需要这个脚本：离线自检 `test_skill.py` 会拿 `references/accepted-api-graph.json`
当基准逐字节比对，这份基准的价值全在"这张图**真的被服务器收下过**"。ComfyUI 升级、节点
schema 变化、工作流重导之后要重新录，所以留一个可重跑的入口。

怎么做到不花钱：故意用一张**无效的 API Key** 提交。ComfyUI 先在 /prompt 阶段做图形状校验
（形状不对立刻 400，比如前端专有节点 `missing_node_type`、参考图输入名写错
`Required input is missing`），校验通过才进执行阶段；执行阶段因为 key 无效报
`Unauthorized`。于是 **HTTP 200 + Unauthorized** 恰好证明"图形状合法"，而云端模型**一次
都没被调用**。本脚本也**不接受任何真凭据**，避免哪天手滑真的付了钱。

    python3 scripts/record_fixture.py                    # 用工作流自带的默认值录
    python3 scripts/record_fixture.py --prompt "把背景换成纯白"
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared  # noqa: E402

_shared.ensure()
import seedream_api as A  # noqa: E402
import seedream_gen as G  # noqa: E402
import seedream_edit as E  # noqa: E402
from seedream_edit_graph import auto_size, build_edit_graph, default_model, image_size  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.normpath(os.path.join(HERE, "..", "references",
                                            "accepted-api-graph.json"))
BOGUS_KEY = "deliberately-invalid-key-shape-probe"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=G.DEFAULT_SERVER)
    ap.add_argument("--workflow", default=E.DEFAULT_WORKFLOW)
    ap.add_argument("--node-info", default=E.DEFAULT_NODE_INFO)
    ap.add_argument("--ref", required=True, help="底图（本地路径，会先上传）")
    ap.add_argument("--annotate", help="标注层（本地路径，会先上传；给了就走 Painter 支路）")
    ap.add_argument("--prompt", default="把红框标出的区域改成纯黑")
    ap.add_argument("--prefix", default=E.DEFAULT_PREFIX)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--timeout", type=float, default=300.0)
    args = ap.parse_args(argv)

    info = A.load_node_info(args.node_info)
    ui = A.load_workflow(args.workflow)
    model = default_model(ui)
    ref_size = image_size(args.ref)
    auto = auto_size(info, model, *ref_size)

    ref_name = E.upload_image(args.server, args.ref)
    annotate_name = E.upload_image(args.server, args.annotate) if args.annotate else None
    print(f"uploaded: {args.ref} -> {ref_name}")
    if annotate_name:
        print(f"uploaded: {args.annotate} -> {annotate_name}")

    api, save_id, meta = build_edit_graph(ui, [ref_name], annotate_name, base_size=ref_size)
    api, report = A.apply_params(api, {
        "prompt": args.prompt, "size": auto["preset"], "filename_prefix": args.prefix,
    }, info)
    problems = A.validate_graph(api, info)
    if problems:
        print("本地 schema 校验没过：\n  - " + "\n  - ".join(problems), file=sys.stderr)
        return 1

    prompt_id = G.queue_prompt(args.server, api, "dsh-seedream-edit-fixture",
                               {"present": True, "channel": "api_key", "value": BOGUS_KEY})
    print(f"queued: {prompt_id}（凭据**故意无效**：只会证形状，不会出图）")
    entry = G.wait_for_history(args.server, prompt_id, timeout=args.timeout)
    errs = G.execution_errors(entry)
    first = errs[0] if errs else {}
    message = str(first.get("exception_message") or "")
    if "Unauthorized" not in message and "login" not in message.lower():
        print(f"预期是 Unauthorized，实际是：{message!r}\n"
              "（图形状可能被服务器拒了，或凭据通道有变；先看 /history 全文）", file=sys.stderr)
        return 1
    health = G.check_server(args.server)
    fixture = {
        "_what": ("seedream-image-edit 的离线自检基准：这份 /prompt API 图被真机**收下过**"
                  "（HTTP 200），只在执行阶段因凭据无效而止步。"),
        "_how": "python3 scripts/record_fixture.py --ref <底图> [--annotate <标注层>]",
        "_probe": {
            "time": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "server": args.server,
            "comfyui_version": (health["stats"].get("system") or {}).get("comfyui_version"),
            "http_status": 200,
            "status_str": (entry.get("status") or {}).get("status_str"),
            "error_node": first.get("node_type"),
            "execution_error": message,
            "credential": f"{BOGUS_KEY}（故意无效；鉴权失败 = 云端模型一次都没被调用）",
            "workflow_sha256": hashlib.sha256(
                open(args.workflow, "rb").read()).hexdigest(),
            "ref_size": list(ref_size),
            "size_auto": auto["preset"],
            "prompt": args.prompt,
            "prefix": args.prefix,
            "annotate": bool(annotate_name),
            "uploaded": {"ref": ref_name, "annotate": annotate_name},
            "dropped": meta["dropped"],
            "ref_keys": ["model.images.image_1"],
        },
        "graph": api,
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(fixture, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"written: {args.out}（save_node={save_id}, applied={report['applied']}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
