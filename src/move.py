import sys
sys.path.append('src')
from sound import SoundPlayer
from figures import Figures

class Move:
    @staticmethod
    def go_space(tetromino, board):
        while not tetromino.intersects(board):
            tetromino.shift_y += 1
        tetromino.shift_y -= 1
        Move.freezeTetronimo(tetromino, board)

    @staticmethod
    def go_down(tetromino, board):
        tetromino.shift_y += 1
        if tetromino.intersects(board):
            tetromino.shift_y -= 1
            Move.freezeTetronimo(tetromino, board)

    @staticmethod
    def go_side(tetromino, board, dx):
        old_x = tetromino.shift_x
        tetromino.shift_x += dx
        if tetromino.intersects(board):
            tetromino.shift_x = old_x

    @staticmethod
    def rotate(tetromino, board):
        soundManager = SoundPlayer()
        old_rotation = tetromino.rotation
        tetromino.rotation = (tetromino.rotation + 1) % len(Figures[tetromino.type])
        if tetromino.intersects(board):
            tetromino.rotation = old_rotation
        soundManager.playRotateSound()

    @staticmethod
    def freezeTetronimo(tetromino, board):
        soundManager = SoundPlayer()
        tetromino.colorManager.changeColor(tetromino)
        for i in range(4):
            for j in range(4):
                if i * 4 + j in tetromino.get_rotation():
                    board.field[i + tetromino.shift_y][j + tetromino.shift_x] = tetromino.color
        tetromino.make_figure(3, 0)
        soundManager.playTetrominoPlacedSound()

        if board.break_lines() > 0:
            soundManager.playLinebreakSound()
            pass
