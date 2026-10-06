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
                                   audio:{src,size,duration_s,seed,sha256,preset,skill,generated},
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

### 5.1 详情页配乐（`reel.audio`）

**数据侧**：期 manifest 里可选写一段 `audio`，生成器（`reel_audio()`）把它翻成站点数据：

```json
"audio": {"file": "bgm/jiu-wei-hu-bgm.mp3", "duration_s": 30.0, "seed": 9097,
          "sha256": "…", "preset": "模板 A · 古琴独奏", "skill": "comfyui-music-minimax3",
          "generated": "2026-10-07"}
```

- `file` 相对**期目录**；生成器换成仓库相对路径（配 `size`），前端按 §6 的 `BASE` 拼接。
- **文件不存在就不出 `audio` 键**：宁可不显示开关，也不要一个点了没声音的按钮。
- 一卷一个配乐（`reel` 级，不是帧级）：同一子主题的成品/对照共用同一首曲子。
- 音频产物入库（是交付物，不是中间产物），但**按"最短够用"出**：30 s / 128 kbps 约 480 KB；
  V0 高码率母版留在 `work/`，站点上是转码后的版本。转码与落位走
  `projects/shanhai-jing/scripts/place_bgm.py`（ffmpeg 转码 + 写回 manifest + 自检）。

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
- **前端资源必须带内容哈希**：`index.html` 里写 `site/app.css?v=<hash>` / `site/app.js?v=<hash>`，
  由 `python3 tools/stamp_frontend.py` 写入（改了 `app.{css,js}` 就重跑一次；`--check` 已进 `check.sh`）。
  为什么必须：无构建步骤 + 裸 URL 时，浏览器会**按文件各缓存**，出现过「新的 `index.html` + 旧的 `app.css` +
  旧的 `app.js`」这种**混合缓存**——表现是主题按钮变成一个**空框**、点了没反应（VS Code 内置浏览器实测；
  用户禁掉缓存后立刻正常）。带哈希后前端一改 URL 就变，不可能新旧混搭。
- **导航从 `index.json` 派生**（有内容的 kind 自动进导航），不要把某个项目写死成顶级项。
- **主题：默认深色，且不跟随系统**（`prefers-color-scheme` 有意不参与——2026-10-06 用户明确要求「默认深色」）。
  浅色只能由用户显式切换：`<html data-theme="light">`；状态存 `localStorage['gm-theme']`。
  - 引导脚本放在 **`index.html` 的 `<link rel=stylesheet>` 之前**（读 `?theme=dark|light` → `localStorage`），
    首屏前打好标记，不闪白；深色是 `:root` 的默认值，切回深色用**移除属性**，样式表里不必把深色写两遍。
  - 开关放在顶栏语言开关右侧：**内联 SVG 图标 + 可见文字**（深色下 `太阳 · 浅色`、浅色下 `月亮 · 深色`）。
    ⛔ **图标不能用文字字形**（`content:'☀'` 这类）：`☀`/`☾` 属于符号字体，IDE 内置浏览器缺字形时
    会渲染成**方块**——2026-10-06 实测踩过。两个 SVG 都在 DOM 里，用 CSS 按主题切 `display`（首屏即正确），
    并且给 SVG 写死 `width/height` 属性；**可见文字**是第二重保险（万一图标没渲染，按钮也不是一个空框）。
    无障碍名走 `T.zh`/`T.en`（`themeToLight` / `themeToDark`）并随语言更新；`aria-pressed` 表示当前是否浅色。
  - `<meta name="theme-color">` 跟着主题走（深 `#0b0b0d` / 浅 `#f7f6f3`）。
  - 改了主题按 §9 验三件：默认深色（**系统偏好为浅色时仍须是深色**）、`?theme=light`、点击切换后刷新保持。
- 海报不裁切（缩略图铺一层模糊底 + 前景 `object-fit:contain`）、`prefers-reduced-motion` 下去掉动效。
- **头图带永远是暗的**（billboard 与项目页 hero 都用 `#0b0b0d` 底 + 白色文案）：
  浅色主题下把深色文字压在深色蒙版上会整块读不清，这是实测踩过的。
- **poster 卡必须是 `display:flex;flex-direction:column`**：`.tile` / `.cap` 都是 `span`，
  不显式 flex 就是行内流——`aspect-ratio` 失效、卡片下面的标题说明整行消失。
- 详细页是覆盖层（`#feed`），不是 `<dialog>` 灯箱：**灯箱已随 feed 一起移除**，
  元数据从"灯箱侧栏"搬到信息面板。
- **详情页配乐开关**（2026-10-07 加，卷有 `reel.audio` 时才渲染）：
  - 位置在最上面的 feed 栏 `.fb-act` 里（`data-act="music"`），样式与文案沿用主题开关的约定：
    **内联 SVG 音符 + 可见文字**（`musicPlay` / `musicStop`），窄屏 ≤720px 只留图标；
    `data-on="1"` 与 `aria-pressed` 表示正在播放，`title`/`aria-label` 里带**配乐署名**
    （`musicCredit`：配乐是 AI 生成的，主动标注）。
  - ⛔ **不做自动播放**：浏览器要求用户手势，静默 `play()` 会被拦。开关就是那个手势；
    被拦或文件坏了 → `musicErr`（`配乐不可用`）+ 按钮回到关闭态，不假装在放。
  - 一个隐藏的 `<audio id="bgm" loop preload="none">` 承载播放；`volume=0.55`（画面上有竖排原文要读）。
  - **离开详情页必停**（`closeFeed()` 里 pause + 清 `src`）；**换卷换音源**（`activate()` → `syncMusic()`），
    当前帧所属卷没有配乐就把开关藏起来并停声；点开帧内视频时先让配乐闭嘴（避免两条音轨打架）。
  - 改了这段按 §9 验：开关存在且 `data-on` 随点击翻转、`#bgm` 的 `src` 指向 `reel.audio.src`、
    离开详情页后 `#bgm.paused === true`。

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

> ⚠️ **2026-10-07 实测补充：chromium 需要「写在工作区内的 HOME」**。只加 `--user-data-dir`
> 不够——`HOME=/home/usb` 时 crashpad 起不来（`chrome_crashpad_handler: --database is required`），
> **stdout 为空**，很容易误判成"页面没渲染"。三组对照：

```sh
WS=/home/usb/wks/gits/GitHub/gen-media
mkdir -p $WS/work/home-dir $WS/work/chrome-prof
# A) HOME 不变 + --user-data-dir 在工作区          → 0 字节 DOM（crashpad 报 --database is required）
# B) HOME=$WS/work/home-dir + --user-data-dir       → ✅ 18160 字节 DOM
# C) A + --disable-crash-reporter --disable-breakpad → 仍然 0 字节
env HOME=$WS/work/home-dir XDG_RUNTIME_DIR=/tmp/xdg \
  /snap/chromium/current/usr/lib/chromium-browser/chrome \
  --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage \
  --user-data-dir=$WS/work/chrome-prof \
  --virtual-time-budget=9000 --dump-dom 'http://127.0.0.1:8090/#/w/shanhai-jing/r/jiu-wei-hu/2'
```

（`--no-zygote --single-process` 这套旗标在本机**会 SIGTRAP 崩溃**（exit 133），别再用它兜底；
需要的是上面的 HOME。）截图仍按 §9 开头那条：**`--screenshot` 不要加** `--no-zygote --single-process`。

`--dump-dom` 看不到的交互（点语言、开信息面板、键盘换帧、进度条跳段、沉浸模式、
**详情页配乐开关**），用一张**临时驱动页**（与 `index.html` 同构 + 末尾一段按 query 触发动作的脚本）
在仓库根跑完就删；三个必须知道的坑：

1. **轮询等待，别用固定 `setTimeout`**：固定延时会在 fetch/render 之前触发，动作落空
   （表现是"DOM 里没有动作痕迹"，很容易误判成功能坏了）。
2. **虚拟时间不推进 CSS 过渡与平滑滚动**：截图会停在过渡起点（图片只有 55% 不透明度、
   面板还在屏幕外、计数停在滚动中途）。驱动页里注入 `*{transition:none!important}`
   并把 `Element.prototype.scrollTo` 的 `behavior` 改成 `auto`，看到的才是终态。
3. **每次一个全新 `--user-data-dir`**：共用一个 profile 会撞 SingletonLock（chromium 直接退出、
   stdout 为空），而且磁盘缓存会让下一轮拿到上一轮的 `app.js`（实测：英文那轮渲染出中文）。
   再加 `--disk-cache-size=1` 更稳。
4. **配乐开关要连点两下**（2026-10-07 加）：第一下开、第二下关。**第二下的断言不能只看
   `data-on=0`**——`play()` 的 promise 会被紧随其后的 `pause()` 以 `AbortError` 打断，
   若把它当播放故障，按钮文案会错成「配乐不可用」（`site/app.js` 的 catch 里已按
   `err.name === 'AbortError'` 放行；探针要同时断言"关闭后文案回到 action"）。
   还要验"离开详情页音频已暂停"：`#bgm` 会随 `feedRoot.innerHTML=''` 一起被移除，
   所以要在点击前把音频元素句柄存到 `window` 上，之后读那个 detached 元素的 `paused`。

**本机实测可用的 chromium 旗标（2026-10-07 更正）**：
~~`--dump-dom` 必须加 `--no-zygote --single-process`~~ —— **这条 2026-10-07 被推翻**：
本机现在加这两个旗标会 **SIGTRAP 崩溃（exit 133）**、stdout 仍是空。
真正缺的是 **`HOME` 必须指向工作区内的可写目录**（crashpad 需要在那里建数据库），
见上一条三组对照。现行可用组合：

```sh
HOME=$WS/work/home-dir XDG_RUNTIME_DIR=/tmp/xdg $CH --headless=new --no-sandbox \
  --disable-gpu --disable-dev-shm-usage --user-data-dir=$WS/work/chrome-prof-<每轮新建> \
  --disk-cache-size=1 --virtual-time-budget=9000 --dump-dom '<url>'
```

`--screenshot` 同样用这套（**不加** `--no-zygote --single-process`，单进程下合成帧拿不到、
报 `blink.mojom.WidgetHost` 且不落文件）。先 `mkdir -p /tmp/xdg && chmod 700 /tmp/xdg` 再给 `XDG_RUNTIME_DIR`。

主题现在**默认深色**，两套都要看：默认（不带参数）必须深色 —— 无头 chromium 的系统偏好本来就是浅色，
所以「`matchMedia('(prefers-color-scheme: light)').matches === true` 而 `body` 背景仍是 `rgb(11,11,13)`」
正好是「不跟随系统」的直接证据；浅色用 `?theme=light`，或驱动页里点一下开关再看刷新后是否保持。
（`.bill` 与 `.hero` 是**永远暗**的影院带，两套主题下都不变。）
