---
name: ark-image-workflow
description: Seedream 图片资产工作流：产物落盘（摆脱 24h 预签名 URL）、目录与命名规范、model+prompt+seed+size 追溯、锚点图复用，以及 T2I 分镜图衔接到 video-gen 图生视频（I2V）。触发词：图片落盘、资产库、命名规范、版本管理、分镜图接视频、T2I 转 I2V、图片存档、产出记录。
whenToUse: 当图片要长期留档、多版本管理、跨项目复用，或作为分镜图接入 video-gen 图生视频时使用。可与任意 Seedream 执行技能搭配。
---

# 图片工作流（Image Workflow）

**用途**：让图片资产可追溯、可复用、可衔接视频；解决"图出来之后怎么办"。

## 何时用

- 图片要长期留档、多版本管理、供团队复用
- 分镜图要接进 video-gen 的图生视频（I2V）

## 目录规范

```
<project>/
├── README.md                项目规划（含 Prompt & 参数、产出记录）
└── out/
    ├── storyboard/          分镜图（按镜号命名：shot1.jpg …）
    ├── views/               多角度角色图（front/side/back/three-quarter）
    ├── scenes/              同角色多场景（移步换景产物）
    ├── lookbook/            角色设定图库
    └── final/               定稿成品
```

**命名建议**

```
<用途>_<主体/镜号>_<视角或场景>_v<版本>.<ext>
例：shot3_v2.jpg / char_front_v1.jpg / char_scene-cyber_v1.jpg
```

- 镜号/角度放前面，方便排序
- 版本号必带（`v1 v2 v3`），避免覆盖
- 编辑链产物标注来源：`char_front_v1_edit-suit_v1.jpg`

## 落盘与追溯

```bash
arkcli +gen --model "doubao-seedream-5-0-lite" \
  --size "2560x1440" --output-format jpeg \
  "<prompt>" --save-to out/storyboard/
```

> ⚠️ `--save-to` 有时不生效、产物落到 CWD；生成后务必确认路径并手动 `mv`。

**追溯表（写进项目 README）**

| 图 | 版本 | 模型 | prompt 摘要 | seed | 路径 | 备注 |
|----|------|------|-------------|------|------|------|
| shot1 | v1 | seedream-5.0-lite | 茶室起舞… | 42 | out/storyboard/shot1.jpg | 定稿 |
| char_front | v2 | seedream-5.0-pro | 角色设定… | 7 | out/views/front_v2.jpg | 锚点 |

- 定稿图必须记录 **model + prompt + seed + size**
- 编辑/派生产物记录**来源图版本**，形成依赖链

## 衔接 video-gen（T2I → I2V）

```
image-gen 文生图出分镜图 ──► 人工审核 ──► 落盘 out/storyboard/
                                              │
                                              ▼
video-gen：arkcli +gen --model <seedance> --input @shotN.jpg ...（I2V 动起来）
```

- **先审后动**：分镜图审核通过再进 I2V，图片返工比视频便宜得多
- **尺寸对齐**：分镜图比例与目标视频一致（16:9 → `2560x1440`；9:16 → `1440x2560`）
- **路径稳定**：I2V 用的图放稳定路径，别用 24h URL
- I2V 具体用法见 `../../../video-gen/methods/image-to-video/README.md`

## 资产复用

- **锚点图**：角色/产品选定一张"权威图"，所有衍生从它派生
- **模板 prompt**：跑通的 prompt 抽成模板，写进项目 README
- **复用清单**：项目 README 维护"可复用资产"表（锚点图路径 + 特征说明）
- **大文件**：批量产物注意仓库体积，必要时 `.gitignore` 中间产物

## 踩坑点

- ⚠️ **不落盘**：只留输出 URL，24h 后无法复取
- ⚠️ **`--save-to` 失灵**：产物落到 CWD，事后找不到
- ⚠️ **覆盖旧版**：同名保存覆盖，无法对比；版本号必带
- ⚠️ **比例不对齐**：分镜图 1:1 却要做 16:9 视频，被迫裁切变形
- ⚠️ **prompt 未记录**：图很好但复现不了、无法微调
- ⚠️ **锚点不唯一**：多张图都被当锚点，派生结果互相打架

## 检查清单

- [ ] 产物已落盘到规范目录
- [ ] 命名含用途/镜号/版本
- [ ] 定稿图记录 model + prompt + seed + size
- [ ] 编辑/派生产物记录来源版本
- [ ] 分镜图比例与目标视频一致
- [ ] 锚点图唯一且已登记
- [ ] 可复用 prompt 已沉淀为模板
