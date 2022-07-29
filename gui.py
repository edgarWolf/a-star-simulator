import pygame
import sys
from board import NUM_BLOCKS_X, NUM_BLOCKS_Y, Board
from status import *


# UI measures
WIDTH = 800
HEIGHT = 800

BLOCKSIZE_X = WIDTH // NUM_BLOCKS_X
BLOCKSIZE_Y = HEIGHT // NUM_BLOCKS_Y

# Colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (124, 252, 0)
RED = (255, 0 , 0)
BLUE = (0,191,255)
YELLOW = (255, 255 , 0)
ORANGE = (255,165,0)

COLOR_MAPPING = {
    NOT_VISITED: WHITE,
    START: GREEN,
    TARGET: RED,
    OBSTACLE: BLACK,
    OPEN: BLUE,
    CLOSED: YELLOW,
    PATH: ORANGE
}

class Gui:
    def __init__(self, board: Board) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = board
        self.screen.fill(WHITE)#
        self.clock = pygame.time.Clock()
        self.is_running = False
        pygame.display.set_caption("A* algorithm")


    
    def _draw_grid(self):
        for i in range(0, WIDTH, BLOCKSIZE_X):
            for j in range (0, HEIGHT, BLOCKSIZE_Y):
                rect = pygame.Rect(i, j, BLOCKSIZE_X, BLOCKSIZE_Y)
                pygame.draw.rect(self.screen, BLACK, rect, 1) 
                node = self.board.board[i // BLOCKSIZE_Y][j // BLOCKSIZE_X]
                pygame.draw.rect(self.screen, COLOR_MAPPING[node.status], pygame.Rect(i + 1, j + 1, BLOCKSIZE_X - 2, BLOCKSIZE_Y - 2))


    def _redraw_grid(self):
        self._draw_grid()
        pygame.display.update()


    def main_loop(self):
        self._draw_grid()
        for event in pygame.event.get():

            # Exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse events
            if event.type == pygame.MOUSEBUTTONUP and not self.is_running:
                mouse_pos = pygame.mouse.get_pos()
                norm_mouse_pos = (mouse_pos[0] // BLOCKSIZE_Y, mouse_pos[1] // BLOCKSIZE_X)
                
                # Start setter
                if event.button == 1:
                    self.board.set_start(norm_mouse_pos[0], norm_mouse_pos[1])
                
                # Target setter
                if event.button == 3:
                    self.board.set_target(norm_mouse_pos[0], norm_mouse_pos[1])

            # Obstacles
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x and not self.is_running:
                mouse_pos = pygame.mouse.get_pos()
                norm_mouse_pos = (mouse_pos[0] // BLOCKSIZE_Y, mouse_pos[1] // BLOCKSIZE_X)
                self.board.set_obstacle(norm_mouse_pos[0], norm_mouse_pos[1])

            # Start algorithm
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.board.start and self.board.target:
                    self.is_running = True
                    self.board.caluclate_heuristics()
                    self.board.expand(update_callback=self._redraw_grid)
                    self.is_running = False
                    return

            # Reset
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.is_running = False
                self.board.reset()
        pygame.display.update()

