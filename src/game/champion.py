import pygame
from .config import config
from .entity import Entity

class Champion(Entity):
    def __init__(self, x, y, team, size=config.champion.size):
        super().__init__(
            x, y, size, config.champion.image,
            health=config.champion.health,
            attack_damage=config.champion.attack_damage,
            team=team,
            center_aligned=True
        )
        self.gold = config.champion.starting_gold
        self.pos = pygame.math.Vector2(x, y)
        self.speed = config.champion.speed
        self.attack_speed = config.champion.attack_speed
        self.target_pos = None
        self.is_dead = False
        self.death_time = None
        self.start_pos = pygame.math.Vector2(x, y)

    def move_to(self, pos):
        self.target_pos = pygame.math.Vector2(pos)

    def update(self):
        if self.target_pos:
            direction = self.target_pos - self.pos
            if direction.length() <= self.speed:
                self.pos = self.target_pos
                self.target_pos = None
            else:
                direction.normalize_ip()
                self.pos += direction * self.speed
            self.rect.center = self.pos

    def draw(self, screen):
        super().draw(screen)
        if config.debug.champion_range_visible:
            pygame.draw.circle(screen, (255, 255, 255), self.rect.center, config.champion.attack_range, 1)

    def die(self):
        self.is_dead = True
        self.death_time = pygame.time.get_ticks()
        self.health = 0

    def respawn(self):
        self.is_dead = False
        self.death_time = None
        self.health = self.max_health
        self.pos = self.start_pos.copy()
        self.rect.center = self.pos
        self.target_pos = None
