---
name: ark-image-editing
description: 用火山方舟 Ark Seedream Pro 对已有图片做图像编辑（I2I）：换背景、移步换景、换装、换元素、局部精修、风格迁移，并保持主体不变。含单图编辑命令模板、编辑指令写法与踩坑点。触发词：图像编辑、改图、换背景、换场景、移步换景、换装、P图、图生图、image editing、I2I。
whenToUse: 当手里已有底图，要修改其内容（背景/服装/元素/风格）同时保持主体时使用。仅 doubao-seedream-5-0-pro-260628 支持。要从零出图走 ark-image-text-to-image；要融合多张素材走 ark-image-multi-reference；只改视角走 ark-image-multi-view。
---

# 图像编辑 I2I（Seedream Pro）

**用途**：1 张参考图 + 编辑指令 → 修改后的图；主体保持不变。

> ⛔ **仅 `doubao-seedream-5-0-pro-260628` 支持**，走 platform 按量 profile；lite 无编辑能力。

## 何时用

- 同一人物换背景（移步换景）、换装/换季、海报元素替换、局部精修、风格迁移
- 做不到"保主体换背景"时，也可把原图 + 场景图一起走 `ark-image-multi-reference`

## 前置检查

```bash
arkcli models get "doubao-seedream-5-0-pro-260628" --transform supported_params
```

- profile 必须显式 `--profile platform_cn-beijing_accountwide`（漏了报 `does not support the agent plan feature`）
- 模型名必须带版本 `-260628`（族名在 platform 数据面 NotFound）

## 执行

**基础编辑**

```bash
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @base.jpg --size "2560x1440" --output-format jpeg \
  "把背景改成赛博都市夜景，霓虹灯箱与车流光轨，人物保持完全不变" --save-to out/
```

**换装**

```bash
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @char.jpg --size "1440x2560" --output-format jpeg \
  "人物形象、五官、发型、姿势完全不变，把服装换成月白色汉服，背景保持原样" --save-to out/
```

**批量换背景（移步换景）**

```bash
MODEL="doubao-seedream-5-0-pro-260628"
BASE="@char.jpg"
for scene in "竹林晨雾，青绿山水" "沙漠落日，金色沙丘" "雪原极光，冷蓝色调"; do
  arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
    --input "$BASE" --size "2560x1440" --output-format jpeg \
    "人物保持完全不变，背景改为：${scene}" --save-to "out/scenes/"
done
```

## 编辑指令结构

```
<保持不变的部分，显式强调> + <要改的部分，具体描述> [+ <光线/色调一致要求>]
```

| 要素 | 示例 |
|------|------|
| 保持 | "人物形象、服装、姿势完全不变" / "产品外观与 logo 保持原样" |
| 修改 | "把背景改为雨夜街道，地面积水反光" |
| 一致 | "保持原图光线方向与色调，边缘过渡自然" |

- 「保持不变」**必须显式写出来**，否则模型可能顺手改动主体
- 一次只改一类东西（先改背景，满意后再换装），叠加修改容易失控
- 编辑结果可继续当下一轮 `--input`，做链式迭代

## 踩坑点

- ⛔ **lite 不支持编辑**：必须用 pro
- ⛔ **pro 走 platform 按量** + 完整版本 ID
- ⚠️ **主体保持是概率性的**：复杂改动（换衣 + 换背景 + 换姿势）一致性下降，拆成多轮更稳
- ⚠️ **尺寸用 `--size`**，不要用 `--ratio`；pro 无像素下限，1920×1080 可直接用
- ⚠️ **结果落盘**：编辑结果同样是 24h 失效的预签名 URL，务必 `--save-to`

## 检查清单

- [ ] 用 pro 模型 + platform 按量 profile（完整版本 ID）
- [ ] `--input @图` 指向要编辑的底图
- [ ] 指令里显式写了「保持不变」的部分
- [ ] 一次只改一类内容
- [ ] `--size` 与目标用途比例一致
- [ ] 结果已落盘并记录本轮 prompt
