import pygame
from .config import config

class Minion:
    def __init__(self, x, y, size=config.minion.size):
        self.rect = pygame.Rect(x, y, size, size)
        self.image = pygame.image.load(config.minion.image)
        self.image = pygame.transform.scale(self.image, (size, size))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
