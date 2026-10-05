---
name: ark-image-text-to-image
description: 用火山方舟 Ark Seedream 从纯文本 prompt 生成静态图片（文生图 T2I）：分镜图、I2V 首帧、海报封面、角色设定初版、概念验证。含 lite/pro 模型路由、命令模板、四要素 prompt 写法与踩坑点。触发词：文生图、用文字生成图片、T2I、text to image、出图、生成分镜图/首帧/封面、seedream。
whenToUse: 当需要从零（没有参考图）生成一张静态图片，或用文字描述批量出图时使用。若手里已有图要改背景/换元素，改用 ark-image-editing；要把多张素材合成一张，改用 ark-image-multi-reference；要补同一角色的其它视角，改用 ark-image-multi-view。
---

# 文生图 T2I（Seedream）

**用途**：仅凭 prompt 生成静态图片；无需任何输入图。

## 何时用

- 只有文字描述，要一张图：分镜图 / 关键帧 / 首帧 / 封面海报 / 角色初版 / 概念验证
- 作为 video-gen 图生视频（I2V）的前置工序：先出图审核，再动起来

## 前置检查

1. 执行前先查参数（必做）：
   ```bash
   arkcli models get "$MODEL" --transform supported_params
   ```
2. 模型与 profile 必须匹配，不可混：

   | 模型 | Profile | 用于 |
   |------|---------|------|
   | `doubao-seedream-5-0-lite` | agent-plan（**默认**，勿用 Auto） | 纯文生图、草稿（套餐内更省） |
   | `doubao-seedream-5-0-pro-260628` | ⚠️ `platform_cn-beijing_accountwide` | 需要编辑/多图参考，或要 1920×1080 小尺寸 |

## 执行

**Step 1 生成（lite）**

```bash
MODEL="doubao-seedream-5-0-lite"
arkcli +gen --model "$MODEL" \
  --size "2560x1440" --output-format jpeg \
  "<prompt>" --save-to out/
```

**Step 2 生成（pro，注意 profile + 完整版本 ID）**

```bash
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --size "2560x1440" --output-format jpeg \
  "<prompt>" --save-to out/
```

**Step 3 一次多张 / 复现**

```bash
# 多张候选
arkcli +gen --model "$MODEL" --size "2560x1440" --output-format jpeg \
  --image-count 4 "<prompt>" --save-to out/draft/

# 复现：同模型 + 同 prompt + 同 seed + 同 size
arkcli +gen --model "$MODEL" --size "2560x1440" --output-format jpeg \
  --seed 42 "<定稿 prompt>" --save-to out/final/
```

> 图片是**同步返回**的：提交即出图，**没有 `task_id`、不要 `gen get` 轮询**（那是视频语义）。

## Prompt 四要素（缺一即多分随机）

```
<主体：谁+外观特征>，<场景：地点+光线>，<风格：色调+画风>，<构图：景别+画面重点>，<增强：镜头/质感>
```

- 分镜图只写**最有代表性的静态瞬间**，动态交给 video-gen I2V
- 要竖版就按 `--size "1440x2560"` 重出，**不要横图硬裁**
- 详细写法见 `../prompt-engineering/SKILL.md`

## 常用尺寸

| 比例 | `--size` | 说明 |
|------|----------|------|
| 16:9 | `2560x1440` | 分镜图 / 横版海报 |
| 9:16 | `1440x2560` | 短视频封面 / 竖版 |
| 1:1 | `2048x2048` | 头像 / 方图 |
| 1920×1080 | `1920x1080` | ⚠️ 仅 pro（lite 低于像素下限会被拒） |

## 踩坑点

- ⛔ **图片比例用 `--size`，不用 `--ratio`**：`--ratio` 是 video task 专属，图片任务传了被忽略 → 默认落到 2048×2048 正方形
- ⛔ **lite 像素下限 ≥3,686,400**（≈2048×1800）：`2560x1440` 恰好达标，1920×1080 会被拒；pro 无下限
- ⛔ **pro 必须完整版本 ID** `doubao-seedream-5-0-pro-260628`：族名在 platform 数据面 NotFound
- ⛔ **profile 传错**：pro 走 agent-plan 报 `does not support the agent plan feature`
- ⛔ **文生图不要传 `--input`**：T2I 没有参考图
- ⚠️ **`--save-to` 可能不生效**：产物可能落到 CWD，执行后确认路径并手动 `mv`
- ⚠️ **URL 24h 失效**：必须落盘，别把预签名地址当成品长期用

## 检查清单

- [ ] 已查 `supported_params`
- [ ] 模型 ID 完整 + profile 匹配（lite↔agent-plan / pro↔platform）
- [ ] 尺寸用 `--size` 且满足像素下限
- [ ] prompt 覆盖主体 / 场景 / 风格 / 构图
- [ ] 图片已落盘（local_path），不依赖 24h URL
- [ ] 定稿记录 model + prompt + seed + size 四元组
