# TOOLS.md - 工具备忘

## 📁 文件交换（唯一默认方式）⭐

### 发送文件给用户 → `message` 工具 + `filePath`

**所有类型文件**（图片、文档、视频、音频等）统一使用此方式：

```
message(action="send", filePath="/absolute/path/to/file", message="说明文字")
```

**适用场景**：
- 图片（png/jpg/webp）
- 文档（pdf/docx/xlsx）
- 视频（mp4/mov）
- 音频（mp3/wav）
- 任何本地文件

**禁止使用的方式**：
- ❌ 飞书云盘链接（默认私有权限，用户无法访问）
- ❌ `MEDIA:/path` 协议（仅作为最后备选）
- ❌ `lark-cli drive +upload`（除非用户明确要求上传到云盘）

**用户已明确反馈**：云盘链接无法访问，直接发送文件才可靠。

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
