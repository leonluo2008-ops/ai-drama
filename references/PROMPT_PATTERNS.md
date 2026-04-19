# AI视频/分镜提示词参考资料库

> 整理时间：2026-04-19
> 来源：全网搜索收集

---

## 一、优质参考资料来源

### 提示词库/工具
| 来源 | 链接 | 说明 |
|------|------|------|
| VlogPrompt | https://vlogprompt.com/ | Sora/Veo/Kling/即梦/可灵提示词库 |
| PromptArk VEO3 | https://promptark.net/zh/prompt-library/veo-3-prompts | VEO3最佳提示词模板 |
| CinePrompt | https://cineprompt.io/ | 结构化提示词构建器 |
| MagicHour Cookbook | https://magichour.ai/blog/cinematic-ai-video-prompt-cookbook | 25个 cinematic patterns |

### 分镜工具
| 来源 | 链接 | 说明 |
|------|------|------|
| AI-Flow Seedance | https://ai-flow.net/templates/storyboard-to-cinematic-video-with-seedance-2.0/ | 分镜→视频工作流 |
| soprompts | https://soprompts.com/tools/sora-storyboard | 15秒分镜脚本生成 |
| video2prompt | https://video2prompt.org/storyboard | 分镜→提示词转换 |
| Storyboarder.ai | https://storyboarder.ai/ | 剧本→分镜 |

---

## 二、MagicHour 25个 Cinematic Patterns

> 来源：https://magichour.ai/blog/cinematic-ai-video-prompt-cookbook

### Category I: Camera & Composition Patterns

#### 1. Static Cinematic Portrait
```
Medium close-up portrait of a young woman, centered composition, 85mm lens, 
shallow depth of field, soft natural lighting, clean background, cinematic look
```
**结构**: framing + lens + depth of field + lighting
**适用**: Talking photo, lipsync, headshot

#### 2. Slow Push-In Shot
```
Close-up of a man looking forward, camera slowly pushing in, maintaining 
sharp focus, shallow depth of field, cinematic lighting
```
**结构**: subject + camera movement + focus control
**适用**: 情感场景, 强调

#### 3. Over-the-Shoulder Shot
```
Over-the-shoulder shot from behind a character, foreground slightly blurred, 
subject in focus, natural indoor lighting, cinematic framing
```
**结构**: foreground subject + background focus + depth
**适用**: 对话, POV

#### 4. Wide Establishing Shot
```
Wide cinematic shot of a city street at sunset, subject walking in the distance, 
high environmental detail, soft golden lighting
```
**结构**: wide angle + environment + subject placement
**适用**: 场景介绍, 过渡

#### 5. Tracking Shot
```
Side tracking shot of a person walking through a busy street, camera moving 
smoothly alongside, stabilized motion, realistic pace
```
**结构**: subject motion + camera tracking + stabilization
**适用**: 运动场景

### Category II: Motion & Action Patterns

#### 6. Natural Walking Loop
```
Person walking forward at a natural pace, consistent stride, smooth body motion, 
realistic foot placement
```
**结构**: subject + repeated motion + rhythm consistency

#### 7. Object Interaction
```
Close-up of hands picking up a cup from a table, smooth motion, 
realistic hand movement, accurate physics
```
**结构**: subject + object + physical interaction
**适用**: 产品演示, 教程

#### 8. Crowd Movement
```
Crowd of people walking in different directions, varied pacing, no repetition, 
natural movement
```
**结构**: multiple subjects + varied motion + randomness
**适用**: 城市, 背景真实感

#### 9. Wind Dynamics
```
Character standing outdoors, hair and clothing moving naturally in the wind, 
subtle environmental motion
```
**结构**: subject + environmental force + reaction
**适用**: 户外场景

#### 10. Idle Micro-Movements
```
Character standing still with subtle breathing, slight head movement, 
natural blinking, realistic posture
```
**结构**: subject + subtle motion + facial detail
**适用**: 对话, close-ups

### Category III: Lighting Patterns

#### 11. Golden Hour Lighting
```
Outdoor scene during golden hour, warm sunlight, long shadows, 
soft highlights, cinematic color grading
```
**结构**: time of day + light direction + tone

#### 12. High Contrast Noir
```
Low key lighting, strong shadows, high contrast, dramatic mood, 
noir cinematic style
```
**结构**: low-key lighting + shadow emphasis

#### 13. Soft Studio Lighting
```
Soft studio lighting, even illumination, minimal shadows, 
clean subject visibility
```
**结构**: even lighting + minimal shadow
**适用**: 产品, headshots

#### 14. Neon Night Scene
```
Urban night scene with neon lights, reflections on wet surfaces, 
vibrant colors, cinematic atmosphere
```
**结构**: artificial light sources + reflections

#### 15. Backlit Silhouette
```
Strong backlight behind subject, partial silhouette, 
rim lighting outlining the figure
```
**结构**: strong backlight + subject outline
**适用**: 揭示,  dramatic shots

### Category IV: Environment & Depth Patterns

#### 16. Layered Depth Scene
```
Scene with clear foreground, midground, and background, 
strong depth separation, cinematic composition
```
**结构**: foreground + midground + background
**适用**: 复杂场景

#### 17. Atmospheric Fog
```
Light fog in the background, soft diffusion, depth enhancement, 
cinematic mood
```
**结构**: environment + diffusion + depth

#### 18. Reflective Surfaces
```
Realistic reflections on glass and water, accurate lighting interaction
```
**结构**: surface + reflection + light interaction

#### 19. Indoor Realism
```
Interior scene with natural lighting from windows, soft shadows, 
realistic room depth
```
**结构**: interior + natural light + shadow

#### 20. Outdoor Realism
```
Natural outdoor lighting, consistent sky color, realistic shadows 
and environmental detail
```
**结构**: environment + sunlight + shadow

### Category V: Continuity & Sequence Patterns

#### 21. Character Consistency
```
Same character appearance across all frames, stable facial features, 
consistent outfit and proportions
```
**结构**: subject identity + stable features
**适用**: 防止角色漂移

#### 22. Motion Continuity
```
Smooth frame-to-frame motion, no jitter, no sudden speed changes
```
**结构**: frame transition + smooth motion
**适用**: 所有动画

#### 23. Lighting Continuity
```
Lighting direction and intensity remain consistent throughout the scene
```
**结构**: light direction + intensity consistency
**适用**: 多镜头序列

#### 24. Expression Consistency
```
Facial expression remains stable, natural transitions if changing
```
**结构**: facial control + gradual change
**适用**: lipsync, 对话

#### 25. Loopable Sequence
```
Seamless looping animation, first and last frames match perfectly, 
continuous motion
```
**结构**: start frame = end frame + seamless motion

---

## 三、CinePrompt 结构框架

> 来源：https://cineprompt.io/

### 核心结构
```
Subject + Action + Camera + Lighting + Environment + Continuity
```

### 详细分类

#### Subject (角色/主体)
- Character (角色)
- Age Range
- Hair, Wardrobe, Expression, Body Language
- Object (物体)
- Environment (环境)

#### Actions (动作)
- Movement Type
- Pacing / Speed
- Interaction Type
- Primary Action
- Beat 1/2/3

#### Cinematography (摄影)
- Format (16:9, 9:16, etc.)
- Shot Type (Wide, Medium, Close-up, etc.)
- Camera Movement (Tracking, Static, Push-in, etc.)
- Camera Body
- Focal Length
- Lens
- Lens Filter
- Depth of Field
- Lighting Style

#### Lighting (灯光)
- Key Light
- Fill / Accent

#### Palette (调色)
- Color Science (raw/log)
- Film Stock
- Color Grade
- Primary / Secondary Colors
- Skin Tones

#### Sound (声音)
- Clean dialogue
- Environment SFX
- Music Genre/Mood

---

## 四、VEO 3 优质提示词示例

> 来源：https://promptark.net/zh/prompt-library/veo-3-prompts

### 示例1: 米其林星级厨师
```
Over-the-shoulder macro shot of a Michelin-starred chef placing microgreens 
onto a gourmet dish. Camera pushes in as he steps back, wipes his hands, 
and says: "Now… it's perfect." Crisp kitchen sounds: sizzling pans, 
sharp knife taps, subtle ambient jazz. Sharp focus on the plate, 
shallow depth behind. No subtitles.
```

### 示例2: 龙妈
```
A queen stands on a cliff during a storm — her cloak whips in the wind — 
camera cranes out to reveal a fleet of dragons in formation across the sky — 
lightning illuminates their eyes
```

### 示例3: 拉力赛车漂移
```
As the camera soars overhead, a rally car speeds along a narrow mountain pass, 
its vibrant red body glinting under the wintry sun. Snow drifts whirl around 
its tires, sending flurries into the air as the vehicle elegantly drifts into 
a sharp turn, tracing graceful arcs against the untouched white canvas below.
```

### 示例4: 赛博士兵
```
Medium handheld shot moves backward, capturing a cyborg soldier advancing 
slowly through an abandoned futuristic city at dawn. Sparks fall from broken 
neon signs. He pauses, scanning emptiness, and murmurs softly: 
'Am I human enough?' Atmospheric synth music rises
```

### 示例5: 中世纪战场
```
First-person view soaring low over a medieval battlefield at dawn, gliding 
past clashing knights in armor, fire-lit arrows whizzing overhead, splintered 
catapults burning near fallen soldiers, flying inches above torn flags and 
mud-soaked ground, ambient sounds of swords striking, war cries, galloping 
hooves, and wind rushing in your ears, raw, terrifying, epic
```

---

## 五、Quality Control Checklist

> 来源：MagicHour

### 1. Subject Consistency
- Face shape remains stable
- No sudden identity changes
- Outfit stays consistent

### 2. Motion Realism
- Movement speed feels natural
- No jitter or frame skipping
- Physics look believable

### 3. Lighting Consistency
- Light direction stays the same
- No flickering or brightness jumps

### 4. Composition & Framing
- Subject stays in frame
- No awkward cropping
- Camera movement is smooth

### 5. Background Integrity
- No warping or melting objects
- Background elements stay consistent

### 6. Expression & Lipsync
- Mouth movement matches speech
- Expression changes feel natural

---

## 六、分镜提示词模板结构

### 镜头级别提示词公式
```
[景别] [角度] of [角色外观描述], [动作/表情], 
camera [运镜方式], [光源], [色调], [氛围关键词], 
[时间标记 if needed]
```

### 示例
```
Medium close-up of a young woman with black long hair wearing white blouse, 
looking forward with a subtle smile, camera slowly pushing in, 
soft golden hour lighting from the left, warm color grading, romantic mood

Wide establishing shot of a city street at dusk, a man in dark coat walking 
in the distance, high environmental detail, cool blue tones, melancholic atmosphere
```

### 运镜关键词库
```
Static: fixed camera, locked frame, stable shot
Movement: tracking, dolly, crane, handheld
Push/Pull: push in, pull back, zoom in/out
Orbit: circling, orbiting, 360 degree rotation
FPV: first-person view, POV
```

### 灯光关键词库
```
Golden hour, blue hour, high key, low key
Soft lighting, hard lighting, rim lighting
Natural light, studio light, neon, candlelight
Warm tones, cool tones, desaturated
```

---

## 七、工作流建议

> 来源：MagicHour Cookbook

### 推荐工作流：Image-to-Video

**Step 1**: 先用图像生成器创建高质量静态图
- 定义清楚角色、服装、环境
- 不要在图像阶段加运动

**Step 2**: 图片质量检查与增强
- 提升分辨率
- 修复伪影
- 确保灯光方向清晰

**Step 3**: Image-to-Video 转换
- 只应用 1-2 个 prompt patterns
- 简单运动优先（push-in, idle movement）
- 时长控制在 3-5 秒

**Step 4** (Optional): 添加对话/表情
- 使用 lipsync 或 talking photo
- 保持头部运动最小

---

_Last updated: 2026-04-19 by Claw_
