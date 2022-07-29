from board import Board
from gui import Gui
from node import Node
from status import *
from math_utils import pythagorean
from node import Node


def heuristic(a: Node, b: Node) -> int:
    return pythagorean((b.x - a.x), (b.y - a.y))

def distance(a: Node, b: Node)-> int:
    return b.x - a.x + b.y - a.y


def main():
    board = Board(heuristic=heuristic)
    gui = Gui(board)
    while True:
        gui.main_loop()

if __name__ == "__main__":
    main()