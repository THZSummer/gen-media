# 画廊站点（site）

> 返回 [SKILL.md](../SKILL.md)

## 1. 两条硬性约定

1. **站点必须双语**：`site/app.js` 里的 `T.zh` / `T.en` 两套界面文案 + 数据里的 `title.{zh,en}`；
   右上角按钮切换，选择存 `localStorage['gm-lang']`，默认 `zh`。**新增任何界面文案都要同时写两份。**
2. **从仓库根发布，资产零复制**：GitHub Pages 源 = `main` + `/`，根目录放 `.nojekyll`。
   `index.html` 与 `site/` 只是薄薄一层，图片/视频按仓库内相对路径就地服务 —— 站点体积 = 仓库体积
   （当前约 550 MB < Pages 的 1 GB 上限）。
   若改成 Actions artifact 部署，每次都要上传 550 MB，**不要这么干**。

## 2. 路径可移植性（踩过的坑）

- 生成的 JSON 里存**仓库相对路径**（`projects/...`），**不要**存站点绝对路径（`/projects/...`）：
  线上站点在 `/gen-media/` 子路径下，绝对路径会 404。
- 前端用 `const BASE = location.pathname.replace(/[^/]*$/, '')` 推导前缀，再拼资源 URL。

## 3. 数据层

- `tools/build_site.py` **只读源素材**（不碰成品、不改 manifest）、**幂等**（同输入产出逐字节相同的 JSON）。
- 数据源：`projects/*/subjects/*/period-*/manifest.json`、`rounds/*-review.md` 的评分表、目录扫描。
- **项目卡片是扫描出来的**，不是硬编码清单：`projects/` 下 `_` 开头跳过、`bio-splice` 单独成卡、
  含 `.mp4` 的归视频汇总卡、其余各成一卡。新增项目放进 `projects/` 就自动进画廊
  （标题/说明/封面可用 `PROJECTS` / `DOCS` / `COVERS` 覆写）。**别再退回硬编码**——实测漏掉过整个项目。
- 轮次文件名要用**宽容正则**：实测有 `r01-review.md`、`ts-r3-review.md`、`fb2-r1-review.md`、`dn-r10-review.md`：
  `^(?:[A-Za-z0-9]+-)?r(\d+)-(review|audit)\.(jpg|md)$`
- **评分维度随项目走**（`RUBRICS`，写进 JSON 由前端读），不要写进 `app.js`——
  bio-splice 是 A–E 五维、shanhai-jing 是 A–F 六维，写死会让第二个项目的期详情页说错。
- 新增内容后重跑生成器；首页/项目页统计数字应随之变化。

### 缩略图（网格与封面**不得直出原图**）

`build_site.py` 会在生成数据的同时产出 `site/thumbs/`（最长边 480px、JPEG）：

| 字段 | 用途 | 谁加载 |
|------|------|--------|
| `thumb` | 网格 / 封面显示的缩略图 | 首屏与滚动时 |
| `path` / `sheet` / `poster` | **原图**，灯箱与播放用 | 点击后才加载 |

- 收益实测：bio-splice 单页 **306 MB → 9.5 MB**；首页封面 **5.34 MB → 0.13 MB**。
- **增量**：缩略图存在且不比源新就跳过 → 重跑几乎零成本。
- **优雅退化**：没有 `ffmpeg` 时返回原图（页面变重但不报错）；`--no-thumbs` 显式跳过。
- ⛔ **两个必须守住的约束**（都实际踩过，见 `thumb_of()` 的注释与断言）：
  1. `src` 可能是**绝对路径**——直接 `os.path.join(THUMB_DIR, src)` 会丢掉前缀、写进源目录；
     所以一律先 `os.path.relpath(src, ROOT)` 归一。
  2. 源本身是 `.jpg` 时，上面那个 bug 会让输出路径**正好等于源路径**，`ffmpeg -y` 直接覆盖原图。
     所以 `thumb_of()` 里有两道 `RuntimeError` 断言：输出必须在 `THUMB_DIR` 内、且不等于源。
- 前端一律写 `e.thumb || e.path`（缺字段时自然退回原图，不会白屏）。

## 4. 前端

- 纯 vanilla：**无框架、无 CDN、无构建**；只加 `site/app.{css,js}` 与 `site/data/*.json`。
- 图片 `loading="lazy" decoding="async"`；视频 `preload="none"` + 分镜图 `poster`（不点不下载）。
- **导航从 `index.json` 派生**（有内页的 kind 自动进导航），不要把某个项目写死成顶级项。
- 点击放大用原生 `<dialog>` 灯箱，左右方向键切换；灯箱始终用 `path`（原图）。

## 5. 本地预览

```sh
tools/preview.sh              # → http://127.0.0.1:8090/
tools/preview.sh 8123 lan     # 局域网 / 手机
tools/preview.sh stop 8090    # 停止
```

- 必须走 `http://`：双击 `index.html` 会因跨源策略读不到 `site/data/*.json`（页面会给出提示）。
- 端口被自己的预览占用会友好提示；被别的程序占用会自动换端口。

## 6. 发布与线上验证

- 推完 `main` 等 Pages 构建（约 1 分钟）；`gh api repos/<owner>/<repo>/pages/builds/latest --jq .status` 看状态。
- 本机对 `github.io` 有线路抖动时，用可用边缘 IP 直连验证：

```sh
for ip in 185.199.108.153 185.199.109.153 185.199.110.153 185.199.111.153; do
  curl -s -o /dev/null -w "$ip %{http_code}\n" --max-time 8 \
    --resolve thzsummer.github.io:443:$ip https://thzsummer.github.io/gen-media/
done
```

实测 `.110` / `.111` 通常可用，`.108` / `.109` 可能超时；DNS 轮到坏 IP 时浏览器会卡住，多刷几次或用 `--resolve` 验证。
