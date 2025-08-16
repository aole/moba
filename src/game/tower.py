import pygame
from .config import config
from .entity import Entity
from .projectile import Projectile

class Tower(Entity):
    def __init__(self, x, y, team):
        self.team = team
        if self.team == 'blue':
            image_path = config.tower.blue_image
        else:
            image_path = config.tower.red_image

        super().__init__(
            x, y, config.tower.size, image_path,
            health=config.tower.health,
            attack_damage=config.tower.attack_damage,
            team=self.team,
            center_aligned=True
        )
        self.pos = pygame.math.Vector2(x, y)
        self.last_attack_time = 0

    def update(self, entities, projectiles):
        closest_enemy = None
        min_distance = float('inf')

        # Target prioritization: Minions first, then Champions
        # In this implementation, we simply find the closest enemy.
        # A more advanced implementation could prioritize minions.
        for entity in entities:
            if entity.team != self.team and not getattr(entity, 'is_dead', False):
                distance = self.pos.distance_to(entity.pos)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = entity

        if closest_enemy and min_distance <= config.tower.attack_range:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time > config.tower.attack_interval:
                self.last_attack_time = current_time
                projectiles.append(Projectile(self.pos.copy(), closest_enemy, self.attack_damage, self.team, config.tower.projectile_speed, config.tower.projectile_size, config.tower.projectile_color))

    def draw(self, screen):
        super().draw(screen)
        if config.debug.tower_range_visible:
            pygame.draw.circle(screen, (255, 255, 255), self.rect.center, config.tower.attack_range, 1)
