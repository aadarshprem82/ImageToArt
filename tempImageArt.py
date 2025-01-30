from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np

# Function to map grayscale pixel value to a symbol
def pixel_to_symbol(value, symbols):
    symbol_index = int(value / 255 * (len(symbols) - 1))
    return symbols[symbol_index]

# Load the image
image_path = 'Doodle.png'  # replace with your image path
image = Image.open(image_path)

# Resize image to fit the desired output (optional)
width, height = image.size
aspect_ratio = height / width
new_width = 100  # Choose a desired width for the output
new_height = int(aspect_ratio * new_width * 0.55)  # Adjust height to maintain aspect ratio
image = image.resize((new_width, new_height))

# Convert image to grayscale
image = image.convert('L')  # 'L' mode for grayscale

image = ImageEnhance.Contrast(image).enhance(1.5)

# Convert image to numpy array
image_array = np.array(image)

# Define the symbol set
symbols = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

# Create the ASCII art string
ascii_art = ""
for row in image_array:
    for pixel in row:
        ascii_art += pixel_to_symbol(pixel, symbols)
    ascii_art += '\n'

# Create a new blank image for the ASCII art
# font = ImageFont.load_default()  # Load a default font
font = ImageFont.truetype("fonts/consolab.ttf")
font_width, font_height = font.getsize('A')  # Get the size of a character
image_width = font_width * new_width  # Width of the image in pixels
image_height = font_height * new_height  # Height of the image in pixels

# Create a white canvas
ascii_image = Image.new('RGB', (image_width, image_height), (255, 255, 255))
draw = ImageDraw.Draw(ascii_image)

# Render the ASCII art text onto the image
y_position = 0
for row in ascii_art.split('\n'):
    draw.text((0, y_position), row, fill=(0, 0, 0), font=font)
    y_position += font_height

# Save the ASCII art image
ascii_image.save('ascii_art_image.png')

# Optionally, show the result
ascii_image.show()
