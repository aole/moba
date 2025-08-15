import pygame
import random
from .champion import Champion
from .minion import Minion
from .projectile import Projectile
from .tower import Tower
from .config import config

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_rect = pygame.Rect(0, 0, screen_width, screen_height)

        self.background = pygame.image.load(config.game.background_image)
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.game_over = False
        self.projectiles = []
        self.towers = []
        self.setup_game()

    def setup_game(self):
        self.player = Champion(self.screen_width // 2, self.screen_height // 2)
        self.minions = []
        self.projectiles = []
        self.towers = []
        self.last_gold_tick = pygame.time.get_ticks()
        self.game_over = False
        self.spawn_minions(4)
        self.towers.append(Tower(100, self.screen_height // 2, 'blue'))
        self.towers.append(Tower(self.screen_width - 100, self.screen_height // 2, 'red'))

    def spawn_minions(self, number):
        for _ in range(number):
            x = random.randint(50, self.screen_width - 50)
            y = random.randint(50, self.screen_height - 50)
            self.minions.append(Minion(x, y))

    def handle_input(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.setup_game()
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right-click
            self.player.move_to(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            mouse_pos = pygame.mouse.get_pos()
            class Target:
                def __init__(self, pos):
                    self.pos = pos
            self.projectiles.append(Projectile(self.player.pos.copy(), Target(pygame.math.Vector2(mouse_pos)), self.player.attack_damage, 'player'))

    def update(self):
        if self.game_over:
            return

        self.player.update()

        # Passive gold generation
        current_time = pygame.time.get_ticks()
        if current_time - self.last_gold_tick > 1000:
            self.player.gold += config.champion.gold_per_second
            self.last_gold_tick = current_time

        # Update minions
        for minion in self.minions:
            minion.update(self.player, self.projectiles)

        # Update towers
        for tower in self.towers:
            tower.update(self.player, self.projectiles)

        # Ensure at least 2 minions are alive
        if len(self.minions) < 2:
            self.spawn_minions(2 - len(self.minions))

        # Update projectiles and check for collisions
        for projectile in list(self.projectiles):
            projectile.update()
            if not self.screen_rect.colliderect(projectile.rect):
                if projectile in self.projectiles:
                    self.projectiles.remove(projectile)
                continue

            if projectile.source == 'player':
                # Check collision with minions
                for minion in list(self.minions):
                    if projectile.rect.colliderect(minion.rect):
                        minion.health -= projectile.attack_damage
                        if minion.health <= 0:
                            self.minions.remove(minion)
                            self.player.gold += config.minion.minion_last_hit_gold
                        if projectile in self.projectiles:
                            self.projectiles.remove(projectile)
                        break
            elif projectile.source == 'minion' or projectile.source in ['blue', 'red']:
                # Check collision with player
                if projectile.rect.colliderect(self.player.rect):
                    self.player.health -= projectile.attack_damage
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    if self.player.health <= 0:
                        self.game_over = True

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        if self.game_over:
            self.draw_game_over(screen)
        else:
            self.player.draw(screen)
            for minion in self.minions:
                minion.draw(screen)
            for projectile in self.projectiles:
                projectile.draw(screen)
            for tower in self.towers:
                tower.draw(screen)



    def draw_game_over(self, screen):
        text = self.font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 50))
        screen.blit(text, text_rect)

        restart_text = self.small_font.render("Press 'SPACE' to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + 50))
        screen.blit(restart_text, restart_rect)
