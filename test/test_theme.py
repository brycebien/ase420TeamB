import pytest
import pygame
from themes import color_themes
import sys
sys.path.append('src')
from theme_selector import ThemeSelector
from tetris import TetrisGame
from themes import color_themes

@pytest.fixture
def theme_selector_instance():
    return ThemeSelector.getInstance()

def test_theme_selector_initialization(theme_selector_instance):
    assert theme_selector_instance.color_theme == color_themes[0]

def test_set_theme_classic(theme_selector_instance):
    theme_selector_instance.set_theme("Classic")
    assert theme_selector_instance.color_theme == color_themes[0]

def test_set_theme_forest(theme_selector_instance):
    theme_selector_instance.set_theme("Forest")
    assert theme_selector_instance.color_theme == color_themes[1]

def test_set_theme_pastel(theme_selector_instance):
    theme_selector_instance.set_theme("Pastel")
    assert theme_selector_instance.color_theme == color_themes[2]

def test_set_theme_vibrant(theme_selector_instance):
    theme_selector_instance.set_theme("Vibrant")
    assert theme_selector_instance.color_theme == color_themes[3]

def testShowThemePicker():
    pygame.init()
    size = (400, 500)
    start_x = 100
    start_y = 60
    square_size = 20
    height = 20
    width = 10
    screen = pygame.display.set_mode(size)
    game = TetrisGame(screen, start_x, start_y, square_size, height, width)
    game.showThemePicker()