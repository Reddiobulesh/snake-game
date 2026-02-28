import pygame
import random
import sys

pygame.init()

width, height = 1000, 600
game_screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Welcome to the REDDIOBULESH GAMING WORLD")

font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

# Snake and Food setup
snake_block = 10

# Load high score
def get_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    high_score = get_high_score()
    if score > high_score:
        with open("highscore.txt", "w") as f:
            f.write(str(score))

# Draw text on screen
def draw_text(text, size, color, x, y, center=True):
    font_obj = pygame.font.SysFont(None, size)
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    game_screen.blit(text_surface, text_rect)

# Spawn food
def spawn_food(snake_body):
    while True:
        fx = random.randrange(0, width, 10)
        fy = random.randrange(0, height, 10)
        if (fx, fy) not in snake_body:
            return fx, fy

# Show start screen
def show_start_screen():
    game_screen.fill((0, 0, 0))
    draw_text("Welcome to REDDIOBULESH GAMING WORLD", 48, (255, 0, 0), width//2, height//3)
    draw_text("Press any key to start", 36, (255, 255, 255), width//2, height//2)
    pygame.display.update()
    wait_for_key()

# Show game over screen
def show_game_over_screen(score):
    game_screen.fill((0, 0, 0))
    draw_text("GAME OVER", 60, (255, 0, 0), width//2, height//3)
    draw_text(f"Score: {score}", 40, (255, 255, 255), width//2, height//2)
    # Display high score
    high_score = get_high_score()
    draw_text(f"High Score: {high_score}", 40, (255, 255, 0), width//2, height * 2//3)
    draw_text("Press any key to restart", 36, (200, 200, 200), width//2, height * 2//3 + 40)
    pygame.display.update()
    wait_for_key()

# Wait for key press
def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

# Run the game logic
def run_game():
    snake_x, snake_y = width // 2, height // 2
    change_x, change_y = 0, 0
    snake_body = [(snake_x, snake_y)]
    food_x, food_y = spawn_food(snake_body)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and change_x == 0:
                    change_x = -snake_block
                    change_y = 0
                elif event.key == pygame.K_RIGHT and change_x == 0:
                    change_x = snake_block
                    change_y = 0
                elif event.key == pygame.K_UP and change_y == 0:
                    change_x = 0
                    change_y = -snake_block
                elif event.key == pygame.K_DOWN and change_y == 0:
                    change_x = 0
                    change_y = snake_block

        snake_x = (snake_x + change_x) % width
        snake_y = (snake_y + change_y) % height

        if (snake_x, snake_y) in snake_body[1:]:
            break  # Game over

        snake_body.append((snake_x, snake_y))
        if (snake_x, snake_y) == (food_x, food_y):
            food_x, food_y = spawn_food(snake_body)
        else:
            del snake_body[0]

        game_screen.fill((0, 0, 0))
        pygame.draw.rect(game_screen, (0, 255, 0), [food_x, food_y, 10, 10])
        for (x, y) in snake_body:
            pygame.draw.rect(game_screen, (255, 255, 255), [x, y, 10, 10])

        # Show score
        score = len(snake_body) - 1
        draw_text(f"Score: {score}", 30, (255, 255, 0), 10, 10, center=False)

        pygame.display.update()
        clock.tick(12)

    # Save high score if necessary
    save_high_score(score)
    show_game_over_screen(score)

# Main loop
while True:
    show_start_screen()
    run_game()
