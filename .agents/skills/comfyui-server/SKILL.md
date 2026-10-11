---
name: comfyui-server
description: 查 ComfyUI 服务器本身（默认 http://192.168.3.5:18000）——状态与版本、显存/队列、本机权重清单（/api/models）、节点类与参数 schema（/api/object_info）、官方模板目录（/templates/index.json，本机 598 个，可搜可拉）、`audit` 判断某模板/工作流在本机缺哪些权重或节点类、历史记录浏览与下载任意产物、userdata 已存工作流；写操作 interrupt / free / clear-queue / upload 一律要 --yes。**一步生成都不做**（出图/改图/出片/出音乐归各自生成技能）。触发词：ComfyUI 有哪些模板、有哪些模型/权重、有哪些节点、服务器状态、显存不够、谁在跑、队列、打断任务、审计工作流能不能跑、/object_info、/api/models、/templates、18000、192.168.3.5。
whenToUse: 当要"先看清楚再动手"——不知道本机有哪些权重/节点/模板、想拿官方模板当起点、想把某个工作流跑之前先确认缺不缺东西、要翻历史产物、或要处理 8 GB 显存被占满 / 队列卡住时使用。真要出图/改图/出片/出音乐，用 text-to-image-comfyui / image-edit-comfyui / image-to-video-fastvideo3 / text-to-video-fastvideo3 / comfyui-music-minimax3，不要用本技能。
---

# ComfyUI 服务器探查与运维（comfyui-server）

**用途**：把**服务器本身**当对象来查——有哪些权重、有哪些节点、官方模板目录里有什么、某个工作流**在本机能不能跑**、现在队列里谁在跑、某次运行的产物在哪。全程 HTTP API，**一步生成都不做**。

- 默认服务器：`http://192.168.3.5:18000`（`--server` 或 `$COMFYUI_SERVER` 覆盖）
- 只依赖 Python 标准库（`urllib`），不需要装任何东西

## 边界判据（为什么它不抢别人的活）

> **"这个功能在完全没有 prompt 的情况下还有意义吗？"**
> 有 → 归本技能；没有 → 归生成技能。

| 归本技能 | 不归本技能 |
|---|---|
| 状态 / 版本 / 显存 / 队列 | 出图、改图、控制图生图 |
| 权重、节点、模板**目录** | 出视频（t2v / i2v） |
| 工作流**能不能跑**（缺什么） | 出音乐 / BGM |
| 历史记录、产物下载、上传 | 把 UI 工作流转成 `/prompt` 图 |

最后一条要特别说明：**UI→API 转换不在本技能**，在 `text-to-image-comfyui` 的 `comfyui_convert.py`
（含 `UI_ONLY_CLASSES` 剔除）。本技能只负责"把它拉下来、告诉你缺什么"，然后交给生成技能。

---

## 前置检查

```sh
# ① 离线自检：起 mock ComfyUI 把每个 verb 跑一遍（64 项，不需要 GPU / 不需要真服务器）
python3 scripts/test_skill.py

# ② 真机自检（只读、零花费）：探活 + 目录/队列摘要
python3 scripts/comfyui_server.py --check
# → {"ok": true, "comfyui_version": "0.39.0", "model_files_total": 114, ...}
```

## 动词表

| verb | 做什么 | 写操作 |
|------|--------|:---:|
| `check` / `--check` | 探活 + 版本 + 模型文件数 + 队列数 | — |
| `status` | 版本、RAM、显存（vram/torch 两套）、队列、运行中 id | — |
| `models [--folder F] [--search KW]` | 本机权重文件（跨目录搜） | — |
| `nodes [--search KW]` / `nodes --class C` | 节点类清单 / 某个类吃哪些参数与枚举值 | — |
| `templates [--search] [--type] [--limit]` | 官方模板目录（本机 598 个） | — |
| `templates --pull NAME [--audit]` | 把模板 UI 工作流拉到 `out/templates/`（附 `.meta.json`） | 写本地 |
| `audit --template NAME` / `audit --workflow PATH` | 本机缺哪些权重/节点类、能不能跑 | — |
| `workflows [--dir] [--search]` | `/api/userdata` 里已存的 UI 工作流 | — |
| `history [--limit N]` | 运行记录（最近的在前） | — |
| `history --download ID [--out-dir]` | 下载某一次的全部产物（默认跳过 temp） | 写本地 |
| `queue` | 正在跑什么、排了多少 | — |
| `interrupt --yes` | 打断当前任务 | ✅ |
| `free --yes [--unload-models]` | 释放显存（默认只回收缓存，不卸权重） | ✅ |
| `clear-queue --yes` | 清空排队中的任务 | ✅ |
| `upload --file PATH [--subfolder]` | 上传文件到服务器 `input/` | ✅ |

**退出码**：`0` 正常 / `1` 失败（含服务器不可达、`audit` 判不可跑）/ `2` 用法错误 / `3` 写操作缺 `--yes`。
默认输出 JSON，`--format text` 给人看。

## 执行

```sh
# ① 先看清楚：这台机器上到底有什么
python3 scripts/comfyui_server.py status
python3 scripts/comfyui_server.py models --search minimax
python3 scripts/comfyui_server.py nodes --search upscale
python3 scripts/comfyui_server.py nodes --class KSampler          # 默认值/范围/枚举一并给出

# ② 模板当起点：搜 → 拉 → 审计（三步都不花钱）
python3 scripts/comfyui_server.py templates --type video --search fasth3
python3 scripts/comfyui_server.py templates --pull video_fastvideo_fasth3_i2v --audit
# → out/templates/video_fastvideo_fasth3_i2v.json（UI 工作流）+ .meta.json（来源/sha256/audit）

# ③ 跑之前先问"缺什么"（支持模板名，也支持本地工作流）
python3 scripts/comfyui_server.py audit --template image_z_image_turbo
python3 scripts/comfyui_server.py audit --workflow ../../image-edit-comfyui/assets/z-image-turbo-fun-union-controlnet.json
# → {"ok": true, "missing_models": [], "missing_nodes": [], "bypassed_models": [...]}; 不可跑时退出 1

# ④ 翻历史与产物（任意一次运行的图/音/视频都能捞回来）
python3 scripts/comfyui_server.py history --limit 10
python3 scripts/comfyui_server.py history --download <prompt_id> --out-dir out/

# ⑤ 8 GB 卡的日常：谁在占、要不要处理
python3 scripts/comfyui_server.py queue
python3 scripts/comfyui_server.py free --yes                     # 只回收缓存（安全）
python3 scripts/comfyui_server.py interrupt --yes                # 打断当前任务
python3 scripts/comfyui_server.py free --yes --unload-models     # 真卸权重（下次生成要重载）
```

## 真机实测（2026-10-11 生产轮）

| 项 | 实测 |
|---|---|
| 服务器 | ComfyUI `0.39.0` + 前端 `1.55.14` + templates `0.11.78`，RTX 4060 Ti 8 GB |
| 权重 | **114 个文件** / 11 个目录（`diffusion_models` 21、`loras` 16、`text_encoders` 11、`vae` 9、`checkpoints` 3、`model_patches` 1 …） |
| 节点类 | **980 个** |
| 官方模板 | **598 个**（image 282 / video 220 / 3d 43 / audio 33 / llm 20） |
| 本机可跑 | 抽查：`image_z_image_turbo` ✅、`..._fun_union_controlnet` ✅、`audio_minimax_music_3` ✅、`video_fastvideo_fasth3_i2v` ✅、`video_minimax_h3_i2v` ✅；反例 `image_qwen_image_edit_2511` ❌ 缺 `qwen_image_edit_2511_fp8mixed.safetensors`、`image_z_image` ❌ 缺 `z_image_bf16.safetensors`、`image_sdxl_simple` ❌ 缺 `sd_xl_base_1.0.safetensors`（`audit` 能准确点名） |
| 队列 | 第一次跑 `queue` 就发现**有一个 MiniMax H3 任务在跑**（这正是写操作要 `--yes` 的理由）；等它跑完再操作，`history` 确认这条 `success`，共 4 次成功记录 |
| 写操作 | 队列空时真机验证：`interrupt --yes` → `interrupted_running: 0`、`clear-queue --yes` → `cleared_pending: 0`、`free --yes` → 只回收缓存。三者都返回 `ok: true` |
| 产物下载 | `history --download <id>` 真机拉回 `MiniMax_H3_00008_.mp4`（3.68 MB / 10.1 s，`ffprobe` 核对） |
| 上传 | 真机上传 70 B 探针 PNG 成功，回报 `comfyui-server-selftest.png`（见下方"踩坑"第 5 条） |

**花费**：只读动词与 `audit` 全部**零成本**（不占 GPU、不提交任务）。写操作不产生任何按量计费，
但 `interrupt` / `clear-queue` 会**毁掉别人正在跑的任务**，所以护栏是硬性的——
本轮就是先 `queue` 看到有任务在跑，**等它自己跑完**才验证写操作。

## 踩坑点（都是实测踩出来的）

1. **`/api/workflow_templates` 是空的**：本机版本（0.39.0 + 前端 1.55.14）对这个新端点返回 `{}`。
   模板目录要用 **`/templates/index.json`**（753 KB，598 条），单条用 `/templates/<name>.json`。
2. **`audit` 必须按 `node.mode` 区分 active / bypass**：官方模板里常备着"另一条分支"的权重
   （int8 与非 int8 两套、或换 LoRA 的备选），默认是 bypass 状态。不区分就会把**能跑的模板误判成缺权重**
   ——实测 `image_z_image_turbo_fun_union_controlnet` 被误判过。bypass 引用的权重单独放在 `bypassed_models`。
3. **ControlNet 权重不在 `controlnet` 目录**：Z-Image 的 Fun Union ControlNet 走 `model_patches`
   （1 个文件），而 `/api/object_info` **不枚举**它的文件名。只查 `/object_info` 会漏，必须叠加
   `/api/models/<folder>` 全量目录。
4. **子图实例的 `type` 是子图 UUID**：实例节点 `type` == `definitions.subgraphs[].id`
   （实测三个官方模板都如此）。审计要先收这批 id，否则会把实例当成"缺节点类"。
   顺带：`definitions.subgraphs[*].nodes` **里面的节点也要扫**（`audit` 会走全图）。
5. **上传会留档、而且删不掉**：`/upload/image` 的字段名对图片/音频/视频**都叫 `image`**；
   文件落到服务器 `input/`，本机版本的 `/api/userdata/...?type=input` **没有删除接口**（实测 DELETE 返回 404）。
   自检留了一个 70 B 的 `comfyui-server-selftest.png` 在服务器 `input/`，无害但**别以为能清干净**。
6. **`free` 默认不卸权重**：`unload_models=false` 只回收缓存；真要在 8 GB 卡上腾地方得显式
   `--unload-models`，代价是下一次生成要重新加载权重（明显变慢）。
7. **探活要在干活之前**：所有动词（除 `--format`/用法错误外）先打 `/system_stats`，
   不可达立刻报错退出并给排查提示（ComfyUI 没启动 / `--listen` 没开 / 防火墙），**不吐 traceback**。

## 与其它技能的分工

| 想要什么 | 用哪个 |
|---|---|
| 看服务器有什么（权重/节点/模板/历史/队列） | **本技能** |
| 工作流能不能跑、缺什么 | **本技能** `audit` |
| 拉官方模板当起点 | **本技能** `templates --pull` |
| UI 工作流 → `/prompt` API 图 | [text-to-image-comfyui](../text-to-image-comfyui/SKILL.md) `comfyui_convert.py` |
| 文生图 / 控制图生图 | [text-to-image-comfyui](../text-to-image-comfyui/SKILL.md) / [image-edit-comfyui](../image-edit-comfyui/SKILL.md) |
| 云端付费出图与改图 | [seedream-text-to-image](../seedream-text-to-image/SKILL.md) / [seedream-image-edit](../seedream-image-edit/SKILL.md) |
| 文生视频 / 图生视频（带同步音频） | [text-to-video-fastvideo3](../text-to-video-fastvideo3/SKILL.md) / [image-to-video-fastvideo3](../image-to-video-fastvideo3/SKILL.md) |
| 文生音乐 / BGM | [comfyui-music-minimax3](../comfyui-music-minimax3/SKILL.md) |
| 拼版/比对/剥元数据 | [image-tools](../image-tools/SKILL.md) |

## 检查清单

- [ ] `python3 scripts/test_skill.py` → `64/64 checks passed` / `RESULT: PASS`
- [ ] `python3 scripts/comfyui_server.py --check` → `ok: true`
- [ ] 用 `status` 确认版本与显存；用 `queue` 确认**没有**别人正在跑，再考虑任何写操作
- [ ] `audit` 判 `ok: true` 只是"权重与节点都有"，**不代表参数语义正确**——最终仍要真机跑一次
- [ ] `templates --pull` / `history --download` 的默认落点是 `out/templates`、`out/history`，
      而**仓库的 `.gitignore` 只忽略 `work/`**：提交前 `git status` 确认没把拉下来的模板或产物一起加进去
- [ ] 写操作前问自己：这会不会毁掉一个正在跑的任务？`--yes` 不是形式
