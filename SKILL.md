---
name: ai-drama
description: AI漫剧全流程制作总控。协调编剧→角色→场景→分镜→音频五个阶段，按流水线执行。触发词：漫剧、制作漫剧、开始制作。
category: ai-drama
version: 2.0-rebuild
---

# AI漫剧全流程制作 · 总控

## 系统架构

```
用户剧本
  ↓
Stage-1 编剧 → 视频脚本 + 角色表 + 场景表 + 场次表 + 风格锁定
  ↓ 用户确认
Stage-2 角色设计 → 角色卡 + 定妆照（跑图）
  ↓ 用户确认
Stage-3 场景设计 → 场景卡 + 场景图（跑图）
  ↓ 用户确认
Stage-4 分镜导演 → 分镜图 + 视频Prompt + 音效Prompt + 台词Prompt
  ↓ 用户确认
Stage-5 音频设计 → TTS脚本 + BGM提示词
  ↓ 用户确认
Stage-6 迭代修正（按需）
```

**工具调用统一出口**：`scripts/` 目录下的Python脚本，Skill不写CLI命令。

---

## 全局约束

| 约束 | 说明 |
|---|---|
| 片段时长 | 每场（scene）固定 15 秒，一集 = 多个场次串联 |
| 场次切分 | Stage-1 必须输出场次表（场次编号 + 场景 + 时长 + 出场角色） |
| 台词切分 | 以 3.5字/秒 为基准，≤15秒为一组 |
| 风格锁定 | Stage-1 产出，后续所有阶段必须遵守 |
| 用户确认 | 每个Stage完成后必须暂停，等用户确认再继续 |
| 角色指代 | 所有Prompt中使用外观全称，不使用角色名字 |
| 禁止跳过Stage | 必须按顺序执行，Stage-1 未完成不得进入 Stage-4 |

---

## Stage-1：编剧

**输入**：用户原始剧本（纯文本）

**执行**：
1. 加载 `references/stage1-script.md` 获取编剧Prompt模板
2. 按模板执行剧本→视频脚本的转化
3. 提取角色表、场景表、场次表、风格锁定

**输出**：
- 视频脚本（含镜头切换、动作补充、情绪标注）
- 角色表（含外观全称）
- 场景表
- 场次表（每场15秒）
- 风格锁定

**阶段产物文件**：`projects/{项目名}/01-script.md`

---

## Stage-2：角色设计

**输入**：Stage-1产出的角色表 + 风格锁定

**执行**：
1. 加载 `references/stage2-character.md` 获取角色设计Prompt模板
2. 为每个角色生成角色卡
3. 调用 `scripts/dreamina_generate.py` 生成定妆照
4. 发送到飞书等待用户确认

**脚本调用**：
```bash
python scripts/dreamina_generate.py \
  --type character \
  --project "{项目名}" \
  --character "{角色名}" \
  --face_prompt "{面部Prompt}" \
  --outfit_prompt "{服装Prompt}" \
  --ratio 1:1
```

**输出**：
- 角色卡（含外观全称、参考素材清单）
- 定妆照（用户确认后归档）

**阶段产物文件**：`projects/{项目名}/02-characters/`

---

## Stage-3：场景设计

**输入**：Stage-1产出的场景表 + 风格锁定

**执行**：
1. 加载 `references/stage3-scene.md` 获取场景设计Prompt模板
2. 为每个场景生成场景卡
3. 调用 `scripts/dreamina_generate.py` 两阶段生成：大场景全景图 → 多角度场景图
4. 发送到飞书等待用户确认

**脚本调用**：
```bash
# 第一阶段：大场景全景图
python scripts/dreamina_generate.py \
  --type scene \
  --project "{项目名}" \
  --scene "{场景名}" \
  --prompt "{场景Prompt}" \
  --ratio 1:1

# 第二阶段：多角度场景图（基于第一阶段结果）
python scripts/dreamina_generate.py \
  --type scene_multi \
  --project "{项目名}" \
  --scene "{场景名}" \
  --source "{大场景图路径}" \
  --ratio 1:1
```

**铁律**：场景图必须为空场景，禁止出现故事角色。

**输出**：
- 场景卡（含环境描述、视觉要素、角度索引）
- 大场景全景图 + 多角度场景图

**阶段产物文件**：`projects/{项目名}/03-scenes/`

---

## Stage-4：分镜导演

**输入**：Stage-1的视频脚本 + Stage-2的角色卡 + Stage-3的场景卡

**执行**：
1. 加载 `references/stage4-storyboard.md` 获取分镜导演Prompt模板
2. 分析叙事类型，推荐叙事路径（等用户确认）
3. 编排分镜方案（等用户确认）
4. 生成宫格图（调用 `scripts/dreamina_generate.py` 逐格生成 + `scripts/stitch_grid.py` 拼合）
5. 基于确认后的宫格图，输出视频Prompt + 音效Prompt + 台词Prompt

**脚本调用**：
```bash
# 逐格生成
python scripts/dreamina_generate.py \
  --type storyboard_panel \
  --project "{项目名}" \
  --panel "{格编号}" \
  --prompt "{分镜Prompt}" \
  --ratio 16:9

# 拼合宫格图
python scripts/stitch_grid.py \
  --project "{项目名}" \
  --panels "{格1路径},{格2路径},..." \
  --layout "3x3" \
  --output "{输出路径}"
```

**输出**：
- 分镜图（宫格图）
- 视频Prompt（Seedance 2.0格式，按六要素）
- 音效Prompt（时间轴对齐）
- 台词Prompt（时间轴对齐）

**阶段产物文件**：`projects/{项目名}/04-storyboards/`

---

## Stage-5：音频设计

**输入**：Stage-1的视频脚本 + Stage-4的分镜方案

**执行**：
1. 加载 `references/stage5-audio.md` 获取音频设计Prompt模板
2. 提取台词，生成TTS脚本（含时间轴）
3. 审查分镜阶段音效Prompt是否完整
4. 生成BGM提示词（供MiniMax Music 2.6使用）

**输出**：
- TTS脚本（含角色、外观全称、时间轴、情绪标注）
- BGM提示词（分段，含情绪弧线）

**阶段产物文件**：`projects/{项目名}/05-audio/`

---

## 角色更新流程（参考图驱动）

**触发条件**：用户提供了角色的参考图，要求按参考图更新角色形象。

**执行**：

### Step-1 分析参考图
用 `mcp_zai_analyze_image` 分析参考图，提取：
- 发型（造型/刘海/发色）
- 脸型
- 眼睛（眼型/眼神）
- 肤色
- 服装（上衣/下装/鞋/配饰/道具）
- 气质/风格

### Step-2 更新Prompt
1. 读取 `references/style.md` 获取当前项目的风格标签（`art_direction`字段）
2. 更新面部Prompt：参考图特征 + 风格标签叠加
   - 从参考图分析结果中提取面部特征描述
   - 拼接 `art_direction` 中的风格标签
3. 更新服装Prompt：采用参考图同款服装
   - 完整保留参考图中的服装描述（上衣+下装+配饰等）
   - 拼贴风格标签

### Step-3 重新生成
按以下顺序重新生成，生成一张确认一张：
1. 新面部图（文生图 or 图生图，取决于参考图质量）
2. 新服装图（文生图，俯视平铺）
3. 新六视图（图生图，参考图=面部+服装）

### Step-4 发送确认
发送以下内容到飞书：
- 参考图原图
- 新面部图
- 新服装图
- 新六视图

等待用户确认后归档。

**注意**：
- 参考图风格与目标风格可能不一致（如参考图是写实，目标是像素风）：以参考图的「角色身份特征」为准，风格标签由 `style.md` 提供，两者叠加
- 服装描述必须完整包含参考图中所有可见元素，不能遗漏配饰/道具
- 六视图Prompt中服装描述须与新服装图完全一致

---

## Stage-6：迭代修正

**触发条件**：用户对某一阶段的产出提出修改意见

**执行**：
1. 定位需要修改的阶段
2. 加载对应stage参考文档
3. 仅重新执行受影响的部分
4. 其他阶段保持不变

---

## 项目文件结构

```
projects/{项目名}/
├── 01-script.md           # Stage-1：视频脚本 + 角色表 + 场景表 + 场次表 + 风格锁定
├── 02-characters/         # Stage-2：角色卡 + 定妆照
├── 03-scenes/            # Stage-3：场景卡 + 场景图
├── 04-storyboards/       # Stage-4：分镜图 + 各类Prompt
├── 05-audio/             # Stage-5：TTS脚本 + BGM提示词
└── 06-revisions/         # Stage-6：修改记录
```

---

## 执行日志规范

每个Stage开始/结束时，打明确日志：

```
【Stage-N：阶段名称】开始
  输入：{具体输入内容}
  风格锁定：{如有}
  → 产出：{预期产出描述}
【Stage-N：阶段名称】完成，耗时 {N}s
```

---

## 调试模式

当用户说「调试分镜」「debug」时：
1. 读取当前项目目录下最新的 `06-revisions/` 修改记录
2. 汇报：当前卡点、评估结果、待解决问题
3. 等用户指令：继续调试 / 修改方案 / 跑测试
