import os
import pygame
import random
import sound
import textwrap
from theme_selector import ThemeSelector
from colors import BasicColors
from tetris_renderer import TetrisRenderer
from figures import Figures
from themes import color_themes

class LockedColor:
    def __init__(self):
        self.lockedColor=7
    def changeColor(self, figure):
        figure.color = self.lockedColor
    def setLockedColor(self, color):
        self.lockedColor = color

class DetermineNextShape:
    MAX_FIGURE_INDEX = len(Figures) - 1
    def __init__(self):
        self.next_shape = None
        self.current_shape = None
        self.has_been_set = False
    
    def determineNext(self):
        if not self.has_been_set:
            self.current_shape = random.randint(0, self.MAX_FIGURE_INDEX)
            self.next_shape = random.randint(0, self.MAX_FIGURE_INDEX)
            self.has_been_set = True
            return self.current_shape
        else:
            self.current_shape = self.next_shape
            self.next_shape = random.randint(0, self.MAX_FIGURE_INDEX)
            return self.current_shape

class Tetromino:
    def __init__(self):
        self.shift_x = 0
        self.shift_y = 0
        self.rotation = 0
        self.type = 0
        self.color = 0
        self.colorManager = LockedColor()
        self.shapeManager = DetermineNextShape()

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
                rows_to_remove.insert(0, i)

        for row in rows_to_remove:
            del self.field[row]
            self.field.insert(0, [0] * self.width)
            lines_cleared += 1
        self.line_manager.notify(lines_cleared)
        return lines_cleared
    

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
        if os.path.exists('highscore.txt'):
            with open ('highscore.txt', 'r') as file:
                self.high_score = int(file.read())
        else:
            with open('highscore.txt', 'w') as file:
                file.write('0')
                self.high_score = 0

    def update_score(self, amnt):
        self.score += amnt
        if self.score > self.high_score:
            self.high_score = self.score
            with open ('highscore.txt', 'w') as file:
                file.write(str(self.high_score))
    
class TetrisGame:
    def __init__(self, screen, start_x, start_y, square_size, height, width):
        self.screen = screen
        self.start_x = start_x
        self.start_y = start_y
        self.square_size = square_size
        self.board = Board(height, width)
        self.tetromino = Tetromino()
        self.score = 0
        self.state = "start"
        self.renderer = TetrisRenderer(screen, start_x, start_y, square_size, height, width)
        self.scoreManager = HighScore()
        self.board.line_manager.subscribe(self)
        self.font1 = pygame.font.SysFont('trebuchetms', 65, True, False)

    def show_instructions(self):
        self.screen.fill(BasicColors.WHITE.value)
        pygame.display.set_caption("Instructions")

        instructions = ["Use the left and right arrow keys to move the tetromino.", "Press the up arrow key to rotate the tetromino.", "Press the spacebar to drop the tetromino.", "Score points by clearing lines by filling in all the squares in a row.", "Points are based on how many lines are cleared at a time", "Press the \"Q\" key to quit the game."]

        font1 = pygame.font.SysFont('trebuchetms', 65, True, False)
        text1 = font1.render("Tetris", True, (0, 255, 0))
        self.screen.blit(text1, [10, 0])
        font = pygame.font.SysFont('trebuchetms', 18, True, False)

        text_y_coord = 80

        for text in instructions:
            wrapped_text = textwrap.wrap(text, width=40)

            for line in wrapped_text:
                display_text = font.render(line, True, BasicColors.BLACK.value)
                self.screen.blit(display_text, [20, text_y_coord])
                text_y_coord += 35

        continue_text = font.render("Press \"C\" to continue.", True, BasicColors.BLACK.value)
        self.screen.blit(continue_text, [20, text_y_coord + 60])

        terminator = True
        while terminator:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        terminator = False
                        break
            pygame.display.flip()

    def showThemePicker(self):
        BUTTON_WIDTH, BUTTON_HEIGHT = 150, 75
        BUTTON_MARGIN = 15
        BUTTON_COLOR = (0, 128, 255)
        BUTTON_TEXT_COLOR = (255, 255, 255)
        THEME_BUTTONS = ["Classic", "Forest", "Pastel", "Vibrant"]
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        CLASSIC = color_themes[0]
        FOREST = color_themes[1]
        PASTEL = color_themes[2]
        VIBRANT = color_themes[3]

        pygame.display.set_caption("Theme Selection")
        font = pygame.font.SysFont('trebuchetms', 36, True, False)

        def draw_color_previews(theme):
            for i in range(6):
                pygame.draw.rect(
                    screen,
                    theme[i],
                    (
                        WIDTH // 2 - 3 * BUTTON_WIDTH // 4 + i * (BUTTON_WIDTH // 6),
                        HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_MARGIN,
                        BUTTON_WIDTH // 6,
                        BUTTON_HEIGHT,
                    ),
                )

        theme_buttons = []
        for i, theme in enumerate(THEME_BUTTONS):
            button_rect = pygame.Rect(
                WIDTH // 2 - BUTTON_WIDTH // 2,
                i * (BUTTON_HEIGHT + BUTTON_MARGIN) + BUTTON_MARGIN,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
            )
            theme_buttons.append((theme, button_rect))

        terminator = True
        while terminator:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for theme, button_rect in theme_buttons:
                        if button_rect.collidepoint(x, y):
                            ThemeSelector.getInstance().set_theme(theme)
                            terminator = False

            screen.fill((255, 255, 255))
            for theme, button_rect in theme_buttons:
                pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
                button_text = font.render(theme, True, BUTTON_TEXT_COLOR)
                text_rect = button_text.get_rect(center=button_rect.center)
                screen.blit(button_text, text_rect)

            x, y = pygame.mouse.get_pos()
            for theme, button_rect in theme_buttons:
                if button_rect.collidepoint(x, y):
                    if theme == "Classic":
                        draw_color_previews(CLASSIC)
                    elif theme == "Forest":
                        draw_color_previews(FOREST)
                    elif theme == "Vibrant":
                        draw_color_previews(VIBRANT)
                    elif theme == "Pastel":
                        draw_color_previews(PASTEL)

            pygame.display.flip()
            
            
    def update(self, lines):
        self.scoreManager.update_score(lines)
        
    def run(self):
    
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
            self.renderer.draw_next(self.tetromino.shapeManager.next_shape)

            font = pygame.font.SysFont('Calibri', 25, True, False)
            next_piece = font.render("Next Piece:", True, BasicColors.BLACK.value)
            score = font.render("Score: " + str(self.scoreManager.score), True, BasicColors.BLACK.value)
            high_score = font.render("High Score: " + str(self.scoreManager.high_score), True, BasicColors.BLACK.value)
            self.screen.blit(next_piece, [275,3])
            self.screen.blit(score, [0, 0])
            self.screen.blit(high_score, [0, 25])

            if self.state == "gameover":
                text_game_over = self.font1.render("Game Over", True, (255, 125, 0))
                text_game_over1 = self.font1.render("Enter q to Quit", True, (255, 215, 0))
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