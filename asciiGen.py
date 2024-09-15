import os
import math
import argparse
from PIL import Image, ImageDraw, ImageFont

# Constants
CHARS = "  .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZ*#MW&8%B@$"
CHAR_ARRAY = list(CHARS)
CHAR_LENGTH = len(CHAR_ARRAY)
INTERVAL = CHAR_LENGTH / 256
DEFAULT_SCALE_FACTOR = 1.0
DEFAULT_BG_COLOR = (0, 0, 0)
DEFAULT_FONT_SIZE = 10


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
        help="Scale factor for the output image size (default: 1.0)",
    )
    parser.add_argument(
        "--bg_color",
        type=int,
        nargs=3,
        default=DEFAULT_BG_COLOR,
        help="Background color as 3 integers representing RGB (default: (0, 0, 0))",
    )
    parser.add_argument(
        '--font_size',
        type=int,
        default=DEFAULT_FONT_SIZE,
        help="Font size of characters in the ASCII Image (default: 10)")
    return parser.parse_args()


def validate_paths(input_path, output_path):
    """Validate input and output paths."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image path '{input_path}' does not exist.")
    if not output_path.endswith(".png"):
        raise ValueError("Output path must be a .png file.")


def process_image_to_ascii(input_path, output_path, scale_factor, bg_color, font_size):
    """Convert image to ASCII art and save the output image."""
    
    # Font setup
    font_path = './fonts/Courier.ttf'
    fnt = ImageFont.truetype(font_path, font_size)
    
    # Dynamically getting the character width and height
    bbox = fnt.getbbox(get_char(128))    # Use medium intensity character to estimate fontsize.
    # bbox --> (left, top, right, bottom)
    char_width = bbox[2] - bbox[0]  # right - left
    char_height = bbox[3] - bbox[1] # bottom - top
    
    # Load the image and get its size
    im = Image.open(input_path).convert("RGB")
    input_width, input_height = im.size

    # Calculate the number of characters to fit based on the image size and font dimensions
    output_width = int(input_width * scale_factor / char_width)
    output_height = int(input_height * scale_factor / char_height)

    # Resize the input image to match the output character grid
    im = im.resize((output_width, output_height), Image.BILINEAR)
    pixels = im.load()

    # Prepare output image and drawing object
    output_image = Image.new("RGB", (char_width * output_width, char_height * output_height), color=tuple(bg_color))
    draw = ImageDraw.Draw(output_image)

    # Process pixels and generate ASCII art
    for i in range(output_height):
        for j in range(output_width):
            r, g, b = pixels[j, i]
            h = int((r + g + b) // 3)
            ascii_char = get_char(h)
            draw.text(
                (j * char_width, i * char_height), ascii_char, font=fnt, fill=(r, g, b)
            )

    # Save the output image
    output_image.save(output_path)


def main():
    """Main function to execute the ASCII art generation."""
    args = parse_args()
    validate_paths(args.input_path, args.output_path)
    process_image_to_ascii(args.input_path, args.output_path, args.scale_factor, args.bg_color, args.font_size)


if __name__ == "__main__":
    main()
