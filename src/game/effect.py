import pygame

class Effect:
    def __init__(self, pos, size, color, duration):
        self.pos = pos
        self.size = size
        self.color = color
        self.duration = duration
        self.created_at = pygame.time.get_ticks()

    def update(self):
        pass

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.created_at
        if elapsed_time > self.duration:
            return

        # Fade effect
        alpha = 255 * (1 - (elapsed_time / self.duration))
        if alpha < 0:
            alpha = 0

        surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (*self.color, alpha), (self.size, self.size), self.size)
        screen.blit(surface, (self.pos.x - self.size, self.pos.y - self.size))
