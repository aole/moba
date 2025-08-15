import pygame
from .game.game import Game
from .game.config import config

def main():
    pygame.init()

    screen_width = 1536
    screen_height = 1024
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("MOBA Game")

    game = Game(screen_width, screen_height)

    # Font for text rendering
    font = pygame.font.Font(config.game.font_path, 36)

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_input(event)

        game.update()
        game.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
