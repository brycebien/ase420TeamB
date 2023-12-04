import pytest
from unittest.mock import Mock
import sys
sys.path.append('src')
from locked_color import LockedColor

def test_locked_color_initialization():
    locked_color_instance = LockedColor()
    assert locked_color_instance.lockedColor == 7

def test_change_color():
    locked_color_instance = LockedColor()
    figure_mock = Mock()
    locked_color_instance.changeColor(figure_mock)
    assert figure_mock.color == locked_color_instance.lockedColor

def test_set_locked_color():
    locked_color_instance = LockedColor()
    locked_color_instance.setLockedColor(10)
    assert locked_color_instance.lockedColor == 10