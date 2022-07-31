class Node:
    def __init__(self, x:int, y:int, status:int) -> None:
        self.x = x
        self.y = y
        self.status = status
        self.g = 0
        self.h = 0
        self.f = 0
        self.predecessor = None
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y}) - {self.status}"

    def __lt__(self, other):
        return self.f < other.f


