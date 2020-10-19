# Import modules
import pygame
import os
import time
import random


# Initialize the font
pygame.font.init()

# Set display
WIDTH, HEIGHT = 900, 750
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
    # Define a constant variable for the cooldown to be half a second (30/60 FPS)
    COOLDOWN = 30

    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    # Draw the ship to the screen
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    # Move laser by its velocity, and remove laser if it disappears offscreen or collides with an object
    # Decrement the player health by 10 if an enemy laser hits it
    def move_lasers(self, velocity, obj):
        # Increment cooldown
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
    
    # Cooldown counter increments until 30 (constant value) and then resets
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # Shooting lasers with a Laser object
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

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

    # Override the inherited move_lasers() function from the parent class
    # Move laser by its velocity, and remove laser if it disappears offscreen or collides with an object
    # Remove the enemy object if the player's laser hits it
    def move_lasers(self, velocity, objs):
        # Increment cooldown
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)


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


# Create a class for the lasers
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(img)

    # Draw the laser to the screen
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # Input velocity will be negative so that the laser shoots upward
    def move(self, velocity):
        self.y += velocity

    # Boolean value for whether the laser is withing the bounds of the screen
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    # Boolean value for whether a collision with an object occurred
    def collision(self, obj):
        return collide(self, obj)

def collide(obj1, obj2):
    # Calculate distances between the two input objects
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    # Return intersection of the masks of the two objects overlap based on offset values
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# Main function
def main():
    run = True
    # Frames per second
    FPS = 60
    level = 0
    lives = 5
    player_velocity = 5
    # Font
    main_font = pygame.font.Font(os.path.join("assets", "nasalization-rg.ttf"), 50)
    # Font for "lost" screen
    lost_font = pygame.font.Font(os.path.join("assets", "nasalization-rg.ttf"), 65)

    # Set a Boolean for the "lost" status
    lost = False
    # Set count-down timer for "lost" status before resetting
    lost_counter = 0

    enemies = []
    # Number of enemies in a given wave
    wave_amount = 5
    enemy_veloctiy = 1

    laser_velocity = 5

    # Initialize a player ship by instantiating a Player object
    player = Player(int(WIDTH / 2), HEIGHT - 100)

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

        # Draw the enemy ships
        for enemy in enemies:
            enemy.draw(WINDOW)

        # Draw the player ship after the enemy ships so it will appear over them if it overlaps with any of them
        player.draw(WINDOW)

        if lost:
            lost_label = lost_font.render("Game Over! You Lost!!", 1, (255, 0, 0))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2))
        
        pygame.display.update()

    while run:
        # Run game at consistent speed across all computers
        clock.tick(FPS)

        # Update all of the display surfaces
        redraw_window()

        # The player loses when all lives are spent or the health bar is depleted
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_counter += 1

        # Stop running the game if the "lost" message appears for more than 3 seconds
        if lost:
            if lost_counter > FPS * 3:
                run = False
            else:
                continue


        if len(enemies) == 0:
            level += 1
            wave_amount += 5
            for i in range(wave_amount):
                enemy = Enemy(random.randint(10, WIDTH - 100), random.randint(-2000, -150), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

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
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Loop through a copy of the enemies list to modify the original list directly
        for enemy in enemies[:]:
            # Move enemies according to their velocity
            enemy.move(enemy_veloctiy)
            # Move the lasers from the enemies to attack the player
            enemy.move_lasers(laser_velocity, player)
            # Select a time (such as once every 3 seconds) for how often each enemy should fire a laser
            if random.randrange(0, 3 * FPS) == 1:
                enemy.shoot()
            # Decrement the lives when an enemy passes the lower boundary of the screen and modify the enemies list
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        # Move the lasers from the player to attack the enemies
        player.move_lasers(-laser_velocity, enemies)



main()