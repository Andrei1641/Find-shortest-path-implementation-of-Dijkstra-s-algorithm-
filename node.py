class Node:
    def __init__(self):
        self.__path: dict[Node, int] = {}


    def add_path(self, next_n: 'Node'):
        self.__path.update({next_n : 10})


    def set_time(self, next_n: 'Node', time: int):
        self.__path[next_n] = time