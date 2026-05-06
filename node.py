import heapq

class Node:
    def __init__(self):
        self.paths: list[tuple[int, Node]] = []
        heapq.heapify(self.paths)

    def add_path(self, next_n: 'Node', towards_time: int = 10, backwards_time: int = 10):
        heapq.heappush(self.paths, (towards_time, next_n))
        heapq.heappush(next_n.paths, (backwards_time, self))