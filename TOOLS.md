# TOOLS.md - 工具备忘

## 📁 文件交换（优先级排序）

### 1. 飞书云盘（首选）⭐
- **命令**: `lark-cli drive +upload/--file ./xxx` / `lark-cli drive +download`
- **用途**: 和用户交换文件的首选方式（上传图片、文档、结果文件等）
- **限制**: 单文件 ≤20MB；必须用相对路径（先 cd 到文件目录）

### 2. 飞书渠道 MEDIA: 协议
- **格式**: `MEDIA:/绝对路径`（独占一行）
- **用途**: 飞书聊天中直接发送图片
- **限制**: 仅飞书渠道有效

## 🖼️ 图片生成

### 即梦 Dreamina CLI
- **命令**: `dreamina`（`/home/luo/.local/bin/dreamina`）
- **UID**: 3994970165613146 / VIP: standard / 积分: 1050
- **文生图**: `dreamina text2image --prompt="..." --ratio=1:1 --resolution_type=2k --poll=0`
- **图生图**: `dreamina image2image --images ./x.png --prompt="..." --resolution_type=2k --poll=0`
- **⚠️ R-010 铁律**: 任务轮询规范——`--poll=0` 获取 submit_id → while 轮询 query_result → 下载后发一次图，详见 `references/dreamina-cli-usage.md`

### 聚鑫平台
- **文生图**: `gemini-3.1-flash-image-preview`
- **视频**: `veo3.1-fast-components`（8秒带音频）
- **前置**: 图生视频必须先上传图床，只传公网 URL

## 📋 飞书操作（lark-cli）

- **版本**: 1.0.3 / **应用**: cli_a9458646dc395bb3
- **用户**: 用户228040（ou_fb27c0df7ab68993f4273fc040a166c9）
- **Token**: 2小时有效，刷新7天，过期需 `lark-cli auth login`
- **常用命令**:
  - 云盘上传: `lark-cli drive +upload --file ./xxx`
  - 云盘下载: `lark-cli drive +download --file-token xxx --output ./xxx`
  - 读文档: `lark-cli docs +fetch --doc "URL或token"`
  - 日程: `lark-cli calendar +agenda`
  - 邮件: `lark-cli mail`
  - 任务: `lark-cli task`

## 🎬 AI漫剧流水线

### 阶段产出目录
```
{项目ID}/
├── 01-script.md            # 阶段1：视频脚本 + 结构化数据
├── 02-characters/          # 阶段2：角色卡
├── 03-scenes/              # 阶段3：场景卡
├── 04-storyboards/        # 阶段4：分镜方案
├── 05-audio/              # 阶段5：音频方案
└── 06-revisions/          # 阶段6：修改记录
```

### 即梦分镜时序图约束
- **镜头数量**：3个镜头横向排列较稳定，4个以上质量下降
- **时间标注**：AI随机生成，不可精确控制
- **多角色同镜**：效果差，建议每个镜头只放1个角色
