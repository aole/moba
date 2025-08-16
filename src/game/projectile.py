import pygame
from .config import config

class Projectile:
    def __init__(self, pos, attack_damage, team, attacker, target=None, direction=None, speed=None, size=None, color=None):
        self.pos = pygame.math.Vector2(pos)
        self.attack_damage = attack_damage
        self.team = team
        self.attacker = attacker
        self.target = target
        self.speed = speed or config.projectile.speed
        self.size = size or config.projectile.size
        self.color = tuple(color or config.projectile.color)
        self.rect = pygame.Rect(self.pos.x - self.size // 2, self.pos.y - self.size // 2, self.size, self.size)
        self.should_be_removed = False
        self.velocity = pygame.math.Vector2(0, 0)

        if self.target:
            direction_to_target = self.target.pos - self.pos
            if direction_to_target.length() > 0:
                self.velocity = direction_to_target.normalize() * self.speed
        elif direction:
            if direction.length() > 0:
                self.velocity = direction.normalize() * self.speed

    def update(self):
        if self.target:
            if getattr(self.target, 'is_dead', False):
                self.should_be_removed = True
                return

            direction = self.target.pos - self.pos
            if direction.length() > 0:
                direction.normalize_ip()
            self.velocity = direction * self.speed

        self.pos += self.velocity
        self.rect.center = self.pos

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.size // 2)
