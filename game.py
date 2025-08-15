import pygame
from champion import Champion
from minion import Minion
from projectile import Projectile
from config import config

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_rect = pygame.Rect(0, 0, screen_width, screen_height)

        self.background = pygame.image.load(config.game.background_image)
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

        self.player = Champion(screen_width // 2, screen_height // 2)
        self.projectiles = []
        self.minions = [Minion(100, 100), Minion(700, 100), Minion(100, 500), Minion(700, 500)]

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right-click
            self.player.move_to(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            mouse_pos = pygame.mouse.get_pos()
            self.projectiles.append(Projectile(self.player.pos, mouse_pos))

    def update(self):
        self.player.update()

        # Update projectiles and check for collisions
        for projectile in self.projectiles[:]:
            projectile.update()
            if not self.screen_rect.colliderect(projectile.rect):
                self.projectiles.remove(projectile)
            else:
                for minion in self.minions[:]:
                    if projectile.rect.colliderect(minion.rect):
                        self.projectiles.remove(projectile)
                        self.minions.remove(minion)
                        break

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.player.draw(screen)
        for minion in self.minions:
            minion.draw(screen)
        for projectile in self.projectiles:
            projectile.draw(screen)
