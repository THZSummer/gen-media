# 项目：荒岛求生（Survival Island）

> 返回[项目索引](../README.md) ｜ 技术方法见 [../../methods/](../../methods/README.md)

---

## 一、项目背景

- **项目名**：荒岛求生（survival-island）
- **核心概念**：**荒岛不荒，人更惨** -- 极致反差。热带孤岛是碧海白沙、椰林繁花的世外桃源；而一名约十八岁的东方少女海难后衣衫褴褛、晒伤干裂、跌跌撞撞地在这座天堂般的岛上求生。**岛越美，人越惨，反差即主题**。
- **目标**：约 30 秒剧情短片，6 个镜头呈现少女**登岛 -> 寻水 -> 生火 -> 搭庇护所 -> 夜宿望海**的求生一天，以"天堂与地狱并置"的反差传达孤独与坚韧。
- **发布渠道**：
  - 主片：作品集 / 长视频平台，横版 16:9
  - 衍生：短视频平台竖版 9:16 精编版
- **交付时间**：2026-07-25
- **风格基调**：电影感、35mm 胶片质感；**岛用高饱和暖阳天堂调，人用低饱和冷峻苦难调**，同框反差不调和

---

## 二、交付物清单

| # | 视频用途 | 时长 | 比例 | 分辨率 | 说明 |
|---|----------|------|------|--------|------|
| 1 | 主片（横版） | ~30s | 16:9 | 1080p | 6 镜 × 5s 续接 |
| 2 | 竖版精编 | ~25s | 9:16 | 1080p | 精选 5 镜，去镜 4 或 5 |

---

## 三、方法选型

### 整体策略

荒岛场景**无现成素材**，以 **T2V 为主**从零构思画面；为保**主角一致性**，关键镜头用**两段式**（seedream 生静图当首帧 -> seedance I2V）。多镜头用 [long-video-chain](../../methods/long-video-chain/README.md) 续接。

| # | 所用方法 | 链接 | 输入素材 |
|---|----------|------|----------|
| 镜 1/4/6 | 文生视频 T2V | [text-to-video](../../methods/text-to-video/README.md) | - |
| 镜 2/3/5 | 两段式：图生视频 I2V | [image-to-video](../../methods/image-to-video/README.md) | seedream 生成首帧 |
| 全片 | 镜头运镜 | [cinematography](../../methods/cinematography/README.md) | - |
| 全片 | 长视频续接 | [long-video-chain](../../methods/long-video-chain/README.md) | `--return-last-frame` 链 |
| 全片 | 质量成本 | [quality-and-cost](../../methods/quality-and-cost/README.md) | 分阶段 |
| 全片 | 内容安全 | [content-safety](../../methods/content-safety/README.md) | 见下方安全策略 |

### 主角一致性策略（剧情片核心难点）

纯 T2V 多镜头主角会漂移。对策：

1. **固定主角描述前缀**（每镜 prompt 都带）：`"一名约十八岁的东方少女，黑色长发凌乱披散，晒伤泛红的皮肤，干裂的嘴唇，破损的浅色长袖衬衫与长裤，浑身泥沙"`
2. **I2V 镜头先用 seedream 生成统一主角形象的首帧**，再让 seedance 动起来（首帧锁定主体）
3. **全链路固定 `--seed`**，保持画风一致
4. **续接时用上一镜真末帧**作下一镜首帧，衔接处主角自然延续

### 反差手法（主题表达）

| 元素 | 岛（天堂） | 人（苦难） |
|------|-----------|-----------|
| 饱和度 | 高饱和 | 低饱和 |
| 色温 | 暖阳 | 冷峻 |
| 关键词 | 碧玉海水、白沙、椰林、繁花、清澈溪流、璀璨银河 | 衣衫褴褛、晒伤、干裂、泥沙、擦伤、颤抖、蜷缩 |
| 构图 | 明信片般开阔 | 局促、疲态 |

同框并置，**不调和**--这是本片的视觉骨架。

### 内容安全策略（本片关键：惨烈需过审）

"惨烈"用**可过审的苦难符号**表达，绝不触血腥/暴露红线。`--force` 绕不过内容审核，必须从 prompt 源头控制。

| 要表达 | ✅ 安全用词 | ❌ 避免用词（会被拦） |
|--------|-----------|---------------------|
| 受伤 | 伤痕累累、擦伤、晒伤脱皮 | 流血、伤口特写、血肉模糊、残肢 |
| 疲惫 | 跌跌撞撞、颤抖、蜷缩、干裂 | （无敏感） |
| 衣物破损 | 破损的衬衫长裤、衣衫褴褛 | 暴露、清凉、半裸、透视 |
| 绝望 | 泪痕、绝望眼神 | 自伤、轻生暗示 |

原则：
- 少女为**虚构成年**角色，定位"坚韧求生"，不渲染受虐/脆弱性感化
- 镜头偏**脸部 / 手部 / 上半身**，避免具暗示性的全身构图
- 被拦按 [content-safety](../../methods/content-safety/README.md) 逐项排除，优先弱化具体伤情描述

---

## 四、分镜表

> 6 镜 × 5s = 30s 主片。运镜一次只一种，衔接以续接为主、硬切调节奏。

| 镜号 | 景别 | 运镜 | 内容 | 时长 | 衔接 | 所用方法 |
|------|------|------|------|------|------|----------|
| 1 | 远景 | 航拍推近 | 碧玉海水环抱白沙孤岛、椰林繁花，少女抱木板在浪中漂流，与天堂海岛格格不入 | 5s | 硬切 | T2V |
| 2 | 全景 | 跟拍 | 少女跌跌撞撞冲上洁白沙滩，衣衫褴褛，背后是明信片般海岸线 | 5s | 续接 | I2V（首帧） |
| 3 | 中景 | 跟移 | 郁郁葱葱雨林繁花似锦，少女拨开树叶扑向清澈溪流俯身饮水 | 5s | 续接 | I2V（首帧） |
| 4 | 特写 | 固定 | 少女擦伤颤抖的双手钻木取火，火苗燃起，暖光照亮伤痕 | 5s | 硬切 | T2V |
| 5 | 全景 | 固定延时 | 椰林花丛间搭起简陋庇护所，黄昏柔和光线如度假村 | 5s | 续接 | I2V（首帧） |
| 6 | 中景 | 固定夜景 | 璀璨银河下，少女蜷缩篝火旁望星空，衣衫褴褛眼神坚毅 | 5s | 结尾 | T2V |

### 反差弧线

```
镜1 天堂海面   vs 漂流少女（孤绝）
镜2 天堂沙滩   vs 狼狈登岛（狼狈）
镜3 丰饶雨林   vs 干渴扑水（渴求）
镜4 暖光火苗   vs 伤痕双手（转机）
镜5 度假黄昏   vs 简陋庇护（安顿）
镜6 绝美银河   vs 蜷缩少女（坚毅）
```

---

## 五、Prompt & 参数

> 主角描述统一前缀：`一名约十八岁的东方少女，黑色长发凌乱结块披散，晒伤脱皮泛红的皮肤，干裂起皮的嘴唇，衣衫褴褛的浅色长袖衬衫撕成碎条半挂在身上，长裤破洞遍布磨损成毛边，袖口裤脚散线，浑身泥污擦伤，狼狈不堪如落难乞丐`
> 🏝️ 岛视觉锚点（每镜必带，保证跨镜头同一座岛）：`同一座热带孤岛：碧玉般海水环抱新月形白沙海岸，椰林摇曳，鸡蛋花与三角梅繁花似锦`
> 画风统一后缀：`电影感，35mm 胶片质感，浅景深`
> 反差统一手法：岛高饱和暖阳，人低饱和冷峻，同框不调和
> 🎯 **实际模型**：`doubao-seedance-2-0-mini-260615`（按量 platform，`--profile platform_cn-beijing_accountwide`）
> ⚠️ mini 不支持 `--draft` / `--return-last-frame`；续接改走两段式 I2V（seedream 生首帧）
> 🔇 mini 无音频输出（`modalities.output` 仅 video），本片声音走后期合成（海浪环境音 + 氛围乐），见音频设计节

### 镜 1（T2V · 航拍推近）

```bash
MODEL="doubao-seedance-2-0-mini-260615"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --ratio 16:9 --resolution 480p --duration 5 \
  "同一座热带孤岛：碧玉般海水环抱新月形白沙海岸，椰林摇曳，鸡蛋花与三角梅繁花似锦，航拍视角缓缓推近，海浪轻拍礁石，一名约十八岁的东方少女，黑色长发凌乱结块披散，晒伤脱皮泛红的皮肤，干裂起皮的嘴唇，衣衫褴褛的浅色长袖衬衫撕成碎条半挂在身上，长裤破洞遍布磨损成毛边，袖口裤脚散线，浑身泥污擦伤，狼狈不堪如落难乞丐，抱着木质浮板在浪中艰难漂流，与天堂般的孤岛格格不入，逆光，电影感，35mm 胶片质感，浅景深" \
  --open
```
- ⚠️ mini 不返回 last_frame，续接走两段式 I2V（见镜 2）

### 镜 2（两段式 I2V · 跟拍）

```bash
# 先 seedream 生成主角登岛首帧（带岛锚点，保证与镜 1 同一座岛）
arkcli +gen --model doubao-seedream-5-0-260128 --size 1920x1080 \
  "同一座热带孤岛：碧玉般海水环抱新月形白沙海岸，椰林摇曳，鸡蛋花与三角梅繁花似锦，一名约十八岁的东方少女，黑色长发凌乱结块披散，晒伤脱皮泛红的皮肤，干裂起皮的嘴唇，衣衫褴褛的浅色长袖衬衫撕成碎条半挂在身上，长裤破洞遍布磨损成毛边，浑身泥污擦伤，狼狈不堪，跌坐在洁白沙滩上，背后是碧玉海水椰林明信片般海岸线，电影感，35mm 胶片质感" --open
# 满意后用静图当首帧
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @shot2_first.jpg --ratio 16:9 --resolution 480p --duration 5 \
  "镜头跟拍，少女跌跌撞撞在洁白沙滩上前行，衣衫褴褛碎条翻飞，海风吹动破损衣角，回头望向天堂般的大海，电影感，35mm 胶片质感，浅景深" \
  --open
```
- 首帧 seedream 生成后存为 `shot2_first.jpg`；mini 不返回 last_frame，镜 3 续接另起首帧

### 镜 3（两段式 I2V · 跟移）

```bash
arkcli +gen --model doubao-seedream-5-0-260128 --size 1920x1080 \
  "热带雨林郁郁葱葱繁花似锦阳光斑驳，一名约十八岁的东方少女站在丛林边缘，黑色长发凌乱，破损浅色衬衫长裤，电影感，35mm 胶片质感" --open
arkcli +gen --model "$MODEL" --input @shot3_first.jpg \
  --ratio 16:9 --resolution 1080p --duration 5 \
  "镜头跟移，少女拨开宽大热带树叶繁花走进雨林，扑向一条清澈溪流俯身饮水，光影斑驳" \
  --return-last-frame --open
```
- 末帧下载为 `shot5_first.jpg`（镜 4 是 T2V 硬切，末帧给镜 5）

### 镜 4（T2V · 特写固定）

```bash
arkcli +gen --model "$MODEL" --camera-fixed \
  --ratio 16:9 --resolution 1080p --duration 5 \
  "特写，一名少女擦伤泛红、沾满泥沙的双手在颤抖着快速钻木取火，木屑冒烟，火苗突然燃起，暖橙色光照亮手指上的伤痕，浅景深，固定镜头，电影感" \
  --open
```
- 硬切，不续接（节奏点）

### 镜 5（两段式 I2V · 固定延时）

```bash
arkcli +gen --model doubao-seedream-5-0-260128 --size 1920x1080 \
  "椰林花丛间用树枝和椰子叶搭起的简陋庇护所半成品，黄昏柔和暖光如度假村，碧海背景，电影感" --open
arkcli +gen --model "$MODEL" --input @shot5_first.jpg --camera-fixed \
  --ratio 16:9 --resolution 1080p --duration 5 \
  "固定镜头延时摄影，树枝椰叶庇护所在花丛间逐渐搭建完成，黄昏柔和光线快速变化，海浪起伏" \
  --return-last-frame --open
```
- 末帧下载为 `shot6_first.jpg`

### 镜 6（T2V · 固定夜景）

```bash
arkcli +gen --model "$MODEL" --camera-fixed \
  --ratio 16:9 --resolution 1080p --duration 5 \
  "夜晚热带海滩，璀璨银河横跨夜空，篝火噼啪燃烧，一名约十八岁的东方少女衣衫褴褛蜷缩在火旁望向星空与大海，火光映在晒伤的脸上，眼神疲惫却坚毅，固定镜头，电影感，35mm 胶片质感" \
  --open
```

### 复现与一致性

- 全链路固定 `--seed 7`（定向阶段锁定，定稿沿用）
- 主角描述前缀、画风后缀、反差手法全 6 镜统一
- I2V 镜头 prompt 只写**运动**，外观交给首帧

---

## 六、执行计划

| 阶段 | 配置 | 目的 | 范围 |
|------|------|------|------|
| 定向 | `--draft --resolution 480p` `seed=7` | 验证 ①反差是否成立 ②少女一致性 ③"惨烈"描述是否过审 | 6 镜全跑一遍 |
| 定型 | `--resolution 720p`（去 draft）`seed=7` | 确认分镜衔接、反差弧线 | 重点镜 1/2/6 |
| 定稿 | `--resolution 1080p --priority 9` `seed=7` | 出成品，逐镜续接 | 6 镜 + ffmpeg 拼接 |

> 定向用 `doubao-seedance-2-0-fast` 省钱省时；定稿切 `doubao-seedance-2-0`。
> 详见 [quality-and-cost](../../methods/quality-and-cost/README.md)。

### 续接执行顺序

```
镜1(T2V) --末帧--> 镜2(I2V) --末帧--> 镜3(I2V)
                                          │ (镜4硬切，镜3末帧留给镜5)
                                          ▼
镜4(T2V,独立)   镜5(I2V,首帧=镜3末帧) --末帧--> 镜6(T2V 或 I2V)
```

> 镜 3 与镜 5 之间是硬切（中间插入镜 4 特写），镜 3 末帧直接作镜 5 首帧即可保证场景连贯。

### 后期拼接

```bash
# 各镜统一 ratio/resolution/seed，可无损拼接
for f in shot1.mp4 shot2.mp4 shot3.mp4 shot4.mp4 shot5.mp4 shot6.mp4; do
  echo "file '$f'"
done > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy survival-island.mp4
```

---

## 七、产出记录

| 镜号 | 版本 | task_id | local_path | 备注 |
|------|------|---------|------------|------|
| 1 | v2 | cgt-20260718180426-rd7sm | out/shot1.mp4 | 480p 定向 ✅；新前缀+岛锚点；旧版 out/shot1_v1.mp4 |
| 2 | v2 | cgt-20260718180428-wpfdk | out/shot2.mp4 | 480p 定向 ✅；新前缀+岛锚点；原 I2V 改 T2V；旧版 out/shot2_v1.mp4 |
| 3 | v1 | cgt-20260718175645-s4v2t | out/shot3.mp4 | 480p 定向 ✅；新前缀+岛锚点；原 I2V 改 T2V（seedream 未激活）|
| 4 | v1 | cgt-20260718174806-rfkp8 | out/shot4.mp4 | 480p 定向 ✅；新前缀+岛锚点 |
| 5 | v1 | cgt-20260718180034-vtr4r | out/shot5.mp4 | 480p 定向 ✅；新前缀+岛锚点；原 I2V 改 T2V（seedream 未激活）|
| 6 | v1 | cgt-20260718175253-mj7zm | out/shot6.mp4 | 480p 定向 ✅；新前缀+岛锚点 |

> 完整拼接预览：`out/survival_island_full.mp4`（6 镜 × 5s ≈ 30s，11MB，h264/864×496/24fps，静音轨）
> 镜 1/2 已用新前缀重做（v2），旧版 v1 保留备份；6 镜全部统一新前缀+岛锚点

> 每镜生成后回填 task_id 与 local_path；`output_url` 24h 失效，依赖 local_path。

---

## 八、检查清单

- [ ] 6 镜 prompt 均含统一主角前缀（东方少女）+ 画风后缀
- [ ] 反差手法到位：岛高饱和暖阳 vs 人低饱和冷峻，同框不调和
- [ ] "惨烈"只用安全苦难符号（擦伤/晒伤/衣衫褴褛/干裂/泪痕），**无血腥/暴露**用词
- [ ] 少女为虚构成年角色，镜头偏脸部/手部/上半身，无暗示性全身构图
- [ ] I2V 镜头 prompt 只写运动，不重复外观
- [ ] 全链路 `--seed 7` 保画风一致
- [ ] `--model` 用完整版本化 ID（非族名）
- [ ] 各镜参数在 `supported_params` 范围内（定稿用 2.0 才能开 `--priority`）
- [ ] 定向/定型/定稿三阶段执行
- [ ] 续接用 `--return-last-frame` 真末帧，不另选图
- [ ] 末帧 URL 立即下载落盘
- [ ] 各镜 ratio/resolution 统一以便 ffmpeg 无损拼接
- [ ] 若被拦按 [content-safety](../../methods/content-safety/README.md) 逐项排除，优先弱化伤情描述

---

## 九、音频设计（旁白配音）

> 因 mini 无音频输出，走后期配音：TTS 生成旁白 → ffmpeg 混音入视频。

### 旁白脚本（反差弧线叙事）

| 镜号 | 旁白 | 时长 |
|------|------|------|
| 1 | 天堂般的海岛，与一个被遗忘的灵魂。 | 4.3s |
| 2 | 她爬上洁白的沙滩，离开了海，却没离开孤独。 | 4.8s |
| 3 | 丰饶的雨林里，她只为了一口水而拼命。 | 3.9s |
| 4 | 火光亮起的那一刻，绝望也成了希望。 | 4.3s |
| 5 | 黄昏柔美如度假，她却用残枝搭起今夜的床。 | 4.7s |
| 6 | 银河璀璨，她蜷缩在火旁，眼里有不灭的光。 | 4.4s |

### TTS 生成

- 模型：`doubao-seed-tts-2.0`（Agent Plan，Resource-Id = `seed-tts-2.0`）
- 音色：`zh_female_vv_uranus_bigtts`（沉稳女声旁白）
- 脚本：`scripts/tts_narration.py`（调用 OpenSpeech 流式 API，base64 解码拼接）
- 输出：`out/narration_<镜号>.mp3`

```bash
python3 scripts/tts_narration.py          # 生成全部 6 段旁白
```

### 混音流程

```bash
# 1. 每段旁白补静音到尾音，与视频时长对齐（5.088s）
for n in 1 2 3 4 5 6; do
  ffmpeg -i narration_$n.mp3 -af apad -t 5.088 narration_${n}_pad.mp3
done

# 2. 拼接 6 段成完整 30s 音轨（重编码避免 DTS 错乱）
printf "file 'narration_1_pad.mp3'\n...file 'narration_6_pad.mp3'\n" > concat_audio.txt
ffmpeg -f concat -safe 0 -i concat_audio.txt -c:a libmp3lame -b:a 128k narration_full.mp3

# 3. 混入视频（⚠️ 关键：不要重编码为 aac，播放器可能不识别！mp3 直塞 mp4 即可）
ffmpeg -i survival_island_full.mp4 -i narration_full.mp3 \
  -c:v copy -c:a copy -map 0:v -map 1:a -shortest survival_island_narrated.mp4
```

> 成品：`out/survival_island_narrated.mp4`（30.8s，旁白配音版）
> ⚠️ 实测 `-c:a aac` 重编码后播放器无声音（音轨有数据但解码失败），`-c:a copy` 保留 mp3 原样即可。

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-07-18 | v1.0 | 荒岛求生项目初始规划（6 镜 30s 剧情短片） | 小七 |
| 2026-07-18 | v1.1 | 改为约 18 岁东方少女 + 极致反差（荒岛不荒、人更惨）；新增反差手法与内容安全策略，重写全部分镜与 prompt | 小七 |
| 2026-07-18 | v1.2 | 实际使用 doubao-seedance-2-0-mini-260615（platform 按量）；标注 mini 不支持 draft/return-last-frame；记录镜 1/2 产出 | 小七 |
| 2026-07-18 | v1.3 | 确认 mini 无音频输出（output 仅 video），声音改走后期合成 | 小七 |
| 2026-07-18 | v1.4 | 强化破败感前缀（撕碎条/破洞/毛边/散线/泥污擦伤）；新增岛视觉锚点解决跨镜头环境一致性 | 小七 |
| 2026-07-18 | v1.5 | 6 镜定向全部完成；镜 3/5 因 seedream 未激活改 T2V；完整拼接 survival_island_full.mp4；记录 profile 路由（mini->platform，其余->agent-plan）| 小七 |
| 2026-07-18 | v1.6 | 镜 1/2 用新前缀+岛锚点重做（v2），旧版留 v1 备份；6 镜全部统一新前缀 | 小七 |
| 2026-07-18 | v1.7 | 新增音频设计：旁白脚本 + TTS 生成（seed-tts-2.0）+ ffmpeg 混音流程；成品 survival_island_narrated.mp4 | 小七 |
| 2026-07-18 | v1.8 | 修复配音无声：混音改 `-c:a copy`（mp3 直塞 mp4），aac 重编码致播放器不识别 | 小七 |
