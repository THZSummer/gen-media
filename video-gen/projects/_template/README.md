# 项目模板（_template）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[项目索引](../README.md) ｜ 技术方法见 [../../methods/](../../methods/README.md)

> 本目录是**模板**，复制后改写。不要在 _template 里直接做项目。

---

## 一、项目背景

- **项目名**：<项目名>
- **目标**：<一句话说清做什么视频、给谁看>
- **发布渠道**：<电商详情 / 短视频平台 / 长视频 / 社媒 / …>
- **交付时间**：<日期>

---

## 二、交付物清单

| # | 视频用途 | 时长 | 比例 | 分辨率 |
|---|----------|------|------|--------|
| 1 | <主视频> | 5s | 16:9 | 1080p |
| 2 | <竖屏版> | 5s | 9:16 | 1080p |

---

## 三、方法选型

| # | 所用方法 | 链接 | 输入素材 |
|---|----------|------|----------|
| 1 | 图生视频 | [image-to-video](../../methods/image-to-video/README.md) | 产品图 first.jpg |
| 2 | 文生视频 | [text-to-video](../../methods/text-to-video/README.md) | - |

> 按需组合 methods/ 下的方法。质量/成本权衡见 [quality-and-cost](../../methods/quality-and-cost/README.md)，多镜头续接见 [long-video-chain](../../methods/long-video-chain/README.md)，镜头运镜见 [cinematography](../../methods/cinematography/README.md)。

---

## 四、分镜表

| 镜号 | 景别 | 运镜 | 内容 | 时长 | 衔接 | 所用方法 |
|------|------|------|------|------|------|----------|
| 1 | 中景 | 环绕 | <内容> | 5s | 续接 | I2V |
| 2 | 特写 | 固定 | <内容> | 5s | 硬切 | T2V |

---

## 五、Prompt & 参数

### 镜号 1

```bash
MODEL="<完整模型 ID，如 doubao-seedance-2-0-260128>"
arkcli +gen --model "$MODEL" \
  --input @first.jpg --ratio 16:9 --resolution 1080p \
  "<prompt>" --open
```

- prompt：<…>
- 参数：ratio / resolution / duration / seed …
- 复现：seed=<…>

---

## 六、执行计划

| 阶段 | 配置 | 目的 |
|------|------|------|
| 定向 | draft + 480p | 验证方向 |
| 定型 | 720p | 定方案 |
| 定稿 | 1080p + priority | 出成品 |

详见 [quality-and-cost](../../methods/quality-and-cost/README.md)。

---

## 七、产出记录

| 镜号 | 版本 | task_id | local_path | 备注 |
|------|------|---------|------------|------|
| 1 | v1 | <task_id> | <path> | |

---

## 八、检查清单

- [ ] 每条视频已选方法并链接 methods/
- [ ] prompt 已按方法 README 策略编写
- [ ] 模型 ID 完整（非族名）
- [ ] 参数在 supported_params 范围内
- [ ] 分阶段执行（定向 / 定型 / 定稿）
- [ ] 产出已落 local_path（URL 24h 失效）
- [ ] 内容已过审（见 [content-safety](../../methods/content-safety/README.md)）

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-07-18 | v1.0 | 项目模板初始版本 | 小七 |
