from PIL import Image, ImageDraw, ImageFont
import math

# Constants
CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZ*#MW&8%B@$"
CHAR_ARRAY = list(CHARS)
CHAR_LENGTH = len(CHAR_ARRAY)
INTERVAL = CHAR_LENGTH / 256

def get_char(input_int):
    """Map grayscale intensity to ASCII characters."""
    return CHAR_ARRAY[math.floor(input_int * INTERVAL)]

def process_image_to_ascii(input_path, output_path, scale_factor, bg_color, font_size):
    """Convert image to ASCII art and save the output image."""
    
    # Font setup
    font_path = './fonts/Courier.ttf'  # Ensure you have this font or use an available system font
    font = ImageFont.truetype(font_path, font_size)
    
    # Dynamically getting the character width and height
    bbox = font.getbbox(get_char(128))    # Use medium intensity character to estimate fontsize.
    char_width = bbox[2] - bbox[0]  # right - left
    char_height = bbox[3] - bbox[1] # bottom - top
    
    # Load the image and get its size
    im = Image.open(input_path).convert("RGB")
    input_width, input_height = im.size

    # Calculate the number of characters to fit based on the image size and font dimensions
    output_width = int(input_width * scale_factor / char_width)
    output_height = int(input_height * scale_factor / char_height)

    # Resize the input image to match the output character grid
    im = im.resize((output_width, output_height), Image.Resampling.LANCZOS)
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
                (j * char_width, i * char_height), ascii_char, font=font, fill=(r, g, b)
            )

    # Save the output image
    output_image.save(output_path)
