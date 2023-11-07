import pygame
import random

# Define some colors
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


class Tetris:
    def __init__(self, height, width):
        self.size = (400, 500)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.fps = 25
        self.game = self.initialize_game(height, width)

    def initialize_game(self, height, width):
        game = GameBoard(height, width)
        game.new_figure()
        return game

    def run(self):
        done = False
        counter = 0
        pressing_down = False

        while not done:
            if self.game.figure is None:
                self.game.new_figure()
            counter += 1
            if counter > 100000:
                counter = 0

            if counter % (self.fps // self.game.level // 2) == 0 or pressing_down:
                if self.game.state == "start":
                    self.game.go_down()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.game.rotate()
                    if event.key == pygame.K_DOWN:
                        pressing_down = True
                    if event.key == pygame.K_LEFT:
                        self.game.go_side(-1)
                    if event.key == pygame.K_RIGHT:
                        self.game.go_side(1)
                    if event.key == pygame.K_SPACE:
                        self.game.go_space()
                    if event.key == pygame.K_ESCAPE:
                        self.game = self.initialize_game(20, 10)

                if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    pressing_down = False

            self.draw_board()
            self.draw_figure()

            font = pygame.font.SysFont('Calibri', 25, True, False)
            font1 = pygame.font.SysFont('Calibri', 65, True, False)
            text = font.render("Score: " + str(self.game.score), True, BLACK)
            text_game_over = font1.render("Game Over", True, (255, 125, 0))
            text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

            self.screen.blit(text, [0, 0])
            if self.game.state == "gameover":
                self.screen.blit(text_game_over, [20, 200])
                self.screen.blit(text_game_over1, [25, 265])

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()

    def draw_board(self):
        self.screen.fill(WHITE)

        for i in range(self.game.height):
            for j in range(self.game.width):
                pygame.draw.rect(self.screen, GRAY, [self.game.x + self.game.zoom * j, self.game.y + self.game.zoom * i, self.game.zoom, self.game.zoom], 1)
                if self.game.field[i][j] > 0:
                    pygame.draw.rect(self.screen, colors[self.game.field[i][j]],
                                     [self.game.x + self.game.zoom * j + 1, self.game.y + self.game.zoom * i + 1, self.game.zoom - 2, self.game.zoom - 1])

    def draw_figure(self):
        if self.game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.game.figure.image():
                        pygame.draw.rect(self.screen, colors[self.game.figure.color],
                                         [self.game.x + self.game.zoom * (j + self.game.figure.x) + 1,
                                          self.game.y + self.game.zoom * (i + self.game.figure.y) + 1,
                                          self.game.zoom - 2, self.game.zoom - 2])

class LockedColor:
    def __init__(self):
        self.lockedColor=7
    def changeColor(self, figure):
        figure.color = self.lockedColor
    def setLockedColor(self, color):
        self.lockedColor = color

class GameBoard():
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure = None
        self.colorManager = LockedColor()
        self.height = height
        self.width = width
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        self.colorManager.changeColor(self.figure)
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

class Figure:
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 2)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

if __name__ == "__main__":
    pygame.init()
    game = Tetris(20, 10)
    game.run()

