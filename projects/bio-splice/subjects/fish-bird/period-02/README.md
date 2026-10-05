# 第二期 · 半出水

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/fb-r11-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 6101 起（多 take 见出处表）**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**水线穿过身体 · 侧光 · 平视 135mm · 方**

时间线的第二格：**水线还横在身体上**。这一格是最难的——露出水面的部分与泡在水里的部分同时存在，而「翼」只能长在露出水面的那一侧上（规律 86）。

> 出水阶段是**期内恒定**的（每期只停在一个瞬间），
> **期间各异**：水线位置、机位、光线、画幅都不同——五期连起来是一条时间线。

## 二、本期主题与结果

**底座 ＝ 鱼（离水）**　**移植件 ＝ 鸟翼 B1**

| 部位 | 编号 | 结果 |
|------|------|------|
| 鸟翼 | B1 | ✅ **完整成立**：鱼躯干上长出一对完整的鸟翼，翼羽结构与鱼体衔接自然 |

> ⚠️ 本期是「生境硬约束」（规律 85）的**直接产物**：
> 同一个底座、同一句话，在水下 0% 落地，在水面之上 100% 落地。
> 所以 fish-bird 的每一期都必须是**离水**的场景。

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-fish-wings-half.png`](01-fish-wings-half.png) | B1（半张、偏上，**主图**） | **5.00** ✅ 首选 | `3fd434ff` | `b1d803e18c` |
| 2 | [`02-fish-wings-half-b.png`](02-fish-wings-half-b.png) | B1（同上，seed 6102） | **5.00** ✅ 首选 | `4006ced6` | `20580afda3` |
| 3 | [`03-fish-wings-half-c.png`](03-fish-wings-half-c.png) | B1（同上，seed 6104） | **5.00** ✅ 首选 | `08fd4153` | `1929d924f7` |

对照：[`controls/fish.png`](controls/fish.png) —— **同轮**的纯鱼底座（同 seed、同呈现、句式骨架相同）。

## 四、本期验证

1. **场景兼容性是按区域判断的**（规律 86）：R7 里同一句翼写在**体侧**（水线以下）被场景吃掉；改成**半张、位置偏上**（露出水面那一侧）就落地。
2. 三个 seed 全成，说明这个写法是稳的——**写法定下来之后多出 take 很便宜**（规律 84）。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject fish-bird 11 --dry
python3 run_round.py --subject fish-bird 11
python3 score.py --round work/fish-bird/r11/round.json --scores work/fish-bird/r11/scores.json \
    --control base-fish --region body=250,300,520,380 \
    --audit-sheet subjects/fish-bird/rounds/fb-r11-audit.jpg \
    --subject fish-bird -o subjects/fish-bird/rounds/fb-r11-review.md
python3 curate.py --period subjects/fish-bird/period-02 --from work/fish-bird/r11/round.json \
    --pick fish-wings-half=01-fish-wings-half \
    --pick fish-wings-half-b=02-fish-wings-half-b \
    --pick fish-wings-half-c=03-fish-wings-half-c \
    --control base-fish=controls/fish --note "…" --force
bash make_sheet.sh period subjects/fish-bird/period-02
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第二期【半出水】交付 3 张（补轮 R11：R7 的同句写法被水线吃掉） | 小七 |
