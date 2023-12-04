import pygame
import sys
sys.path.append('src')
from tetris import TetrisGame

if __name__ == "__main__":
    pygame.init()
    size = (400, 500)
    start_x = 100
    start_y = 60
    square_size = 20
    height = 20
    width = 10
    screen = pygame.display.set_mode(size)
    game = TetrisGame(screen, start_x, start_y, square_size, height, width)
    game.show_instructions()
    game.showThemePicker()
    game.run()