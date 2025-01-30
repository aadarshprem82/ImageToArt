from PIL import Image
import numpy as np

# Function to map grayscale pixel value to a symbol
def pixel_to_symbol(value, symbols):
    # Map the pixel value to the symbol range
    symbol_index = int(value / 255 * (len(symbols) - 1))
    return symbols[symbol_index]

# Load the image
image_path = 'Doodle1.jpg'  # replace with your image path
image = Image.open(image_path)

# Resize image to fit the desired output (optional)
width, height = image.size
aspect_ratio = height / width
new_width = 100  # Choose a desired width for the output
new_height = int(aspect_ratio * new_width * 0.55)  # Adjust height to maintain aspect ratio
image = image.resize((new_width, new_height))

# Convert image to grayscale
grayscale_image = image.convert('L')  # 'L' mode for grayscale

# Convert image to numpy array
image_array = np.array(grayscale_image)

# Define the symbol set
symbols = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

# Create the ASCII art output
ascii_art = ""
for row in image_array:
    for pixel in row:
        ascii_art += pixel_to_symbol(pixel, symbols)
    ascii_art += '\n'

# Save or print the result
# print(ascii_art)
with open("ascii_art.txt", "w") as f:
    f.write(ascii_art)