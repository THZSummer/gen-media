# 第四期 · 合龙

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/dn-r7-review.md)
> 引擎：Z-Image-Turbo　1024×1024　steps 12　**全 3 张共用 seed 4201**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点

**雨中岩石高地 · 黄昏逆光 + 雨丝 · 广角低机位 35mm · 横幅 1280×1024**

收官期要的是**气势**：湿岩、雨丝、逆光把鹿角剪影映在天光上，
湿鳞反光勾出体表质感。四件叠加（角 2 处 + 前后肢各 1 处）在这个呈现下读作
**真正的龙形生物**，而不是"同一只蜥蜴加了配件"。

## 二、本期主题：把可行的部件叠到同一个体上

到第三期为止，九似里可行的部件是：**角 D1（头）、耳 D9（头）、爪 D7（前肢）、掌 D8（后肢）**。
本期的「合龙」把它们叠到同一个体上，同时压住规律 59 的**区域边界**：

| 变体 | 叠加 | 区域分布 | 是否越界 |
|------|------|----------|----------|
| `dragon-3parts` | 角 + 爪 + 掌 | 头 1 · 前肢 1 · 后肢 1 | 否 |
| `dragon-4parts` | 角 + 耳 + 爪 + 掌 | **头 2** · 前肢 1 · 后肢 1 | 否（头部正好在上限 2） |

底座沿用第二期的**蜥蜴**（有四肢、且没描述爪）。

## 三、成品

| # | 文件 | 叠加 | 评分 | prompt_id | sha256 |
|---|------|------|------|-----------|--------|
| 1 | [`01-dragon-3parts.png`](01-dragon-3parts.png) | 角+爪+掌 | **4.40** ✅ 成品 | `a51afce2` | `1795a7e783` |
| 2 | [`02-dragon-4parts.png`](02-dragon-4parts.png) | 角+耳+爪+掌（**主图**） | **4.70** ✅ 首选 | `2695a1ce` | `f5ae48e7f6` |

对照：[`controls/lizard.png`](controls/lizard.png) —— 纯蜥蜴底座（同轮同 seed）。

**「合龙」成立**：蜥蜴长出一对完整的**分叉鹿角**（+4 处版还有尖形带毛的**牛耳**），
整体读作龙形生物，而不是拼贴。

## 四、本期验证的两条

### 1. 区域上限在 4 件叠加下依然成立（规律 59 再验证）

`dragon-4parts` 四件齐上（头 2 + 前肢 1 + 后肢 1），**没有出现"多画一个个体"**。
对比 cat-eagle 第五期发现的反例（同一区域要承担三处 → 模型另画一个个体），
说明规律 59 的"区域 ≤2"确实是有效的**排布约束**，可以直接当设计规则用。

### 2. 逐件如实记录，不把"部分"当"完全"

| 部位 | 结果 |
|---|---|
D1 鹿角 | ✅ 完整成立 |
D9 牛耳 | ✅ 完整成立（4 处版头部可见） |
D7 鹰爪 | ⚠️ 部分（前足长弯爪，同第二期） |
D8 虎掌 | ❌ 未成立（后足仍是蜥蜴足） |

四件里两件完整、一件部分、一件未成 → A 给 4（两件完整算满，部分与未成各扣）。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject dragon-nines 7 --dry
python3 run_round.py --subject dragon-nines 4
python3 score.py --round work/dragon-nines/r7/round.json --scores work/dragon-nines/r7/scores.json \
    --control base-lizard --region head=380,100,400,320 --region feet=280,580,420,400 \
    --audit-sheet subjects/dragon-nines/rounds/dn-r7-audit.jpg \
    -o subjects/dragon-nines/rounds/dn-r7-review.md
python3 curate.py --period subjects/dragon-nines/period-04 --from work/dragon-nines/r7/round.json \
    --pick dragon-3parts=01-dragon-3parts --pick dragon-4parts=02-dragon-4parts \
    --control base-lizard=controls/lizard --note "…" --force
bash make_sheet.sh period subjects/dragon-nines/period-04
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第四期【合龙】交付：3 处 / 4 处叠加 共 2 张 | 小七 |
