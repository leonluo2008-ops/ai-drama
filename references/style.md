# 风格锚点配置

## 使用方式

每个项目的风格锁定通过此文件定义。
脚本读取 `art_direction` 字段，注入到所有生成 Prompt 中。

## 字段说明

| 字段 | 说明 |
|------|------|
| art_direction | 主体艺术风格描述（AI 理解即可，不必是关键词堆砌）|
| color_palette | 色调关键词 |
| lighting | 光影关键词 |
| mood | 整体氛围 |
| composition | 构图偏好 |
| texture | 质感关键词 |

## 风格模板

```yaml
art_direction: {主体艺术风格描述}
color_palette: {色调关键词}
lighting: {光影关键词}
mood: {整体氛围}
composition: {构图偏好}
texture: {质感关键词}
```

**种族锁定规则**：由项目剧本和角色风格决定，详见 `references/character-style-guide.md`。不要擅自决定——先向创作者确认项目风格，再按规则执行。

---

## 修改记录（通用格式）

| 日期 | 修改内容 |
|------|---------|
| YYYY-MM-DD | {修改内容描述} |
