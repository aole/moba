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

        self.font = pygame.font.Font(config.game.font_path, 74)
        self.small_font = pygame.font.Font(config.game.font_path, 36)
        self.game_over = False
        self.projectiles = []
        self.towers = []
        self.setup_game()

    def setup_game(self):
        self.player = Champion(self.screen_width // 2, self.screen_height // 2, 'blue')
        self.minions = []
        self.projectiles = []
        self.towers = []
        self.last_gold_tick = pygame.time.get_ticks()
        self.game_over = False
        self.spawn_minions(2, 'blue')
        self.spawn_minions(2, 'red')
        for tower_config in config.tower.locations:
            self.towers.append(Tower(tower_config['x'], tower_config['y'], tower_config['team']))

    def spawn_minions(self, number, team):
        for _ in range(number):
            if team == 'blue':
                x = random.randint(50, self.screen_width // 2 - 100)
            else: # red
                x = random.randint(self.screen_width // 2 + 100, self.screen_width - 50)
            y = random.randint(50, self.screen_height - 50)
            self.minions.append(Minion(x, y, team))

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
            self.projectiles.append(Projectile(self.player.pos.copy(), Target(pygame.math.Vector2(mouse_pos)), self.player.attack_damage, self.player.team, is_homing=False))

    def update(self):
        if self.game_over:
            return

        self.player.update()

        # Passive gold generation
        current_time = pygame.time.get_ticks()
        if current_time - self.last_gold_tick > 1000:
            self.player.gold += config.champion.gold_per_second
            self.last_gold_tick = current_time

        entities = [self.player] + self.minions + self.towers
        # Update minions
        for minion in self.minions:
            minion.update(entities, self.projectiles)

        # Update towers
        for tower in self.towers:
            tower.update(entities, self.projectiles)

        # Ensure at least 1 minion of each team is alive
        blue_minions = sum(1 for m in self.minions if m.team == 'blue')
        red_minions = sum(1 for m in self.minions if m.team == 'red')

        if blue_minions == 0:
            self.spawn_minions(1, 'blue')
        if red_minions == 0:
            self.spawn_minions(1, 'red')

        # Update projectiles and check for collisions
        entities = self.minions + self.towers + [self.player]
        for projectile in list(self.projectiles):
            projectile.update()
            if not self.screen_rect.colliderect(projectile.rect):
                if projectile in self.projectiles:
                    self.projectiles.remove(projectile)
                continue

            for entity in entities:
                if projectile.rect.colliderect(entity.rect) and projectile.source != entity.team:
                    entity.health -= projectile.attack_damage
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)

                    if entity.health <= 0:
                        if isinstance(entity, Minion):
                            self.minions.remove(entity)
                            if projectile.source == self.player.team: # Gold for last hit
                                self.player.gold += config.minion.minion_last_hit_gold
                        elif isinstance(entity, Champion):
                            self.game_over = True
                        elif isinstance(entity, Tower):
                            self.towers.remove(entity)
                            # Potentially end the game or grant a large amount of gold
                    break # Projectile hits one entity at a time

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
            self.draw_status_bar(screen)

    def draw_status_bar(self, screen):
        # Define the stats to display
        stats = [
            f"Gold: {self.player.gold}",
            f"Health: {self.player.health}",
            f"Attack Damage: {self.player.attack_damage}",
            f"Attack Speed: {self.player.attack_speed}"
        ]

        # Starting position for the first stat
        start_x = 10
        y = 10
        padding = 20  # Pixels between stats

        # Render and blit each stat
        for stat in stats:
            text_surface = self.small_font.render(stat, True, (255, 255, 255))
            screen.blit(text_surface, (start_x, y))
            start_x += text_surface.get_width() + padding

    def draw_game_over(self, screen):
        text = self.font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 50))
        screen.blit(text, text_rect)

        restart_text = self.small_font.render("Press 'SPACE' to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + 50))
        screen.blit(restart_text, restart_rect)
