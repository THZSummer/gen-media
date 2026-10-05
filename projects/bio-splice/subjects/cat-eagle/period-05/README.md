# 第五期 · 三重鹰化的猫

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/r13-review.md)
> 引擎：Z-Image-Turbo　**1280×1024**　steps 12　**全 4 张共用 seed 4201**（含同轮底座对照）
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**雪原雨雾 · 平光 · 长焦压缩 600mm · 横幅 1280×1024**

收官期要的是**气势与体量**：雪地 + 雨雾把背景压成一片灰，600mm 长焦把猫与展开的鹰翼压在一起，三重鹰化在这个呈现下读作一只**猛禽化的兽**。

> 呈现层是**期内恒定**的：本轮所有镜头（含底座对照）共用同一生境/光线/机位/画布，
> 所以「移植 vs 底座」的对照仍然干净。**期间各异**——五期各有身份，见
> [子主题首页](../README.md) 的期风格表。

## 二、本期主题与结果

**底座 ＝ 猫**　**移植件 ＝ 鹰的三处**

| 部位 | 编号 | 结果 |
|------|------|------|
| 鹰颈羽 | E6 | ✅ 颈侧长出厚实的深褐色羽领 |
| 鹰尾羽 + 颈羽 | E5+E6 | ✅ 跨区域两处 |
| 鹰翼 + 尾羽 + 颈羽 | E2+E5+E6 | ✅ 三处叠加，仍是一只个体（**主图**） |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-cat-eagle-ruff.png`](01-cat-eagle-ruff.png) | E6 颈羽 | **4.55** ✅ 首选 | `6cc0e647` | `9004e88a52` |
| 2 | [`02-cat-eagle-tail-ruff.png`](02-cat-eagle-tail-ruff.png) | E5+E6 | **4.55** ✅ 首选 | `743c101b` | `3254f5eaf1` |
| 3 | [`03-cat-eagle-wings-tail-ruff.png`](03-cat-eagle-wings-tail-ruff.png) | E2+E5+E6（**主图**） | **4.70** ✅ 首选 | `b985e1f1` | `dde7a2453e` |

对照：[`controls/cat.png`](controls/cat.png) —— **同轮**的纯猫底座（同 seed、同呈现、句式骨架相同），
本轮所有客观指标都是与它比出来的。

## 四、本期验证

1. **「同区域 ≤2」的约束在跨区域叠加时成立**：三处（翼/尾羽/颈羽）分属三个区域，没有出现第二个个体、也没有部件互相挤掉。
2. **雪原平光把主体从背景里推出来**：长焦压缩 + 平光让翼展与羽领的轮廓都读得清，是「用呈现放大机制结论」的一期。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject cat-eagle 13 --dry
python3 run_round.py --subject cat-eagle 13
python3 score.py --round work/cat-eagle/r13/round.json --scores work/cat-eagle/r13/scores.json \
    --control base-cat --region head=430,60,340,360 --region body=380,420,520,480 \
    --audit-sheet subjects/cat-eagle/rounds/r13-audit.jpg \
    --subject cat-eagle -o subjects/cat-eagle/rounds/r13-review.md
python3 curate.py --period subjects/cat-eagle/period-05 --from work/cat-eagle/r13/round.json \
    --pick c-eagle-ruff=01-cat-eagle-ruff --pick c-eagle-tail-ruff=02-cat-eagle-tail-ruff \
    --pick c-eagle-3parts=03-cat-eagle-wings-tail-ruff \
    --control base-cat=controls/cat.png --note "…" --force
bash make_sheet.sh period subjects/cat-eagle/period-05
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第二期交付：猫耳 / 猫尾 / 耳+尾 共 3 张（原呈现＝秋日草甸） | 小七 |
| 2026-10-04 | **v0.2** | **呈现重做**：换成雪原雨雾 + 长焦压缩横幅，突出收官期的体量与气势 | 小七 |
