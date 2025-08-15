import pygame

class Projectile:
    def __init__(self, pos, target_pos):
        self.pos = pygame.math.Vector2(pos)
        self.speed = 10
        direction = pygame.math.Vector2(target_pos) - self.pos
        if direction.length() > 0:
            direction.normalize_ip()
        self.velocity = direction * self.speed
        self.rect = pygame.Rect(self.pos.x - 5, self.pos.y - 5, 10, 10)
        self.color = (255, 0, 0) # Red

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, 5)
