# Import modules
import pygame
import os
import time
import random


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

# Background
BG = pygame.image.load(os.path.join("assets", "background-black.png"))


# Main function
def main():
    run = True
    # Frames per second
    FPS = 60

    # Clock object
    clock = pygame.time.Clock()

    while run:
        # Run game at consistent speed across all computers
        clock.tick(FPS)

        # Quit game when user clicks exit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


main()