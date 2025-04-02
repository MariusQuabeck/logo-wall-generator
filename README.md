# Logo Wall Generator 🧱🖼️

Generate a clean, padded 1920×1080 logo wall from assorted image files — perfect for associations, events, and sponsor showcases.

## Features

- 🖼️ Fixed output size: 1920x1080
- 🧩 Automatically arranges logos in a grid with padding
- 📂 Supports `.png`, `.jpg`, `.jpeg`, `.webp`, and `.svg` formats
- 🧭 Logos sorted alphabetically by filename
- 🧼 Preserves logo aspect ratios with white padding background
- 🔁 Easy to update — just change files in the `logos/` folder and rerun

## Installation

Install Python dependencies:

```bash
pip install pillow cairosvg
```

On macOS, you may also need the following system libraries for `cairosvg`:

```bash
brew install cairo pango gdk-pixbuf libffi
```

## Usage

1. Place all logo files into a folder named `logos/` (same directory as the script).
2. Run the script:

```bash
python logo_wall_generator.py
```

3. The output image will be saved as `logo_wall.png` in the current directory.

## Example Output

Here’s a preview of a generated logo wall (230 logos):

![Example output](example_output.png)

## Customization

You can tweak the following parameters in the script:

- `CANVAS_WIDTH` / `CANVAS_HEIGHT` — size of the output image
- `PADDING` — spacing between logos
- `BACKGROUND_COLOR` — RGB tuple (default is white)

## License

This project is licensed under the **GNU GPL v3**.  
See the [LICENSE](LICENSE) file for details.
