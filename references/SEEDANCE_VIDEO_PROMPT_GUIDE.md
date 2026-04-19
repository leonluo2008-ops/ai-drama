# Seedance AI Video Prompt Guide

> 来源：https://www.seedance.tv/blog/ai-video-prompt-guide

## 核心要素（必须包含5项）

### 1. Subject（主体）
Be specific. Not "a person" but "a middle-aged man with grey stubble wearing a navy suit."

### 2. Action（动作）
Use active, specific verbs. Not "driving" but "accelerating aggressively down an empty highway."

### 3. Environment（环境）
Include surface, background, depth cues, and atmosphere. Not "outside" but "in a misty Japanese forest, pine trees receding into fog, soft diffused morning light."

### 4. Camera（镜头）
Most commonly omitted element. Specify:
- Distance: close-up, medium shot, wide establishing shot
- Movement: "slow dolly forward," "handheld camera," "orbital shot," "static locked-off"
- Angle: "low angle looking up," "bird's eye view," "eye level"

### 5. Style/Quality（风格）
- "cinematic 4K" (generic quality boost)
- "documentary style" (naturalistic)
- "commercial photography" (clean, product-friendly)
- "film noir" (high contrast, shadows)

---

## Camera Movement Reference

| Effect | Prompt Phrase |
|--------|--------------|
| Zoom in | "slow dolly forward," "slow push in," "gentle zoom in" |
| Zoom out | "slow pull back," "dolly out to reveal," "zoom out" |
| Circle subject | "slow orbital shot," "360-degree rotation," "circling camera" |
| Side movement | "slow pan left," "lateral tracking shot," "camera glides left" |
| Vertical | "slow tilt up," "crane rising," "camera drifts upward" |
| No movement | "static shot," "locked-off camera," "no camera movement" |
| Handheld | "handheld camera," "slight camera shake," "documentary movement" |
| Aerial | "aerial drone view," "bird's eye view," "overhead looking down" |

---

## Lighting Reference

| Look | Prompt Phrase |
|------|--------------|
| Golden hour | "golden hour light," "late afternoon sun," "warm directional sunlight" |
| Dramatic | "dramatic side lighting," "strong shadows," "chiaroscuro" |
| Studio | "clean studio lighting," "three-point lighting," "product lighting" |
| Moody | "low-key lighting," "single candle/lamp light," "film noir" |
| Natural outdoor | "overcast diffused light," "cloudy day," "soft ambient" |
| Night/neon | "neon signs reflecting," "nighttime city lights," "cyberpunk lighting" |

---

## Template by Content Type

### Portrait and Character
```
[Character description] [specific action],
[environment with detail], [camera framing and movement],
[lighting], [style]
```

Example:
```
A young chef with flour-dusted hands and focused expression delicately 
crimping the edge of a fresh pie, rustic kitchen with morning light 
through a small window, close-up medium shot with gentle pull focus 
from hands to face, warm natural light, cinematic food film
```

### Landscape and Nature
```
[Specific landscape] at [time of day], [weather/atmosphere],
[camera movement] revealing the scene, [quality descriptor]
```

Example:
```
Rolling hills of green Irish countryside at golden hour, low clouds 
casting moving shadows, slow drone pull-back revealing the full 
panorama, cinematic nature documentary
```

### Product Showcase
```
[Product description] on [surface/environment],
[lighting setup], [camera movement], [style]
```

Example:
```
A premium perfume bottle on a marble surface with water droplets, 
soft side lighting with highlight sweep, slow 360-degree rotation 
revealing the label, commercial luxury product photography
```

---

## Common Mistakes

### Mistake 1: No camera movement specified
The AI will improvise camera movement, often producing jittery or unmotivated results.
→ Fix: Always specify what the camera does, even if it's "static locked-off camera"

### Mistake 2: Contradictory style descriptors
Combining "photorealistic" with "cartoon style" confuses the model.
→ Fix: Pick one visual aesthetic and stick to it

### Mistake 3: Too many subjects
Multiple subjects competing for attention produces inconsistent output.
→ Fix: Focus on one primary subject per generation

### Mistake 4: Vague actions
"Walking" gives the model too many options.
→ Fix: "walking briskly with purpose, arms swinging naturally" is unambiguous

### Mistake 5: Neglecting environment depth
Flat backgrounds produce flat video.
→ Fix: Describe foreground, midground, and background separately

---

## Platform-Specific Tips

### Seedance 2.0
- Responds well to cinematic language: "cinematic 4K," "film-quality"
- Strong on landscape, environment, and product
- Motion prompts like "slow dolly" are reliably executed
- Image-to-video: keep motion prompts under 20 words for best adherence

### Kling 2.0
- Prioritize the human subject description first
- Body mechanics language works: "natural gait," "fluid arm movement"
- Shorter prompts (under 50 words) often perform better

### Pika 2.1
- Effect names work: "inflate," "explode," "melt," "crush," "cake"
- Specify what to apply the effect to clearly
- Clean subjects on simple backgrounds produce the best effect results

### Runway Gen-4
- Use camera preset names when possible: "orbit," "dolly," "pan"
- Motion brush regions override text prompt motion for specified areas
- Reference footage (Act One) > text description for human subjects

---

_Last updated: 2026-04-19 by Claw_
