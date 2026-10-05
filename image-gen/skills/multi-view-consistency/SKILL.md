---
name: ark-image-multi-view
description: 用火山方舟 Ark Seedream Pro 从单张参考图生成同一主体的其它视角（多视角一致性）：正面→背面/侧面/四分之三侧面，用于角色三视图、多角度图库、机位补充、表情姿势扩展。含锚点策略与防漂移规则。触发词：多视角、三视图、生成角色背面、同一角色不同角度、角色一致性、多角度图库、multi-view。
whenToUse: 当已有一张角色/主体参考图，要补出同一形象的其他视角或姿势以保持一致性时使用。仅 doubao-seedream-5-0-pro-260628 支持。要改内容（背景/服装）而非视角用 ark-image-editing；从零出角色初版用 ark-image-text-to-image。
---

# 多视角一致性（Seedream Pro）

**用途**：1 张参考图 + 视角指令 → 同一主体的新视角图；解决"多张图各画各的、形象对不上"。

> ⛔ **仅 `doubao-seedream-5-0-pro-260628` 支持**，走 platform 按量 profile。

## 何时用

- 角色三视图（正/侧/背）、多角度图库（3D 参考、周边设计、视频分镜复用）、机位补充、表情/姿势扩展
- **这是角色一致性性价比最高的做法**：一次锁定形象，所有角度从锚点图派生

## 前置检查

```bash
arkcli models get "doubao-seedream-5-0-pro-260628" --transform supported_params
```

- 必须 `--profile platform_cn-beijing_accountwide`，模型名带 `-260628`
- **锚点选择**：挑形象最完整、信息最多的那张（通常正面或四分之三侧面）作为 `BASE`

## 执行

**正面 → 背面**

```bash
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @front.jpg --size "1440x2560" --output-format jpeg \
  "保持@图像1中人物的形象、服装、翅膀、配色完全不变，改为背面视角全身像，背景简洁" \
  --save-to out/views/
```

**正面 → 四分之三侧面**

```bash
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @front.jpg --size "1440x2560" --output-format jpeg \
  "保持@图像1人物形象、服装完全不变，改为四分之三侧面视角，视线朝向画面右侧" \
  --save-to out/views/
```

**三视图批量**

```bash
MODEL="doubao-seedream-5-0-pro-260628"
BASE="@front.jpg"
for view in "正侧面（90度）" "背面（180度）" "四分之三侧面（45度）"; do
  arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
    --input "$BASE" --size "1440x2560" --output-format jpeg \
    "保持@图像1人物形象、服装、配色完全不变，改为${view}视角全身像，纯色背景" \
    --save-to out/views/
done
```

## 指令结构

```
保持@图像1的<形象/服装/配饰/配色>完全不变，改为<视角角度>视角，<背景/景别/光线要求>
```

- **特征写全**：不只说"保持不变"，把关键特征列出来（翅膀、发色、纹样）
- **视角用角度词**：90° 正侧面 / 180° 背面 / 45° 四分之三侧面
- **所有角度都直接从锚点图派生**，不要从背面再派生侧面

## 踩坑点

- ⛔ **必须用 pro**：lite 不支持参考图生成新视角
- ⛔ **pro 走 platform 按量** + 完整版本 ID
- ⚠️ **避免链式套娃**：从正面派生背面可以；再从背面派生侧面会累积漂移
- ⚠️ **生成后逐项比对**锚点图（配饰数量、纹样方向），不一致的重生成而非硬用
- ⚠️ **命名规范**：`front.jpg` / `side.jpg` / `back.jpg` / `three-quarter.jpg`，进资产库

## 检查清单

- [ ] 锚点图选的是信息最完整的那张
- [ ] 用 pro 模型 + platform 按量 profile（完整版本 ID）
- [ ] 每张新视角**直接从锚点图**派生（非链式套娃）
- [ ] 指令中列全了要保持不变的特征
- [ ] 视角用明确角度描述
- [ ] 结果已与锚点图逐项比对一致性
- [ ] 落盘命名规范统一
