---
name: seedance-director-mode
description: Seedance 2.0 导演模式完整指南 — 提示词结构、@-Tag用法、多镜头工作流和素材准备。触发词：导演模式、Seedance提示词、视频分镜、AI视频创作
category: video
tags: [seedance, AI视频, 导演模式, 提示词, 分镜]
version: 1.0
created: 2026-05-20
updated: 2026-05-20
inputs:
  - topic (string, required): 想要的方向 — 结构学习/模板参考/素材清单
outputs:
  - 完整导演模式使用指南（按需输出不同部分）
---

# Seedance 2.0 导演模式使用指南

## 核心定位

Seedance 2.0 = **虚拟导演 + 摄影师**，不是绘图工具。

模型需要的不是「美丽的描述」，而是**分镜脚本**。

**普通提示词失效原因**：写"美丽的日落，一个女孩走在海滩上"——模型随便做，但不是你想要的。

**导演模式正确姿势**：回答镜头语言的所有问题——机位、速度、景别、光源、环境音。

---

## 一、提示词结构（六要素）

严格按顺序写，训练数据就是按此组织：

| 顺序 | 要素 | 作用 | 示例 |
|---|---|---|---|
| 1 | Subject（主体） | 焦点是谁/什么 | A female warrior in black tactical bodysuit |
| 2 | Action（动作） | 具体在做什么 | delivers a powerful roundhouse kick |
| 3 | Environment（环境） | 在哪发生 | abandoned neon-lit industrial factory |
| 4 | Camera（运镜） | 镜头怎么动 | dramatic side-angle tracking shot |
| 5 | Style（风格） | 视觉美学 | cinematic action movie style like John Wick |
| 6 | Lighting/Mood（光/氛围） | 光线和情绪 | golden hour backlighting mixed with blue neon |

**四步法（简化版）**：①说主体 → ②描述场景 → ③镜头运动 → ④控制节奏

---

## 二、@-Tag 文件引用系统

最多同时输入 12 个文件：
- 最多 9 张图片
- 最多 3 段视频（总时长 ≤15 秒）
- 最多 3 个音频文件（每个 ≤15 秒）

### 常用 @-Tag 指令

| 想要的效果 | 提示词写法 |
|---|---|
| 设置视频第一帧 | `@Image1 as the first frame` |
| 锁定角色外观 | `@Image2 for character appearance` |
| 视觉风格参考 | `@Image3 as style reference` |
| 复制镜头运动 | `Reference @Video1 for camera movements and transitions` |
| 替换视频中的人物 | `Replace the person in @Video1 with @Image1` |
| 多帧连续镜头 | `@Image1 through @Image5` |

**原则**：角色描述越具体越好。`@Image1 as reference` ❌ → `@Image1 as character's face and clothing` ✅

---

## 三、多镜头时间线写法

```
[00–05s] Shot 1: 特写 — 女孩脸部表情
[05–10s] Shot 2: 全景 — 她冲出工厂大门
[10–15s] Shot 3: 升格 — 爆炸，火光充满画面
```

模型按时间顺序生成连续镜头。

---

## 四、运镜术语（直接用）

- tracking shot — 摄像机跟随主体
- dolly zoom — 后退+镜头推进（眩晕效果）
- shallow depth of field — 背景虚化
- anamorphic lens — 宽银幕光晕镜头
- golden hour backlighting — 日落逆光
- 360° rotation — 360度旋转
- steady tracking shot — 平稳跟拍
- push in / pull out — 推进/拉远

---

## 五、素材准备清单

### 必须准备
- 🎯 **主体图片**：角色正脸/全身，锁定外观
- 🎬 **首帧图片**：视频第一帧（可选但推荐）
- ✍️ **提示词**：按六要素写的分镜脚本

### 可选准备
- 🌄 **风格参考图**：色调/光感/视觉风格
- 📹 **运镜参考视频**：镜头运动示例
- 🎵 **音频文件**：MP3，最长15秒
- 🖼️ **尾帧图片**：最后一帧（做循环时尤其重要）

### 省成本技巧
先用 Seedance 1.5 或图片模式测试分镜构图，确认无误再正式生成。

---

## 六、爆款提示词模板

### ① 电影感动作场景
```
@Image1 as first frame and character reference, @Image2 as environment style.
A female warrior in black tactical bodysuit stands in the center of an abandoned neon-lit industrial factory. She delivers a powerful roundhouse kick sending an enemy flying, then seamlessly transitions into precise one-handed handgun fire with bright muzzle flashes. Dramatic side-angle tracking shot with dynamic camera shake, cinematic action movie style like John Wick, realistic physics and gravity, golden hour backlighting mixed with blue neon, 1080p, ultra-smooth motion.
```

### ② 病毒式无缝循环
```
@Image1 as the product (first and last frame).
A perfect sphere of liquid mercury sits on a mirror surface in a minimalist studio. It slowly deforms under invisible force into a perfect cube, then smoothly morphs back into a sphere. Reflections shift realistically, extreme macro close-up, seamless loop-ready motion, ASMR-satisfying aesthetic, clean white background with soft directional lighting, high-end commercial style.
```

### ③ 情感故事多镜头
```
@Image1 as main character appearance, @Image2 as location style.
A young man (@Image1) comes home tired after work, walks down a warm hallway, stops at the door, takes a deep breath and smiles. Close-up of his face relaxing, then his daughter and dog run to hug him. One continuous tracking shot, cozy home interior, cinematic family drama style like "The Pursuit of Happyness", soft natural window light, gentle camera movement, native warm ambient sound.
```

### ④ 高端产品广告
```
@Image1 as the product reference.
Premium wristwatch floats and slowly rotates in mid-air against pure black background. Water droplets suspended around it catch dramatic spotlight like diamonds. Extreme macro details on every texture and reflection, high-end jewelry commercial aesthetic, ultra-smooth 360° rotation, Apple-level cinematic quality.
```

### ⑤ 超现实梦境
```
@Image1 as person, @Image2 as doorway style.
A person walks through a normal doorway and steps into an impossible M.C. Escher landscape where staircases go upside down and gravity shifts. Floating dust particles catch golden light shafts, smooth steady tracking shot following the walker, dreamlike ethereal atmosphere, Christopher Nolan's Inception meets Studio Ghibli style.
```

### ⑥ 前后对比 Transformation
```
@Image1 as starting object, @Image2 as final object.
Split-screen: left side shows ordinary plain coffee mug on desk, right side dramatically transforms the same mug into an ornate golden chalice with jewels and glowing effects. Satisfying swipe transition, dramatic before-after reveal, clean studio lighting, viral transformation trend style, fast-paced editing.
```

### ⑦ 赛车/动作多镜头时间线
```
Style: Hollywood professional racing movie (Le Mans style), cinematic night, heavy rain.
[00–05s] Veteran driver in helmet looks focused, rain lashes windshield.
[05–10s] Rival car next to him, adrenaline in eyes.
[10–15s] Green light — both cars accelerate on wet track, water sprays into camera, motion blur on stadium lights.
```

---

## 七、爆款算法关键词

提升平台推荐率的词：

- `seamless loop-ready motion` — 无缝循环
- `satisfying ASMR` — 舒缓催眠感
- `before-after transformation` — 前后对比
- `fast-paced editing` — 快节奏剪辑
- `viral transformation trend style` — 社交流行趋势

**必须避免**：「有点」「大概」「某种」「美丽的」——模型无法猜测。
❌ `beautiful light` → ✅ `soft golden hour backlighting`

---

## 八、工作流总结

```
Step 1: 明确视频主题和主体
Step 2: 按六要素结构写提示词
Step 3: 准备 @-Tag 素材（角色图、风格参考、首帧图）
Step 4: 组合进 Seedance 2.0（先用1.5测试分镜）
Step 5: 生成 + 检查首帧/尾帧/运镜是否符合预期
Step 6: 如需多镜头，用时间线语法重新生成
```
