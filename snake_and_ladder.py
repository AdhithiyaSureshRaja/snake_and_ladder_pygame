import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
SQUARE_SIZE = WIDTH // COLS
INFO_HEIGHT = 150
screen = pygame.display.set_mode((WIDTH + 150, HEIGHT + INFO_HEIGHT))
pygame.display.set_caption("Snake and Ladder with Dice")

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
player_positions = [1, 1]
player_colors = [(200, 50, 50), (50, 50, 200)]
current_player = 0

# Load dice images
dice_images = [pygame.image.load(f"dice{i}.png") for i in range(1, 7)]
for i in range(len(dice_images)):
    dice_images[i] = pygame.transform.scale(dice_images[i], (100, 100))

current_dice = dice_images[0]

def draw_board():
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
    row = (position - 1) // 10
    col = (position - 1) % 10
    if row % 2 == 1:
        col = 9 - col
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = (9 - row) * SQUARE_SIZE + SQUARE_SIZE // 2
    return x, y

def draw_arrow_line(start, end, color):
    # Draw main line
    pygame.draw.line(screen, color, start, end, 5)

    # Draw arrowhead
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    arrow_length = 15
    arrow_angle = math.pi / 6  # 30 degrees
    # Left side of arrow
    x1 = end[0] - arrow_length * math.cos(angle - arrow_angle)
    y1 = end[1] - arrow_length * math.sin(angle - arrow_angle)
    # Right side of arrow
    x2 = end[0] - arrow_length * math.cos(angle + arrow_angle)
    y2 = end[1] - arrow_length * math.sin(angle + arrow_angle)

    pygame.draw.line(screen, color, end, (x1, y1), 5)
    pygame.draw.line(screen, color, end, (x2, y2), 5)

def draw_snakes_and_ladders():
    # Snakes: red arrows pointing down
    for start, end in snakes.items():
        start_pos = get_coordinates(start)
        end_pos = get_coordinates(end)
        draw_arrow_line(start_pos, end_pos, RED)
    # Ladders: blue arrows pointing up
    for start, end in ladders.items():
        start_pos = get_coordinates(start)
        end_pos = get_coordinates(end)
        draw_arrow_line(start_pos, end_pos, BLUE)

def draw_players():
    for i, pos in enumerate(player_positions):
        x, y = get_coordinates(pos)

        # If both players are on same tile, offset
        if player_positions.count(pos) > 1:
            if i == 0:
                x -= 10
            else:
                x += 10

        pygame.draw.circle(screen, player_colors[i], (x, y), 15)

def roll_dice_animation():
    global current_dice
    for _ in range(10):  # Spin effect
        current_dice = random.choice(dice_images)
        draw_screen()
        pygame.display.flip()
        pygame.time.delay(100)
    return random.randint(1, 6)

def move_player(player, steps):
    for _ in range(steps):
        if player_positions[player] < 100:
            player_positions[player] += 1
            draw_screen()
            pygame.display.flip()
            pygame.time.delay(200)  # Adjust speed (200 ms per tile)

    # If landed on a ladder or snake, animate that too
    while player_positions[player] in ladders or player_positions[player] in snakes:
        if player_positions[player] in ladders:
            destination = ladders[player_positions[player]]
        else:
            destination = snakes[player_positions[player]]

        # Animate moving to destination
        while player_positions[player] != destination:
            if player_positions[player] < destination:
                player_positions[player] += 1
            else:
                player_positions[player] -= 1
            draw_screen()
            pygame.display.flip()
            pygame.time.delay(200)


def display_message(message):
    text = font.render(message, True, BLACK)
    pygame.draw.rect(screen, GREEN, (0, HEIGHT, WIDTH + 150, INFO_HEIGHT))
    screen.blit(text, (20, HEIGHT + 50))

def draw_dice():
    screen.blit(current_dice, (WIDTH + 20, 200))

def draw_screen():
    screen.fill(WHITE)
    draw_board()
    draw_snakes_and_ladders()  # Draw arrowed lines
    draw_players()
    draw_dice()
    if player_positions[current_player] >= 100:
        display_message(f"Player {current_player + 1} Wins! Press Q to quit")
    else:
        display_message(f"Player {current_player + 1}'s turn. Press SPACE to roll dice")

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    draw_screen()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_SPACE and player_positions[current_player] < 100:
                steps = roll_dice_animation()
                current_dice = dice_images[steps - 1]
                move_player(current_player, steps)
                current_player = (current_player + 1) % 2

    clock.tick(30)

pygame.quit()
sys.exit()
