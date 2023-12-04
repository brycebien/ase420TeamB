import pygame
import textwrap
import sys
sys.path.append('src')
from sound import SoundPlayer
from theme_selector import ThemeSelector
from colors import BasicColors
from tetris_renderer import TetrisRenderer
from themes import color_themes
from board import Board
from tetromino import Tetromino
from high_score import HighScore
from move import Move

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
        self.soundManager = SoundPlayer()
        self.board.line_manager.subscribe(self)
        self.font1 = pygame.font.SysFont('trebuchetms', 65, True, False)

    def show_instructions(self):
        self.screen.fill(BasicColors.WHITE.value)
        pygame.display.set_caption("Instructions")

        instructions = ["Use the left and right arrow keys to move the tetromino.", "Press the up arrow key to rotate the tetromino.", "Press the spacebar to drop the tetromino.", "Score points by clearing lines by filling in all the squares in a row.", "Points are based on how many lines are cleared at a time", "Press the \"Q\" key to quit the game.", "Press \"C\" to continue."]

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
                    self.screen,
                    theme[i],
                    (
                        WIDTH // 2 - 2 * BUTTON_WIDTH // 4 + i * (BUTTON_WIDTH // 6),
                        len(THEME_BUTTONS) * (BUTTON_HEIGHT + BUTTON_MARGIN) + BUTTON_MARGIN,
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

            self.screen.fill((255, 255, 255))
            for theme, button_rect in theme_buttons:
                pygame.draw.rect(self.screen, BUTTON_COLOR, button_rect)
                button_text = font.render(theme, True, BUTTON_TEXT_COLOR)
                text_rect = button_text.get_rect(center=button_rect.center)
                self.screen.blit(button_text, text_rect)

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

        self.soundManager.playBackgroundMusic()

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
                pygame.mixer.music.stop()
                break

            pygame.display.flip()
            clock.tick(fps)

        self.soundManager.playGameOverSound()
        
        while(pygame.mixer.get_busy()):
            pygame.time.wait(1)

        pygame.quit()