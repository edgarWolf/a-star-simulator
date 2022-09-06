from pyclbr import Function
from algorithm import Algorithm
from node import Node
from status import *
import math

NUM_BLOCKS_X = 50
NUM_BLOCKS_Y = 50

class Board:
    def __init__(self, heuristic: Function) -> None:
        self.heuristic = heuristic
        self.init_board()
        self.algorithm = Algorithm()
    
    def init_board(self) -> None:
        self.board = [ [Node(i, j, NOT_VISITED) for j in range(NUM_BLOCKS_X)] for i in range(NUM_BLOCKS_Y) ]
        self.target = None
        self.start = None
    
    def reset(self) -> None:
        self.init_board()

    def reset_found_path(self) -> None:
        for row in self.board:
            for node in row:
                if node.status == CLOSED or node.status == OPEN or node.status == PATH:
                    node.status = NOT_VISITED

    def set_target(self, row: int, col: int) -> None:
        if not self.target:
            self.board[row][col].status = TARGET
            self.target = self.board[row][col]

        elif self.board[row][col].status == TARGET and self.target:
            self.board[row][col].status = NOT_VISITED
            self.target = None
        self.algorithm.set_target(self.target)

    def set_obstacle(self, row: int, col: int) -> None:
        node = self.board[row][col]
        if node.status == NOT_VISITED:
            node.status = OBSTACLE
        elif node.status == OBSTACLE:
            node.status = NOT_VISITED

    def set_start(self, row: int, col: int) -> None:
        if not self.start:
            self.board[row][col].status = START
            self.start = self.board[row][col]

        elif self.board[row][col].status == START and self.start:
            self.board[row][col].status = NOT_VISITED
            self.start = None
        self.algorithm.set_start(self.start)

    def get_neighbors(self, node):
        neighbors = []

        # Left
        if node.x - 1 >= 0:
            neighbor = self.board[node.x - 1][node.y]
            if neighbor.status != OBSTACLE:
                neighbors.append(neighbor)

        # Right
        if node.x + 1 < NUM_BLOCKS_X:
            neighbor = self.board[node.x + 1][node.y]
            if neighbor.status != OBSTACLE:
                neighbors.append(neighbor)

        # Upper
        if node.y - 1 >= 0:
            neighbor = self.board[node.x][node.y - 1]
            if neighbor.status != OBSTACLE:
                neighbors.append(neighbor)
        
        # Lower
        if node.y + 1 < NUM_BLOCKS_Y:
            neighbor = self.board[node.x][node.y + 1]
            if neighbor.status != OBSTACLE:
                neighbors.append(neighbor)

        # Diagonal upper left
        if node.y - 1 >= 0 and node.x - 1 >= 0:
            neighbor = self.board[node.x - 1][node.y - 1]
            neighbors.append(neighbor)
        
        # Diagonal upper right
        if node.y - 1 >= 0 and node.x + 1 < NUM_BLOCKS_X:
            neighbor = self.board[node.x + 1][node.y - 1]
            neighbors.append(neighbor)

        # Diagonal lower left
        if node.y + 1 < NUM_BLOCKS_Y and node.x - 1 >= 0:
            neighbor = self.board[node.x - 1][node.y + 1]
            neighbors.append(neighbor)

        # Diagonal lower right
        if node.y + 1 < NUM_BLOCKS_Y and node.x + 1 < NUM_BLOCKS_X:
            neighbor = self.board[node.x + 1][node.y + 1]
            neighbors.append(neighbor)



        return neighbors

    def expand(self, update_callback=None):

        self.algorithm.initialize(self)

        while not self.algorithm.is_finished():
            if update_callback:
               update_callback()
            self.algorithm.step(self)
            
        self.algorithm.reset()
                


        

            
                



        
