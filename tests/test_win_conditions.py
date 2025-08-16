import pygame
from src.game.game import Game
from src.game.state import GameState
from src.game.tower import Tower
from src.game.projectile import Projectile

def test_red_tower_destruction_ends_game():
    """Test that the game ends and blue wins when the red tower is destroyed."""
    pygame.init()
    game = Game(1536, 1024) # Use full screen size
    game.setup_game()
    game.state = GameState.PLAYING

    # Find the red tower
    red_tower = None
    for tower in game.towers:
        if tower.team == 'red':
            red_tower = tower
            break

    assert red_tower is not None

    # Destroy the red tower
    red_tower.health = 1 # Set health to 1 so one hit will destroy it

    # Create a projectile that will hit the tower
    projectile = Projectile(pos=red_tower.pos, attack_damage=1, source='blue', target=red_tower)
    game.projectiles.append(projectile)

    game.update()

    assert game.state == GameState.GAME_OVER
    assert game.winner == 'blue'

def test_blue_tower_destruction_ends_game():
    """Test that the game ends and red wins when the blue tower is destroyed."""
    pygame.init()
    game = Game(1536, 1024) # Use full screen size
    game.setup_game()
    game.state = GameState.PLAYING

    # Find the blue tower
    blue_tower = None
    for tower in game.towers:
        if tower.team == 'blue':
            blue_tower = tower
            break

    assert blue_tower is not None

    # Destroy the blue tower
    blue_tower.health = 1 # Set health to 1 so one hit will destroy it

    projectile = Projectile(pos=blue_tower.pos, attack_damage=1, source='red', target=blue_tower)
    game.projectiles.append(projectile)
    game.update()

    assert game.state == GameState.GAME_OVER
    assert game.winner == 'red'
