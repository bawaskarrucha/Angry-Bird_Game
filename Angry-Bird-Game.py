import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_SPEED = 5

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Game")
clock = pygame.time.Clock()

# Load bird image
bird_img = pygame.image.load('bird.png')
bird_img = pygame.transform.scale(bird_img, (40, 30))  # Resize the bird image if necessary
bird_rect = bird_img.get_rect()
bird_x = 100
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0

# Pipe parameters
def create_pipe():
    pipe_height = random.randint(150, 450)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, pipe_height + PIPE_GAP // 2, PIPE_WIDTH, SCREEN_HEIGHT - pipe_height)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, pipe_height - PIPE_GAP // 2)
    return top_pipe, bottom_pipe

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

score = 0
font = pygame.font.Font(None, 36)

# Timer variables
play_time = 0  # in seconds
MAX_PLAY_TIME = 3600  # 1 hour in seconds

# Game loop
running = True
while running:
    # Calculate elapsed time
    elapsed = pygame.time.get_ticks() / 1000  # convert to seconds
    play_time = int(elapsed)

    # Exit game if time limit reached
    if play_time >= MAX_PLAY_TIME:
        print(f"Time's up! Your final score: {score}")
        break

    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = FLAP_STRENGTH

    # Bird movement
    bird_velocity += GRAVITY
    bird_y += bird_velocity

    # Update bird position
    bird_rect.y = bird_y

    # Move pipes
    pipe_list = [pipe.move(-PIPE_SPEED, 0) for pipe in pipe_list]

    # Remove off-screen pipes and update score
    for pipe in pipe_list[:]:
        if pipe.right <= 0:
            pipe_list.remove(pipe)
            score += 1

    # Check collisions with pipes
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe):
            print(f"Game Over! Your score: {score}")
            running = False

    # Check if bird touches top or bottom of screen
    if bird_y <= 0 or bird_y >= SCREEN_HEIGHT:
        print(f"Game Over! Your score: {score}")
        running = False

    # Draw bird
    screen.blit(bird_img, (bird_x, int(bird_y)))

    # Draw pipes
    for pipe in pipe_list:
        pygame.draw.rect(screen, GREEN, pipe)

    # Draw ground
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10))

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Draw play time
    time_text = font.render(f"Time: {play_time} sec", True, BLACK)
    screen.blit(time_text, (SCREEN_WIDTH - 150, 10))

    # Update display
    pygame.display.flip()
    clock.tick(20)

# Quit pygame
pygame.quit()
sys.exit()
