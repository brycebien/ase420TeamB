import pytest
from unittest.mock import Mock
from unittest import TestCase
import sys
sys.path.append('src')
from locked_color import LockedColor
from next_shape import NextShape
from high_score import HighScore



class TestLockedColor(TestCase):
    def test_locked_color_initialization(self):
        locked_color_instance = LockedColor()
        assert locked_color_instance.lockedColor == 7

    def test_change_color(self):
        locked_color_instance = LockedColor()
        figure_mock = Mock()
        locked_color_instance.changeColor(figure_mock)
        assert figure_mock.color == locked_color_instance.lockedColor

    def test_set_locked_color(self):
        locked_color_instance = LockedColor()
        locked_color_instance.setLockedColor(10)
        assert locked_color_instance.lockedColor == 10

class TestNextShape(TestCase):
    def test_determine_next_shape_initialization(self):
        determine_next_instance = NextShape()
        assert determine_next_instance.next_shape == None
        assert determine_next_instance.current_shape == None
        assert determine_next_instance.has_been_set == False

    def determine_next_first_call(self):
        determine_next_instance = NextShape()
        res = determine_next_instance.determineNext()
        assert determine_next_instance.current_shape == res
        assert determine_next_instance.next_shape is not None
        assert determine_next_instance.has_been_set is True

    def test_determine_next_subsequent_calls(self):
        determine_next_instance = NextShape()
        determine_next_instance.determineNext()  # First call
        current_shape_before = determine_next_instance.current_shape
        result = determine_next_instance.determineNext()  # Subsequent call
        assert determine_next_instance.current_shape == result
        assert determine_next_instance.next_shape is not None
        assert determine_next_instance.current_shape != current_shape_before
        assert determine_next_instance.has_been_set is True

class TestHighScore(TestCase):
    def test_high_score_initialization(self):
        highscore_instance = HighScore()
        assert highscore_instance.score == 0
        assert highscore_instance.high_score == 0

    def test_highscore_update_score(self):
        highscore_instance = HighScore()
        highscore_instance.update_score(10)
        assert highscore_instance.score == 10
        assert highscore_instance.high_score == 10

    def test_highscore_write_to_file(self):
        highscore_instance = HighScore()
        highscore_instance.update_score(25)
        assert highscore_instance.high_score == 25

        #reset high score file to 0 after testing
        highscore_instance.score = 0
        highscore_instance.high_score = -1
        highscore_instance.update_score(0)

