import pygame
import random
from .champion import Champion
from .minion import Minion
from .projectile import Projectile
from .tower import Tower
from .config import config
from .state import GameState
from .button import Button

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_rect = pygame.Rect(0, 0, screen_width, screen_height)

        self.background = pygame.image.load(config.game.background_image)
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

        self.font = pygame.font.Font(config.game.font_path, 74)
        self.small_font = pygame.font.Font(config.game.font_path, 36)
        self.state = GameState.START
        self.projectiles = []
        self.towers = []
        self.running = True

        self._create_buttons()

    def _create_buttons(self):
        button_width = 200
        button_height = 50
        button_x = self.screen_width / 2 - button_width / 2
        button_bg_color = (100, 100, 100)
        text_color = (255, 255, 255)

        self.start_buttons = [
            Button(button_x, 400, button_width, button_height, "New Game", self.small_font, button_bg_color, text_color, self.start_new_game),
            Button(button_x, 500, button_width, button_height, "Exit", self.small_font, button_bg_color, text_color, self.exit_game)
        ]

        self.pause_buttons = [
            Button(button_x, 300, button_width, button_height, "Resume", self.small_font, button_bg_color, text_color, self.resume_game),
            Button(button_x, 400, button_width, button_height, "New Game", self.small_font, button_bg_color, text_color, self.start_new_game),
            Button(button_x, 500, button_width, button_height, "Exit", self.small_font, button_bg_color, text_color, self.exit_game)
        ]

        self.game_over_buttons = [
            Button(button_x, 400, button_width, button_height, "New Game", self.small_font, button_bg_color, text_color, self.start_new_game),
            Button(button_x, 500, button_width, button_height, "Exit", self.small_font, button_bg_color, text_color, self.exit_game)
        ]

    def start_new_game(self):
        self.setup_game()

    def resume_game(self):
        self.state = GameState.PLAYING

    def exit_game(self):
        self.running = False

    def setup_game(self):
        self.player = Champion(self.screen_width // 2, self.screen_height // 2, 'blue')
        self.minions = []
        self.projectiles = []
        self.towers = []
        self.last_gold_tick = pygame.time.get_ticks()
        self.state = GameState.PLAYING
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
        if self.state == GameState.START:
            self.handle_start_input(event)
        elif self.state == GameState.PLAYING:
            self.handle_playing_input(event)
        elif self.state == GameState.PAUSED:
            self.handle_pause_input(event)
        elif self.state == GameState.GAME_OVER:
            self.handle_game_over_input(event)

    def handle_start_input(self, event):
        for button in self.start_buttons:
            button.handle_event(event)

    def handle_playing_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = GameState.PAUSED
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right-click
            self.player.move_to(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            mouse_pos = pygame.mouse.get_pos()
            class Target:
                def __init__(self, pos):
                    self.pos = pos
            self.projectiles.append(Projectile(self.player.pos.copy(), Target(pygame.math.Vector2(mouse_pos)), self.player.attack_damage, self.player.team, is_homing=False))

    def handle_pause_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.resume_game()
        for button in self.pause_buttons:
            button.handle_event(event)

    def handle_game_over_input(self, event):
        for button in self.game_over_buttons:
            button.handle_event(event)

    def update(self):
        if self.state != GameState.PLAYING:
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
                            self.state = GameState.GAME_OVER
                        elif isinstance(entity, Tower):
                            self.towers.remove(entity)
                            # Potentially end the game or grant a large amount of gold
                    break # Projectile hits one entity at a time

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        if self.state == GameState.START:
            self.draw_start_screen(screen)
        elif self.state == GameState.PLAYING:
            self.draw_playing_screen(screen)
        elif self.state == GameState.PAUSED:
            # Draw the playing screen underneath the pause menu
            self.draw_playing_screen(screen)
            self.draw_pause_screen(screen)
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over_screen(screen)

    def draw_playing_screen(self, screen):
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

    def draw_start_screen(self, screen):
        title_text = self.font.render("MOBA Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width / 2, 200))
        screen.blit(title_text, title_rect)

        for button in self.start_buttons:
            button.draw(screen)

    def draw_pause_screen(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0,0))

        title_text = self.font.render("Paused", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width / 2, 200))
        screen.blit(title_text, title_rect)

        for button in self.pause_buttons:
            button.draw(screen)

    def draw_game_over_screen(self, screen):
        title_text = self.font.render("Game Over", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.screen_width / 2, 200))
        screen.blit(title_text, title_rect)

        for button in self.game_over_buttons:
            button.draw(screen)
