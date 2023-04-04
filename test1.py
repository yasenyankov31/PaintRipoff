import pygame
from PIL import Image, ImageDraw

width = 400
height = 300
image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

# Draw a rectangle on the image
draw = ImageDraw.Draw(image)
draw.rectangle((50, 50, 150, 150), fill=(255, 0, 0, 255), outline=(0, 0, 0, 255))

# Save the image to a file (optional)
image.save("rectangle.png")
# Load the image
image = pygame.image.load("rectangle.png")

# Rotate the image
rotated_image = pygame.transform.rotate(image, 45)

# Define Ellipse class
class Shape:
    def __init__(self, x, y, width, height, color, border_width=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.border_width = border_width

    def draw(self, surface):
        #pygame.draw.ellipse(surface, self.color, (self.x, self.y, self.width, self.height), self.border_width)
        screen.blit(rotated_image, (self.x, self.y))

    def contains_point(self, x, y):
        # Check if point (x, y) is within ellipse bounds
        a = self.width / 2
        b = self.height / 2
        center_x = self.x + a
        center_y = self.y + b
        if ((x - center_x) ** 2) / (a ** 2) + ((y - center_y) ** 2) / (b ** 2) <= 1:
            return True
        else:
            return False
        
# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height),pygame.RESIZABLE)

# Set up the ellipse
shape_x = 0
shape_y = 0
shape_width = 0
shape_height = 0
shape_color = (0, 0, 0)

# Set up the drawing flag
drawing = False


shapes=[]


# Run the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit the game
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Start drawing the ellipse
            drawing = True
            shape_x, shape_y = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            # Stop drawing the ellipse
            drawing = False
            if shape_width > 0 and shape_height > 0:
                new_shape=Shape(shape_x, shape_y, shape_width, shape_height, shape_color)
                shapes.append(new_shape)
                #pygame.draw.ellipse(screen, shape_color, (shape_x, shape_y, shape_width, shape_height), 1)
            if shape_width < 0 and shape_height < 0:
                new_shape=Shape(shape_x + shape_width, shape_y + shape_height, abs(shape_width), abs(shape_height), shape_color)
                shapes.append(new_shape)
                #pygame.draw.ellipse(screen, shape_color, (shape_x + shape_width, shape_y + shape_height, abs(shape_width), abs(shape_height)), 1)    
            elif shape_width < 0:
                new_shape=Shape(shape_x + shape_width, shape_y, abs(shape_width), shape_height, shape_color)
                shapes.append(new_shape)
                #pygame.draw.ellipse(screen, shape_color, (shape_x + shape_width, shape_y, abs(shape_width), shape_height), 1)
            elif  shape_height < 0:
                new_shape=Shape(shape_x, shape_y + shape_height, shape_width, abs(shape_height), shape_color)
                shapes.append(new_shape)
                #pygame.draw.ellipse(screen, shape_color, (shape_x, shape_y + shape_height, shape_width, abs(shape_height)), 1)

            shape_width = 0
            shape_height = 0
        elif event.type == pygame.MOUSEMOTION:
            # Update the ellipse size while drawing
            if drawing:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                shape_width = mouse_x - shape_x
                shape_height = mouse_y - shape_y

    # Draw the screen
    screen.fill((255, 255, 255))
    if drawing:
        if shape_width > 0 and shape_height > 0:
            pygame.draw.ellipse(screen, shape_color, (shape_x, shape_y, shape_width, shape_height), 1)
        if shape_width < 0 and shape_height < 0:
            pygame.draw.ellipse(screen, shape_color, (shape_x + shape_width, shape_y + shape_height, abs(shape_width), abs(shape_height)), 1)    
        elif shape_width < 0:
            pygame.draw.ellipse(screen, shape_color, (shape_x + shape_width, shape_y, abs(shape_width), shape_height), 1)
        elif  shape_height < 0:
            pygame.draw.ellipse(screen, shape_color, (shape_x, shape_y + shape_height, shape_width, abs(shape_height)), 1)
    
    for shape in shapes:
        shape.draw(screen)
   
    pygame.display.flip()