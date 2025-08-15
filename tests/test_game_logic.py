import pygame
from game.game import Game
from game.minion import Minion
from game.projectile import Projectile

def test_projectile_off_screen():
    """Test that a projectile is removed when it goes off-screen."""
    pygame.init()
    game = Game(800, 600)
    game.projectiles = []

    # Create a projectile that is already off-screen
    class Target:
        def __init__(self, pos):
            self.pos = pos
    projectile = Projectile(pygame.math.Vector2(-20, -20), Target(pygame.math.Vector2(-30, -30)), 1, 'player')
    game.projectiles.append(projectile)

    assert len(game.projectiles) == 1

    game.update()

    assert len(game.projectiles) == 0


def test_projectile_damages_minion():
    """Test that a projectile damages a minion and removes it when health is depleted."""
    pygame.init()
    game = Game(800, 600)
    game.minions = []
    game.projectiles = []
    # Disable automatic minion spawning for this test
    game.spawn_minions = lambda x, y: None

    minion = Minion(100, 100, 'red')
    minion.speed = 0 # Prevent minion from moving during test
    initial_health = minion.health
    game.minions.append(minion)

    # The champion's attack damage is from the config, so the projectile will have that damage
    class Target:
        def __init__(self, pos):
            self.pos = pos
    projectile = Projectile(pygame.math.Vector2(90, 100), Target(pygame.math.Vector2(100, 100)), game.player.attack_damage, 'player')
    projectile.rect = pygame.Rect(95, 95, 10, 10) # Ensure collision
    game.projectiles.append(projectile)

    # First hit
    game.update()

    assert len(game.projectiles) == 0 # Projectile is removed after hit
    assert len(game.minions) == 1 # Minion is not removed yet
    assert minion.health == initial_health - game.player.attack_damage

    # Keep hitting the minion until its health is depleted
    # The number of hits is ceiling of initial_health / attack_damage
    hits_to_kill = -(-initial_health // game.player.attack_damage) # Ceiling division
    for i in range(1, hits_to_kill):
        if minion not in game.minions:
            break
        class Target:
            def __init__(self, pos):
                self.pos = pos
        projectile = Projectile(pygame.math.Vector2(90, 100), Target(pygame.math.Vector2(100, 100)), game.player.attack_damage, 'player')
        projectile.rect = pygame.Rect(95, 95, 10, 10)
        game.projectiles.append(projectile)
        game.update()

    assert len(game.minions) == 0 # Minion is removed after its health is depleted
