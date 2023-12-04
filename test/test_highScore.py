import pytest
import sys
sys.path.append('src')
from high_score import HighScore

@pytest.fixture
def test_high_score_initialization():
    highscore_instance = HighScore()
    assert highscore_instance.score == 0
    assert highscore_instance.high_score == 0

def test_highscore_update_score():
    highscore_instance = HighScore()
    highscore_instance.update_score(10)
    assert highscore_instance.score == 10
    assert highscore_instance.high_score == 10

def test_highscore_write_to_file():
    highscore_instance = HighScore()
    highscore_instance.update_score(25)
    assert highscore_instance.high_score == 25

    
    highscore_instance.score = 0
    highscore_instance.high_score = -1
    highscore_instance.update_score(0)