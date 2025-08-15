import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
SQUARE_SIZE = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))
pygame.display.set_caption("Snake and Ladder")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GREEN = (50, 200, 50)

# Fonts
font = pygame.font.Font(None, 36)

# Snakes and ladders mapping
snakes = {98: 78, 95: 75, 93: 73, 87: 24, 64: 60, 62: 19, 54: 34, 17: 7}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Players
player_positions = [1, 1]  # Player 1 and Player 2 start at position 1
player_colors = [RED, BLUE]
current_player = 0

def draw_board():
    screen.fill(WHITE)
    num = 100
    for row in range(ROWS):
        for col in range(COLS):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            pygame.draw.rect(screen, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE), 1)
            text = font.render(str(num), True, BLACK)
            screen.blit(text, (x + 10, y + 10))
            num -= 1 if row % 2 == 0 else -1
        num -= 10 if row % 2 == 0 else 10

def get_coordinates(position):
    # Converts board number to pixel coordinates
    row = (position - 1) // 10
    col = (position - 1) % 10
    if row % 2 == 1:  # Zigzag pattern
        col = 9 - col
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = (9 - row) * SQUARE_SIZE + SQUARE_SIZE // 2
    return x, y

def draw_players():
    for i, pos in enumerate(player_positions):
        x, y = get_coordinates(pos)
        pygame.draw.circle(screen, player_colors[i], (x, y), 15)

def roll_dice():
    return random.randint(1, 6)

def move_player(player, steps):
    player_positions[player] += steps
    if player_positions[player] > 100:
        player_positions[player] = 100
    # Check ladders
    if player_positions[player] in ladders:
        player_positions[player] = ladders[player_positions[player]]
    # Check snakes
    if player_positions[player] in snakes:
        player_positions[player] = snakes[player_positions[player]]

def display_message(message):
    text = font.render(message, True, BLACK)
    pygame.draw.rect(screen, GREEN, (0, HEIGHT, WIDTH, 100))
    screen.blit(text, (20, HEIGHT + 30))

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)
    draw_board()
    draw_players()

    if player_positions[current_player] >= 100:
        display_message(f"Player {current_player + 1} Wins! Press Q to quit")
    else:
        display_message(f"Player {current_player + 1}'s turn. Press SPACE to roll dice")

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_SPACE and player_positions[current_player] < 100:
                steps = roll_dice()
                move_player(current_player, steps)
                current_player = (current_player + 1) % 2

    clock.tick(30)

pygame.quit()
sys.exit()
