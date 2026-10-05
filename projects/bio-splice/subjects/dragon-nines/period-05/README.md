# 第五期 · 九似 · 龙首特写

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/dn-r10-review.md)
> 引擎：Z-Image-Turbo　1024×1024　steps 12　**全 3 张共用 seed 4201**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点

**晨雾芦苇 · 侧逆光勾轮廓 · 贴面特写 200mm · 方 1024²**

本期是全子主题**唯一的特写**——前四期都是全身像，靠生境与光线区分；
本期把镜头推到脸上，背景化成一团灰，身份由**机位**承担。
光线用**侧逆光勾边**：第一缕低角度日光从侧后方来，
把鹿角、牛耳与颈侧鳞列勾出一条亮边，正脸落在阴影里。

## 二、本期主题：九似小成（能成的都放上）

原计划本期做 D2 头似驼 + D3 眼似兔。**两件都实测失败**（见第四节），
于是收官期改用九似里**已经验证成立**的头部件排一组龙首特写：

| 变体 | 部位 | 区域分布 | 是否越界 |
|------|------|----------|----------|
| `dragon-head` | 角 D1 + 耳 D9 | **头 2** | 否（正好在上限） |
| `dragon-head-scale` | 角 + 耳 + 鱼鳞 D6 | 头 2 · 体 1 | 否 |

底座沿用**蛇**（「项似蛇」是主轴，头部件本就该落在蛇头上）；
`dragon-head-scale` 用**腾出鳞占位**的底座（`snake-clean` 同款改法）。

## 三、成品

| # | 文件 | 部位 | 评分 | prompt_id | sha256 |
|---|------|------|------|-----------|--------|
| 1 | [`01-dragon-head.png`](01-dragon-head.png) | 角 + 耳（**主图**） | **5.00** ✅ 首选 | `b5470cfb` | `a65e257ffb` |
| 2 | [`02-dragon-head-scale.png`](02-dragon-head-scale.png) | 角 + 耳 + 鱼鳞 | **4.70** ✅ 首选 | `0cab32ea` | `d74fc18bc8` |

对照：[`controls/snake.png`](controls/snake.png) —— 纯蛇底座（同轮同 seed、同特写机位）。

**「龙首」成立**：一对完整的分叉鹿角 + 尖形带毛的牛耳长在蛇头上，
昂首吐信，读作龙首而不是"一条蛇戴了角"。
这是本子主题**最像龙的一张**，也说明**九似的可行路线是"头部件 + 躯干件"，
不是"换头"。**

## 四、本期验证的三条（含两条否定结论）

### 1. ❌ D2 头似驼：腾出占位也换不来头部件（R8）

把底座里的头形（`a blunt scaled head`）与名词（`its head raised`）都删掉，
再写 `an elongated camel's head with a blunt muzzle`——**四张全都没出现驼头**，
而且画面比原文**更"蛇"**（模型补出了眼镜蛇式的颈褶）。
即：腾出占位在这里无效，模型回退到了自己的蛇先验。

### 2. ❌ D2 反向也不行：拿掉物种名词 → 供体独占画面（R9）

假设"占位的来源还包括底座物种名词本身"，于是底座**完全不写物种名**
（`a long muscular low body with keeled scales and a flickering forked tongue`）：

| 底座 | 移植件 | 结果 |
|------|--------|------|
| 有物种名（`snake`） | 驼头 | **驼头 0%** —— 被底座先验压住 |
| 无物种名 | 驼头 | **整只骆驼** —— 供体把整个个体接管了 |

**头部件在 zimage 上是双向死局**：
底座物种名词既是"占位"（挡住移植件），也是"锚"（把画面按在底座物种上）。
删了它，供体就不只是接管一个部位，而是接管整只动物。

> 这条与规律 57（`whose body is entirely a deer's` → 拖出整只鹿）互为镜像：
> **整体名词点名的危险，在底座侧同样成立。**

### 3. ❌ D3 眼似兔：腾出眼位也没落地（R8）

计划里把 D3 记成"空位新增、易成"，是**规划时的误判**——
底座原文写明了 `dark lidless eyes`，眼位本来就占着。
按"腾出占位"改法腾出后移植，**仍没落地**（眼仍是蛇眼）。
小部件（眼）移植在本引擎上没有可用的手法。

## 五、如何复现

```bash
cd ../../..
# 期 05 定稿（成品来源）
python3 run_round.py --subject dragon-nines 10 --dry
python3 run_round.py --subject dragon-nines 10
python3 score.py --round work/dragon-nines/r10/round.json --scores work/dragon-nines/r10/scores.json \
    --control base-snake --region head=280,60,480,420 --region body=380,470,320,510 \
    --audit-sheet subjects/dragon-nines/rounds/r10-audit.jpg --subject dragon-nines \
    -o subjects/dragon-nines/rounds/dn-r10-review.md
python3 curate.py --period subjects/dragon-nines/period-05 --from work/dragon-nines/r10/round.json \
    --pick dragon-head=01-dragon-head --pick dragon-head-scale=02-dragon-head-scale \
    --control base-snake=controls/snake --note "…"
bash make_sheet.sh period subjects/dragon-nines/period-05
# 两条否定结论的证据轮
python3 run_round.py --subject dragon-nines 8    # 腾出占位 → 0
python3 run_round.py --subject dragon-nines 9    # 无物种名词 → 整只骆驼
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第五期【龙首特写】交付 2 张；记录 D2 驼头 / D3 兔眼 的两条否定结论 | 小七 |
