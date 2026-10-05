# 第二期 · 兽耳兽尾的鹰

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/r17-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**全 4 张共用 seed 4201**（含同轮底座对照）
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**黄昏湿草地 · 暖侧逆光 · 平视全身 400mm · 方**

本期要展示的是**耳与尾**两件小件：耳在头上、尾在身后，一头一尾拉开，所以机位保持**平视全身**把两端都收进画面；身份改由**光线**承担——暮色湿地上的暖侧逆光把耳尖与尾根勾亮，与第一期的晨雾柔光完全分开。

> 呈现层是**期内恒定**的：本轮所有镜头（含底座对照）共用同一生境/光线/机位/画布，
> 所以「移植 vs 底座」的对照仍然干净。**期间各异**——五期各有身份，见
> [子主题首页](../README.md) 的期风格表。

## 二、本期主题与结果

**底座 ＝ 鹰**（强物种，让它整体成）　**移植件 ＝ 猫的小件**

| 部位 | 编号 | 结果 |
|------|------|------|
| 猫耳 | C1 | ✅ 鹰头上长出尖猫耳 |
| 猫尾 | C5 | ✅ 尾根伸出**虎斑环纹猫尾**（向上卷起） |
| 猫耳 + 猫尾 | C1+C5 | ✅ 两处同时成立（**主图**） |
| 猫掌（未纳入） | C4 | ❌ 脚仍是鹰爪，`soft furry paws` 未执行 |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-eagle-cat-ears.png`](01-eagle-cat-ears.png) | C1 猫耳 | **5.00** ✅ 首选 | `430f0453` | `32467573ac` |
| 2 | [`02-eagle-cat-tail.png`](02-eagle-cat-tail.png) | C5 猫尾 | **4.85** ✅ 首选 | `06115702` | `cb0485ce3d` |
| 3 | [`03-eagle-cat-ears-tail.png`](03-eagle-cat-ears-tail.png) | C1+C5（**主图**） | **5.00** ✅ 首选 | `538f8462` | `3f64c94f5b` |

对照：[`controls/eagle.png`](controls/eagle.png) —— **同轮**的纯鹰底座（同 seed、同呈现、句式骨架相同），
本轮所有客观指标都是与它比出来的。

## 四、本期验证

1. **移植能否成立，取决于底座有没有「占位」**：鹰的描述里没有耳、没有猫式尾，两件都成立；而脚被 `scaled yellow legs with black talons` 占住，猫掌就不成立。
2. **⚠️ 呈现层不是中性的**：同一句猫尾，在 R6 的平视 600mm 全身像里**成立**，在 R10/R14 的**低机位 85mm 竖幅**里却**多画出一只完整的猫**（供体被个体化）；把机位退回平视（本轮）又恢复成立 → 换机位/画幅必须复核部位是否仍落地（规律 80）。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject cat-eagle 17 --dry
python3 run_round.py --subject cat-eagle 17
python3 score.py --round work/cat-eagle/r17/round.json --scores work/cat-eagle/r17/scores.json \
    --control base-eagle --region ears=400,60,320,300 --region tail=560,200,400,500 \
    --audit-sheet subjects/cat-eagle/rounds/r17-audit.jpg \
    --subject cat-eagle -o subjects/cat-eagle/rounds/r17-review.md
python3 curate.py --period subjects/cat-eagle/period-02 --from work/cat-eagle/r17/round.json \
    --pick e-cat-ears=01-eagle-cat-ears --pick e-cat-tail=02-eagle-cat-tail \
    --pick e-cat-ears-tail=03-eagle-cat-ears-tail \
    --control base-eagle=controls/eagle.png --note "…" --force
bash make_sheet.sh period subjects/cat-eagle/period-02
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第二期交付：猫耳 / 猫尾 / 耳+尾 共 3 张（原呈现＝秋日草甸） | 小七 |
| 2026-10-04 | **v0.2** | **呈现重做**：机位退回平视全身、身份改由黄昏暖侧逆光承担；`e-cat-tail` 在低机位竖幅下拖出第二只猫的证据留在 R10/R14 | 小七 |
