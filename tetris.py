import os
import pygame
import random
import sound

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
    GRAY
]


Figures = (
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [2, 6, 5, 9]],
    [[6, 7, 9, 10], [1, 5, 6, 10]],
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    [[1, 2, 5, 6]]
)

class LockedColor:
    def __init__(self):
        self.lockedColor=7
    def changeColor(self, figure):
        figure.color = self.lockedColor
    def setLockedColor(self, color):
        self.lockedColor = color

class Tetromino:
    def __init__(self):
        self.shift_x = 0
        self.shift_y = 0
        self.rotation = 0
        self.type = 0
        self.color = 0
        self.colorManager = LockedColor()

    def get_rotation(self):
        return Figures[self.type][self.rotation % len(Figures[self.type])]

    def make_figure(self, x, y):
        self.shift_x = x
        self.shift_y = y
        self.type = random.randint(0, len(Figures) - 1)
        self.rotation = 0
        self.color = random.randint(1, len(colors) - 2)

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

class EventManager:
    def __init__(self):
        self._listeners = []
    
    def subscribe(self, listener):
        self._listeners.append(listener)

    def notify(self, lines):
        for listener in self._listeners:
            listener.update(lines)

class Board:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = [[0] * width for _ in range(height)]
        self.line_manager=EventManager()

    def break_lines(self):
        lines_cleared = 0
        rows_to_remove = []

        for i in range(self.height - 1, -1, -1):
            if all(self.field[i]):
                rows_to_remove.append(i)

        for row in rows_to_remove:
            del self.field[row]
            self.field.insert(0, [0] * self.width)
            lines_cleared += 1
        self.line_manager.notify(lines_cleared)
        return lines_cleared
class TetrisRenderer:
    def __init__(self, screen, start_x, start_y, square_size, board_height, board_width):
        self.screen = screen
        self.start_x = start_x
        self.start_y = start_y
        self.square_size = square_size
        self.board_height = board_height
        self.board_width = board_width

    def init_board(self, board):
        board.field = [[0] * board.width for i in range(board.height)]

    def draw_board(self, board):
        self.screen.fill(WHITE)
        for i in range(board.height):
            for j in range(board.width):
                pygame.draw.rect(self.screen, GRAY, [self.start_x + self.square_size * j, self.start_y + self.square_size * i, self.square_size, self.square_size], 1)
                if board.field[i][j] > 0:
                    pygame.draw.rect(self.screen, colors[board.field[i][j]], [self.start_x + self.square_size * j + 1, self.start_y + self.square_size * i + 1, self.square_size - 2, self.square_size - 1])

    def draw_figure(self, tetromino):
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in Figures[tetromino.type][tetromino.rotation]:
                    pygame.draw.rect(self.screen, colors[tetromino.color],
                                     [self.start_x + self.square_size * (j + tetromino.shift_x) + 1,
                                      self.start_y + self.square_size * (i + tetromino.shift_y) + 1,
                                      self.square_size - 2, self.square_size - 2])

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
        old_rotation = tetromino.rotation
        tetromino.rotation = (tetromino.rotation + 1) % len(Figures[tetromino.type])
        if tetromino.intersects(board):
            tetromino.rotation = old_rotation
        pygame.mixer.Sound.play(sound.rotate_sound)

    @staticmethod
    def freezeTetronimo(tetromino, board):
        tetromino.colorManager.changeColor(tetromino)
        for i in range(4):
            for j in range(4):
                if i * 4 + j in tetromino.get_rotation():
                    board.field[i + tetromino.shift_y][j + tetromino.shift_x] = tetromino.color
        tetromino.make_figure(3, 0)
        pygame.mixer.Sound.play(sound.tetromino_placed_sound)

        if board.break_lines() > 0:
            pygame.mixer.Sound.play(sound.linebreak_sound)

class HighScore:
    def __init__(self):
        self.score = 0
        #TODO: write hs to file when it is > 0/>old hs -- grab hs from file
        if os.path.exists('highscore.txt'):
            with open ('highscore.txt', 'r') as file:
                self.high_score = int(file.read())
        else:
            with open('highscore.txt', 'w') as file:
                file.write('0')
                self.high_score = 0


    def _check_highscore(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open ('highscore.txt', 'w') as file:
                file.write(str(self.high_score))

    def update_score(self, amnt):
        self.score += amnt
        self._check_highscore()
    
class TetrisGame:
    def __init__(self, screen, start_x, start_y, square_size, height, width):
        self.screen = screen
        self.start_x = start_x
        self.start_y = start_y
        self.square_size = square_size
        self.board = Board(height, width)
        self.tetromino = Tetromino()
        self.state = "start"
        self.renderer = TetrisRenderer(screen, start_x, start_y, square_size, height, width)
        self.scoreManager = HighScore()
        self.board.line_manager.subscribe(self)

    def update(self, lines):
        self.scoreManager.update_score(lines)
        
    def run(self):
        pygame.init()
        pygame.display.set_caption("Tetris")
        clock = pygame.time.Clock()

        fps = 25
        counter = 0
        pressing_down = False
        
        self.renderer.init_board(self.board)
        self.tetromino.make_figure(3, 0)

        sound.playBackgroundMusic()

        done = False
        while not done:
            if self.tetromino.intersects(self.board):
                self.state = "gameover"

            counter += 1
            if counter > 100000:
                counter = 0

            if counter % (fps // 2) == 0 or pressing_down:
                if self.state == "start":
                    Move.go_down(self.tetromino, self.board)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        Move.rotate(self.tetromino, self.board)
                    if event.key == pygame.K_LEFT:
                        Move.go_side(self.tetromino, self.board, -1)
                    if event.key == pygame.K_RIGHT:
                        Move.go_side(self.tetromino, self.board, 1)
                    if event.key == pygame.K_SPACE:
                        Move.go_space(self.tetromino, self.board)
                    if event.key == pygame.K_q:
                        if self.state == "gameover":
                            done = True
                    if event.key == pygame.K_DOWN:
                        pressing_down = True

                if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    pressing_down = False
        
            self.renderer.draw_board(self.board)
            self.renderer.draw_figure(self.tetromino)

            font = pygame.font.SysFont('Calibri', 25, True, False)
            score = font.render("Score: " + str(self.scoreManager.score), True, BLACK)
            high_score = font.render("High Score: " + str(self.scoreManager.high_score), True, BLACK)
            self.screen.blit(score, [0, 0])
            self.screen.blit(high_score, [0, 25])

            if self.state == "gameover":
                font1 = pygame.font.SysFont('Calibri', 65, True, False)
                text_game_over = font1.render("Game Over", True, (255, 125, 0))
                text_game_over1 = font1.render("Enter q to Quit", True, (255, 215, 0))
                self.screen.blit(text_game_over, [20, 200])
                self.screen.blit(text_game_over1, [25, 265])
                pygame.mixer.music.stop()
                break

            pygame.display.flip()
            clock.tick(fps)


        pygame.mixer.Sound.play(sound.game_over_sound)

        while(pygame.mixer.get_busy()):
            pygame.time.wait(1)

        pygame.quit()

if __name__ == "__main__":
    size = (400, 500)
    start_x = 100
    start_y = 60
    square_size = 20
    height = 20
    width = 10
    screen = pygame.display.set_mode(size)
    game = TetrisGame(screen, start_x, start_y, square_size, height, width)
    game.run()