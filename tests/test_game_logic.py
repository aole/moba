import pygame
from game.game import Game
from game.minion import Minion
from game.projectile import Projectile

def test_projectile_minion_collision():
    """Test that a projectile and a minion are removed upon collision."""
    # Mocking pygame.init() and other display related things is not necessary
    # as we are not testing drawing or event handling that requires a display.
    # We can directly instantiate and manipulate our game objects.

    game = Game(800, 600)

    # Clear existing minions and projectiles for a clean test environment
    game.minions = []
    game.projectiles = []

    # Add a minion and a projectile that will collide
    minion = Minion(100, 100)
    game.minions.append(minion)

    # Projectile aimed at the minion
    projectile = Projectile((90, 100), (100, 100))
    # Manually set the rect for the projectile to ensure collision for the test
    projectile.rect = pygame.Rect(95, 95, 10, 10)
    game.projectiles.append(projectile)

    assert len(game.minions) == 1
    assert len(game.projectiles) == 1

    # In the game's update loop, the projectile moves first, then collision is checked.
    # Let's move the projectile to the collision point.
    projectile.update()

    # Now call the game's update method to check for collisions
    game.update()

    assert len(game.minions) == 0
    assert len(game.projectiles) == 0

def test_projectile_off_screen():
    """Test that a projectile is removed when it goes off-screen."""
    game = Game(800, 600)
    game.projectiles = []

    # Create a projectile that is already off-screen
    projectile = Projectile((-20, -20), (-30, -30))
    game.projectiles.append(projectile)

    assert len(game.projectiles) == 1

    game.update()

    assert len(game.projectiles) == 0
