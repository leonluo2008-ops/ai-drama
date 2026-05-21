---
name: ai-drama
description: AI短剧视频生成Pipeline — 从剧本到角色图→场景图→分镜→音频的完整生产流水线。触发词：ai-drama、短剧生成、角色图、场景图、分镜图、剧本生成、AI视频、imgs2img视频
---

# AI-Drama 短剧生成 Pipeline

## 架构：三层分离

| 层级 | 位置 | 职责 |
|------|------|------|
| 编排层 | SKILL.md | 唯一入口，Stage分段组织，数据契约定义 |
| 生成层 | references/*.md | prompt 规格说明（视角列表/约束条件）+ 方法论文档 |
| 工具层 | scripts/*.py | 执行命令、文件操作，不含业务内容 |

### 设计原则：框架 > 模板

**核心原则**：Skill 是工作流框架，不是硬编码模板。

| 原则 | 含义 |
|------|------|
| **占位符思维** | 具体值→变量。路径/ID/示例内容一律留占位符。新机器/新用户/新场景能直接用的才是好框架。 |
| **禁止套模板** | 示例=参考，不是素材。照搬结构但不知道原因=套路化，能举一反三=原理化。封装前先问：为什么work？ |
| **理解原理** | 抽取推理链而非格式。封装的是决策逻辑，不是操作步骤。 |
| **工具与逻辑分离** | Skill只管「说什么」，scripts只管「怎么做」，references只管「内容模板」。工具升级只改scripts，不动SKILL.md。 |

**违反这些原则的特征（发现问题时的自我检查）**：
- 脚本里有硬编码的角色名、项目名、具体prompt内容
- SKILL.md 引用了特定实测案例的细节
- 新用户/新项目无法直接使用，需要大面积替换内容才能跑

## Pipeline Stage 顺序

```
Stage-1 剧本 → Stage-2 角色 → Stage-3 场景 → Stage-4 分镜 → Stage-5 音频
```

每Stage完成后必须人工确认，再进入下一Stage。

---

## ⚠️ 关键概念区分

| 概念 | 说明 |
|---|---|
| **场次时长** | 纯粹的故事/剧本概念，由台词量+动作量决定，代表"这场戏发生多久" |
| **视频时长** | Seedance 2.0 的技术参数，支持 4-15s，在 Phase 4 输出Prompt时体现 |

**禁止混淆**：不得以"Seedance只能生成X秒"为由建议合并/拆分场次；场次划分由剧本内容决定，时长适配是生成阶段的独立问题。
**正确处理**：如果某场次时长<4秒 → 由导演告知编剧，该场次需填充内容延展到4秒（不合并场次边界）

---

## 场次划分方法论（AI必须遵循）

### 核心原则
- **每个场次独立生成**（不合并）
- **场次时长必须能容纳完整台词音频**
- **切分点：按台词自然停顿，不是按时长硬切**

### 划分步骤

**步骤1：统计台词**
- 逐场统计台词字数
- 计算朗读时间 = 台词字数 ÷ 3.5（中文基准）

**步骤2：划分场次**
- 按叙事节奏切分（静/快/急/缓）
- 切分点在台词自然停顿处（自然分段）
- 每场时长 = 台词时间 + 画面填充时间

**步骤3：验证Seedance约束**
- 每场时长必须在4-15秒内
- **不足4秒 → 填充静默镜头/延展画面，不合并**
- **超过15秒 → 在台词自然停顿处拆成两个场次**

**步骤4：台词时间与场次时长对齐**
- 确保每场时长能容纳完整台词
- 语速保持正常（3.5字/秒），不压缩

### 示例计算

| 场次 | 台词字数 | 台词时间 | 画面填充 | 场次时长 | Seedance |
|---|---|---|---|---|---|
| 3 | 24字 | 7s | 0s | 7s | ✅ |
| 5 | 65字 | 19s | 0s | 19s | ❌超15s→拆成2场 |

### 常见错误
- ❌ 合并场次来"适配"Seedance（禁止）
- ❌ 场次时长小于台词所需时间（音频放不进去）
- ❌ 按时长硬切（破坏台词完整性）

---

## AI决策边界

AI负责：信息完整呈现 + 方案建议 + 执行
用户决定：场次合并/拆分/调整、最终拍板

---

## 风格锚定：references/style.md 外置配置 ⚠️ 关键
- **风格不应硬编码在 prompt 里**：不同项目需要不同风格，切换风格时不能改脚本
- **正确做法**：在 `references/style.md` 中定义 `art_direction` 等字段，脚本启动时动态加载
- **切换风格流程**：用户提供参考图 → `mcp_zai_analyze_image` 提取风格关键词 → 更新 `references/style.md` 的 art_direction 字段 → 重新生成一代图
- **脚本加载逻辑**：见 `references/dreamina-pipeline.md`
- **切换风格后必须**：清理旧图 → 重新生成 → 发飞书确认 → commit

### 参考图 + 风格叠加 workflow

**问题**：用户提供的参考图（写实人像）风格 ≠ 项目风格，两者如何统一？

**解法**：参考图驱动「角色是谁」，style.md 驱动「画成什么风格」，叠加输出

**流程**：
1. 用户发参考图 → `mcp_zai_analyze_image` 提取外观特征（发型、脸型、服装等）
2. 将外观特征描述 + style.md 的 art_direction 组合成最终 prompt
3. 图生图（参考图），追加风格标签
4. 服装同理：参考图服装特征描述 + 风格标签 → 服装平铺图
5. 六视图用新版面部+新版服装图生图

### 即梦 5.0 prompt 雷区
- **禁止用 portrait photo/portrait**（model 5.0 会出插画/卡通风，不是写实人像）
- **服装图**：需要纯白背景、俯视角度（flat lay）、所有物品完整可见，避免 fashion photography 风格
- **prompt 精简原则**：文生图 prompt 过长会导致 generation failed。保留核心特征描述（主体+颜色+关键配饰），删除修饰性形容词

### 文生图 prompt 复杂度陷阱 ⚠️
即梦文生图对 prompt 长度敏感，过长的 prompt 会导致 generation failed。

**失败征兆**：`gen_status: fail, fail_reason: "generation failed: final generation failed"`

**经验规则**：
- 主体描述 + 颜色/材质 + 关键特征 ≤ 3-4 个短句
- 删除形容词词组（"friendly", "confident", "detailed" 等）
- 只保留：主体词 + 颜色 + 关键元素

**正确示例**：
```
# ❌ 失败：过多修饰词
"minion style male character, yellow skin, orange short spiky hair, green eyes, silver goggles on head, blue denim overalls, teal accents, white t-shirt, big friendly smile, confident expression, pure white background"

# ✅ 成功：精简核心（删除形容词词组，保留主体+颜色+关键元素）
"minion style male character, yellow skin, orange hair, green eyes, silver goggles, blue overalls, white t-shirt, pure white background"
```

**注**：卡通风格角色（如小黄人）不需要 `Asian Chinese` 前缀；写实人像风格角色才需要。

### 种族/风格铁律 ⚠️ 必须遵守
**所有角色 prompt 必须以 `Asian Chinese` 开头**，不能用模糊写法。模型默认会混入欧美人种，必须强制锁定。

```python
# ❌ 错误：模型可能出欧美人
face_prompt = "young handsome man, black short hair..."

# ✅ 正确：强制亚洲中国人
face_prompt = "Asian Chinese male, Asian Chinese face, young handsome man..."
```

**style.md 必须与项目实际风格一致**。如果 style.md 设成一种风格但项目要另一种，会造成风格错乱。切换风格后必须验证脚本实际调用了 style.md 的内容。

### 参考图分支：单图 vs 双图 ⚠️ 关键

**一张参考图时，不能同时当脸和服装传**：即梦图生图按 `@` 顺序对应 prompt 中的"图片1"、"图片2"。如果同一张全身图既当"图片1（角色）"又当"图片2（服装）"，模型会混淆。

**三种场景的正确处理**：

| 场景 | 处理方式 |
|------|---------|
| 用户提供1张参考图 | 直接用原图做六视图（只传1个参考图），prompt 强调"保持参考图中所有特征" |
| 用户提供2张参考图（面部+服装分开的平铺图） | 用双图六视图，prompt 区分"图片1是角色"和"图片2是服装" |
| 无参考图，已生成面部+服装 | 用双图六视图，传生成的2张图 |

**服装参考图必须是纯服装平铺图**（flat lay），不是包含角色的全身照。如果用户提供的是角色全身照作为参考，应该走单图六视图流程。

### ⚠️ 禁止用同一参考图生成多个不同角色

**常见错误**：以为AI会自动对同一参考图做"差异化处理"，生成不同角色。

**事实**：同一参考图生成多个角色，结果是相同或高度相似的。AI图生图是"复刻"，不是"创作"。

**正确做法**：
- 每个角色各提供一张独立参考图
- 或为每个角色设计独立的文生图 prompt（不同的发型/颜色/体型描述）
- 参考图只解决"这个角色长什么样"，不解决"我有两个不同角色"

**合法场景：服装风格模板复用**
同一参考图可以作为多个角色的服装风格模板（因为同一世界观下服装统一），但面部特征必须各自独立：
- ✅ 同参考图 + 各角色独立 face_prompt → 可行
- ✅ 同参考图 + 各角色独立文生图 face → 可行
- ❌ 同参考图 + 同 face_prompt → 生成相同角色

### 参考图必须真正使用 ⚠️ 关键
收到用户参考图后，必须：
1. `mcp_zai_analyze_image` 提取外观特征（发型、服装、配饰）
2. outfit_prompt **必须按参考图描述**，不能用脑补
3. 面部图优先用参考图做图生图（`use_ref=True`）
4. 六视图 prompt 里也要写明参考图的特征（发型/配饰）

**原则**：outfit_prompt 必须严格按参考图描述，不能脑补。如果描述内容与参考图不符，会导致服装完全不对。

### 发图前必须验证 ⚠️
发图给用户前，先 `mcp_zai_analyze_image` 本地文件，确认：
- 种族正确（亚洲中国人）
- 关键特征存在（参考图的配饰、服装颜色等）
- 文件不是其他任务覆盖后的残留
本地验证通过后再发飞书。不要只看 dreamina 后台截图就发。

### 六视图参考图必须覆盖六个视角
详见 `references/sixview-template.md`

## ⚠️ 关键检查点：Stage-4 需要「镜头规划表」步骤
详见 `references/shot-planning-method.md`

**核心问题**：场次表只解决"切成几块"，没解决"每块用什么镜头"。  
**待确认**：镜头规划表粒度（每镜头一行 vs 每场3-5个关键镜）、表达形式（纯文字 vs 图示）。

---

## 正确工作流程（必须遵守）

```
用户发送剧本内容（台词+动作描述）
      ↓
AI读取完整剧本，理解故事内容
      ↓
AI按场次划分方法论切分场次（步骤1-4）
      ↓
输出：场次表（含台词字数|台词时长|画面时长|总时长|出场角色|节奏）
      ↓
用户确认/调整
      ↓
AI输出镜头规划表
      ↓
用户确认
      ↓
AI输出分镜脚本
```

**⚠️ 绝对禁止**：
- 用户发送场次表 → AI未读剧本就输出场次分析
- 跳过「读取剧本」步骤直接处理表格数据
- 以"SSeedance只能生成X秒"为由建议合并/拆分场次
- 把「编剧给的场次时长」当成最终场次（那是叙事参考，AI需要重新按公式计算）

**关键纠正**：
- 场景划分是AI的职责，不是编剧的职责
- 编剧发送的是「叙事参考时长」，AI必须先读剧本，再按公式重新计算
- 时长不足4秒 → 告知编剧延展内容，不合并场次
- 超过15秒 → 在台词自然停顿处拆成两个场次

---

## Stage-2 角色图生成

### 分支判断：有参考图 vs 无参考图

```
用户提供了参考图？
  ↓ 是
  ┌─ 有 --face_image → 面部用参考图图生图（跳过面部生成）
  ├─ 有 --outfit_image → 服装用参考图（跳过服装生成）
  └─ 六视图 → 用 --face_image + --outfit_image 做图生图

  ↓ 否
  character 类型，三步全跑：面部→服装→六视图（均为文生图）
```

**核心规则**：默认使用参考图中的服装，不额外生成。除非用户明确要求「服化道设计」才走独立生成流程。

### dreamina_generate.py type 清单

|| type | 场景 | 必选参数 |
||------|------|----------|
|| `character` | 角色定妆照（面部→服装→六视图，全流程） | `--character` + `--face_prompt` + `--outfit_prompt` |
|| `scene` | 场景大图（文生图） | `--scene` + `--prompt` |
|| `scene_multi` | 场景多角度图（图生图） | `--scene` + `--source`（源图路径） |
|| `storyboard_panel` | 分镜格图（文生图） | `--panel` + `--prompt` |

### character 类型命令

```bash
# 有参考图：默认使用参考图中的服装，跳过服装生成
python scripts/dreamina_generate.py \
  --type character \
  --project "{项目名}" \
  --character "{角色名}" \
  --face_image "/path/to/参考图.png" \
  --outfit_image "/path/to/参考图.png" \
  --ratio 1:1

# 无参考图：三步全跑（文生图）
python scripts/dreamina_generate.py \
  --type character \
  --project "{项目名}" \
  --character "{角色名}" \
  --face_prompt "{Asian Chinese female, long straight black hair...}" \
  --outfit_prompt "{描述角色服装的英文文本}" \
  --ratio 1:1
```

### 其他 type 命令

```bash
# 场景大图
python scripts/dreamina_generate.py \
  --type scene --project "{项目}" --scene "{场景名}" \
  --prompt "{场景描述}" --ratio 1:1

# 场景多角度图（图生图，以场景大图为源）
python scripts/dreamina_generate.py \
  --type scene_multi --project "{项目}" --scene "{场景名}" \
  --source "/path/to/场景大图.png" --ratio 1:1

# 分镜格图
python scripts/dreamina_generate.py \
  --type storyboard_panel --project "{项目}" \
  --panel "1" --prompt "{分镜描述}" --ratio 16:9
```

### 即梦 query_result 下载逻辑 ⚠️ 关键 bug

**有两层风险，必须同时修复**：

**第一层：共享目录冲突**
- **根因**：多个角色/场景并发时，共用 `/tmp` 会互相覆盖文件
- **修复**：每个角色/场景用**各自独立的目录**做下载目标
  ```python
  # ❌ 错误：共用 /tmp，4个角色会互相踩
  imgs = download_result(r["submit_id"], TMP_DIR)

  # ✅ 正确：每个角色用自己的目录
  imgs = download_result(r["submit_id"], char_dir)
  ```

**第二层：glob 重新扫描目录 bug ⚠️ 严重**
- **根因**：`download_result()` 返回文件列表后，caller 不用这个列表，反而 `glob("*.png")` 重新扫描目标目录。目录里可能有旧残留文件（更早生成的、同名的、更大的），`glob` 取到的是旧文件而非新下载的文件。
- **现象**：dreamina 后台看是对的（任务ID对应正确图片），但 `glob` 取到的是旧残留文件，导致后续所有图片都错
- **原则**：即梦后台截图正确 ≠ 本地文件正确，必须本地验证
- **修复**：caller 必须**直接使用 `download_result` 返回的文件列表**，不要重新扫描目录：
  ```python
  # ❌ 错误：download_result 返回后 caller 又 glob，踩到旧残留
  downloaded = download_result(r["submit_id"], char_dir)
  latest = max(Path(char_dir).glob("*.png"), key=lambda f: f.stat().st_mtime)  # 错！

  # ✅ 正确：直接用 download_result 返回的列表
  downloaded = download_result(r["submit_id"], char_dir)
  latest = max(downloaded, key=lambda f: Path(f).stat().st_mtime)
  ```

**验证原则**：发图前必须 `mcp_zai_analyze_image` 本地文件确认内容正确，不能只看 dreamina 后台截图。

### 跨设备文件操作
- **不要用 `Path.rename()`**：会报 `Invalid cross-device link`
- **正确做法**：
  ```python
  import shutil
  shutil.copy2(src, dst)
  Path(src).unlink()
  ```

### dreamina CLI 参数格式 ⚠️

```
# ❌ 错误：--images 拆成独立参数，或 --images <p1> <p2> 空格分隔
cmd = ["dreamina", "image2image", "--images", img1, img2, "--prompt", prompt, ...]

# ✅ 正确：--images= 格式，重复flag每个图单独写
cmd = ["dreamina", "image2image",
       f"--images={img1}", f"--images={img2}",
       f"--prompt={prompt}", f"--ratio={ratio}", ...]
```

**所有参数必须用 `--key=value` 格式**，不能用空格分隔：`--prompt {val}` 是错的，`--prompt={val}` 是对的。

---

## 工作目录约定

每个项目独立目录，结构如下：

```
projects/
  {项目名}/
    01-scripts/          # 剧本
    02-characters/       # 角色图
      {角色名}/
        {角色}_面部.png
        {角色}_服装.png
        {角色}_六视图.png
    03-scenes/           # 场景图
    04-storyboards/      # 分镜脚本
    05-audio/            # 音频
references/
  style.md              # 风格锚定（art_direction）
  dreamina-pipeline.md   # 工具层技术细节
```

**角色目录命名**：用角色真实名字，不用代号。
