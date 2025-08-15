import pygame
from .champion import Champion
from .minion import Minion
from .projectile import Projectile
from .config import config

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
        self.last_gold_tick = pygame.time.get_ticks()

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right-click
            self.player.move_to(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            mouse_pos = pygame.mouse.get_pos()
            self.projectiles.append(Projectile(self.player.pos, mouse_pos, self.player.attack_damage))

    def update(self):
        self.player.update()

        # Passive gold generation
        current_time = pygame.time.get_ticks()
        if current_time - self.last_gold_tick > 1000:
            self.player.gold += config.champion.gold_per_second
            self.last_gold_tick = current_time

        # Update projectiles and check for collisions
        for projectile in self.projectiles[:]:
            projectile.update()
            if not self.screen_rect.colliderect(projectile.rect):
                self.projectiles.remove(projectile)
            else:
                for minion in self.minions[:]:
                    if projectile.rect.colliderect(minion.rect):
                        minion.health -= projectile.attack_damage
                        if minion.health <= 0:
                            self.minions.remove(minion)
                            self.player.gold += config.minion.minion_last_hit_gold
                        self.projectiles.remove(projectile)
                        break

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.player.draw(screen)
        for minion in self.minions:
            minion.draw(screen)
        for projectile in self.projectiles:
            projectile.draw(screen)
