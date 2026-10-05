# 第二部分 · 鹿角

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ha-r2-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 14101 / 14102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**晨雾草场 · 侧逆光 · 平视 · 方**

侧逆光把鹿角的分叉勾在天光上——本页的主角是**角的分叉结构**，
所以光从侧后方来，让分叉的每一支都有独立的轮廓。

## 二、本期主题与结果

**底座 ＝ 一匹无角的马**　**移植件 ＝ 分叉鹿角 H1**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 鹿角 | H1 | 额顶（**空面**） | ✅ **完整成立**：一对完整的分叉鹿角，与头骨衔接自然 |

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-horse-antlers.png`](01-horse-antlers.png) | **5.00** ✅ 首选 | `f2fe91d6` | `c1e6a90a26` |
| 2 | [`02-horse-antlers-b.png`](02-horse-antlers-b.png) | **5.00** ✅ 首选 | `ab8b8a67` | `4ed1f3f244` |

对照：[`controls/horse.png`](controls/horse.png) —— **同轮**的纯马（无角）。

## 四、本期验证

**五条门槛全过**（规律 105/107）：落点是空面（马本来无角）、不需要承载结构、
不需要腾占位、不同形且高辨识度、供体**本身就是角**。
→ 这是本册"零失败"的第一页实证。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject horn-atlas 2 --dry
python3 run_round.py --subject horn-atlas 2
python3 score.py --round work/horn-atlas/r2/round.json --scores work/horn-atlas/r2/scores.json \
    --control base-horse --region head=350,80,400,400 \
    --audit-sheet subjects/horn-atlas/rounds/ha-r2-audit.jpg \
    --subject horn-atlas -o subjects/horn-atlas/rounds/ha-r2-review.md
python3 curate.py --period subjects/horn-atlas/period-02 --from work/horn-atlas/r2/round.json \
    --pick horse-antlers=01-horse-antlers --pick horse-antlers-b=02-horse-antlers-b \
    --control base-horse=controls/horse --note "…" --force
bash make_sheet.sh period subjects/horn-atlas/period-02
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第二部分【鹿角】交付 2 张 | 小七 |
