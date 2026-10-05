# 文生图（Text-to-Image, T2I / Seedream）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 输入：prompt。输出：静态图片。当前走 `doubao-seedream-5-0-lite`（Agent Plan Medium 含，agent-plan profile）。
> 返回[方法总览](../README.md)

---

## 一、主题定位

文生图是**从文字生成静态画面**的路径：给一段描述，拿一张图。在视频生成流程里，它主要作为**前置工序**：

| 用途 | 说明 |
|------|------|
| **分镜图 / 关键帧** | 先出每镜的静态构图，人工审核后再 I2V 动起来（返工防火墙） |
| **I2V 首帧** | seedream 生首帧 → mini I2V 续动（两段式工作流） |
| **海报 / 封面** | 短视频封面、社媒配图、详情页图 |
| **概念验证** | 低成本验证画面风格/色调/构图是否符合预期 |

### 与视频路径的区别

| | 文生图 T2I（本篇） | 文生视频 T2V |
|---|------------------|--------------|
| 输出 | 静态图片 | 动态视频 |
| 耗时/成本 | 低（同步返回） | 高（异步 + token 多） |
| 动感 | 无 | 有 |
| 典型用法 | 分镜图、首帧、封面 | 成片 |

> 推荐流程：**先 T2I 出图审核 → 再 I2V 动起来**，不要直接用 T2V 猜画面。

---

## 二、模型与路由

当前两个 Seedream 生图模型可选（2026-08-01 实测）：

| 项 | `doubao-seedream-5-0-lite` | `doubao-seedream-5-0-pro` |
|----|---------------------------|---------------------------|
| 定位 | Agent Plan Medium 含，轻量 | 独立按量，**精准图像编辑** |
| 完整 ID | `doubao-seedream-5-0-lite` | `doubao-seedream-5-0-pro-260628` |
| Profile | agent-plan（默认，勿用 Auto） | ⚠️ **platform 按量**（`--profile platform_cn-beijing_accountwide`，不支持 agent-plan） |
| 像素下限 | ⚠️ ≥3,686,400（1920×1080 被拒） | ✅ 无下限（1920×1080 可用） |
| 核心能力 | 文生图 | 文生图 + **图生图编辑**（改背景/改元素/换场景，主体可保持） |
| 返回 | 图片同步返回（区别于视频异步） | 同左 |
| 成本 | 图片按张计费 | 同左 |

> 🔀 路由注意：
> - lite 走 **agent-plan** 默认 profile；pro 走 **platform 按量**（pro 调 agent-plan 会报 "does not support the agent plan feature"）。
> - `doubao-seedance-2-0-mini`（视频）也走 platform 按量；seedream lite（图片）走 agent-plan。三者路由别混。
> - pro 模型名须用**完整版本 ID** `doubao-seedream-5-0-pro-260628`（族名 `doubao-seedream-5-0-pro` 在 platform 数据面 NotFound，控制面可见但数据面未部署）。

### pro 的图像编辑能力（核心价值）

```
文生图生成一张基础图 ──► 拿它当 --input 参考图 ──► 编辑指令改背景/元素/场景
                        （人物主体可保持不变）
```

实测（2026-08-01）：
- 把"竹林少女"的**背景改成赛博都市**成功，人物保持一致 → 对「移步换景」类项目是利器：**同一张人物图，改背景即换景**
- 编辑时 `--input @图` + 编辑指令 prompt，`--size`/`--output-format` 同文生图

### pro 图生图扩展能力（2026-08-02 实测新增）

| 能力 | 做法 | 实测 |
|------|------|------|
| **单图编辑** | `--input @图` + 编辑指令 | ✅ 改姿势/背景/元素，主体保持 |
| **多图参考** | 多个 `--input @图`，prompt 用 `@图像1/@图像2` 引用 | ✅ 角色图+场景图融合（"把@图像1的蝴蝶女放入@图像2的书桌"） |
| **参考图生成新视角** | `--input @正面图` + "改为背面/侧面视角，形象服装翅膀不变" | ✅ 正面→背面，形象保持一致 |

> **价值**：多角度角色图库可以**用参考图递归生成**（正面图→生成背面/侧面），比独立生成（每张凭空画）形象一致性高得多。prompt 里强调"保持@图像N的形象/服装/翅膀不变，只改视角/姿势"。

---

## 三、命令模板

### 单张生成

```bash
# lite（agent-plan 默认）
MODEL="doubao-seedream-5-0-lite"
arkcli +gen --model "$MODEL" \
  --size "2560x1440" --output-format jpeg \
  "<prompt>" --save-to out/

# pro（platform 按量，完整版本 ID；无像素下限，1920x1080 可用）
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --size "2560x1440" --output-format jpeg \
  "<prompt>" --save-to out/
```

> ⚠️ **图片比例用 `--size`，不用 `--ratio`**：`--ratio` 仅对视频任务生效，图片任务传了会被忽略（seedream 默认出 2048×2048 正方形）。`--size` 写具体像素。

### pro 图像编辑（改背景/换场景）

```bash
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @base.jpg --size "2560x1440" --output-format jpeg \
  "把背景改成赛博都市夜景，霓虹灯箱与车流光轨，人物保持完全不变" --save-to out/
```

> 适用场景：同一人物换背景（移步换景）、海报元素替换、局部精修。人物保持依赖编辑指令强调"人物保持完全不变"。

### 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--size` | 输出尺寸（像素，必须 ≥3,686,400 像素） | `2560x1440`（16:9）/ `1440x2560`（9:16）/ `2048x2048`（1:1） |
| `--output-format` | 输出格式 | `jpeg` / `png` |
| `--image-count` / `--n` | 一次出多张 | `--image-count 4`（>1 时自动顺序出图） |
| `--seed` | 固定随机种子，复现 | `--seed 42` |
| `--guidance-scale` | 提示词遵循度（float） | `7.5` |
| `--optimize-prompt` | 服务端 prompt 优化 | 开/关 |
| `--response-format` | 返回方式 | `url` / `b64_json` |
| `--stream` | 流式输出（仅图片） | NDJSON |
| `--save-to` | 落盘目录 | `out/storyboard/` |

> ⚠️ 竖屏/横屏按 `--size` 像素写，**不要横图硬裁**成竖图（构图会变形）。

---

## 四、Prompt 策略

与 T2V 同源，但强调**静态构图**：

1. **主体明确**：谁 + 穿什么 + 在哪（如"现代舞者，女性，浅青水墨渐变纱裙，发髻简洁"）
2. **场景明确**：背景 + 光（如"淡雅茶室，木质、纸屏、暖光"）
3. **色调/风格明确**：青绿水墨、留白、氛围感
4. **构图明确**：景别（全景/中景/特写）+ 画面重点
5. **静态瞬间**：取最有代表性的定格（"举盏亮相"），动态过程交给 I2V

### 分镜图场景

取该镜**最有代表性的静态瞬间**，不描述动态：

```
<通用视觉锚点> + <该镜关键姿态描述，如：舞者双手捧盏低头凝神，茶烟升腾，淡雅茶室，青绿水墨色调，留白氛围>
```

> 具体见 [projects/tea-shake-dance §4.3](../../projects/tea-shake-dance/README.md)（分镜图生成与审核清单）。

---

## 五、踩坑点

- **模型 ID 完整**：`doubao-seedream-5-0-lite`（5.0 用点号）或 `doubao-seedream-5-0-pro-260628`（pro 必须带版本，族名在 platform 数据面 NotFound）
- **profile 路由**：lite → agent-plan 默认；pro → ⚠️ **platform 按量**（pro 走 agent-plan 报 "does not support the agent plan feature"）
- **同步语义**：图片是同步返回的，不需要 `gen get` 轮询（那是视频）
- **`--input` 不加（文生图）**：T2I 是纯文生图，没有参考图；pro 编辑场景才加 `--input`
- **⚠️ 图片比例用 `--size` 不用 `--ratio`**：`--ratio` 是 video task 专属，图片任务传了被忽略 → 默认出 2048×2048 正方形，与视频比例不一致。用 `--size "2560x1440"`（16:9）等像素值。
- **⚠️ 像素下限（仅 lite）**：lite 要求 ≥ 3,686,400 像素（≈2048×1800），1920×1080 会被拒；**pro 无下限**（1920×1080 实测可用）。常用尺寸：`2560x1440`（16:9）、`1440x2560`（9:16）、`2048x2048`（1:1）
- **I2V 衔接**：生成的分镜图要落盘留档（`--save-to` / 手动 mv），因为预签名 URL 24h 失效

---

## 六、检查清单

- [ ] 模型 ID 完整（lite 无版本 / pro 带 -260628）
- [ ] profile 正确（lite→agent-plan / pro→platform 按量）
- [ ] 用 `--size` 指定像素尺寸（含宽高比），非 `--ratio`
- [ ] lite 需 ≥3,686,400 像素（pro 无下限）
- [ ] prompt 含主体/场景/色调/构图
- [ ] 图片已落盘（local_path），不依赖 24h URL
- [ ] 分镜图已过审（如适用，见项目 §4.3）

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-08-01 | v1.0 | 初始版本：文生图方法（seedream-5.0-lite），覆盖分镜图/首帧/封面用法，含命令模板、参数、prompt 策略、踩坑点 | 小七 |
| 2026-08-01 | v1.1 | 实测修正：图片比例用 `--size` 而非 `--ratio`（`--ratio` 仅视频有效，忽略后默认 2048×2048 正方形）；记录 size 像素下限 3,686,400（1920×1080 被拒）及合规尺寸 | 小七 |
| 2026-08-01 | v1.2 | 新增 seedream-5.0-pro：platform 按量路由、完整版本 ID、无像素下限（1920×1080 可用）、核心卖点"精准图像编辑"（改背景/换场景保人物，实测竹林→赛博成功）；模型对比表 + 命令模板 + 踩坑点更新 | 小七 |
| 2026-08-02 | v1.3 | 实测新增 pro 图生图扩展：多图参考（@图像N 引用融合）+ 参考图生成新视角（正面→背面保形象），多角度图库可递归生成 | 小七 |
