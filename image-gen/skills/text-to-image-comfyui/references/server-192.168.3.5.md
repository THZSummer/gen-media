# 目标 ComfyUI 服务器实测档案（192.168.3.5:18000）

> 2026-10-02 联调实测，用于排查连不上 / 模型不匹配 / 出图异常。

## 服务器事实

| 项 | 值 |
|----|----|
| 地址 | `http://192.168.3.5:18000`（`--listen 0.0.0.0 --port 18000`） |
| ComfyUI | **0.38.0**（前端 1.53.10，模板 0.11.73，embedded Python 3.12.11，PyTorch 2.8.0+cu129） |
| 宿主 | Windows，WLAN = Private，RAM 64G，磁盘 `S:\Comfy-Desktop\...` |
| GPU | NVIDIA GeForce RTX 4060 Ti，显存 8 GB（free ≈ 4.5 GB） |
| 启动方式 | ComfyUI Desktop 启动器（带 `--enable-manager --extra-model-paths-config ...`） |

## 工作流所需模型（已确认在位）

| 目录 | 文件 |
|------|------|
| `diffusion_models` | `z_image_turbo_bf16.safetensors` |
| `text_encoders` | `qwen_3_4b.safetensors` |
| `vae` | `ae.safetensors` |

## 已通过的端到端验证（2026-10-02）

```
conversion: OK / mock roundtrip: OK / live probe: OK   -> RESULT: PASS
--prompt "a red fox in fresh snow, cinematic close-up, shallow depth of field, soft morning light"
--width 1024 --height 1024 --steps 8 --seed 42
-> prompt_id 05cf990f-8639-4039-852b-853248fba637, status success
-> out/z-image-turbo_00016_.png (1024x1024 PNG, 1,149,683 bytes)
同参数重跑 sha256 一致（17b60489…）-> seed 复现有效
```

## 参数矩阵实测（2026-10-02，verify_params.py：9/9 PASS）

| 参数 | 验证方式 | 结果 |
|------|----------|------|
| `--prompt` | 换词后图像 sha256 变化 | ✅ |
| `--width/--height` | PNG 头解析出 (768, 1152) | ✅ |
| `--seed` 生效 | seed 99 与 seed 11 图像不同 | ✅ |
| `--seed` 复现 | 同参数两次 sha256 完全一致 | ✅ |
| `--steps` | steps 3 与 steps 6 图像不同 | ✅ |
| `--filename-prefix` | 落盘名 `paramcheck_00001_.png` | ✅ |
| `--unet/clip/vae-name` | 三个名字进入 API 请求体 | ✅ |
| 模型名校验 | 非法 unet_name → 服务器 HTTP 400 | ✅ |

> 结论：工作流暴露的 8 个子图参数 + `filename_prefix` 全部可覆盖；未传的参数保持工作流原值。

## 连不上时的排查记录（本次真实故障）

**症状**：Windows 本机浏览器可打开 `http://192.168.3.5:18000`，但 Linux/VM 侧 `ping` 通、TCP 18000 SYN 超时。

**关键判据**：浏览器访问本机走 **loopback，绕过防火墙**，所以「本机能开」不能证明「局域网可达」。

**定位过程**：
```powershell
Get-NetTCPConnection -LocalPort 18000 -State Listen     # 已绑 0.0.0.0:18000（排除只监听回环）
Get-NetFirewallRule -Direction Inbound -Enabled True |
  Where DisplayName -like "*python*"                    # 规则存在，但 Profile = Public
Get-NetConnectionProfile                                # 实际网络是 Private -> 规则不匹配
```

**根因**：`python.exe` 的入站放通规则只绑了 **Public** 配置文件，实际 WLAN 是 **Private**，规则未生效。

**修复**（管理员 PowerShell，按端口放通、覆盖所有配置文件）：
```powershell
New-NetFirewallRule -DisplayName "ComfyUI 18000" -Direction Inbound `
  -Protocol TCP -LocalPort 18000 -Action Allow -Profile Any
```

> 备选：把已有的 `python.exe` 规则改成 `Set-NetFirewallRule -Profile Any`。

## 性能观察

- 首次出图需加载 7.5 GB 文本编码器 + 11.5 GB 主模型，等待明显长于采样本身；`--timeout` 建议 ≥900s
- 1024×1024 / 8 steps 在 4060 Ti 上可稳定跑通；显存 8 GB 余量不大，更高分辨率或批量前先看 `system_stats` 的 `vram_free`
