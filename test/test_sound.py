import pytest
import pygame
import sys
sys.path.append('src')
from sound import SoundPlayer


@pytest.fixture
def sound_player():
    yield SoundPlayer()

def testPlayRotateSound(sound_player):
    pygame.mixer.init()
    sound_player.playRotateSound()
    pygame.time.wait(500)
    pygame.mixer.quit()

def testPlayTetrominoPlacedSound(sound_player):
    pygame.mixer.init()   
    sound_player.playTetrominoPlacedSound()
    pygame.time.wait(500)
    pygame.mixer.quit()


def testPlayLinebreakSound(sound_player):
    pygame.mixer.init()
    sound_player.playLinebreakSound()
    pygame.time.wait(500)
    pygame.mixer.quit()


def testPlayGameOverSound(sound_player):
    pygame.mixer.init()   
    sound_player.playGameOverSound()
    pygame.time.wait(500)
    pygame.mixer.quit()

def testPlayBackgroundMusic(sound_player):
    pygame.mixer.init()   
    sound_player.playBackgroundMusic()
    pygame.time.wait(1000)
    pygame.quit()
