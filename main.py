import pygame
from bot_mode import play_bot_mode
from two_player_mode import play_two_player_mode  # You must create or update this module too

pygame.init()
screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption("Whack-a-Mole")
font = pygame.font.SysFont('arial', 36)
BACKGROUND_COLOR = (0, 128, 0)


def show_mode_selection():
    selecting = True
    while selecting:
        screen.fill(BACKGROUND_COLOR)
        screen.blit(font.render("Choose Mode", True, (255, 255, 255)), (200, 250))
        screen.blit(font.render("1 - Human vs Bot", True, (255, 255, 255)), (180, 300))
        screen.blit(font.render("2 - 2 Player Mode", True, (255, 255, 255)), (180, 350))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play_bot_mode(screen, font)
                    selecting = False
                elif event.key == pygame.K_2:
                    play_two_player_mode(screen, font)
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
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    show_mode_selection()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return


if __name__ == "__main__":
    show_home_page()
