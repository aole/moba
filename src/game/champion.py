import pygame
from .config import config
from .entity import Entity

class Champion(Entity):
    def __init__(self, x, y, size=config.champion.size):
        super().__init__(x, y, size, config.champion.image, health=50, center_aligned=True)
        self.pos = pygame.math.Vector2(x, y)
        self.speed = config.champion.speed
        self.target_pos = None

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
