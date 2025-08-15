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

