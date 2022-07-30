from pyclbr import Function
from node import Node
from status import *
import math

NUM_BLOCKS_X = 50
NUM_BLOCKS_Y = 50

class Board:
    def __init__(self, heuristic: Function) -> None:
        self.heuristic = heuristic
        self.init_board()
    
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

    def distance(self, start: Node, target: Node) -> int:
        return abs(target.x - start.x) + abs(target.y - start.y)

    def set_target(self, row: int, col: int) -> None:
        if not self.target:
            self.board[row][col].status = TARGET
            self.target = self.board[row][col]

        elif self.board[row][col].status == TARGET and self.target:
            self.board[row][col].status = NOT_VISITED
            self.target = None

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
    
    def caluclate_heuristics(self) -> None:
        for row in self.board:
            for node in row:
                if node == self.target:
                    node.h = 0
                    node.g = math.inf
                elif node == self.start:
                    node.h = self.heuristic(node, self.target)
                    node.g = 0
                elif node.status != OBSTACLE:
                    node.h = self.heuristic(node, self.target)
                    node.g = math.inf
                node.f = node.h + node.g

    def get_neighbors(self, node):
        neighbors = []
        if node.x - 1 >= 0:
            neighbor = self.board[node.x - 1][node.y]
            if neighbor.status != OBSTACLE:
                neighbors.append(neighbor)

        if node.x + 1 < NUM_BLOCKS_X:
            neighbor = self.board[node.x + 1][node.y]
            if neighbor.status != OBSTACLE:
                neighbors.append(neighbor)

        if node.y - 1 >= 0:
            neighbor = self.board[node.x][node.y - 1]
            if neighbor.status != OBSTACLE:
                neighbors.append(neighbor)

        if node.y + 1 < NUM_BLOCKS_Y:
            neighbor = self.board[node.x][node.y + 1]
            if neighbor.status != OBSTACLE:
                neighbors.append(neighbor)

        return neighbors

    def expand(self, update_callback=None):

        # Initialize open list with start node and closed list with empty set.
        open_list = {self.start}
        closed_list = set()

        # Perform algorithm while we are having nodes in the open list.
        while open_list:
            #if update_callback:
            #    update_callback()
            if update_callback:
               update_callback()

            # Find node with minimum f cost.
            node = min(open_list, key=lambda x: x.f)
            
            # Minimum node is target node --> Path found
            if node == self.target:
                # Reconstruct path
                node.status = TARGET
                predecessor = node.predecessor
                predecessor.status = PATH
                while predecessor.predecessor:
                    predecessor = predecessor.predecessor
                    predecessor.status = PATH if predecessor.status != START and predecessor.status != TARGET else predecessor.status
                return

            # Expand
            neighbors = self.get_neighbors(node)
            # Update costs for neighbors
            for neighbor in neighbors:
                if neighbor not in closed_list:
                    neighbor.g = node.g + self.distance(node, neighbor)
                    cost = neighbor.g + neighbor.h
                    if cost < neighbor.f:
                        neighbor.f = cost
                        neighbor.predecessor = node
                    neighbor.status = OPEN
                    open_list.add(neighbor)
            
            # Remove current node from open list, add to closed list.
            open_list.remove(node)
            closed_list.add(node)
            node.status = CLOSED if node.status != START else START


        

            
                



        
