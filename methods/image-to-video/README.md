# 图生视频（Image-to-Video）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 输入：首帧/尾帧图片 + prompt。输出：图片"动起来"的视频。
> 返回[方法总览](../README.md) ｜ 适用模型：Seedance 系列（I2V 路径）

---

## 一、主题定位

图生视频是**用静态图片驱动动态**的路径：手里有一张现成图（产品图、海报、关键帧、AI 生成的静图），想让它产生合理的运动。相比 T2V，I2V **画面起点确定**，控制力强得多，是商业产出最常用的路径。

### 何时选 I2V

- 已有产品图/插画，要做成动态广告
- 用 seedream 先生成满意静图，再让它动起来（图+视频两段式最稳）
- 关键帧驱动：设计好起止画面，让模型补中间运动
- 海报、封面动态化

### 何时不选

- 完全没有图、只想从文字试 -> [text-to-video](../text-to-video/README.md)
- 想复刻某段现成视频的运动 -> [reference-video](../reference-video/README.md)

---

## 二、能力映射

| 控制维度 | I2V 下的手段 |
|----------|-------------|
| 起点画面 | 首帧图（强约束） |
| 终点画面 | 尾帧图（可选，`last:` 前缀） |
| 运动方式 | prompt 描述运动 + `--camera-fixed` |
| 主体一致性 | 首帧锁定主体，比 T2V 稳定得多 |
| 多图参考 | 多张 `--input`，第一张为首帧，其余为参考 |

### 两种典型用法

```
A) 单首帧：静图 -> 动起来
   arkcli +gen --model $M --input @first.jpg "镜头缓慢拉远"

B) 首尾帧：起点 + 终点 -> 模型补间
   arkcli +gen --model $M --input first:@a.jpg --input last:@b.jpg "从A平滑过渡到B"
```

---

## 三、首帧/尾帧策略

### 单首帧（最常用）

- 第一张 `--input` 默认就是首帧
- prompt 重点描述**运动**而非主体外观（外观已被图锁定）
- 好的 prompt：`"镜头缓慢拉远，主体保持不动，背景云层流动"`
- 差的 prompt：`"一个穿红衣的少年"`（外观已由图给定，重复描述反而干扰）

### 首尾帧（补间动画）

- 用 `first:` / `last:` 显式标注，避免歧义
- 适合**过渡镜头**：表情变化、物体变形、场景转换
- 两帧差异过大 -> 中间会出现扭曲/跳变，建议两帧主体构图一致

### 多图参考

- 第一张 = 首帧；其余图默认作为参考图（非首帧）
- 想让某张图只作参考不作首帧：用 `ref:` 前缀

```bash
# 第一张首帧，第二张仅参考风格
arkcli +gen --model "$MODEL" \
  --input @subject.jpg --input ref:@style.jpg \
  "主体保持，背景切换为参考图的水彩风格"
```

---

## 四、两段式工作流（强烈推荐）

I2V 最稳的产出方式是 **seedream 生图 -> seedance 生视频**：

```
1) seedream 生成满意静图（图片便宜、可反复调）
   arkcli +gen --model doubao-seedream-5-0-260128 --size 1920x1920 "..." 
   -> 得到 first.jpg

2) seedance 用静图当首帧生成视频
   arkcli +gen --model $MODEL --input @first.jpg "镜头缓慢推近" --open
```

**为什么推荐**：
- 图片生成快（几秒）、便宜，可反复迭代直到画面满意
- 视频生成慢、贵，用确定的好图驱动，一次成功率远高于纯 T2V
- 主体一致性大幅提升

---

## 五、参数选型

| 参数 | I2V 建议 | 说明 |
|------|----------|------|
| `--input` | `@first.jpg` 或 `first:@a.jpg last:@b.jpg` | 必填，没有图就不叫 I2V |
| `--ratio` | 与首帧图比例一致 | 不一致会被裁切/拉伸 |
| `--resolution` | 匹配首帧图清晰度 | 低图配高分辨率无意义 |
| `--camera-fixed` | 静态构图时用 | 防止模型自作主张运镜 |
| `--return-last-frame` | 续接长视频时用 | ⛔ mini 不返回，改两段式 I2V（另见 [long-video-chain](../long-video-chain/README.md)） |
| `--draft` | 试运动方向时用 | ⛔ mini 不支持，用 480p 替代 |

---

## 六、命令模板

```bash
# 补全模型 ID
VER=$(arkcli models get doubao-seedance-2-0 --transform 'primary_version' | tr -d '"')
MODEL="doubao-seedance-2-0-${VER:-260128}"

# 1) 单首帧：静图动起来
arkcli +gen --model "$MODEL" \
  --input @product.jpg --ratio 16:9 --resolution 720p \
  "镜头缓慢拉远，产品居中，背景纯色渐变光影流动" --open

# 2) 首尾帧补间
arkcli +gen --model "$MODEL" \
  --input first:@start.jpg --input last:@end.jpg \
  "表情从微笑自然过渡到大笑" --open

# 3) 两段式：先图后视频
arkcli +gen --model doubao-seedream-5-0-260128 \
  --size 1920x1080 "赛博朋克街道全景，雨夜，霓虹" --open
# (满意后)
arkcli +gen --model "$MODEL" --input @ark-gen.jpeg \
  "镜头向前推进，雨滴落下，霓虹闪烁" --open

# 4) 续接：拿到上一条最后一帧作下一条首帧
arkcli +gen --model "$MODEL" --return-last-frame \
  --input @first.jpg "镜头向右摇" --open
```

---

## 七、踩坑点

| 现象 | 原因 | 处理 |
|------|------|------|
| 首帧被改得面目全非 | prompt 过度描述外观 | prompt 只写运动，外观交给图 |
| `--ratio` 与图不匹配 | 裁切/拉伸 | 让 ratio 等于原图比例 |
| 多图时首帧选错 | 默认第一张为首帧 | 显式 `first:` `last:` `ref:` 标注 |
| 尾帧补间扭曲 | 两帧差异太大 | 保持两帧构图/主体一致 |
| 低清图配 1080p | 放大无细节 | 分辨率匹配素材质量 |
| 非图扩展名被丢 | `--input` 按扩展名分流 | 确认传的是图片文件 |

---

## 八、检查清单

- [ ] 首帧图质量足够（清晰、构图合理）
- [ ] `--ratio` 与首帧图一致
- [ ] 多图时用 `first:`/`last:`/`ref:` 显式标注角色
- [ ] prompt 只描述运动，不重复外观
- [ ] 静态构图加 `--camera-fixed`
- [ ] 优先用两段式（图+视频）而非纯 T2V
- [ ] 续接场景加 `--return-last-frame`

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-07-18 | v1.0 | 初始主题规划 | 小七 |
| 2026-07-18 | v1.1 | 标注 --draft/--return-last-frame mini 不支持 | 小七 |
