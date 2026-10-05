# 真机验证记录（2026-10-03）

> 返回[技能首页](../../SKILL.md)

本目录保留**已真机执行过**的提交图与请求台账，作为"这套参数确实能跑"的证据。
`t2v.api.json` 就是当时 `POST /prompt` 发出去的完整 API 图（未改动），
可用 `GET /history/{prompt_id}` 向服务器复核。

## 运行

| 运行 | 提交图 | prompt_id | 耗时 | 成品 |
|------|--------|-----------|------|------|
| 文生视频（t2v） | [t2v.api.json](t2v.api.json) | `6ca04e25-8e68-49d8-b838-abb22edf419c` | **165.3 s** | 576×736 / 56 帧 / 2.333 s / 646 KB |

台账：[requests.jsonl](requests.jsonl)。

## 参数

```
--duration 2                                  → 56 帧 / 2.333 s（17k+5 栅格）
--aspect-ratio "3:4 (Portrait Standard)" --megapixels 0.4
                                              → ResolutionSelector 算出 576×736（32 对齐）
--seed 42
steps 8 · sampler res_multistep · scheduler simple · attention "comfy kitchen attention"
```

## 结论

| 问题 | 答案 |
|------|------|
| 能出片吗 | ✅ `status: success`，画布/帧数/时长与 `--plan` 预测完全一致 |
| 有声音吗 | ✅ AAC 32 kHz 双声道 |
| 内容听 prompt 吗 | ✅ 画面逐项吻合：银累丝冠镶蓝宝石、珍珠项链与珍珠耳坠、白色蕾丝礼服、瓷玫瑰捧花、纱幕扬起、镜头推近 |
| 画幅旋钮生效吗 | ✅ `--aspect-ratio` + `--megapixels` → 576×736（该旋钮曾被一个转换器 bug 静默吞掉，已修复并有回归测试） |
| 提交图与服务器执行图一致吗 | ✅ 逐字段比对：**20 节点 / 0 处差异**（另外用服务器上更早的一次真实运行复核过同样结论） |

## 未覆盖

- 只跑了 2 秒 / 0.4MP 这一档；更长帧数、更大画布按 SKILL.md 的经验公式估时
- 单参数敏感性未做真机矩阵（参数正确性由 `--plan` + 60 项离线断言覆盖）
