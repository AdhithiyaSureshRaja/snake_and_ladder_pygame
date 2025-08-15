import pygame
import sys
import random
import math

# ---------------- Pygame Initialization ---------------- #
pygame.init()
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
SQUARE_SIZE = WIDTH // COLS
INFO_HEIGHT = 150
screen = pygame.display.set_mode((WIDTH + 150, HEIGHT + INFO_HEIGHT))
pygame.display.set_caption("Snake and Ladder")

# Colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GREEN = (50, 200, 50)
font = pygame.font.Font(None, 36)

# ---------------- Random Snakes and Ladders ---------------- #
def generate_snakes_and_ladders(num_snakes=8, num_ladders=9):
    snake_positions = {}
    ladder_positions = {}
    occupied = set()

    # Snakes: start > end
    while len(snake_positions) < num_snakes:
        start = random.randint(20, 99)
        end = random.randint(1, start - 1)
        if start not in occupied and end not in occupied and start != 100 and end != 1:
            snake_positions[start] = end
            occupied.add(start)
            occupied.add(end)

    # Ladders: start < end
    while len(ladder_positions) < num_ladders:
        start = random.randint(1, 79)
        end = random.randint(start + 1, 100)
        if start not in occupied and end not in occupied and start != 1 and end != 100:
            ladder_positions[start] = end
            occupied.add(start)
            occupied.add(end)

    return snake_positions, ladder_positions

snakes, ladders = generate_snakes_and_ladders()

# ---------------- Players and Dice ---------------- #
player_positions = [1, 1]
player_colors = [(200, 50, 50), (50, 50, 200)]
current_player = 0
dice_images = [pygame.image.load(f"dice{i}.png") for i in range(1, 7)]
for i in range(len(dice_images)):
    dice_images[i] = pygame.transform.scale(dice_images[i], (100, 100))
current_dice = dice_images[0]

# ---------------- Functions ---------------- #
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
    pygame.draw.line(screen, color, start, end, 5)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    arrow_length = 15
    arrow_angle = math.pi / 6
    x1 = end[0] - arrow_length * math.cos(angle - arrow_angle)
    y1 = end[1] - arrow_length * math.sin(angle - arrow_angle)
    x2 = end[0] - arrow_length * math.cos(angle + arrow_angle)
    y2 = end[1] - arrow_length * math.sin(angle + arrow_angle)
    pygame.draw.line(screen, color, end, (x1, y1), 5)
    pygame.draw.line(screen, color, end, (x2, y2), 5)

def draw_snakes_and_ladders():
    for start, end in snakes.items():
        draw_arrow_line(get_coordinates(start), get_coordinates(end), RED)
    for start, end in ladders.items():
        draw_arrow_line(get_coordinates(start), get_coordinates(end), BLUE)

def draw_players(exclude_player=None, moving_pos=None):
    for i, pos in enumerate(player_positions):
        if i == exclude_player and moving_pos is None:
            continue
        if i == exclude_player and moving_pos is not None:
            x, y = moving_pos
        else:
            x, y = get_coordinates(pos)
        if player_positions.count(pos) > 1 and (i != exclude_player or moving_pos is None):
            x += -10 if i == 0 else 10
        pygame.draw.circle(screen, player_colors[i], (x, y), 15)

def roll_dice_animation():
    global current_dice
    for _ in range(10):
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
            pygame.time.delay(200)
    while player_positions[player] in ladders or player_positions[player] in snakes:
        destination = ladders.get(player_positions[player], snakes.get(player_positions[player]))
        start_pos = get_coordinates(player_positions[player])
        end_pos = get_coordinates(destination)
        steps_count = 20
        for i in range(steps_count + 1):
            t = i / steps_count
            x = int(start_pos[0] + (end_pos[0] - start_pos[0]) * t)
            y = int(start_pos[1] + (end_pos[1] - start_pos[1]) * t)
            screen.fill(WHITE)
            draw_board()
            draw_snakes_and_ladders()
            draw_players(exclude_player=player, moving_pos=(x, y))
            draw_dice()
            pygame.display.flip()
            pygame.time.delay(50)
        player_positions[player] = destination

def display_message(message):
    text = font.render(message, True, BLACK)
    pygame.draw.rect(screen, GREEN, (0, HEIGHT, WIDTH + 150, INFO_HEIGHT))
    screen.blit(text, (20, HEIGHT + 50))

def draw_dice():
    screen.blit(current_dice, (WIDTH + 20, 200))

def draw_screen():
    screen.fill(WHITE)
    draw_board()
    draw_snakes_and_ladders()
    draw_players()
    draw_dice()
    if player_positions[current_player] >= 100:
        display_message(f"Player {current_player + 1} Wins! Press Q to quit")
    else:
        display_message(f"Player {current_player + 1}'s turn. Press SPACE to roll dice")

# ---------------- Main Loop ---------------- #
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
