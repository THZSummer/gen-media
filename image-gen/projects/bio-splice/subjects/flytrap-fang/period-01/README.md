# 第一期 · 有牙的捕蝇草

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ff-r3-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 10101 / 10102 / 10103**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**沼泽 · 侧逆光 · 微距 100mm · 方**

掠射侧逆光让红色内面发亮、边缘的獠牙被勾出轮廓——
本期的主角是**夹子边缘那一列牙**，所以光必须从边缘斜过来。

## 二、本期主题与结果

**底座 ＝ 捕蝇草（腾出版：不写缘齿）**　**移植件 ＝ 兽牙 T1**

| 部位 | 编号 | 结果 |
|------|------|------|
| 兽牙 | T1 | ✅ **完整成立**：光秃的夹子边缘排出一整列白色三角獠牙 |

⚠️ **底座用「腾出版」是有意的**（规律 100）：R1 的占用版（底座已写 `a fringe of
stiff marginal teeth`）只看到「缘齿变粗变白」（4.55）；把缘齿腾掉后，獠牙是**凭空出现**的（5.00）。

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-flytrap-fangs.png`](01-flytrap-fangs.png) | T1（**主图**） | **5.00** ✅ 首选 | `10d93ab2` | `6a684ffd56` |
| 2 | [`02-flytrap-fangs-b.png`](02-flytrap-fangs-b.png) | T1（seed 10102） | **5.00** ✅ 首选 | `06522e4e` | `b32fb3ea87` |
| 3 | [`03-flytrap-fangs-c.png`](03-flytrap-fangs-c.png) | T1（seed 10103） | **5.00** ✅ 首选 | `36512398` | `75787548b2` |

对照：[`controls/flytrap.png`](controls/flytrap.png) —— **同轮**的纯捕蝇草（腾出版，边缘没有牙）。

## 四、本期验证

1. **边界附属物 ≈ 属性，可以腾出**（规律 100）：缘齿是边缘的形态，不是器官，
   所以删掉不影响「这是捕蝇草」——与鹿腿、鱼鳍（结构）形成对照。
2. 落点是**夹子边缘**（一个附属属性的位置）而不是典范结构（规律 99）。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject flytrap-fang 3 --dry
python3 run_round.py --subject flytrap-fang 3
python3 score.py --round work/flytrap-fang/r3/round.json --scores work/flytrap-fang/r3/scores.json \
    --control base-flytrap --region lobe=250,150,550,500 \
    --audit-sheet subjects/flytrap-fang/rounds/ff-r3-audit.jpg \
    --subject flytrap-fang -o subjects/flytrap-fang/rounds/ff-r3-review.md
python3 curate.py --period subjects/flytrap-fang/period-01 --from work/flytrap-fang/r3/round.json \
    --pick flytrap-fangs=01-flytrap-fangs --pick flytrap-fangs-b=02-flytrap-fangs-b \
    --pick flytrap-fangs-c=03-flytrap-fangs-c \
    --control base-flytrap=controls/flytrap --note "…" --force
bash make_sheet.sh period subjects/flytrap-fang/period-01
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第一期【有牙的捕蝇草】交付 3 张（腾出版底座，全部首选） | 小七 |
