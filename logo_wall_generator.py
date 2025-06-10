import os
import math
import locale
from PIL import Image, ImageOps, UnidentifiedImageError
import cairosvg
import gc, sys

# === CONFIG ===
LOGO_DIR = "logos"  # Folder with logos
OUTPUT_FILE = "logo_wall.png"
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080
PADDING = 10  # Space between logos
BACKGROUND_COLOR = (255, 255, 255)  # White
SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".svg")

# === LOCALE CONFIG FOR SORTING ===
locale.setlocale(locale.LC_ALL, '')

# === HELPERS ===
def load_and_prepare_logo(path, size):
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".svg":
            png_path = path + ".converted.png"
            cairosvg.svg2png(url=path, write_to=png_path, unsafe=True)
            img = Image.open(png_path).convert("RGBA")
            os.remove(png_path)
        else:
            img = Image.open(path).convert("RGBA")

        img.thumbnail((size, size), Image.LANCZOS)
        square = Image.new("RGBA", (size, size), BACKGROUND_COLOR + (255,))
        offset = ((size - img.width) // 2, (size - img.height) // 2)
        square.paste(img, offset, mask=img if img.mode == 'RGBA' else None)
        return square.convert("RGB")
    except (UnidentifiedImageError, OSError, Exception) as e:
        return f"{os.path.basename(path)} — {str(e)}"

# === MAIN ===
logo_files = sorted([
    os.path.join(LOGO_DIR, f)
    for f in os.listdir(LOGO_DIR)
    if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
], key=lambda x: locale.strxfrm(os.path.basename(x).lower()))

num_logos_total = len(logo_files)
if num_logos_total == 0:
    raise ValueError("No supported logo files found in the folder.")

# Determine grid layout
grid_cols = math.ceil(math.sqrt((CANVAS_WIDTH / CANVAS_HEIGHT) * num_logos_total))
grid_rows = math.ceil(num_logos_total / grid_cols)
cell_width = (CANVAS_WIDTH - (grid_cols + 1) * PADDING) // grid_cols
cell_height = (CANVAS_HEIGHT - (grid_rows + 1) * PADDING) // grid_rows
cell_size = min(cell_width, cell_height)

canvas = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), BACKGROUND_COLOR)

processed = 0
skipped = []

for index, path in enumerate(logo_files):
    row = index // grid_cols
    col = index % grid_cols
    x = PADDING + col * (cell_size + PADDING)
    y = PADDING + row * (cell_size + PADDING)
    result = load_and_prepare_logo(path, cell_size)
    if isinstance(result, Image.Image):
        canvas.paste(result, (x, y))
        processed += 1
        print(f"✔️ Processed {os.path.basename(path)} ({processed}/{num_logos_total})")
    else:
        skipped.append(result)
        print(f"❌ Skipped {os.path.basename(path)}")

canvas.save(OUTPUT_FILE)
print(f"✅ Saved logo wall with {processed}/{num_logos_total} logos to '{OUTPUT_FILE}'")

if skipped:
    print("\n⚠️ Skipped files:")
    for s in skipped:
        print(f"  - {s}")
gc.collect()
sys.exit(0)