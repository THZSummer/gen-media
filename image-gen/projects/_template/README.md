# 项目模板（_template）

> 返回[项目索引](../README.md) ｜ 技术技能见 [../../skills/](../../skills/README.md)

> 本目录是**模板**，复制后改写。不要在 _template 里直接做项目。

---

## 一、项目背景

- **项目名**：<项目名>
- **目标**：<一句话说清出什么图、给谁看、用在哪>
- **用途**：<分镜前置 / 海报封面 / 角色设定 / 电商详情 / 社媒配图 …>
- **交付时间**：<日期>

---

## 二、交付物清单

| # | 图用途 | 尺寸 | 比例 | 数量 |
|---|--------|------|------|------|
| 1 | <主图> | 2560x1440 | 16:9 | 1 |
| 2 | <竖版> | 1440x2560 | 9:16 | 1 |

---

## 三、技能选型

| # | 所用技能 | 链接 | 输入素材 |
|---|----------|------|----------|
| 1 | 文生图 | [text-to-image](../../skills/text-to-image/SKILL.md) | - |
| 2 | 图像编辑 | [image-editing](../../skills/image-editing/SKILL.md) | base.jpg |

> 按需组合 skills/ 下的技能。质量/成本权衡见 [quality-and-cost](../../skills/quality-and-cost/SKILL.md)，多视角一致性见 [multi-view-consistency](../../skills/multi-view-consistency/SKILL.md)，多图融合见 [multi-image-reference](../../skills/multi-image-reference/SKILL.md)。

---

## 四、图片清单

| 图号 | 主体 | 场景 | 视角 | 风格/色调 | 所用技能 |
|------|------|------|------|-----------|----------|
| 1 | <主体描述> | <场景> | 正面 | <风格> | T2I |
| 2 | 同 1 | 同 1 | 背面 | 同 1 | 多视角 |
| 3 | 同 1 | <新场景> | 正面 | 同 1 | 多图参考 |

---

## 五、Prompt & 参数

### 图 1

```bash
MODEL="<完整模型 ID，如 doubao-seedream-5-0-lite>"
arkcli +gen --model "$MODEL" \
  --size "2560x1440" --output-format jpeg --seed 42 \
  "<prompt，覆盖主体/场景/风格/构图四要素>" --save-to out/
```

- prompt：<…>
- 参数：size / output-format / seed / guidance-scale …
- 复现：seed=<…>（记录 model + prompt + seed + size 四元组）

### 图 2（编辑，pro 示例）

```bash
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @out/img1.jpg --size "2560x1440" --output-format jpeg \
  "把背景改成<新场景>，主体保持完全不变" --save-to out/edited/
```

---

## 六、执行计划

| 阶段 | 模型 | 尺寸 | 目的 |
|------|------|------|------|
| 定向 | lite | 目标比例小图 | 验证主体/风格/构图 |
| 定型 | lite | 目标尺寸 | 定 prompt 与 seed |
| 定稿 | lite/pro | 目标尺寸 | 出成品 |
| 衍生 | pro | 目标尺寸 | 编辑 / 多视角 / 多场景 |

详见 [quality-and-cost](../../skills/quality-and-cost/SKILL.md)。

---

## 七、产出记录

| 图号 | 版本 | 模型 | seed | local_path | 备注 |
|------|------|------|------|------------|------|
| 1 | v1 | seedream-5.0-lite | 42 | out/img1.jpg | 定稿 |
| 2 | v1 | seedream-5.0-pro | 7 | out/views/back_v1.jpg | 派生自图1 |

---

## 八、检查清单

- [ ] 模型 ID + profile 匹配正确
- [ ] 尺寸用 `--size` 且满足像素下限
- [ ] prompt 覆盖四要素
- [ ] 所有产物已落盘，不依赖 24h URL
- [ ] 定稿记录 model + prompt + seed + size
- [ ] 编辑器产物记录来源版本
- [ ] 若对接视频，图片比例与目标视频一致

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-02 | v1.0 | 新建图片项目模板 | 小七 |
| 2026-10-02 | v1.1 | 随 `methods/`→`skills/` 改组：链接指向 SKILL.md，术语改为"技能" | 小七 |
