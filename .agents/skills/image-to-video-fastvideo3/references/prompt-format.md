# FastH3 图生视频（fl2va）的 prompt 写法

> 返回[技能首页](../SKILL.md) ｜ 真实样本：`python3 scripts/comfyui_i2v.py --show-default-prompt`

图生视频的 prompt 和文生视频**同一个三节结构**（见 [../../text-to-video-fastvideo3/references/prompt-format.md](../../text-to-video-fastvideo3/references/prompt-format.md)），
但在开头多一句把**输入图**引进来：

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
integrated_multimodal_description: [Shot 1] ... [Shot 2] At 01.200, ... [Shot 3] At 02.500, ...
overall_soundscape: ...
non_diegetic_music: ...
```

## 第一句在做什么

- **`<Picture 1>`** 是模板给输入图起的引用名：后面的描述里可以继续用它指代"画面里那个人/那个东西"
- **`at 0.00 seconds ... is fully referenced`** 声明从第 0 秒开始完全按这张图；想让它**动起来但不变形**，
  就要在 `[Shot 1]` 里把这个主体**重新描述一遍**（外观、服装、材质），模型才知道哪些该保留
- 模板样本的写法是"把它当成一个必须保持一致的既有主体"，然后在后续镜头里改变**姿态、运镜与画面效果**

## 图生视频特有的注意点

| 事项 | 说明 |
|------|------|
| **画幅跟着输入图走** | 没有 `aspect_ratio` 参数。要改比例就**改输入图**（裁剪/扩展），画幅由 `ImageScaleToTotalPixels → GetImageSize` 从图里读 |
| **`--megapixels` 只定尺寸** | 它决定目标画布总像素（默认 0.4MP ≈ 640×640），**不会**改变喂给模型的那一帧；模板把 LoadImage 的**原图**直接接到 `first_frame` |
| **输入图别给太大** | 因为上一行，原图会整张喂进模型。建议先把输入图压到与目标画布同量级（例如 ≤1MP），否则白白多传数据 |
| **首帧 ≠ 静止** | 想"完全照搬这张图再让它动"，要在 `[Shot 1]` 里写清哪些不变、哪些开始动；只写"图里的人动起来"通常会漂 |
| **尾帧** | 本技能支持 `--last-frame`（脚本注入一个 LoadImage 接到 `last_frame`）；模板默认只接首帧 |

## 分镜时间码

模板样本 4 个镜头、5 秒，切点写作 `At 01.200,` / `At 02.500,` / `At 03.800,`
（文生视频那份模板写的是 `At 00:02.100`，两种写法官方都在用）。

## 与文生视频 prompt 的差别

- 文生视频：从零描述**整个画面**
- 图生视频：先**锚定**输入图里已有的主体，再描述**它怎么动、镜头怎么动、画面加什么效果**
- 声音两节（`overall_soundscape` / `non_diegetic_music`）写法完全一样，不能省

> ⚠️ 以上是"官方模板这么写、模板的接口这么连"的记录。**本工作流尚未真机出过片**，
> 所以"不写 `<Picture 1>` 那句会怎样"这类对照结论都没有实测依据。
