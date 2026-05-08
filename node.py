import heapq

class Node:
    def __init__(self):
        self.paths: list[tuple[int, int, Node]] = []
        heapq.heapify(self.paths)

    def add_path(self, next_n: 'Node', counter: int, towards_time: int = 10, backwards_time: int = 10):
        heapq.heappush(self.paths, (towards_time, counter,next_n))
        counter += 1
        heapq.heappush(next_n.paths, (backwards_time, counter,self))