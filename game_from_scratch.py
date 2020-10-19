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

# Create abstract class for ships
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
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50), 0)


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

    ship = Ship(WIDTH / 2, HEIGHT - 100)

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

        ship.draw(WINDOW)
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
        if keys[pygame.K_LEFT]:
            ship.x -= player_velocity
        if keys[pygame.K_RIGHT]:
            ship.x += player_velocity
        if keys[pygame.K_UP]:
            ship.y -= player_velocity
        if keys[pygame.K_DOWN]:
            ship.y += player_velocity


main()