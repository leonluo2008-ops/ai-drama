# AI漫剧制作工具链

把剧本创意转化为完整的漫剧制作方案，协调5个专业工种按流水线执行。

## 架构

```
用户剧本
    ↓
[编剧] → 视频脚本 + 角色表 + 场景表 + 场次表 + 风格锁定
    ↓
[角色设计师] → 角色卡 + 定妆照prompt
    ↓
[场景设计师] → 场景卡 + 大场景/多角度prompt
    ↓
[分镜导演] → 分镜图prompt + 视频prompt + 音效prompt + 台词prompt
    ↓
[音频设计师] → BGM提示词 + TTS脚本
    ↓
迭代优化
```

## Skill列表

| Skill | 路径 | 职责 |
|-------|------|------|
| 总控 | `skills/ai-drama/SKILL.md` | 流水线调度、阶段切换 |
| 编剧 | `skills/ai-drama-script/SKILL.md` | 剧本→视频脚本→提取角色/场景/场次 |
| 角色设计 | `skills/ai-drama-character/SKILL.md` | 角色卡 + 定妆照prompt |
| 场景设计 | `skills/ai-drama-scene/SKILL.md` | 场景卡 + 大场景/多角度prompt |
| 分镜导演 | `skills/ai-drama-storyboard/SKILL.md` | 分镜编排 + 视频/音效/台词prompt |
| 音频设计 | `skills/ai-drama-audio/SKILL.md` | BGM提示词 + TTS脚本 |

## 关键约束

- **视频片段固定15秒**（Seedance标准时长规格）
- **台词优先切分**：台词朗读时间（~3-4字/秒）+ 动作/停顿 ≤ 15秒
- **风格锁定**：阶段1产出，后续阶段只消费不修改
- **用户确认是硬卡点**：每个阶段完成后暂停

## 使用的外部工具

| 工具 | 用途 |
|------|------|
| Dreamina CLI | 即梦AI图片生成（定妆照、场景图、分镜图） |
| Seedance 2.0 | AI视频生成（图生视频） |
| 聚鑫平台 | 文生图 / 视频生成备选 |

## 项目结构

```
├── skills/                 # 6个专业skill
├── references/             # 参考资料（分镜方法论、prompt模式等）
├── projects/               # 按项目组织产出
│   └── {项目ID}/
│       ├── 01-script.md
│       ├── 02-characters/
│       ├── 03-scenes/
│       ├── 04-storyboards/
│       ├── 05-audio/
│       └── 06-revisions/
├── AGENTS.md               # Agent总控配置
├── SOUL.md                 # 身份定义
└── TOOLS.md                # 工具备忘
```

## 参考资料

- `references/storyboard-methodology.md` — 分镜方法论（从Notion案例提炼）
- `references/SEEDANCE_VIDEO_PROMPT_GUIDE.md` — Seedance视频prompt规范
- `references/PROMPT_PATTERNS.md` — prompt模式参考
- `references/notion-storyboard-reference.md` — Notion分镜案例参考

## 状态

🧪 实验阶段。已完成1个测试项目（婆婆五十大寿），正在调试Seedance视频生成参数问题。
