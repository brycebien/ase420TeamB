import pygame

pygame.init()

class SoundPlayer:
    def playBackgroundMusic(self):
        pygame.mixer.music.load('assets/sound/2010-Toyota-Corolla.wav')
        pygame.mixer.music.play(-1)

    def playRotateSound(self):
        rotate_sound = pygame.mixer.Sound('assets/sound/rotate.wav')
        pygame.mixer.Sound.play(rotate_sound)

    def playTetrominoPlacedSound(self):
        tetromino_placed_sound = pygame.mixer.Sound('assets/sound/tetromino_placed.wav')
        pygame.mixer.Sound.play(tetromino_placed_sound)

    def playLinebreakSound(self):
        linebreak_sound = pygame.mixer.Sound('assets/sound/linebreak.wav')
        pygame.mixer.Sound.play(linebreak_sound)

    def playGameOverSound(self):
        game_over_sound = pygame.mixer.Sound('assets/sound/gameover.wav')
        pygame.mixer.Sound.play(game_over_sound)