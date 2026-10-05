# 第二期 · 蛇尾的龟

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ts-r4-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**全 4 张共用 seed 5101（另加 5102/5103 的 take）**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**湿地泥岸 · 阴天 · 平视全身 400mm · 方**

尾要**贴着地**才看得出是蛇尾，所以本期用湿地泥岸 + 平视全身：泥面给了尾一个可以平铺的地方，阴天平光保住了鳞列细节。

> ⚠️ PLAN 原定「低机位贴地 · 竖」，**按规律 80 改成平视全身**：低机位竖幅在 cat-eagle 上把「尾巴句」变成了另一只完整动物。

> 呈现层**期内恒定**：本轮所有镜头（含底座对照）共用同一生境/光线/机位/画布，
> 所以「移植 vs 底座」的对照干净；**期间各异**，五期各有身份。

## 二、本期主题与结果

**底座 ＝ 龟**　**移植件 ＝ 蛇尾 N2**

| 部位 | 编号 | 结果 |
|------|------|------|
| 蛇尾 | N2 | ✅ **完整成立**：长而收尖的尾从壳后伸出，带一节节鳞列 |

对照 R1（溪石上、尾翘起）→ 本期的平视泥岸版**明显更自然**：尾平铺在泥面上，鳞片逐节可见。

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-turtle-snaketail.png`](01-turtle-snaketail.png) | N2 蛇尾（**主图**） | **5.00** ✅ 首选 | `ef036bd4` | `7c251a9c88` |
| 2 | [`02-turtle-snaketail-b.png`](02-turtle-snaketail-b.png) | N2 蛇尾（seed 5102） | **4.85** ✅ 首选 | `efb648cc` | `c8710666ee` |
| 3 | [`03-turtle-snaketail.png`](03-turtle-snaketail.png) | N2 蛇尾（seed 5101） | **4.55** ✅ 首选 | `fbfbb314` | `e7687746b4` |

对照：[`controls/turtle.png`](controls/turtle.png) —— **同轮**的纯龟底座（同 seed、同呈现、句式骨架相同），
本轮所有客观指标都是与它比出来的。

## 四、本期验证

1. **同一个部件在不同呈现下的可读性差很多**：R1 的溪石版尾翘在空中、显得不自然（4.35）；本期的平视泥岸版鳞列逐节可见（5.00）。
2. 平视机位**同时避开了规律 80 的坑**：低机位竖幅会让末端部件被画成独立个体，本期没有任何多余个体。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject turtle-snake 4 --dry
python3 run_round.py --subject turtle-snake 4
python3 score.py --round work/turtle-snake/r4/round.json --scores work/turtle-snake/r4/scores.json \
    --control base-turtle --region neck=300,200,300,250 --region tail=250,420,450,300 \
    --audit-sheet subjects/turtle-snake/rounds/ts-r4-audit.jpg \
    --subject turtle-snake -o subjects/turtle-snake/rounds/ts-r4-review.md
python3 curate.py --period subjects/turtle-snake/period-02 --from work/turtle-snake/r4/round.json \
    --pick turtle-snaketail-c=01-turtle-snaketail \
    --pick turtle-snaketail-b=02-turtle-snaketail-b \
    --pick turtle-snaketail=03-turtle-snaketail \
    --control base-turtle=controls/turtle --note "…" --force
bash make_sheet.sh period subjects/turtle-snake/period-02
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第二期【蛇尾的龟】交付 3 张；呈现按规律 80 由低机位竖幅改为平视全身 | 小七 |
