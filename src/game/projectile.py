import pygame
from .config import config

class Projectile:
    def __init__(self, pos, target, attack_damage, source, speed=None, size=None, color=None, is_homing=True):
        self.pos = pygame.math.Vector2(pos)
        self.target = target
        self.attack_damage = attack_damage
        self.source = source
        self.speed = speed or config.projectile.speed
        self.size = size or config.projectile.size
        self.color = tuple(color or config.projectile.color)
        self.is_homing = is_homing
        self.rect = pygame.Rect(self.pos.x - self.size // 2, self.pos.y - self.size // 2, self.size, self.size)
        self.should_be_removed = False

        direction = self.target.pos - self.pos
        if direction.length() > 0:
            direction.normalize_ip()
        self.velocity = direction * self.speed

    def update(self):
        if self.is_homing:
            direction = self.target.pos - self.pos
            if direction.length() > 0:
                direction.normalize_ip()
            self.velocity = direction * self.speed

        self.pos += self.velocity
        self.rect.center = self.pos

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.size // 2)
