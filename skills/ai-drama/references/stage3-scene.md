# Stage-3 参考：场景设计

## 输入

- Stage-1产出的场景表
- Stage-1产出的风格锁定

## 核心铁律

**场景图必须为空场景，禁止出现故事角色。**

- ✅ 正确：生成纯场景背景，无人
- ❌ 错误：场景中出现了主角、配角、故事角色
- ⚠️ 唯一例外：场景氛围所需的背景群众（如餐厅服务员、街道行人）可以作为氛围元素出现，但不能占主导

**违反此规则会导致：角色外观与场景合成后出现重复穿帮。**

## 两阶段场景生成

### 阶段A：大场景全景图（文生图）

**Prompt结构**：
```
[风格锁定], [场景描述], [时间/天气], [氛围关键词],
Pixel Art style, cyberpunk city night, pixelated urban environment,
俯视广角构图, high-saturation neon colors, blocky pixel brushstrokes,
NO HUMANS NO CHARACTERS, no people, empty scene, detailed environment, high detail
```

**关键约束**：
- 必须包含 `NO HUMANS NO CHARACTERS`
- 必须包含 `empty scene`

### 阶段B：多角度场景图（图生图，基于大场景全景图）

**Prompt结构**：
```
根据图像1中的场景，生成一张2×2多角度场景参考图，
左上：平视中景，展示家具高度与空间尺度，
右上：仰视天花板/顶部，展示顶部建筑设计与灯光细节，
左下：近景特写，展示材质纹理与道具细节，
右下：俯视鸟瞰，展示空间平面布局与动线。
NO HUMANS NO CHARACTERS，禁止出现任何人物。
保持Pixel Art风格，霓虹光影，块状像素笔触。不要出现文字。
```

## 场景卡格式

```markdown
## 场景卡：[场景名]

### 环境描述
[详细的环境描写]

### 视觉要素
- 地形/建筑：
- 光照：
- 色调：（与风格锁定一致）
- 氛围粒子（如有）：

### 场景角度索引
| 角度 | 描述 | 适用场景 |
|---|---|---|
| 平视中景 | 展示空间尺度 | 对话、常规叙事 |
| 仰视 | 展示顶部设计 | 权威感、压迫感 |
| 近景特写 | 展示材质道具 | 道具特写、细节互动 |
| 俯视鸟瞰 | 展示平面布局 | 大场面、角色入场 |

### 参考素材
| 素材 | 用途 | 状态 |
|---|---|---|
| 大场景全景图 | 多角度图生图输入 | 用户上传/待生成 |
| 多角度场景图 | 分镜参考图 | 待生成 |
```

## 脚本调用

**第一阶段：大场景全景图**
```bash
python scripts/dreamina_generate.py \
  --type scene \
  --project "{项目名}" \
  --scene "{场景名}" \
  --prompt "{场景Prompt（含NO HUMANS约束）}" \
  --ratio 1:1
```

**第二阶段：多角度场景图**
```bash
python scripts/dreamina_generate.py \
  --type scene_multi \
  --project "{项目名}" \
  --scene "{场景名}" \
  --source "{大场景图路径}" \
  --ratio 1:1
```

## 用户上传场景图的处理

如用户提供了场景参考图：
1. 直接作为大场景全景图使用
2. 只需执行阶段B生成多角度图
3. 确认大场景图满意后再生成多角度图
