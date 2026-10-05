# 项目模板（_template）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[项目索引](../README.md) ｜ 技能见 [../../.agents/skills/](../../.agents/skills/README.md) ｜ 视频方法见 [../../methods/](../../methods/README.md)

> 本目录是**模板**，复制后改写。不要在 _template 里直接做项目。
> 图片与视频项目共用这一个模板：按需保留「图片清单」或「分镜表」章节即可。

---

## 一、项目背景

- **项目名**：<项目名>
- **目标**：<一句话说清出什么、给谁看、用在哪>
- **类型**：<图片 / 视频 / 图片＋视频>
- **发布渠道**：<小红书 / 短视频平台 / 电商详情 / 社媒 / …>
- **交付时间**：<日期>

---

## 二、交付物清单

| # | 用途 | 尺寸或时长 | 比例 | 数量 |
|---|------|------------|------|------|
| 1 | <主图 / 主视频> | <1024x1360 / 5s> | <3:4 / 16:9> | 1 |
| 2 | <竖版> | <1080x1440 / 9:16> | <3:4 / 9:16> | 1 |

---

## 三、技能 / 方法选型

| # | 所用技能或方法 | 链接 | 输入素材 |
|---|----------------|------|----------|
| 1 | 文生图 | [text-to-image-comfyui](../../.agents/skills/text-to-image-comfyui/SKILL.md) | - |
| 2 | 控制图生图 | [image-edit-comfyui](../../.agents/skills/image-edit-comfyui/SKILL.md) | base.png（控制图） |
| 3 | 图生视频 | [image-to-video-fastvideo3](../../.agents/skills/image-to-video-fastvideo3/SKILL.md) | first.jpg |
| 4 | 合图 / 比对 / 剥元数据 | [image-tools](../../.agents/skills/image-tools/SKILL.md) | 成品图 |

> 全部技能见 [.agents/skills/](../../.agents/skills/README.md)（5 个，都带脚本与自检入口）。
> 云端视频方法（Seedance）见 [methods/](../../methods/README.md)。
> 每个技能的第一件事都是**自检**：`--check` 或 `test_skill.py`，环境不健康就别提交任务。

---

## 四、图片清单 / 分镜表

图片项目用这张（视频项目可删）：

| 图号 | 主体 | 场景 | 视角 | 风格/色调 | 所用技能 |
|------|------|------|------|-----------|----------|
| 1 | <主体描述> | <场景> | 正面 | <风格> | T2I |

视频项目用这张（图片项目可删）：

| 镜号 | 景别 | 运镜 | 内容 | 时长 | 衔接 | 所用技能/方法 |
|------|------|------|------|------|------|---------------|
| 1 | 中景 | 环绕 | <内容> | 5s | 续接 | I2V |

---

## 五、Prompt & 参数

### 图 / 镜 1（本地 ComfyUI 文生图）

```bash
cd .agents/skills/text-to-image-comfyui
python3 scripts/comfyui_gen.py --check          # 先自检
python3 scripts/comfyui_gen.py \
  --prompt "<prompt：主体 + 场景 + 风格 + 构图>" \
  --width 1024 --height 1360 --steps 12 --seed 42 --out-dir out/
```

- prompt：<…>
- 参数：width / height / steps / seed
- 复现：记录 **模型 + prompt 原文 + 参数 + seed** 四元组（`--out-dir` 会自动留档 `.api.json` 与 `requests.jsonl`）

### 镜 2（本地 ComfyUI 图生视频）

```bash
cd .agents/skills/image-to-video-fastvideo3
python3 scripts/comfyui_i2v.py --check
python3 scripts/comfyui_i2v.py --first first.jpg --prompt "<prompt>" --out-dir out/
```

### 备选：云端视频（Seedance，按量计费）

```bash
arkcli resources list --modality video                    # 查可用模型
arkcli models get "$MODEL" --transform supported_params   # 查参数
arkcli +gen --model "$MODEL" --input @first.jpg --ratio 16:9 --resolution 1080p "<prompt>" --open
```

---

## 六、执行计划

| 阶段 | 配置 | 目的 |
|------|------|------|
| 定向 | 小图 / 低步数（或 480p draft） | 验证方向：主体 / 风格 / 构图 |
| 定型 | 目标尺寸 / 中步数（或 720p） | 定 prompt 与 seed |
| 定稿 | 目标尺寸 / 高步数（或 1080p） | 出成品 |
| 衍生 | `image-edit-comfyui` 以定稿为控制图 | 换场景 / 换装扮 / 补角度 |

> 计费路径的取舍见 [quality-and-cost](../../methods/quality-and-cost/README.md)，多镜头续接见 [long-video-chain](../../methods/long-video-chain/README.md)。

---

## 七、产出记录

| 图/镜号 | 版本 | 模型 | seed / task_id | local_path | 备注 |
|---------|------|------|----------------|------------|------|
| 1 | v1 | z-image-turbo | seed 42 | out/img1.png | 定稿 |

---

## 八、检查清单

- [ ] 技能 `--check` / `test_skill.py` 通过
- [ ] prompt 覆盖四要素（主体 / 场景 / 风格 / 构图）
- [ ] 产物已落盘 **local_path**，不依赖 24h 失效的 URL
- [ ] 定稿记录 模型 + prompt 原文 + 参数 + seed（或 task_id）
- [ ] 比例与下游对齐（若对接视频，图片比例需与目标视频一致）
- [ ] 定稿已脱敏（`image-tools` 的 `ffkit strip`）
- [ ] 大体积中间产物（`work/`、`out/r*/`）未入库
- [ ] 文档已中英成对（`README.md` + `README.en.md`）

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-02 | v1.0 | 项目模板初始版本（图片侧） | 小七 |
| 2026-07-18 | v1.0 | 项目模板初始版本（视频侧） | 小七 |
| **2026-10-05** | **v2.0** | **扁平化合并**：图片与视频两个 `_template` 合并为本模板；示例命令改为当前的本地 ComfyUI 技能，云端 Seedance 降为备选 | 小七 |
