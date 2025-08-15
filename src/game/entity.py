import pygame

class Entity:
    def __init__(self, x, y, size, image_path, health, attack_damage, team=None, center_aligned=False):
        self.image = pygame.image.load(image_path)
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        aspect_ratio = original_height / original_width
        new_width = size
        new_height = int(new_width * aspect_ratio)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        if center_aligned:
            self.rect = self.image.get_rect(center=(x, y))
        else:
            self.rect = self.image.get_rect(topleft=(x, y))
        self.max_health = health
        self.health = health
        self.attack_damage = attack_damage
        self.team = team

    def draw(self, screen):
        # Draw health bar
        health_bar_width = self.rect.width
        health_bar_height = 5
        health_bar_x = self.rect.x
        health_bar_y = self.rect.y - health_bar_height - 5

        health_percentage = self.health / self.max_health
        current_health_width = health_bar_width * health_percentage

        health_bar_color = (255, 0, 0) # Default red
        if self.team == 'blue':
            health_bar_color = (0, 0, 255)

        # Health bar background
        pygame.draw.rect(screen, (128, 128, 128), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        # Current health
        pygame.draw.rect(screen, health_bar_color, (health_bar_x, health_bar_y, current_health_width, health_bar_height))

        screen.blit(self.image, self.rect)
