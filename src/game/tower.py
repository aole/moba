import pygame
from .config import config
from .entity import Entity
from .projectile import Projectile

class Tower(Entity):
    def __init__(self, x, y, team, size=100):
        self.team = team
        if self.team == 'blue':
            image_path = config.tower.blue_image
        else:
            image_path = config.tower.red_image

        super().__init__(
            x, y, size, image_path,
            health=config.tower.health,
            attack_damage=config.tower.attack_damage
        )
        self.pos = pygame.math.Vector2(x, y)
        self.last_attack_time = 0

    def update(self, target, projectiles):
        if not target:
            return

        distance_to_target = self.pos.distance_to(target.pos)
        current_time = pygame.time.get_ticks()

        if distance_to_target <= config.tower.attack_range:
            if current_time - self.last_attack_time > config.tower.attack_interval:
                self.last_attack_time = current_time
                projectiles.append(Projectile(self.pos.copy(), target, self.attack_damage, self.team, config.tower.projectile_speed, config.tower.projectile_size, config.tower.projectile_color))

    def draw(self, screen):
        super().draw(screen)
        if config.debug.tower_range_visible:
            pygame.draw.circle(screen, (255, 255, 255), self.rect.center, config.tower.attack_range, 1)
