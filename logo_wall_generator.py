import os
import math
import locale
from PIL import Image, ImageOps
import cairosvg

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

# === MAIN ===
logo_files = sorted([
    os.path.join(LOGO_DIR, f)
    for f in os.listdir(LOGO_DIR)
    if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
], key=lambda x: locale.strxfrm(os.path.basename(x).lower()))

num_logos = len(logo_files)
if num_logos == 0:
    raise ValueError("No supported logo files found in the folder.")

# Determine grid layout
grid_cols = math.ceil(math.sqrt((CANVAS_WIDTH / CANVAS_HEIGHT) * num_logos))
grid_rows = math.ceil(num_logos / grid_cols)
cell_width = (CANVAS_WIDTH - (grid_cols + 1) * PADDING) // grid_cols
cell_height = (CANVAS_HEIGHT - (grid_rows + 1) * PADDING) // grid_rows
cell_size = min(cell_width, cell_height)

canvas = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), BACKGROUND_COLOR)

for index, path in enumerate(logo_files):
    row = index // grid_cols
    col = index % grid_cols
    x = PADDING + col * (cell_size + PADDING)
    y = PADDING + row * (cell_size + PADDING)
    logo_img = load_and_prepare_logo(path, cell_size)
    canvas.paste(logo_img, (x, y))

canvas.save(OUTPUT_FILE)
print(f"Saved logo wall with {num_logos} logos to '{OUTPUT_FILE}'")
