# 生成方法总览（Methods）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[首页](../README.md) ｜ 项目实践见 [../projects/](../projects/README.md)

> 本篇是**技术方法手册**：按生成技术路径组织（**图片 / 视频 / 语音** + 横切控制），讲"**怎么生成**"。
> 具体项目（"**生成什么**"）见 [projects/](../projects/README.md)，一项目一目录，按需引用本篇方法。
> 工具入口：`arkcli +gen`（三步工作流：① `resources list` 查可用模型 -> ② `models get` 查 supported_params -> ③ `+gen` 生成）。
> 📚 **官方教程（seedance-2.0 多模态/音效/编辑用法）**：<https://ark.volcengine.com/region:cn-beijing/docs/82379/2298881?lang=zh>（含 @视频/@图像/@音频 参考输入、音效描述、视频延长编辑等官方示例，按需参考）

### seedance-2.0 多模态参考输入（2026-08-01 实测）

seedance-2.0 支持**多模态参考输入**（视频/图像/音频），正确用法：

```bash
MODEL="doubao-seedance-2-0-260128"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input "reference_image:@图1.jpg" \
  --input "reference_audio:@音频1.mp3" \
  --ratio 16:9 --resolution 480p --duration 5 \
  "参考@图像1中的人物形象和场景，生成……；背景音乐使用@音频1中的声音" --wait
```

**`--input` 角色前缀规则**（按出现顺序进入 content[]）：

| 前缀 | wire role | 说明 |
|------|-----------|------|
| `first:` | 首帧 | 视频任务第 1 张图默认首帧 |
| `last:` | 尾帧 | - |
| `ref:` | 简写，wire 不传 role | 服务端按位置推断（参考素材） |
| `reference_image:` | reference_image | ✅ 参考图（显式 role） |
| `reference_video:` | reference_video | ✅ 参考视频 |
| `reference_audio:` | reference_audio | ✅ 参考音频（**音频必须用这个前缀**） |

**实测踩坑**：
- ⛔ 音频参考必须用 `reference_audio:` 前缀（裸 `@音频` 报 "requires audio role to be reference_audio"）
- ⛔ `reference_audio` 不能是唯一参考（需搭配图/视频参考）
- ⛔ 首帧模式（I2V first frame）**不能与参考媒体混用**（"first/last frame content cannot be mixed with reference media content"）——多模态参考要走纯 T2V + reference_image/audio
- ⛔ `--generate-audio`（布尔）+ prompt 描述音效 → ❌ 生成的是极低音量无效音频（实测 RMS -30~-45dB 平缓无起伏）
- ⚠️ **`reference_audio` 参考输入反而使音频音量暴跌**（对照实测：传了 RMS -45~-65dB 几乎无声；**不传** RMS -25~-27dB 正常可听）——**结论：视频音效不要传 reference_audio，让模型按画面原生生成**（会自动配环境音/动作音，音量正常）
- ✅ **有效音频路径（2026-08-01 实测定版）**：**用 `--extra-body '{"generate_audio": true}'` 显式传请求体参数**（⚠️ `--generate-audio` flag 实测未正确映射到请求体，音频偏弱/不均匀；extra-body 版每秒 RMS 58-75 最响最匀）。prompt 里写"音画同步：环境音效匹配画面（风声、雨声…）"引导。
- prompt 中引用格式：`@音频1`（对应第 1 个音频参考）、`@图像1`、`@视频1`（按 --input 出现顺序编号）



---

## 一、为什么做这个规划

日常做视频生成时，常遇到以下问题：

- **不知道从哪条路径入手**：纯文字、给张图、给段参考视频、跟着音乐节奏、要配音——路径能力边界完全不同
- **参数乱传被拒**：分辨率、时长、优先级、草稿模式……不同模型支持范围不同，不查 `supported_params` 瞎猜必然失败
- **视频是异步的**：提交后返回 `task_id` + `queued`，很多人以为"失败了"就重提，结果建一堆重复任务
- **单条视频太短**：默认 5 秒，想做长内容/连续镜头需要续接策略
- **内容被审核拦截**：prompt 敏感、参考素材违规，`--force` 也绕不过，需要从源头调整
- **成本不可控**：1080p + 长时长 + 高优先级，单条成本可能数倍于草稿模式

### 规划目标

把生成从"碰运气式单次调用"变成**按媒体类型分主题的可复用规划**：

- 每个方法 = 一类技术路径，独立成册，按需取用
- 每册包含：能力映射、prompt 策略、参数选型、命令模板、踩坑点、检查清单
- 方法之间正交，可组合（如「文生图」+「图生视频」+「镜头运镜」+「长视频续接」+「语音合成」串成一条完整片子）
- 具体业务项目在 [projects/](../projects/README.md) 里按项目引用本篇方法

---

## 二、能力地图

Ark 生成能力按**输出媒体类型**分三类：**图片、视频、语音**；外加横切控制参数。

### 图片类（输出：静态图片）

| 路径 | 输入 | 典型场景 | 对应方法 |
|------|------|----------|----------|
| **文生图 T2I** | 仅 prompt | 分镜图、I2V 首帧、海报封面 | [text-to-image](text-to-image/README.md) |

### 视频类（输出：动态视频）

| 路径 | 输入 | 典型场景 | 对应方法 |
|------|------|----------|----------|
| **文生视频 T2V** | 仅 prompt | 从零构思画面、抽象概念可视化 | [text-to-video](text-to-video/README.md) |
| **图生视频 I2V** | 首帧 / 尾帧图 + prompt | 让静图动起来、关键帧驱动 | [image-to-video](image-to-video/README.md) |
| **参考视频 R2V** | 参考视频 + prompt | 运动迁移、风格保持、换主角 | [reference-video](reference-video/README.md) |
| **音频驱动** | 参考音频 + prompt | 卡点、节拍切换、蒙太奇 | [audio-driven](audio-driven/README.md) |

### 语音类（输出：语音音频）

| 路径 | 输入 | 典型场景 | 对应方法 |
|------|------|----------|----------|
| **语音合成 TTS** | 文本 | 后期配音、旁白、口播 | [text-to-speech](text-to-speech/README.md) |

### 横切控制（适用于所有类型）

| 维度 | 关键参数 / 能力 | 方法 |
|------|----------------|------|
| 镜头与运镜 | `--camera-fixed`、prompt 内运镜描述、分镜 | [cinematography](cinematography/README.md) |
| 质量与成本 | `--resolution` `--duration` `--frames` `--draft` `--priority` | [quality-and-cost](quality-and-cost/README.md) |
| 长视频续接 | `--return-last-frame` 链式串联、seed 复现 | [long-video-chain](long-video-chain/README.md) |
| 内容安全 | 审核拦截 subtype、prompt 调整、素材合规 | [content-safety](content-safety/README.md) |

---

## 三、方法导航

```
methods/
├── README.md                ← 你在这里（方法总览，按媒体类型分组）
│
├── 🖼️ 图片类
│   └── text-to-image/       文生图：分镜图/首帧/封面（seedream）
│
├── 🎬 视频类
│   ├── text-to-video/       文生视频：从文字到动态画面
│   ├── image-to-video/      图生视频：首帧/尾帧驱动
│   ├── reference-video/     参考视频：运动迁移与风格保持
│   ├── audio-driven/        音频驱动：节拍与节奏同步
│   ├── cinematography/      镜头运镜：镜头控制与分镜
│   ├── quality-and-cost/    质量与成本：参数权衡
│   ├── long-video-chain/    长视频：续接与连续生成
│   └── content-safety/      内容安全：审核策略与合规
│
└── 🎙️ 语音类
    └── text-to-speech/      语音合成：后期配音/旁白（seed-tts-2.0）
```

### 按媒体类型的方法表

#### 🖼️ 图片类

| 方法 | 一句话定位 | 何时用 |
|------|-----------|--------|
| [text-to-image](text-to-image/README.md) | 纯 prompt 生成静态图 | 分镜图、I2V 首帧、封面海报、概念验证 |

#### 🎬 视频类

| 方法 | 一句话定位 | 何时用 |
|------|-----------|--------|
| [text-to-video](text-to-video/README.md) | 纯 prompt 从零生成 | 有明确文字描述、无现成素材 |
| [image-to-video](image-to-video/README.md) | 用图片当首/尾帧驱动 | 已有静图、海报、关键帧 |
| [reference-video](reference-video/README.md) | 借参考视频的运动轨迹 | 想复刻某段运镜/动作、换主体 |
| [audio-driven](audio-driven/README.md) | 让画面跟着音频节奏走 | 卡点视频、MV、广告蒙太奇 |
| [cinematography](cinematography/README.md) | 镜头控制与分镜设计 | 需要专业运镜语言、多镜头 |
| [quality-and-cost](quality-and-cost/README.md) | 在质量/速度/成本间权衡 | 批量生成、预算受限、出样稿 |
| [long-video-chain](long-video-chain/README.md) | 把多条短视频续接成长片 | 单条不够长、需要连续叙事 |
| [content-safety](content-safety/README.md) | 应对审核拦截与合规 | 命中敏感内容、需要稳定产出 |

#### 🎙️ 语音类

| 方法 | 一句话定位 | 何时用 |
|------|-----------|--------|
| [text-to-speech](text-to-speech/README.md) | 文本转语音（后期配音） | 旁白、口播、多语言配音 |

### 组合用法示例

- **产品广告片**：`image-to-video`（产品图当首帧）+ `cinematography`（运镜）+ `audio-driven`（配乐卡点）+ `long-video-chain`（多镜头续接）
- **快速出样稿**：`quality-and-cost`（draft + 480p）先定方向 -> 定稿后切 1080p 正式生成
- **风格化短片**：`reference-video`（借参考视频运动）+ `text-to-video`（补充镜头）
- **分镜图先行**：`text-to-image`（seedream 出每镜关键帧）→ 审核 → `image-to-video`（分镜图当首帧动起来），返工成本最低
- **成片配音**：`text-to-speech`（TTS 生成旁白）→ ffmpeg `-c:a copy` 混入视频

> 这些组合在 [projects/](../projects/README.md) 里落地为具体项目。

---

## 四、通用执行三步法

> 所有方法都遵循这个流程，区别只在 Step 3 的参数与 `--input` 组合。

```bash
# Step 1：列当前 profile 可用的视频模型（platform=EP，agent-plan=模型名）
arkcli resources list --modality video

# Step 2：查选定模型 $MODEL 支持的参数（sp 空则用 modality 兜底默认）
arkcli models get "$MODEL" --transform supported_params

# Step 3：按可用参数生成（视频默认异步，返回 task_id）
arkcli +gen --model "$MODEL" "<prompt>" --open
# 同步阻塞等结果：加 --wait
```

### 视频结果处理（异步语义，重点）

```
+gen 提交 -> 返回 task_id + status=queued   ← 不是失败！
   │
   ▼ 用 arkcli gen get <task_id> --open 轮询
   │
   └─► status=succeeded -> 自动下载到本地 + 桌面弹出成品（看 local_path）
```

- **不要**因为没立刻拿到视频就重提 `+gen`（会建新任务）
- 预签名 `output_url` **24 小时失效**，长期保存依赖 `local_path` 或及时下载
- 要同步阻塞：`arkcli +gen ... --wait --open`
- ⚠️ `--save-to` 在 `gen get` 轮询下载时可能不生效，产物落到 `gen get` 的 CWD；建议轮询后手动 `mv` 到目标目录

---

## 五、模型说明

Seedance 是豆包视频生成系列，常见形态（具体以 `resources list` 当前 profile 输出为准）：

| 模型族 | 定位 | 备注 |
|--------|------|------|
| `doubao-seedance-1-5-pro` | 1.5 Pro，质量优先 | 不支持 `--priority`，⚠️ 即将下线 |
| `doubao-seedance-2-0` | 2.0 主线（✅ 已开通） | 支持 `--priority`/`--draft`/`--generate-audio`/`--return-last-frame`，输入支持 text/image/video/audio |
| `doubao-seedance-2-0-fast` | 2.0 快速版 | 速度/成本权衡 |
| `doubao-seedance-2-0-r2v` | 2.0 参考视频专用 | R2V 路径首选 |
| `doubao-seedance-2-0-mini` | 2.0 mini 轻量版 | ⛔ 不支持 --draft 与 --return-last-frame；output 仅 video 无音频 |

> ⚠️ `--model` 必须是**完整版本化 ID**（如 `doubao-seedance-2-0-260128`），只传族名会 404。版本号不固定（6/8 位日期或短数字），用 `arkcli models get <族名> --transform 'primary_version'` 补全，**不要自己正则猜**。

> 🔀 **Profile 路由规则**：`doubao-seedance-2-0-mini`（2.0 系列）走 **platform 按量**（`--profile platform_cn-beijing_accountwide`，gen get 也要带同 profile，否则 task not found）；其余模型走 **agent-plan**（默认 profile）。

> 📦 **Agent Plan Medium 套餐包含的模型**（来源：Agent Plan 配置指南）：
> - **视觉模型**（⛔ 不支持 Auto 及控制台切换，需在配置/命令显式指定模型）：
>   - `doubao-seedance-1-5-pro`（视频，⚠️ 即将下线，当前不支持新增接入）
>   - `doubao-seedream-5.0-lite`（图片生成）
>   - ⛔ Medium 套餐**不支持 Seedance 2.0 系列**（2.0/2.0-fast/2.0-mini/2.0-r2v）-> 这些走 platform 按量
> - **语音模型**（⛔ 同样不支持 Auto 及控制台切换）：
>   - 豆包语音合成 2.0（`doubao-seed-tts-2.0`），Resource-Id = `seed-tts-2.0`
>   - 豆包流式语音识别 2.0（`doubao-seed-asr-2.0`），Resource-Id = `volc.seedasr.sauc.duration`

> 🎯 **当前实际可用**：
> - platform 按量：✅ `doubao-seedance-2-0-260128`（视频，2026-08-01 开通，支持 generate-audio/priority/draft）+ `doubao-seedream-5-0-pro-260628`（图片，精准图像编辑）+ `doubao-seedance-2-0-mini-260615`（视频，轻量）
> - agent-plan：✅ `doubao-seedream-5-0-lite`（图片，实测可用）、`doubao-seedance-1-5-pro`、TTS / ASR（按上述模型名/Resource-Id 指定，勿用 Auto）
> 🔇 **音频输出能力**（已验证 `arkcli models get` 的 `modalities.output` / `task_types`）：并非所有 Seedance 都输出音频。
>   - `doubao-seedance-1-5-pro`：✅ 支持音画同步（task_types 含 `TextToAudioVideo`/`ImageToAudioVideo`，覆盖环境音/动作音/人声/背景音）
>   - `doubao-seedance-2-0`（260128）：✅ **实测支持 `--generate-audio`**（2026-08-01 验证，输出含环境音/动作音，max -10.9dB 非静音）
>   - `doubao-seedance-2-0-fast` / `2-0-mini`：❌ output 仅 video，无音频（`--generate-audio` 无效）
>   - 默认视频含 -35dB 静音占位轨，非真音频；要声音要么用 2.0/1.5-pro 生成，要么后期 ffmpeg 混音

### TTS 语音合成调用方式（后期配音）

> ⚠️ **arkcli 不覆盖 TTS/ASR**。TTS 走 OpenSpeech 服务（独立于 Ark Runtime），需自己写脚本调 HTTP 流式接口。`+chat`/`+gen`/`+code-example` 均不支持语音模型。
> 📄 **完整方法已独立成册：[text-to-speech](text-to-speech/README.md)**（端点/请求体/流式解码/speaker/ffmpeg 混音）。

| 项 | 值 |
|----|----|
| 端点 | `https://openspeech.bytedance.com/api/v3/plan/tts/unidirectional`（`/plan/` 路径 = Agent Plan 通道）|
| 认证 | Header `X-Api-Key: <ark-api-key>` + `X-Api-Resource-Id: seed-tts-2.0` |
| Profile | agent-plan（TTS 含在 Medium 套餐，走 ARK API Key） |
| 请求体 | `{"req_params":{"text":"...","speaker":"zh_female_vv_uranus_bigtts","audio_params":{"format":"mp3","sample_rate":24000}}}` |
| 响应 | 流式 JSON Lines，每行 `{"code":0,"data":"<base64 音频块>"}`，`code=20000000` 表结束 |
| 解码 | 逐行 `base64.b64decode(data)` 拼接成完整 mp3 |
| speaker | `zh_female_vv_uranus_bigtts`（沉稳女声，适合旁白）；其他音色见控制台语音合成音色列表 |

调用示例见 `projects/survival-island/scripts/tts_narration.py`（流式接收 + base64 拼接 + 落盘）。

> ⚠️ 混入视频时**不要用 `-c:a aac` 重编码**，mp3 直塞 mp4（`-c:a copy`）即可，实测 aac 重编码后播放器可能不识别音轨。

> 拿 API Key：`arkcli auth status` 看掩码，完整值在 `~/.arkcli/identities/<volc-id>/apikey.json`。

---

## 六、术语速查

| 术语 | 含义 |
|------|------|
| T2V / I2V / R2V | 文生视频 / 图生视频 / 参考视频生成 |
| 首帧 / 尾帧 | I2V 中驱动视频起点/终点的图片 |
| `queued` | 视频任务已排队（异步，非失败） |
| `supported_params` | 模型实际支持的参数清单，Step 2 必查 |
| 草稿模式 `--draft` | 更快更便宜、质量更低的出样模式 |
| 续接 | 用上一条的最后一帧作为下一条首帧，串成长片 |

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-07-18 | v1.0 | 初始规划，建立 8 个主题子目录与总导航 | 小七 |
| 2026-07-18 | v1.1 | 顶层重构为「项目制」：本篇迁入 methods/ 作为方法总览，顶层改按项目组织（projects/） | 小七 |
| 2026-07-18 | v1.2 | 新增 doubao-seedance-2-0-mini 模型；标注 Agent Plan 不含视频需 platform 按量；补充 --draft/--save-to/--return-last-frame 实际踩坑 | 小七 |
| 2026-07-18 | v1.3 | 补充音频输出能力对照：仅 1.5-pro 支持音画同步，2.0 系列（含 mini）output 仅 video | 小七 |
| 2026-07-18 | v1.4 | 记录 Agent Plan Medium 完整模型清单（视觉 seedream-5.0-lite/seedance-1.5-pro + 语音 TTS/ASR 及 Resource-Id）+ profile 路由规则；修正"不含视频"为"不含 2.0 系列" | 小七 |
| 2026-07-18 | v1.5 | 新增 TTS 语音合成调用方式（OpenSpeech 端点 + 请求体 + 流式解码），arkcli 不覆盖需自写脚本 | 小七 |
| 2026-08-01 | v1.6 | 新增文生图方法 text-to-image（seedream-5.0-lite）；修正"seedream 全系未激活"为已激活实测可用；能力地图/导航/组合用法补 T2I 行 | 小七 |
| 2026-08-01 | v1.7 | 目录结构按媒体类型重组：图片/视频/语音三大类 + 横切控制；TTS 独立成册 text-to-speech/；导航树与方法表分组展示 | 小七 |
| 2026-08-01 | v1.8 | 新增 seedream-5.0-pro（platform 按量，精准图像编辑）；模型可用列表补 pro + mini | 小七 |
| 2026-08-01 | v1.9 | 实测开通 seedance-2.0-260128（platform 按量）：支持 --generate-audio（有真音频）/--priority/--draft/--return-last-frame 参数；修正"2.0 无音频"过时记录 | 小七 |
| 2026-08-01 | v2.0 | 补 seedance-2.0 多模态参考输入完整用法：reference_image/reference_audio 角色前缀规则、@引用格式、实测踩坑（--generate-audio 无效、首帧不能混参考媒体、音频需 reference_audio 前缀）；记录官方教程地址 | 小七 |
| 2026-08-01 | v2.2 | 音频再验证：传 reference_audio 音量暴跌（RMS -45~-65dB 近无声），不传则模型原生音效正常（RMS -25~-27dB）——修正音频方案为"不传音频参考，模型原生生成" | 小七 |
| 2026-08-01 | v2.3 | 音频最终定版：`--extra-body '{"generate_audio": true}'` 显式传请求体参数才生效（--generate-audio flag 未正确映射）；对照实测 3 种方式音量 | 小七 |
