---
name: comfyui-image-tools
description: 不用 AI 的确定性图片处理：拼版速览图（contact sheet）、像素比对与 PSNR/SSIM、PNG 元数据剥离、缩放/裁切/格式转换。基于 ffmpeg + numpy，纯本地、无模型、无网络。触发词：拼图、合并图片、速览图、contact sheet、montage、缩略图墙、对比图、像素比对、复现性检查、SSIM、PSNR、去元数据、strip、裁切、缩放。
whenToUse: 当需要把多张图合并成一张速览图、逐像素比对两张图是否相同、计算 SSIM/PSNR、剥离 ComfyUI 写进 PNG 的执行图元数据、或做缩放/裁切等确定性图片操作时使用。**不要**用生成模型做这些事——那会让结果不再是产物的忠实拷贝，也就不能作为判读证据。
---

# 确定性图片处理（无 AI）

**用途**：对已生成的图片做**确定性**处理——拼版、比对、量测、裁切、去元数据。
全程本地，不调用任何生成模型，不占 GPU，不连 ComfyUI。

## 为什么强调"不用 AI"

这些工具产出的东西是**判读证据**：

- 拼版速览图是**你用来评判 prompt / seed 的那张图** → 每格必须逐像素等于实际产物
- 像素比对是**"这轮能不能复现"的判据** → 不能受模型随机性影响

一旦生成模型碰过它们，画面就不再忠实，建立在其上的判断全部作废。
所以这里每个操作都是输入的纯函数。

## 依赖（必须）

| 依赖 | 版本 | 说明 |
|------|------|------|
| **ffmpeg / ffprobe** | 8.x 已验证 | 解码/编码/滤镜（`drawtext` 用于标签）。缺了会给出安装提示 |
| **numpy** | 2.x 已验证 | 像素运算、box 降采样、SSIM/PSNR |

两者本机已就位（`make_macro.sh` 本来就用 ffmpeg 做 lanczos 裁切）。
可用 `$FFMPEG` / `$FFPROBE` 指定二进制路径。

> 不依赖 Pillow / ImageMagick / OpenCV —— 本机没有，也不需要。

## 三个工具

| 脚本 | 作用 |
|------|------|
| `scripts/contact_sheet.py` | 多图合并成一张**带标签**的速览图（支持中文标签） |
| `scripts/pngdiff.py` | 逐像素比对 + **PSNR / SSIM**（复现性判据） |
| `scripts/ffkit.py` | 底层：解码/编码/缩放/裁切/元数据剥离/几何查询 |

## 1. 拼版速览图

```bash
# 整轮出图，按 round.json 顺序，标签 = 镜头名 + seed
python3 scripts/contact_sheet.py --round out/r1/round.json -o out/r1/sheet.png --cols 3

# 显式指定顺序（"-" = 空位），中文标签与标题
python3 scripts/contact_sheet.py a.png b.png - c.png -o sheet.png --cols 3 \
    --title "R1 · 拼接矩阵" 

# 原生分辨率（不做任何重采样）
python3 scripts/contact_sheet.py --glob 'out/r1/*.png' -o sheet.png --cell 0
```

- **标签是真字体**（ffmpeg `drawtext`），装了 CJK 字体就能写中文；默认自动探测
  Noto CJK / DejaVu，也可 `--font` 指定
- 每格默认压到 512px，用 **box 平均**（不是最近邻）——速览图就是用来判读喙、接缝、毛皮过渡的，
  最近邻的锯齿会恰好糊掉要看的细节
- `--round` 会读项目 `run_round.py` 写的 `round.json`，标题自动带上轮次/引擎/seed；
  **某张的 `unapplied` 非空时标题会打上 `UNAPPLIED!`**——那说明该轮有参数没生效，别急着判读

## 2. 像素比对与量测

```bash
python3 scripts/pngdiff.py a.png b.png                 # 0=同 1=异 2=出错
python3 scripts/pngdiff.py a.png b.png --json          # 含 psnr/ssim/chunks
python3 scripts/pngdiff.py a.png b.png --tolerance 2   # 忽略 1~2 的通道差
```

判据是**解码像素**，不是文件 sha。ComfyUI 把执行过的图写进 PNG 的 `tEXt`，
所以换了 `filename_prefix` 就会变 sha 而画面不变（实测：同 0 个像素不同、sha 却不同）。

`mean_abs_diff` 还能当**"这句 prompt 到底做了多少事"的仪表**：
数值接近 0 说明那句是空操作（本项目就用它证明了"超现实"语义句无效）。

PSNR/SSIM 说明：`psnr` 是标准 MSE 形式；`ssim` 是 11×11 均匀窗口 + 标准常数
（K1=0.01 / K2=0.03）。**这是我们自己的实现，不是 scikit-image 的逐位克隆**——
本仓曾在一份技能文档里引用 SSIM 0.929 / PSNR 30.3 dB 却没有实现，那两个数字当时不可复现，现在可以重算了。

## 3. 底层操作

```bash
python3 scripts/ffkit.py info a.png b.png            # 几何 / 编码 / 元数据 chunk
python3 scripts/ffkit.py pngchunks a.png             # 只看 chunk（元数据取证）
python3 scripts/ffkit.py strip in.png -o out.png     # 剥掉 tEXt 等（像素不变）
python3 scripts/ffkit.py resize in.png -o s.png --max-edge 512
python3 scripts/ffkit.py crop in.png -o f.png --box 100,200,400,400
python3 scripts/ffkit.py scale in.png -o x2.png --factor 2
```

### PNG 还是 JPEG

`encode()` **按扩展名选编码器**：

| 输出 | 用途 | 说明 |
|------|------|------|
| `.png` | **成品与对照图**（要逐像素比对的东西） | 无损；`minimal=True` 时输出固定为 `IHDR/IDAT/IEND` |
| `.jpg` / `.jpeg` | **速览图 / 合并图 / 审计图**（只用来看的东西） | 有损，`quality=`（ffmpeg `-q:v`，2 = 视觉无损，默认 3）；体积约为 PNG 的 1/8 |

> ⚠️ **不要把要参与像素判据的图存成 JPEG**：实测 JPEG q2 会给同一张图引入
> **平均通道差 ≈ 1.21** 的块效应，而本仓「区域差 < 1.5 判定为空操作」的阈值就在旁边——
> 噪声底会直接吃掉判据。**成品与对照一律 PNG，速览类一律 JPEG。**

> ⚠️ **ffmpeg 无法关掉 `pHYs`**（`-map_metadata -1`、`setsar=1` 都试过无效），
> 而 ComfyUI 本来不写它。所以 `encode()` 之后会再跑一遍纯 Python 的
> `drop_metadata()`，输出固定为 `IHDR/IDAT/IEND` ——与被比对的文件同一约定。
> 纯 Python 编解码只保留这一处（chunk 级裁剪），解码/编码本身交给 ffmpeg。

## 与生成技能的关系

依赖方向是**单向**的：生成技能依赖本技能，反之不成立。

```
image-tools（ffmpeg + numpy，无 AI）
    ▲
    ├── text-to-image-comfyui   的 verify_params.py / test_skill.py 用 pngdiff
    └── image-edit-comfyui      的 _shared.py 把本技能加进 sys.path
```

因此库层（`ffkit` / `pngdiff`）的签名要保持稳定，改动后必须跑全部技能的
`test_skill.py`（见下）。

## 验证

```bash
# 全离线自检：不需要服务器、不需要模型、不需要网络
python3 scripts/test_skill.py
```

覆盖：编解码往返逐字节一致（RGB/RGBA）、box 降采样精确均值、裁切裁剪、
元数据剥离后像素不变、`psnr/ssim` 的教科书样例（同图 → inf/1.0；均匀 +1 → 48.13 dB；
噪声 → SSIM<0.2；不相似排序正确）、容差、几何不匹配、非图片文件报错、
拼版尺寸/空位/标签墨迹、**对抗性标签**（`:` `'` `%` `,` `[` `]` `=` `\`）不破坏 filtergraph、
中文标题真的被画出来、`--round` 模式与 `UNAPPLIED!` 提示。

## 检查清单

- [ ] `ffmpeg -version` 与 `python3 -c "import numpy"` 都可用
- [ ] 速览图用的是**产物原图**，不是已经被处理过的中间文件
- [ ] 判读前先看标题：出现 `UNAPPLIED!` 说明该轮参数没生效，先别下结论
- [ ] 说"复现了"要报像素结论（`identical pixels`），不要报文件 sha
- [ ] 交付外发图片前跑一次 `strip`（去掉内嵌执行图，体积也小很多）
