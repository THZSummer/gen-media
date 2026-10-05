---
name: ark-image-parameters
description: Seedream 图片生成的参数与输出选型：--size 尺寸比例、lite 像素下限、--output-format、--image-count/--n、--seed 复现、--guidance-scale、--optimize-prompt、--save-to，以及 model 与 profile 的匹配。触发词：图片参数、--size、尺寸、分辨率、像素下限、seed 复现、一次出多张、参数被拒、supported_params。
whenToUse: 当需要确定出图尺寸/格式/张数、复现某张图、参数被拒，或不确定某模型支持哪些参数时使用。执行任何 Seedream 生成前都应先查 supported_params。
---

# 参数与输出（Parameters & Output）

**用途**：选对尺寸、格式、张数、种子，并让结果可复现。

> ⚠️ 参数以 2026-08 实测为准；执行前用 `arkcli models get "$MODEL" --transform supported_params` 核对。

## 前置检查（必做）

```bash
arkcli resources list --modality image
arkcli models get "$MODEL" --transform supported_params
```

## 参数总表

| 参数 | 作用 | 取值 | 备注 |
|------|------|------|------|
| `--model` | 模型 | `doubao-seedream-5-0-lite` / `doubao-seedream-5-0-pro-260628` | 见下表 |
| `--profile` | 计费通道 | `platform_cn-beijing_accountwide` | lite 用默认 agent-plan；pro 必须显式 platform |
| `--size` | 输出尺寸（像素） | `2560x1440` / `1440x2560` / `2048x2048` | ⚠️ 图片比例靠它，不用 `--ratio` |
| `--output-format` | 输出格式 | `jpeg` / `png` | 透明需求用 png |
| `--image-count` / `--n` | 一次出多张 | 整数，>1 顺序出图 | 张数直接乘成本 |
| `--seed` | 固定随机种子 | 整数 | 复现同图的关键 |
| `--guidance-scale` | 提示词遵循度 | float，如 `7.5` | 越高越贴 prompt，过高僵硬 |
| `--optimize-prompt` | 服务端优化 prompt | 开 / 关 | 追求可控时关掉 |
| `--response-format` | 返回方式 | `url` / `b64_json` | 默认 url（24h 失效） |
| `--stream` | 流式输出 | 仅图片 | NDJSON |
| `--save-to` | 落盘目录 | 路径 | **每次都应带** |
| `--input` | 参考图 | `@文件路径` | 文生图不传；编辑/多图参考才传 |

> 🚫 **`--ratio` 对图片任务无效**：那是 video task 专属参数，传了被忽略 → 默认落到 2048×2048 正方形。

## 模型与 Profile

| 模型 | Profile | 何时用 |
|------|---------|--------|
| `doubao-seedream-5-0-lite` | agent-plan（**默认**，勿用 Auto） | 纯文生图、批量草稿 |
| `doubao-seedream-5-0-pro-260628` | ⚠️ `platform_cn-beijing_accountwide` | 编辑 / 多图参考 / 多视角 / 小尺寸 |

## 尺寸选型

| 比例 | 推荐 `--size` | 用途 |
|------|--------------|------|
| 16:9 | `2560x1440` | 分镜图、视频首帧、横版海报 |
| 9:16 | `1440x2560` | 短视频封面、手机壁纸、竖版海报 |
| 1:1 | `2048x2048` | 头像、社媒方图、商品主图 |
| 1920×1080 | `1920x1080` | ⚠️ 仅 pro（lite 低于像素下限会被拒） |

- **lite 像素下限 ≥3,686,400**（≈2048×1800）：`2560x1440`(3,686,400) 恰好达标，`1920x1080`(2,073,600) 会被拒
- **pro 无下限**：`1920x1080` 实测可用
- **要竖版就重出，不要横裁**

## 复现与批量

```bash
# 复现：同模型 + 同 prompt + 同 --seed + 同 --size
arkcli +gen --model "doubao-seedream-5-0-lite" \
  --size "2560x1440" --output-format jpeg --seed 42 \
  "<定稿 prompt>" --save-to out/final/

# 批量出草稿
arkcli +gen --model "doubao-seedream-5-0-lite" \
  --size "2560x1440" --output-format jpeg --image-count 4 \
  "<prompt>" --save-to out/draft/
```

## 踩坑点

- ⛔ **profile 传错**：pro 走 agent-plan 报 `does not support the agent plan feature`
- ⛔ **模型名不完整**：pro 族名数据面 NotFound，必须带 `-260628`
- ⚠️ **`--ratio` 被忽略**：尺寸必须用 `--size`
- ⚠️ **lite 尺寸被拒**：低于 3,686,400 像素报错，别照搬 pro 的 1920×1080
- ⚠️ **`--image-count` 成本翻倍**：草稿阶段用 lite
- ⚠️ **`--seed` 不能跨模型复现**：lite 的 seed 42 ≠ pro 的 seed 42
- ⚠️ **`--optimize-prompt` 改写不可见**：团队协作建议关闭
- ⚠️ **`--save-to` 可能不生效**：产物可能落到 CWD，执行后确认并手动 `mv`
- ⚠️ **url 24h 失效**：拿到的是预签名地址，必须落盘

## 检查清单

- [ ] 执行前查过 `supported_params`
- [ ] 模型 ID + profile 匹配（lite↔agent-plan / pro↔platform）
- [ ] 尺寸用 `--size` 且满足模型像素下限
- [ ] 比例与最终用途一致
- [ ] 定稿图记录 model + prompt + seed + size
- [ ] 产物已确认落盘路径
