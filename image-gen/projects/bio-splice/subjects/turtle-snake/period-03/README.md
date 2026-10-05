# 第三期 · 缠体的龟

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ts-r2-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**全 4 张共用 seed 5101（另加 5102/5103 的 take）**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**古井石台 · 侧光 · 侧俯视 100mm · 方**

缠体是**绕在壳上**的结构，只有**侧俯视**才看得清壳面与缠绕的关系；侧光把盘绕的起伏打出阴影。玄武的经典构图就是这一张。

> 呈现层**期内恒定**：本轮所有镜头（含底座对照）共用同一生境/光线/机位/画布，
> 所以「移植 vs 底座」的对照干净；**期间各异**，五期各有身份。

## 二、本期主题与结果

**底座 ＝ 龟**　**移植件 ＝ 缠体 N3**

| 写法 | 结果 |
|------|------|
| ❌ `the thick coiled body of a large snake wrapped around its shell` | **0% 落地**（R1）|
| ✅ `a thick snake's body coiled on the stones beneath it…` | ✅ 沿着壳左侧盘在石面上 |
| ✅ `thick snake coils around its shell` | ✅ 盘绕关系成立（**最短最稳**）|
| ✅ `thick snake coils around the rim of its shell` | ✅ 弧线搭在壳沿上 |

同一轮三种写法全部落地，所以 R1 的失败**不是占位问题，而是写法问题**。

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-turtle-coil-ground.png`](01-turtle-coil-ground.png) | N3（盘在身下石面，**主图**） | **4.70** ✅ 首选 | `a8d7b0f9` | `b1248558db` |
| 2 | [`02-turtle-coil-min.png`](02-turtle-coil-min.png) | N3（最短写法） | **4.70** ✅ 首选 | `93223dcd` | `766047844d` |
| 3 | [`03-turtle-coil-rim.png`](03-turtle-coil-rim.png) | N3（绕壳沿） | **4.55** ✅ 首选 | `1e1960d7` | `bc71b31a12` |

对照：[`controls/turtle.png`](controls/turtle.png) —— **同轮**的纯龟底座（同 seed、同呈现、句式骨架相同），
本轮所有客观指标都是与它比出来的。

## 四、本期验证

1. **空间关系从句会失效**：`X wrapped around Y` 是空操作；改成名词短语 `coils around Y` 才落地 → **规律 81**。
2. 这把规律 69（复合部件要拆开写）从「部件内部」推广到了「部件与底座的关系」：**凡是需要模型理解空间关系的地方，都改用最直白的名词短语**。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject turtle-snake 2 --dry
python3 run_round.py --subject turtle-snake 2
python3 score.py --round work/turtle-snake/r2/round.json --scores work/turtle-snake/r2/scores.json \
    --control base-turtle --region shell=300,150,440,320 \
    --audit-sheet subjects/turtle-snake/rounds/ts-r2-audit.jpg \
    --subject turtle-snake -o subjects/turtle-snake/rounds/ts-r2-review.md
python3 curate.py --period subjects/turtle-snake/period-03 --from work/turtle-snake/r2/round.json \
    --pick coil-ground=01-turtle-coil-ground \
    --pick coil-min=02-turtle-coil-min \
    --pick coil-rim=03-turtle-coil-rim \
    --control base-turtle=controls/turtle --note "…" --force
bash make_sheet.sh period subjects/turtle-snake/period-03
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第三期【缠体的龟】交付 3 张；定位缠体失败的真正原因是写法（规律 81） | 小七 |
