import pytest
from src.game.champion import Champion
from src.game.game import Game
from src.game.config import config
import pygame

@pytest.fixture
def game():
    pygame.init()
    game = Game(800, 600)
    return game

class TestGoldSystem:
    def test_starting_gold(self, game):
        assert game.player.gold == config.champion.starting_gold

    def test_passive_gold_generation(self, game, mocker):
        mocker.patch('pygame.time.get_ticks', return_value=0)
        game.last_gold_tick = 0
        initial_gold = game.player.gold

        # Simulate 1 second passing
        mocker.patch('pygame.time.get_ticks', return_value=1001)
        game.update()

        expected_gold = initial_gold + config.champion.gold_per_second
        assert game.player.gold == expected_gold

    def test_last_hit_gold(self, game, mocker):
        # We need to control time to avoid passive gold generation
        mock_time = mocker.patch('pygame.time.get_ticks')
        mock_time.return_value = 0
        game.last_gold_tick = 0

        minion = game.minions[0]
        minion.health = 1
        initial_gold = game.player.gold

        # Create a projectile that will kill the minion
        from src.game.projectile import Projectile
        projectile = Projectile(game.player.pos, minion.rect.center, game.player.attack_damage)
        game.projectiles.append(projectile)

        # Update the game to process the collision and minion death
        # Loop enough times for the projectile to reach the minion
        for i in range(1, 21):
            # We don't want passive gold to interfere, so we advance time by a small amount
            mock_time.return_value = i * 10
            game.update()
            # If minion is dead, we can stop
            if len(game.minions) < 4:
                break

        expected_gold = initial_gold + config.minion.minion_last_hit_gold
        assert game.player.gold == expected_gold
