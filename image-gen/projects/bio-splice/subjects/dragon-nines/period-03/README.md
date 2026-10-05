# 第三期 · 鱼鳞的蛇

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/dn-r6-review.md)
> 引擎：Z-Image-Turbo　1024×1024　steps 12　**全 3 张共用 seed 4201**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点

**林下枯叶 · 斑驳林光 · 侧俯贴体、鳞列占满画面 · 方 1024²**

这一期的机位是**冲着"鳞"去的**：让蛇把身体平铺、整个背脊朝向镜头，
再用侧俯与较深的景深让**鳞列成为画面的主纹理**。
R3 里"同材质替换（鳞换鳞）天然难判读"的问题，在侧俯贴体下**一眼可辨**：
基准是细碎粒状鳞，移植后是成排叠压的大片鳞（评分 4.10→4.55，带鹿角那张 4.55→5.00）。

## 二、本期主题

九似的 **鳞似鱼（D6）**——这是九似里**唯一"已占位"的部位**：
蛇自己有鳞，而第一期的底座描述里明确写了 `keeled scales along a long muscular body`。
按规律 56，移植件会被底座描述覆盖。

**对策：把底座里描述该部位的那几个词删掉，把位置腾出来。**

```
R1 底座：... a blunt scaled head, ..., keeled scales along a long muscular body
R3 底座：... a blunt head,        ..., and a long smooth muscular body   ← 腾出鳞的占位
```

与第二期在蜥蜴底座上刻意不写 `clawed` 是**同一个手法**。
底座与 R1 的差别只有这一处，所以归因清楚。

| 部位 | 编号 | 结果 |
|------|------|------|
| 鱼鳞 | D6 | ⚠️ **部分成立**：体鳞由基准的细碎鳞变为**更大、更规则、相互叠压**的鳞列 |
| 鹿角 + 鱼鳞 | D1+D6 | ⚠️ 同上；鹿角完整成立，两处不互相干扰 |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-snake-fishscale.png`](01-snake-fishscale.png) | D6 | **4.55** ✅ 首选 | `1e2c96ad` | `1eb1737cff` |
| 2 | [`02-snake-antler-fishscale.png`](02-snake-antler-fishscale.png) | D1+D6（**主图**） | **5.00** ✅ 首选 | `e3738ba6` | `8e5c5b4eb3` |

对照：[`controls/snake-clean.png`](controls/snake-clean.png) —— **已腾出鳞的占位**的纯蛇底座（同轮同 seed）。

> ⚠️ 同第二期：**本期的成品是"部分成立"**，文档如实标注。

## 四、为什么只到"部分"，以及一个判读上的难处

1. `large overlapping fish scales` 同样是个**复合部件**：鳞的大小 + 排列方式（层叠如瓦）
   + 鱼鳞特有的扇形边缘 / 虹彩。模型执行了前两层，没有第三层。
2. **更难判读**：对照基准本身也有鳞，所以这个移植是**同材质替换**而不是**空位新增**。
   与第一期的"角"（蛇根本没有角）相比，差异天然更细微，
   这也让 E（概念可读）只能给 3——不懂项目的人不容易看出这是"鱼鳞"。

> **结论**：空位新增 > 腾出占位后的新增 > 已占位新增。
> 选题时若两个部位难度相近，优先挑**底座根本没有的部件**。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject dragon-nines 6 --dry
python3 run_round.py --subject dragon-nines 3
python3 score.py --round work/dragon-nines/r6/round.json --scores work/dragon-nines/r6/scores.json \
    --control base-snake-clean --region head=430,120,380,260 --region body=430,500,400,380 \
    --audit-sheet subjects/dragon-nines/rounds/dn-r6-audit.jpg \
    -o subjects/dragon-nines/rounds/dn-r6-review.md
python3 curate.py --period subjects/dragon-nines/period-03 --from work/dragon-nines/r6/round.json \
    --pick snake-fishscale=01-snake-fishscale \
    --pick snake-fishscale-antler=02-snake-antler-fishscale \
    --control base-snake-clean=controls/snake-clean --note "…" --force
bash make_sheet.sh period subjects/dragon-nines/period-03
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|------|----------|
| 2026-10-04 | v0.1 | 第三期交付：鱼鳞 / 鹿角+鱼鳞 共 2 张（部分成立，如实标注） | 小七 |
