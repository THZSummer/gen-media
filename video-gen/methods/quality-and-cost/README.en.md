# Quality and Cost Control (Quality & Cost)

> 🌐 Language: **English** | [中文](README.md)

> A cross-cutting topic on trading off picture quality, generation speed, and cost; applies to every input path.
> Back to [method overview](../README.en.md)

---

## 1. Topic positioning

Video generation is far more expensive and slower than image generation. Blindly turning everything up — 1080p + long duration + high priority — can cost several times a draft-mode generation per clip. This topic gives a **staged, on-demand** parameter strategy so the money is spent where it matters.

### The core tension

| Dimension | High quality | Low cost |
|------|--------|--------|
| Resolution | 1080p | 480p |
| Duration | Long | Short |
| Mode | Final | `--draft` draft |
| Priority | `--priority 9` | `--priority 0` |
| Speed | Slow | Fast |

---

## 2. Staged strategy (recommended workflow)

### Stage 1: Direction (try the direction with the cheapest settings)

```
--draft --resolution 480p --duration 5 --priority 0
```
- Purpose: verify whether the prompt/composition/motion direction are right, **without chasing image quality**
- Lowest cost, fastest speed
- Iterate the prompt repeatedly and try several versions

### Stage 2: Locking the approach (settle the plan at medium settings)

```
--resolution 720p --duration 5        (去掉 draft)
```
- Purpose: confirm the final approach at acceptable image quality
- 720p is the **sweet spot for value**, good enough for most scenarios

### Stage 3: Final render (deliver at high quality)

```
--resolution 1080p --duration <需要> --priority 9
```
- Purpose: produce the final deliverable
- Run it once, after the approach is settled, to avoid repeated high-cost generations

> Principle: **try many cheap ones, run the expensive one once**. Do not start by guessing at 1080p.

---

## 3. Parameters in detail

### `--resolution` resolution

| Value | Use | Cost |
|----|------|------|
| `480p` | Draft/direction | Lowest |
| `720p` | Value sweet spot, most scenarios | Medium |
| `1080p` | Final render/delivery | Highest |

- Constrained by the model's supported range (check the enum in supported_params at Step 2)
- A low-res image with a high resolution is pointless (I2V scenarios)

### `--duration` / `--frames` duration

| Parameter | Notes |
|------|------|
| `--duration` | Video seconds; the model ceiling is usually 5-10s |
| `--frames` | Frame count; overrides duration on models that support it |

- The longer the duration, the higher the cost (roughly linear or even superlinear)
- For very long needs, use [long-video-chain](../long-video-chain/README.en.md) chaining instead of forcing it into one clip

### `--draft` draft mode

- Faster, cheaper, lower quality
- **Always use it in the direction stage**; it must be removed for the final render
- Good for batch-testing directions
- ⛔ **fast and mini do not support --draft** (rejected: param_not_supported); in the direction stage use 480p as the low-fidelity substitute

### `--priority` priority

- Range `0-9`; higher means scheduled with higher priority
- **Constrained by model support**: measured that seedance-2.0 / 2.0-fast support `[0,9]`, while **1.5-pro does not**, and passing it is rejected
- Use high priority for urgent renders; for non-urgent work use low priority to save money (low priority may queue longer but may have a lower unit price; actual billing prevails)

### `--seed` reproduction

- Same seed + same parameters = reproducible
- Fix one seed in the direction stage to keep the picture consistent while fine-tuning the prompt
- Changing the seed = a different random result

---

## 4. Strategies for cost-sensitive scenarios

### Batch sample drafts

```bash
# 多版 prompt 用 draft + 480p 快速跑，挑最好的
for p in "版本A..." "版本B..." "版本C..."; do
  arkcli +gen --model "$MODEL" --draft --resolution 480p "$p" --open
done
```
- Omit `--open` in batch scenarios (do not pop up windows for batches of more than 4)

### A single high-quality clip

```bash
# 方案确定后，只跑一次 1080p
arkcli +gen --model "$MODEL" --resolution 1080p --priority 9 \
  "<定稿 prompt>" --open
```

### Vertical short video

```bash
# 短视频平台，9:16，720p 多数够用
arkcli +gen --model "$MODEL" --ratio 9:16 --resolution 720p --duration 5 \
  "<prompt>" --open
```

---

## 5. How model choice affects cost

| Model | Cost/speed | Quality | Applies to |
|------|-----------|------|------|
| `doubao-seedance-2-0-fast` | Fast/cheap | Medium | Batch, direction |
| `doubao-seedance-2-0` | Medium | High | Locking the approach, final render |
| `doubao-seedance-1-5-pro` | Slow/expensive | High | Quality first, not urgent |
| `doubao-seedance-2-0-mini` | Medium | Medium | ⚠️ The only one available on pay-as-you-go; does not support draft/priority/last-frame |

- Use fast in the direction stage to save money and time
- Switch to 2.0 or 1.5-pro for the final render
- 1.5-pro does not support `--priority`; do not pass it

---

## 6. Command templates

```bash
VER=$(arkcli models get doubao-seedance-2-0-fast --transform 'primary_version' | tr -d '"')
FAST="doubao-seedance-2-0-fast-${VER:-260128}"

# 阶段1 定向：最便宜
arkcli +gen --model "$FAST" --draft --resolution 480p --duration 5 --priority 0 \
  "<试方向 prompt>" --open

# 阶段2 定型：720p
arkcli +gen --model "$FAST" --resolution 720p --duration 5 \
  "<定方案 prompt>" --open

# 阶段3 定稿：1080p 高优先级
VER2=$(arkcli models get doubao-seedance-2-0 --transform 'primary_version' | tr -d '"')
PRO="doubao-seedance-2-0-${VER2:-260128}"
arkcli +gen --model "$PRO" --resolution 1080p --priority 9 \
  "<定稿 prompt>" --open
```

---

## 7. Pitfalls

| Symptom | Cause | Fix |
|------|------|------|
| Repeatedly trying 1080p from the start | No staging | Use draft+480p for direction |
| `--priority` rejected | 1.5-pro does not support it | Switch to the 2.0 series or drop priority |
| A draft used as the final | Forgot to remove `--draft` | draft must be removed for the final render |
| A single very long clip is too expensive | Forcing a long video into one clip | Use chaining and split it into several |
| The look differs between versions | Random seed | Fix the seed in the direction stage |
| A low-res image at 1080p | Wasted cost | Match the I2V resolution to the material |

---

## 8. Checklist

- [ ] Three stages: direction (480p+draft) -> locking the approach (720p) -> final render (1080p)
- [ ] Use the fast model for direction and 2.0/1.5-pro for the final render
- [ ] Fix `--seed` in the direction stage to keep consistency
- [ ] Remove `--draft` for the final render
- [ ] Use `--priority` only on models that support it (2.0/2.0-fast)
- [ ] Omit `--open` in batch scenarios
- [ ] For very long needs use chaining instead of forcing one clip

---

## Document revision history

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-07-18 | v1.0 | Initial topic plan | 小七 |
| 2026-07-18 | v1.1 | Noted that fast/mini do not support --draft; added the mini model row; the direction stage switched to 480p instead of draft | 小七 |
