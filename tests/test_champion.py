import pygame
import pytest
from src.game.champion import Champion
from src.game.config import config

@pytest.fixture
def mock_pygame_image_load(mocker):
    """Fixture to mock pygame.image.load."""
    mock_surface = pygame.Surface((50, 50))
    return mocker.patch('pygame.image.load', return_value=mock_surface)

def test_champion_creation(mock_pygame_image_load):
    """Test that a Champion can be created."""
    champion = Champion(100, 100, 'blue')
    assert champion.pos == pygame.math.Vector2(100, 100)
    assert champion.rect.center == (100, 100)
    assert champion.target_pos is None
    mock_pygame_image_load.assert_called_once_with(config.champion.image)

def test_champion_move_to(mock_pygame_image_load):
    """Test that move_to sets the target position."""
    champion = Champion(100, 100, 'blue')
    champion.move_to((200, 200))
    assert champion.target_pos == pygame.math.Vector2(200, 200)

def test_champion_update_movement(mock_pygame_image_load):
    """Test that the champion moves towards the target position."""
    champion = Champion(0, 0, 'blue')
    champion.speed = 1
    champion.move_to((10, 0))

    # Update multiple times to check movement
    champion.update()
    assert champion.pos.x == 1
    champion.update()
    assert champion.pos.x == 2

def test_champion_reaches_destination(mock_pygame_image_load):
    """Test that the champion stops when it reaches the target destination."""
    champion = Champion(0, 0, 'blue')
    champion.speed = 5
    champion.move_to((10, 0))

    # Move close to the destination
    for _ in range(2):
        champion.update()

    assert champion.pos == pygame.math.Vector2(10, 0)
    assert champion.target_pos is None

    # Test that the champion doesn't move further
    champion.update()
    assert champion.pos == pygame.math.Vector2(10, 0)

from src.game.game import Game

def test_champion_respawn(mocker, mock_pygame_image_load):
    """Test that the champion respawns after 5 seconds."""
    pygame.init()
    game = Game(1536, 1024)
    game.setup_game()
    player = game.player

    # Mock pygame.time.get_ticks
    mock_ticks = mocker.patch('pygame.time.get_ticks')

    # Kill the player
    mock_ticks.return_value = 1000  # Initial time
    player.health = 0

    # To trigger the death, we need to go through the game's update loop
    # where it checks for collisions and health.
    # We'll simulate a projectile hitting the player.
    class FakeProjectile:
        def __init__(self, target):
            self.rect = target.rect
            self.source = 'red' # Enemy team
            self.attack_damage = 1
            self.should_be_removed = False
        def update(self):
            pass

    # A dummy projectile to trigger the health check
    game.projectiles.append(FakeProjectile(player))

    # This update call will process the projectile hit and call player.die()
    game.update()

    assert player.is_dead is True
    assert player.death_time == 1000

    # Advance time to just before the respawn time
    mock_ticks.return_value = 5999 # 4999ms after death
    game.update()
    assert player.is_dead is True # Should not have respawned yet

    # Advance time to the respawn time
    mock_ticks.return_value = 6000 # 5000ms after death
    game.update()
    assert player.is_dead is False
    assert player.health == player.max_health
    assert player.pos == player.start_pos
