# 画廊站点（site）

> 返回 [SKILL.md](../SKILL.md)

站点是**流媒体式**的两层结构：**列表页**（billboard 巨幅头图 + 横向行）→ **详情页**
（全屏 feed，一屏一帧 = 一张图 + 一段文字，**上下滑动换图**）。

## 1. 两条硬性约定

1. **站点必须双语**：`site/app.js` 里的 `T.zh` / `T.en` 两套界面文案 + 数据里的 `title.{zh,en}`；
   右上角按钮切换，选择存 `localStorage['gm-lang']`，默认 `zh`。
   **新增任何界面文案都要同时写两份**，并跑 `python3 tools/i18n.py ui`——它机械检查
   两表键一致、英文值里没有汉字、`t('key')` 没有写错的键名、T 表之外没有中文串。
2. **从仓库根发布，资产零复制**：GitHub Pages 源 = `main` + `/`，根目录放 `.nojekyll`。
   `index.html` 与 `site/` 只是薄薄一层，图片/视频按仓库内相对路径就地服务 —— 站点体积 = 仓库体积
   （当前约 550 MB < Pages 的 1 GB 上限）。
   若改成 Actions artifact 部署，每次都要上传 550 MB，**不要这么干**。

## 2. 路由

| 路由 | 页面 |
|------|------|
| `#/` | 列表页第一层：billboard（4 张轮播）+ 每个项目一条横向行 + 全部项目 |
| `#/p/<pid>` | 列表页第二层（项目页）：项目头图 + **每卷一条横向行** |
| `#/w/<pid>` | 详情页：整个项目的 feed（各卷首尾相接） |
| `#/w/<pid>/<n>` | 详情页：项目 feed 的第 n 帧（1 起） |
| `#/w/<pid>/r/<rid>[/<n>]` | 详情页：某一卷的 feed（`/s/<sid>` 也认，兼容旧链接） |
| `#/videos` · `#/bio-splice` · `#/s/<sid>` | 旧链接：分别落到视频项目页 / 生物拼接项目页 / 对应卷 |

- **帧的位置就是路由**：feed 内滚动时用 `history.replaceState` 同步 `#/w/.../<n>`，
  所以刷新、分享、前进后退都能回到同一帧。
- 路由解析只有一处（`parse()`）。前端**不猜**如何拼链接：首页卡片的目标写在
  `index.json` 的 `strip[].route` 里，项目页卡片由 `pager(pid)` 统一拼。

## 3. 列表页

- **首页只读 `index.json`**（约 12 KB）：项目卡片自带 `strip[]`——首页横向行要展示的
  卡片（海报缩略图 + 标题 + 计数 + 目标路由）在 build 时就生成好了，
  所以**首屏不必拉任何项目数据**（bio-splice 一份就 343 KB）。
  `strip` 规则：有多个卷 → 每卷一张卡（点进该卷）；只有一个卷（shanhai-jing）→ 直接摊开该卷的帧。
- billboard 用**封面缩略图放大 + 模糊**当背景（480px 够用），右侧放一张 2:3 的清晰海报；
  7 秒轮播，鼠标悬停暂停，圆点可点。**没有封面的项目不进 billboard**。
- 无内容项目（character-lookbook）不进横向行，只在"全部项目"里出现并外链 README。

## 4. 详情页（feed）

- 一屏一帧：`.fr{height:100dvh; scroll-snap-align:start; scroll-snap-stop:always}`，
  容器 `.feed{scroll-snap-type:y mandatory}`——**上下滑动/滚轮/触屏都是原生行为**，不靠手势库。
- 换帧方式：滑动、`↑↓←→`、`PgUp/PgDn`、`Home/End`、右侧 ↑↓ 按钮、顶部进度条分段点击。
- **进度条按「卷 + 角色」分段**（`computeRuns()`，宽度按帧数）：一眼看出这段是定稿还是
  合图/对照/审计，也用来跳段。
- **一屏只放一张图 + 一段文字**：抬头（卷 · 期）、标题（帧标签，缺省用角色名）、说明、
  原文块（数据里有 `text_ref` 才有）、徽标 chips（角色/期/评分/种子/体积）。
  文字超过 4 行折叠，点画面切换沉浸模式（隐藏所有浮层），`i` 打开信息面板看
  提示词 / 评分明细 / 种子 / SHA / 文件。
- **资源策略（重要）**：卡片与首屏占位一律用 `site/thumbs` 的缩略图；
  只有 `FEED_WINDOW = ±2` 帧内的图才把 `src` 换成原图，滑走就退回缩略图——
  否则 bio-splice 一卷 30 件、合计 300 MB 会全挂在内存里。
  视频 `preload="none"`，滑到才挂 `src`，滑走暂停。

## 5. 数据层（`tools/build_site.py`）

只读源素材、**幂等**（同输入产出逐字节相同的 JSON）、零依赖。契约：

```
site/data/index.json      {counts, projects:[卡片 … 卡片.strip 见 §3]}
site/data/<pid>.json      {id, kind, title, desc, readme, summary, plan, rubric, stats,
                           reels:[{id, title, desc, poster, cover, count, finals, bytes,
                                   periods:[{id,title,note,doc}], text_ref, doc,
                                   items:[{kind, src, thumb, size, role, period, label,
                                           note, shot, round, engine, seed, sha256,
                                           prompt, scores}]}]}
```

- **一帧 = 一张图或一段视频**；文字全部挂在帧上，前端只负责渲染，不再自己拼文案、
  也不再按项目名硬编码渲染器。`role` 取值：`final` / `control` / `retired-control` /
  `sheet` / `audit` / `image` / `video`（文案在 app.js 的 `ROLE`→`T` 里）。
- **归类按结构**，不按名字（`kind_of_reel()`）：
  | kind | 判据 | 卷的划分 | 前端表现 |
  |------|------|----------|----------|
  | `periods` | 有 `subjects/*/period-*/manifest.json` | 一卷 = 一个子主题 | 项目页每卷一行；feed 成品在前、合图/对照/审计在后 |
  | `gallery` | 有图片、无期 manifest 也无 mp4 | 一卷 = 一个阶段目录 | 同上（bone-china-doll 5 卷） |
  | `videos` | 含 `.mp4` | 一卷 = 一个视频子项目 | 同上（video-projects 5 卷 7 段） |
  | `project` | 都没有（character-lookbook 尚无成品） | — | 只出现在"全部项目"，外链 README |
  `_` 开头（`_template`）跳过。**别再退回硬编码**——实测漏掉过整个项目。
- **卷内顺序是刻意的**：定稿 → 本期合图 → 同期对照 → 全套合图 → 轮次审计。
  一进来滑到的都是成品，过程件集中在后面，且每帧都带 role 徽标。
- **帧级文字的来源与优先级**（能查证才写，查不到就留空让前端退回角色名）：
  1. 期 README 成品表第三列（`read_captions()`，实测覆盖约 46%，`| # | 文件 | 移植部位 | …` 这类布局）；
  2. manifest `note` 的抬头（`split_note()` 认「图赞主图：…」与「白描画心（供制版使用）」两种写法）；
  3. manifest `kind`（`plate`→白描画心 / `card`→图赞卡片）；
  4. 说明文字：帧 `note` → 期 `note` → 卷 `desc`（`read_para()` 取 README 首段，
     中英分别读 `X.md` 与 `X.en.md`——**英文侧是真翻译，不是把中文塞过去**）。
  - `label.en` 缺省时留空，前端用角色名兜底（英文界面不会露出中文抬头）；
    只有少数几种已知抬头写在 `LABEL_EN` 里。
- **子主题元数据**：有 `SUMMARY.md` 就用它（bio-splice）；没有就 `discover_subjects()` 扫目录自建
  （shanhai-jing）。标题查 `SUBJECT_TITLES`，缺了退回目录名。
- 轮次文件名要用**宽容正则**：实测有 `r01-review.md`、`ts-r3-review.md`、`fb2-r1-review.md`、
  `dn-r10-review.md`：`^(?:[A-Za-z0-9]+-)?r(\d+)-(review|audit)\.(jpg|md)$`
- **评分维度随项目走**（`RUBRICS`，写进 JSON 由前端读），不要写进 `app.js`——
  bio-splice 是 A–E 五维、shanhai-jing 是 A–F 六维。
- 新增内容后重跑生成器；`main()` 末尾会拿 SUMMARY.md 的基线（12/60/135/59）自检，
  不一致就退出码 2。

### 缩略图（卡片与占位**不得直出原图**）

`build_site.py` 在生成数据的同时产出 `site/thumbs/`（最长边 480px、JPEG）：

| 字段 | 用途 | 谁加载 |
|------|------|--------|
| `thumb` | 卡片、feed 首屏占位与模糊底 | 首屏与滚动时 |
| `src` / `cover` / `poster` | **原图** | 详情页当前 ±2 帧、点"原图"时 |

- 收益实测：bio-splice 单页 **306 MB → 9.5 MB**；首页封面 **5.34 MB → 0.13 MB**。
- **增量**：缩略图存在且不比源新就跳过 → 重跑几乎零成本（实测 415 张全部命中缓存）。
- **优雅退化**：没有 `ffmpeg` 时返回原图（页面变重但不报错）；`--no-thumbs` 显式跳过。
- ⛔ **三个必须守住的约束**（都实际踩过，见 `thumb_of()` 的注释与断言）：
  1. `src` 可能是**绝对路径**——直接 `os.path.join(THUMB_DIR, src)` 会丢掉前缀、写进源目录；
     所以一律先 `os.path.relpath(src, ROOT)` 归一。
  2. 源本身是 `.jpg` 时，上面那个 bug 会让输出路径**正好等于源路径**，`ffmpeg -y` 直接覆盖原图。
     所以有两道 `RuntimeError` 断言：输出必须在 `THUMB_DIR` 内、且不等于源。
  3. **已经是缩略图**的路径不能再缩一遍（会生成 `site/thumbs/site/thumbs/…` 套娃）：
     命中 `THUMB_DIR` 前缀直接返回。
- 前端一律写 `e.thumb || e.src`（缺字段时自然退回原图，不会白屏）。

## 6. 前端

- 纯 vanilla：**无框架、无 CDN、无构建**；只加 `site/index.html`、`site/app.{css,js}` 与 `site/data/*.json`。
- 图片 `loading="lazy" decoding="async"`；视频 `preload="none"` + 分镜图 `poster`（不滑到不下载）。
- **导航从 `index.json` 派生**（有内容的 kind 自动进导航），不要把某个项目写死成顶级项。
- 风格：暗色优先（`prefers-color-scheme: light` 有浅色变体）、海报不裁切
  （缩略图铺一层模糊底 + 前景 `object-fit:contain`）、`prefers-reduced-motion` 下去掉动效。
- **头图带永远是暗的**（billboard 与项目页 hero 都用 `#0b0b0d` 底 + 白色文案）：
  浅色主题下把深色文字压在深色蒙版上会整块读不清，这是实测踩过的。
- **poster 卡必须是 `display:flex;flex-direction:column`**：`.tile` / `.cap` 都是 `span`，
  不显式 flex 就是行内流——`aspect-ratio` 失效、卡片下面的标题说明整行消失。
- 详细页是覆盖层（`#feed`），不是 `<dialog>` 灯箱：**灯箱已随 feed 一起移除**，
  元数据从"灯箱侧栏"搬到信息面板。

## 7. 本地预览

```sh
tools/preview.sh              # → http://127.0.0.1:8090/
tools/preview.sh 8123 lan     # 局域网 / 手机
tools/preview.sh stop 8090    # 停止
```

- 必须走 `http://`：双击 `index.html` 会因跨源策略读不到 `site/data/*.json`（页面会给出提示）。
- 端口被自己的预览占用会友好提示；被别的程序占用会自动换端口。

## 8. 发布与线上验证

- 推完 `main` 等 Pages 构建（约 1 分钟）；`gh api repos/<owner>/<repo>/pages/builds/latest --jq .status` 看状态。
- 本机对 `github.io` 有线路抖动时，用可用边缘 IP 直连验证：

```sh
for ip in 185.199.108.153 185.199.109.153 185.199.110.153 185.199.111.153; do
  curl -s -o /dev/null -w "$ip %{http_code}\n" --max-time 8 \
    --resolve thzsummer.github.io:443:$ip https://thzsummer.github.io/gen-media/
done
```

实测 `.110` / `.111` 通常可用，`.108` / `.109` 可能超时；DNS 轮到坏 IP 时浏览器会卡住，多刷几次或用 `--resolve` 验证。

## 9. 无头验证（改了前端就跑一遍）

本机的 chromium 是 snap 包，`snap run` 在容器里会因 transient scope 失败；**用 snap 目录里的
二进制直接跑**可以绕过：

```sh
CH=/snap/chromium/current/usr/lib/chromium-browser/chrome
XDG_RUNTIME_DIR=/tmp/xdg $CH --headless=new --no-sandbox --disable-gpu \
  --virtual-time-budget=9000 --dump-dom 'http://127.0.0.1:8090/#/w/shanhai-jing/r/jiu-wei-hu/2'
```

数 DOM 结构（`class="fr"` / `class="pcard"` / `#runs button`）验证渲染，比只看 HTTP 200 可靠。

`--dump-dom` 看不到的交互（点语言、开信息面板、键盘换帧、进度条跳段、沉浸模式），
用一张**临时驱动页**（与 `index.html` 同构 + 末尾一段按 query 触发动作的脚本）
在仓库根跑完就删；三个必须知道的坑：

1. **轮询等待，别用固定 `setTimeout`**：固定延时会在 fetch/render 之前触发，动作落空
   （表现是"DOM 里没有动作痕迹"，很容易误判成功能坏了）。
2. **虚拟时间不推进 CSS 过渡与平滑滚动**：截图会停在过渡起点（图片只有 55% 不透明度、
   面板还在屏幕外、计数停在滚动中途）。驱动页里注入 `*{transition:none!important}`
   并把 `Element.prototype.scrollTo` 的 `behavior` 改成 `auto`，看到的才是终态。
3. **每次一个全新 `--user-data-dir`**：共用一个 profile 会撞 SingletonLock（chromium 直接退出、
   stdout 为空），而且磁盘缓存会让下一轮拿到上一轮的 `app.js`（实测：英文那轮渲染出中文）。
   再加 `--disk-cache-size=1` 更稳。

暗色/浅色都要看：无头默认是浅色，暗色用驱动页注入一份 `:root{--bg:…}` 覆盖即可
（`.bill` 与 `.hero` 是**永远暗**的影院带，两套主题下都不变）。
