import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300
PLAYER_SIZE = 50
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 40
GRAVITY = 0.5
JUMP_FORCE = -10
JUMP_HOLD_FORCE = -0.5  # Additional force applied while holding spacebar
FLYING_OBJECT_WIDTH = 40
FLYING_OBJECT_HEIGHT = 40
OBJ_RATE = 0.005
FLY_RATE = 0.005

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Luna in Flight")

# Load the soundtrack (background music)
pygame.mixer.music.load("audio_materials/background_music.mp3")
pygame.mixer.music.play(-1) # Play the soundtrack (looping indefinitely)
pygame.mixer.music.set_volume(0.5)  # Set volume

# Load audio effects
collision_sound = pygame.mixer.Sound("audio_materials/collision.mp3")

# Load player images
player_image1 = pygame.image.load("img_materials/luna_run1.png").convert_alpha()
player_image1 = pygame.transform.scale(player_image1, (PLAYER_SIZE, PLAYER_SIZE))
player_image2 = pygame.image.load("img_materials/luna_run2.png").convert_alpha()
player_image2 = pygame.transform.scale(player_image2, (PLAYER_SIZE, PLAYER_SIZE))
player_image3 = pygame.image.load("img_materials/luna_fly1.png").convert_alpha()
player_image3 = pygame.transform.scale(player_image3, (PLAYER_SIZE, PLAYER_SIZE))
player_image4 = pygame.image.load("img_materials/luna_fly2.png").convert_alpha()
player_image4 = pygame.transform.scale(player_image4, (PLAYER_SIZE, PLAYER_SIZE))

# Load obstacle and flying object images
# Obstacle 1: Rock
# Obstacle 2: Dark rock
# Obstacle 3: Yellow and dark rock
# Obstacle 4: Blue circle

# Flying 1: Crescent moon
# Flying 2: Full moon
# Flying 3: Yellow star
# Flying 4: Pink star
# Flying 5: Blue star
# Flying 6: Cloud
# Flying 7: White diamond
# Flying 8: Sparkles

n_obs = 4
obstacle_images = []
for i in range(1, n_obs+1):  # n_obs is the number of obstacle images
    image_path = f"img_materials/obstacle{i}.png"
    obstacle_image = pygame.image.load(image_path).convert_alpha()
    obstacle_image = pygame.transform.scale(obstacle_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
    obstacle_images.append(obstacle_image)

n_fly = 8 # n_fly is the number of flying object images
flying_images = []
for i in range(1, n_fly+1): 
    image_path = f"img_materials/flying{i}.png"
    flying_image = pygame.image.load(image_path).convert_alpha()
    flying_image = pygame.transform.scale(flying_image, (FLYING_OBJECT_WIDTH, FLYING_OBJECT_HEIGHT))
    flying_images.append(flying_image)

# Player position
player_x = SCREEN_WIDTH // 4
player_y = SCREEN_HEIGHT - PLAYER_SIZE
player_velocity_y = 0
is_jumping = False
player_image = player_image1

# Animation counter
image_onrun = 0 

# Obstacles
obstacles = []

# Flying objects
flying_objects = []

# Font
font_file = "font_materials/static/PixelifySans-Regular.ttf"  # Replace "your_font.ttf" with the path to your font file

# Score
score = 0
font = pygame.font.Font(font_file, 36)
highest_score = 0

# Game states
START_SCREEN = 0
GAME_RUNNING = 1
GAME_OVER = 2
game_state = START_SCREEN

# Background image
background_image = pygame.image.load("img_materials/background.png").convert()  # Load background image
background_image2 = pygame.image.load("img_materials/background2.png").convert()
background_x = 0  # Initial position for scrolling

# Game loop
clock = pygame.time.Clock()

def create_obstacle():
    obstacle_x = SCREEN_WIDTH
    obstacle_y = SCREEN_HEIGHT - OBSTACLE_HEIGHT  # Adjusted to place the obstacle on the ground
    obstacle_image = random.choice(obstacle_images)
    obstacles.append({'image': obstacle_image, 'rect': obstacle_image.get_rect(bottomleft=(obstacle_x, SCREEN_HEIGHT)), 'collided': False})

def create_flying_object():
    flying_object_x = SCREEN_WIDTH
    flying_object_y = random.randint(0, SCREEN_HEIGHT - flying_images[0].get_height())
    flying_object_image = random.choice(flying_images)
    flying_objects.append({'image': flying_object_image, 'rect': flying_object_image.get_rect(midbottom=(flying_object_x, flying_object_y))})

def reset_game():
    global player_y, player_velocity_y, obstacles, flying_objects, score
    player_y = SCREEN_HEIGHT - PLAYER_SIZE
    player_velocity_y = 0
    obstacles = []
    flying_objects = []
    score = 0

def start_screen():
    screen.fill(WHITE)
    screen.blit(background_image2, (background_x, 0))
    title_text = font.render("Welcome to Luna in Flight", True, BLACK)
    title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
    screen.blit(title_text, title_text_rect)
    
    start_text = font.render("Press SPACE to start", True, BLACK)
    start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
    screen.blit(start_text, start_text_rect)
    
    pygame.display.flip()

def end_screen():
    global highest_score
    screen.fill(WHITE)
    screen.blit(background_image2, (background_x, 0))
    screen.blit(background_image2, (background_x + background_image2.get_width(), 0))
    
    end_text = font.render("Game Over. Press SPACE to play again", True, BLACK)
    end_text_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
    screen.blit(end_text, end_text_rect)
    
    score_text = font.render("Score: " + str(score), True, BLACK)
    score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 170))
    screen.blit(score_text, score_text_rect)
    
    highest_score_text = font.render("Highest Score: " + str(highest_score), True, BLACK)
    highest_score_text_rect = highest_score_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
    screen.blit(highest_score_text, highest_score_text_rect)
    
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

        # Change player images to animate while in flight and running
        im_mod = image_onrun % 10
        if is_jumping: 
            if im_mod == 0: player_image = player_image3
            elif im_mod == 5: player_image = player_image4
        elif im_mod == 0: player_image = player_image1
        elif im_mod == 5: player_image = player_image2
        image_onrun = image_onrun + 1

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

        # Draw background
        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + background_image.get_width(), 0))

        # Move and draw obstacles
        for obstacle in obstacles:
            obstacle['rect'].x -= 5  # Adjust speed of obstacles here
            screen.blit(obstacle['image'], obstacle['rect'])

            # Check collision with player
            if obstacle['rect'].colliderect(pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)):
                collision_sound.play()
                game_state = GAME_OVER

            # Check if player jumped over the obstacle
            if obstacle['rect'].x + OBSTACLE_WIDTH < player_x and not obstacle['collided']:
                obstacle['collided'] = True
                score += 1

        # Move and draw flying objects
        for flying_object in flying_objects:
            flying_object['rect'].x -= 3  # Adjust speed of flying objects here
            screen.blit(flying_object['image'], flying_object['rect'])

            # Check collision with player
            if flying_object['rect'].colliderect(pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)):
                game_state = GAME_OVER

        # Remove obstacles that are off-screen
        obstacles = [obstacle for obstacle in obstacles if obstacle['rect'].x > -OBSTACLE_WIDTH]

        # Remove flying objects that are off-screen
        flying_objects = [flying_object for flying_object in flying_objects if flying_object['rect'].x > -FLYING_OBJECT_WIDTH]

        # Scroll the background
        background_x -= 1
        if background_x <= -background_image.get_width():
            background_x = 0

        # Draw player
        screen.blit(player_image, (player_x, player_y))

        # Update highest score
        if score > highest_score:
            highest_score = score

        # Draw score
        score_text = font.render("Score: " + str(score), True, WHITE)
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
