import pygame
from .config import config
from .entity import Entity

class Champion(Entity):
    def __init__(self, x, y, team, tower_pos):
        champion_config = config.blue_champion if team == 'blue' else config.red_champion
        super().__init__(
            x, y, champion_config.size, champion_config.image,
            health=champion_config.health,
            attack_damage=champion_config.attack_damage,
            team=team,
            center_aligned=True
        )
        self.gold = champion_config.starting_gold
        self.pos = pygame.math.Vector2(x, y)
        self.speed = champion_config.speed
        self.attack_speed = champion_config.attack_speed
        self.attack_range = champion_config.attack_range
        self.target_pos = None
        self.is_dead = False
        self.death_time = None
        self.start_pos = pygame.math.Vector2(x, y)
        self.last_attack_time = 0
        self.kills = 0
        self.deaths = 0
        self.assists = 0

        if tower_pos:
            offset = pygame.math.Vector2(config.tower.respawn_offset.x, config.tower.respawn_offset.y)
            self.respawn_pos = tower_pos + offset
        else:
            self.respawn_pos = self.start_pos

    def move_to(self, pos):
        self.target_pos = pygame.math.Vector2(pos)

    def update(self, entities, projectiles):
        if self.team == 'red':
            # AI for red champion
            target = self.find_closest_enemy(entities)
            if target:
                distance = self.pos.distance_to(target.pos)
                if distance < self.attack_range:
                    self.attack(target, projectiles)
                else:
                    self.move_to(target.pos)

        if self.target_pos:
            direction = self.target_pos - self.pos
            if direction.length() <= self.speed:
                self.pos = self.target_pos
                self.target_pos = None
            else:
                direction.normalize_ip()
                self.pos += direction * self.speed
            self.rect.center = self.pos

    def find_closest_enemy(self, entities):
        closest_enemy = None
        min_distance = float('inf')

        for entity in entities:
            if entity.team != self.team and not getattr(entity, 'is_dead', False):
                distance = self.pos.distance_to(entity.pos)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = entity
        return closest_enemy

    def attack(self, target, projectiles):
        from .projectile import Projectile
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > 1000 / self.attack_speed:
            projectiles.append(Projectile(self.pos.copy(), self.attack_damage, self.team, self, target=target))
            self.last_attack_time = current_time

    def draw(self, screen):
        super().draw(screen)
        champion_config = config.blue_champion if self.team == 'blue' else config.red_champion
        if config.debug.champion_range_visible:
            pygame.draw.circle(screen, (255, 255, 255), self.rect.center, champion_config.attack_range, 1)

    def die(self):
        super().die()
        self.deaths += 1
        self.death_time = pygame.time.get_ticks()

    def respawn(self):
        self.is_dead = False
        self.death_time = None
        self.health = self.max_health
        self.pos = self.respawn_pos.copy()
        self.rect.center = self.pos
        self.target_pos = None
