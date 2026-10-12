# 工作流解剖：Qwen-Image-Edit 2511 多角度批量（8 角度）

> 返回[技能首页](../SKILL.md)

> 这些事实来自**静态解剖**（`assets/qwen-2511-batch-angles-ui.json`，498 KB）与**真机实测**
> （`--check` / `--plan` / 一次 8 角度出片），不是从官方文档抄的。踩到的两个坑写在 §4。

## 1. 图层结构（三级）

```text
顶层（11 个节点）
├── LoadImage #25                 ← 唯一的参考图
├── MarkdownNote #75              ← 模型下载链接（前端专有节点，转换时剔掉）
├── SaveImage ×8  (#373 374 376 377 379 380 381 424)
└── 父图实例 #427  type=6b6e4ec3…  "Qwen-Image 2511: Batch Angle Generation"
        └── 父图内部 8 个子图实例（各自 type = 一个独立的子图定义 id）
                └── 子图 "Image Edit (Qwen-Image 2511 with LoRA)"（24 节点，8 份独立定义）
```

- 展开后 **193 个节点**：8 × (UNETLoader / CLIPLoader / VAELoader / 2×LoraLoaderModelOnly /
  2×TextEncodeQwenImageEditPlus / KSampler / VAEEncode / VAEDecode /
  FluxKontextImageScale / 2×FluxKontextMultiReferenceLatentMethod / ModelSamplingAuraFlow /
  CFGNorm / VAEloader / 3×ComfySwitchNode / 2×PrimitiveFloat / 2×PrimitiveInt /
  PrimitiveBoolean) + 1×LoadImage + 8×SaveImage。
- 8 份权重加载器看着重复，实际 ComfyUI 按文件缓存 → **只加载一次**。

## 2. 8 个角度（顺序 = 父图 `outputs` 声明顺序，**不是** JSON 里节点的排列顺序）

| 槽 | 角度键 | 提示词（原文） | SaveImage |
|---|---|---|---|
| 0 | `close_up` | `Turn the camera to a close-up.` | #373 |
| 1 | `45_right` | `Rotate the camera 45 degrees to the right.` | #374 |
| 2 | `aerial_view` | `Turn the camera to an aerial view.` | #376 |
| 3 | `wide_shot` | `Turn the camera to a wide-angle lens.` | #379 |
| 4 | `90_right` | `Rotate the camera 90 degrees to the right.` | #380 |
| 5 | `low_angle` | `Turn the camera to a low-angle view.` | #377 |
| 6 | `90_left` | `Rotate the camera 90 degrees to the left.` | #381 |
| 7 | `45_left` | `Rotate the camera 45 degrees to the left.` | #424 |

⚠️ **按文件里的节点顺序读会张冠李戴**：#377(low_angle) 在 JSON 里排在 #379(wide_shot) 之前，
但槽位顺序是 #379 在前。脚本因此按**父图 `outputs[].linkIds → 内部连线 → 子图实例 id`** 建表。

⚠️ **官方模板有两处输出前缀写错/重名**：#374（45° 右）写成 `wide_shot`、#380（90° 右）写成
`aerial_view`，与 #379/#376 撞名。本技能的资产已改成 `ComfyUI-45_right` 与 `ComfyUI-90_right`，
8 个前缀互不重复（`test_skill.py` 钉住这一点）。文件名不会覆盖（ComfyUI 会自动加序号），
但**名字对不上角度**会让一整套图无法使用。

## 3. 快档 / 慢档：`value`（enable_turbo_mode）开关

子图内部有三个 `ComfySwitchNode`，全部由同一个布尔值驱动：

| 开关 | on_true | on_false |
|---|---|---|
| Switch (Steps) → `KSampler.steps` | `PrimitiveInt` **4** | `PrimitiveInt` **40** |
| Switch (CFG) → `KSampler.cfg` | `PrimitiveFloat` **1** | `PrimitiveFloat` **4** |
| Switch (Model) → `KSampler.model` | 走 Lightning LoRA 的模型 | 不走 Lightning 的模型 |

- `value=True`（模板默认）= **快档**：4 步 + cfg 1 + Lightning 4steps LoRA
- `value=False` = **慢档**：40 步 + cfg 4
- CLI 的 `--fast` / `--no-fast` 就是它。

## 4. 两个实测踩到的坑（都已修，别退回去）

### 4.1 这是**两级嵌套**，共享转换器只可靠处理一级

`顶层 → 父图 → 子图`。直接把这份 UI 图丢给 `comfyui_convert.convert_ex()` 会**同时坏两头**：

| 侧 | 症状（实测） |
|---|---|
| 输入 | 子图内部 `FluxKontextImageScale.image` 变成 `None` —— **参考图根本没进模型**，出来的会是纯噪声/纯文本结果 |
| 输出 | 8 个 `SaveImage.images` 指向 `['221', 0]` 这类**父图内部实例 id**，而这些 id **不在展开后的图里** → 提交判"找不到节点" |

**修法（`flatten_parent()`）**：转换前把父图这一层摊平——把 8 个子图实例提到顶层（新 id），
父图接口里**真正是连线**的（这里只有 `image`）改接到真实上游（`LoadImage`），
子图输出按槽位接回 8 个 `SaveImage`，然后删掉父图实例。摊平后回到**一级嵌套**，
正是转换器与兄弟技能验证过的形态：

- 摊平前：8 条悬空连线 + `FluxKontextImageScale.image = None`
- 摊平后：0 条悬空 + 参考图被 8 个角度各引用一次（`['25', 0]`）

`validate()` 现在把"**任何指向图外节点的连线**"当硬错误（正是这类坑的通用检测器）。

### 4.2 父图内部连到接口的线用**虚拟节点 -10**，不是接口 UUID

`origin_id: -10` + `origin_slot` = **接口下标**（`-20` 是输出侧）。用 UUID 去匹配会一条都匹配不上，
表现就是"参考图没接进去"。摊平器按下标查接口名。

## 5. `--only` 是怎么省时间的

未选中角度的 `SaveImage` 在 UI 上被标 `mode=4`（bypass）→ 转换时丢弃 → 再做一次
**从输出出发的可达性剪枝**（`prune_unreachable`），把没人依赖的分支整段删掉：

| 场景 | 图内节点 | KSampler |
|---|---|---|
| 8 个角度 | 193 | 8 |
| `--only 45_right,90_right` | **49** | **2** |

> 注：`convert_ex(node_modes=...)` 是**按类名**生效的（`{"SaveImage": 4}` 会旁路掉全部 SaveImage），
> 所以精确旁路必须在 UI 上按**节点 id**设 `mode`。

## 6. 参考图与产物

- **输入**：一张图（`LoadImage`）。子图里还有 `image2` / `image3` 两个可选参考输入，但**父图没接线**，
  所以转换后 `TextEncodeQwenImageEditPlus` 不带 `image2/image3` —— 这是模板原样，属**可选输入**，
  服务器接受（转换器会为它们打 warning，是预期的）。
- **尺寸**：由 `FluxKontextImageScale` 决定（Kontext 系预置档），**没有** `--width/--height`；
  输出尺寸与输入比例相关。
- **产物**：8 张 PNG，前缀即角度名（本技能资产已修正）。

## 7. 未做 / 待验证

- [ ] `image2/image3` 多参考（父图未接线，要自己接线才能用）
- [ ] `--no-fast`（慢档 40 步）真机耗时未实测（ETA 里的 150 s/张是粗估）
- [ ] 与官方 MarkdownNote 里列的 2509 版本模型混用（本模板实际用的是 **2511** 系列文件）
