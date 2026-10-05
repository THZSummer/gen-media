# 质量与成本控制（Quality & Cost）

> 在画面质量、生成速度、成本之间做权衡的横切主题，适用于所有输入路径。
> 返回[方法总览](../README.md)

---

## 一、主题定位

视频生成比图片贵得多、慢得多。盲目全开 1080p + 长时长 + 高优先级，单条成本可能数倍于草稿模式。本主题给出一套**分阶段、按需取舍**的参数策略，让钱花在刀刃上。

### 核心矛盾

| 维度 | 高质量 | 低成本 |
|------|--------|--------|
| 分辨率 | 1080p | 480p |
| 时长 | 长 | 短 |
| 模式 | 正式 | `--draft` 草稿 |
| 优先级 | `--priority 9` | `--priority 0` |
| 速度 | 慢 | 快 |

---

## 二、分阶段策略（推荐工作流）

### 阶段 1：定向（用最便宜配置试方向）

```
--draft --resolution 480p --duration 5 --priority 0
```
- 目的：验证 prompt/构图/运动方向是否对，**不追求画质**
- 成本最低、速度最快
- 可反复迭代 prompt，多试几版

### 阶段 2：定型（中等配置定方案）

```
--resolution 720p --duration 5        (去掉 draft)
```
- 目的：在可接受画质下确认最终方案
- 720p 是**性价比甜点**，多数场景够用

### 阶段 3：定稿（高质量出成品）

```
--resolution 1080p --duration <需要> --priority 9
```
- 目的：出最终交付件
- 只在方案确定后跑一次，避免重复高成本生成

> 原则：**便宜的多试，贵的一次**。不要一上来就 1080p 瞎试。

---

## 三、参数详解

### `--resolution` 分辨率

| 值 | 用途 | 成本 |
|----|------|------|
| `480p` | 草稿/定向 | 最低 |
| `720p` | 性价比甜点、多数场景 | 中 |
| `1080p` | 定稿/交付 | 最高 |

- 受模型支持范围约束（Step 2 查 supported_params 的 enum）
- 低清图配高分辨率无意义（I2V 场景）

### `--duration` / `--frames` 时长

| 参数 | 说明 |
|------|------|
| `--duration` | 视频秒数，模型上限通常 5-10s |
| `--frames` | 帧数，在支持的模型上覆盖 duration |

- 时长越长成本越高（近似线性甚至超线性）
- 超长需求走 [long-video-chain](../long-video-chain/README.md) 续接，别强求单条

### `--draft` 草稿模式

- 更快、更便宜、质量更低
- **定向阶段必用**，定稿必须去掉
- 适合批量试方向
- ⛔ **fast 和 mini 不支持 --draft**（被拒：param_not_supported），定向阶段改用 480p 低保真替代

### `--priority` 优先级

- 范围 `0-9`，越高越优先调度
- **受模型支持约束**：实测 seedance-2.0 / 2.0-fast 支持 `[0,9]`，**1.5-pro 不支持**，传了被拒
- 紧急出片用高优先级；不急用低优先级省钱（低优先级可能排队更久但单价可能更低，以实际计费为准）

### `--seed` 复现

- 相同 seed + 相同参数 = 复现
- 定向阶段固定一个 seed，微调 prompt 时保持画面一致性
- 换 seed = 换一版随机结果

---

## 四、成本敏感场景策略

### 批量出样稿

```bash
# 多版 prompt 用 draft + 480p 快速跑，挑最好的
for p in "版本A..." "版本B..." "版本C..."; do
  arkcli +gen --model "$MODEL" --draft --resolution 480p "$p" --open
done
```
- 批量场景省略 `--open`（>4 张批量别弹窗）

### 单条高质量

```bash
# 方案确定后，只跑一次 1080p
arkcli +gen --model "$MODEL" --resolution 1080p --priority 9 \
  "<定稿 prompt>" --open
```

### 竖屏短视频

```bash
# 短视频平台，9:16，720p 多数够用
arkcli +gen --model "$MODEL" --ratio 9:16 --resolution 720p --duration 5 \
  "<prompt>" --open
```

---

## 五、模型选择对成本的影响

| 模型 | 成本/速度 | 质量 | 适用 |
|------|-----------|------|------|
| `doubao-seedance-2-0-fast` | 快/便宜 | 中 | 批量、定向 |
| `doubao-seedance-2-0` | 中 | 高 | 定型、定稿 |
| `doubao-seedance-1-5-pro` | 慢/贵 | 高 | 质量优先、不急 |
| `doubao-seedance-2-0-mini` | 中等 | 中 | ⚠️ 按量仅此可用，不支持 draft/priority/last-frame |

- 定向阶段用 fast 省钱省时
- 定稿切 2.0 或 1.5-pro
- 1.5-pro 不支持 `--priority`，别传

---

## 六、命令模板

```bash
VER=$(arkcli models get doubao-seedance-2-0-fast --transform 'primary_version' | tr -d '"')
FAST="doubao-seedance-2-0-fast-${VER:-260128}"

# 阶段1 定向：最便宜
arkcli +gen --model "$FAST" --draft --resolution 480p --duration 5 --priority 0 \
  "<试方向 prompt>" --open

# 阶段2 定型：720p
arkcli +gen --model "$FAST" --resolution 720p --duration 5 \
  "<定方案 prompt>" --open

# 阶段3 定稿：1080p 高优先级
VER2=$(arkcli models get doubao-seedance-2-0 --transform 'primary_version' | tr -d '"')
PRO="doubao-seedance-2-0-${VER2:-260128}"
arkcli +gen --model "$PRO" --resolution 1080p --priority 9 \
  "<定稿 prompt>" --open
```

---

## 七、踩坑点

| 现象 | 原因 | 处理 |
|------|------|------|
| 一上来 1080p 反复试 | 没分阶段 | 定向用 draft+480p |
| `--priority` 被拒 | 1.5-pro 不支持 | 换 2.0 系列或去掉 priority |
| 草稿当成品 | 忘了去 `--draft` | 定稿必须去掉 draft |
| 单条超长太贵 | 强求单条长视频 | 走续接拆多条 |
| 画风每版不同 | seed 随机 | 定向阶段固定 seed |
| 低清图配 1080p | 浪费成本 | I2V 分辨率匹配素材 |

---

## 八、检查清单

- [ ] 分三阶段：定向(480p+draft) -> 定型(720p) -> 定稿(1080p)
- [ ] 定向用 fast 模型，定稿用 2.0/1.5-pro
- [ ] 定向阶段固定 `--seed` 保一致性
- [ ] 定稿去掉 `--draft`
- [ ] `--priority` 只在支持模型上用（2.0/2.0-fast）
- [ ] 批量场景省略 `--open`
- [ ] 超长需求走续接，不强求单条

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-07-18 | v1.0 | 初始主题规划 | 小七 |
| 2026-07-18 | v1.1 | 标注 fast/mini 不支持 --draft；新增 mini 模型行；定向改 480p 替代 draft | 小七 |
