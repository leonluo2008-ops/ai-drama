# 飞书文件发送规范

> 适用于：所有通过 OpenClaw + 飞书渠道与用户交互的 Agent

## 核心规则

**发送文件给用户，统一使用 `message` 工具的 `filePath` 参数。**

这是唯一默认且可靠的文件传输方式。图片、文档、视频、音频，所有类型都一样。

## 调用方式

```
message(action="send", filePath="/absolute/path/to/file.ext", message="简短说明文字")
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `action` | 是 | 固定为 `"send"` |
| `filePath` | 是 | 文件的**绝对路径**（如 `/home/user/output/result.png`） |
| `message` | 否 | 伴随文件的说明文字 |

### 支持的文件类型

| 类型 | 格式示例 | 效果 |
|------|---------|------|
| 图片 | `.png` `.jpg` `.webp` `.gif` | 聊天中直接显示图片 |
| 文档 | `.pdf` `.docx` `.xlsx` `.pptx` | 以文件卡片形式发送 |
| 视频 | `.mp4` `.mov` | 以视频卡片形式发送，可在线播放 |
| 音频 | `.mp3` `.wav` | 以音频卡片形式发送 |
| 其他 | 任意格式 | 以文件卡片形式发送，可下载 |

## 完整示例

### 发送图片

```json
message(
  action="send",
  filePath="/home/user/workspace/output/storyboard.png",
  message="🎬 分镜图已生成"
)
```

用户在飞书中直接看到图片，无需额外操作。

### 发送PDF文档

```json
message(
  action="send",
  filePath="/home/user/workspace/output/report.pdf",
  message="📊 项目报告"
)
```

### 发送视频

```json
message(
  action="send",
  filePath="/home/user/workspace/output/clip.mp4",
  message="🎥 视频片段"
)
```

## ⚠️ 其他方式（存在问题待解决）

以下方式目前有已知问题，**暂不作为默认发送方式**：

| 方式 | 问题 |
|------|------|
| `lark-cli drive +upload` + 云盘链接 | 默认私有权限，用户无法打开链接 |
| `feishu_drive_file upload` + 返回链接 | 同上，权限问题 |
| `MEDIA:/path` 协议 | 仅部分场景有效，不够稳定 |

> 这些方式并非不可用，而是需要解决权限/稳定性问题后才适合作为常规方案。当用户明确要求"上传到云盘"时可以正常使用。

## 工作流示例：生成文件后发送

```python
# 1. 生成本地文件（图片/视频/文档）
output_path = "/home/user/workspace/output/result.png"

# 2. 直接发送给用户
message(action="send", filePath=output_path, message="✅ 文件已生成")
```

## 注意事项

1. **使用绝对路径**：`filePath` 必须是完整绝对路径
2. **文件必须存在**：发送前确认文件已下载/生成到本地
3. **一次一个文件**：每次调用发送一个文件，多个文件多次调用
4. **说明文字简洁**：`message` 参数写简短描述即可

---

_本文档基于用户实际测试验证：2026-05-18_
