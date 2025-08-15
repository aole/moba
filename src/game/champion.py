import pygame
from .config import config

class Champion:
    def __init__(self, x, y, size=config.champion.size):
        self.pos = pygame.math.Vector2(x, y)
        self.rect = pygame.Rect(x - size // 2, y - size // 2, size, size)
        self.image = pygame.image.load(config.champion.image)
        self.image = pygame.transform.scale(self.image, (size, size))
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

    def draw(self, screen):
        screen.blit(self.image, self.rect)
