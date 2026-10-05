# 语音合成（Text-to-Speech, TTS / 后期配音）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 输入：文本。输出：语音音频（mp3）。当前走 `seed-tts-2.0`（Agent Plan Medium 含，agent-plan profile）。
> 返回[方法总览](../README.md)

> ⚠️ **arkcli 不覆盖 TTS/ASR**。TTS 走 OpenSpeech 服务（独立于 Ark Runtime），需自己写脚本调 HTTP 流式接口。`+chat`/`+gen`/`+code-example` 均不支持语音模型。

---

## 一、主题定位

语音合成是**从文本生成人声**的路径：给一段文字，拿一段语音。在视频生成流程里，它主要用于**后期配音**——给成片加旁白、台词、文案朗读。

### 典型用途

| 用途 | 说明 |
|------|------|
| **视频旁白** | 纪录片/短片解说，TTS 生成 → ffmpeg 混音入视频 |
| **产品台词** | 广告片口播文案 |
| **多语言配音** | 同一画面换不同语言旁白 |

### 与视频自带音频的区别

| | TTS 后期配音（本篇） | 视频生成自带音频 |
|---|---------------------|-----------------|
| 谁生成 | OpenSpeech（独立服务） | Seedance 1.5-pro（`--generate-audio`） |
| 可控性 | 文本逐字可控、可反复生成 | 不可控 |
| 适用模型 | 任意视频模型（不依赖音画能力） | 自带音频：✅ 1.5-pro / 2.0（260128）；⛔ 2.0-fast / mini 无音频，须后期 TTS |
| 工作流 | 视频生成完再配音 | 视频生成时同步出音 |

> ⚠️ mini 无音频输出 → 后期 TTS + ffmpeg 混音是 2.0 系列的标准配音路径。

---

## 二、模型与路由

| 项 | 值 |
|----|----|
| 模型 | 豆包语音合成 2.0（`doubao-seed-tts-2.0`） |
| Resource-Id | `seed-tts-2.0` |
| Profile | agent-plan（TTS 含在 Medium 套餐，走 ARK API Key） |
| 端点 | `https://openspeech.bytedance.com/api/v3/plan/tts/unidirectional`（`/plan/` 路径 = Agent Plan 通道）|
| 认证 | Header `X-Api-Key: <ark-api-key>` + `X-Api-Resource-Id: seed-tts-2.0` |

---

## 三、请求与解码

### 请求体

```json
{
  "req_params": {
    "text": "需要合成的文本",
    "speaker": "zh_female_vv_uranus_bigtts",
    "audio_params": {
      "format": "mp3",
      "sample_rate": 24000
    }
  }
}
```

### 响应（流式 JSON Lines）

每行 `{"code":0,"data":"<base64 音频块>"}`，`code=20000000` 表示结束；逐行 `base64.b64decode(data)` 拼接成完整 mp3。

### 常用 speaker

| speaker | 音色 | 适用 |
|---------|------|------|
| `zh_female_vv_uranus_bigtts` | 沉稳女声 | 旁白、解说 |
| 其他 | 见控制台语音合成音色列表 | - |

---

## 四、命令 / 脚本

调用示例见 `projects/survival-island/scripts/tts_narration.py`（流式接收 + base64 拼接 + 落盘，可复用）。

```bash
python3 scripts/tts_narration.py   # 生成全部旁白段
```

> 拿 API Key：`arkcli auth status` 看掩码，完整值在 `~/.arkcli/identities/<volc-id>/apikey.json`。

---

## 五、混音入视频（ffmpeg）

> ⚠️ **不要用 `-c:a aac` 重编码**，mp3 直塞 mp4（`-c:a copy`）即可，实测 aac 重编码后播放器可能不识别音轨。

```bash
# 拼接多段旁白（重编码避免 DTS 错乱）
ffmpeg -f concat -safe 0 -i concat_audio.txt -c:a libmp3lame -b:a 128k narration_full.mp3

# 混入视频（视频 copy + 音频 copy）
ffmpeg -i video.mp4 -i narration_full.mp3 \
  -c:v copy -c:a copy -map 0:v -map 1:a -shortest out.mp4
```

- 视频流 `-c:v copy` 不重编码；音频流 `-c:a copy` 直塞
- mp3 拼接（concat）时**禁止** `-c copy`（DTS 错乱），须重编码 `-c:a libmp3lame`
- 单段旁白对齐视频：`ffmpeg -i seg.mp3 -af apad -t <时长> seg_pad.mp3`

---

## 六、检查清单

- [ ] 端点用 `/plan/` 路径（Agent Plan 通道）
- [ ] Header 带 X-Api-Key + X-Api-Resource-Id: seed-tts-2.0
- [ ] 流式解码：base64 逐行拼接，code=20000000 收尾
- [ ] 旁白时长与视频对齐（apad + -t）
- [ ] 混音用 `-c:a copy`，不用 aac
- [ ] 音色选择符合内容调性

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-08-01 | v1.0 | 从方法总览 TTS 章节独立成册：语音合成（seed-tts-2.0），含端点/请求体/流式解码/speaker/混音 | 小七 |
