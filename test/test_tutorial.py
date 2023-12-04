import pytest
import pygame
from pygame.locals import KEYDOWN, K_c
from unittest.mock import patch, Mock
import sys
sys.path.append('src')
from tetris import TetrisGame

@pytest.fixture
def tetris_game():
    pygame.init()
    size = (400, 500)
    start_x = 100
    start_y = 60
    square_size = 20
    height = 20
    width = 10
    screen = pygame.display.set_mode(size)
    game = TetrisGame(screen, start_x, start_y, square_size, height, width)
    yield game
    pygame.quit()

def test_show_instructions(tetris_game):
    tetris_game.show_instructions()

def test_show_instructions_advance_with_c_key(tetris_game):
    with patch("pygame.event.get") as mock_get_event:
        mock_get_event.return_value = [pygame.event.Event(KEYDOWN, {"key": K_c})]

        tetris_game.show_instructions()