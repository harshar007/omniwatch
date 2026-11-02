"""Generate high-resolution Omnitrix icon files (.ico and .png)."""

from pathlib import Path
from PIL import Image, ImageDraw

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def draw_omnitrix(size: int = 512) -> Image.Image:
    """Render a crisp vector-style Omnitrix dial emblem."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size / 2, size / 2
    r_outer = size * 0.46
    r_bezel = size * 0.42
    r_core = size * 0.35

    # 1. Outer metallic chassis ring (Dark titanium)
    draw.ellipse(
        [cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer],
        fill=(14, 22, 17, 255),
        outline=(38, 74, 52, 255),
        width=int(size * 0.03),
    )

    # 2. Glowing inner ring
    draw.ellipse(
        [cx - r_bezel, cy - r_bezel, cx + r_bezel, cy + r_bezel],
        fill=(5, 16, 9, 255),
        outline=(0, 255, 85, 200),
        width=int(size * 0.02),
    )

    # 3. Outer notches (12 watch bezel notches)
    import math
    for i in range(12):
        angle = i * (2 * math.pi / 12)
        x1 = cx + (r_outer - size * 0.015) * math.cos(angle)
        y1 = cy + (r_outer - size * 0.015) * math.sin(angle)
        x2 = cx + (r_outer - size * 0.05) * math.cos(angle)
        y2 = cy + (r_outer - size * 0.05) * math.sin(angle)
        color = (0, 255, 85, 255) if i % 3 == 0 else (14, 133, 63, 200)
        draw.line([x1, y1, x2, y2], fill=color, width=int(size * 0.02))

    # 4. Deep core face (Black base)
    draw.ellipse(
        [cx - r_core, cy - r_core, cx + r_core, cy + r_core],
        fill=(6, 10, 8, 255),
        outline=(0, 255, 85, 255),
        width=int(size * 0.018),
    )

    # 5. Iconic Omnitrix Hourglass (Neon green triangles)
    tri_w = r_core * 0.95
    tri_h = r_core * 0.95
    # Top triangle (pointing down into center)
    top_tri = [
        (cx - tri_w, cy - tri_h),
        (cx + tri_w, cy - tri_h),
        (cx, cy),
    ]
    # Bottom triangle (pointing up into center)
    bot_tri = [
        (cx - tri_w, cy + tri_h),
        (cx + tri_w, cy + tri_h),
        (cx, cy),
    ]

    # Draw neon green hourglass triangles with dark green border
    draw.polygon(top_tri, fill=(0, 255, 85, 255), outline=(112, 255, 148, 255))
    draw.polygon(bot_tri, fill=(0, 255, 85, 255), outline=(112, 255, 148, 255))

    # 6. Center core circular pivot
    r_pivot = r_core * 0.22
    draw.ellipse(
        [cx - r_pivot, cy - r_pivot, cx + r_pivot, cy + r_pivot],
        fill=(6, 10, 8, 255),
        outline=(0, 255, 85, 255),
        width=int(size * 0.02),
    )
    # Inner glowing dot
    r_dot = r_pivot * 0.4
    draw.ellipse(
        [cx - r_dot, cy - r_dot, cx + r_dot, cy + r_dot],
        fill=(112, 255, 148, 255),
    )

    return img


def main() -> None:
    img = draw_omnitrix(512)
    png_path = ASSETS_DIR / "omnitrix.png"
    ico_path = ASSETS_DIR / "omnitrix.ico"

    img.save(png_path, format="PNG")
    print(f"[+] Saved PNG icon: {png_path}")

    # Generate multi-size .ico
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save(ico_path, format="ICO", sizes=sizes)
    print(f"[+] Saved multi-resolution ICO icon: {ico_path}")


if __name__ == "__main__":
    main()
