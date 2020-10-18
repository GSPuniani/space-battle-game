################################################################################
# INSTRUCTIONS:
# Complete the TODOS below to add another "enemy" character. When the player 
# collides with the enemy, it should reset points to 0.
# 
# STRETCH CHALLENGES (complete if you've already finished the main challenge):
# 1. Add a "You Lose" screen that shows for 2 seconds if the player collides
#    with an enemy.
# 2. Create multiple enemies that can all fall at once.
################################################################################

# YouTube video timer: 0:06:31

import pygame
import random

# Initialize Pygame
pygame.init()
pygame.display.set_caption('Space Battle!')

################################################################################
# VARIABLES
################################################################################

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

CHARACTER_WIDTH = 40
CHARACTER_HEIGHT = 40

# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set player to middle of the bottom
player_x = SCREEN_WIDTH / 2
player_y = SCREEN_HEIGHT - CHARACTER_HEIGHT


# Add variables for the "Enemy" class
class Enemy():
    """
    A class of enemy objects that the user should avoid colliding into
    """
    def __init__(self):
        """Position the incoming enemy at a random spot"""
        self.x = random.random() * (SCREEN_WIDTH - SCREEN_HEIGHT)
        self.y = 300

# Instantiate Enemy class twice
enemy1 = Enemy()
enemy2 = Enemy()

# Other variables
velocity = 3
points = 0

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


################################################################################
# HELPER FUNCTIONS
################################################################################

def is_colliding(x1, y1, x2, y2, width, height):
    """Returns True if two rectangles are colliding, or False otherwise"""
    # If one rectangle is on left side of the other 
    if (x1 >= x2 + width) or (x2 >= x1 + width):
        return False
  
    # If one rectangle is above the other
    if (y1 >= y2 + height) or (y2 >= y1 + height):
        return False
  
    return True

def draw_text(text, color, font_size, x, y):
    font = pygame.font.SysFont(None, font_size)
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Define a function for resetting an enemy object once it has collided or passed off screen
def resetEnemy(enemy, screenWidth, characterWidth):
    enemy.y = 0
    enemy.x = random.random() * (screenWidth - characterWidth)

################################################################################
# GAME LOOP
################################################################################

# Run until the user asks to quit
running = True
while running:
    # Advance the clock
    pygame.time.delay(20)

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Update the player
    if keys[pygame.K_LEFT]:
        player_x -= velocity
    if keys[pygame.K_RIGHT]:
        player_x += velocity

    # Update the enemy y-positions based on its velocity
    enemy1.y += velocity
    enemy2.y += velocity


    # If enemy went off the screen, reset it
    if enemy1.y > SCREEN_HEIGHT: 
        resetEnemy(enemy1, SCREEN_WIDTH, CHARACTER_WIDTH)
    if enemy2.y > SCREEN_HEIGHT: 
        resetEnemy(enemy2, SCREEN_WIDTH, CHARACTER_WIDTH)


    # If player collides with enemy, reset it & set points to 0
    if is_colliding(player_x, player_y, enemy1.x, enemy1.y, CHARACTER_WIDTH, CHARACTER_HEIGHT):
        points -= 10
        resetEnemy(enemy1, SCREEN_WIDTH, CHARACTER_WIDTH)
    if is_colliding(player_x, player_y, enemy2.x, enemy2.y, CHARACTER_WIDTH, CHARACTER_HEIGHT):
        points -= 10
        resetEnemy(enemy2, SCREEN_WIDTH, CHARACTER_WIDTH)

    # Fill screen with white
    screen.fill(WHITE)

    # Draw the player as a blue square
    pygame.draw.rect(screen, BLUE, (player_x, player_y, CHARACTER_WIDTH, CHARACTER_HEIGHT))


    # Draw each enemy as a red square
    pygame.draw.rect(screen, RED, (enemy1.x, enemy1.y, CHARACTER_WIDTH, CHARACTER_HEIGHT))
    pygame.draw.rect(screen, RED, (enemy2.x, enemy2.y, CHARACTER_WIDTH, CHARACTER_HEIGHT))


    # Draw the points
    draw_text(text=f'Points: {points}', color=BLACK, font_size=24, x=20, y=20)

    # Update the game display
    pygame.display.update()

# Done! Time to quit.
pygame.quit()