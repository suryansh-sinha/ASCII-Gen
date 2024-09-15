import streamlit as st
from PIL import Image
from ascii_art import process_image_to_ascii
import os

st.title("VisualGlyph: Convert Images to ASCII Art!")

# Upload an image file
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

# User input for scale factor, font size, and background color
scale_factor = st.slider("Scale Factor", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
font_size = st.slider("Font Size", min_value=1, max_value=25, value=10, step=1)
bg_color = st.color_picker("Background Color", value='#000000')
bg_color_rgb = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))

# When an image is uploaded
if uploaded_file is not None:
    input_image = Image.open(uploaded_file)
    st.image(input_image, caption="Uploaded Image", use_column_width=True)

    output_path = "output_ascii_image.png"
    
    # Convert the image to ASCII art when the button is pressed
    if st.button("Convert to ASCII Art"):
        input_path = "uploaded_image.png"
        input_image.save(input_path)

        process_image_to_ascii(input_path, output_path, scale_factor, bg_color_rgb, font_size)
        
        st.image(output_path, caption="Generated ASCII Art", use_column_width=True)

        with open(output_path, "rb") as file:
            st.download_button(
                label="Download ASCII Art",
                data=file,
                file_name="ascii_art.png",
                mime="image/png"
            )
