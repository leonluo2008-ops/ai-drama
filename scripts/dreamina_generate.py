#!/usr/bin/env python3
"""
dreamina_generate.py - Dreamina任务提交+轮询+下载统一入口

用法：
  # 生成角色定妆照（有参考图）
  python dreamina_generate.py --type character --project "项目名" --character "角色名" \
    --face_image "/path/to/参考图.png" --outfit_image "/path/to/参考图.png" --ratio 1:1

  # 生成角色定妆照（无参考图）
  python dreamina_generate.py --type character --project "项目名" --character "角色名" \
    --face_prompt "面部Prompt" --outfit_prompt "服装Prompt" --ratio 1:1

  # 生成场景大图
  python dreamina_generate.py --type scene --project "项目名" --scene "场景名" \
    --prompt "场景Prompt" --ratio 1:1

  # 生成场景多角度图
  python dreamina_generate.py --type scene_multi --project "项目名" --scene "场景名" \
    --source "/path/to/大场景图.png" --ratio 1:1

  # 生成分镜格图
  python dreamina_generate.py --type storyboard_panel --project "项目名" \
    --panel "1" --prompt "分镜Prompt" --ratio 16:9
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_BASE = PROJECT_ROOT / "projects"
SKILL_REFS = PROJECT_ROOT / "references"


def _load_style():
    """从 references/style.md 加载风格配置（如果存在）"""
    style_path = SKILL_REFS / "style.md"
    if not style_path.exists():
        return {}
    try:
        content = style_path.read_text()
        # 简单解析 YAML frontmatter 后的 art_direction
        art_dir = {}
        in_frontmatter = False
        for line in content.splitlines():
            if line.strip() == "---":
                in_frontmatter = not in_frontmatter
                continue
            if in_frontmatter and ":" in line:
                key, _, val = line.partition(":")
                art_dir[key.strip()] = val.strip()
        return art_dir
    except Exception:
        return {}


def ensure_project_dir(project: str) -> Path:
    """确保项目目录存在"""
    path = OUTPUT_BASE / project
    path.mkdir(parents=True, exist_ok=True)
    return path


def submit_and_wait(prompt: str, images: list = None, ratio: str = "1:1", resolution: str = "2k", model: str = "5.0") -> dict:
    """
    提交Dreamina任务并轮询直到完成
    返回：{"status": "success"/"failed", "images": [图片路径列表], "submit_id": "..."}
    """
    if images is None:
        images = []
    # 构造命令
    if images:
        # 图生图：--images=path 格式（重复flag每个图单独写）
        img_args = []
        for img in images:
            img_args.append(f"--images={img}")
        cmd = [
            "dreamina", "image2image",
            *img_args,
            f"--prompt={prompt}",
            f"--ratio={ratio}",
            f"--resolution_type={resolution}",
            f"--model_version={model}",
            "--poll=0"
        ]
    else:
        # 文生图
        cmd = [
            "dreamina", "text2image",
            f"--prompt={prompt}",
            f"--ratio={ratio}",
            f"--resolution_type={resolution}",
            f"--model_version={model}",
            "--poll=0"
        ]

    # 提交任务
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"提交失败: {result.stderr}", file=sys.stderr)
        return {"status": "failed", "error": result.stderr}

    try:
        data = json.loads(result.stdout)
        submit_id = data.get("submit_id")
        if not submit_id:
            return {"status": "failed", "error": "无submit_id"}
    except json.JSONDecodeError:
        return {"status": "failed", "error": f"JSON解析失败: {result.stdout[:200]}"}

    print(f"任务已提交: {submit_id}", file=sys.stderr)

    # 轮询
    while True:
        time.sleep(10)
        query_cmd = ["dreamina", "query_result", "--submit_id", submit_id]
        query_result = subprocess.run(query_cmd, capture_output=True, text=True)

        if query_result.returncode != 0:
            print(f"查询失败: {query_result.stderr}", file=sys.stderr)
            continue

        try:
            status_data = json.loads(query_result.stdout)
            gen_status = status_data.get("gen_status", "")
            if gen_status == "success":
                print(f"生成成功: {submit_id}", file=sys.stderr)
                return {
                    "status": "success",
                    "submit_id": submit_id,
                    "data": status_data
                }
            elif gen_status == "failed":
                print(f"生成失败: {submit_id}", file=sys.stderr)
                return {"status": "failed", "submit_id": submit_id, "error": "gen_status=failed"}
        except json.JSONDecodeError:
            print(f"状态查询解析失败: {query_result.stdout[:200]}", file=sys.stderr)
            continue


def download_result(submit_id: str, output_path: str) -> list:
    """下载生成结果到指定目录"""
    cmd = ["dreamina", "query_result", "--submit_id", submit_id, "--download_dir", output_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"下载失败: {result.stderr}", file=sys.stderr)
        return []
    # 返回目录下所有图片
    downloaded = []
    for f in Path(output_path).iterdir():
        if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
            downloaded.append(str(f))
    return downloaded


def _load_prompt_template(name: str) -> str:
    """从 references/ 目录加载 prompt 模板"""
    skill_dir = Path(__file__).resolve().parent.parent
    template_path = skill_dir / "references" / f"{name}.md"
    if not template_path.exists():
        return ""
    content = template_path.read_text()
    # 提取 ## 模板内容 之后的部分（跳过标题和说明）
    marker = "## 模板内容"
    idx = content.find(marker)
    if idx >= 0:
        return content[idx + len(marker):].strip()
    return content.strip()


def _build_sixview_prompt(face_path: str, outfit_path: str) -> str:
    """根据六视图模板构建 prompt"""
    six_views = [
        "人物面部正面特写",
        "人物面部45度侧面特写",
        "人物面部背面特写",
        "人物正面全身照",
        "人物45度侧面全身照",
        "人物背面全身照",
    ]
    views_text = "、".join(six_views)
    return (
        f"参考图生图：请严格根据图片1中的角色，生成一张人物的六视图角色定妆照；"
        f"不要出现文字，要求纯白色背景，有{views_text}。"
        f"该人物穿着图片2中的服饰。注意：只输出成一张图片。"
    )


def _build_scene_multi_prompt() -> str:
    """根据场景多角度模板构建 prompt"""
    return (
        "根据图像1中的场景，生成一张2×2多角度场景参考图，"
        "左上：平视中景，展示家具高度与空间尺度，"
        "右上：仰视天花板/顶部，展示顶部建筑设计与灯光细节，"
        "左下：近景特写，展示材质纹理与道具细节，"
        "右下：俯视鸟瞰，展示空间平面布局与动线。"
        "NO HUMANS NO CHARACTERS，禁止出现任何人物。"
        "不要出现文字，保持与原图一致的色调与光影风格。"
    )


def run_character(project: str, character: str, face_prompt: str, outfit_prompt: str, ratio: str,
                  face_image: str = None, outfit_image: str = None):
    """
    生成角色定妆照

    核心逻辑：
    - 有 face_image → 跳过面部生成，直接用 face_image 作为面部参考图
    - 有 outfit_image → 跳过服装生成，直接用 outfit_image 作为服装参考图
    - 无参考图 → 三步全跑（文生图）
    - 六视图总是用面部+服装参考图做图生图
    """
    import shutil
    proj_dir = ensure_project_dir(f"{project}/02-characters/{character}")
    proj_dir.mkdir(parents=True, exist_ok=True)
    results = {}

    # 加载风格配置（如果有）
    style = _load_style()
    art_direction = style.get("art_direction", "")

    # Step 1: 面部图（有无参考图分支）
    face_path = None
    if face_image:
        # 有参考图：用参考图做面部图生图
        print(f"\n[角色:{character}] Step 1/3 使用参考图生成面部图...", file=sys.stderr)
        face_prompt_for_img2img = (
            f"请严格根据参考图，生成一张人物的面部特写图。"
            f"保持参考图中的发型、脸型、眼睛、配饰等所有特征完全一致。"
            f"纯白色背景，人物居中。"
        )
        r = submit_and_wait(face_prompt_for_img2img, images=[face_image], ratio=ratio)
        if r["status"] != "success":
            print(f"面部图生成失败: {r.get('error')}", file=sys.stderr)
            return None
        face_path = str(proj_dir / f"{character}_面部.png")
        downloaded = download_result(r["submit_id"], str(proj_dir))
        if downloaded:
            latest = max(Path(proj_dir).glob("*.png"), key=lambda f: f.stat().st_mtime)
            shutil.copy2(latest, face_path)
            latest.unlink()
            results["face"] = face_path
            print(f"面部图已保存: {face_path}", file=sys.stderr)
    else:
        # 无参考图：纯文字生成
        print(f"\n[角色:{character}] Step 1/3 生成面部图...", file=sys.stderr)
        r = submit_and_wait(face_prompt, images=[], ratio=ratio)
        if r["status"] != "success":
            print(f"面部图生成失败: {r.get('error')}", file=sys.stderr)
            return None
        face_path = str(proj_dir / f"{character}_面部.png")
        downloaded = download_result(r["submit_id"], str(proj_dir))
        if downloaded:
            latest = max(Path(proj_dir).glob("*.png"), key=lambda f: f.stat().st_mtime)
            shutil.copy2(latest, face_path)
            latest.unlink()
            results["face"] = face_path
            print(f"面部图已保存: {face_path}", file=sys.stderr)

    # Step 2: 服装参考图（有无参考图分支）
    outfit_path = None
    if outfit_image:
        # 有参考图：直接复制参考图作为服装图
        print(f"\n[角色:{character}] Step 2/3 使用参考图作为服装图...", file=sys.stderr)
        outfit_path = str(proj_dir / f"{character}_服装.png")
        shutil.copy2(outfit_image, outfit_path)
        results["outfit"] = outfit_path
        print(f"服装参考图已保存: {outfit_path}", file=sys.stderr)
    else:
        # 无参考图：纯文字生成服装图
        print(f"\n[角色:{character}] Step 2/3 生成服装参考图...", file=sys.stderr)
        r = submit_and_wait(outfit_prompt, images=[], ratio=ratio)
        if r["status"] != "success":
            print(f"服装图生成失败: {r.get('error')}", file=sys.stderr)
            return None
        outfit_path = str(proj_dir / f"{character}_服装.png")
        downloaded = download_result(r["submit_id"], str(proj_dir))
        if downloaded:
            latest = max(Path(proj_dir).glob("*.png"), key=lambda f: f.stat().st_mtime)
            shutil.copy2(latest, outfit_path)
            latest.unlink()
            results["outfit"] = outfit_path
            print(f"服装参考图已保存: {outfit_path}", file=sys.stderr)

    # Step 3: 六视图（总是用面部+服装参考图）
    print(f"\n[角色:{character}] Step 3/3 生成六视图定妆照...", file=sys.stderr)
    six_view_prompt = _build_sixview_prompt(face_path, outfit_path)
    r = submit_and_wait(six_view_prompt, images=[face_path, outfit_path], ratio=ratio)
    if r["status"] != "success":
        print(f"六视图生成失败: {r.get('error')}", file=sys.stderr)
        return None
    six_view_path = str(proj_dir / f"{character}_六视图.png")
    downloaded = download_result(r["submit_id"], str(proj_dir))
    if downloaded:
        latest = max(Path(proj_dir).glob("*.png"), key=lambda f: f.stat().st_mtime)
        shutil.copy2(latest, six_view_path)
        latest.unlink()
        results["six_view"] = six_view_path
        print(f"六视图已保存: {six_view_path}", file=sys.stderr)

    return results


def run_scene(project: str, scene: str, prompt: str, ratio: str):
    """生成场景大图"""
    import shutil
    proj_dir = ensure_project_dir(f"{project}/03-scenes/{scene}")
    proj_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[场景:{scene}] 生成大场景全景图...", file=sys.stderr)
    r = submit_and_wait(prompt, images=[], ratio=ratio)
    if r["status"] != "success":
        print(f"场景图生成失败: {r.get('error')}", file=sys.stderr)
        return None

    scene_path = str(proj_dir / f"{scene}_大图.png")
    downloaded = download_result(r["submit_id"], str(proj_dir))
    if downloaded:
        latest = max(Path(proj_dir).glob("*.png"), key=lambda f: f.stat().st_mtime)
        shutil.copy2(latest, scene_path)
        latest.unlink()
        print(f"场景大图已保存: {scene_path}", file=sys.stderr)
        return {"scene_image": scene_path}
    return None


def run_scene_multi(project: str, scene: str, source: str, ratio: str):
    """基于场景大图生成多角度图"""
    import shutil
    proj_dir = ensure_project_dir(f"{project}/03-scenes/{scene}")
    proj_dir.mkdir(parents=True, exist_ok=True)

    multi_prompt = _build_scene_multi_prompt()

    print(f"\n[场景:{scene}] 生成多角度场景图...", file=sys.stderr)
    r = submit_and_wait(multi_prompt, images=[source], ratio=ratio)
    if r["status"] != "success":
        print(f"多角度图生成失败: {r.get('error')}", file=sys.stderr)
        return None

    multi_path = str(proj_dir / f"{scene}_多角度.png")
    downloaded = download_result(r["submit_id"], str(proj_dir))
    if downloaded:
        latest = max(Path(proj_dir).glob("*.png"), key=lambda f: f.stat().st_mtime)
        shutil.copy2(latest, multi_path)
        latest.unlink()
        print(f"多角度图已保存: {multi_path}", file=sys.stderr)
        return {"multi_image": multi_path}
    return None


def run_storyboard_panel(project: str, panel: str, prompt: str, ratio: str):
    """生成分镜格图"""
    import shutil
    proj_dir = ensure_project_dir(f"{project}/04-storyboards")
    proj_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[分镜格:{panel}] 生成图片...", file=sys.stderr)
    r = submit_and_wait(prompt, images=[], ratio=ratio)
    if r["status"] != "success":
        print(f"分镜格生成失败: {r.get('error')}", file=sys.stderr)
        return None

    panel_path = str(proj_dir / f"panel_{panel}.png")
    downloaded = download_result(r["submit_id"], str(proj_dir))
    if downloaded:
        latest = max(Path(proj_dir).glob("*.png"), key=lambda f: f.stat().st_mtime)
        shutil.copy2(latest, panel_path)
        latest.unlink()
        print(f"分镜格{panel}已保存: {panel_path}", file=sys.stderr)
        return {"panel_image": panel_path}
    return None


def main():
    parser = argparse.ArgumentParser(description="Dreamina统一生成入口")
    parser.add_argument("--type", required=True,
                        choices=["character", "scene", "scene_multi", "storyboard_panel"],
                        help="生成类型")
    parser.add_argument("--project", required=True, help="项目名")
    parser.add_argument("--character", help="角色名（character类型）")
    parser.add_argument("--scene", help="场景名（scene类型）")
    parser.add_argument("--panel", help="格编号（storyboard_panel类型）")
    parser.add_argument("--face_prompt", help="面部Prompt（character类型，无参考图时）")
    parser.add_argument("--outfit_prompt", help="服装Prompt（character类型，无参考图时）")
    parser.add_argument("--face_image", help="面部参考图路径（character类型，有参考图时）")
    parser.add_argument("--outfit_image", help="服装参考图路径（character类型，有参考图时）")
    parser.add_argument("--prompt", help="主Prompt（scene/storyboard_panel类型）")
    parser.add_argument("--source", help="源图路径（scene_multi类型）")
    parser.add_argument("--ratio", default="1:1", help="图片比例")

    args = parser.parse_args()

    if args.type == "character":
        # 有参考图时不需要 face_prompt/outfit_prompt，有参考图时必须至少有一个
        has_face_ref = bool(args.face_image)
        has_outfit_ref = bool(args.outfit_image)
        has_face_prompt = bool(args.face_prompt)
        has_outfit_prompt = bool(args.outfit_prompt)

        if has_face_ref or has_outfit_ref:
            # 有参考图：至少需要一个参考图
            if not (has_face_ref or has_outfit_ref):
                print("至少需要提供 --face_image 或 --outfit_image 其中一个参考图", file=sys.stderr)
                sys.exit(1)
            result = run_character(
                args.project, args.character,
                args.face_prompt or "", args.outfit_prompt or "",
                args.ratio,
                face_image=args.face_image, outfit_image=args.outfit_image
            )
        else:
            # 无参考图：必须同时提供 face_prompt 和 outfit_prompt
            if not (has_face_prompt and has_outfit_prompt):
                print("无参考图时必须提供 --face_prompt 和 --outfit_prompt", file=sys.stderr)
                sys.exit(1)
            result = run_character(
                args.project, args.character,
                args.face_prompt, args.outfit_prompt,
                args.ratio
            )

    elif args.type == "scene":
        if not all([args.scene, args.prompt]):
            print("--scene, --prompt 均必须提供", file=sys.stderr)
            sys.exit(1)
        result = run_scene(args.project, args.scene, args.prompt, args.ratio)

    elif args.type == "scene_multi":
        if not all([args.scene, args.source]):
            print("--scene, --source 均必须提供", file=sys.stderr)
            sys.exit(1)
        result = run_scene_multi(args.project, args.scene, args.source, args.ratio)

    elif args.type == "storyboard_panel":
        if not all([args.panel, args.prompt]):
            print("--panel, --prompt 均必须提供", file=sys.stderr)
            sys.exit(1)
        result = run_storyboard_panel(args.project, args.panel, args.prompt, args.ratio)

    if result:
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
