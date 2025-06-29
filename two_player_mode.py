import pygame
import random
import time

GRID_SIZE = 4
CELL_SIZE = 150
MOLE_SIZE = 100
GRID_SPACING = 10
BACKGROUND_COLOR = (0, 128, 0)
HOLE_COLOR = (139, 69, 19)
FPS = 30
GAME_TIME = 20

# Load assets globally
player1_img = pygame.transform.scale(pygame.image.load('assets/mole1.png'), (MOLE_SIZE, MOLE_SIZE))
player2_img = pygame.transform.scale(pygame.image.load('assets/mole2.png'), (MOLE_SIZE, MOLE_SIZE))
hammer_img = pygame.transform.scale(pygame.image.load('assets/hammer.png'), (50, 50))

def draw_grid(screen):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * (CELL_SIZE + GRID_SPACING)
            y = row * (CELL_SIZE + GRID_SPACING)
            pygame.draw.rect(screen, HOLE_COLOR, (x, y, CELL_SIZE, CELL_SIZE))

def draw_mole(screen, position, player):
    row, col = position
    x = col * (CELL_SIZE + GRID_SPACING) + (CELL_SIZE - MOLE_SIZE) // 2
    y = row * (CELL_SIZE + GRID_SPACING) + (CELL_SIZE - MOLE_SIZE) // 2
    img = player1_img if player == 1 else player2_img
    screen.blit(img, (x, y))

def get_cell_from_mouse(pos):
    x, y = pos
    col = x // (CELL_SIZE + GRID_SPACING)
    row = y // (CELL_SIZE + GRID_SPACING)
    return row, col

def play_two_player_mode(screen, font):
    clock = pygame.time.Clock()
    player1_score = player2_score = 0
    mole_position = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    start_time = time.time()
    mole_visible = True

    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen)
        elapsed = time.time() - start_time
        if elapsed > GAME_TIME:
            break

        draw_mole(screen, mole_position, 1 if int(elapsed) % 2 == 0 else 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_cell_from_mouse(pygame.mouse.get_pos())
                if (row, col) == mole_position:
                    if int(elapsed) % 2 == 0:
                        player1_score += 1
                    else:
                        player2_score += 1
                    mole_position = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))

        screen.blit(font.render(f"P1 Score: {player1_score}", True, (0, 0, 0)), (10, 650))
        screen.blit(font.render(f"P2 Score: {player2_score}", True, (0, 0, 0)), (300, 650))
        screen.blit(hammer_img, hammer_img.get_rect(center=pygame.mouse.get_pos()).topleft)
        pygame.display.flip()
        clock.tick(FPS)

    # Game Over
    screen.fill(BACKGROUND_COLOR)
    screen.blit(font.render("Game Over!", True, (255, 255, 255)), (200, 300))
    screen.blit(font.render(f"P1: {player1_score} | P2: {player2_score}", True, (255, 255, 255)), (150, 350))
    result = "P1 Wins!" if player1_score > player2_score else "P2 Wins!" if player2_score > player1_score else "Tie!"
    screen.blit(font.render(result, True, (255, 255, 255)), (230, 400))
    pygame.display.flip()
    pygame.time.wait(3000)
