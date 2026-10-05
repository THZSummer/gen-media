# 生物拼接（Bio Splice）

> 返回[项目索引](../README.md) ｜ 技术技能见 [../../skills/](../../skills/README.md)

> 🏁 **本项目已全部交付（12 个子主题 / 60 期 / 135 成品）**，全线总结见 [`SUMMARY.md`](SUMMARY.md)。

**一个拼接项目**：把 A 的器官接到 B 的身上，用纪实摄影（或显微/标本）的写实语言拍出来，
像真实存在的物种。

**不限于动物**——植物、真菌、藻类、地衣都可以做底座或供体；
子主题按**生物组合**划分，每组 5 期，每期 2–3 件成品。

完整规划见 [`PLAN.md`](PLAN.md)（12 个子主题 × 5 期）。

---

## 一、目录结构

```
bio-splice/
├── README.md                    ← 本文件（项目总览）
├── run_round.py                 ← 轮次驱动入口（--subject 选子主题）
├── roundkit.py                  ← 驱动的通用机械（跑轮 / 存档 / 分句换行）
├── curate.py                    ← 成品提升：work/ → period/，并留下出处
├── score.py                     ← 打分复核：客观报警 + 主观维度，按门槛判定能否进成品
├── make_sheet.sh                ← 速览图（round = 开发用 / period = 期成品 / subject = 跨期总览 / all = 全部一次出）
├── PLAN.md                      ← **全部子主题与 5 期规划**
├── subjects/                    ← 子主题，按生物组合划分
│   ├── cat-eagle/               ← 子主题：猫 + 鹰（period-01 … period-05）
│   │   ├── sheet.jpg            ← **跨期总览图**（每期一行，全子主题成品拼一张）
│   │   ├── sheet-thumb.jpg      ← 上面那张的缩略图（供文档内嵌，点击看原图）
│   │   └── ...
│   └── dragon-nines/            ← 子主题：龙 · 九似（period-01 … period-04）
│       ├── README.md            ← 子主题概念与结论
│       ├── sheet.jpg            ← **跨期总览图**
│       ├── sheet-thumb.jpg      ← 缩略图（同上）
│       ├── parts.md             ← 该子主题的**部位表**
│       ├── rounds/              ← 该子主题的开发记录（轮次、诊断、prompt 存档）
│       └── period-01/           ← 期：**只放成品**
│           ├── README.md
│           ├── manifest.json    ← 每件成品的出处（轮次/镜头/seed/prompt_id/sha256）
│           ├── sheet.jpg        ← 本期速览图
│           ├── 01-*.png …       ← 成品
│           └── controls/        ← 对照（不是本期成品，是系列的参照系）
└── work/<子主题>/rN/            ← 探索产物（半成品/失败轮次）**不进仓库**
                                   轮号是子主题内的编号，两个子主题的 r1 不冲突
```

## 二、纪律：成品与半成品分开放

| 位置 | 内容 | 进仓库？ |
|------|------|----------|
| `work/<子主题>/rN/` | 每一轮的**全部**原始产物，含失败轮次（轮号是**子主题内**编号） | ❌ **不进** |
| `subjects/<子>/period-NN/` | **只放成品** | ✅ 进 |

- **一眼假的产物不进成品**。判定标准：不懂这个项目的人扫一眼会不会觉得"这是假的/坏了"。
  典型不合格：双头、错位、拼贴痕迹突兀、物种退化（要做鹰头猫却出了纯鹰）。
- **半成品不必进仓库，是因为它可以被复现**：`run_round.py` 全部固定 seed，
  且已验证同一 prompt/seed/画布下**解码像素逐字节相同**。
  所以 `work/` 清掉也不丢证据——重跑即得。
- **成品只能经 `curate.py` 进入交付目录**，它会写下 `manifest.json`
  （来源轮次、镜头名、seed、prompt_id、prompt 原文、sha256）。手工 `cp` 会丢出处。
- **每轮生成后必须打分**（`score.py`）：A 移植到位 .30 ｜ B 底座完整 .20 ｜ C 解剖可信 .20 ｜
  D 摄影统一 .15 ｜ E 概念可读 .15；`fatal` 非空 / A<3 / B<3 → 不合格。
  **只有 ✅（总分 ≥3.5）才进期目录**，⚠️ 备选与 ❌ 一律不进。
  客观指标（与同轮底座对照的区域差）只用于**报警**——区域没变说明移植句是空操作；
  区域变了**不能**证明是部位造成的（姿态漂移也会变），必须目视确认。

```bash
# 从某一轮里挑成品，提升到某期
python3 curate.py --period subjects/cat-eagle/period-01 \
    --from work/cat-eagle/r1/round.json \
    --pick owl-seamless=01-owl-seamless \
    --control cat=controls/cat
```

## 三、子主题（12 个 × 5 期，详见 [PLAN.md](PLAN.md)）

| # | 组 | 子主题 | 概念钩子 | 状态 |
|---|----|--------|----------|------|
| 1 | 甲 | [cat-eagle](subjects/cat-eagle/README.md) · 猫 + 鹰 | 「猫头鹰」这个词本身就是拼接（猫+头+鹰） | **5 期已交付**（各有专属呈现） |
| 2 | 甲 | [dragon-nines](subjects/dragon-nines/README.md) · 龙 · 九似 | 画龙口诀「三停九似」本身就是一张九项部位表 | **5 期已交付** |
| 3 | 甲 | [turtle-snake](subjects/turtle-snake/README.md) · 龟 + 蛇 | 四象之「玄武」就是龟蛇合体 | **5 期已交付** |
| 4 | 甲 | [fish-bird](subjects/fish-bird/README.md) · 鱼 + 鸟 | 《庄子》北冥有鱼…化而为鸟（鲲鹏） | **5 期已交付**（排期重做） |
| 5 | 甲 | [deer-crane](subjects/deer-crane/README.md) · 鹿 + 鹤 | 传统吉祥纹样「鹿鹤同春」 | **5 期已交付**（部分成立为主） |
| 6 | 乙 | [lichen](subjects/lichen/README.md) · 地衣 | **地衣本身就是拼接生物**（真菌 + 藻共生体） | **5 期已交付**（11 成品全首选） |
| 7 | 乙 | [cordyceps](subjects/cordyceps/README.md) · 冬虫夏草 | 《本草》里的虫与菌拼接体 | **5 期已交付**（11 成品全首选） |
| 8 | 乙 | [flytrap-fang](subjects/flytrap-fang/README.md) · 捕蝇草 + 动物器官 | 植物长出动物的器官（牙/眼/舌） | **5 期已交付**（11 成品全首选） |
| 9 | 乙 | [flower-bird](subjects/flower-bird/README.md) · 花 + 鸟 | 「花鸟」是中国画的基本单元 | **5 期已交付**（12 成品全首选） |
| 10 | 乙 | [tree-beast](subjects/tree-beast/README.md) · 树 + 兽 | 树皮↔兽皮、根系↔足、年轮↔骨 | **5 期已交付** |
| 11 | 丙 | [wing-atlas](subjects/wing-atlas/README.md) · 翅 · 图鉴 | 固定一只鸟，原翼之外**再加一对**（空位新增） | **5 期已交付**（11 成品全首选） |
| 12 | 丙 | [horn-atlas](subjects/horn-atlas/README.md) · 角 · 图鉴 | 固定一匹**无角**的马，轮流长五种「角」 | **5 期已交付**（**零失败**，均分 5.00） |

> **每期一张合并图**（`make_sheet.sh period`）、**每子主题一张合并图**（`make_sheet.sh subject`）；
> 一次全出用 `bash make_sheet.sh all`。

## 四、执行计划

| 阶段 | 引擎 | 用途 |
|------|------|------|
| 定向 | Z-Image-Turbo（~10 s/张，**无负向提示词**） | 试句式、定构图、控成本 |
| 定稿 | Qwen-Image 2512（6–13 min/张，**有真负向**） | 材质与解剖细节，压掉不许出现的东西 |
| 结构锁 | [image-edit-comfyui](../../skills/image-edit-comfyui/SKILL.md)（ControlNet） | 提示词压不住时，用控制图锁住身体结构 |

> ⚠️ **没有负向提示词的引擎上，"要减掉什么"的需求无解**（正向 `no X` 与 `exactly one X`
> 都实测无效）。这类需求必须换 Qwen，或改用 ControlNet 结构锁。详见
> [子主题第一轮诊断](subjects/cat-eagle/rounds/r02.md)。

## 五、产出记录（跨子主题）

| 子主题 | 期 | 成品数 | 内容 | 记录 |
|--------|----|--------|------|------|
| cat-eagle | period-01 | 3（+2 对照） | 猫头鹰：三种拼接语义各一张 | [period-01](subjects/cat-eagle/period-01/README.md) |
| cat-eagle | period-02 | 3 | 兽耳兽尾的鹰：鹰底座 + 猫耳 / 猫尾（黄昏湿地 · 暖侧逆光 · 平视 400mm） | [period-02](subjects/cat-eagle/period-02/README.md) |
| cat-eagle | period-03 | 3 | 有翅的猫：猫底座 + 鹰翼 / 鹰尾羽（雨后林地 · 逆光 · 广角低机位翼展） | [period-03](subjects/cat-eagle/period-03/README.md) |
| cat-eagle | period-04 | 2 | 有须的鹰：鹰底座 + 猫胡须 / 耳+胡须（暗背景 · 单侧光 · 贴面特写） | [period-04](subjects/cat-eagle/period-04/README.md) |
| cat-eagle | period-05 | 3 | 三重鹰化的猫：猫底座 + 鹰颈羽 / 尾羽 / 翼（雪原雨雾 · 长焦压缩） | [period-05](subjects/cat-eagle/period-05/README.md) |
| dragon-nines | period-01 | 2 | 有角的蛇：蛇底座 + 鹿角 / 鹿角+牛耳 | [period-01](subjects/dragon-nines/period-01/README.md) |
| dragon-nines | period-02 | 2 | 有爪的蜥：蜥蜴底座 + 鹰爪（部分成立）/ 鹰爪+虎掌 | [period-02](subjects/dragon-nines/period-02/README.md) |
| dragon-nines | period-03 | 2 | 鱼鳞的蛇：先腾出底座的鳞占位，再移植鱼鳞 | [period-03](subjects/dragon-nines/period-03/README.md) |
| dragon-nines | period-04 | 2 | 合龙：蜥蜴底座 + 角/耳/爪/掌 3~4 件叠加 | [period-04](subjects/dragon-nines/period-04/README.md) |
| dragon-nines | period-05 | 2 | 龙首特写（收官）：蛇底座 + 鹿角/牛耳（+鱼鳞），全子主题唯一特写 | [period-05](subjects/dragon-nines/period-05/README.md) |
| turtle-snake | period-01 | 3 | 蛇颈的龟：龟底座 + 蛇颈 N1（三个 seed 全成立） | [period-01](subjects/turtle-snake/period-01/README.md) |
| turtle-snake | period-02 | 3 | 蛇尾的龟：龟底座 + 蛇尾 N2（湿地泥岸 · 平视） | [period-02](subjects/turtle-snake/period-02/README.md) |
| turtle-snake | period-03 | 3 | 缠体的龟：龟底座 + 蛇身盘绕（三种写法，规律 81） | [period-03](subjects/turtle-snake/period-03/README.md) |
| turtle-snake | period-04 | 2 | 颈尾俱全：N1+N2 跨区域叠加 | [period-04](subjects/turtle-snake/period-04/README.md) |
| turtle-snake | period-05 | 2 | **玄武**（收官）：颈+尾+缠体三件同体，暮色水面剪影 | [period-05](subjects/turtle-snake/period-05/README.md) |
| fish-bird | period-01 | 2 | **跃出水面**：鱼 + 鸟翼，刚离水、水花未落 | [period-01](subjects/fish-bird/period-01/README.md) |
| fish-bird | period-02 | 3 | **半出水**：水线穿过身体，半张的翼在露出水面那一侧 | [period-02](subjects/fish-bird/period-02/README.md) |
| fish-bird | period-03 | 2 | **完全离水·双翼全展**：侧上方视角、逆光勾羽 | [period-03](subjects/fish-bird/period-03/README.md) |
| fish-bird | period-04 | 2 | **低空掠水**：长焦压缩、平光灰水 | [period-04](subjects/fish-bird/period-04/README.md) |
| fish-bird | period-05 | 2 | **鲲鹏**（收官）：暮色海面、逆光剪影、全展鸟翼 | [period-05](subjects/fish-bird/period-05/README.md) |
| deer-crane | period-01 | 2 | 长颈的鹿：鹿底座 + 鹤颈（部分成立） | [period-01](subjects/deer-crane/period-01/README.md) |
| deer-crane | period-02 | 2 | 鹤腿的鹿：鹿底座 + 鹤腿（部分成立，含占用版对照） | [period-02](subjects/deer-crane/period-02/README.md) |
| deer-crane | period-03 | 1 | 鹤尾的鹿：**唯一完整成立的一件**，命中率 1/4 | [period-03](subjects/deer-crane/period-03/README.md) |
| deer-crane | period-04 | 2 | 颈腿俱全：G1+G2 跨区域叠加 | [period-04](subjects/deer-crane/period-04/README.md) |
| deer-crane | period-05 | 2 | 鹿鹤同春（收官）：颈+腿+尾三件同体 | [period-05](subjects/deer-crane/period-05/README.md) |
| lichen | period-01 | 3 | 壳状地衣：菌丝体 + 壳状形态 + 绿色藻细胞（跨域件首次 100% 落地） | [period-01](subjects/lichen/period-01/README.md) |
| lichen | period-02 | 2 | 叶状地衣：树皮上的叶状裂片 + 藻丝 | [period-02](subjects/lichen/period-02/README.md) |
| lichen | period-03 | 2 | 枝状地衣：冻原逆光下的分叉枝状体 | [period-03](subjects/lichen/period-03/README.md) |
| lichen | period-04 | 2 | 藻层可见：拟剖面里的绿球与藻丝（呈现救弱期） | [period-04](subjects/lichen/period-04/README.md) |
| lichen | period-05 | 2 | 共生体（收官）：叶状 + 枝状 + 藻细胞的复合地衣 | [period-05](subjects/lichen/period-05/README.md) |
| cordyceps | period-01 | 3 | 菌丝覆体的虫：蛾幼虫 + 菌丝覆体（腾出体表） | [period-01](subjects/cordyceps/period-01/README.md) |
| cordyceps | period-02 | 2 | 单根子座：棒状子座从虫体拔起 | [period-02](subjects/cordyceps/period-02/README.md) |
| cordyceps | period-03 | 2 | 多根子座：四根子座同时长出 | [period-03](subjects/cordyceps/period-03/README.md) |
| cordyceps | period-04 | 2 | 子座与孢子：子座表面覆粉状孢子 | [period-04](subjects/cordyceps/period-04/README.md) |
| cordyceps | period-05 | 2 | **冬虫夏草**（标本照收官）：菌丝+子座+孢子，中性背景环形光 | [period-05](subjects/cordyceps/period-05/README.md) |
| flytrap-fang | period-01 | 3 | 有牙的捕蝇草：夹子边缘排出白色兽牙（腾出缘齿） | [period-01](subjects/flytrap-fang/period-01/README.md) |
| flytrap-fang | period-02 | 2 | 有眼的捕蝇草：叶面上长出一只动物眼 | [period-02](subjects/flytrap-fang/period-02/README.md) |
| flytrap-fang | period-03 | 2 | 吐信的捕蝇草：夹子内腔卷出一条粉色兽舌 | [period-03](subjects/flytrap-fang/period-03/README.md) |
| flytrap-fang | period-04 | 2 | 牙舌俱全：獠牙 + 兽舌同体（雨后硬侧光） | [period-04](subjects/flytrap-fang/period-04/README.md) |
| flytrap-fang | period-05 | 2 | 食肉植物（收官）：牙+眼+舌三件，晨雾沼泽逆光 | [period-05](subjects/flytrap-fang/period-05/README.md) |
| flower-bird | period-01 | 3 | 翎枝的花：一束羽翎从花心升起（玉兰晨露） | [period-01](subjects/flower-bird/period-01/README.md) |
| flower-bird | period-02 | 2 | 绒心的花：花蕊被读成绒羽（部分成立） | [period-02](subjects/flower-bird/period-02/README.md) |
| flower-bird | period-03 | 2 | 翎绒俱全：翎羽 + 绒心同体（暗背景硬光） | [period-03](subjects/flower-bird/period-03/README.md) |
| flower-bird | period-04 | 3 | 百合的绒与翎：换花种，命中率降到 1/2 后补 take | [period-04](subjects/flower-bird/period-04/README.md) |
| flower-bird | period-05 | 2 | 花鸟（收官）：满枝花朵各生一支羽翎 | [period-05](subjects/flower-bird/period-05/README.md) |
| tree-beast | period-01 | 3 | 兽皮的树：树干覆上兽皮/毛皮（腾出树皮） | [period-01](subjects/tree-beast/period-01/README.md) |
| tree-beast | period-02 | 2 | 有角的树：树干上挑着一对巨大弯角 | [period-02](subjects/tree-beast/period-02/README.md) |
| tree-beast | period-03 | 2 | 皮角俱全：兽皮 + 兽角（雨后硬光） | [period-03](subjects/tree-beast/period-03/README.md) |
| tree-beast | period-04 | 2 | 枯木的皮与角：换底座（枯立木）后仍成 | [period-04](subjects/tree-beast/period-04/README.md) |
| tree-beast | period-05 | 2 | 树兽（收官）：暮色逆光剪影，**兽足未落地** | [period-05](subjects/tree-beast/period-05/README.md) |
| wing-atlas | period-01 | 3 | **基准**：统一底座鸟（无移植件，作后四部分的参照） | [period-01](subjects/wing-atlas/period-01/README.md) |
| wing-atlas | period-02 | 2 | 四翼（膜）：背上加一对昆虫膜翅 | [period-02](subjects/wing-atlas/period-02/README.md) |
| wing-atlas | period-03 | 2 | 四翼（皮）：背上加一对蝙蝠皮翼 | [period-03](subjects/wing-atlas/period-03/README.md) |
| wing-atlas | period-04 | 2 | 四翼（飞鱼鳍）：背上加一对飞鱼长鳍（自带「飞」义） | [period-04](subjects/wing-atlas/period-04/README.md) |
| wing-atlas | period-05 | 2 | 四翼（鹤羽）：背上加一对鹤的白翼（收官） | [period-05](subjects/wing-atlas/period-05/README.md) |
| horn-atlas | period-01 | 3 | **基准**：无角的马（无移植件，作后四部分的参照） | [period-01](subjects/horn-atlas/period-01/README.md) |
| horn-atlas | period-02 | 2 | 鹿角：额顶长出一对分叉鹿角 | [period-02](subjects/horn-atlas/period-02/README.md) |
| horn-atlas | period-03 | 2 | 牛角：额顶长出一对粗壮牛角 | [period-03](subjects/horn-atlas/period-03/README.md) |
| horn-atlas | period-04 | 2 | 羊角：额顶长出一对卷曲羊角 | [period-04](subjects/horn-atlas/period-04/README.md) |
| horn-atlas | period-05 | 2 | 独角鲸长牙 + 犀角（收官）：霜晨贴面特写 | [period-05](subjects/horn-atlas/period-05/README.md) |

## 六、检查清单

- [ ] **期内**生境/光线/机位/画布恒定（保住该期对照），**期间**各异（每期有身份）
- [ ] **每轮跑过 `score.py`**，且期目录里只收了 ✅ 的镜头（⚠️ 备选与 ❌ 一律不进）
- [ ] 期目录里**没有**半成品（双头/多出个体/退化/一眼假）
- [ ] 每件成品都能在 `manifest.json` 里查到出处（seed / prompt_id / prompt）
- [ ] 本轮有**同轮底座对照镜头**（否则客观指标不可用）
- [ ] `bash make_sheet.sh period <期目录>` 的期速览图是最新的
- [ ] `bash make_sheet.sh subject <子主题>` 的**跨期总览图**（含 `sheet-thumb.jpg` 缩略图）是最新的
- [ ] [`SUMMARY.md`](SUMMARY.md) 里嵌的缩略图与 `subjects/*/sheet-thumb.jpg` 一致（重跑 `make_sheet.sh all` 即可）
- [ ] `work/` 没有混进仓库（`git status` 干净）
- [ ] 轮次记录写进了 `subjects/<子>/rounds/`

---

## 九、仓库体积维护（**每次推不动先看这里**）

本项目是**图像密集**仓库：每交付一个子主题约增加 25–30MB（成品 PNG + 对照 + 合并图 + 审计图）。
Gitee 的仓库配额是 **1024MB**，超限时 `git push` 会被 **pre-receive hook 拒绝**
（`Push rejected for repository [size exceeds limit]`）——**这不是本地问题**。

| 现象 | 原因 | 处置 |
|------|------|------|
| push 被拒，提示 `Repo size: … exceeds quota 1024MB` | 远端历史里累积了旧版本对象（本地 `git gc` 不影响远端） | 打开 **<https://gitee.com/thz_summer/gits/settings#git-gc>** 点一次 **Repository GC**，再重新 push |

**节奏**：约每推进 **2–3 个子主题**跑一次 GC（一次 GC 能把远端从 ~1400MB 压回 ~460MB）。

**为什么不用"把成品改 JPEG"来省体积**：实测 JPEG q2 会给同一张图引入
**平均通道差 ≈ 1.21**，而本仓「区域差 < 1.5 判定为移植句空操作」的阈值就在旁边——
噪声底会直接吃掉判据。所以**合并图/审计图用 JPEG，成品与对照必须 PNG**
（详见 [image-tools/SKILL.md](../../skills/image-tools/SKILL.md)）。

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 由 `owl-splice` 重构为拼接项目：项目 → 子主题（按动物对）→ 期（只放成品）；新增 `curate.py` 与成品门槛，`work/` 移出仓库 | 小七 |
| 2026-10-05 | **v1.0** | `horn-atlas` **五部分收官（零失败）** —— **12 个子主题 / 60 期 / 135 成品全部交付**；新增 [`SUMMARY.md`](SUMMARY.md) 全线总结（机制结论总表 51–110 / 否定结论清单 / 后续建议）；补规律 109–110 | 小七 |
| 2026-10-05 | v0.14 | `wing-atlas` **五部分收官**（丙组 1/2，11 成品全首选）；提出**规律 107（语义类别必须与落点功能匹配，鱼胸鳍 0%）**与 108（图鉴册的基准部分） | 小七 |
| 2026-10-05 | v0.13 | `tree-beast` **五期收官**（**乙组完成**，11 成品）；**兽足 0% 的否定结论**；补规律 105/106（两条独立门槛 / 换底座是否降命中率取决于落点性质） | 小七 |
| 2026-10-05 | v0.11 | `flower-bird` **五期收官**（乙组 4/5，12 成品全首选）；花瓣第三次验证「典范结构换不掉」；补规律 102–104（换底座要重验命中率 / 写法连着落点看 / **机制限制常常给出更好的构图**） | 小七 |
| 2026-10-05 | v0.10 | `flytrap-fang` **五期收官**（乙组 3/5，11 成品全首选）；提出**规律 99（判据落在落点而非整体）**、100（边界附属物≈属性）、101（接缝决定可信度·假设） | 小七 |
| 2026-10-05 | v0.9 | `cordyceps` **五期收官**（乙组 2/5，11 成品全首选）；补规律 96–98（**属性可腾出/结构不可腾**、从体表长出的件无需承载结构、换呈现媒介＝收官升级） | 小七 |
| 2026-10-05 | v0.8 | `lichen` **五期收官**（乙组开工，11 成品全首选）；提出**规律 92（底座形态自由度决定移植难度）**与 93–95（尺度即呈现 / 呈现救弱期 / 对照做了一半要扣分） | 小七 |
| 2026-10-05 | v0.7 | `deer-crane` **五期收官**（甲组完成，9 成品/部分成立为主）；补规律 89–91（**改形不改质** / 空位非充分 / **不同形优先**）；修 `curate.py` 的 `--force` 语义（曾把旧成品条目与新条目合并，导致期目录出现同源两份） | 小七 |
| 2026-10-04 | v0.6 | `fish-bird` **五期收官**（11 成品）；发现规律 85–88（**生境是硬约束**、场景兼容性按区域、典范结构腾不出占位、「唯一部件」也能撑起子主题），并据此把排期主轴改为「出水阶段」 | 小七 |
| 2026-10-04 | v0.5 | `turtle-snake` **五期收官**（13 成品，含收官「玄武」）；补规律 81–84（空间关系写法、先怀疑写法、腾出占位分档、多 take 检验） | 小七 |
| 2026-10-04 | v0.4 | `cat-eagle` 期 02–05 **呈现重做**（五期各有身份）；据 R10–R17 补规律 79/80（姿态句不得提部位、呈现层不是中性的）；`cat-eagle` period-06 鹰头猫正式作废 | 小七 |
| 2026-10-04 | v0.3 | `dragon-nines` 五期收官（期 05【龙首特写】）；据实测规律 73–78 **重排 7 个子主题的期内容**（清掉头部件与无载体件），`eye-atlas` 改写为 `horn-atlas`、`wing-atlas` 改为「第二对翅」 | 小七 |
| 2026-10-04 | v0.2 | 改名 `animal-splice` → `bio-splice`：概念由「动物拼接」扩为「生物拼接」（植物/真菌/藻/地衣可作底座或供体），子主题扩至 12 个；成品前缀 `as-*` → `bs-*`；`make_sheet.sh` 增 `all` 模式 | 小七 |
| 2026-10-05 | v0.12 | 增补「仓库体积维护」一节：Gitee 1024MB 配额与 Repository GC 的处置节奏 | 小七 |
| 2026-10-05 | v1.1 | 交付物约定补「子主题合图缩略图」`sheet-thumb.jpg`（`make_sheet.sh` 一并产出）；SUMMARY 首页嵌入 12 张缩略图 | 小七 |
