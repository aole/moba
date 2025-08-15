import pygame
from game.projectile import Projectile

def test_projectile_creation():
    """Test that a Projectile can be created."""
    class Target:
        def __init__(self, pos):
            self.pos = pos
    projectile = Projectile(pygame.math.Vector2(100, 100), Target(pygame.math.Vector2(200, 100)), 1, 'player')
    projectile.update()
    assert projectile.velocity.x > 0
    assert projectile.velocity.y == 0

def test_projectile_update():
    """Test that the projectile's position is updated correctly."""
    # Create a projectile moving horizontally
    class Target:
        def __init__(self, pos):
            self.pos = pos
    projectile = Projectile(pygame.math.Vector2(0, 0), Target(pygame.math.Vector2(10, 0)), 1, 'player', speed=5)

    # Update position and check
    projectile.update()
    assert projectile.pos == pygame.math.Vector2(5, 0)

    projectile.update()
    assert projectile.pos == pygame.math.Vector2(10, 0)

def test_tower_projectile_movement():
    """Test that a projectile from a tower moves correctly."""
    class Target:
        def __init__(self, pos):
            self.pos = pos
    projectile = Projectile(pygame.math.Vector2(100, 100), Target(pygame.math.Vector2(200, 100)), 1, 'blue', speed=10)

    initial_pos = projectile.pos.copy()
    projectile.update()

    assert projectile.pos.x > initial_pos.x
    assert projectile.pos.y == initial_pos.y
