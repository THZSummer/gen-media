# 第五期 · 鲲鹏（收官）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/fb-r10-review.md)
> 引擎：Z-Image-Turbo　**1280×1024**　steps 12　**seed 6101 起（多 take 见出处表）**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**暮色海面 · 逆光剪影 · 广角 · 横幅 1280×1024**

收官期把时间线推到**最高点**：暮色海面之上一跃而起，双翼全展，逆光把整只动物压成剪影——正是《逍遥游》那句「化而为鸟」。

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
| 1 | [`01-kunpeng.png`](01-kunpeng.png) | B1（全展，**主图**） | **5.00** ✅ 首选 | `c7d00a36` | `40b6299913` |
| 2 | [`02-kunpeng-spread.png`](02-kunpeng-spread.png) | B1（全展，seed 6102） | **5.00** ✅ 首选 | `cf50a24b` | `d42af2cf04` |

对照：[`controls/fish.png`](controls/fish.png) —— **同轮**的纯鱼底座（同 seed、同呈现、句式骨架相同）。

## 四、本期验证

1. **剪影把「鱼身 + 鸟翼」这个矛盾读成了一种生物**：形体轮廓完全由翼与鱼身的组合决定。
2. 收官期用呈现（暮色 + 逆光 + 广角）把前三期的机制结论一次性收束成一个形象。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject fish-bird 10 --dry
python3 run_round.py --subject fish-bird 10
python3 score.py --round work/fish-bird/r10/round.json --scores work/fish-bird/r10/scores.json \
    --control base-fish --region body=300,400,650,350 \
    --audit-sheet subjects/fish-bird/rounds/fb-r10-audit.jpg \
    --subject fish-bird -o subjects/fish-bird/rounds/fb-r10-review.md
python3 curate.py --period subjects/fish-bird/period-05 --from work/fish-bird/r10/round.json \
    --pick fish-wings-spread=01-kunpeng --pick fish-wings-spread-b=02-kunpeng-spread \
    --control base-fish=controls/fish --note "…" --force
bash make_sheet.sh period subjects/fish-bird/period-05
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第五期【鲲鹏】交付 2 张（收官） | 小七 |
