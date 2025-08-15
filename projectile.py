import pygame
from config import config

class Projectile:
    def __init__(self, pos, target_pos):
        self.pos = pygame.math.Vector2(pos)
        self.speed = config.projectile.speed
        direction = pygame.math.Vector2(target_pos) - self.pos
        if direction.length() > 0:
            direction.normalize_ip()
        self.velocity = direction * self.speed
        size = config.projectile.size
        self.rect = pygame.Rect(self.pos.x - size // 2, self.pos.y - size // 2, size, size)
        self.color = tuple(config.projectile.color)

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, 5)
