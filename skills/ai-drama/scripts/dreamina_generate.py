#!/usr/bin/env python3
"""
dreamina_generate.py - Dreamina任务提交+轮询+下载统一入口

用法：
  # 生成角色定妆照
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
    # 构造命令
    if images:
        # 图生图
        cmd = [
            "dreamina", "image2image",
            "--images"] + images + [
            "--prompt", prompt,
            "--ratio", ratio,
            "--resolution_type", resolution,
            "--model_version", model,
            "--poll", "0"
        ]
    else:
        # 文生图
        cmd = [
            "dreamina", "text2image",
            "--prompt", prompt,
            "--ratio", ratio,
            "--resolution_type", resolution,
            "--model_version", model,
            "--poll", "0"
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


def run_character(project: str, character: str, face_prompt: str, outfit_prompt: str, ratio: str):
    """生成角色定妆照"""
    proj_dir = ensure_project_dir(f"{project}/02-characters")
    tmp_dir = Path("/tmp")
    results = {}

    # Step 1: 生成面部图
    print(f"\n[角色:{character}] Step 1/3 生成面部图...", file=sys.stderr)
    r = submit_and_wait(face_prompt, images=None, ratio=ratio)
    if r["status"] != "success":
        print(f"面部图生成失败: {r.get('error')}", file=sys.stderr)
        return None
    face_path = str(proj_dir / f"{character}_面部.png")
    downloaded = download_result(r["submit_id"], tmp_dir)
    if downloaded:
        Path(downloaded[0]).rename(face_path)
        results["face"] = face_path
        print(f"面部图已保存: {face_path}", file=sys.stderr)

    # Step 2: 生成服装参考图
    print(f"\n[角色:{character}] Step 2/3 生成服装参考图...", file=sys.stderr)
    r = submit_and_wait(outfit_prompt, images=None, ratio=ratio)
    if r["status"] != "success":
        print(f"服装图生成失败: {r.get('error')}", file=sys.stderr)
        return None
    outfit_path = str(proj_dir / f"{character}_服装.png")
    downloaded = download_result(r["submit_id"], tmp_dir)
    if downloaded:
        Path(downloaded[0]).rename(outfit_path)
        results["outfit"] = outfit_path
        print(f"服装参考图已保存: {outfit_path}", file=sys.stderr)

    # Step 3: 图生图生成六视图
    print(f"\n[角色:{character}] Step 3/3 生成六视图定妆照...", file=sys.stderr)
    six_view_prompt = (
        "参考图生图：请严格根据图片1中的角色，生成一张人物的六视图角色定妆照；"
        "不要出现文字，要求纯白色背景，有人物面部正面特写、人物面部45度侧面特写、"
        "人物面部背面特写、人物正面全身照、人物45度侧面全身照以及人物背面全身照。"
        f"该人物穿着图片2中的服饰。注意：只输出成一张图片。"
    )
    r = submit_and_wait(six_view_prompt, images=[face_path, outfit_path], ratio=ratio)
    if r["status"] != "success":
        print(f"六视图生成失败: {r.get('error')}", file=sys.stderr)
        return None
    six_view_path = str(proj_dir / f"{character}_六视图.png")
    downloaded = download_result(r["submit_id"], tmp_dir)
    if downloaded:
        Path(downloaded[0]).rename(six_view_path)
        results["six_view"] = six_view_path
        print(f"六视图已保存: {six_view_path}", file=sys.stderr)

    return results


def run_scene(project: str, scene: str, prompt: str, ratio: str):
    """生成场景大图"""
    proj_dir = ensure_project_dir(f"{project}/03-scenes")
    tmp_dir = Path("/tmp")

    print(f"\n[场景:{scene}] 生成大场景全景图...", file=sys.stderr)
    r = submit_and_wait(prompt, images=None, ratio=ratio)
    if r["status"] != "success":
        print(f"场景图生成失败: {r.get('error')}", file=sys.stderr)
        return None

    scene_path = str(proj_dir / f"{scene}_大图.png")
    downloaded = download_result(r["submit_id"], tmp_dir)
    if downloaded:
        Path(downloaded[0]).rename(scene_path)
        print(f"场景大图已保存: {scene_path}", file=sys.stderr)
        return {"scene_image": scene_path}
    return None


def run_scene_multi(project: str, scene: str, source: str, ratio: str):
    """基于场景大图生成多角度图"""
    proj_dir = ensure_project_dir(f"{project}/03-scenes")
    tmp_dir = Path("/tmp")

    multi_prompt = (
        "根据图像1中的场景，生成一张2×2多角度场景参考图，"
        "左上：平视中景，展示家具高度与空间尺度，"
        "右上：仰视天花板/顶部，展示顶部建筑设计与灯光细节，"
        "左下：近景特写，展示材质纹理与道具细节，"
        "右下：俯视鸟瞰，展示空间平面布局与动线。"
        "NO HUMANS NO CHARACTERS，禁止出现任何人物。"
        "不要出现文字，保持与原图一致的色调与光影风格。"
    )

    print(f"\n[场景:{scene}] 生成多角度场景图...", file=sys.stderr)
    r = submit_and_wait(multi_prompt, images=[source], ratio=ratio)
    if r["status"] != "success":
        print(f"多角度图生成失败: {r.get('error')}", file=sys.stderr)
        return None

    multi_path = str(proj_dir / f"{scene}_多角度.png")
    downloaded = download_result(r["submit_id"], tmp_dir)
    if downloaded:
        Path(downloaded[0]).rename(multi_path)
        print(f"多角度图已保存: {multi_path}", file=sys.stderr)
        return {"multi_image": multi_path}
    return None


def run_storyboard_panel(project: str, panel: str, prompt: str, ratio: str):
    """生成分镜格图"""
    proj_dir = ensure_project_dir(f"{project}/04-storyboards")
    tmp_dir = Path("/tmp")

    print(f"\n[分镜格:{panel}] 生成图片...", file=sys.stderr)
    r = submit_and_wait(prompt, images=None, ratio=ratio)
    if r["status"] != "success":
        print(f"分镜格生成失败: {r.get('error')}", file=sys.stderr)
        return None

    panel_path = str(proj_dir / f"panel_{panel}.png")
    downloaded = download_result(r["submit_id"], tmp_dir)
    if downloaded:
        Path(downloaded[0]).rename(panel_path)
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
    parser.add_argument("--face_prompt", help="面部Prompt（character类型）")
    parser.add_argument("--outfit_prompt", help="服装Prompt（character类型）")
    parser.add_argument("--prompt", help="主Prompt（scene/storyboard_panel类型）")
    parser.add_argument("--source", help="源图路径（scene_multi类型）")
    parser.add_argument("--ratio", default="1:1", help="图片比例")

    args = parser.parse_args()

    if args.type == "character":
        if not all([args.character, args.face_prompt, args.outfit_prompt]):
            print("--character, --face_prompt, --outfit_prompt 均必须提供", file=sys.stderr)
            sys.exit(1)
        result = run_character(args.project, args.character, args.face_prompt, args.outfit_prompt, args.ratio)

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
