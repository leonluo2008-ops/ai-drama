#!/usr/bin/env python3
"""
角色图+场景图总控脚本
按顺序执行：角色面部+服装 → 六视图 → 场景图
"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

PROJECT = "guyan-mother-appeared"
PROJECT_DIR = Path(__file__).resolve().parent.parent / "projects" / PROJECT
CHAR_DIR = PROJECT_DIR / "02-characters"
SCENE_DIR = PROJECT_DIR / "03-scenes"
TMP_DIR = Path("/tmp")
SCRIPT_DIR = Path(__file__).resolve().parent

CHARACTERS = [
    {
        "name": "顾砚",
        "face_prompt": "一位年轻英俊的亚洲男性，黑色短发精致偏分，身着深色高定西装，暗纹领带，冷峻表情，Pixel Art style, cyberpunk aesthetic, pixelated portrait, clean solid color background, high detail, 2k",
        "outfit_prompt": "黑色高定西装套装，白色衬衫，暗纹领带，黑色西裤，袖扣，纯白色背景俯视平铺，所有物品完整展示不裁切，Pixel Art style, cyberpunk flat lay aesthetic, pixelated fabric texture, high detail, 2k",
        "six_view_prompt": "参考图生图：请严格根据图片1中的角色，生成一张人物的六视图角色定妆照；不要出现文字，要求纯白色背景，有人物面部正面特写、人物面部45度侧面特写、人物面部背面特写、人物正面全身照、人物45度侧面全身照以及人物背面全身照。该人物穿着图片2中的服饰。注意：只输出成一张图片。",
    },
    {
        "name": "林浅浅",
        "face_prompt": "一位年轻漂亮的亚洲女性，栗色长卷发精致盘发造型，香槟色亮面礼服裙收腰设计，银色细高跟，精致耳坠，表情傲慢轻蔑，Pixel Art style, cyberpunk aesthetic, pixelated portrait, clean solid color background, high detail, 2k",
        "outfit_prompt": "香槟色亮面礼服裙，收腰设计，裙摆及膝，银色细高跟，精致耳坠，细项链，纯白色背景俯视平铺，所有物品完整展示不裁切，Pixel Art style, cyberpunk flat lay aesthetic, pixelated fabric texture, high detail, 2k",
        "six_view_prompt": "参考图生图：请严格根据图片1中的角色，生成一张人物的六视图角色定妆照；不要出现文字，要求纯白色背景，有人物面部正面特写、人物面部45度侧面特写、人物面部背面特写、人物正面全身照、人物45度侧面全身照以及人物背面全身照。该人物穿着图片2中的服饰。注意：只输出成一张图片。",
    },
    {
        "name": "沈晚宁",
        "face_prompt": "一位亚洲年轻女性，黑色长发自然垂落，米白色简约衬衫，深灰色直筒裙，黑色粗跟单鞋，表情被动尴尬，Pixel Art style, cyberpunk aesthetic, pixelated portrait, clean solid color background, high detail, 2k",
        "outfit_prompt": "米白色简约衬衫，款式保守，深灰色直筒裙长度及膝，黑色粗跟单鞋，无明显配饰，纯白色背景俯视平铺，所有物品完整展示不裁切，Pixel Art style, cyberpunk flat lay aesthetic, pixelated fabric texture, high detail, 2k",
        "six_view_prompt": "参考图生图：请严格根据图片1中的角色，生成一张人物的六视图角色定妆照；不要出现文字，要求纯白色背景，有人物面部正面特写、人物面部45度侧面特写、人物面部背面特写、人物正面全身照、人物45度侧面全身照以及人物背面全身照。该人物穿着图片2中的服饰。注意：只输出成一张图片。",
    },
    {
        "name": "我妈",
        "face_prompt": "一位亚洲年长女性，花白短发微乱无造型感，洗到发白的藏青色旧棉褂手工布盘扣，褪色深灰色粗布裤子，黑色老式布鞋磨损严重，表情善良无措，Pixel Art style, cyberpunk aesthetic, pixelated portrait, clean solid color background, high detail, 2k",
        "outfit_prompt": "洗到发白的藏青色旧棉褂，手工布盘扣，褪色深灰色粗布裤子，黑色老式布鞋磨损严重，旧布袋，纯白色背景俯视平铺，所有物品完整展示不裁切，Pixel Art style, cyberpunk flat lay aesthetic, pixelated fabric texture, high detail, 2k",
        "six_view_prompt": "参考图生图：请严格根据图片1中的角色，生成一张人物的六视图角色定妆照；不要出现文字，要求纯白色背景，有人物面部正面特写、人物面部45度侧面特写、人物面部背面特写、人物正面全身照、人物45度侧面全身照以及人物背面全身照。该人物穿着图片2中的服饰。注意：只输出成一张图片。",
    },
]

SCENE_PROMPT = (
    "豪华宴会厅，金色水晶吊灯垂悬中央，长条白色桌布宴会桌，精致银器餐具排列整齐，"
    "落地窗外暮色将至，红色帷幕装饰墙面，大理石地面反射暖光，空气中弥漫着花香，"
    "Pixel Art style, cyberpunk city night, 俯视广角构图, high-saturation neon colors, "
    "blocky pixel brushstrokes, NO HUMANS NO CHARACTERS, no people, empty scene, high detail, 2k"
)

SIX_VIEW_MULTI_PROMPT = (
    "根据图像1中的场景，生成一张2x2多角度场景参考图，"
    "左上：平视中景，展示家具高度与空间尺度，"
    "右上：仰视天花板或顶部，展示顶部建筑设计与灯光细节，"
    "左下：近景特写，展示材质纹理与道具细节，"
    "右下：俯视鸟瞰，展示空间平面布局与动线，"
    "NO HUMANS NO CHARACTERS，禁止出现任何人物，"
    "保持Pixel Art风格，霓虹光影，块状像素笔触，不要出现文字，2k"
)


def run_cmd(cmd, timeout=300):
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return result


def submit_and_wait(prompt, images=None, ratio="1:1", model="5.0"):
    """提交dreamina任务并轮询等待结果"""
    if images:
        cmd = ["dreamina", "image2image", "--images"] + images + [
            "--prompt", prompt, "--ratio", ratio,
            "--resolution_type", "2k", "--model_version", model, "--poll", "0"
        ]
    else:
        cmd = ["dreamina", "text2image", "--prompt", prompt, "--ratio", ratio,
               "--resolution_type", "2k", "--model_version", model, "--poll", "0"
        ]

    r = run_cmd(cmd)
    if r.returncode != 0:
        return {"status": "failed", "error": r.stderr}

    try:
        data = json.loads(r.stdout)
        submit_id = data.get("submit_id")
    except json.JSONDecodeError:
        return {"status": "failed", "error": f"JSON解析失败: {r.stdout[:200]}"}

    print(f"  提交成功: {submit_id}", flush=True)

    # 轮询
    while True:
        time.sleep(10)
        q = run_cmd(["dreamina", "query_result", "--submit_id", submit_id])
        if q.returncode != 0:
            print(f"  查询失败: {q.stderr}", flush=True)
            continue
        try:
            sd = json.loads(q.stdout)
            gs = sd.get("gen_status", "")
            if gs == "success":
                print(f"  生成成功!", flush=True)
                return {"status": "success", "submit_id": submit_id, "data": sd}
            elif gs == "failed":
                print(f"  生成失败", flush=True)
                return {"status": "failed", "submit_id": submit_id}
        except json.JSONDecodeError:
            continue


def download_result(submit_id, output_dir):
    """下载结果到指定目录（每个任务单独目录，避免文件冲突）"""
    run_cmd(["dreamina", "query_result", "--submit_id", submit_id, "--download_dir", str(output_dir)])
    # 只取这个目录下本次任务的图（按修改时间取最新的）
    imgs = [str(f) for f in output_dir.iterdir() if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
    if not imgs:
        return []
    # 如果有多个文件，取最新的那个
    latest = max(imgs, key=lambda f: Path(f).stat().st_mtime)
    return [latest]


def copy_to_dest(src, dst):
    shutil.copy2(src, dst)
    Path(src).unlink()


def main():
    print("=" * 50)
    print("Stage-2 角色图生成 开始")
    print("=" * 50)

    all_results = {}

    for char in CHARACTERS:
        name = char["name"]
        print(f"\n>>> 处理角色: {name}", flush=True)
        char_dir = CHAR_DIR / name
        char_dir.mkdir(parents=True, exist_ok=True)
        results = {}

        # Step 1: 面部图
        print(f"  [{name}] Step1/3 生成面部图...", flush=True)
        r = submit_and_wait(char["face_prompt"], images=None, ratio="1:1")
        if r["status"] == "success":
            imgs = download_result(r["submit_id"], char_dir)
            if imgs:
                dst = char_dir / f"{name}_面部.png"
                copy_to_dest(imgs[0], dst)
                results["face"] = str(dst)
                print(f"  面部图完成: {dst}", flush=True)

        # Step 2: 服装图
        print(f"  [{name}] Step2/3 生成服装图...", flush=True)
        r = submit_and_wait(char["outfit_prompt"], images=None, ratio="1:1")
        if r["status"] == "success":
            imgs = download_result(r["submit_id"], char_dir)
            if imgs:
                dst = char_dir / f"{name}_服装.png"
                copy_to_dest(imgs[0], dst)
                results["outfit"] = str(dst)
                print(f"  服装图完成: {dst}", flush=True)

        # Step 3: 六视图
        if results.get("face") and results.get("outfit"):
            print(f"  [{name}] Step3/3 生成六视图...", flush=True)
            r = submit_and_wait(char["six_view_prompt"], images=[results["face"], results["outfit"]], ratio="1:1")
            if r["status"] == "success":
                imgs = download_result(r["submit_id"], char_dir)
                if imgs:
                    dst = char_dir / f"{name}_六视图.png"
                    copy_to_dest(imgs[0], dst)
                    results["six_view"] = str(dst)
                    print(f"  六视图完成: {dst}", flush=True)

        all_results[name] = results
        print(f"  [{name}] 完成: {list(results.keys())}", flush=True)

    # Stage-3: 场景图
    print("\n>>> 处理场景: 寿宴大厅", flush=True)
    SCENE_DIR.mkdir(parents=True, exist_ok=True)
    scene_results = {}

    print(f"  [寿宴大厅] Step1/2 生成大场景...", flush=True)
    r = submit_and_wait(SCENE_PROMPT, images=None, ratio="1:1")
    if r["status"] == "success":
        imgs = download_result(r["submit_id"], SCENE_DIR)
        if imgs:
            dst = SCENE_DIR / "寿宴大厅_大图.png"
            copy_to_dest(imgs[0], dst)
            scene_results["scene"] = str(dst)
            print(f"  大场景完成: {dst}", flush=True)

            # Step 2: 多角度
            print(f"  [寿宴大厅] Step2/2 生成多角度...", flush=True)
            r2 = submit_and_wait(SIX_VIEW_MULTI_PROMPT, images=[str(dst)], ratio="1:1")
            if r2["status"] == "success":
                imgs2 = download_result(r2["submit_id"], SCENE_DIR)
                if imgs2:
                    dst2 = SCENE_DIR / "寿宴大厅_多角度.png"
                    copy_to_dest(imgs2[0], dst2)
                    scene_results["multi"] = str(dst2)
                    print(f"  多角度完成: {dst2}", flush=True)

    # 保存结果
    output_file = PROJECT_DIR / "image_results.json"
    output = {"characters": all_results, "scenes": scene_results}
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存: {output_file}", flush=True)
    print("=" * 50)
    print("全部完成!", flush=True)

    # 发送飞书通知
    try:
        char_list = ", ".join(all_results.keys())
        scene_status = f"✓大场景 {'✓多角度' if scene_results.get('multi') else '✗多角度'}"
        msg = (
            f"【Stage-2 角色图 生成完成】\n\n"
            f"项目：{PROJECT}\n"
            f"角色定妆照：{char_list}\n"
            f"寿宴场景图：{scene_status}\n\n"
            f"图片目录：{CHAR_DIR.parent}/\n\n"
            "请确认后继续下一阶段。"
        )
        subprocess.run(
            ["python3", str(SCRIPT_DIR / "feishu_send.py"), "--message", msg],
            timeout=30
        )
    except Exception as e:
        print(f"飞书通知失败: {e}", flush=True)


if __name__ == "__main__":
    main()
