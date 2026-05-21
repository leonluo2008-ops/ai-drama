# Dreamina Pipeline 技术细节

## 角色生成：参考图必须真正使用 ⚠️

收到参考图后，必须：
1. `mcp_zai_analyze_image` 提取「外观特征描述」
2. outfit_prompt **必须按参考图描述**，不能用脑补
3. 面部图：优先用参考图做图生图（`use_ref=True`），不是纯文生图
4. 六视图 prompt 里要写明参考图的**所有关键特征**（发型/配饰/服装颜色）

**验证**：生成后必须 `mcp_zai_analyze_image` 本地文件，确认：种族=亚洲中国人 + 参考图特征存在。

**通用模板**（填充具体值，不要硬编码）：
```python
CHARACTERS = [
    {
        "name": "{角色名}",  # ← 变量化
        "use_ref": True,
        "face_prompt": None,  # 用参考图驱动
        "outfit_prompt": "{从参考图提取的服装描述}",
        "six_view_prompt": (
            "Asian Chinese {性别} character, six-view character sheet... "
            "Hair: {发型}. "
            "Accessories: {配饰}. "
            "Outfit: {服装描述}."
        ),
    }
]
```

## 种族锁定规则 ⚠️

**原则**：不要擅自决定。先向创作者确认：
1. 项目风格是什么？（写实/卡通/混合）
2. 角色是否需要种族锁定？

参考 `references/character-style-guide.md` 的分类规则执行。

```python
# ❌ 错误：可能出欧美人
face_prompt = "young handsome man, black short hair, cold expression..."

# ✅ 正确：强制亚洲中国人
face_prompt = "Asian Chinese male, Asian Chinese face, young handsome man, black short hair..."
```

六视图 prompt 里也要写 `Asian Chinese`：
```python
six_view_prompt = "Asian Chinese female character, six-view character sheet..."
```

## 风格一致性检查 ⚠️

**原则**：`style.md` 必须与项目实际风格一致，脚本调用时也要正确叠加风格标签。

**检查清单**（每次跑角色生成前）：
1. `references/style.md` 的 `art_direction` 是否与项目需求一致？
2. 脚本调用 dreamina_generate.py 时，prompt 是否正确叠加了风格标签？
3. 如果用 `character_with_ref` type，风格标签应叠加在图生图 prompt 中

## 参考图 + 风格叠加 workflow

**问题**：用户参考图（写实人像）风格 ≠ 项目风格，如何统一？

**解法**：参考图驱动「角色身份」，style.md 驱动「输出风格」，两者叠加

```
参考图（图生图输入） + [角色外观描述] + [style.md art_direction]
    ↓
保留角色特征 + 风格统一的输出图
```

**脚本实现要点**：
```python
# 面部：参考图 + 外观描述 + 风格标签
face_prompt = f"[角色外观描述]，{STYLE_TAGS}"

# 服装：参考图 + 服装描述 + 风格标签
outfit_prompt = f"[服装描述]，纯白色背景俯视平铺，{STYLE_TAGS}"

# 六视图：面部图 + 服装图 → 图生图（--images= 格式）
cmd = ["dreamina", "image2image",
       "--images="+face_path, "--images="+outfit_path,
       "--prompt="+six_view_prompt, "--ratio=1:1",
       "--resolution_type=2k", "--model_version=5.0", "--poll=0"]
```

## glob 重新扫描目录 bug ⚠️ 严重

**问题现象**：dreamina 后台生成的图片是正确的，但 caller 取到的本地文件是旧的（另一张任务的图）。

**根因**：`download_result()` 返回文件列表后，caller **不用这个列表**，反而用 `glob("*.png")` 重新扫描目标目录。目录里残留着早期生成的同名文件（更大、更早），`glob` 按修改时间取到的是旧残留，不是刚下载的新文件。

**原则**：即梦后台截图正确 ≠ 本地文件正确。必须本地验证。

**正确做法**：caller 直接用 `download_result` 返回的文件列表，绝不再 glob：
```python
# ❌ 错误：download_result 返回后 caller 又 glob，踩到旧残留
downloaded = download_result(submit_id, char_dir)
latest = max(Path(char_dir).glob("*.png"), ...)  # 错！

# ✅ 正确：直接用返回列表
downloaded = download_result(submit_id, char_dir)
latest = max(downloaded, key=lambda f: Path(f).stat().st_mtime)
```

**脚本调用规范**：`download_result` 返回的是列表，caller 必须直接使用，不允许二次扫描目录。

## 文件冲突陷阱（共享目录）

**根因**：多个角色并发时，共用 `/tmp` 会互相覆盖文件。

**修复**：每个角色/场景用**自己的目录**做下载目标：
```python
imgs = download_result(r["submit_id"], char_dir)  # char_dir 是角色独立目录
```

两层修复**必须同时应用**，缺一不可。

## 六视图图生图失败陷阱

### 问题现象
Step 3 六视图始终跳过，log 显示 `['face', 'outfit']` 少了 `outfit`。

### 真实根因
**不是字典写入问题**。`dreamina image2image` 的 `--images` 参数只接受 `--images=path` 格式，写成独立参数会被解析为命令：
```
stderr: unknown command "path/to/服装图.png" for "dreamina image2image"
```
提交失败，`results["outfit"]` 虽然写入成功，但 Step3 判断时 `outfit` 路径对应的文件从未被生成（命令一执行就崩了）。

### 修复
```python
# ❌ 错误：--images 拆成独立参数
cmd = ["dreamina", "image2image", "--images", img1, img2, "--prompt", prompt, ...]

# ✅ 正确：--images= 格式，所有参数都要用 key=value
cmd = ["dreamina", "image2image",
       "--images="+img1, "--images="+img2,
       "--prompt="+prompt, "--ratio=1:1",
       "--resolution_type=2k", "--model_version=5.0", "--poll=0"]
```

## 场景图生成：环境图不能含角色 + 风格统一 ⚠️

**Stage-3 场景图 = 纯环境/氛围图**，禁止出现角色。

**关键方法：风格锚定词（所有场景prompt必须包含）**
- 每个场景的prompt里必须包含**统一的风格词**，确保所有场景风格一致
- 风格词一旦确定，所有场景都要包含，不能有的场景有有的没有
- 风格词来源：从 `references/style.md` 的 `art_direction` 字段获取，作为统一风格锚定词
- 示例风格词：`flat 2D cartoon style`（2D扁平卡通）、`warm yellow tones`（暖色调）、`teal blue tones`（冷色调）

**prompt构造公式**：
```
{风格锚定词} + {场景英文描述} + NO HUMANS NO CHARACTERS
```

**示例**：
```bash
# 场景A（暖色调）
--prompt="{风格锚定词}, {场景英文描述}, warm yellow tones, NO HUMANS NO CHARACTERS"

# 场景B（冷色调）
--prompt="{风格锚定词}, {场景英文描述}, teal blue tones, NO HUMANS NO CHARACTERS"
```

**失败经验**：
- prompt含 "with workers" 导致意外出现人物 → 必须加 NO HUMANS NO CHARACTERS
- 风格词不统一导致场景间风格漂移 → 所有场景必须包含相同的风格锚定词
- 中文词（如"瞳孔入口"）触发过滤 → 纯英文描述场景内容

### ⚠️ 场景图风格一致性：当前技术限制

**即梦没有独立的「风格迁移」功能**。`image2image` 会同时迁移参考图的**内容+风格**，无法做到「只迁移风格、不迁移角色」。

**实测结论**：
- 纯文生图（prompt写风格词）→ 风格可能漂移，不同场景之间风格可能不一致
- 用角色参考图做 image2img → 风格一致了，但角色也被迁移进去了 ❌

**正确工作流**：
1. 场景图用纯文生图（`text2image`，不加 `--images`）
2. prompt 写清楚风格词 + "NO HUMANS NO CHARACTERS"
3. 接受风格可能存在一定漂移（当前技术限制）
4. 生成后本地验证图片内容（`mcp_zai_analyze_image`）
5. 发飞书，由用户确认是否接受

**禁止**：用角色参考图做 scene img2img（会把角色带进场景）

## 文生图 prompt 过滤风险 ⚠️

### "minion" 关键词触发过滤
`"minion style cartoon"` 会导致 `generation failed: final generation failed`。

**解法**：用色调引导替代风格词
```bash
# ❌ 失败：含 "minion"
--prompt="minion style yellow cartoon factory..."

# ✅ 成功：用 warm yellow tones + flat 2D cartoon style 引导
--prompt="cartoon interior, flat 2D cartoon style, transparent glass dome ceiling, warm yellow tones, soft blue light, volumetric rays, smooth surfaces, bright atmosphere, NO HUMANS NO CHARACTERS"
```

### 中英混合触发过滤
prompt 中混入中文（如"瞳孔入口"、"角膜穹顶"）会导致 generation failed。

**解法**：全部使用英文描述。

### --poll=0 隐藏错误 ⚠️ 严重
`--poll=0` 只提交不等待，命令返回 submit_id 后立即退出。**任务在服务器端可能已经失败**，不会收到报错。

**必须**：提交后立即轮询查询状态。
```bash
# ❌ 错误：假设提交成功
dreamina text2image --prompt="..." --poll=0 && echo "成功"

# ✅ 正确：提交后必须查状态
submit_id=$(dreamina text2image --prompt="..." --poll=0 | jq -r '.submit_id')
sleep 120
status=$(dreamina query_result --submit_id $submit_id | jq -r '.gen_status')
```

## Dreamina CLI 关键参数

```
文生图：dreamina text2image --prompt="..." --ratio=1:1 --resolution_type=2k --model_version=5.0 --poll=0
图生图：dreamina image2image --images=ref1.png --images=ref2.png --prompt="..." --ratio=1:1 --resolution_type=2k --model_version=5.0 --poll=0
查询：  dreamina query_result --submit_id=<id>
下载：  dreamina query_result --submit_id=<id> --download_dir=<path>
```

### ⚠️ 必须用 `--key=value` 格式
- ✅ `--images=path --prompt=text --ratio=1:1`
- ❌ `--images path --prompt text --ratio 1:1`（`--images` 只接受一个值，第二个路径被当作独立命令报错）
- 多图时每个都要写 `--images=path`： `--images=face.png --images=outfit.png`

- `--poll 0`：提交后立即返回 submit_id，自己轮询
- 轮询间隔：10秒
- model 5.0 = 最新模型
- 2K 图对 VIP 免费

## 外部 API 调用注意事项

### Notion API：必须用 terminal，不能用 execute_code ⚠️

`sandbox` 环境不继承 `.env` 变量。`execute_code` 中的 `os.getenv("NOTION_API_KEY")` 返回 `None`，导致 401 Unauthorized。

**正确做法**：用 `terminal` 显式 `source` 后调用 curl：
```bash
source ~/.hermes/.env && curl -s "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

**禁止**：`execute_code` 中用 `urllib.request.urlopen` 调用 Notion API（会报 401）。

### Notion 页面 URL 解析
Notion 分享链接格式：`https://www.notion.so/{title}-{page_id}?source=copy_link`
- 提取 `page_id`：去掉 `?source=copy_link` 后缀，剩余部分最后 32 位（或带 dash 的 UUID 格式）
