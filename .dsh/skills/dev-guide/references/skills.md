# 技能库规范

> 返回 [SKILL.md](../SKILL.md)

## 1. DSH 项目技能的目录结构

DSH 按 rank 扫描本地技能根（见 `docs/subsystems/skills` 规范），**项目级有两个**：

| Rank | Source | Root |
|------|--------|------|
| 100 | `project-dsh` | `<projectRoot>/.dsh/skills` ← 本项目用这个 |
| 200 | `project-agents` | `<projectRoot>/.agents/skills`（Agent Skills 通用位置） |

`projectRoot` = 最近的含 `.git` 的祖先目录。**本项目根 = gen-media 根**，所以技能放：

```text
gen-media/.dsh/skills/dev-guide/
├── SKILL.md           必需；目录名必须等于 frontmatter 的 name
├── references/        可选；详细参考资料（按需加载）
├── scripts/           可选；可执行脚本
├── templates/         可选；模板
└── assets/            可选；静态资产
```

规则：

- **name 必须 kebab-case**：`^[a-z0-9]+(?:-[a-z0-9]+)*$`，且与父目录名一致（DSH 不强制，但其他实现强制，保持一致最省事）。
- **只接受目录包 `<name>/SKILL.md` 与扁平文件 `<name>.md`；不支持嵌套递归 `**/SKILL.md` 发现。**
- 资源文件（`references/`、`scripts/`、`templates/`）用**相对本技能目录**的路径引用；加载时才按需解析，目录不会被枚举。
- 改了技能正文，下一次工具调用即可见（无需重载目录）；改目录结构由 watcher 感知。

## 2. frontmatter

```yaml
---
name: dev-guide                                     # 必需，kebab-case，= 目录名
description: 做什么 + 何时用（路由描述，模型靠它决定是否加载）   # 必需
whenToUse: 补充路由指引（可选）                       # 可选
disable-model-invocation: true                      # 可选：只允许用户显式调用
user-invocable: false                               # 可选：只允许模型自动调用
---
```

- `description` 要写"**做什么 + 何时用**"，别写"帮助处理 X"这种没有路由信息的话。
- DSH 的模型目录默认把 description 截到 **500 字符**（`catalogDescriptionMaxLength`），要点前置。
- 不要把 `name` 与目录名写得不一致；不要用大写、下划线、连续连字符。

## 3. 什么时候该写技能、什么时候不该

| 该写技能 | 不该写技能 |
|----------|------------|
| 一套需要多步上下文的工作流（本项目：开发规范、出图规范） | 一次性任务说明（写进项目 README） |
| 需要把脚本/模板/参考捆在一起、按需加载 | 只是"某命令怎么用"（写进 references 或 README） |
| 面向 Agent 的可复用执行指引 | 面向人的成品展示（进 site 或项目 README） |

**准入标准**：技能库里只放**带脚本、有自检入口、能在真机跑通**的技能。纯文档（教怎么用外部 CLI、仓库里没有可执行代码）不进技能库 —— image-gen 曾按此把 9 个纯文档技能移除，只留 3 个可执行技能。

## 4. 可执行技能的必要件

| 必须有 | 说明 |
|--------|------|
| `SKILL.md` | frontmatter + 何时用 + 前置检查 + 执行步骤 + 踩坑点 + 检查清单 |
| 自检入口 | `--check`（探活 + 查模型文件在位）或离线 `scripts/test_skill.py`（mock 服务器也能跑） |
| 明确术语 | 参数含义、默认值、返回字段 |

脚本行为纪律：

- **先探活再干活**：服务器不可达立刻报错退出，不要提交任务后长等。
- **参数静默失效要报错**：拿不到落点的参数默认抛 `UnappliedOverrideError`（`--allow-unapplied` 可放行）。
- **判据用解码像素，不用文件哈希**：ComfyUI 会把执行图写进 PNG 的 `tEXt`，同像素也会哈希不同。

## 5. 技能文档不翻译

技能面向 Agent 执行，**只有中文版**；`tools/i18n.py` 已排除 `.dsh/skills/`、`skills/`、`skills/`。
但技能里**指向的仓库文档**（项目 README、SUMMARY 等）必须双语。
