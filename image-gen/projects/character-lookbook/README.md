# 角色设定图库（Character Lookbook）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[项目索引](../README.md) ｜ 技术技能见 [../../skills/](../../skills/README.md)
> 示例项目：演示如何用「文生图 + 多视角一致性 + 多图参考 + 图像编辑」搭出一个可复用的角色资产库。

---

## 一、项目背景

- **项目名**：角色设定图库（character-lookbook）
- **目标**：为一个**原创虚构角色**建立多角度、多场景、多装扮的设定图库，供后续分镜、视频 I2V、周边设计复用
- **用途**：角色资产沉淀（不是一次性出图，而是**可派生**的锚点库）
- **交付时间**：<日期>

> ⚠️ **合规前置**：角色为原创虚构，不指涉任何真实人物或既有 IP；服装与姿态按正常表达设计。生成时按需自查内容安全与平台审核规则。

---

## 二、交付物清单

| # | 图用途 | 尺寸 | 比例 | 数量 |
|---|--------|------|------|------|
| 1 | 三视图（正/侧/背，全身） | 1440x2560 | 9:16 | 3 |
| 2 | 四分之三侧面 | 1440x2560 | 9:16 | 1 |
| 3 | 多场景（同角色，换背景） | 2560x1440 | 16:9 | 2 |
| 4 | 多装扮（同角色，换服装） | 1440x2560 | 9:16 | 2 |
| 5 | 定稿头像 / 半身 | 2048x2048 | 1:1 | 1 |

---

## 三、技能选型

| 阶段 | 所用技能 | 链接 | 输入素材 |
|------|----------|------|----------|
| 初版正面 | 文生图 | [text-to-image-comfyui](../../skills/text-to-image-comfyui/SKILL.md) | - |
| 补侧/背/半侧视角 | 控制图生图（以正视图为控制图，Canny 约束构图与姿态） | [image-edit-comfyui](../../skills/image-edit-comfyui/SKILL.md) | 正面锚点图 |
| 换场景 | 控制图生图（人物轮廓为控制图，背景在 prompt 里改） | [image-edit-comfyui](../../skills/image-edit-comfyui/SKILL.md) | 正面锚点图 |
| 换装扮 | 控制图生图 | [image-edit-comfyui](../../skills/image-edit-comfyui/SKILL.md) | 正面锚点图 |
| 定稿整理 | 合图 / 比对 / 剥元数据 | [image-tools](../../skills/image-tools/SKILL.md) | 全部成品 |

> ⚠️ 原先的「多视角一致性」「多图参考（场景融合）」「图像编辑」三个**云端文档技能**已于 2026-10-05 移除（无脚本、无法自检）。
> 现在的做法是**用控制图生图（`image-edit-comfyui`）替代**：拿已定稿的正面图当控制图，约束住人物轮廓与姿态，只让 prompt 改场景/装扮。
> 纯"多图融合"（角色图 × 场景图合成一张）目前**没有可用技能**，需要时再补一个带脚本的实现。

---

## 四、角色设定与视觉锚点

所有派生图共享同一段**视觉锚点**（视觉锚点 = 每次 prompt 都要复述的那段角色描述）：

```
东方少女，18 岁，虚构角色；黑长直发，发间一枚青玉簪；浅青水墨渐变纱裙，腰系月白缎带；
赤足，脚踝银铃；身形纤细，气质清泠。青绿水墨画风，留白氛围。
```

> 🔒 **锚点唯一**：图库以"正面全身图"为**权威锚点**，其余所有角度/场景/装扮都从它派生，避免各自凭空生成导致形象漂移。

| 可复用资产 | 路径 | 说明 |
|------------|------|------|
| 正面锚点图 | `out/views/front_v1.jpg` | 后续所有派生的源头 |
| 视觉锚点文本 | 本节 | 每条 prompt 必带 |

---

## 五、图片清单

| 图号 | 主体 | 场景 | 视角 | 所用技能 |
|------|------|------|------|----------|
| 1 | 视觉锚点 | 纯色简洁背景 | 正面全身 | T2I |
| 2 | 同 1 | 纯色简洁背景 | 正侧面 90° | 多视角 |
| 3 | 同 1 | 纯色简洁背景 | 背面 180° | 多视角 |
| 4 | 同 1 | 纯色简洁背景 | 四分之三侧面 45° | 多视角 |
| 5 | 同 1 | 竹林晨雾，青绿山水 | 正面 | 图像编辑 |
| 6 | 同 1 | 赛博都市夜景，霓虹光轨 | 正面 | 图像编辑 |
| 7 | 同 1 | 纯色背景 | 正面，月白汉服 | 图像编辑 |
| 8 | 同 1 | 纯色背景 | 正面，青绿舞裙 | 图像编辑 |
| 9 | 同 1 | 纯色背景 | 半身特写 | T2I |

---

## 六、Prompt & 参数

### 图 1：正面锚点（T2I · lite）

```bash
MODEL="doubao-seedream-5-0-lite"
arkcli +gen --model "$MODEL" \
  --size "1440x2560" --output-format jpeg --seed 42 \
  "东方少女，18 岁，虚构角色；黑长直发，发间一枚青玉簪；浅青水墨渐变纱裙，腰系月白缎带；赤足，脚踝银铃；身形纤细，气质清泠。青绿水墨画风，留白氛围。纯色简洁背景，全身正面像，中景，人物居中。" \
  --save-to out/views/
```

- 复现四元组：`lite` + 上述 prompt + `seed 42` + `1440x2560`

### 图 2：正侧面（多视角 · pro）

```bash
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @out/views/front_v1.jpg --size "1440x2560" --output-format jpeg \
  "保持@图像1中人物的形象、黑长直发、青玉簪、浅青水墨纱裙、月白缎带、银铃完全不变，改为正侧面 90° 视角全身像，纯色简洁背景。" \
  --save-to out/views/
```

### 图 3 / 4：背面 / 四分之三侧面

同图 2 模板，把视角替换为「背面 180°」「四分之三侧面 45°」；**都直接从 `front_v1.jpg` 派生**，不要从侧面图再派生。

### 图 5 / 6：换场景（图像编辑 · pro）

```bash
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @out/views/front_v1.jpg --size "2560x1440" --output-format jpeg \
  "人物形象、服装、发饰、配色保持完全不变，背景改为竹林晨雾、青绿山水，光线柔和一致。" \
  --save-to out/scenes/
```

### 图 7 / 8：换装扮（图像编辑 · pro）

```bash
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @out/views/front_v1.jpg --size "1440x2560" --output-format jpeg \
  "人物形象、五官、发型、姿势、背景保持完全不变，服装换成月白色汉服，材质丝绸，配色与整体青绿水墨风一致。" \
  --save-to out/lookbook/
```

### 图 9：半身特写（T2I · lite）

用视觉锚点 + "半身特写，1:1 方图，纯色背景"。

---

## 七、执行计划

| 阶段 | 模型 | 尺寸 | 目的 |
|------|------|------|------|
| 定向 | lite | 1440x2560 | 试 3~4 组视觉锚点措辞，选形象 |
| 定型 | lite | 1440x2560 | 固定 seed=42，出正面锚点图并过审 |
| 视角 | pro | 1440x2560 | 从锚点派生侧/背/半侧三视图 |
| 场景 | pro | 2560x1440 | 编辑换背景（竹林 / 赛博） |
| 装扮 | pro | 1440x2560 | 编辑换服装（汉服 / 舞裙） |
| 定稿 | lite | 2048x2048 | 半身头像 |

---

## 八、产出记录

| 图号 | 版本 | 模型 | seed | local_path | 备注 |
|------|------|------|------|------------|------|
| 1 | v1 | seedream-5.0-lite | 42 | out/views/front_v1.jpg | ✅ 锚点，定稿 |
| 2 | v1 | seedream-5.0-pro | - | out/views/side_v1.jpg | 派生自图1 |
| 3 | v1 | seedream-5.0-pro | - | out/views/back_v1.jpg | 派生自图1 |
| 4 | v1 | seedream-5.0-pro | - | out/views/three-quarter_v1.jpg | 派生自图1 |
| 5 | v1 | seedream-5.0-pro | - | out/scenes/bamboo_v1.jpg | 派生自图1 |
| 6 | v1 | seedream-5.0-pro | - | out/scenes/cyber_v1.jpg | 派生自图1 |
| 7 | v1 | seedream-5.0-pro | - | out/lookbook/hanfu_v1.jpg | 派生自图1 |
| 8 | v1 | seedream-5.0-pro | - | out/lookbook/dance-dress_v1.jpg | 派生自图1 |

> 实际执行后补齐模型返回的 seed 与真实文件名。

---

## 九、检查清单

- [ ] 角色为原创虚构，未指涉真人 / IP
- [ ] 正面锚点图已过审并锁定 seed
- [ ] 所有视角/场景/装扮均**直接从锚点图**派生
- [ ] 每张派生图已与锚点图逐项比对（发饰、服装、配色、银铃）
- [ ] 尺寸用 `--size`，比例与用途一致
- [ ] 全部产物已落盘，不依赖 24h URL
- [ ] 产出记录表已补齐 model + seed + 路径
- [ ] 若进视频：比例与 video-gen I2V 目标一致，见 [image-to-video-fastvideo3](../../../video-gen/skills/image-to-video-fastvideo3/SKILL.md)

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-02 | v1.0 | 新建示例项目：原创角色多角度/多场景/多装扮设定图库规划 | 小七 |
| 2026-10-02 | v1.1 | 随 `methods/`→`skills/` 改组：技能链接指向 SKILL.md，术语改为"技能" | 小七 |
| 2026-10-05 | v1.2 | 技能收敛后重映射：三个云端文档技能（text-to-image / multi-view-consistency / image-editing / multi-image-reference）已移除，改为「文生图 + 控制图生图 + 确定性工具」三件本地技能的可行路线；多图融合暂缺 | 小七 |
