from queue import PriorityQueue
from math_utils import pythagorean
from node import Node
from status import *
import math


class Algorithm:
    def __init__(self) -> None:
        self.reset()

    def distance(self, start: Node, target: Node) -> int:
        return abs(target.x - start.x) + abs(target.y - start.y)
    
    def equal_distance(self) -> int:
        # Consider equal distance for each neighbor.
        return 1
    
    def set_start(self, start) -> None:
        self.start = start

    def set_target(self, target) -> None:
        self.target = target

    def heuristic(self, a: Node, b: Node) -> int:
        return pythagorean((b.x - a.x), (b.y - a.y))

    
    def caluclate_heuristics(self, board) -> None:
        for row in board.board:
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
    
    def initialize(self, board) -> None:
        # Initialize open list with start node and closed list with empty set.
        if self.start:
            self.open.put(self.start)
            self.caluclate_heuristics(board)
        else:
            self.open.get()
            self.start = None
    

    def step(self, board) -> None:
        if not self.open.empty():
            # Get node with minimum f cost.
            node = self.open.get()
            
            # We have found the target node as the next node with minimum f cost.
            if node == self.target:
                node.status = TARGET
                predecessor = node.predecessor
                predecessor.status = PATH
                while predecessor.predecessor:
                    predecessor = predecessor.predecessor
                    predecessor.status = PATH if predecessor.status != START and predecessor.status != TARGET else predecessor.status
                # Since a path is found, the algorithm terminates.
                self.finished = True
                return

            # Expand neighbors.
            neighbors = board.get_neighbors(node)
            for neighbor in neighbors:
                if neighbor not in self.closed:

                    # You may call here a other distance method.
                    g = node.g + self.equal_distance()
                    
                    # We have found one neighbor with less cost.
                    if g < neighbor.g:
                        f = g + neighbor.h
                        neighbor.g = g
                        neighbor.f = f
                        neighbor.predecessor = node
                        neighbor.status = OPEN
                        if neighbor not in self.open.queue:
                            self.open.put(neighbor)
            
            # Add to closed list.
            self.closed.add(node)
            node.status = CLOSED if node.status != START else START

            # We are finished when the open list is empty.
            self.finished = self.open.empty()
    
    def is_finished(self) -> bool:
        return self.finished
        
    def reset(self) -> bool:
        self.start = None
        self.target = None
        
        # Use priority queue for logarithmic time complexity for access.
        self.open = PriorityQueue()
        self.closed = set()
        self.finished = False