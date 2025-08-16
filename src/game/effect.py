import pygame

class Effect(pygame.sprite.Sprite):
    def __init__(self, pos, size, color, duration):
        super().__init__()
        self.duration = duration  # milliseconds
        self.start_time = pygame.time.get_ticks()

        self.radius = size
        self.color = color

        # Create a glow surface with alpha
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        # How long has the flash been alive
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed > self.duration:
            self.kill()
            return

        # Fade out over time
        alpha = 255 * (1 - elapsed / self.duration)
        self.image.fill((0, 0, 0, 0))  # clear
        pygame.draw.circle(self.image, (*self.color, int(alpha)), (self.radius, self.radius), self.radius)

    def draw(self, screen):
        # This draw method is not strictly necessary if using sprite groups to draw,
        # but can be useful for debugging or alternative drawing methods.
        screen.blit(self.image, self.rect)
