# 第三期 · 吐信的捕蝇草

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ff-r5-review.md)
> 引擎：Z-Image-Turbo　**1024×1280**　steps 12　**seed 10101 / 10102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**苔藓 · 低机位 · 竖 1024×1280**

要看清「夹子内腔里的舌」，机位必须**低、且正对内腔**；竖幅给舌的卷曲留出空间。
苔藓与湿地色把画面压暗，粉色的舌因此更跳。

## 二、本期主题与结果

**底座 ＝ 捕蝇草（宽叶面版）**　**移植件 ＝ 舌 T4**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 舌 | T4 | 夹子内腔（**空面**） | ✅ **完整成立**：一条粉色哺乳动物舌头从夹子里卷出来 |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-flytrap-tongue.png`](01-flytrap-tongue.png) | T4（**主图**） | **5.00** ✅ 首选 | `b4b44ade` | `4e93d157ca` |
| 2 | [`02-flytrap-tongue-b.png`](02-flytrap-tongue-b.png) | T4（seed 10102） | **5.00** ✅ 首选 | `2b35ec69` | `bb822c0c3c` |

对照：[`controls/flytrap.png`](controls/flytrap.png) —— **同轮**的纯捕蝇草（张着夹子、内腔是空的）。

## 四、本期验证

1. **夹子内腔是一个空面**，舌的落点毫无阻力（规律 97/99）；
   而且一旦有了舌，**夹子立刻被读成「嘴」**——这是本期最有趣的效果。
2. 舌的材质（粉色、湿润、卷曲）与植物的绿色形成强对比，是「跨界」读得最直白的一张。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject flytrap-fang 5 --dry
python3 run_round.py --subject flytrap-fang 5
python3 score.py --round work/flytrap-fang/r5/round.json --scores work/flytrap-fang/r5/scores.json \
    --control base-flytrap --region lobe=250,200,520,700 \
    --audit-sheet subjects/flytrap-fang/rounds/ff-r5-audit.jpg \
    --subject flytrap-fang -o subjects/flytrap-fang/rounds/ff-r5-review.md
python3 curate.py --period subjects/flytrap-fang/period-03 --from work/flytrap-fang/r5/round.json \
    --pick flytrap-tongue=01-flytrap-tongue --pick flytrap-tongue-b=02-flytrap-tongue-b \
    --control base-flytrap=controls/flytrap --note "…" --force
bash make_sheet.sh period subjects/flytrap-fang/period-03
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第三期【吐信的捕蝇草】交付 2 张（全部首选） | 小七 |
