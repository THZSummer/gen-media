# 第一期 · 菌丝覆体的虫

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/cd-r3-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 9101 / 9102 / 9103**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**土面 · 柔光 · 微距平视 100mm · 方**

立题期先拍"最基础的那一半"：虫体被菌丝覆住。
林地土面 + 柔散光让白色菌丝与深色土壤形成最直接的对比。

## 二、本期主题与结果

**底座 ＝ 蛾幼虫（腾出版：只写头与足，不写体表质感）**　**移植件 ＝ 菌丝覆体 MY1**

⚠️ **底座用"腾出版"是有意的**（规律 96）：R1 的占用版（`segmented pale body`）
里虫本身就发白发绒，菌丝覆体的边际贡献看不出来；
把体表描述腾掉之后，白色菌丝覆盖**一眼可辨**。三个 seed 全部成立。

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-larva-mycelium.png`](01-larva-mycelium.png) | MY1（**主图**） | **4.55** ✅ 首选 | `0a0d84ac` | `bc3c839810` |
| 2 | [`02-larva-mycelium-b.png`](02-larva-mycelium-b.png) | MY1（seed 9102） | **4.55** ✅ 首选 | `fa533870` | `9a2cb8f21b` |
| 3 | [`03-larva-mycelium-c.png`](03-larva-mycelium-c.png) | MY1（seed 9103） | **4.55** ✅ 首选 | `3e391d97` | `8cbe75747b` |

对照：[`controls/larva.png`](controls/larva.png) —— **同轮**的纯幼虫底座（腾出版，光滑褐色）。

## 四、本期验证

1. **可腾出的是「属性」，腾不出的是「结构」**（规律 96）：
   体表质感删得掉，所以腾出版有效；对比前几轮——鹿腿、鱼鳍、猫掌删了也会被补回来。
2. 材质仍是「绒层」而非真正的菌丝毡，所以 A=4 而不是 5 ——**如实标注部分成立**。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject cordyceps 3 --dry
python3 run_round.py --subject cordyceps 3
python3 score.py --round work/cordyceps/r3/round.json --scores work/cordyceps/r3/scores.json \
    --control base-larva --region body=200,250,620,550 \
    --audit-sheet subjects/cordyceps/rounds/cd-r3-audit.jpg \
    --subject cordyceps -o subjects/cordyceps/rounds/cd-r3-review.md
python3 curate.py --period subjects/cordyceps/period-01 --from work/cordyceps/r3/round.json \
    --pick larva-mycelium=01-larva-mycelium --pick larva-mycelium-b=02-larva-mycelium-b \
    --pick larva-mycelium-c=03-larva-mycelium-c \
    --control base-larva=controls/larva --note "…" --force
bash make_sheet.sh period subjects/cordyceps/period-01
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第一期【菌丝覆体的虫】交付 3 张（腾出版底座） | 小七 |
