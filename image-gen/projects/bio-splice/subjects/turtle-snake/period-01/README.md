# 第一期 · 蛇颈的龟

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ts-r3-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**全 4 张共用 seed 5101（另加 5102/5103 的 take）**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**溪石浅滩 · 晨光 · 平视 600mm · 方**

立题期：先把蛇的那一半单独立住。龟从水里爬上溪石、正面朝向镜头，平视长焦让**颈的长度**成为画面里的主要信息——这正是本期要展示的东西。

> 呈现层**期内恒定**：本轮所有镜头（含底座对照）共用同一生境/光线/机位/画布，
> 所以「移植 vs 底座」的对照干净；**期间各异**，五期各有身份。

## 二、本期主题与结果

**底座 ＝ 龟**（刻意不写颈、不写尾，把两处腾出来）　**移植件 ＝ 蛇颈 N1**

| 部位 | 编号 | 结果 |
|------|------|------|
| 蛇颈 | N1 | ✅ **完整成立**：长而弯曲的颈从壳口伸出，细密鳞片一路到下颌 |

同一呈现下换了三个 seed（5101 / 5102 / 5103），三次都成立——**N1 是这一组里最稳的部件**。

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-turtle-snakeneck.png`](01-turtle-snakeneck.png) | N1 蛇颈（**主图**） | **5.00** ✅ 首选 | `fcf005fd` | `113a634362` |
| 2 | [`02-turtle-snakeneck-b.png`](02-turtle-snakeneck-b.png) | N1 蛇颈（seed 5102） | **5.00** ✅ 首选 | `094cd85a` | `92fa46833` |
| 3 | [`03-turtle-snakeneck-c.png`](03-turtle-snakeneck-c.png) | N1 蛇颈（seed 5103） | **5.00** ✅ 首选 | `c5139ad3` | `f1e071af3c` |

对照：[`controls/turtle.png`](controls/turtle.png) —— **同轮**的纯龟底座（同 seed、同呈现、句式骨架相同），
本轮所有客观指标都是与它比出来的。

## 四、本期验证

1. **腾出占位的做法在「颈」上完全有效**：底座不写颈的长短，`a long sinuous snake's neck` 就长了出来（规律 66）。
2. 三个 seed 都成立，说明这不是抽卡抽中的一次——**部件级移植在这类底座上是可重复的**。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject turtle-snake 3 --dry
python3 run_round.py --subject turtle-snake 3
python3 score.py --round work/turtle-snake/r3/round.json --scores work/turtle-snake/r3/scores.json \
    --control base-turtle --region neck=380,120,300,320 \
    --audit-sheet subjects/turtle-snake/rounds/ts-r3-audit.jpg \
    --subject turtle-snake -o subjects/turtle-snake/rounds/ts-r3-review.md
python3 curate.py --period subjects/turtle-snake/period-01 --from work/turtle-snake/r3/round.json \
    --pick turtle-snakeneck=01-turtle-snakeneck \
    --pick turtle-snakeneck-b=02-turtle-snakeneck-b \
    --pick turtle-snakeneck-c=03-turtle-snakeneck-c \
    --control base-turtle=controls/turtle --note "…" --force
bash make_sheet.sh period subjects/turtle-snake/period-01
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第一期【蛇颈的龟】交付 3 张（三个 seed 全成立） | 小七 |
