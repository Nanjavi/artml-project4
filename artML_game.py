import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300
PLAYER_SIZE = 50
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 50
GRAVITY = 0.5
JUMP_FORCE = -10
JUMP_HOLD_FORCE = -0.5  # Additional force applied while holding spacebar
FLYING_OBJECT_WIDTH = 20
FLYING_OBJECT_HEIGHT = 20
OBJ_RATE = 0.02
FLY_RATE = 0.005

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Luna in Flight")

# Load player images
player_image1 = pygame.image.load("img_materials/luna_run1.png").convert_alpha()  # Load custom player image
player_image1 = pygame.transform.scale(player_image1, (PLAYER_SIZE, PLAYER_SIZE))  # Scale image to match player size
player_image2 = pygame.image.load("img_materials/luna_fly1.png").convert_alpha()  # Load alternative player image
player_image2 = pygame.transform.scale(player_image2, (PLAYER_SIZE, PLAYER_SIZE))  # Scale image to match player size
player_image3 = pygame.image.load("img_materials/luna_run2.png").convert_alpha()  # Load alternative player image
player_image3 = pygame.transform.scale(player_image3, (PLAYER_SIZE, PLAYER_SIZE))  # Scale image to match player size
player_image4 = pygame.image.load("img_materials/luna_fly2.png").convert_alpha()  # Load alternative player image
player_image4 = pygame.transform.scale(player_image4, (PLAYER_SIZE, PLAYER_SIZE))  # Scale image to match player size
player_image_onrun = 0

# Load obstacle images
obstacle_images = []
obstacle_images.append(pygame.image.load("img_materials/obstacle1.png").convert_alpha())  # Load obstacle image 1
obstacle_images.append(pygame.image.load("img_materials/obstacle2.png").convert_alpha())  # Load obstacle image 2

# Load flying object images
flying_object_images = []
flying_object_images.append(pygame.image.load("img_materials/obstacle1.png").convert_alpha())  # Load flying object image 1
flying_object_images.append(pygame.image.load("img_materials/obstacle2.png").convert_alpha())  # Load flying object image 2

# Player position
player_x = SCREEN_WIDTH // 4
player_y = SCREEN_HEIGHT - PLAYER_SIZE
player_velocity_y = 0
is_jumping = False
player_image = player_image1

# Obstacles
obstacles = []

# Flying objects
flying_objects = []

# Score
score = 0
font = pygame.font.Font(None, 36)
highest_score = 0

# Game states
START_SCREEN = 0
GAME_RUNNING = 1
GAME_OVER = 2
game_state = START_SCREEN

# Game loop
clock = pygame.time.Clock()

def create_obstacle():
    obstacle_x = SCREEN_WIDTH
    obstacle_y = SCREEN_HEIGHT - PLAYER_SIZE
    obstacles.append({'rect': pygame.Rect(obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT), 'collided': False})

def create_flying_object():
    flying_object_x = SCREEN_WIDTH
    flying_object_y = random.randint(0, SCREEN_HEIGHT - FLYING_OBJECT_HEIGHT)
    flying_objects.append(pygame.Rect(flying_object_x, flying_object_y, FLYING_OBJECT_WIDTH, FLYING_OBJECT_HEIGHT))

def reset_game():
    global player_y, player_velocity_y, obstacles, flying_objects, score
    player_y = SCREEN_HEIGHT - PLAYER_SIZE
    player_velocity_y = 0
    obstacles = []
    flying_objects = []
    score = 0

def start_screen():
    screen.fill(WHITE)
    title_text = font.render("Welcome to Luna in Flight", True, BLACK)
    screen.blit(title_text, (250, 120))
    start_text = font.render("Press SPACE to start", True, BLACK)
    screen.blit(start_text, (260, 220))
    pygame.display.flip()

def end_screen():
    global highest_score
    screen.fill(WHITE)
    end_text = font.render("Game Over. Press SPACE to play again", True, BLACK)
    screen.blit(end_text, (200, 120))
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (320, 170))
    highest_score_text = font.render("Highest Score: " + str(highest_score), True, BLACK)
    screen.blit(highest_score_text, (260, 220))
    pygame.display.flip()

while True:
    if game_state == START_SCREEN:
        start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = GAME_RUNNING
                reset_game()
    elif game_state == GAME_RUNNING:
        screen.fill(WHITE)  # Clear the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_y == SCREEN_HEIGHT - PLAYER_SIZE:
                    is_jumping = True
                    player_velocity_y = JUMP_FORCE

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and is_jumping:
                    is_jumping = False

        # Apply gravity
        player_velocity_y += GRAVITY

        # Clamp additional force while holding spacebar
        if is_jumping and player_velocity_y > JUMP_HOLD_FORCE:
            player_velocity_y = max(player_velocity_y + JUMP_HOLD_FORCE, JUMP_FORCE)

        player_y += player_velocity_y

        # Change image while in flight
        im_mod = player_image_onrun%8
        if is_jumping: 
            if im_mod == 0: player_image = player_image2
            elif im_mod ==4: player_image = player_image4
        elif im_mod == 0: player_image = player_image1
        elif im_mod == 4: player_image = player_image3
        player_image_onrun = player_image_onrun + 1

        # Prevent player from falling below the ground
        if player_y > SCREEN_HEIGHT - PLAYER_SIZE:
            player_y = SCREEN_HEIGHT - PLAYER_SIZE
            player_velocity_y = 0

        # Generate obstacles
        if random.random() < OBJ_RATE:
            create_obstacle()

        # Generate flying objects
        if random.random() < FLY_RATE:
            create_flying_object()

        # Move and draw obstacles
        for obstacle in obstacles:
            obstacle['rect'].x -= 5  # Adjust speed of obstacles here
            pygame.draw.rect(screen, BLACK, obstacle['rect'])

            # Check collision with player
            if obstacle['rect'].colliderect(pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)):
                game_state = GAME_OVER

            # Check if player jumped over the obstacle
            if obstacle['rect'].x + OBSTACLE_WIDTH < player_x and not obstacle['collided']:
                obstacle['collided'] = True
                score += 1

        # Move and draw flying objects
        for flying_object in flying_objects:
            flying_object.x -= 3  # Adjust speed of flying objects here
            pygame.draw.rect(screen, BLACK, flying_object)

            # Check collision with player
            if flying_object.colliderect(pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)):
                game_state = GAME_OVER

        # Remove obstacles that are off-screen
        obstacles = [obstacle for obstacle in obstacles if obstacle['rect'].x > -OBSTACLE_WIDTH]

        # Remove flying objects that are off-screen
        flying_objects = [flying_object for flying_object in flying_objects if flying_object.x > -FLYING_OBJECT_WIDTH]

        # Draw player
        screen.blit(player_image, (player_x, player_y))

        # Update highest score
        if score > highest_score:
            highest_score = score

        # Draw score
        score_text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    elif game_state == GAME_OVER:
        end_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = GAME_RUNNING
                reset_game()
