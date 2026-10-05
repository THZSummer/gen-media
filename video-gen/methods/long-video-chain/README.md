# 长视频续接（Long-Video Chain）

> 把多条短视频首尾相接，串成连贯长片的主题。
> 返回[方法总览](../README.md) ｜ 核心机制：`--return-last-frame` 链式续接

---

## 一、主题定位

单条视频时长有限（默认 5s，模型上限通常 5-10s）。要做几十秒甚至几分钟的长内容，靠**续接**：用上一条的最后一帧作为下一条的首帧，逐段生成、首尾相接，形成连续长片。

### 何时需要续接

- 单条时长不够表达完整叙事
- 多镜头连续叙事（与 [cinematography](../cinematography/README.md) 分镜配合）
- 镜头跟随主体持续运动（跟拍、长镜头感）

### 何时不选

- 5s 够用 -> 直接单条生成
- 镜头之间是硬切（不需连续） -> 各自独立生成，后期剪辑拼接

---

## 二、续接机制

```
第1条: --input @first1.jpg --return-last-frame "镜头向右摇"
         │
         └─► 返回 last_frame_url (第1条末帧)
                 │
                 ▼ 下载作第2条首帧
第2条: --input @first2.jpg(=第1条末帧) --return-last-frame "镜头继续推进"
         │
         └─► 返回 last_frame_url (第2条末帧)
                 │
                 ▼ ...链式续接
第N条: ...
```

### 关键 flag

| flag | 作用 |
|------|------|
| `--return-last-frame` | 生成时额外返回最后一帧 URL，供下一条作首帧 | 
| `--input @<末帧图>` | 下一条用上一条返回的末帧当首帧 |

> ⚠️ **实测更新（2026-08-01）**：`doubao-seedance-2-0-260128` 支持 `--return-last-frame` 参数但**当前 +gen/gen get 响应中未返回 last_frame 字段**（实测 `--wait` 与 `gen get` 均无）——暂不可用。实测替代：**ffmpeg 从视频手动抽末帧**（`-sseof -0.1`）作下一条首帧。

### 衔接质量要点

- 上一条末帧 -> 下一条首帧**必须一致**，否则接缝跳变
- 用 `--return-last-frame` 返回的真末帧，**别另选一张图**当首帧
- 末帧 URL 也是预签名，**24h 失效**，及时下载落盘
- ⛔ **mini 模型不返回 last_frame_url**（--return-last-frame 被忽略），续接改走**两段式 I2V**：用 seedream 生成下一镜首帧静图，再 I2V 生视频
- ⚠️ **seedance-2.0 实测**：支持参数但响应无 last_frame 字段（见上表注释），需 ffmpeg 手动抽帧；且**视频帧可能触发真人隐私拦截**（`InputImageSensitiveContentDetected.PrivacyInformation`）——用 seedream 分镜图当首帧可规避

---

## 三、续接工作流

### 准备：分镜表

续接前先设计分镜（见 [cinematography](../cinematography/README.md) 分镜表模板），明确每段内容、运镜、衔接方式。

### 执行循环

```bash
VER=$(arkcli models get doubao-seedance-2-0 --transform 'primary_version' | tr -d '"')
MODEL="doubao-seedance-2-0-${VER:-260128}"

# 第1条：从首帧开始，拿末帧
arkcli +gen --model "$MODEL" --return-last-frame \
  --input @shot1_first.jpg --ratio 16:9 --resolution 720p \
  "镜头向右摇，展现街道" --wait --open
# -> 记下返回的 last_frame_url，下载为 shot2_first.jpg

# 第2条：用第1条末帧当首帧，再拿末帧
arkcli +gen --model "$MODEL" --return-last-frame \
  --input @shot2_first.jpg --ratio 16:9 --resolution 720p \
  "镜头继续推进，主角走入画面" --wait --open
# -> 下载末帧为 shot3_first.jpg

# 第N条：依此类推...
```

### 自动化脚本思路

```bash
# 伪代码
first="shot1_first.jpg"
for i in 1 2 3 ...; do
  resp=$(arkcli +gen --model "$MODEL" --return-last-frame \
    --input @"$first" --wait --format json "<shot$i prompt>")
  last_url=$(echo "$resp" | jq -r '.last_frame_url')   # 字段名以实际返回为准
  first="shot$((i+1))_first.jpg"
  curl -o "$first" "$last_url"                          # 下载末帧作下一条首帧
done
# 最后用 ffmpeg 把各段 mp4 拼接
```

> 字段名以 `--format json` 实际返回为准；末帧下载后**立即落盘**，URL 24h 失效。

---

## 四、参数选型

| 参数 | 续接建议 | 说明 |
|------|----------|------|
| `--return-last-frame` | 每条都加（除最后一条） | 拿末帧给下一条 |
| `--input` | 上一条末帧 | 首帧必须一致 |
| `--ratio` | 全链路统一 | 否则接缝处裁切 |
| `--resolution` | 全链路统一 | 否则画质跳变 |
| `--seed` | 全链路固定 | 保持画风一致 |
| `--wait` | 建议用 | 续接需顺序执行，同步等更省心 |
| `--draft` | 链路调试时用 | 定稿去掉 |

### 一致性是续接的生命线

```
ratio + resolution + seed 全链路一致  ──► 接缝平滑
任一参数变化                          ──► 接缝跳变/画风断裂
```

---

## 五、衔接方式对比

| 方式 | 连续性 | 实现 | 适用 |
|------|--------|------|------|
| **末帧续接** | 高（首尾相接） | `--return-last-frame` 链 | 长镜头、连续叙事 |
| 硬切拼接 | 低（独立镜头） | 各自生成 + 后期剪辑 | 节奏快的蒙太奇 |
| 动作衔接 | 中 | prompt 描述动作连续 + 续接 | 跟拍、运动延续 |

- 续接适合**需要画面连续**的场景
- 节奏快、镜头独立的多蒙太奇，直接硬切更自然，不必强续接

---

## 六、后期拼接

各段 mp4 生成后，用 ffmpeg 拼接：

```bash
# 1) 生成 concat 列表
for f in shot1.mp4 shot2.mp4 shot3.mp4; do echo "file '$f'"; done > list.txt

# 2) 无损拼接（要求编码/参数一致——续接时统一 ratio/resolution 正为此）
ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4

# 3) 参数不一致时重新编码
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -crf 18 out.mp4
```

> 续接时全链路统一 ratio/resolution/seed，正是为了让 `-c copy` 无损拼接可行。

---

## 七、踩坑点

| 现象 | 原因 | 处理 |
|------|------|------|
| 接缝跳变 | 末帧与下条首帧不一致 | 用 `--return-last-frame` 真末帧 |
| 画风断裂 | seed/分辨率/比例变化 | 全链路统一 ratio/resolution/seed |
| 末帧 URL 失效 | 超过 24h 才下载 | 生成后立即下载落盘 |
| 链路中断 | 某条失败 | 单条重试该段，不影响已生成段 |
| 拼接报错 | 各段编码不一致 | 统一参数或重新编码拼接 |
| 主角漂移 | 多段续接主体渐变 | 关键段用 I2V 首帧锁定主体 |

---

## 八、检查清单

- [ ] 先列分镜表，明确每段内容与衔接
- [ ] 全链路统一 `--ratio` `--resolution` `--seed`
- [ ] 每条加 `--return-last-frame`（除最后一条）
- [ ] 用上一条真末帧作下一条首帧
- [ ] 末帧 URL 立即下载落盘（24h 失效）
- [ ] 建议用 `--wait` 顺序执行
- [ ] 各段统一参数以便 ffmpeg 无损拼接
- [ ] 主角一致性用 I2V 首帧锁定

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-07-18 | v1.0 | 初始主题规划 | 小七 |
| 2026-07-18 | v1.1 | 标注 mini 模型不返回 last_frame_url，续接改走两段式 I2V 方案 | 小七 |
| 2026-08-01 | v1.2 | 实测 seedance-2.0 支持参数但响应无 last_frame 字段；补充真人隐私拦截规避（seedream 分镜图当首帧） | 小七 |
