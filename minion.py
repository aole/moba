import pygame

class Minion:
    def __init__(self, x, y, size=40):
        self.rect = pygame.Rect(x, y, size, size)
        self.image = pygame.image.load("minion.png")
        self.image = pygame.transform.scale(self.image, (size, size))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
