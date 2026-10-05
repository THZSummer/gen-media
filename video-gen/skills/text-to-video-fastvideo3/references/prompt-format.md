# FastH3 的 prompt 写法（t2va：视频 + 音频一起生成）

> 返回[技能首页](../SKILL.md) ｜ 真实样本：`python3 scripts/comfyui_video.py --show-default-prompt`

MiniMax-H3 是 **t2va** 模型：一次生成画面**和**声音。所以 prompt 不是"描述一张图"，而是
"描述一段有声音的片段"。工作流自带的模板 prompt 就是标准形态，一节不能少：

```text
integrated_multimodal_description: [Shot 1] Cinematic, a wide-angle shot ... The camera pushes in slowly ...
[Shot 2] At 00:02.100, the camera cuts to a medium shot ... The camera arcs right at a medium speed ...
[Shot 3] At 00:03.600, the camera cuts to a wide tracking shot ... The camera pulls out at a fast speed ...
overall_soundscape: A faint, continuous urban hum ... A loud, resonant thud is heard ... followed by the crisp ...
non_diegetic_music: Electronic bass music, fast tempo, featuring a heavy, rhythmic drum machine beat ...
```

## 三节各自负责什么

| 节 | 写什么 | 不写会怎样 |
|----|--------|-----------|
| `integrated_multimodal_description` | 逐镜头：画面内容 + **动作的先后** + **运镜** + 画面内文字 | 只会得到一个近乎静止的镜头 |
| `overall_soundscape` | 环境底噪 + 同期声（脚步、布料、器物） | 音频轨趋于死寂或随机 |
| `non_diegetic_music` | 配乐风格/速度/乐器/有没有旋律起伏 | 配乐会缺位或与画面情绪不符 |

## 逐镜头的写法

- **用 `[Shot N]` 分镜**，切镜时刻用时间码引出：`[Shot 2] At 00:02.100, ...`
  （模板样本：5 秒放 3 个镜头，切点 00:02.100 / 00:03.600）
- **动作要写成过程**，不是状态：
  ✅ `The man lowers his raised foot, and the massive tan boot descends rapidly, striking the pavement. He then raises both hands to adjust his cap's brim.`
  ❌ `a man standing on the pavement`
- **运镜要显式**：`The camera pushes in slowly` / `cuts to a medium shot` / `arcs right at a medium speed` / `pulls out at a fast speed`
- **镜头数要与时长匹配**：5 秒 3 镜是模板的密度；镜头多了每个都来不及动
- 画面内文字可以直接写进描述（模板样本里有 `"STREETWEAR"`、`"VOL. 1"`、`"AVAILABLE NOW"` 三段排版文字）

## 与图像提示词的区别

- **不需要**材质咒语（`8K`、`masterpiece`、`ultra detailed` 之类）：引擎不是 SD 系文生图模型，
  写"有声音的片段"更有效
- **必须**写运动与声音：这两件事在图像 prompt 里根本不存在
- 想拿到"骨瓷/丝绸"这类材质，按图像那边的经验写**具体的物理项**（层数、厚度、透光、边缘），
  而不是形容词堆叠

## 实测记录

- 用户那次 5 秒 640×640 的实跑成品：**H.264 视频 + AAC 音频（32 kHz 双声道）**，
  `overall_soundscape` / `non_diegetic_music` 两节描述的声音确实被生成出来了。
- 音频不需要（也没有）单独的开关：这个工作流把音频 VAE（`minimax_h3_audio_vae_fp32`）
  和视频 VAE 都接在同一个采样结果上，`CreateVideo` 把两路合成一个文件。

> ⚠️ 上面是"模板这么写、成品确实带音频"的事实记录，**不等于**做过"删掉音频两节会怎样"的对照实验。
