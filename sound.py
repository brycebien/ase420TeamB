import pygame

pygame.init()

rotate_sound = pygame.mixer.Sound('assets/sound/rotate.wav')
tetromino_placed_sound = pygame.mixer.Sound('assets/sound/tetromino_placed.wav')
linebreak_sound = pygame.mixer.Sound('assets/sound/linebreak.wav')
game_over_sound = pygame.mixer.Sound('assets/sound/gameover.wav')

def playBackgroundMusic():
    pygame.mixer.music.load('assets/sound/2010-Toyota-Corolla.wav')
    pygame.mixer.music.play(-1)

