import pytest
from themes import color_themes
from unittest import TestCase
import sys
sys.path.append('src')
from theme_selector import ThemeSelector
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