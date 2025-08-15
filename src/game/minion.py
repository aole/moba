import pygame
from .config import config
from .entity import Entity
from .projectile import Projectile

class Minion(Entity):
    def __init__(self, x, y, size=config.minion.size):
        super().__init__(
            x, y, size, config.minion.image,
            health=config.minion.health,
            attack_damage=config.minion.attack_damage
        )
        self.pos = pygame.math.Vector2(x, y)
        self.last_attack_time = 0

    def update(self, champion, projectiles):
        distance_to_champion = self.pos.distance_to(champion.pos)
        current_time = pygame.time.get_ticks()

        if distance_to_champion <= config.minion.attack_range:
            if current_time - self.last_attack_time > config.minion.attack_interval:
                self.last_attack_time = current_time
                projectiles.append(Projectile(self.pos.copy(), champion, self.attack_damage, 'minion', config.minion.projectile_speed, config.minion.projectile_size, config.minion.projectile_color))
