---
name: ark-image-multi-reference
description: 用火山方舟 Ark Seedream Pro 把多张参考图融合成一张图（多图参考）：角色×场景合成、主体×道具摆拍、元素拼合、风格+内容组合。含多 --input 顺序与 @图像N 引用规则、命令模板与踩坑点。触发词：多图参考、多图融合、图片合成、把角色放进场景、元素合成、换主体、multi-image reference。
whenToUse: 当需要把 ≥2 张素材里的元素合成到一张新图时使用。仅 doubao-seedream-5-0-pro-260628 支持。单张图做修改用 ark-image-editing；从零出图用 ark-image-text-to-image。
---

# 多图参考（Seedream Pro）

**用途**：≥2 张参考图 + prompt → 融合后的图；解决"素材分散、需要拼合"。

> ⛔ **仅 `doubao-seedream-5-0-pro-260628` 支持**，走 platform 按量 profile。

## 何时用

- 角色 × 场景（把角色放进目标场景）、主体 × 道具、元素拼合、一张给内容一张给画风
- 单图保主体换背景不理想时，可把原图 + 场景图一起作为多图参考

## 前置检查

```bash
arkcli models get "doubao-seedream-5-0-pro-260628" --transform supported_params
```

- 必须 `--profile platform_cn-beijing_accountwide`，模型名带 `-260628`

## 执行

**角色 + 场景融合**

```bash
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @char.jpg \
  --input @scene.jpg \
  --size "2560x1440" --output-format jpeg \
  "把@图像1的蝴蝶女放入@图像2的书桌场景中，人物形象、服装、翅膀保持完全不变，光线与场景一致" \
  --save-to out/
```

**主体 + 道具**

```bash
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @product.jpg --input @prop.jpg \
  --size "2048x2048" --output-format jpeg \
  "把@图像1的产品放到@图像2的木质托盘上，产品外观与 logo 不变，暖光摄影棚布光" \
  --save-to out/
```

## 引用规则

- 多个 `--input` **按出现顺序**编号，prompt 用 **`@图像1` / `@图像2` / `@图像3`** 引用
- 每张图明确分工："@图像1 提供人物，@图像2 提供场景"
- 要保留的元素加强约束："形象/服装/翅膀保持完全不变"
- 明确融合方式：谁放哪、朝向、景别、光线统一

### 指令模板

```
把@图像A的<主体>放入@图像B的<场景>，<主体特征>保持完全不变，<光线/比例/风格>与场景一致
```

## 踩坑点

- ⛔ **lite 不支持多图参考**，必须用 pro + platform 按量 profile
- ⚠️ **编号容易错**：`@图像N` 按 `--input` 出现顺序，命令行顺序改了编号就变；团队协作把顺序写进项目 README
- ⚠️ **三张以上参考易互相污染**：优先控制在 2 张；需要更多元素改链式（先合成 A+B，再把结果与 C 合成）
- ⚠️ **不要期待像素级复制**：参考是语义级引导，logo/文字仍需人工核对
- ⚠️ **参考图质量**：用清晰、主体完整、背景干净的素材

## 检查清单

- [ ] 用 pro 模型 + platform 按量 profile
- [ ] `--input` 顺序与 `@图像N` 编号一致
- [ ] 每张参考图在 prompt 里有明确分工
- [ ] 需保留的主体特征已用"保持完全不变"约束
- [ ] 参考图数量 ≤2（超出改链式合成）
- [ ] 结果已落盘并记录输入图版本
