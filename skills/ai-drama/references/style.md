# 风格锚点配置

## 使用方式

每个项目的风格锁定通过此文件定义。
脚本读取 `art_direction` 字段，注入到所有生成 Prompt 中。

## 字段说明

- **art_direction**: 主体艺术风格描述（AI 理解即可，不必是关键词堆砌）
- **color_palette**: 色调关键词
- **lighting**: 光影关键词
- **mood**: 整体氛围
- **composition**: 构图偏好
- **texture**: 质感关键词
- **quality**: 质量规格

## 当前项目风格

```yaml
art_direction: Pixel Art style, cyberpunk city night aesthetic, blocky pixel brushstrokes
color_palette: high-saturation neon colors (red, blue, yellow, green), dark background with cold grays
lighting: neon light source, blocky gradient shadows, strong contrast between bright neon and dark areas
mood: bustling night city atmosphere, retro 8-bit digital art aesthetic, cold yet vibrant
composition: 俯视广角构图 preferred for scenes
texture: pixelated details, clear outlines, retro digital art质感
quality: high detail, 2k resolution
```

---

## 修改记录

| 日期 | 修改内容 |
|------|---------|
| 2026-05-20 | 初始化：Pixel Art + Cyberpunk 风格 |
