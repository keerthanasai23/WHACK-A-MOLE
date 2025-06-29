import pygame
import random
import time

def play_bot_mode(screen, font):
    # === CONSTANTS ===
    GRID_SIZE, CELL_SIZE, MOLE_SIZE = 4, 150, 100
    GRID_SPACING = 10
    FPS = 30
    GAME_TIME = 20
    BACKGROUND_COLOR = (0, 128, 0)
    HOLE_COLOR = (139, 69, 19)
    clock = pygame.time.Clock()

    # === ASSETS ===
    player_mole_image = pygame.transform.scale(pygame.image.load('assets/mole1.png'), (MOLE_SIZE, MOLE_SIZE))
    ai_mole_image = pygame.transform.scale(pygame.image.load('assets/mole2.png'), (MOLE_SIZE, MOLE_SIZE))
    golden_mole_image = pygame.transform.scale(pygame.image.load('assets/golden_mole.png'), (MOLE_SIZE, MOLE_SIZE))
    hammer_image = pygame.transform.scale(pygame.image.load('assets/hammer.png'), (50, 50))

    hit_sound = pygame.mixer.Sound('assets/sound-1-167181.mp3')
    ai_hit_sound = pygame.mixer.Sound('assets/sound-1-167181.mp3')
    hit_sound.set_volume(1.0)
    ai_hit_sound.set_volume(1.0)

    pygame.mixer.music.load('assets/background-game-145867.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    def draw_grid():
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * (CELL_SIZE + GRID_SPACING)
                y = row * (CELL_SIZE + GRID_SPACING)
                pygame.draw.rect(screen, HOLE_COLOR, (x, y, CELL_SIZE, CELL_SIZE))

    def draw_mole(pos, mole_type):
        row, col = pos
        x = col * (CELL_SIZE + GRID_SPACING) + (CELL_SIZE - MOLE_SIZE) // 2
        y = row * (CELL_SIZE + GRID_SPACING) + (CELL_SIZE - MOLE_SIZE) // 2
        img = player_mole_image if mole_type == "player" else ai_mole_image if mole_type == "ai" else golden_mole_image
        screen.blit(img, (x, y))

    def get_cell(pos):
        x, y = pos
        col = x // (CELL_SIZE + GRID_SPACING)
        row = y // (CELL_SIZE + GRID_SPACING)
        return row, col

    def ai_ready(last_hit_time, reaction_time):
        return time.time() - last_hit_time >= reaction_time

    def draw_hit_flash(pos):
        row, col = pos
        x = col * (CELL_SIZE + GRID_SPACING)
        y = row * (CELL_SIZE + GRID_SPACING)
        pygame.draw.rect(screen, (255, 0, 0), (x, y, CELL_SIZE, CELL_SIZE))

    def show_result(player_score, ai_score):
        screen.fill(BACKGROUND_COLOR)
        screen.blit(font.render("Game Over!", True, (255, 255, 255)), (200, 300))
        screen.blit(font.render(f"Player: {player_score} | AI: {ai_score}", True, (255, 255, 255)), (100, 350))
        winner = "You win!" if player_score > ai_score else "AI wins!" if ai_score > player_score else "It's a tie!"
        screen.blit(font.render(winner, True, (255, 255, 255)), (200, 400))
        pygame.display.flip()
        pygame.time.wait(3000)

    # === GAME LOOP ===
    mole_time = 1.5
    ai_speed_range = (0.6, 1.0)
    player_score = ai_score = 0
    start_time = time.time()
    mole_pos = None
    mole_type = ""
    mole_visible = False
    last_mole_time = ai_last_hit_time = 0
    player_moles = ai_moles = 0
    golden_done = False
    max_moles = 20
    pygame.mouse.set_visible(False)

    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        now = time.time()
        elapsed = now - start_time
        time_left = GAME_TIME - elapsed

        if time_left <= 0 or player_moles + ai_moles >= max_moles:
            break

        if now - last_mole_time > mole_time and (player_moles + ai_moles < max_moles):
            mole_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if 8.0 <= elapsed <= 12.0 and not golden_done:
                mole_type = "golden"
                golden_done = True
            elif player_moles <= ai_moles:
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
            elif event.type == pygame.MOUSEBUTTONDOWN and mole_visible:
                if get_cell(pygame.mouse.get_pos()) == mole_pos:
                    if mole_type == "player":
                        player_score += 1
                    elif mole_type == "ai":
                        player_score -= 1
                    elif mole_type == "golden":
                        player_score += 3
                    hit_sound.play()
                    draw_hit_flash(mole_pos)
                    mole_visible = False
                    pygame.display.flip()
                    pygame.time.wait(100)

        if mole_visible and mole_type == "ai":
            if ai_ready(ai_last_hit_time, random.uniform(*ai_speed_range)):
                ai_score += 1
                ai_hit_sound.play()
                draw_hit_flash(mole_pos)
                mole_visible = False
                pygame.display.flip()
                pygame.time.wait(100)

        if mole_visible:
            draw_mole(mole_pos, mole_type)

        # UI
        screen.blit(font.render(f"Time: {int(time_left)}s", True, (0, 0, 0)), (400, 660))
        screen.blit(font.render(f"Player: {player_score}", True, (0, 0, 0)), (10, 660))
        screen.blit(font.render(f"AI: {ai_score}", True, (0, 0, 0)), (200, 660))
        screen.blit(hammer_image, hammer_image.get_rect(center=pygame.mouse.get_pos()).topleft)

        pygame.display.flip()
        clock.tick(FPS)

    show_result(player_score, ai_score)
