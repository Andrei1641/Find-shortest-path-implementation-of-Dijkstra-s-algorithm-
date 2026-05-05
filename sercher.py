from node import Node
import heapq


class Searcher:
    def __init__(self, distances: list[list[Node | float]]):
        self.distances = distances
        heapq.heapify(self.distances)
        self.__processed_points = []
        self.path_to_point = {}


    #search the shortest path to unprocessed node
    def search_smallest_path(self) -> list[float | Node] | None:
        for distance in self.distances:
            if distance[1] not in self.__processed_points:
                return distance
        return None


# взять предыдущий родитель по пути и отнять от длины пути к исследуемой точки значение родителя добавить новый путь сравнить со старым значением, если менье - изменить родителя
#     def set_new_distances(self, smolest_dist: list[float | Node]):
#         node: Node = smolest_dist[1]
#         for path in node.paths:
#             if path[0] + self.distances[path[1]]