import pygame
from projectile import Projectile

def test_projectile_creation():
    """Test that a Projectile can be created."""
    projectile = Projectile((100, 100), (200, 100))
    assert projectile.pos == pygame.math.Vector2(100, 100)
    # The direction should be (1, 0)
    assert projectile.velocity.x > 0
    assert projectile.velocity.y == 0

def test_projectile_update():
    """Test that the projectile's position is updated correctly."""
    # Create a projectile moving horizontally
    projectile = Projectile((0, 0), (10, 0))
    projectile.speed = 5
    projectile.velocity = pygame.math.Vector2(5, 0) # Overriding for predictability

    # Update position and check
    projectile.update()
    assert projectile.pos == pygame.math.Vector2(5, 0)

    projectile.update()
    assert projectile.pos == pygame.math.Vector2(10, 0)
