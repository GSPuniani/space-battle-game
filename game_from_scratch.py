# Import modules
import pygame
import os
import time
import random


# Initialize the font
pygame.font.init()

# Set display
WIDTH, HEIGHT = 750, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle")

# Load images for spaceships, lasers, and background
# Enemy ships
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))

# Main player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background scaled to fit entire screen
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# Create abstract class for player and enemy ship classes to inherit
class Ship:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

# Create a class for the player ship
class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        # Define mask to be pixel-perfect
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

# Create a class for the enemy ships
class Enemy(Ship):
    # Define a dictionary for the color styles of the enemy ships
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER)
    }

    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        # Define mask to be pixel-perfect
        self.mask = pygame.mask.from_surface(self.ship_img)

    # Define downward movement for enemy ship
    def move(self, velocity):
        self.y += velocity



# Main function
def main():
    run = True
    # Frames per second
    FPS = 60
    level = 1
    lives = 5
    player_velocity = 5
    # Font
    main_font = pygame.font.Font(os.path.join("assets", "nasalization-rg.ttf"), 50)

    # Initialize a player ship by instantiating a Player object
    player = Player(WIDTH / 2, HEIGHT - 100)

    # Clock object
    clock = pygame.time.Clock()


    # Below are functions defined here within main() since they use other variables defined in main()

    def redraw_window():
        WINDOW.blit(BG, (0,0))
        # Draw text for level and lives labels and place them on the top corners
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 100, 0))
        level_label = main_font.render(f"Level: {level}", 1, (255, 100, 0))
        WINDOW.blit(lives_label, (WIDTH - lives_label.get_width() - 20, 15))
        WINDOW.blit(level_label, (20, 15))

        player.draw(WINDOW)
        pygame.display.update()

    while run:
        # Run game at consistent speed across all computers
        clock.tick(FPS)
        # Update all of the display surfaces
        redraw_window()

        # Quit game when user clicks exit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Dictionary for key presses
        keys = pygame.key.get_pressed()
        # Move keys with arrows and keep player within the bounds of the screen
        if keys[pygame.K_LEFT] and player.x - player_velocity > 0:
            player.x -= player_velocity
        if keys[pygame.K_RIGHT] and player.x + player_velocity + player.get_width() < WIDTH:
            player.x += player_velocity
        if keys[pygame.K_UP] and player.y - player_velocity > 0:
            player.y -= player_velocity
        if keys[pygame.K_DOWN] and player.y + player_velocity + player.get_height() < HEIGHT:
            player.y += player_velocity


main()