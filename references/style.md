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

## 当前项目风格

```yaml
art_direction: 摄影级写实人像，亚洲面孔，电影质感，光影细腻，高细节，2K分辨率
color_palette: 自然色调，暖调背景，肤色真实
lighting: 电影布光，伦勃朗光，自然眼神光，柔和阴影
mood: 电影质感，氛围感强，叙事感
composition: 中景构图为主，兼顾特写
texture: 皮肤纹理清晰，真实感强，无过度美化
quality: 8K超高细节，RAW格式质感
```

**铁律：所有角色 prompt 必须以 Asian Chinese 开头，强调亚洲中国人种。**

---

## 修改记录（通用格式）

| 日期 | 修改内容 |
|------|---------|
| YYYY-MM-DD | {修改内容描述} |
