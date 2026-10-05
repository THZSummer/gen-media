# 第四期 · 牙舌俱全

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ff-r6-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 10101 / 10102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**雨后 · 硬侧光 · 方**

两件同体，需要**硬光把结构分开**：雨后的水珠挂在夹子上，
硬侧光让獠牙、水珠、舌头三者的边缘都不互相糊在一起。

## 二、本期主题与结果

**底座 ＝ 捕蝇草（不写缘齿）**　**移植件 ＝ 兽牙 T1 + 舌 T4**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 兽牙 | T1 | 夹子边缘 | ✅ 完整成立 |
| 舌 | T4 | 夹子内腔 | ✅ 完整成立 |
| 两件同体 | T1+T4 | 边缘与内腔 | ✅ **互不抢占**：一个在边上，一个在腔里 |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-flytrap-fangs-tongue.png`](01-flytrap-fangs-tongue.png) | T1+T4（**主图**） | **5.00** ✅ 首选 | `390ef57e` | `6e2c4d49ae` |
| 2 | [`02-flytrap-fangs-tongue-b.png`](02-flytrap-fangs-tongue-b.png) | T1+T4（seed 10102） | **5.00** ✅ 首选 | `269a7ef9` | `b0c7d745a9` |

对照：[`controls/flytrap.png`](controls/flytrap.png) —— **同轮**的纯捕蝇草。

## 四、本期验证

1. **「同区域 ≤2」在这里不是约束**（规律 59 的适用边界）：
   牙在**边缘**、舌在**内腔**，属于两个不同的面，所以不抢占。
2. 有了牙与舌，整株植物读作**一张兽口**——这是本子主题的立意所在（跨越的不是物种，是界）。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject flytrap-fang 6 --dry
python3 run_round.py --subject flytrap-fang 6
python3 score.py --round work/flytrap-fang/r6/round.json --scores work/flytrap-fang/r6/scores.json \
    --control base-flytrap --region lobe=250,150,550,500 \
    --audit-sheet subjects/flytrap-fang/rounds/ff-r6-audit.jpg \
    --subject flytrap-fang -o subjects/flytrap-fang/rounds/ff-r6-review.md
python3 curate.py --period subjects/flytrap-fang/period-04 --from work/flytrap-fang/r6/round.json \
    --pick flytrap-fangs-tongue=01-flytrap-fangs-tongue \
    --pick flytrap-fangs-tongue-b=02-flytrap-fangs-tongue-b \
    --control base-flytrap=controls/flytrap --note "…" --force
bash make_sheet.sh period subjects/flytrap-fang/period-04
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第四期【牙舌俱全】交付 2 张（全部首选） | 小七 |
