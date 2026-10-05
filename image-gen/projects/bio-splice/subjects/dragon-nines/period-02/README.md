# 第二期 · 有爪的蜥

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/dn-r5-review.md)
> 引擎：Z-Image-Turbo　1024×1024　steps 12　**全 3 张共用 seed 4201**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点

**卵石河滩 · 雨后侧逆光 · 低机位贴地、聚焦前足 · 竖幅 1024×1280**

这一期的机位是**冲着"爪"去的**：让动物抬起前身、把前足张开，再用低机位与浅景深把前足做成视觉主体。
在 R2 里"爪只到部分成立、且不易看清"，换成这个呈现后**长而弯的猛禽式爪一眼可辨**（评分 3.90→4.55）。
与期 01 的晨雾芦苇完全不同的身份：湿石、水光、逆光轮廓。

## 二、本期主题

九似的 **爪似鹰（D7）** 与 **掌似虎（D8）**。

底座从蛇换成**蜥蜴**——因为第一期实测：蛇**没有四肢**，鹰爪"无处可长"。
蜥蜴同样有蛇形躯干，但有四肢。

**关键写法**：底座**刻意不描述爪**（写 `four stout legs` 而不写 `clawed`），
把脚的位置留给移植件——否则会像 cat-eagle 的「猫掌」那样被底座自己的描述覆盖。

| 部位 | 编号 | 结果 |
|------|------|------|
| 鹰爪（前足） | D7 | ⚠️ **部分成立**：爪形由短钝变为长而弯的猛禽式，但足部仍是深色鳞质 |
| 虎掌（后足） | D8 | ❌ 未成立：后足仍是蜥蜴足，未见虎的宽厚肉垫 |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-lizard-talons.png`](01-lizard-talons.png) | D7（**主图**） | **4.55** ✅ 首选 | `b067dd4b` | `208886912f` |
| 2 | [`02-lizard-talons-paws.png`](02-lizard-talons-paws.png) | D7+D8 | **4.40** ✅ 成品 | `f404a726` | `000f02adb6` |

对照：[`controls/lizard.png`](controls/lizard.png) —— 未移植的纯蜥蜴底座（同轮同 seed）。

> ⚠️ **本期的成品是"部分成立"**：爪形对，材质没对。文档如实标注，不当作完全成功。

## 四、判定依据（放大 ×3）

| | 基准·蜥蜴 | 移植后 |
|---|---|---|
| 前足爪形 | **短钝**的蜥蜴爪，平贴地面 | **长而弯**、抬起作抓握状的猛禽式爪 |

**为什么只到"部分"**：`eagle talons` 是一个**复合部件**——爪的曲度 + 黄色的鳞状跗跖 + 爪的黑色。
模型只执行了最显眼的一层（爪的曲度）。要完全成立，需把复合部件拆开分条写，
或换有真负向的引擎（Qwen）压掉蜥蜴足的特征。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject dragon-nines 5 --dry
python3 run_round.py --subject dragon-nines 2
python3 score.py --round work/dragon-nines/r5/round.json --scores work/dragon-nines/r5/scores.json --control base-lizard \
    --region feet=380,560,520,420 --region head=430,120,380,260 \
    --audit-sheet subjects/dragon-nines/rounds/dn-r5-audit.jpg \
    -o subjects/dragon-nines/rounds/dn-r5-review.md
python3 curate.py --period subjects/dragon-nines/period-02 --from work/dragon-nines/r5/round.json \
    --pick lizard-talons=01-lizard-talons \
    --pick lizard-talons-paws=02-lizard-talons-paws \
    --control base-lizard=controls/lizard --note "…" --force
bash make_sheet.sh period subjects/dragon-nines/period-02
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第二期交付：鹰爪 / 鹰爪+虎掌 共 2 张（爪部分成立，如实标注） | 小七 |
