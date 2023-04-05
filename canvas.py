from PIL import Image

# Open the transparent image
img = Image.open("d.PNG")

# Create a new image with a white background
background = Image.new("RGBA", img.size, (255, 255, 255, 255))

# Paste the transparent image onto the white background
background.paste(img, mask=img)

# Save the resulting image
background.save("white_background_image.png")