import pygame

PLAYER_SPEED = 0.1

class Champion:
    def __init__(self, x, y, size=50):
        self.pos = pygame.math.Vector2(x, y)
        self.rect = pygame.Rect(x - size // 2, y - size // 2, size, size)
        self.image = pygame.image.load("champion.png")
        self.image = pygame.transform.scale(self.image, (size, size))
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
        screen.blit(self.image, self.rect)
