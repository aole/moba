import pygame
from .config import config
from .entity import Entity

class Minion(Entity):
    def __init__(self, x, y, size=config.minion.size):
        super().__init__(
            x, y, size, config.minion.image,
            health=config.minion.health,
            attack_damage=config.minion.attack_damage
        )
