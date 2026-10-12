---
name: comfyui-multi-angle
description: 通过本机 ComfyUI（默认 http://192.168.3.5:18000）把**一张图**一次生成**8 个不同角度**（Qwen-Image-Edit 2511 + Multiple-Angles LoRA，**本地模型、免费、可重复跑**）：8 个角度=特写/45°右/俯拍/广角/90°右/低机位/90°左/45°左，可 `--only` 只出几个、`--angle` 改角度提示词、`--fast/--no-fast` 切 4 步快档与 40 步慢档。**实测 8 张 1024×1024 约 4 分 46 秒（单张 35.7 s）**，脚本提交前打印 ETA。触发词：多角度、不同角度、一张图生成多视角、角色三视图/多视图、multiple angles、character angles、Qwen-Image-Edit 2511、多个机位、18000、192.168.3.5。
whenToUse: 当要**同一主体的一致多视角**时使用——角色设定图、人物多机位参考、给视频/图生视频准备多张不同机位的参考图、检查一张图的立体感。只要一张图、要本机免费重复跑就用它；要按提示词改图用 image-edit-comfyui 或 seedream-image-edit；要云端出图用 seedream-text-to-image；纯图片后处理用 image-tools。
---

# ComfyUI 一张图 → 8 个角度（Qwen-Image-Edit 2511 + Multiple-Angles LoRA）

**用途**：喂**一张参考图**，一次出**8 张同一主体、不同机位**的图。本机模型、**免费**、可固定
seed 重复跑；代价是**慢**——实测 **8 张 ≈ 4 分 46 秒**。

- 默认服务器：`http://192.168.3.5:18000`（`--server` 或 `$COMFYUI_SERVER` 覆盖）
- 工作流：`assets/qwen-2511-batch-angles-ui.json`（ComfyUI 官方模板 "1 Click Multiple Character
  Angles" 的导出图；**498 KB / 三级图层 / 展开后 193 节点**）
- 解剖与踩坑：[references/workflow-map.md](references/workflow-map.md)
- 权重（5 个文件，**本机已有**）：`qwen_image_edit_2511_bf16` / `qwen_2.5_vl_7b_fp8_scaled` /
  `qwen_image_vae` / `Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16` /
  `qwen-image-edit-2511-multiple-angles-lora`

## 与其它技能的边界

| 想要什么 | 用哪个 |
|---|---|
| **同一张图的多个机位/角度**（本机免费） | **本技能** |
| 按提示词**改**这张图（换背景/换装/局部） | [image-edit-comfyui](../image-edit-comfyui/SKILL.md) · [seedream-image-edit](../seedream-image-edit/SKILL.md) |
| 从零出图（本机 / 云端） | [text-to-image-comfyui](../text-to-image-comfyui/SKILL.md) · [seedream-text-to-image](../seedream-text-to-image/SKILL.md) |
| 拼版速览 / 比对 / 剥元数据 | [image-tools](../image-tools/SKILL.md) |

## 前置检查

```sh
cd .agents/skills/comfyui-multi-angle

python3 scripts/test_skill.py        # ① 离线自检 65 项（不需要服务器/GPU）
python3 scripts/comfyui_angles.py --list    # ② 看 8 个角度、5 个模型、快/慢档语义
python3 scripts/comfyui_angles.py --check   # ③ 真机：5 个模型 + 13 个节点类在不在
python3 scripts/comfyui_angles.py --image ref.png --plan   # ④ 免费：只验证接线，不提交不上传
```

## 成本与实测（2026-10-12 真机）

| 项 | 实测 |
|---|---|
| **8 个角度（快档 4 步）** | **285.8 s（4 分 46 秒）**，单张 **35.7 s** |
| 输入 | 1024×1024 PNG（上传 1.7 MB） |
| 输出 | **8 × 1024×1024 PNG**（尺寸由 `FluxKontextImageScale` 决定，没有 `--width/--height`） |
| 一致性（人眼核对） | `close_up` 是特写、`aerial_view` 是俯拍：**同一角色、同一服装/花冠**，机位确实变了 |
| 差异（数值） | 8 张两两平均绝对差 **42–60**（0–255 尺度），没有两张相同 |
| `--only 45_right,90_right` | 图内节点 **193 → 49**、KSampler **8 → 2**（真省时间，不是只丢输出） |
| ETA | 脚本按 **36 s/张** 估（实测 35.7）；`--plan` 也会先报 ETA |
| 慢档（`--no-fast`，40 步） | ⚠️ **未实测**，ETA 里的 150 s/张是粗估 |

## 参数

| 参数 | 作用 | 默认 |
|------|------|------|
| `--image` / `--image-name` | 参考图：本地文件（自动上传）／服务器 input 已有文件 | 必填其一 |
| `--only K1,K2` | **只出这些角度**（键见 `--list`），其余整段剪掉 | 全 8 个 |
| `--angle KEY=TEXT` | 改写某个角度的提示词（可重复） | 模板原文 |
| `--prompt-prefix` / `--prompt-suffix` | 给 8 条角度提示词统一加前后缀（如"保持服装一致"） | 空 |
| `--output-prefix NAME` | 输出前缀改成 `NAME/<角度名>`（便于一次跑出一组有名字的文件） | 模板前缀 |
| `--fast` / `--no-fast` | 快档（4 步 + cfg 1 + Lightning LoRA）／慢档（40 步 + cfg 4） | 模板为 `--fast` |
| `--seed` | 固定种子：8 个角度依次用 `seed, seed+1, …`（不传则沿用工作流里的随机种子） | — |
| `--unet-name` `--clip-name` `--vae-name` `--lora-name` `--lora-name-1` | 覆盖模型文件 | 工作流自带 |
| `--out-dir` / `--timeout` / `--poll` / `--quiet` / `--no-record` | 产物与留档 | `out` / 3600 / 5 / — / 留档开 |
| `--plan` | 免费：不提交、不上传，只验证接线与参数 | — |
| `--list` / `--check` | 离线看参数 / 真机看依赖 | — |

## 8 个角度（键 = 输出文件名）

| 键 | 角度提示词（模板原文） |
|---|---|
| `close_up` | `Turn the camera to a close-up.` |
| `45_right` | `Rotate the camera 45 degrees to the right.` |
| `aerial_view` | `Turn the camera to an aerial view.` |
| `wide_shot` | `Turn the camera to a wide-angle lens.` |
| `90_right` | `Rotate the camera 90 degrees to the right.` |
| `low_angle` | `Turn the camera to a low-angle view.` |
| `90_left` | `Rotate the camera 90 degrees to the left.` |
| `45_left` | `Rotate the camera 45 degrees to the left.` |

## 执行

```sh
# ① 先免费验证（不提交、不上传）
python3 scripts/comfyui_angles.py --image ref.png --output-prefix r1 --plan

# ② 全 8 个角度（≈5 分钟）
python3 scripts/comfyui_angles.py --image ref.png --output-prefix r1 \
    --seed 20261012 --out-dir out/

# ③ 只要两个机位（≈1 分 15 秒）
python3 scripts/comfyui_angles.py --image ref.png --only close_up,aerial_view --out-dir out/

# ④ 加"保持人物一致性"的约束 + 改一个角度
python3 scripts/comfyui_angles.py --image ref.png \
    --prompt-suffix "Keep the same face, hairstyle and outfit as the reference." \
    --angle aerial_view="Turn the camera to a high bird's-eye view." --out-dir out/

# ⑤ 慢档（40 步，更慢；本技能未实测耗时）
python3 scripts/comfyui_angles.py --image ref.png --no-fast --only close_up --out-dir out/
```

## 输出与留档

| 文件 | 内容 |
|------|------|
| `out/<角度名>.png` × N | 产物（按角度命名，不再用服务器那串 `ComfyUI-xxx_00001_`） |
| `out/multi-angle-<N>[-<prefix>].api.json` | 实际提交的完整 API 图（193 或剪枝后的节点） |
| `out/requests.jsonl` | 每行一次请求：参数 / `prompt_id` / **`elapsed_s`** / `per_angle_s` / 产物路径 |

**退出码**：0 正常 / 1 没有产物 / 2 参数问题 / 3 服务器不可达 / 4 缺模型或节点 / 5 超时。

## 踩坑点（都是实测踩出来的，详见 references/workflow-map.md）

1. **这是两级嵌套（顶层 → 父图 → 子图），共享转换器只可靠处理一级**：直接转换会**同时坏两头**——
   参考图**根本没进模型**（`FluxKontextImageScale.image = None`）、8 条输出连线**悬空**
   （指向父图内部实例 id）。本技能在转换前**把父图摊平**（`flatten_parent()`），回到一级嵌套；
   `validate()` 把"任何指向图外节点的连线"当硬错误。
2. **官方模板有两处输出前缀写错/重名**：45° 右被写成 `wide_shot`、90° 右被写成 `aerial_view`，
   与广角/俯拍撞名。资产里已改成 `45_right` / `90_right`，8 个前缀互不重复。
3. **父图内部连到接口的线用虚拟节点 `-10`**（`origin_slot` = 接口下标），不是接口 UUID；按 UUID 匹配会一条都对不上。
4. **`--only` 不能用 `node_modes` 实现**：`convert_ex(node_modes=...)` 是**按类名**生效的
   （`{"SaveImage": 4}` 会旁路掉全部输出），必须在 UI 上按**节点 id** 设 `mode=4`，再做可达性剪枝。
5. **快档开关的取值只认"子图实例上的 widget"**：改父图实例的 `value` 无用（转换器不透传实例接口值）、
   改子图**定义**里的 `PrimitiveBoolean` 也无用（被实例覆盖）——必须改 8 个子图**实例**的 `value`。
6. **子图自带 `image2`/`image3` 两个参考输入，但父图没接线**：转换时会打 16 条 warning，属**预期**
   （它们是可选项，服务器接受）。要双参考得自己接线。
7. **尺寸不受参数控制**：`FluxKontextImageScale` 按 Kontext 预置档定尺寸，输出与输入同比例。

## 验证记录

| 项 | 结果 |
|----|------|
| 离线自检 `scripts/test_skill.py` | ✅ **65/65 PASS**（解剖/开关语义/摊平+转换/参数落图/负向对照/CLI） |
| 真机 `--check` | ✅ `ok: true`：5 个模型文件 + 13 个节点类全在（ComfyUI 0.39.0） |
| 真机 `--plan` | ✅ 8 个输出、193 节点、**0 悬空连线**、无未落图参数 |
| **真机出片（2026-10-12）** | ✅ `status: success`，**285.8 s**，8 × 1024×1024 PNG，单张 35.7 s |
| 人眼核对 | ✅ `close_up` 特写 / `aerial_view` 俯拍：同一角色同一服装，机位确实变了 |
| 数值对照 | ✅ 8 张两两平均绝对差 42–60，无两张相同 |
| `--only` 省时 | ✅ 图内节点 193 → 49、KSampler 8 → 2 |
| 慢档 `--no-fast` | ❌ 未实测（仅离线验证开关语义与图结构） |
| `image2/image3` 双参考 | ❌ 未做（父图未接线） |

## 检查清单

- [ ] `scripts/test_skill.py` → `65/65 checks passed`
- [ ] `--check`：`ok: true`（缺模型会点名；按工作流 MarkdownNote 里的链接下载）
- [ ] `--plan` 通过：输出数 = 想要的角度数、`dangling_links` 为空
- [ ] 首次出片先用 `--only` 挑 2 个角度验方向（≈1 分 15 秒），再上全 8 个
- [ ] 需要复现时给 `--seed`（8 个角度依次 `seed..seed+7`）
- [ ] 大体积中间产物（`work/`、`out/`）未入库

## 修订记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-10-12 | v1.0 | **建立并真机验证**：以官方模板 "1 Click Multiple Character Angles" 的导出图为资产（498 KB / 三级图层 / 193 节点）；脚本 `comfyui_angles.py` 提供 `--list / --check / --plan / 生成`，支持 `--only`（按节点 id 旁路 + 可达性剪枝）、`--angle`、前后缀、`--output-prefix`、`--fast/--no-fast`、`--seed`。**新增 `flatten_parent()`**：把两级嵌套摊平成一级（否则参考图丢失 + 8 条连线悬空）；`validate()` 加图完整性检查。修正官方模板两处输出前缀错名。实时测：8 张 285.8 s（单张 35.7 s）、0 悬空、人眼与数值双核对；离线自检 65/65 |
