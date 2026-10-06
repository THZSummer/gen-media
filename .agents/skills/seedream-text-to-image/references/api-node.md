# ByteDance Seedream 付费节点（远端模型）实测档案

> 返回 [SKILL.md](../SKILL.md) ｜ 服务器通识见 [../../text-to-image-comfyui/references/server-192.168.3.5.md](../../text-to-image-comfyui/references/server-192.168.3.5.md)

**一句话**：这个技能跑的节点 `ByteDanceSeedreamNodeV3` 属于 ComfyUI 的 **partner / API 节点**——
图在本机 ComfyUI 里编排，**推理在 ByteDance 云端**，按张计费。所以本机既没有权重文件，
也不需要下模型；但**必须给 ComfyUI 账号凭据**，否则执行阶段一律 `Unauthorized`。

---

## 一、服务器与节点事实（2026-10-06 实测）

| 项 | 值 |
|----|----|
| 地址 | `http://192.168.3.5:18000`（局域网可达，`/system_stats` HTTP 200） |
| ComfyUI | **0.38.0**（前端 1.53.10，host 为 Windows 桌面版 `local-desktop2-standalone`） |
| 节点 | `ByteDanceSeedreamNodeV3`（category `partner/image/ByteDance`，`api_node: true`）、`SaveImageAdvanced` |
| 模型键 | `seedream 5.0 pro` / `seedream 5.0 flash` / `seedream 5.0 lite` / `seedream-4-5-251128` / `seedream-4-0-250828` |
| 本机权重 | **没有**。`--check` 的 `model_files_needed` 恒为空，这是对的：权重在云端 |
| schema 快照 | [node-info.json](node-info.json)（`/object_info` 的子集，含取快照时的 `object_info_sha256`） |

> ⚠️ traceback 里出现的安装目录名是 `ComfyUI (v0.30.1 + 5 commits (c44dea1))`，而
> `/system_stats` 报 `comfyui_version: 0.38.0`。**以 `/system_stats` 为准**，目录名只是安装时的标签。

---

## 二、鉴权：桌面端点 Run 能出图 ≠ 脚本能出图

这是本技能最容易踩的坑，实测三次复现：

| 场景 | 结果 |
|------|------|
| 桌面版界面里点 Run（邮箱/浏览器登录态） | ✅ 出图（用户实测） |
| 无头 `POST /prompt`（本技能，无凭据） | ❌ `Unauthorized: Please login first to use this node.` |
| 无头 `POST /prompt` + `extra_data.api_key_comfy_org` | 官方支持的通道（见下） |

**报错原文**（`/history/<pid>` 的 `status.messages[].execution_error`）：

```
exception_message: "Unauthorized: Please login first to use this node.\n"
node_id: "3", node_type: "ByteDanceSeedreamNodeV3"
traceback 末帧: comfy_api_nodes/util/client.py:1091, in _request_base -> raise Exception(msg)
```

**为什么**：桌面端的登录态是**前端（浏览器）会话**，只在界面发请求时随请求带走；服务端自己**没有**
存凭据——实测 `GET /api/userdata/comfy.settings.json`（27 个设置项）里没有任何 `*Key` / `*Token` 项。

> ⚠️ 别用 `/api/features` 的 `show_signin_button: true` 判断登录状态：那是 Desktop 启动时通过
> `--feature-flag show_signin_button=true` 注入的（见 `/system_stats` 的 `argv`），跟登没登录无关。

**官方给无头用的通道**（[ComfyUI 文档](https://docs.comfy.org/development/comfyui-server/api-key-integration)、
[发布说明](https://blog.comfy.org/p/api-nodes-login-via-comfyui-api-key)）：把凭据放进 `POST /prompt`
的 `extra_data`：

```json
{"prompt": {...API 图...},
 "client_id": "dsh-seedream-12345",
 "extra_data": {"api_key_comfy_org": "comfyui-************"}}
```

服务端到底认哪些键、认到什么程度，直接看 ComfyUI 源码最清楚
（`comfy_api_nodes/util/_helpers.py`，2026-10-06 取 master 版）：

```python
if node_cls.hidden.auth_token_comfy_org:
    return {"Authorization": f"Bearer {node_cls.hidden.auth_token_comfy_org}"}
if node_cls.hidden.api_key_comfy_org:
    return {"X-API-KEY": node_cls.hidden.api_key_comfy_org}
```

对应两个通道 —— **本技能两个都支持**：

| 通道 | `extra_data` 键 | 从哪来 | 何时用 |
|------|----------------|--------|--------|
| **API Key**（推荐） | `api_key_comfy_org` | [platform.comfy.org](https://platform.comfy.org) → API Keys → `+ New`（只在创建时显示一次） | 脚本化/无头；不会过期 |
| Bearer token | `auth_token_comfy_org` | 桌面端/浏览器 OAuth 登录态（前端每次请求现取） | 只有在拿得到 token 时；**会过期** |

技能里的给法：`--api-key` > `--api-key-file` > `$COMFYUI_API_KEY` / `$COMFY_API_KEY`
> `--auth-token` > `$COMFYUI_AUTH_TOKEN`（前两个命中就不再找后面的）。
账号里要有 credits（[余额/充值](https://docs.comfy.org/interface/credits)）。
也可以把同一个 API Key 填进 ComfyUI 的 Settings → User（走 API Key 登录而不是邮箱登录），
让服务端替所有无头请求带上 —— 注意**邮箱/浏览器登录不写服务端**，所以那种"配置过"对脚本无效。

> 🔍 **为什么报错文案都一样**：ComfyUI 把上游 401 统一成一句
> `Unauthorized: Please login first to use this node.`
> （`comfy_api_nodes/util/client.py` 里 `if status == 401: return "Unauthorized: ..."`）。
> 所以"没带凭据"和"凭据无效"在日志里长得一模一样 —— 别靠报错区分，用 `--check` 看
> `credential.present / credential.channel`。

**纪律**：凭据只进请求体，**不进留档**。`requests.jsonl` 只记 `credential_channel` 与
`credential_source`；`test_skill.py` 里有一条断言专门守这件事（留档里出现凭据明文即失败）。

---

## 三、API 图的形状：**带点的输入名**

UI 版工作流的 `widgets_values_named` 就是 API 格式的输入名，**照抄即可**：

| 节点 | API 输入 |
|------|----------|
| `ByteDanceSeedreamNodeV3` | `prompt`、`model` |
| ↳ 动态下拉框 `model` 的子输入 | `model.size_preset`、`model.width`、`model.height`、`model.seed`、`model.watermark`、`model.thinking`、`model.prompt_optimization`、`model.max_images`、`model.fail_on_partial`、`model.images.image_N` |
| `SaveImageAdvanced` | `images`、`filename_prefix`、`format` |
| ↳ 动态下拉框 `format` 的子输入 | `format.bit_depth`、`format.input_color_space`（换 `exr`/`avif` 后子输入集合会变） |

证据：把 `model.height` 写成 `height`，服务器直接拒：

```
HTTP 400 {"error": {"type": "prompt_outputs_failed_validation", ...},
          "node_errors": {"3": {"errors": [{"type": "required_input_missing",
              "details": "height", "extra_info": {"input_name": "model.height"}}]}}}
```

改成带点名字后：`HTTP 200 {"prompt_id": "43779f26-...", "number": 515, "node_errors": {}}` ——
**图本身合法**，卡在后一步的鉴权。

其余两条形状规则：

* `control_after_generate`、`control_after_generate#1` 是前端伪 widget，进 API 图会被当成未知输入；
* `model.images`（`COMFY_AUTOGROW_V3`）在 schema 里挂在 `required` 下，但**不给也能过校验**
  （上述 200 那张图就没有它）。它是采集式可选输入，纯文生图不需要；
  要**给**参考图（编辑）时按序号带点接 `model.images.image_1` / `image_2` …
  —— 那是 [seedream-image-edit](../../seedream-image-edit/SKILL.md) 的技能，本页不展开。

**前端专有节点要剔掉**：桌面导出的图里可能带 `MarkdownNote` 之类的界面节点，服务器上没有对应的类，
原样提交会被判 `missing_node_type`（HTTP 400）。转换后统一过一遍
`seedream_api.prune_ui_only(api[, known_classes])`：默认按静态名单剔，给了真机 `/object_info`
的类名集合就按"服务器上没有的一律剔"，并清掉指向被删节点的输入。实测见
[seedream-image-edit/references/api-node.md §2](../../seedream-image-edit/references/api-node.md)。

---

## 四、参数面：每个模型支持的东西不一样

| 模型键 | `thinking` | `prompt_optimization` | `max_images` + `fail_on_partial` | 尺寸档 |
|--------|-----------|----------------------|----------------------------------|--------|
| `seedream 5.0 pro` | ✅ | ✅ | ❌ | 1K / 2K / Custom |
| `seedream 5.0 flash` | ❌ | ❌ | ❌ | 1K / 1.5K / 2K / Custom |
| `seedream 5.0 lite` | ✅ | ❌ | ✅ | 2K / 3K / 4K / Custom |
| `seedream-4-5-251128` | ✅ | ❌ | ✅ | 2K / 4K / Custom |
| `seedream-4-0-250828` | ✅ | ❌ | ✅ | 1K / 2K / 4K / Custom |

（`seed` / `watermark` / `size_preset` / `width` / `height` 五个所有模型都有；完整预设清单用
`python3 scripts/seedream_gen.py --list` 看。）

**纪律**：`thinking` 给了 flash、`max_images` 给了 pro —— 这类请求会被本地 schema 直接拒
（`UnappliedOverrideError`，exit 8），不会跑到云端再白花一张图的钱。

`size_preset` 的三条约束（都写进了 `parse_size`）：

1. `--size 1024x1024` 命中预设就用预设；命中不了走 `Custom` + `width/height`；
2. `Custom` 必须配 `--width/--height`（Node 3 的 `model.width/height` 只在 preset 为 `Custom` 时生效）；
3. 宽高受该模型的 `min/max` 约束（pro：1024–4514；lite：宽 1024–6240 / 高 1024–4992），越界直接拒。

---

## 五、验证记录（2026-10-06 真机跑通）

| 项 | 结果 |
|----|------|
| 服务器 / 节点 / 模型列表 / schema 对账 | `--check`：`reachable: true`、ComfyUI 0.38.0、5 个模型、`schema_drift: none`、`credential.present: true` |
| **首次真机出图** | `九尾狐 素描 线稿` / pro 1K(`(1K) 1024x1024 (1:1)`) / seed 1766827367 / thinking 开 → `status: success`，**端到端 63 秒**，1024×1024 PNG 1,266,220 字节 |
| 出图内容复核 | 人眼看过：正常的九尾狐素描线稿，中文「九尾狐」与印章都渲染正确 —— 不是错误占位图 |
| **参数矩阵 6 步**（`verify_params.py --yes`） | 6/6 通过，合计 **3 分 41 秒** |

参数矩阵逐项（宽高读 PNG 头，差异比解码后的像素）：

| 步 | 断言 | 实测 |
|----|------|------|
| baseline | 1K 预设 → 1024×1024 | ✅ 1024×1024 |
| seed | 换 seed 像素必须变（证明 seed 真的到了模型） | ✅ digest `4fa443bc…` → `677bcf4f…` |
| size | `--size 1440x2560` 走 Custom → 1440×2560 | ✅ 1440×2560 |
| thinking | `--no-thinking` 能出图 | ✅ 1024×1024（digest 与 baseline 不同 → thinking 确实影响结果） |
| model | 换 `seedream 5.0 flash` 能出图 | ✅ 1024×1024 |

> ⚠️ **"同 seed 重跑逐像素一致"这次算不得数**：repeat 那轮图与 baseline 完全一致，但
> `/history` 里写着 `execution_cached: ["2","3"]` —— Seedream 节点**根本没再调云端**，ComfyUI
> 直接复用了上一次的节点结果。所以它证明的是**缓存语义**，不是远端模型的复现性。
> 要真测远端复现性，得让服务器带 `--cache-none` 重启（缓存按"节点输入"命中，改文件名之类的
> 小动作不会让节点 3 失效）。引擎会把这件事解析出来：`generate()` 返回 `cached_nodes`。

**仍未验证**（要花真钱，按需再说）：`--watermark`、`--prompt-optimization fast`、
lite/4.5/4.0 的 `--max-images`、2K/4K 预设档、以及上面那条"远端模型本身是否可复现"。

补验命令（每条都是一次计费）：

```bash
python3 scripts/verify_params.py --api-key-file <key文件> --yes
python3 scripts/seedream_gen.py --prompt "..." --watermark --out-dir .verify/seedream/
```

> 没有凭据时 `verify_params.py` 以 `SKIPPED_NO_CREDENTIAL` 退出（exit 2）——**不会假装通过**。

---

## 六、成本与并发注意

* 云端按张计费（ComfyUI 账号 credits），**每次重试都是一次计费**：本地 schema 校验先把
  明显不合法的请求挡住，就是为了不在云端白花钱。
* 换 `--seed` 会真的产生新图（本技能不做本地缓存复用）。
* 这个节点与本机的 Z-Image / Qwen / FastH3 权重**互不干扰**：不占显存、不抢模型，
  瓶颈在网络与云端排队。
* 想完全绕开 Comfy 账号额度、直接用火山方舟按量计费出 Seedream 图，见
  [methods/text-to-image](../../../methods/text-to-image/README.md)（`arkcli +gen` 路线，
  与本技能是两条不同的账）。
