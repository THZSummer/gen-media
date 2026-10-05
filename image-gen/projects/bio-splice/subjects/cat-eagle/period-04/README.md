# 第四期 · 有须的鹰

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/r16-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**全 3 张共用 seed 4201**（含同轮底座对照）
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**暗背景 · 单侧低角度光 · 贴面特写 200mm · 方**

胡须是**细线**部件，能不能读出来几乎完全由光决定。原计划用正午硬光，实测**胡须在硬光下完全读不出来**（R12）；改成**暗背景 + 单侧光**后，细须被照成一条条亮线——本期因此以「暗调特写」作为身份，与其余四期都不重样。

> 呈现层是**期内恒定**的：本轮所有镜头（含底座对照）共用同一生境/光线/机位/画布，
> 所以「移植 vs 底座」的对照仍然干净。**期间各异**——五期各有身份，见
> [子主题首页](../README.md) 的期风格表。

## 二、本期主题与结果

**底座 ＝ 鹰**　**移植件 ＝ 猫的面部件**

| 部位 | 编号 | 结果 |
|------|------|------|
| 猫胡须 | C6 | ✅ 喙根两侧长出细长猫须（**主图**） |
| 猫耳 + 猫胡须 | C1+C6 | ✅ 两处同框；侧逆光下耳廓落在阴影里，不如胡须明确 |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-eagle-cat-whiskers.png`](01-eagle-cat-whiskers.png) | C6 猫胡须（**主图**） | **5.00** ✅ 首选 | `23eb6fdd` | `b5254b6f83` |
| 2 | [`02-eagle-cat-ears-whiskers.png`](02-eagle-cat-ears-whiskers.png) | C1+C6 | **4.55** ✅ 首选 | `a918515a` | `4a009cd088` |

对照：[`controls/eagle.png`](controls/eagle.png) —— **同轮**的纯鹰底座（同 seed、同呈现、句式骨架相同），
本轮所有客观指标都是与它比出来的。

## 四、本期验证

1. **细部件的成败直接由光线决定**：同一句胡须，正午硬光下完全不可读（R12），暗背景单侧光下清晰成立（本轮）→ 选光要**冲着部件的材质**去。
2. 特写期的 CN 取景句必须跟着改（「头部特写」而不是「全身像」），否则 CN 层与摄影层互相打架（规律 78）。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject cat-eagle 16 --dry
python3 run_round.py --subject cat-eagle 16
python3 score.py --round work/cat-eagle/r16/round.json --scores work/cat-eagle/r16/scores.json \
    --control base-eagle --region whiskers=250,150,520,380 \
    --audit-sheet subjects/cat-eagle/rounds/r16-audit.jpg \
    --subject cat-eagle -o subjects/cat-eagle/rounds/r16-review.md
python3 curate.py --period subjects/cat-eagle/period-04 --from work/cat-eagle/r16/round.json \
    --pick e-cat-whiskers=01-eagle-cat-whiskers \
    --pick e-cat-ears-whiskers=02-eagle-cat-ears-whiskers \
    --control base-eagle=controls/eagle.png --note "…" --force
bash make_sheet.sh period subjects/cat-eagle/period-04
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第二期交付：猫耳 / 猫尾 / 耳+尾 共 3 张（原呈现＝秋日草甸） | 小七 |
| 2026-10-04 | **v0.2** | **呈现重做**：把「正午硬光」换成「暗背景 + 单侧光」（硬光下胡须不可读），并改成真正的贴面特写 | 小七 |
