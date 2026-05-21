#!/usr/bin/env python3
"""
stitch_grid.py - 分镜宫格图拼合工具

用法：
  python stitch_grid.py \
    --panels "/path/to/p1.png,/path/to/p2.png,/path/to/p3.png" \
    --layout "3x3" \
    --output "/path/to/grid.png" \
    --border 6

支持布局：
  1x1, 2x1, 3x1, 2x2, 3x2, 3x3, 2x3
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("需要安装 Pillow: pip install Pillow", file=sys.stderr)
    sys.exit(1)

# 默认每格尺寸（像素）
DEFAULT_PANEL_W = 1280
DEFAULT_PANEL_H = 720
BORDER = 6  # 白边宽度


def load_image(path: str) -> Image.Image:
    """加载图片，统一转为RGB"""
    img = Image.open(path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    return img


def resize_to_fit(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """缩放图片使其适应目标尺寸（保持比例，填满）"""
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h

    if img_ratio > target_ratio:
        # 图片更宽，以宽度为准缩放
        new_w = target_w
        new_h = int(target_w / img_ratio)
    else:
        # 图片更高，以高度为准缩放
        new_h = target_h
        new_w = int(target_h * img_ratio)

    return img.resize((new_w, new_h), Image.LANCZOS)


def parse_layout(layout: str) -> tuple:
    """解析布局字符串，如 '3x3' -> (3, 3)"""
    parts = layout.lower().split("x")
    if len(parts) != 2:
        raise ValueError(f"布局格式无效: {layout}，应为如 3x3")
    return int(parts[0]), int(parts[1])


def stitch(panels: list, layout: str, output: str, panel_w: int = DEFAULT_PANEL_W, panel_h: int = DEFAULT_PANEL_H, border: int = BORDER):
    """
    将分镜格图拼合成宫格图
    """
    cols, rows = parse_layout(layout)
    required = cols * rows
    if len(panels) < required:
        print(f"警告: 布局 {layout} 需要 {required} 张图，当前只有 {len(panels)} 张", file=sys.stderr)
        print(f"用空白图补齐", file=sys.stderr)
        # 补充空白图
        blank = Image.new("RGB", (panel_w, panel_h), (200, 200, 200))
        while len(panels) < required:
            panels.append(blank)

    # 计算画布尺寸
    total_w = cols * panel_w + (cols + 1) * border
    total_h = rows * panel_h + (rows + 1) * border
    canvas = Image.new("RGB", (total_w, total_h), (255, 255, 255))

    for idx, panel_path in enumerate(panels[:required]):
        row = idx // cols
        col = idx % cols

        # 加载并缩放图片
        if isinstance(panel_path, str) and Path(panel_path).exists():
            img = load_image(panel_path)
            img = resize_to_fit(img, panel_w, panel_h)
        else:
            img = Image.new("RGB", (panel_w, panel_h), (220, 220, 220))

        # 计算放置位置（居中，带白边）
        x = border + col * (panel_w + border) + (panel_w - img.width) // 2
        y = border + row * (panel_h + border) + (panel_h - img.height) // 2

        canvas.paste(img, (x, y))

    canvas.save(output, "PNG")
    print(f"宫格图已保存: {output} ({cols}x{rows}, {total_w}x{total_h})", file=sys.stderr)
    return output


def main():
    parser = argparse.ArgumentParser(description="分镜宫格图拼合")
    parser.add_argument("--panels", required=True, help="图片路径，逗号分隔")
    parser.add_argument("--layout", required=True, help="布局，如 3x3")
    parser.add_argument("--output", required=True, help="输出路径")
    parser.add_argument("--panel_w", type=int, default=DEFAULT_PANEL_W, help=f"每格宽度（默认{DEFAULT_PANEL_W}）")
    parser.add_argument("--panel_h", type=int, default=DEFAULT_PANEL_H, help=f"每格高度（默认{DEFAULT_PANEL_H}）")
    parser.add_argument("--border", type=int, default=BORDER, help=f"白边宽度（默认{BORDER}）")

    args = parser.parse_args()

    panels = [p.strip() for p in args.panels.split(",")]
    stitch(panels, args.layout, args.output, args.panel_w, args.panel_h, args.border)
    print(args.output)


if __name__ == "__main__":
    main()
