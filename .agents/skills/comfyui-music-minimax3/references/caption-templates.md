# 配乐 caption 模板（MiniMax Music 3 · 山海经图赞）

> 本文件是 [SKILL.md](../SKILL.md) 的配套用词库；选曲规则见 `projects/shanhai-jing/DOUYIN.md` §九。
> 目标：**无词、肃穆苍茫、BPM 60–90**，给竖屏图文/短视频当 BGM，不抢画面上的竖排原文与榜题。

## 一、为什么用「caption + 空 lyrics」而不是歌词

MiniMax Music 3 的两个输入分工明确（见工作流内注释）：

| 输入 | 作用 |
|------|------|
| Caption | 结构化描述：Global Metadata → Vocal Details → Arrangement |
| Lyrics | 段落标签（`[intro]`/`[verse]`/`[chorus]`…）+ 歌词文本；**标签是唯一可执行的结构指令**，歌词文本只传递情绪 |

所以我们走**纯音乐**：`--instrumental` 会把 lyrics 写成 `[intro] / [instrumental] / [outro]` 的最小脚本，并在 Caption 里**显式否掉人声**（"no vocals / no humming / no choir"）。
⚠️ 模型是否 100% 不给人声是它的行为，不是保证——**交付前必须用耳朵验一遍**（本技能的测试只验证管线，不验证听感）。

## 二、四个模板（直接复制，按需改 BPM 与主奏乐器）

### 模板 A · 古琴独奏（最稳，荐为默认）

```
Global Metadata: Chinese guqin instrumental, 66 BPM, D pentatonic, solemn and vast, ancient ritual atmosphere, slow and unhurried throughout, no vocals at all.
Vocal Details: fully instrumental, no voice, no humming, no choir, no lyrics.
Arrangement: solo guqin with sparse plucked notes and long silences, a distant low bamboo flute (xiao) answering occasionally, faint stone chime accents, deep hall reverb like a mountain temple, subtle tape hiss, no drums, no percussion, no bass.
```

### 模板 B · 箫与埙（更空、更苍茫；适合"荒山异兽"）

```
Global Metadata: Chinese xiao and xun instrumental, 60 BPM, minor pentatonic, desolate and open, misty mountain air at dawn, unhurried, no vocals.
Vocal Details: instrumental only, no voice, no breathy vocalise, no choir.
Arrangement: low bamboo flute (xiao) carrying a long sustained melody, clay ocarina (xun) answering in the low register, a single far-off temple bell every few phrases, wind-like room tone, almost no rhythm, no percussion.
```

### 模板 C · 编钟与鼓（有仪式感但克制；适合封面/片头）

```
Global Metadata: Chinese ritual instrumental, 72 BPM, pentatonic, ceremonial and dignified, bronze bells with a slow deep drum, no vocals.
Vocal Details: instrumental only, no chant, no choir, no voice.
Arrangement: sparse bronze bianzhong bell motifs, a single low frame drum on the downbeat every two bars, sustained low strings underneath, large stone-hall reverb, no melody in the high register.
```

### 模板 D · 筝与弦乐（略明亮；适合"验算/讲解"段，不要用在肃穆段）

```
Global Metadata: Chinese guzheng with soft strings, 84 BPM, pentatonic, calm and lucid, a quiet workshop mood, no vocals.
Vocal Details: instrumental only, no voice, no humming.
Arrangement: plucked guzheng arpeggios, sustained warm string pad, light paper-like percussion texture, clean and close-miked, small room reverb, nothing busy.
```

## 三、按内容段位选模板（与 `DOUYIN.md` 的内容公式对齐）

| 段 | 模板 | 理由 |
|----|------|------|
| ① 反差（封面/前 3 秒） | C | 有仪式感但不吵，配"你以为的 X"这句钩子 |
| ② 原文 | A | 古琴独奏最像"读古籍"的环境音，不抢字 |
| ③ 验算 | D | 略明亮，配"我们试了两种写法"的信息密度 |
| ④ 结论 + 提问 | B | 空下来，把注意力交给最后那句提问 |

> 一条 20–30 s 的图文/短视频**建议只用 1 个模板**；上面这张表是给 40 s 以上的短视频分段用的。

## 四、负向写法（实测有效，写在 caption 里比写在 lyrics 里有用）

- 明确排除：`no vocals` / `no humming` / `no choir` / `no drums` / `no percussion` / `no bass`
- 明确排除"现代感"：`no synth pad` / `no electronic beat` / `no cinematic braams`
- 明确排除"燃"：`never building to a climax` / `no riser` / `no drop`

## 五、成本与参数基线（真机实测）

| 项 | 值 |
|----|----|
| 20 s 音频 | 约 334 s 墙钟（`--eta` 会先报） |
| 60 s 音频 | 约 1000 s 墙钟（用户实测） |
| 换算 | ≈ **16.7 s 墙钟 / 1 s 音频**（`SECONDS_PER_AUDIO_SECOND`，RTX 4060 Ti 8 GB + fp16 DiT + 30 步 + tiled decode） |
| 常用参数 | `--instrumental`、`--duration 20~30`、`--steps 30`、`--cfg-scale 1.7`、`--seed <固定值>`、默认 tiled decode |
| 复现 | 同一 `--seed` + 同一 caption + 同一 duration → 同一条音频；`<prefix>.api.json` 与 `requests.jsonl` 一并留档 |

## 六、许可（⚠️ 商用前必读）

权重是**开放权重**，采用 **MiniMax-Music3 COMMUNITY LICENSE**（模型卡见 [Comfy-Org/MiniMax-Music-3](https://huggingface.co/Comfy-Org/MiniMax-Music-3)，ComfyUI 教程见 [docs.comfy.org](https://docs.comfy.org/tutorials/audio/minimax/minimax-music-3)）。
社区许可通常含**署名**与**可接受使用**条款，且可能对规模/竞争用途另设条件——**具体以许可原文为准，本技能不代为解释法律条款**。

> 对我们项目的意义：自产 BGM 把"站内曲库授权只覆盖本平台"的问题换成了"模型许可允许怎么用"的问题。
> 在 `DOUYIN.md` §九 第 6 条（商用边界）未改成"已解决"之前，**自产音频按"待核实"处理**。
