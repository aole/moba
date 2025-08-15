import pygame
from .config import config
from .entity import Entity
from .projectile import Projectile
from .tower import Tower

class Minion(Entity):
    def __init__(self, x, y, team, size=config.minion.size):
        super().__init__(
            x, y, size, config.minion.image,
            health=config.minion.health,
            attack_damage=config.minion.attack_damage,
            team=team
        )
        self.pos = pygame.math.Vector2(x, y)
        self.last_attack_time = 0
        self.speed = config.minion.speed

    def update(self, entities, projectiles):
        # Separate towers from other entities
        enemy_towers = [entity for entity in entities if isinstance(entity, Tower) and entity.team != self.team]
        other_enemies = [entity for entity in entities if not isinstance(entity, Tower) and entity.team != self.team]

        target = None
        min_distance = float('inf')

        # Prioritize towers
        if enemy_towers:
            for tower in enemy_towers:
                distance = self.pos.distance_to(tower.pos)
                if distance < min_distance:
                    min_distance = distance
                    target = tower
        else: # If no towers, target other enemies
            for entity in other_enemies:
                distance = self.pos.distance_to(entity.pos)
                if distance < min_distance:
                    min_distance = distance
                    target = entity

        if target:
            distance_to_target = self.pos.distance_to(target.pos)
            if distance_to_target > config.minion.attack_range:
                # Move towards the target if it's outside attack range
                direction = (target.pos - self.pos).normalize()
                self.pos += direction * self.speed
                self.rect.topleft = self.pos
            else:
                # Attack if in range
                current_time = pygame.time.get_ticks()
                if current_time - self.last_attack_time > config.minion.attack_interval:
                    self.last_attack_time = current_time
                    projectiles.append(Projectile(self.pos.copy(), target, self.attack_damage, self.team, config.minion.projectile_speed, config.minion.projectile_size, config.minion.projectile_color))


    def draw(self, screen):
        super().draw(screen)
        if config.debug.minion_range_visible:
            pygame.draw.circle(screen, (255, 255, 255), self.rect.center, config.minion.attack_range, 1)
