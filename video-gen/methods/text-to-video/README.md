# 文生视频（Text-to-Video）

> 输入：仅一段文字描述。输出：动态视频。
> 返回[方法总览](../README.md) ｜ 适用模型：Seedance 系列（T2V 路径）
> 📚 **官方教程（seedance-2.0 多模态/音效/编辑）**：<https://ark.volcengine.com/region:cn-beijing/docs/82379/2298881?lang=zh>（含 @视频/@图像/@音频 参考输入、音效描述、视频延长编辑等官方示例）

---

## 一、主题定位

文生视频是**从零构思**的路径：手里没有图片、没有参考视频，只有一段脑海中的画面描述。它是视频生成的基线能力，也是验证 prompt 表达力最直接的场景。

### 何时选 T2V

- 抽象概念、超现实画面（没有现成素材可拍）
- 快速验证一个镜头想法是否成立
- 没有图、但文字描述足够具体
- 作为其他路径的对照基线

### 何时不选

- 已有静图想让它动起来 -> 去 [image-to-video](../image-to-video/README.md)
- 想复刻某段运镜/动作 -> 去 [reference-video](../reference-video/README.md)

---

## 二、能力映射

| 控制维度 | T2V 下的可用手段 |
|----------|----------------|
| 画面内容 | 纯靠 prompt 描述 |
| 镜头运动 | prompt 内描述 + `--camera-fixed` 固定镜头 |
| 时长 | `--duration` / `--frames`（受模型支持范围约束） |
| 分辨率/比例 | `--resolution` `--ratio` |
| 复现 | `--seed` 相同种子复现 |
| 音频 | `--generate-audio` 同步生成 | ✅ 1.5-pro / 2.0（260128，实测 2026-08-01）；⛔ 2.0-fast / mini 无音频 |
| 出样 | `--draft` 草稿模式快速预览 |

---

## 三、Prompt 策略

文生视频的成败 **80% 在 prompt**。模型没有图片兜底，描述不到位画面就糊。

### 推荐结构（四段式）

```
[主体] + [动作/状态] + [场景/环境] + [镜头语言 + 风格 + 光影]
```

**示例（好）**：
> 一只柴犬在樱花树下奔跑，慢镜头，花瓣随风飘落，午后逆光，电影感调色，浅景深

**示例（差，太笼统）**：
> 一只狗在跑

### 要点

| 要素 | 说明 | 例子 |
|------|------|------|
| 主体 | 越具体越好，避免"一个人""一只动物" | "穿红色卫衣的少年" |
| 动作 | 明确动词与时态，描述运动方向 | "从画面左侧跑入，向镜头靠近" |
| 场景 | 交代环境、天气、时间 | "雨后城市街道，傍晚，霓虹倒影" |
| 镜头 | 推/拉/摇/移/跟/固定；慢镜头/延时 | "镜头缓慢拉远，主体居中保持不动" |
| 风格 | 写实 / 动画 / 赛博 / 胶片 | "35mm 胶片质感，颗粒感" |
| 光影 | 逆光 / 侧光 / 黄金时刻 | "黄金时刻侧逆光" |

### 反模式（容易翻车）

- 纯形容词堆砌，无主体动作 -> 画面静止或乱动
- 多主体 + 多动作 -> 模型顾此失彼，主体跳变
- 过长复杂句 -> 关键信息被稀释，建议拆成短句逗号分隔
- 写"不要出现 XX" -> 模型对否定描述弱，正面描述更有效

---

## 四、参数选型

### Step 2 查可用参数

```bash
arkcli models get "$MODEL" --transform supported_params
```

- `supported_params` 非空：**只用列出的参数**，取值落 min/max/enum 内
- `supported_params` 为空：`+gen` 自动套 video 兜底默认（`resolution=720p` / `duration=5` / `ratio=adaptive`），不手动填

### 常用参数

| 参数 | 建议值 | 说明 |
|------|--------|------|
| `--ratio` | `16:9` / `9:16` / `1:1` | 横屏/竖屏/方形，按发布渠道选 |
| `--resolution` | `720p` 起步，定稿 `1080p` | 见 [quality-and-cost](../quality-and-cost/README.md) |
| `--duration` | `5`（默认） | 模型上限通常 5-10s，超长走续接 |
| `--seed` | 固定一个 | 微调 prompt 时复现画面一致性 |
| `--draft` | 出样阶段用 | ⛔ fast/mini 不支持，用 480p 替代 |
| `--camera-fixed` | 静态构图用 | 固定虚拟镜头，避免意外运镜 |

---

## 五、命令模板

```bash
# 0. 补全完整模型 ID（不要自己猜版本号）
VER=$(arkcli models get doubao-seedance-2-0 --transform 'primary_version' | tr -d '"')
MODEL="doubao-seedance-2-0-${VER:-260128}"

# 1. 标准文生视频（异步，返回 task_id）
arkcli +gen --model "$MODEL" \
  --ratio 16:9 --resolution 720p --duration 5 \
  "一只柴犬在樱花树下奔跑，慢镜头，花瓣飘落，午后逆光，电影感，浅景深" \
  --open

# 2. 同步等结果（阻塞到完成）
arkcli +gen --model "$MODEL" --wait --open \
  "城市夜景航拍，霓虹灯流，延时摄影" 

# 3. 出样稿（草稿模式快速看方向）
arkcli +gen --model "$MODEL" --draft --resolution 480p \
  "赛博朋克街道，雨夜，主角回头" --open

# 4. 固定种子复现微调
arkcli +gen --model "$MODEL" --seed 42 \
  "森林清晨，雾气，光束穿过树冠" --open
```

### 拿到 task_id 后轮询

```bash
arkcli gen get <task_id> --open   # 轮到 succeeded 自动下载 + 桌面弹出
```

---

## 六、踩坑点

| 现象 | 原因 | 处理 |
|------|------|------|
| 404 `InvalidEndpointOrModel.NotFound` | `--model` 传了族名 | 用 `models get ... --transform primary_version` 补全完整 ID |
| 提交后"没反应" | 视频异步，`queued` 非失败 | `gen get <task_id>` 轮询，别重提 |
| 主体跳变/糊 | prompt 主体动作不清 | 强化主体+动作描述，减少并列 |
| 意外运镜 | 模型自行脑补镜头 | 加 `--camera-fixed` 或在 prompt 写明镜头 |
| 参数被拒 `param_not_supported` | 模型不支持该参数 | 回 Step 2 看 supported_params，如 1.5-pro 不支持 `--priority` |
| 画面被审核拦截 | prompt 含敏感词 | 见 [content-safety](../content-safety/README.md) |

---

## 七、检查清单

- [ ] `--model` 是完整版本化 ID（非族名）
- [ ] 已查 `supported_params`，参数都在支持范围内
- [ ] prompt 四段式：主体+动作+场景+镜头风格
- [ ] 比例/分辨率匹配发布渠道
- [ ] 出样阶段用 `--draft`，定稿再升 1080p
- [ ] 需要复现时锁定 `--seed`
- [ ] 记下 `task_id`，用 `gen get` 轮询而非重提
- [ ] 成品已落 `local_path`（URL 24h 失效）

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-07-18 | v1.0 | 初始主题规划 | 小七 |
| 2026-07-18 | v1.1 | 标注 --draft fast/mini 不支持，改 480p | 小七 |
| 2026-07-18 | v1.2 | 标注 --generate-audio 仅 1.5-pro 支持，2.0 系列无音频输出 | 小七 |
| 2026-08-01 | v1.3 | 修正：实测 seedance-2.0（260128）支持 --generate-audio 输出真音频；2.0-fast/mini 仍无音频 | 小七 |
