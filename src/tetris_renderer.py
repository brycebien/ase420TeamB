import pygame
import sys
sys.path.append('src')
from theme_selector import ThemeSelector
from colors import BasicColors
from figures import Figures

class TetrisRenderer:

    def __init__(self, screen, start_x, start_y, square_size, board_height, board_width):
        self.screen = screen
        self.start_x = start_x
        self.start_y = start_y
        self.square_size = square_size
        self.board_height = board_height
        self.board_width = board_width
        self.theme_manager = ThemeSelector.getInstance()

    def init_board(self, board):
        board.field = [[0] * board.width for i in range(board.height)]

    def draw_board(self, board):
        self.screen.fill(BasicColors.WHITE.value)
        for i in range(board.height):
            for j in range(board.width):
                pygame.draw.rect(self.screen, BasicColors.BLACK.value, [self.start_x + self.square_size * j, self.start_y + self.square_size * i, self.square_size, self.square_size], 1)
                if board.field[i][j] > 0:
                    pygame.draw.rect(self.screen, self.theme_manager.color_theme[board.field[i][j]], [self.start_x + self.square_size * j + 1, self.start_y + self.square_size * i + 1, self.square_size - 2, self.square_size - 1])

    def draw_figure(self, tetromino):
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in Figures[tetromino.type][tetromino.rotation]:
                    pygame.draw.rect(self.screen, self.theme_manager.color_theme[tetromino.color],
                                     [self.start_x + self.square_size * (j + tetromino.shift_x) + 1,
                                      self.start_y + self.square_size * (i + tetromino.shift_y) + 1,
                                      self.square_size - 2, self.square_size - 2])

    def draw_next(self, tetromino):
        figure = Figures[tetromino][0]
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in Figures[tetromino][0]:
                    pygame.draw.rect(self.screen, BasicColors.BLACK.value,
                                     [self.start_x + self.square_size * (j + 10.5) + 1,
                                      self.start_y + self.square_size * (i - 1) + 1,
                                      self.square_size - 2, self.square_size - 2])