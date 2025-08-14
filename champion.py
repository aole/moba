import pygame

PLAYER_SPEED = 0.1

class Champion:
    def __init__(self, x, y, size=50):
        self.pos = pygame.math.Vector2(x, y)
        self.rect = pygame.Rect(x - size // 2, y - size // 2, size, size)
        self.color = (0, 0, 255)  # Blue
        self.speed = PLAYER_SPEED
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
        pygame.draw.rect(screen, self.color, self.rect)
