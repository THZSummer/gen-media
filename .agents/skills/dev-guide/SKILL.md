---
name: dev-guide
description: gen-media 仓库的开发规范总纲，新增或修改任何内容前先加载：双语文档（中文 X.md 默认 + 英文 X.en.md，两侧语言切换行）、双语画廊站点（GitHub Pages 从仓库根零复制发布）、技能库准入标准与 DSH 项目技能格式、生成纪律（同轮底座对照 / 评分过关 / 像素判据）、资产与文件规范、gits submodule 协作与交付前检查清单。触发词：给这个仓库加东西、新增项目/技能/文档、站点怎么发、要不要做英文版、提交前检查、规范是什么。
whenToUse: 在 gen-media（或它的 gits submodule 检出）里新增/修改任何内容之前加载 —— 新增项目、新增技能、改文档、改站点、动脚本、提交推送时都用它对齐规范；不确定某个文件要不要英文版、图片要不要入库、站点怎么发布时也用它。
---

# gen-media 开发规范（dev-guide）

## Summary

gen-media 是"图片生成 + 视频生成"的作品集仓库，**扁平化为三块**：`.agents/skills/`（技能库，图片与视频技能合一处）、`projects/`（项目库，一项目一目录）、`methods/`（视频方法手册）；外加一个双语画廊站点（`site/`）与一条工具链（`tools/`）。这个技能是**项目级规范总纲**，把所有"往仓库里加东西"时必须遵守的约定收在一处；具体怎么出图/出片仍看 `.agents/skills/` 里的技能。

三条最容易踩的硬约束：**非技能 markdown 必须中英成对**、**站点与界面文案必须双语**、**大体积中间产物不入库**。

## Table of Contents

- [硬性要求](#硬性要求)
- [工作流](#工作流)
- [交付前校验](#交付前校验)
- [详细参考](#详细参考)
- [Dev Note](#dev-note)

## 硬性要求

| # | 要求 | 检查 |
|---|------|------|
| 1 | **站点必须支持双语**：默认中文，界面可切 EN，选择存在浏览器 | 点两次切换按钮，界面文案与数据标题都跟着换 |
| 2 | **非技能 markdown 必须双语**：中文 `X.md` 为默认，英文为同名 `X.en.md`，两侧顶部一行语言切换 | `python3 tools/i18n.py check` 三项必须全 0 |
| 3 | **技能文档只写中文**：`.agents/skills/` 下的技能不做英文版 | `i18n.py` 已排除该前缀，`check` 不应把它们算作缺件 |
| 4 | **大体积中间产物不入库**：`work/`、`out/r*/`、逐镜头 mp4 等留本地 | `git status` 里看不到；文档指向它们的链接属"预期断链" |
| 5 | **定稿必须经评分过关**才进期目录；**每轮必带同轮底座对照** | 期目录有 `manifest.json`（`role: final` / `control`）与 `controls/` |
| 6 | **新增技能要能被 DSH 发现**：放在 `.agents/skills/<kebab-name>/SKILL.md` | 目录名 = frontmatter `name`；见 [references/skills.md](references/skills.md) |
| 7 | **技能根下的索引 README 不写 frontmatter**（写了会被当成技能加载） | `.agents/skills/README.md` 无 YAML 头；见 [references/skills.md](references/skills.md) |
| 8 | **图片不成对改**：成品与对照用 PNG，合图/审计图用 JPEG | 见 [references/assets.md](references/assets.md) |
| 9 | **站点是「列表页 + 详情页」两层**：列表页是 billboard + 横向行，详情页是一屏一帧的全屏 feed（上下滑动换图）；卡片只用缩略图 | `python3 tools/i18n.py ui`；改前端后按 [references/site.md](references/site.md) §9 无头验证 |

## 工作流

### 新增或修改文档

```sh
# 1) 改中文版
$EDITOR path/to/X.md
# 2) 同步英文版（结构一一对应：标题层级、表格行列、代码块数量与内容）
$EDITOR path/to/X.en.md
# 3) 流水线补齐切换行、改内链、体检
python3 tools/i18n.py switch   # 两侧语言切换行（幂等）
python3 tools/i18n.py links    # 英文版内链改指 .en.md
python3 tools/i18n.py check    # 缺件 / 疑似未翻译 / 断链 必须全 0
```

细节与判据见 [references/i18n.md](references/i18n.md)。

### 新增项目

1. 复制模板：`cp -r projects/_template projects/<项目名>`（视频项目用 `projects/_template`）。
2. 在项目 `README.md` 写清交付物、图片清单、所用技能、验收标准；**同时写 `README.en.md`**。
3. 把项目登记进 `projects/README.md`（及 `.en.md`）。
4. 出图/出片遵循 [references/generation.md](references/generation.md) 的纪律。

### 新增技能

按 DSH 项目技能规范落位：

```sh
mkdir -p .agents/skills/<kebab-name>/references
$EDITOR .agents/skills/<kebab-name>/SKILL.md
```

- `name` 必须 kebab-case 且与目录名一致；`description` 要写"做什么 + 何时用"（路由描述，DSH 目录默认截断到 500 字符）。
- 详细的参考资料放 `references/*.md`，脚本放 `scripts/`，模板放 `templates/` —— 用**相对本技能目录**的路径引用。
- 只在技能库里放**带脚本、有自检入口、能在真机跑通**的技能；纯文档不收（见 [references/skills.md](references/skills.md)）。

### 改站点

- 形态是**流媒体式两层**：列表页（`#/` 与 `#/p/<pid>`：billboard + 横向行）
  → 详情页（`#/w/<pid>[/r/<rid>][/<n>]`：全屏 feed，一屏一帧 = 一张图 + 一段文字，上下滑动换图）。
- 数据层：改 `tools/build_site.py`（只读、幂等），产物 `site/data/*.json` 随仓库提交；
  帧级文字也在这里装配（**不在前端拼文案**）。
- 前端：改 `site/app.{css,js}`（纯 vanilla，无框架/CDN/构建）；**任何界面文案都要同时写 `T.zh` 与 `T.en`**，
  改完跑 `python3 tools/i18n.py ui`。
- 资源纪律：卡片/占位用 `thumb`，只有详情页当前 ±2 帧才换原图。
- 本地看：`tools/preview.sh`（必须走 http，别双击 `index.html`）。
- 发布：Pages 源为 `main` + `/`（根目录放 `.nojekyll` 关掉 Jekyll）；详见 [references/site.md](references/site.md)。

### 提交与协作

```sh
git add -A && git commit -m "<做了什么 + 验证证据>" && git push
# 回 gits 推进 submodule 指针（否则 gits 记的还是旧版本）
cd ../.. && git submodule update --remote GitHub/gen-media && git add GitHub/gen-media \
  && git commit -m "chore(submodule): gen-media → <sha>" && git push
```

配额、submodule 纪律见 [references/workflow.md](references/workflow.md)。

## 交付前校验

```sh
.agents/skills/dev-guide/scripts/check.sh          # 一键跑完全部机械检查
```

脚本依次执行：双语三项体检 → 站点数据幂等性 → 技能自检 → **站点界面文案双语（`i18n.py ui`）** → 技能自身格式。通过后再人工确认：新文档有没有英文版？新界面文案有没有中英两份？新图有没有进 `manifest.json`？中间产物有没有被误加进 git？

## 详细参考

| 参考 | 内容 |
|------|------|
| [references/i18n.md](references/i18n.md) | 双语规范：命名、切换行格式、翻什么/不翻什么、`tools/i18n.py` 用法与判据 |
| [references/site.md](references/site.md) | 站点：列表页/详情页两层结构与路由、feed 数据契约、缩略图纪律、双语界面文案、无头验证、零复制发布 |
| [references/skills.md](references/skills.md) | 技能库：DSH 项目技能格式（目录结构 / frontmatter / 发现优先级）、准入标准、脚本纪律 |
| [references/generation.md](references/generation.md) | 生成纪律：期内恒定、同轮对照、评分维度、像素判据、轮次记录 |
| [references/assets.md](references/assets.md) | 资产：PNG/JPEG 分工、体积与单文件上限、不入库清单、可复现性说法 |
| [references/workflow.md](references/workflow.md) | 协作：submodule 指针、Gitee 配额、提交信息、不虚报原则 |

## Dev Note

- **为什么条文这么琐碎**：这些都是实际踩过的坑。例如英文版内链曾被批量改成指向自己（`links` 不排除语言切换行）、`prompts-all` 类存档被"疑似未翻译"误报（正文中文都在代码块内）、以及 GitHub Pages 在 `/gen-media/` 子路径下必须用仓库相对路径才不会 404。
- **规范随事实更新**：改了流水线判据、换了发布方式、调整了目录结构，都要回来改这个技能与对应 references，并在下方记录。
- **技能本身不翻译**：技能面向 Agent 执行，只有中文版；但技能里指向的**仓库文档**必须双语。

## 修订记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-10-05 | v1.0 | 建立：按 DSH 项目技能规范（`.agents/skills/<name>/SKILL.md`）落位，收录双语、站点、技能、生成、资产、协作六类规范与交付前检查脚本 |
| 2026-10-05 | v1.1 | **随扁平化重构同步**：结构描述从"两个内容库"改为三块（`.agents/skills/` / `projects/` / `methods/`）；技能路径 `image-gen/skills/**`、`video-gen/skills/**` → `.agents/skills/**`；`i18n` 排除前缀随之收敛；站点文档的示例路径改为 `projects/...`；协作文档订正 submodule 事实（`gits` 以指针引用本仓库） | 小七 |
| 2026-10-05 | v1.2 | **dev-guide 自身迁入 `.agents/skills/`**：与 5 个执行技能并列（技能根 rank 从 `project-dsh` 换到 `project-agents`），`.dsh/` 目录随之移除；`i18n` 排除前缀收敛为 `(".agents/skills/",)`；`check.sh` 的 `ROOT` 推导注释同步（深度未变，`../../..` 仍指向仓库根）；清理此前替换遗留的重复枚举 | 小七 |
| 2026-10-05 | v1.3 | **索引 README 不写 frontmatter**：`.agents/skills/README.md` 去掉 YAML 头（带 frontmatter 的 md 在技能根下会被当成技能加载，实测它曾以 `gen-media-skills-index` 身份出现在技能目录里）；硬性要求新增第 7 条 + `references/skills.md` 补判断标准 | 小七 |
| 2026-10-05 | v1.4 | **站点改为流媒体式两层**：列表页（billboard + 横向行）与详情页（全屏 feed，一屏一帧、上下滑动换图），灯箱移除；`build_site.py` 的数据契约改为`reels[].items[]`（帧级文字 + `index.json` 里的 `strip` 首页卡片）；新增第 9 条硬性要求、`i18n.py ui` 界面文案体检（并进 `check.sh` 第 4 步）、`references/site.md` 重写 | 小七 |
| 2026-10-06 | v1.5 | **`check.sh` 覆盖付费云端技能**：第 3 步新增 `seedream-text-to-image` 两项（离线 `test_skill.py` + 真机 `--check`，都不花钱）；明确**付费矩阵 `verify_params.py` 不进**自动检查（每步一张图，要人工决定）；准入标准未变——"只收录带脚本、有自检、能真机跑通"的技能，这次是同一标准下的**重新收录**（9 个无脚本 Seedream 文档技能已于 2026-10-05 移除） | 小七 |
| 2026-10-06 | v1.7 | **站点主题改为「默认深色 + 显式切换」**（`references/site.md` §6/§9）：原先 `:root` 深色 + `@media (prefers-color-scheme: light)` = 跟随系统；现改为深色恒为默认、**不跟随系统**，浅色只在 `<html data-theme="light">` 时生效，状态存 `localStorage['gm-theme']`，`?theme=dark|light` 可覆盖；顶栏加图标开关（可见内容只有 `☀`/`☾`，无障碍名走双语 T 表，`meta[theme-color]` 跟随）。§9 补本机实测的 chromium 旗标：`--dump-dom` 要 `--no-zygote --single-process`，`--screenshot` 不能加 | 小七 |
| 2026-10-06 | v1.6 | **`check.sh` 纳入 `seedream-image-edit`**：同一个付费 partner 节点的**图片编辑**技能（参考图接 `model.images.image_N`、Painter 按 alpha 合成标注层），第 3 步加它的离线 `test_skill.py` 与真机 `--check`；付费矩阵 `verify_edits.py` 同样**不进**自动检查 | 小七 |
