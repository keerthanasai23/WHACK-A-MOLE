import random
import time
import pygame

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
GRID_SIZE = 4
CELL_SIZE = 150
MOLE_SIZE = 100
GRID_SPACING = 10
BACKGROUND_COLOR = (0, 128, 0)
HOLE_COLOR = (139, 69, 19)
FPS = 30
GAME_TIME = 20

# Load assets
PLAYER_MOLE_IMAGE_PATH = 'mole1.png'
AI_MOLE_IMAGE_PATH = 'mole2.png'
HAMMER_IMAGE_PATH = 'hammer.png'
GOLDEN_MOLE_IMAGE_PATH = 'golden_mole.png'

player_mole_image = pygame.transform.scale(pygame.image.load(PLAYER_MOLE_IMAGE_PATH), (MOLE_SIZE, MOLE_SIZE))
ai_mole_image = pygame.transform.scale(pygame.image.load(AI_MOLE_IMAGE_PATH), (MOLE_SIZE, MOLE_SIZE))
hammer_image = pygame.transform.scale(pygame.image.load(HAMMER_IMAGE_PATH), (50, 50))
golden_mole_image = pygame.transform.scale(pygame.image.load(GOLDEN_MOLE_IMAGE_PATH), (MOLE_SIZE, MOLE_SIZE))

# Load sounds
hit_sound = pygame.mixer.Sound('sound-1-167181.mp3')
ai_hit_sound = pygame.mixer.Sound('sound-1-167181.mp3')
hit_sound.set_volume(1.0)
ai_hit_sound.set_volume(1.0)
pygame.mixer.music.load('background-game-145867.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Whack-a-Mole")
font = pygame.font.SysFont('arial', 36)

# Utility Functions
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * (CELL_SIZE + GRID_SPACING)
            y = row * (CELL_SIZE + GRID_SPACING)
            pygame.draw.rect(screen, HOLE_COLOR, (x, y, CELL_SIZE, CELL_SIZE))

def draw_mole(mole_position, mole_type):
    row, col = mole_position
    x = col * (CELL_SIZE + GRID_SPACING) + (CELL_SIZE - MOLE_SIZE) // 2
    y = row * (CELL_SIZE + GRID_SPACING) + (CELL_SIZE - MOLE_SIZE) // 2
    if mole_type == "player":
        screen.blit(player_mole_image, (x, y))
    elif mole_type == "ai":
        screen.blit(ai_mole_image, (x, y))
    elif mole_type == "golden":
        screen.blit(golden_mole_image, (x, y))

def get_cell_from_mouse_pos(pos):
    x, y = pos
    col = x // (CELL_SIZE + GRID_SPACING)
    row = y // (CELL_SIZE + GRID_SPACING)
    return row, col

def ai_decide_hit(last_hit_time, reaction_time):
    return time.time() - last_hit_time >= reaction_time

def draw_hit_effect(mole_position):
    row, col = mole_position
    x = col * (CELL_SIZE + GRID_SPACING)
    y = row * (CELL_SIZE + GRID_SPACING)
    pygame.draw.rect(screen, (255, 0, 0), (x, y, CELL_SIZE, CELL_SIZE))

# Game Logic
def play_game(mole_time, ai_speed_range):
    clock = pygame.time.Clock()
    player_score = ai_score = 0
    last_mole_time = 0
    mole_position = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    mole_visible = False
    start_time = time.time()
    ai_last_hit_time = 0
    mole_type = ""
    golden_mole_appeared = False

    player_moles = ai_moles = 0
    max_moles = 20
    pygame.mouse.set_visible(False)

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        now = time.time()
        elapsed = now - start_time
        time_left = GAME_TIME - elapsed

        if time_left <= 0 or (player_moles + ai_moles) >= max_moles:
            break

        if now - last_mole_time > mole_time and (player_moles + ai_moles < max_moles):
            mole_position = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            if 9.5 <= elapsed <= 10.5 and not golden_mole_appeared:
                mole_type = "golden"
                golden_mole_appeared = True
            else:
                if player_moles <= ai_moles:
                    mole_type = "player"
                    player_moles += 1
                else:
                    mole_type = "ai"
                    ai_moles += 1
            mole_visible = True
            last_mole_time = now
            ai_last_hit_time = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mole_visible:
                    if get_cell_from_mouse_pos(pygame.mouse.get_pos()) == mole_position:
                        if mole_type == "player":
                            player_score += 1
                        elif mole_type == "ai":
                            player_score -= 1
                        elif mole_type == "golden":
                            player_score += 3
                        hit_sound.play()
                        draw_hit_effect(mole_position)
                        mole_visible = False
                        pygame.display.flip()
                        pygame.time.wait(100)

        # AI Turn
        if mole_visible and mole_type == "ai":
            if ai_decide_hit(ai_last_hit_time, random.uniform(*ai_speed_range)):
                ai_score += 1
                ai_hit_sound.play()
                draw_hit_effect(mole_position)
                mole_visible = False
                pygame.display.flip()
                pygame.time.wait(100)

        # Draw mole if visible
        if mole_visible:
            draw_mole(mole_position, mole_type)

        # UI
        screen.blit(font.render(f"Time: {int(time_left)}s", True, (0, 0, 0)), (400, SCREEN_HEIGHT - 50))
        screen.blit(font.render(f"My Score: {player_score}", True, (0, 0, 0)), (10, SCREEN_HEIGHT - 50))
        screen.blit(font.render(f"AI Score: {ai_score}", True, (0, 0, 0)), (200, SCREEN_HEIGHT - 50))
        screen.blit(hammer_image, hammer_image.get_rect(center=pygame.mouse.get_pos()).topleft)

        pygame.display.flip()
        clock.tick(FPS)

    # Game Over
    show_game_over(player_score, ai_score)

def show_game_over(player_score, ai_score):
    screen.fill(BACKGROUND_COLOR)
    screen.blit(font.render("Game Over!", True, (255, 255, 255)), (200, 300))
    screen.blit(font.render(f"Player: {player_score} | AI: {ai_score}", True, (255, 255, 255)), (100, 350))
    winner = "You win!" if player_score > ai_score else "AI wins!" if ai_score > player_score else "It's a tie!"
    screen.blit(font.render(winner, True, (255, 255, 255)), (200, 400))
    pygame.display.flip()
    pygame.time.wait(3000)

def show_level_selection():
    selecting = True
    while selecting:
        screen.fill(BACKGROUND_COLOR)
        screen.blit(font.render("Select Level:", True, (255, 255, 255)), (200, 250))
        screen.blit(font.render("1 - Easy", True, (255, 255, 255)), (220, 300))
        screen.blit(font.render("2 - Medium", True, (255, 255, 255)), (220, 350))
        screen.blit(font.render("3 - Hard", True, (255, 255, 255)), (220, 400))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play_game(mole_time=3, ai_speed_range=(1.0, 1.5))  # Easy
                    selecting = False
                elif event.key == pygame.K_2:
                    play_game(mole_time=2, ai_speed_range=(0.6, 1.0))  # Medium
                    selecting = False
                elif event.key == pygame.K_3:
                    play_game(mole_time=0.6, ai_speed_range=(0.3, 0.7))  # Hard
                    selecting = False

def show_home_page():
    while True:
        screen.fill(BACKGROUND_COLOR)
        screen.blit(font.render("Whack-a-Mole", True, (255, 255, 255)), (180, 250))
        screen.blit(font.render("Press ENTER to Start", True, (255, 255, 255)), (130, 310))
        screen.blit(font.render("Press ESC to Exit", True, (255, 255, 255)), (150, 360))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    show_level_selection()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); return

if __name__ == "__main__":
    show_home_page()
