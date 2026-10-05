# Generation Methods Overview (Methods)

> 🌐 Language: **English** | [中文](README.md)

> Back to [home](../README.en.md) ｜ For project practice see [../projects/](../projects/README.en.md)

> This is the **technical method handbook**: organised by generation technical path (**image / video / speech** + cross-cutting controls), covering "**how to generate**".
> For concrete projects ("**what to generate**") see [projects/](../projects/README.en.md): one directory per project, referencing the methods here as needed.
> Tool entry: `arkcli +gen` (three-step workflow: ① `resources list` to find available models -> ② `models get` to check supported_params -> ③ `+gen` to generate).
> 📚 **Official tutorial (seedance-2.0 multimodal / sound effects / editing usage)**: <https://ark.volcengine.com/region:cn-beijing/docs/82379/2298881?lang=zh> (contains official examples for @video/@image/@audio reference input, sound-effect descriptions, video extension editing, etc.; consult as needed)

### seedance-2.0 multimodal reference input (measured 2026-08-01)

seedance-2.0 supports **multimodal reference input** (video/image/audio). The correct usage:

```bash
MODEL="doubao-seedance-2-0-260128"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input "reference_image:@图1.jpg" \
  --input "reference_audio:@音频1.mp3" \
  --ratio 16:9 --resolution 480p --duration 5 \
  "参考@图像1中的人物形象和场景，生成……；背景音乐使用@音频1中的声音" --wait
```

**`--input` role prefix rules** (they enter content[] in order of appearance):

| Prefix | wire role | Notes |
|------|-----------|------|
| `first:` | first frame | The 1st image of a video task is the first frame by default |
| `last:` | last frame | - |
| `ref:` | shorthand, no role is sent on the wire | The server infers it by position (reference material) |
| `reference_image:` | reference_image | ✅ reference image (explicit role) |
| `reference_video:` | reference_video | ✅ reference video |
| `reference_audio:` | reference_audio | ✅ reference audio (**audio must use this prefix**) |

**Measured pitfalls**:
- ⛔ An audio reference must use the `reference_audio:` prefix (a bare `@音频` reports "requires audio role to be reference_audio")
- ⛔ `reference_audio` cannot be the only reference (it needs an image/video reference alongside)
- ⛔ First-frame mode (I2V first frame) **cannot be mixed with reference media** ("first/last frame content cannot be mixed with reference media content") — for multimodal reference use pure T2V + reference_image/audio
- ⛔ `--generate-audio` (boolean) + a prompt describing sound effects → ❌ produces extremely quiet, useless audio (measured RMS -30~-45 dB, flat with no dynamics)
- ⚠️ **A `reference_audio` reference input actually makes the audio volume collapse** (controlled measurement: with it, RMS -45~-65 dB, essentially silent; **without** it, RMS -25~-27 dB, normally audible) — **Conclusion: for video sound effects do not pass reference_audio; let the model generate natively from the picture** (it adds ambient/action sound automatically, at a normal volume)
- ✅ **Working audio path (measured and finalised 2026-08-01)**: **use `--extra-body '{"generate_audio": true}'` to pass the request-body parameter explicitly** (⚠️ the `--generate-audio` flag was measured not to map correctly onto the request body, giving weak/uneven audio; the extra-body version gives the loudest and most even audio, per-second RMS 58-75). Guide it in the prompt by writing "audio-picture sync: ambient sound effects matching the picture (wind, rain…)".
- Reference format in the prompt: `@音频1` (the 1st audio reference), `@图像1`, `@视频1` (numbered by the order they appear in --input)



---

## 1. Why this plan exists

In day-to-day video generation, the following problems come up often:

- **Not knowing which path to start from**: plain text, one image, a reference video, following a music beat, needing a voice-over — the capability boundaries of the paths are completely different
- **Parameters passed blindly and rejected**: resolution, duration, priority, draft mode… support differs per model, and guessing without checking `supported_params` is bound to fail
- **Video is asynchronous**: submission returns `task_id` + `queued`; many people assume it "failed" and resubmit, ending up with a pile of duplicate tasks
- **A single clip is too short**: 5 seconds by default, so long content / continuous shots need a chaining strategy
- **Content blocked by moderation**: a sensitive prompt or non-compliant reference material cannot be bypassed even with `--force`, so it must be fixed at the source
- **Uncontrollable cost**: 1080p + long duration + high priority can cost several times a draft-mode generation

### Goals of this plan

Turn generation from "a one-off lucky-dip call" into **reusable planning organised by media type**:

- Each method = one class of technical path, documented on its own, to be used as needed
- Each document covers: capability mapping, prompt strategy, parameter selection, command templates, pitfalls, checklists
- Methods are orthogonal and composable (e.g. "text-to-image" + "image-to-video" + "cinematography" + "long-video chain" + "text-to-speech" strung into one complete film)
- Concrete business projects reference these methods per project in [projects/](../projects/README.en.md)

---

## 2. Capability map

Ark generation capabilities fall into three classes by **output media type**: **image, video, speech**; plus cross-cutting control parameters.

### Image class (output: still images)

| Path | Input | Typical scenario | Method |
|------|------|----------|----------|
| **Text-to-image T2I** | prompt only | Storyboard frames, I2V first frames, poster covers | [text-to-image](text-to-image/README.en.md) |

### Video class (output: motion video)

| Path | Input | Typical scenario | Method |
|------|------|----------|----------|
| **Text-to-video T2V** | prompt only | Conceiving a shot from scratch, visualising abstract concepts | [text-to-video](text-to-video/README.en.md) |
| **Image-to-video I2V** | first-frame / last-frame image + prompt | Bringing a still to life, keyframe-driven | [image-to-video](image-to-video/README.en.md) |
| **Reference video R2V** | reference video + prompt | Motion transfer, style retention, swapping the subject | [reference-video](reference-video/README.en.md) |
| **Audio-driven** | reference audio + prompt | Beat cuts, rhythmic switching, montage | [audio-driven](audio-driven/README.en.md) |

### Speech class (output: speech audio)

| Path | Input | Typical scenario | Method |
|------|------|----------|----------|
| **Text-to-speech TTS** | text | Post-production dubbing, narration, talking-head voice-over | [text-to-speech](text-to-speech/README.en.md) |

### Cross-cutting controls (apply to all types)

| Dimension | Key parameters / capabilities | Method |
|------|----------------|------|
| Shot and camera movement | `--camera-fixed`, camera-movement description in the prompt, storyboard | [cinematography](cinematography/README.en.md) |
| Quality and cost | `--resolution` `--duration` `--frames` `--draft` `--priority` | [quality-and-cost](quality-and-cost/README.en.md) |
| Long-video chain | `--return-last-frame` chaining, seed reproduction | [long-video-chain](long-video-chain/README.en.md) |
| Content safety | moderation-block subtypes, prompt adjustment, material compliance | [content-safety](content-safety/README.en.md) |

---

## 3. Method navigation

```
video-gen/methods/
├── README.md                ← you are here (method overview, grouped by media type)
│
├── 🖼️ Image class
│   └── text-to-image/       text-to-image: storyboard frames / first frames / covers (seedream)
│
├── 🎬 Video class
│   ├── text-to-video/       text-to-video: from text to a moving picture
│   ├── image-to-video/      image-to-video: driven by a first/last frame
│   ├── reference-video/     reference video: motion transfer and style retention
│   ├── audio-driven/        audio-driven: beat and rhythm sync
│   ├── cinematography/      cinematography: shot control and storyboarding
│   ├── quality-and-cost/    quality and cost: parameter trade-offs
│   ├── long-video-chain/    long video: chaining and continuous generation
│   └── content-safety/      content safety: moderation strategy and compliance
│
└── 🎙️ Speech class
    └── text-to-speech/      text-to-speech: post-production dubbing / narration (seed-tts-2.0)
```

### Method table by media type

#### 🖼️ Image class

| Method | One-line positioning | When to use |
|------|-----------|--------|
| [text-to-image](text-to-image/README.en.md) | Generates still images from prompt alone | Storyboard frames, I2V first frames, cover posters, concept validation |

#### 🎬 Video class

| Method | One-line positioning | When to use |
|------|-----------|--------|
| [text-to-video](text-to-video/README.en.md) | Generates from scratch with prompt alone | You have a clear text description but no existing material |
| [image-to-video](image-to-video/README.en.md) | Drives generation with an image as first/last frame | You already have a still, poster, or keyframe |
| [reference-video](reference-video/README.en.md) | Borrows the motion trajectory of a reference video | You want to replicate a camera move/action, or swap the subject |
| [audio-driven](audio-driven/README.en.md) | Makes the picture follow the audio's rhythm | Beat-cut videos, MVs, ad montages |
| [cinematography](cinematography/README.en.md) | Shot control and storyboard design | You need professional camera language, multiple shots |
| [quality-and-cost](quality-and-cost/README.en.md) | Trades off quality/speed/cost | Batch generation, tight budget, sample drafts |
| [long-video-chain](long-video-chain/README.en.md) | Chains several short clips into a long film | One clip is not long enough, or you need continuous narrative |
| [content-safety](content-safety/README.en.md) | Handles moderation blocks and compliance | You hit sensitive content or need stable output |

#### 🎙️ Speech class

| Method | One-line positioning | When to use |
|------|-----------|--------|
| [text-to-speech](text-to-speech/README.en.md) | Text to speech (post-production dubbing) | Narration, talking-head voice-over, multilingual dubbing |

### Combination examples

- **Product ad film**: `image-to-video` (product shot as first frame) + `cinematography` (camera movement) + `audio-driven` (beat-synced score) + `long-video-chain` (multi-shot chaining)
- **Fast sample drafts**: `quality-and-cost` (draft + 480p) to fix the direction first -> switch to 1080p for the final render once approved
- **Stylised short film**: `reference-video` (borrow the reference video's motion) + `text-to-video` (extra shots)
- **Storyboard frames first**: `text-to-image` (seedream produces each shot's keyframe) → review → `image-to-video` (storyboard frame as first frame, brought to life) — the lowest rework cost
- **Dubbing the final film**: `text-to-speech` (TTS generates narration) → ffmpeg `-c:a copy` to mux it into the video

> These combinations become concrete projects in [projects/](../projects/README.en.md).

---

## 4. The universal three-step workflow

> Every method follows this workflow; only the Step 3 parameters and the `--input` combination differ.

```bash
# Step 1: list the video models available to the current profile (platform=EP, agent-plan=model name)
arkcli resources list --modality video

# Step 2: check the parameters supported by the chosen model $MODEL (if sp is empty, fall back to the modality default)
arkcli models get "$MODEL" --transform supported_params

# Step 3: generate with the available parameters (video is asynchronous by default, returns task_id)
arkcli +gen --model "$MODEL" "<prompt>" --open
# to block synchronously for the result: add --wait
```

### Handling video results (asynchronous semantics, key point)

```
+gen submit -> returns task_id + status=queued   ← not a failure!
   │
   ▼ poll with arkcli gen get <task_id> --open
   │
   └─► status=succeeded -> auto-download locally + pop the finished file on the desktop (see local_path)
```

- **Do not** resubmit `+gen` just because the video is not ready immediately (it creates a new task)
- The presigned `output_url` **expires after 24 hours**; long-term storage relies on `local_path` or downloading in time
- To block synchronously: `arkcli +gen ... --wait --open`
- ⚠️ `--save-to` may not take effect when `gen get` polls and downloads, so the artifact lands in the CWD of `gen get`; after polling, `mv` it to the target directory manually

---

## 5. Model notes

Seedance is Doubao's video generation series; the common forms (defer to the current profile output of `resources list`):

| Model family | Positioning | Notes |
|--------|------|------|
| `doubao-seedance-1-5-pro` | 1.5 Pro, quality first | Does not support `--priority`, ⚠️ about to be retired |
| `doubao-seedance-2-0` | 2.0 mainline (✅ activated) | Supports `--priority`/`--draft`/`--generate-audio`/`--return-last-frame`; inputs support text/image/video/audio |
| `doubao-seedance-2-0-fast` | 2.0 fast version | Speed/cost trade-off |
| `doubao-seedance-2-0-r2v` | 2.0 reference-video specialist | First choice for the R2V path |
| `doubao-seedance-2-0-mini` | 2.0 mini lightweight version | ⛔ Does not support --draft or --return-last-frame; output is video only, no audio |

> ⚠️ `--model` must be the **full versioned ID** (e.g. `doubao-seedance-2-0-260128`); passing only the family name returns 404. The version number is not fixed (a 6/8-digit date or a short number); complete it with `arkcli models get <族名> --transform 'primary_version'`, and **do not guess with your own regex**.

> 🔀 **Profile routing rules**: `doubao-seedance-2-0-mini` (the 2.0 series) goes through **platform pay-as-you-go** (`--profile platform_cn-beijing_accountwide`; `gen get` must carry the same profile too, otherwise task not found); all other models go through **agent-plan** (the default profile).

> 📦 **Models included in the Agent Plan Medium plan** (source: Agent Plan configuration guide):
> - **Vision models** (⛔ Auto and console switching are not supported; the model must be specified explicitly in the configuration/command):
>   - `doubao-seedance-1-5-pro` (video, ⚠️ about to be retired, new activations are currently not supported)
>   - `doubao-seedream-5.0-lite` (image generation)
>   - ⛔ The Medium plan **does not support the Seedance 2.0 series** (2.0/2.0-fast/2.0-mini/2.0-r2v) -> these go through platform pay-as-you-go
> - **Speech models** (⛔ likewise no Auto and no console switching):
>   - Doubao speech synthesis 2.0 (`doubao-seed-tts-2.0`), Resource-Id = `seed-tts-2.0`
>   - Doubao streaming speech recognition 2.0 (`doubao-seed-asr-2.0`), Resource-Id = `volc.seedasr.sauc.duration`

> 🎯 **Actually available right now**:
> - platform pay-as-you-go: ✅ `doubao-seedance-2-0-260128` (video, activated 2026-08-01, supports generate-audio/priority/draft) + `doubao-seedream-5-0-pro-260628` (images, precise image editing) + `doubao-seedance-2-0-mini-260615` (video, lightweight)
> - agent-plan: ✅ `doubao-seedream-5-0-lite` (images, measured working), `doubao-seedance-1-5-pro`, TTS / ASR (specify by the model names/Resource-Ids above; do not use Auto)
> 🔇 **Audio output capability** (verified through the `modalities.output` / `task_types` of `arkcli models get`): not every Seedance model outputs audio.
>   - `doubao-seedance-1-5-pro`: ✅ supports synchronized audio (task_types include `TextToAudioVideo`/`ImageToAudioVideo`, covering ambient sound/action sound/voice/background audio)
>   - `doubao-seedance-2-0` (260128): ✅ **measured to support `--generate-audio`** (verified 2026-08-01; the output includes ambient/action sound, max -10.9 dB, not silent)
>   - `doubao-seedance-2-0-fast` / `2-0-mini`: ❌ output is video only, no audio (`--generate-audio` has no effect)
>   - By default the video contains a -35 dB silent placeholder track, not real audio; for sound either generate with 2.0/1.5-pro or mux it later with ffmpeg

### How to call TTS speech synthesis (post-production dubbing)

> ⚠️ **arkcli does not cover TTS/ASR**. TTS goes through the OpenSpeech service (independent of Ark Runtime), so you have to write your own script to call the HTTP streaming interface. `+chat`/`+gen`/`+code-example` all do not support speech models.
> 📄 **The complete method has its own document: [text-to-speech](text-to-speech/README.en.md)** (endpoint/request body/stream decoding/speaker/ffmpeg muxing).

| Item | Value |
|----|----|
| Endpoint | `https://openspeech.bytedance.com/api/v3/plan/tts/unidirectional` (the `/plan/` path = the Agent Plan channel)|
| Authentication | Header `X-Api-Key: <ark-api-key>` + `X-Api-Resource-Id: seed-tts-2.0` |
| Profile | agent-plan (TTS is included in the Medium plan and uses the ARK API Key) |
| Request body | `{"req_params":{"text":"...","speaker":"zh_female_vv_uranus_bigtts","audio_params":{"format":"mp3","sample_rate":24000}}}` |
| Response | Streaming JSON Lines, each line `{"code":0,"data":"<base64 音频块>"}`, `code=20000000` marks the end |
| Decoding | `base64.b64decode(data)` line by line, concatenated into a complete mp3 |
| speaker | `zh_female_vv_uranus_bigtts` (a steady female voice, good for narration); for other voices see the speech synthesis voice list in the console |

See `projects/survival-island/scripts/tts_narration.py` for a call example (streaming receive + base64 concatenation + writing to disk).

> ⚠️ When muxing into video **do not re-encode with `-c:a aac`**; putting the mp3 straight into the mp4 (`-c:a copy`) is enough, because in practice players may not recognise the audio track after an aac re-encode.

> Getting the API Key: `arkcli auth status` shows the mask; the full value is in `~/.arkcli/identities/<volc-id>/apikey.json`.

---

## 6. Glossary

| Term | Meaning |
|------|------|
| T2V / I2V / R2V | Text-to-video / image-to-video / reference video generation |
| First frame / last frame | In I2V, the images that drive the start/end point of the video |
| `queued` | The video task is queued (asynchronous, not a failure) |
| `supported_params` | The list of parameters the model actually supports; always check it in Step 2 |
| Draft mode `--draft` | A sample mode that is faster and cheaper but lower quality |
| Chaining | Using the last frame of one clip as the first frame of the next, stringing them into a long film |

---

## Document revision history

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-07-18 | v1.0 | Initial plan; created the 8 topic subdirectories and the main navigation | 小七 |
| 2026-07-18 | v1.1 | Restructured the top level around "projects": this document moved into methods/ as the method overview, and the top level is now organised by project (projects/) | 小七 |
| 2026-07-18 | v1.2 | Added the doubao-seedance-2-0-mini model; noted that Agent Plan does not include video and platform pay-as-you-go is required; added real-world pitfalls for --draft/--save-to/--return-last-frame | 小七 |
| 2026-07-18 | v1.3 | Added the audio output capability comparison: only 1.5-pro supports synchronized audio; the 2.0 series (including mini) outputs video only | 小七 |
| 2026-07-18 | v1.4 | Recorded the complete Agent Plan Medium model list (vision seedream-5.0-lite/seedance-1.5-pro + speech TTS/ASR with Resource-Ids) + the profile routing rules; corrected "does not include video" to "does not include the 2.0 series" | 小七 |
| 2026-07-18 | v1.5 | Added the TTS speech synthesis call method (OpenSpeech endpoint + request body + stream decoding); arkcli does not cover it, so you must write your own script | 小七 |
| 2026-08-01 | v1.6 | Added the text-to-image method (seedream-5.0-lite); corrected "the whole seedream line is not activated" to activated and measured working; added the T2I row to the capability map/navigation/combination usage | 小七 |
| 2026-08-01 | v1.7 | Reorganised the directory structure by media type: three classes — image/video/speech — plus cross-cutting controls; TTS gets its own document text-to-speech/; the navigation tree and method table are shown grouped | 小七 |
| 2026-08-01 | v1.8 | Added seedream-5.0-pro (platform pay-as-you-go, precise image editing); added pro + mini to the available-model list | 小七 |
| 2026-08-01 | v1.9 | Measured activation of seedance-2.0-260128 (platform pay-as-you-go): supports --generate-audio (real audio)/--priority/--draft/--return-last-frame; corrected the outdated "2.0 has no audio" record | 小七 |
| 2026-08-01 | v2.0 | Added the complete usage of seedance-2.0 multimodal reference input: the reference_image/reference_audio role prefix rules, the @ reference format, measured pitfalls (--generate-audio ineffective, first frames cannot be mixed with reference media, audio needs the reference_audio prefix); recorded the official tutorial URL | 小七 |
| 2026-08-01 | v2.2 | Re-verified audio: passing reference_audio makes the volume collapse (RMS -45~-65 dB, near-silent), while without it the model's native sound effects are normal (RMS -25~-27 dB) — the audio approach was corrected to "do not pass an audio reference; let the model generate natively" | 小七 |
| 2026-08-01 | v2.3 | Final audio version: only passing the request-body parameter explicitly with `--extra-body '{"generate_audio": true}'` takes effect (the --generate-audio flag does not map correctly); the volume of the 3 approaches was measured side by side | 小七 |
