# Camera Movement and Storyboard (Cinematography)

> 🌐 Language: **English** | [中文](README.md)

> A cross-cutting topic covering camera movement, composition, and storyboard design; applies to every input path (T2V/I2V/R2V/audio-driven).
> Back to [method overview](../README.en.md)

---

## 1. Topic positioning

Camera language is the key to turning "a picture that moves" into "a video with narrative". This topic does not restrict the input path; it focuses on **how to make the camera move the way you intend**, and on how to organise multi-shot narrative with a storyboard.

### Applicable scenarios

- You need professional camera moves (push/pull/pan/track/follow/orbit)
- Multi-shot narrative (wide shot -> medium shot -> close-up)
- Avoiding "the model inventing random camera moves"
- Designing a storyboard for [long-video-chain](../long-video-chain/README.en.md)

---

## 2. Camera-movement vocabulary

Use these words in the prompt to describe camera movement; the model recognises them well:

| Move | Descriptive words | Effect |
|------|--------|------|
| Push in | camera moves closer / dolly in / push in | Moves towards the subject, emphasises it |
| Pull out | camera moves away / dolly out / pull back | Moves away from the subject, establishes the environment |
| Pan | camera pans left/right / pan | Rotates horizontally, sweeps |
| Track | camera tracks / tracking | Moves along with the subject |
| Follow | follow shot / follow | Follows the subject's motion |
| Orbit | camera orbits / orbit | Circles around the subject |
| Crane | camera rises/descends / crane | Vertical camera move |
| Static | static shot / static | The camera stays still, the subject moves |
| Aerial | aerial shot / aerial | A wide view from above |
| Timelapse | timelapse photography / timelapse | Compressed time |

### Composition and shot-size words

- Shot size: extreme wide / full shot / medium shot / medium close-up / close-up / extreme close-up
- Angle: eye level / low angle / high angle / bird's-eye
- Depth of field: shallow depth of field / deep depth of field
- Focal length: wide angle / telephoto / macro

---

## 3. Two control paths

### Path A: describe the camera move in the prompt (default)

State the camera movement in the prompt and the model generates accordingly. **Most commonly used.**

```
"镜头缓慢拉远，主体居中保持不动，背景云层流动"
"镜头环绕产品旋转一圈，影棚光"
"航拍视角，从高空俯冲向城市"
```

Key points:
- Describe only **one main camera move** at a time; mixing several conflicts
- Camera move + a speed modifier (slow/fast/steady) is more controllable
- Pair it with shot-size/angle words to strengthen the expression

### Path B: `--camera-fixed` fixed camera

When you want a **static composition where the subject moves and the camera does not**, use `--camera-fixed` to lock the virtual camera and stop the model from inventing camera moves.

```bash
arkcli +gen --model "$MODEL" --camera-fixed \
  "主体在画面中央活动，背景固定" --open
```

Applies to:
- Product showcases (product moves, camera does not)
- Recording from a fixed position
- Avoiding accidental camera moves ruining the composition

> Counter-example: adding `--camera-fixed` when you want a camera move -> the camera is locked and the move fails. The two are mutually exclusive; pick one as needed.

---

## 4. Storyboard design (multi-shot narrative)

A single clip's duration is limited (5 s by default), so narrative relies on **concatenating several storyboard shots**. Designing the storyboard is the upfront planning for [long-video-chain](../long-video-chain/README.en.md).

### Storyboard table template

| Shot # | Shot size | Camera move | Content | Duration | Transition |
|------|------|------|------|------|------|
| 1 | Extreme wide | Aerial push in | The whole city | 5s | Cut |
| 2 | Medium | Follow shot | The protagonist walks into the street | 5s | Chain (last frame -> first frame) |
| 3 | Close-up | Static | The protagonist's expression | 5s | Cut |

### Transition methods

| Method | Notes | Implementation |
|------|------|------|
| Hard cut | Direct concatenation, fast pace | Edited in post, or generated independently |
| Chaining | The previous clip's last frame becomes the next clip's first frame, continuous | `--return-last-frame` chaining |
| Action continuity | The previous clip's action continues into the next | Describe the continuous action in the prompt |

### The single-shot principle

Each video should tell **only one camera move + one subject action**; do not cram in too much. Split complex narrative into several storyboard shots and chain them in [long-video-chain](../long-video-chain/README.en.md).

---

## 5. Parameter selection

| Parameter | Recommendation for camera-move scenarios | Notes |
|------|-------------|------|
| `--camera-fixed` | Use for static compositions | Locks the camera |
| `--ratio` | Landscape narrative `16:9`, portrait `9:16` | |
| `--duration` | From 5s per shot | Complex camera moves can be lengthened a little |
| `--return-last-frame` | For chaining | Takes the last frame for the next clip |
| `--seed` | Storyboard consistency | Fix the seed across several shots of one scene to keep the look consistent |

---

## 6. Command templates

```bash
VER=$(arkcli models get doubao-seedance-2-0 --transform 'primary_version' | tr -d '"')
MODEL="doubao-seedance-2-0-${VER:-260128}"

# A) prompt 运镜：环绕
arkcli +gen --model "$MODEL" --ratio 16:9 \
  "镜头环绕一双运动鞋缓慢旋转一圈，影棚光，纯黑背景，浅景深" --open

# B) 固定镜头：主体动镜头不动
arkcli +gen --model "$MODEL" --camera-fixed \
  "咖啡杯在画面中央，热气升起，背景虚化固定" --open

# C) 航拍推近
arkcli +gen --model "$MODEL" \
  "航拍视角，从高空俯冲向雪山村庄，云层从镜头旁掠过" --open

# D) 续接分镜：拿末帧作下一条首帧
arkcli +gen --model "$MODEL" --return-last-frame \
  --input @shot1.jpg "镜头向右摇，展现街道" --open
```

---

## 7. Pitfalls

| Symptom | Cause | Fix |
|------|------|------|
| Erratic/jumpy camera | Several camera moves mixed in the prompt | Write only one main camera move at a time |
| No movement when a move was wanted | `--camera-fixed` added by mistake | Remove the flag in camera-move scenarios |
| Dizzying camera | The move is too fast/excessive | Add "slow/steady"; one camera move per shot |
| Inconsistent look across shots | Random seed | Fix `--seed` for the same scene |
| Chaining jump | The last frame does not match the next clip's first frame | Use the real last frame from `--return-last-frame`, do not pick another image |

---

## 8. Checklist

- [ ] The prompt describes only one main camera move + a speed modifier
- [ ] Use `--camera-fixed` only for static compositions, not in camera-move scenarios
- [ ] For multi-shot narrative, list the storyboard table first
- [ ] Fix `--seed` across several shots of one scene to keep the look consistent
- [ ] Use `--return-last-frame` to get the real last frame for chaining
- [ ] One shot, one camera move, one subject action

---

## Document revision history

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-07-18 | v1.0 | Initial topic plan | 小七 |
