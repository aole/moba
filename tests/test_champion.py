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
