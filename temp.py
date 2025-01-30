from PIL import Image, ImageDraw, ImageFont

# Create an image with white background
width, height = 800, 100
image = Image.new('RGB', (width, height), color = (255, 255, 255))

# Get default font
font = ImageFont.load_default()

# Create a drawing context
draw = ImageDraw.Draw(image)

# Define the text to display
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

# Start drawing the text
x, y = 10, 20
for letter in alphabet:
    draw.text((x, y), letter, font=font, fill=(0, 0, 0))
    x += font.getsize(letter)[0] + 2  # Move x position after each letter
    if x > width - 100:  # If we exceed the width, move to the next line
        x = 10
        y += font.getsize(letter)[1] + 2

# Save or show the image
image.show()
# image.save("alphabet_image.png")
