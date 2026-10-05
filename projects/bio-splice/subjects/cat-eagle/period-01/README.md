# 第一期 · 猫头鹰（猫的头 + 鹰的身体）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [项目索引](../../../../README.md)
> 引擎：Z-Image-Turbo　尺寸：1024×1024　steps：12　**全 5 张共用 seed 4201**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期成品

词面直译「猫头鹰」：**猫的头 + 鹰的身体**。三种拼接语义各一张，供选用。

| # | 文件 | 拼接语义 | seed | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-owl-seamless.png`](01-owl-seamless.png) | **A 无缝融合**（接合处自然过渡，「像进化成这样」） | 4201 | `be679edd` | `64b994f7f3` |
| 2 | [`02-owl-seam.png`](02-owl-seam.png) | **B 可见接缝**（颈前缘有纵向缝线，标本感） | 4201 | `c16ee1aa` | `768e4f2e67` |
| 3 | [`03-owl-surreal.png`](03-owl-surreal.png) | **C 超现实**（比例刻意不对，仍按纪实拍摄） | 4201 | `1ccb65b9` | `845bb12956` |

> ⚠️ **C 与 A 几乎相同**：同 seed 下两版 `mean_abs_diff` 仅 **8.9**（全部对照里最小），
> 说明"超现实"那句是**空操作**。若只要两张，保留 1 与 2 即可。

### 对照（不是本期成品）

| 文件 | 说明 |
|------|------|
| [`controls/cat.png`](controls/cat.png) | 退化角：纯猫。与成品同一套摄影语言，用来校准"哪部分是拼接带来的" |
| [`controls/eagle.png`](controls/eagle.png) | 退化角：纯鹰。成品 1 的机位/姿态几乎与它重合——**同一只鹰换了个猫头** |

## 二、单变量设计

组装式（权威源见 [`run_round.py`](../../../run_round.py) 的 `_photo()`）：

```
{CN 取景句}{主体定义}. {拼接语义句} {环境句} {摄影层}
     恒定        ↑变化      ↑A/B/C变化      恒定            恒定
```

- **唯一变量 = 拼接语义句**。取景句、环境句（雾中秋草）、摄影层
  （600mm f/4 浅景深 阴天柔光 无锐化）全轮恒定
- **全 5 张共用 seed 4201**：同 seed 让拼接体复用对照组的构图，A/B/C 之间才可比
- 取景句用中文、材质与解剖用英文（沿用本仓已验证的中英分工）

## 三、两处关键手法

1. **不能直接写「猫头鹰」**——模型会读成真实存在的那个物种。必须写**分解式**：
   `whose head is entirely a domestic cat's and whose body is entirely a golden eagle's`。
   这与该词的构词法同构。
2. **鹰的身体必须保留翅膀**（`folded wings`），否则会漂成无翅的猫头鹰玩偶。
   注意本引擎**没有负向提示词**，所有约束只能正向写。

## 四、如何复现

```bash
cd ../../..                      # 到项目根
python3 run_round.py 1 --dry     # 打印逐字 prompt
python3 run_round.py 1           # 重新出图到 work/cat-eagle/r1/（固定 seed，逐像素可复现）
python3 curate.py --period subjects/cat-eagle/period-01 \
    --from work/cat-eagle/r1/round.json \
    --pick owl-seamless=01-owl-seamless \
    --pick owl-seam=02-owl-seam \
    --pick owl-surreal=03-owl-surreal \
    --control cat=controls/cat --control eagle=controls/eagle \
    --note "第一期：猫头鹰（猫的头 + 鹰的身体）" --force
bash make_sheet.sh period subjects/cat-eagle/period-01
```

> 复现判据是**解码像素**，不是文件 sha（ComfyUI 把执行图写进 PNG 的 `tEXt`，
> 换 `filename_prefix` 就会变 sha 而画面不变）。用
> `python3 ../../../../.agents/skills/image-tools/scripts/pngdiff.py a.png b.png`。

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第一期交付：猫头鹰 3 张 + 2 对照，附出处与复现步骤 | 小七 |
