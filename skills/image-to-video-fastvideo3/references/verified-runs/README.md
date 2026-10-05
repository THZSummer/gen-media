# 真机验证记录（2026-10-03）

> 返回[技能首页](../../SKILL.md)

本目录保留**已真机执行过**的提交图与请求台账，作为"这套参数确实能跑"的证据。
`*.api.json` 就是当时 `POST /prompt` 发出去的完整 API 图（未改动），
可用 `GET /history/{prompt_id}` 向服务器复核。

## 三次运行

| 运行 | 提交图 | prompt_id | 耗时 | 成品 |
|------|--------|-----------|------|------|
| 首帧（i2v） | [i2v-first-frame.api.json](i2v-first-frame.api.json) | `5de7f02c-d0c2-4281-9483-63fbd3ed54d8` | **180.2 s** | 576×736 / 56 帧 / 2.333 s / 761 KB |
| 首帧+尾帧（fl2va） | [i2v-first-last-frame.api.json](i2v-first-last-frame.api.json) | `dadcfbc4-15ba-42ea-b57f-8a6986d751ba` | **195.2 s** | 576×736 / 56 帧 / 2.333 s / 806 KB |

台账：[requests.jsonl](requests.jsonl)（含 `elapsed_s` / `input_image` / `last_frame_image` / ffprobe 摘要）。

## 公共参数

```
--duration 2            → 56 帧 / 2.333 s（17k+5 栅格，与 --plan 预测一致）
--megapixels 0.4        → 画布 576×736（输入图 1024×1360，比例 1.328，32 对齐）
--seed 42
steps 8 · sampler res_multistep · scheduler simple · attention "comfy kitchen attention"
```

首帧 = `final-bone-china-princess.png`；尾帧 = `final-bone-china-princess-v2.png`
（均来自 image-gen 的骨瓷国公主项目，上传后走 `/upload/image`）。

## 结论

| 问题 | 答案 |
|------|------|
| 能出片吗 | ✅ `status: success` ×2，画布/帧数/时长与 `--plan` 预测完全一致 |
| 有声音吗 | ✅ AAC 32 kHz 双声道 |
| 首帧条件生效吗 | ✅ 输出首帧与输入图 SSIM **0.929** / PSNR **30.3 dB**（高度相似，但**非像素级复制**：模型重绘并轻微重新构图） |
| 蒸馏权重支持 fl2va 吗 | ✅ **支持**。传首尾帧跑通，**帧 0 = 图 A，帧 55 = 图 B**，视频在两张图之间插值。这裁定了两个官方模板的矛盾说法——T2V 模板那句 "supports t2va only；FL2VA 未蒸馏" 已过时 |
| 提交图与服务器执行图一致吗 | ✅ 逐字段比对：**22 节点 / 0 处差异** |

## 未覆盖

- 只跑了 2 秒 / 0.4MP 这一档；更长帧数、更大画布按 SKILL.md 的经验公式估时
- 多参考（Ref2VA）未测（模板声明未蒸馏）
- 单参数敏感性未做真机矩阵（参数正确性由 `--plan` + 62 项离线断言覆盖）
