import pygame

class Minion:
    def __init__(self, x, y, size=40):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = (0, 255, 0)  # Green

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
