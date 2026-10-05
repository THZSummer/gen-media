# 版本控制与协作

> 返回 [SKILL.md](../SKILL.md)

## 1. 仓库关系

| 仓库 | 位置 | 角色 |
|------|------|------|
| **gen-media** | github.com/THZSummer/gen-media（公开） | **唯一内容源头**：图片、视频、文档、站点、工具 |
| **gits** | gitee.com/thz_summer/gits（私有） | 工作区仓库，通过 submodule 引用 gen-media |

`gits` 的 `.gitmodules`：

```ini
[submodule "GitHub/gen-media"]
	path = GitHub/gen-media
	url = git@github.com:THZSummer/gen-media.git
	branch = main
```

`gits` 里 `Book/image-gen`、`Book/video-gen` 的内容与历史**已移除**（因为 Gitee 单仓 1 GB 配额），本地工作副本也已删除。
所以：**gen-media 是这些内容的唯一副本，别在 gits 里重建同名目录。**

## 2. submodule 指针纪律（最常忘的一条）

`gitlink` 是"钉住某个提交"，不是活指针。在 gen-media 里推了新内容，`gits` 不会自动跟上：

```sh
# 1) 先在 gen-media 提交推送
cd GitHub/gen-media && git add -A && git commit -m "..." && git push

# 2) 回 gits 推进指针
cd ../..    # → gits 根
git submodule update --remote GitHub/gen-media
git add GitHub/gen-media
git commit -m "chore(submodule): gen-media → <sha>"
git push
```

判断是否落后：`git submodule status` 前面出现 `+` = 固定提交与检出 HEAD 不一致。

## 3. 配额与体积

- **Gitee 社区版单仓 1 GB**：超限会拒推，需要跑 Repository GC。因此大体积内容只放 GitHub。
- `gits` 当前约 990 MB（历史里仍有旧对象），**不要再往 gits 提交大文件**。
- gen-media 约 550 MB；单文件上限 100 MB，不用 Git LFS。

## 4. 提交信息

- 用中文，写清「**做了什么 + 验证证据**」；一处改动一个主题。
- 涉及数据/计数时，把核对结果写进去（例如"缺英文版 286 → 0；疑似未翻译 0；断链 0"）。
- 不虚报：数字（计数/体积/评分）必须与实践一致；拿不到的证据标注"未验证"，不要编造。
- 修 bug 时写清**根因**与**复现/验证方式**，别只写"修复了问题"。

## 5. 网络与环境注意

- 本机 `/etc/ssh/ssh_config.d/` 属主异常，git 走 ssh 需要 `-F /dev/null`（各检出已配 `core.sshCommand`）。
- `raw.githubusercontent.com` 在本网络被 RST；`github.io` 的 `.108`/`.109` 边缘可能超时（见 [site.md](site.md)）。
- 云端 `arkcli` 需要可写的 `$HOME`；在受限沙箱里会因无法创建状态目录而失败 —— 这类命令交由用户在本机终端执行。
