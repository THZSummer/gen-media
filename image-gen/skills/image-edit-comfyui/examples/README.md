# 示例（image-edit-comfyui）

## 结构保留的画风迁移

控制图：`../../projects/bone-china-doll/out/r11/bc-r11-portrait-velvet_00001_.png`（骨瓷公主定稿）
输出：`example-oil-painting.png`（768×1024）

```bash
python3 scripts/comfyui_edit.py \
  --image ../../projects/bone-china-doll/out/r11/bc-r11-portrait-velvet_00001_.png \
  --prompt "oil painting of a porcelain princess in a deep blue velvet gown, thick impasto brushstrokes, warm varnish, oil on canvas" \
  --width 768 --height 1024 --steps 8 --seed 7 \
  --filename-prefix realtest --out-dir out/
```

保留：姿势、构图、冠冕、珍珠项链、丝绒礼服结构；改变：材质与画风（写实瓷 → 厚涂油画）。
本次运行的完整执行图实际留在 `.verify/real/realtest.api.json`（`.verify/` 是本地验证产物，
已列在 `.gitignore` 中，不入库）；按上面的命令重跑即可在 `--out-dir` 得到新的
`<prefix>.api.json` 与 `requests.jsonl`。
