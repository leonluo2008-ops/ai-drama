# Dreamina Pipeline 技术细节

## 参考图 + 风格叠加 workflow（2026-05-20 实测 ✅）

**问题**：用户参考图（写实人像）风格 ≠ 项目风格（像素风），如何统一？

**解法**：参考图驱动「角色身份」，style.md 驱动「输出风格」，两者叠加

```
参考图（图生图输入） + [角色外观描述] + [style.md art_direction]
    ↓
保留角色特征 + 风格统一的输出图
```

**沈晚宁案例（已验证）**：
- 参考图：写实女性（黑色长直发、鹅蛋脸、黑色无袖上衣+金色手链）
- 输出：像素风女性（六视图保留角色辨识度）
- 服装从「米白衬衫+深灰裙」更新为参考图同款

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

## 文件冲突陷阱（已踩坑，2026-05-20）

### 问题现象
dreamina 后台生成的图片是正确的，但发到飞书给用户看到的图不对（是另一张任务的图）。

### 根因
`download_result()` 下载到共享目录 `/tmp`，多角色并发轮跑时：
1. 任务A提交，下载到 `/tmp/bg_4x3.jpg`
2. 任务B提交，下载到 `/tmp/bg_4x3.jpg`（覆盖）
3. 脚本取 `list(Path("/tmp").iterdir())` 拿到的是 B 的图，但任务ID还是A的

### 修复方案
每个角色/场景用**自己的目录**做下载目标，不用共享 `/tmp`：

```python
# 错误：共用 /tmp
imgs = download_result(r["submit_id"], TMP_DIR)

# 正确：每个角色用自己的目录
imgs = download_result(r["submit_id"], char_dir)
```

`download_result` 内部用 `max(imgs, key=lambda f: Path(f).stat().st_mtime)` 取最新文件做兜底。

## 六视图图生图失败陷阱（已踩坑，2026-05-20）

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

## Dreamina CLI 关键参数

```
文生图：dreamina text2image --prompt="..." --ratio=1:1 --resolution_type=2k --model_version=5.0 --poll=0
图生图：dreamina image2image --images=ref1.png --images=ref2.png --prompt="..." --ratio=1:1 --resolution_type=2k --model_version=5.0 --poll=0
查询：  dreamina query_result --submit_id=<id>
下载：  dreamina query_result --submit_id=<id> --download_dir=<path>
```

### ⚠️ 必须用 `--key=value` 格式（2026-05-20 实测）
- ✅ `--images=path --prompt=text --ratio=1:1`
- ❌ `--images path --prompt text --ratio 1:1`（`--images` 只接受一个值，第二个路径被当作独立命令报错）
- 多图时每个都要写 `--images=path`： `--images=face.png --images=outfit.png`

- `--poll 0`：提交后立即返回 submit_id，自己轮询
- 轮询间隔：10秒
- model 5.0 = 最新模型
- 2K 图对 VIP 免费
