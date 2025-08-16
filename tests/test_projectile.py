import pygame
import pytest
from game.projectile import Projectile
from game.config import config

# Mock Target class for testing purposes
class MockTarget:
    def __init__(self, pos, is_dead=False):
        self.pos = pygame.math.Vector2(pos)
        self.is_dead = is_dead

@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

def test_honing_projectile_creation():
    """Test that a honing Projectile can be created."""
    target = MockTarget((200, 100))
    projectile = Projectile(pos=pygame.math.Vector2(100, 100), attack_damage=1, team='player', attacker=None, target=target)
    assert projectile.target == target
    assert projectile.velocity.x > 0
    assert projectile.velocity.y == 0

def test_skill_shot_projectile_creation():
    """Test that a skill shot Projectile can be created."""
    direction = pygame.math.Vector2(1, 0)
    projectile = Projectile(pos=pygame.math.Vector2(100, 100), attack_damage=1, team='player', attacker=None, direction=direction)
    assert projectile.target is None
    assert projectile.velocity.x > 0
    assert projectile.velocity.y == 0

def test_projectile_update_honing():
    """Test that the honing projectile's position is updated correctly."""
    target = MockTarget((10, 0))
    projectile = Projectile(pos=pygame.math.Vector2(0, 0), attack_damage=1, team='player', attacker=None, target=target, speed=5)

    projectile.update()
    assert projectile.pos == pygame.math.Vector2(5, 0)

    projectile.update()
    assert projectile.pos == pygame.math.Vector2(10, 0)

def test_projectile_update_skill_shot():
    """Test that the skill shot projectile's position is updated correctly."""
    direction = pygame.math.Vector2(1, 0)
    projectile = Projectile(pos=pygame.math.Vector2(0, 0), attack_damage=1, team='player', attacker=None, direction=direction, speed=5)

    projectile.update()
    assert projectile.pos == pygame.math.Vector2(5, 0)

    projectile.update()
    assert projectile.pos == pygame.math.Vector2(10, 0)


def test_honing_projectile_target_dies():
    """Test that a honing projectile is removed if its target dies."""
    target = MockTarget((200, 100), is_dead=False)
    projectile = Projectile(pos=pygame.math.Vector2(100, 100), attack_damage=1, team='player', attacker=None, target=target)

    # Target is alive, projectile should not be removed
    projectile.update()
    assert not projectile.should_be_removed

    # Target dies
    target.is_dead = True
    projectile.update()
    assert projectile.should_be_removed
