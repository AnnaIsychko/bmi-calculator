import pygame
import random
# Initialize Pygame
pygame.init()
# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
SHAPE_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 165, 0)]

# Shapes
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]
# Functions
def new_piece():
    shape = random.choice(tetris_shapes)
    color = random.choice(SHAPE_COLORS)
    return {'shape': shape, 'rotation': 0, 'x': 4, 'y': 0, 'color': color}
def draw_block(screen, x, y, color):
    pygame.draw.rect(screen, color, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    pygame.draw.rect(screen, BLACK, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
def draw_board(screen, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                draw_block(screen, x, y, cell)


def check_collision(board, piece, offset):
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                # Вычисляем новые координаты блока с учетом смещения
                new_x = x + piece['x'] + offset['x']
                new_y = y + piece['y'] + offset['y']
                # Проверяем, что новые координаты в пределах игрового поля
                if (new_x < 0 or new_x >= GRID_WIDTH or
                    new_y < 0 or new_y >= GRID_HEIGHT or
                    board[new_y][new_x] != 0):
                    return True  # Коллизия
    return False  # Нет коллизии
def rotate_piece(piece):
    return {'shape': [list(reversed(row)) for row in zip(*piece['shape'])],
            'rotation': (piece['rotation'] + 1) % len(piece['shape']),
            'x': piece['x'],
            'y': piece['y'],
            'color': piece['color']}
def merge_board(board, piece):
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                board[y + piece['y']][x + piece['x']] = piece['color']
def clear_lines(board):
    lines_cleared = 0
    y = GRID_HEIGHT - 1
    while y >= 0:
        if all(board[y]):
            del board[y]
            board.insert(0, [0] * GRID_WIDTH)
            lines_cleared += 1
        else:
            y -= 1
    return lines_cleared
# Initialize game variables
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')
clock = pygame.time.Clock()
board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
piece = new_piece()
fall_time = 0
fall_speed = 0.5
game_over = False

# Game loop
while not game_over:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not check_collision(board, piece, {'x': -1, 'y': 0}):
                piece['x'] -= 1
            elif event.key == pygame.K_RIGHT and not check_collision(board, piece, {'x': 1, 'y': 0}):
                piece['x'] += 1
            elif event.key == pygame.K_DOWN and not check_collision(board, piece, {'x': 0, 'y': 1}):
                piece['y'] += 1
            elif event.key == pygame.K_UP:
                new_piece_rotation = rotate_piece(piece)
                if not check_collision(board, new_piece_rotation, {'x': 0, 'y': 0}):
                    piece = new_piece_rotation

    # Update game state
    fall_time += clock.get_rawtime()
    clock.tick()
    if fall_time / 1000 >= fall_speed:
        fall_time = 0
        if not check_collision(board, piece, {'x': 0, 'y': 1}):
            piece['y'] += 1
        else:
            merge_board(board, piece)
            lines_cleared = clear_lines(board)
            if lines_cleared == 1:
                fall_speed = 0.5
            elif lines_cleared == 2:
                fall_speed = 0.4
            elif lines_cleared == 3:
                fall_speed = 0.3
            elif lines_cleared == 4:
                fall_speed = 0.2
            piece = new_piece()
            if check_collision(board, piece, {'x': 0, 'y': 0}):
                game_over = True

    # Draw everything
    draw_board(screen, board)
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                draw_block(screen, x + piece['x'], y + piece['y'], piece['color'])

    pygame.display.flip()
pygame.quit()
