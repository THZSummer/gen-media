# 第五期 · 冬虫夏草（标本照·收官）

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/cd-r7-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 9101 / 9102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**标本摄影：中性灰背景 · 环形光 · 全焦点 · 方**

**本子主题唯一换呈现媒介的一期**，也是本项目第一次：
不再是野外生态照，而是**标本照**——取景句也从「微距特写」换成「标本照」，
光线换成环形光 + 全焦点（`f/16`）。

## 二、本期主题与结果

**底座 ＝ 蛾幼虫**　**移植件 ＝ 菌丝覆体 MY1 + 子座 ST1 + 孢子 SP1**

| 部位 | 编号 | 结果 |
|------|------|------|
| 菌丝覆体 | MY1 | ✅ 成立 |
| 子座 | ST1 | ✅ 完整成立 |
| 孢子 | SP1 | ✅ 完整成立（子座顶端成簇） |
| 三件同体 | 全部 | ✅ 读作一份**标本**，而不是"一只虫 + 一根草" |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-cordyceps-specimen.png`](01-cordyceps-specimen.png) | MY1+ST1+SP1（**主图**） | **5.00** ✅ 首选 | `201ca842` | `bc2cc76668` |
| 2 | [`02-cordyceps-specimen-b.png`](02-cordyceps-specimen-b.png) | MY1+ST1+SP1（seed 9102） | **5.00** ✅ 首选 | `d28740af` | `bcb54576da` |

对照：[`controls/larva.png`](controls/larva.png) —— **同轮**的纯幼虫标本照。

## 四、本期验证

1. **换呈现媒介 = 收官期的低成本升级**（规律 98）：部件一字未改，
   但交付物的身份从「拍到的」变成「收藏的」——
   同一只虫，放在土面上是生态照，放在灰台上就是标本。
2. 中性背景把注意力全部收回到**结构关系**上：虫体—菌丝—子座—孢子，
   四层关系一眼读完，这正是"标本照"的价值。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject cordyceps 7 --dry
python3 run_round.py --subject cordyceps 7
python3 score.py --round work/cordyceps/r7/round.json --scores work/cordyceps/r7/scores.json \
    --control base-larva --region body=200,250,620,550 \
    --audit-sheet subjects/cordyceps/rounds/cd-r7-audit.jpg \
    --subject cordyceps -o subjects/cordyceps/rounds/cd-r7-review.md
python3 curate.py --period subjects/cordyceps/period-05 --from work/cordyceps/r7/round.json \
    --pick cordyceps-specimen=01-cordyceps-specimen \
    --pick cordyceps-specimen-b=02-cordyceps-specimen-b \
    --control base-larva=controls/larva --note "…" --force
bash make_sheet.sh period subjects/cordyceps/period-05
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第五期【冬虫夏草·标本照】交付 2 张（收官） | 小七 |
