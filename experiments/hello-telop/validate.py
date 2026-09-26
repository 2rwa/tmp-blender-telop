from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageStat


OUTPUT_DIR = Path.cwd() / "output"
RENDER_PATH = OUTPUT_DIR / "render.png"


def main() -> None:
    if not RENDER_PATH.is_file():
        raise SystemExit(f"render missing: {RENDER_PATH}")

    size_bytes = RENDER_PATH.stat().st_size
    if size_bytes < 4_000:
        raise SystemExit(f"render suspiciously small: {size_bytes} bytes")

    with Image.open(RENDER_PATH) as image:
        image.load()
        if image.size != (1280, 720):
            raise SystemExit(f"unexpected render size: {image.size}")

        rgb = image.convert("RGB")
        gray = rgb.convert("L")
        stddev = float(ImageStat.Stat(gray).stddev[0])

        center = gray.crop((250, 220, 1030, 500))
        bright_pixels = sum(1 for value in center.getdata() if value >= 150)

        tiny = rgb.resize((64, 36))
        colors = tiny.getcolors(maxcolors=64 * 36)
        unique_colors = len(colors) if colors is not None else 64 * 36

    if stddev < 8.0:
        raise SystemExit(f"render looks too uniform: stddev={stddev:.3f}")
    if bright_pixels < 2500:
        raise SystemExit(f"Hello world text was not detected: bright_pixels={bright_pixels}")
    if unique_colors < 8:
        raise SystemExit(f"render has too little visual variation: {unique_colors} colors")

    result = {
        "path": str(RENDER_PATH),
        "size_bytes": size_bytes,
        "width": 1280,
        "height": 720,
        "luminance_stddev": round(stddev, 3),
        "hello_bright_pixels": bright_pixels,
        "unique_colors_64x36": unique_colors,
        "sha256": hashlib.sha256(RENDER_PATH.read_bytes()).hexdigest(),
    }
    (OUTPUT_DIR / "validation.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
