import os
import math
import argparse
from PIL import Image, ImageDraw, ImageFont

# Constants
CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
CHAR_ARRAY = list(CHARS)
CHAR_LENGTH = len(CHAR_ARRAY)
INTERVAL = CHAR_LENGTH / 256
ONE_CHAR_WIDTH = 10
ONE_CHAR_HEIGHT = 18
DEFAULT_SCALE_FACTOR = 0.5
DEFAULT_BG_COLOR = (0, 0, 0)


def get_char(input_int):
    """Map grayscale intensity to ASCII characters."""
    return CHAR_ARRAY[math.floor(input_int * INTERVAL)]


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert image to ASCII art and save as output image."
    )
    parser.add_argument("input_path", type=str, help="Path to the input image")
    parser.add_argument("output_path", type=str, help="Path to save the output image")
    parser.add_argument(
        "--scale_factor",
        type=float,
        default=DEFAULT_SCALE_FACTOR,
        help="Scale factor for the output image size (default: 0.5)",
    )
    parser.add_argument(
        "--bg_color",
        type=int,
        nargs=3,
        default=DEFAULT_BG_COLOR,
        help="Background color as 3 integers representing RGB (default: (0, 0, 0))",
    )
    return parser.parse_args()


def validate_paths(input_path, output_path):
    """Validate input and output paths."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image path '{input_path}' does not exist.")
    if not output_path.endswith(".png"):
        raise ValueError("Output path must be a .png file.")


def process_image_to_ascii(input_path, output_path, scale_factor, bg_color):
    """Convert image to ASCII art and save the output image."""
    # Load image and resize.
    im = Image.open(input_path).convert("RGB")
    im = im.resize(
        (
            int(scale_factor * im.size[0]),
            int(scale_factor * im.size[1] * (ONE_CHAR_WIDTH / ONE_CHAR_HEIGHT)),
        ),
        Image.BILINEAR,
    )
    width, height = im.size
    pixels = im.load()

    # Prepare output image and drawing object
    output_image = Image.new("RGB", (ONE_CHAR_WIDTH * width, ONE_CHAR_HEIGHT * height), color=tuple(bg_color))
    draw = ImageDraw.Draw(output_image)

    # Font setup
    font_path = "/System/Library/Fonts/SFCompact.ttf"  # Adjust for other OS if needed
    fnt = ImageFont.truetype(font_path, 15)

    # Process pixels and generate ASCII art
    for i in range(height):
        for j in range(width):
            r, g, b = pixels[j, i]
            h = int((r + g + b) // 3)
            ascii_char = get_char(h)
            draw.text(
                (j * ONE_CHAR_WIDTH, i * ONE_CHAR_HEIGHT), ascii_char, font=fnt, fill=(r, g, b)
            )

    # Save the output image
    output_image.save(output_path)


def main():
    """Main function to execute the ASCII art generation."""
    args = parse_args()
    validate_paths(args.input_path, args.output_path)
    process_image_to_ascii(args.input_path, args.output_path, args.scale_factor, args.bg_color)


if __name__ == "__main__":
    main()
