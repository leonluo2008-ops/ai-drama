# Stage-4 参考：分镜导演

## 输入

- Stage-1产出的视频脚本
- Stage-2产出的角色卡（含定妆照）
- Stage-3产出的场景卡（含场景图）

## 执行流程（必须按顺序执行）

```
⚠️ 重要：分镜是按「场次」逐场进行的，不是按整集。

Phase 0：确认场次表 → 选取本集第一场未分镜的场次 → ⏸ 等用户确认
Phase 1：分析本场 → 推荐叙事路径 → ⏸ 等用户确认
Phase 2：编排分镜 → 输出分镜方案 → ⏸ 等用户确认
Phase 3：生成宫格图 → 拼合 → 发送用户 → ⏸ 等用户确认
Phase 3.5：分镜描述 → 用户编辑调整 → ⏸ 等用户确认
Phase 4：输出Prompt → 视频Prompt + 音效Prompt + 台词Prompt

→ 循环 Phase 0~4，直到所有场次分镜完成
→ 全部场次完成后，Stage-4 结束，进入 Stage-5
```

**「场」的概念**：
- 1集 = 多个「场」（scene）串联
- 1「场」= 约15秒，包含1个或多个镜头
- 分镜的最小单位是「场」，不是整集

**Phase 0 等用户确认的内容**：
- 当前场次编号（例：第3场 / 共7场）
- 本场出场角色列表
- 本场场景描述
- 本场预计时长

## 叙事路径推荐

读完文稿后识别叙事类型，推荐对应路径：

| 路径 | 适用场景 | 叙事结构 | 镜头走向 |
|---|---|---|---|
| 戏剧冲突型 | 故事/剧情向 | 起势→冲突→余韵 | 远景开场→推进特写→高潮快切→定格 |
| 科普讲解型 | 知识科普/旁白驱动 | 提出问题→分析过程→结论 | 特写引出→中景展示→全景总结 |
| 氛围展示型 | 风景/产品/美食 | 远景引入→细节特写→全景收束 | 大场面→微距→鸟瞰 |
| 动作快切型 | 打斗/运动/高潮 | 快速推进→爆发顶点→定格冲击 | 快切→慢动作→定格 |
| 对话节奏型 | 人物对话/情感戏 | 建立关系→冲突/转折→和解/悬念 | 双人景→正反打→表情特写 |

## 时间切分原则

**每场固定15秒。**

```
步骤1：统计本场所有台词字数
步骤2：计算台词朗读时间 = 字数 ÷ 3.5
步骤3：计算画面填充时间 = 15秒 - 台词朗读时间
步骤4：将画面时间分配给非台词镜头
步骤5：验证 台词时间 + 所有镜头时间 = 15秒（允许±0.5s误差）
```

## Prompt分层结构（分镜图生成）

**三层架构**（避免逐格重复全局信息）：

```
第一层（全局声明，写一次）：
  Global: [角色外观] + [环境/氛围] + [风格]

第二层（逐格描述，只写差异）：
  Panel N (景别/叙事功能)：[画面内容]

第三层（尾部约束）：
  No text.
```

**示例**：
```
Global: A black ant with glossy chitin shell. Sunlit green meadow, warm golden side-backlighting, shallow depth of field. Ghibli illustration, hand-painted texture.
Panel 1 (close-up/opening): Standing alert on a withered orange leaf, antennae raised high, a small grey pebble nearby.
Panel 2 (medium/action): Marching with 3 others on dirt path, antennae swaying.
Panel 3 (wide/closing): Ant hill mound from above, late afternoon light casting long shadows.
No text.
```

## 宫格排列规范

**每格的画幅比例 = 最终视频比例。**

| 视频比例 | 推荐场景 |
|---|---|
| 16:9 | 短视频、B站、YouTube |
| 9:16 | 抖音、快手、小红书 |
| 1:1 | Instagram、朋友圈 |

**16:9 竖屏分镜宫格（纵向堆叠，避免超宽条）**：
| 格数 | 排列 | 总比例 | 即梦输出 |
|---|---|---|---|
| 1格 | 1×1 | 16:9 | 16:9 |
| 2格 | 2行1列 | 9:16 | 9:16 |
| 3格 | 3行1列 | 3:5 | 2:3 |
| 4格 | 2行2列 | 16:9 | 16:9 |
| 6格 | 3行2列 | 7:6 | 1:1 |
| 9格 | 3行3列 | 16:9 | 16:9 |

## 景别多样性检查（6格及以上必须包含）

- 至少1个特写（表情/关键道具）
- 至少1个远景（环境/大场面）
- 至少1个俯拍或仰拍
- 至少1个运动镜头

## Seedance 2.0 视频Prompt格式

**六要素顺序**：Subject → Action → Environment → Camera → Style → Lighting/Mood

```
15秒，[质量规格]，[角色外观描述]，[色调]，[特效类型]，运镜丝滑，无穿模，无文字。

0–Xs：
[景别][角度]，[角色外观全称] [动作微细节]，[运镜描述]，[光影/氛围细节]。

X–Ys：
[景别][角度]，[角色外观全称] [动作微细节]，[运镜描述]，[光影/氛围细节]。
```

## @-Tag 文件引用

| 用途 | @-Tag写法 |
|---|---|
| 设置视频首帧 | `@Image1 as the first frame` |
| 锁定角色外观 | `@Image2 for character appearance` |
| 视觉风格参考 | `@Image3 as style reference` |
| 场景环境参考 | `@Image4 as environment reference` |

## 音效Prompt格式

```
0～Xs：[空间层次]，[主要声源]，[声学细节]。
X～Ys：[空间层次]，[主要声源]，[声学细节]。
```

## 台词Prompt格式

```
0.0～Xs：【角色/旁白】："台词内容。"（约N字）
X～Ys：【角色/旁白】："台词内容。"（约N字）
```

## 分镜描述格式（Phase 3.5，用户创作界面）

```markdown
【场景】时间 + 地点 + 室内/室外

Panel 1 (0-Xs)：
角色（动作/表情）：“台词”
角色（内心OS）：“内心独白”

Panel 2 (X-Ys)：
角色（动作/表情）：“台词”

[收束指令，如：定格2秒余韵]
```

## 脚本调用

**逐格生成**：
```bash
python scripts/dreamina_generate.py \
  --type storyboard_panel \
  --project "{项目名}" \
  --panel "{格编号}" \
  --prompt "{分镜Prompt}" \
  --ratio 16:9
```

**拼合宫格图**：
```bash
python scripts/stitch_grid.py \
  --project "{项目名}" \
  --panels "{格1路径},{格2路径},..." \
  --layout "3x3" \
  --output "{输出路径}"
```

## 运镜词汇库

FPV贴地低掠 / 丝滑上移 / 极速贴合 / 360度环绕 / 急速拉升 / 高空俯瞰 / 慢镜头拉远 / 旋转推进 / 横向漂移 / 跟拍疾行 / 固定机位 / 慢推 / 慢拉
