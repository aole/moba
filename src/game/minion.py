import pygame
from .config import config
from .entity import Entity
from .projectile import Projectile
from .tower import Tower
from .effect import Effect

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

    def update(self, entities, projectiles, effects):
        # 1. Find tower_target for movement
        enemy_towers = [entity for entity in entities if isinstance(entity, Tower) and entity.team != self.team]
        tower_target = None
        if enemy_towers:
            min_distance_to_tower = float('inf')
            for tower in enemy_towers:
                distance = self.pos.distance_to(tower.pos)
                if distance < min_distance_to_tower:
                    min_distance_to_tower = distance
                    tower_target = tower

        # 2. Find attack_target for attacking
        all_enemies = [entity for entity in entities if entity.team != self.team]
        attack_target = None
        min_distance_to_enemy = float('inf')
        if all_enemies:
            for enemy in all_enemies:
                distance = self.pos.distance_to(enemy.pos)
                if distance < min_distance_to_enemy:
                    min_distance_to_enemy = distance
                    attack_target = enemy

        # 3. Decide whether to attack or move
        if attack_target and min_distance_to_enemy <= config.minion.attack_range:
            # If any enemy is in range, attack it
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time > config.minion.attack_interval:
                self.last_attack_time = current_time
                projectiles.append(Projectile(self.pos.copy(), self.attack_damage, self.team, self, target=attack_target, speed=config.minion.projectile_speed, size=config.minion.projectile_size, color=config.minion.projectile_color))
                effects.append(Effect(self.pos.copy(), config.effect.flash.size, tuple(config.effect.flash.color), config.effect.flash.duration))
        else:
            # No enemy in attack range, so move
            movement_target = tower_target if tower_target else attack_target
            if movement_target:
                direction = (movement_target.pos - self.pos).normalize()
                self.pos += direction * self.speed
                self.rect.topleft = self.pos


    def draw(self, screen):
        super().draw(screen)
        if config.debug.minion_range_visible:
            pygame.draw.circle(screen, (255, 255, 255), self.rect.center, config.minion.attack_range, 1)
