# Seedance 2.5 参考生视频节点（`ByteDance2ReferenceNodeV2`）事实记录

> 返回[技能首页](../SKILL.md)

> **这些事实是怎么来的**：全部来自 **① 一份导出的 UI 工作流**（`assets/seedance-2.5-reference-r2v-ui.json`，
> 里面带 `widgets_values_named`，参数字段名是显式写着的）和 **② 一份本地缓存的 `/object_info` 快照**
> （`references/node-info.json`，抓取时间 2026-10-06，**970** 个节点类）。
> 以及 **③ 同一天缓存下来的 24 个官方 Seedance 模板**（`work/tpl-cache/api_seedance2_*.json`，仅本地）。
> ⚠️ **没有任何一条来自真机运行** —— 本技能"只建不验"，见 SKILL.md 顶部声明。

## 1. 节点身份

| 项 | 值 |
|---|---|
| 类名 | `ByteDance2ReferenceNodeV2` |
| 分类 | `partner/video/ByteDance` → **付费云端节点** |
| 输出 | `VIDEO`、`draft_task_id`（STRING） |
| 顶层必填输入 | `model`（`COMFY_DYNAMICCOMBO_V3`）、`seed`（INT）、`watermark`（BOOLEAN） |
| 权重 | **无**：模型在字节云端，本机不需要、也不该去找权重文件 |

> 同族的其它节点（同一份快照里就有）：`ByteDance2TextToVideoNode`（t2v）、
> `ByteDance2FirstLastFrameNode`（首尾帧）、`ByteDance2DraftToFinalVideoNode`（草稿转正片）、
> `ByteDance2ReferenceNode`（无 V2）、`ByteDanceVideoEnhanceNode`（视频增强）等。
> 本技能只做 **V2 的参考生视频**。

## 2. 工作流形状（3 个节点）

```text
LoadImage(12) ──IMAGE──► ByteDance2ReferenceNodeV2(24).model.reference_images.image_1
                              │
                              └──VIDEO──► SaveVideo(16)   # filename_prefix = video/Seedance2.5_r2v
```

- `LoadImage` 的 widget 是 `image` = 服务器 `input/` 里的文件名；脚本会把本地图**上传后**改写成上传得到的新名字。
- `SaveVideo` 的 widget：`filename_prefix` / `format` / `format.codec` / `codec`（后三个是动态下拉框）。
- 导出的 UI 图里带有前端伪 widget **`control_after_generate`**（值 `randomize`）—— 它不是节点输入，
  提交前必须剔除（共享引擎的 `PSEUDO_WIDGETS` 已经处理）。

## 3. `model` 是动态下拉框：参数全挂在它下面

**这一点最容易踩**：`/object_info` 里这个节点只有 `model` / `seed` / `watermark` 三个字段，
但 `prompt`、`resolution`、`ratio`… 都是**所选模型的下级子输入**，在 API 图里的名字**带点**
（`model.prompt` / `model.resolution` / …）。少给一个必填子输入，图就过不了校验。

| 子输入 | Seedance 2.5 | Seedance 2.0 系列 | 说明 |
|---|---|---|---|
| `model.prompt` | 必填 | 必填 | 提示词（见 §5） |
| `model.resolution` | `480p` / `720p` / `1080p`（默认 `720p`） | 同上 **+ `4k`** | |
| `model.ratio` | `16:9` / `4:3` / `1:1` / `3:4` / `9:16` / `21:9` / `adaptive`（默认 `16:9`） | 同上（默认 `adaptive`） | `adaptive` = 跟随参考图比例 |
| `model.duration` | INT **4–30**（默认 `5`） | INT **4–15**（默认 `7`） | 秒 |
| `model.generate_audio` | BOOLEAN（默认 `true`） | 同 | 同步音频 |
| `model.task_type` | `auto` / `reference` / `edit` / `extend`（默认 `auto`） | **没有这一项** | 见 §6 |
| `model.output_format` | `mp4` | 同 | |
| `model.auto_downscale`（可选） | BOOLEAN 默认 `true` | 同 | 云端自动降采样 |
| `model.auto_upscale`（可选） | BOOLEAN 默认 `false` | 同 | 云端自动放大 |

模型键共 **5 个**：`Seedance 2.5`、`Seedance 2.5 Draft`、`Seedance 2.0`、`Seedance 2.0 Fast`、`Seedance 2.0 Mini`。

## 4. 参考输入是采集式（autogrow）

| 输入 | Seedance 2.5 / 2.5 Draft | Seedance 2.0 / Fast / Mini |
|---|---|---|
| `model.reference_images.image_N` | 最多 **30** | 最多 **9** |
| `model.reference_videos.video_N` | 最多 **10** | 最多 **3** |
| `model.reference_audios.audio_N` | 最多 **10** | 最多 **3** |
| `model.reference_assets.asset_N` | 最多 **30** | 最多 **9** |

- 类型是 `COMFY_AUTOGROW_V3`：接口是**带序号的 dotted 名**，`image_1` 就是第一个参考图，
  在提示词里用 `<Picture 1>` 指代（与 H3 系写法一致）。
- schema 给的 `min` 是 **0**，也就是"节点本身不强制要参考图"；
  但本技能是**参考生视频**技能，脚本要求**至少 1 张**（要给纯文生视频，请用
  [text-to-video-fastvideo3](../../text-to-video-fastvideo3/SKILL.md) 或官方 t2v 模板）。
- ⚠️ **v1 只支持参考图**：工作流里只有 `LoadImage` 一个源节点，没有视频/音频输入节点。
  传 `--task-type edit` / `extend` 会给一条 warning（那两档通常要参考视频）。

## 5. r2v 提示词格式

工作流里自带一条 **13929 字符**的样本（雨林花神的 7 镜 15 s 芭蕾），
`--show-default-prompt` 可以打印它。它用的就是标准三节结构：

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
integrated_multimodal_description: [Shot 1] ... At 01.900, ... At 03.900, ... At 06.300, ...
overall_soundscape: ...
non_diegetic_music: ...
```

- 逐镜头写法、切点惯例、声音两节的职责见
  [image-to-video-fastvideo3/references/prompt-format.md](../../image-to-video-fastvideo3/references/prompt-format.md)。
- **本技能不给默认提示词**：工作流里那条是样本；一次出片是花钱的，脚本要求显式 `--prompt/--prompt-file`。

## 6. `task_type` 四档（**证据来自官方模板，不是厂商文档**）

| 值 | 依据（本地缓存的官方模板） | 本技能的判断 |
|---|---|---|
| `reference` | `api_seedance2_5_r2v.json` 用的就是它 | **参考生视频的正确档**，脚本默认 |
| `edit` | `api_seedance2_5_video_editing.json` | 视频编辑：要参考视频，本工作流没接 |
| `extend` | `api_seedance2_5_video_extend.json` | 视频延长：同上 |
| `auto` | `api_seedance2_0_r2v_real_human.json`、`api_seedance2_5_draft_r2v.json` | 让云端自己判断；给图也能跑（两个模板都这么用） |

> ⚠️ 这四档的**准确语义**（尤其是 `auto` 与 `reference` 的差别）**没有官方文档可引**，
> 上面的判断是从"哪个官方模板用了哪一档"反推的。要下结论需要真机对照 —— 尚未做。

## 7. `SaveVideo` 的输出参数

| 输入 | 类型 | 可选值 |
|---|---|---|
| `filename_prefix` | STRING | 默认 `video/ComfyUI`（本工作流是 `video/Seedance2.5_r2v`） |
| `format` | `COMFY_DYNAMICCOMBO_V3` | `auto` / `mp4` / `mkv` / `webm` |
| `codec` | `COMFY_DYNAMICCOMBO_V3` | `auto` / `h264`（另有 `av1`，带 `encoding` 子项） |

成品在服务器 `output/<prefix>`（默认 `output/video/`）；`/view` 需要带 `subfolder=video`，
共享引擎的下载函数会自己带上。

## 8. 凭据通道（与 Seedream 系列完全一样）

无头调用付费节点，必须在 `POST /prompt` 的 `extra_data` 里带 ComfyUI 账号凭据：

| 通道 | 键 | 来源 |
|---|---|---|
| API Key（推荐） | `api_key_comfy_org` | `--api-key` / `--api-key-file` / `$COMFYUI_API_KEY` / `$COMFY_API_KEY` |
| OAuth Bearer（会过期） | `auth_token_comfy_org` | `--auth-token` / `$COMFYUI_AUTH_TOKEN` |

⚠️ **在桌面端用邮箱/浏览器登录不足以**让无头请求通过（实测报 `Unauthorized`）；
`extra_data` 里两个键名取自 ComfyUI 的 `comfy_api_nodes/util/_helpers.py`。

## 9. 快照的来源与漂移

| 项 | 值 |
|---|---|
| 快照文件 | [node-info.json](node-info.json) |
| 抓取时间 | **2026-10-06 17:57**（本地缓存，不是为本技能专门抓的） |
| 服务器 | `http://192.168.3.5:18000` |
| 快照里的节点类总数 | **970** |
| 同一台服务器 2026-10-11 实测 | **980** ← **可能已漂移** |
| `/object_info` 的 sha256 | 见快照 `_source.object_info_sha256` |

`--check` 会拿这份快照和真机 `/object_info` 逐项对账（模型增删 / 每个模型的参数增删 / 保存格式），
结果为 `schema_drift`；`"none"` 才说明快照还没过期。**首次真机使用前先跑它。**

## 10. 未验证清单（交付时明确没做的事）

- [ ] `--check` 没跑过（不知道这台服务器现在有没有这个节点、schema 漂了多少）
- [ ] `--list` 没跑过（枚举值是从快照里读的，没和真机比过）
- [ ] `--plan` 没跑过（**参考图接线、参数落图、autogrow 节点增删都还没有一次真实验证**）
- [ ] 真出片没跑过（不知道能不能过云端校验、能不能下到 mp4、留档是否正常）
- [ ] 没有 `test_skill.py`、没有进 `check.sh`
