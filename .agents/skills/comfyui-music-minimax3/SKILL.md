---
name: comfyui-music-minimax3
description: 通过 HTTP API 调用远程 ComfyUI（默认 http://192.168.3.5:18000）跑 MiniMax Music 3 文生音乐（caption + lyrics → mp3，最长约 300 s；开放权重、无 API 计费）：把 UI 工作流的 "Text to Music (MiniMax Music 3)" 子图转成 /prompt API 格式（8 个子图接口：caption / lyrics / max_duration / seed / unet_name / clip_name / vae_name / tiled_decode 开关），提交排队、轮询 /history、从 /view 下载音频并留档（api.json + requests.jsonl）。**很慢：真机实测 60 s 音频 ≈ 1000 s 墙钟（≈16.7 s 墙钟 / 1 s 音频），20 s 约 5–6 分钟**，脚本在提交前先报 ETA。触发词：MiniMax Music 3、minimax_music3、music3、文生音乐、生成音乐、AI 作曲、BGM 生成、配乐生成、背景音乐、18000、192.168.3.5。
whenToUse: 当用户要生成音乐/纯音乐/BGM（尤其给图文或短视频配乐）、要按 caption+lyrics 控制曲式与时长、或要脚本化批量出音频时使用。要人声朗读/配音用 TTS（见 methods/text-to-speech）；要"视频自带同步音效"用 text-to-video-fastvideo3；要云端付费视频用 methods/text-to-video。
---

# ComfyUI 文生音乐（MiniMax Music 3 · 开放权重）

**用途**：给一段**结构化 caption**（+ 可选歌词）出**一整条音频**。全程走 HTTP API，可脚本化、可复现（固定 seed）。
模型跑在远端 ComfyUI 所在机器上（权重约 13.4 GB：DiT 4.58 GB + 文本编码器 8.57 GB + 音频 VAE 0.21 GB），**没有 API 计费**，代价是墙钟时间。

- 默认服务器：`http://192.168.3.5:18000`（`--server` 或 `$COMFYUI_SERVER` 覆盖）
- 工作流：`assets/audio_minimax_music_3.json`（ComfyUI 官方模板 "Text to Music (MiniMax Music 3)"，sha256 前缀 `841b9320ec6e`）
- 参数档：`assets/audio_minimax_music_3.profile.json`（接口名 → 图内节点/字段的映射）

---

## 前置检查

```sh
# ① 离线自检：43 项断言（接口未改名 / 参数落图 / 时长单旋钮 / --set / 音频键 / mock 全往返）
python3 scripts/test_skill.py

# ② 真机自检（免费、不占 GPU）：三个权重 + 七个节点在不在
python3 scripts/comfyui_music.py --check
# → {"ok": true, "missing_models": [], "missing_nodes": [], "hint": null}

# ③ 看工作流暴露的参数与默认值
python3 scripts/comfyui_music.py --list

# ④ 出完音频后：人声（词）核查 —— 把"是不是纯音乐"变成可复现的数字（免费、离线）
python3 scripts/check_vocals.py out/my-bgm.mp3 \
    --control ../../../../projects/tea-shake-dance/out/video/tea_shake_narrated.mp4
```

> `check_vocals.py` 需要 `vosk` + 一个模型目录（默认 `~/.cache/vosk/vosk-model-small-cn-0.22`，
> 用 `--model` / `$VOSK_MODEL` 覆盖）；缺依赖时以 `SKIPPED_NO_VOSK*` 退出，**不假装通过**。
> 它**不进 `check.sh`**：模型路径是机器相关的，属"每条音频人工决定"的检查（与付费矩阵同类）。

## ⏱️ 成本：真机实测 ≈ 16.7 s 墙钟 / 1 s 音频

| 想要的时长 | 预计墙钟 | 说明 |
|-----------|---------|------|
| 15 s | ~250 s（4 分钟） | 图文 BGM 循环的最短可用档 |
| 20 s | ~334 s（5.5 分钟） | 单人旁白型短视频够用（**实测 315 s**） |
| 60 s | ~1000 s（17 分钟） | 用户实测基准点 |
| 120 s | ~33 分钟 | 完整歌曲，慎用 |
| 300 s | ~84 分钟 | 模型上限附近，不建议 |

> 基准环境：RTX 4060 Ti 8 GB + `minimax_music3_dit_fp16` + 30 步 + tiled decode。
> `--eta` 默认开启，**提交前**会打印估算；`--duration` 是唯一成本旋钮，**按"最短够用"要**。
> 实测短档比估算更快（20 s 实测 15.77 s/音频秒）——**ETA 是上界，不是承诺**。

## 执行

```sh
# ① 先免费验证参数真的落图（不提交、不占 GPU）—— 养成习惯，别用真机试参
python3 scripts/comfyui_music.py --caption-file bgm.txt --instrumental --duration 20 --plan

# ② 正式生成（20 s ≈ 5.5 分钟）
python3 scripts/comfyui_music.py --caption-file bgm.txt --instrumental --duration 20 \
    --seed 6611 --filename-prefix audio/jwh-bgm-r1 --out-dir out/

# ③ 有歌词的歌（不是 BGM）
python3 scripts/comfyui_music.py --caption-file song.txt --lyrics-file lyrics.txt \
    --duration 120 --seed 42

# ④ 低显存/高显存切换
python3 scripts/comfyui_music.py --caption-file bgm.txt --instrumental --duration 20 --no-tiled

# ⑤ 兜底：改任何 profile 没命名的字段
python3 scripts/comfyui_music.py --caption-file bgm.txt --instrumental --duration 20 \
    --set KSampler.denoise=0.9 --set SaveAudioAdvanced.format=flac
```

## 参数

| 参数 | 落点 | 默认（模板） | 说明 |
|------|------|-------------|------|
| `--caption` / `--caption-file` | `MiniMaxMusic3TextEncode.caption` | — | **必填**（一次出片很贵，刻意不给默认） |
| `--lyrics` / `--lyrics-file` / `--instrumental` | `MiniMaxMusic3TextEncode.lyrics` | 空 | `--instrumental` 写入 `[intro]/[instrumental]/[outro]` |
| `--duration` / `--seconds` | `MiniMaxMusic3TextEncode.max_duration` | 60 | 经 FLOAT 链路同步到 `EmptyMiniMaxMusic3LatentAudio.seconds`（**唯一的时长旋钮**） |
| `--seed` | `SeedNode.seed` | 随机 | 同时供给文本编码与采样器，固定即复现 |
| `--steps` | `KSampler.steps` | 30 | |
| `--cfg-scale` | `MiniMaxMusic3TextEncode.cfg_scale` | 1.7 | 给了它也会把 `KSampler.cfg` 一起钉住（两处本应同步） |
| `--sampler-cfg` | `KSampler.cfg` | 1.7 | 想单独调采样器 cfg 时用 |
| `--top-k` | `MiniMaxMusic3TextEncode.top_k` | 50 | |
| `--sampler` / `--scheduler` / `--denoise` | `KSampler` | euler / simple / 1.0 | |
| `--tiled` / `--no-tiled` | `ComfySwitchNode.switch` | **on** | tiled 解码省显存、略慢、接缝有极小风险 |
| `--tile-size` / `--overlap` | `VAEDecodeAudioTiled` | 1536 / 64 | |
| `--filename-prefix` | `SaveAudioAdvanced.filename_prefix` | `audio/audio_minimax_music3` | 服务端子目录也由它决定 |
| `--unet-name` / `--clip-name` / `--vae-name` | 三个 loader | 见 profile | 换 int8 DiT 等变体时用 |
| `--set CLASS.FIELD=VALUE` | 任意 | — | 未命名字段的兜底（可重复） |
| `--plan` / `--check` / `--list` | — | — | 免费：出图前验证 / 查依赖 / 看默认值 |

## UI→API 转换的三个约定

1. **时长只有一个旋钮**。模板把 `MiniMaxMusic3TextEncode.max_duration` 的第二路输出（FLOAT）接到了 `EmptyMiniMaxMusic3LatentAudio.seconds`。所以**不要**去改 latent 的 seconds——改 `--duration` 即可，两处自动一致（`test_skill.py` 断言这条连线还在，防止模板更新后静默断掉）。
2. **`--instrumental` 只改 lyrics**。不给人声这件事靠 caption 里显式写 `no vocals` 更可靠（负向写法见 `references/caption-templates.md`），但**模型行为不是保证，交付前必须试听**。
3. **`MarkdownNote` 之类的前端专有节点必须被剔掉**。本技能的转换复用共享引擎的 `NON_EXECUTABLE_TYPES`；`test_skill.py` 断言产物里不含 note 节点。

> 顺带记录一条共享引擎的改动：`comfyui_convert.OUTPUT_NODE_CLASSES` 增加了 `SaveAudioAdvanced`——
> 原先只认 `SaveImage / SaveVideo / SaveWEBM / SaveAudio`，音频模板会被判成"没有输出节点"。
> 影响面：仅新增一个类名，其余技能的工作流不含它（各自 mock 自检已复跑通过）。

## 输出与留档

产物落到 `--out-dir`（默认 `out/`），包含：

- `*.mp3`（SaveAudioAdvanced 写出，模板默认 `mp3 / V0`；要 flac 用 `--set SaveAudioAdvanced.format=flac`）
- `<prefix>.api.json` —— 实际提交的 API 图，可原样重投
- `requests.jsonl` —— 一行一次请求：engine=`minimax-music3-t2m`、caption / lyrics、seed、duration、**eta_s 与 elapsed_s**、音频探测（时长/采样率/码率/字节）、prompt_id、产物路径

音频参数由 `ffprobe` 探测（**可选依赖**：没有 ffprobe 也能跑，只是 `audio` 字段为 `null`）。

## 验证

```sh
python3 scripts/test_skill.py                      # 43 项离线断言（含 mock ComfyUI 全往返）
python3 scripts/comfyui_music.py --check           # 真机：权重 + 节点
python3 scripts/comfyui_music.py --caption "..." --instrumental --duration 20 --plan   # 免费
```

> 这个技能**不做**真机全参数矩阵：单次成本 4 分钟起（见上表），跑矩阵不划算。
> 三层替代：`test_skill.py` 覆盖转换与 HTTP 往返，`--plan` 覆盖参数落图，`--check` 覆盖真机依赖；
> 另外保留**一次真机出片**作为端到端证据，记录在下方"真机实测"。

**真机实测记录**（每次真机跑完追加一行，含日期 / 参数 / 墙钟 / 产物）：

| 日期 | 参数 | 墙钟 | 产物 | 结论 |
|------|------|------|------|------|
| 2026-10-07 | 模板 A 古琴 · `--instrumental --duration 20 --seed 6611`（steps 30 / cfg 1.7 / tiled on） | **315.2 s**（ETA 报 334 s） | `work/music-out/jwh-bgm-r1_00001.mp3` · 19.992 s · 44.1 kHz 立体声 · 243 kbps · 607,746 B · sha256 `029120167340…`（本地工作区，不入库） | ✅ 端到端跑通：`status=success`、无 warning、`unapplied_overrides={}`、输出节点 `35`。**实测 15.77 s 墙钟/音频秒，比 16.7 的 ETA 保守约 6%**；听感（是否真无词）仍需人耳验收 |

> 可复核证据：`references/verified-runs/2026-10-07-jwh-bgm-r1.json`（含参数、探测结果、mp3 sha256 与**实际提交的 API 图**，可原样重投）。

### 🎤 人声核查（`check_vocals.py`，2026-10-07 建立）

**动机**：`--instrumental` 只改 lyrics；caption 里写 `no vocals` 也只是措辞。所以"是不是纯音乐"必须**测**，不能靠感觉。

**做法**：用离线 vosk（中文小模型）跑 ASR，并在**同一次运行里**带一个已知有旁白的对照——对照识别不出词就说明"方法没生效"，本次检测作废（防止把"ASR 坏了"误读成"没人声"）。

**实测（2026-10-07）**：

| 音频 | 时长 | 识别词数 | 语音占比 | 结论 |
|------|------|---------|---------|------|
| `jiu-wei-hu-bgm.mp3`（本技能出的配乐） | 29.99 s | **0** | **0.00 %** | 未检出人声词 |
| `tea_shake_narrated.mp4`（对照：真有旁白） | 35.59 s | 46 | 53.2 % | 方法有效 ✅ |
| `butterfly_girl_v3_full.mp4`（对照：音乐/音效轨） | 51.04 s | 3（「啊 嘿嘿 姐姐」） | 2.6 % | **ASR 会在音乐上幻觉** ⚠️ |

**怎么用这个结果**：0 词是"纯音乐"的**强证据**，但不是绝对证明——
① ASR 认的是**词**，无词哼唱/气声可能 0 词；② 模型分语种（默认中文，英文歌词要换模型）；
③ 非 0 词要人耳复核，可能是幻觉（上表第三行就是）。
**所以流程是：ASR 0 词 + 人耳终判**，两者都过才算"纯音乐"。

## 已知限制

- **慢**：16.7 s 墙钟 / 1 s 音频是这台机器 + fp16 DiT + 30 步 + tiled 的成绩；换 int8 DiT / 减步数会变，但没人测过音质代价。
- **不做听感判定**：脚本只验证"有音频、时长对、可复现"，**好不好听必须人耳**。别把 ETA 和字节数当成验收通过。
- **纯音乐不是保证**：`--instrumental` 是提示词层面的约束。`check_vocals.py` 的 ASR 0 词是强证据，但认词不认无词哼唱（见上"人声核查"）。
- **模板会变**：节点接口名一旦被上游改动，`test_skill.py` 的接口断言会先失败——那是保护，不是故障。
- **许可**：开放权重 + MiniMax-Music3 COMMUNITY LICENSE，**商用前读许可原文**（见 `references/caption-templates.md` §六）。

## 修订记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-10-07 | v1.1 | **加人声核查 `scripts/check_vocals.py`**：离线 vosk + **同法对照**（对照识别不出词就判定方法失效），把"是不是纯音乐"变成数字；实测本技能出的 30 s 配乐 **0 词 / 语音占比 0.00%**，而旁白对照 46 词 / 53.2%，另一条音乐轨被幻觉出 3 词（2.6%）。三条限制（认词不认哼唱 / 分语种 / 会幻觉）写进 SKILL.md；不进 `check.sh`（机器相关依赖，属人工决定的检查） |
| 2026-10-07 | v1.0 | 建立：从用户提供的 `audio_minimax_music_3.json`（sha256 `841b9320ec6e…`）落位为技能；profile 打通 8 个子图接口；脚本支持 check/list/plan/生成 + 留档；离线自检 43 项；共享引擎补认 `SaveAudioAdvanced` 为输出节点；实测成本模型写进 `--eta` |
