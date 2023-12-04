import random
import sys
sys.path.append('src')
from locked_color import LockedColor
from next_shape import NextShape
from figures import Figures
from theme_selector import ThemeSelector



class Tetromino:
    def __init__(self):
        self.shift_x = 0
        self.shift_y = 0
        self.rotation = 0
        self.type = 0
        self.color = 0
        self.colorManager = LockedColor()
        self.shapeManager = NextShape()

    def get_rotation(self):
        return Figures[self.type][self.rotation % len(Figures[self.type])]

    def make_figure(self, x, y):
        self.shift_x = x
        self.shift_y = y
        self.type = self.shapeManager.determineNext()
        self.rotation = 0
        self.color = random.randint(1, len(ThemeSelector.getInstance().color_theme) - 2)

    def intersects(self, board):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.get_rotation():
                    if (i + self.shift_y >= board.height or
                        j + self.shift_x >= board.width or
                        j + self.shift_x < 0 or
                        self.shift_y < 0 or
                        board.field[i + self.shift_y][j + self.shift_x] > 0):
                        return True
        return False