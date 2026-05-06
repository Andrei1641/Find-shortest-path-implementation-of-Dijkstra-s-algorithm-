from node import Node
import heapq


class Searcher:
    def __init__(self, distances_heap: list[tuple[float, Node]], distances_dict: dict[Node, float]):
        self.distances_heap = distances_heap
        self.distances_dict = distances_dict
        heapq.heapify(self.distances_heap)
        self.__processed_node: set[Node] = set()
        self.path_to_point = {}


    #search the shortest path to unprocessed node
    def search_smallest_path(self) -> tuple[float, Node] | None:
        if self.distances_heap:
            distance = heapq.heappop(self.distances_heap)
            return distance
        return None


    def set_new_distances(self, smolest_dist: tuple[float, Node]):
        dist, processing_node = smolest_dist

        if dist > self.distances_dict[processing_node]:
            return

        for path in processing_node.paths:

            if path[1] in self.__processed_node:
                continue

            new_path_to_point: float = path[0] + dist
            if new_path_to_point < self.distances_dict[path[1]]:
                self.distances_dict[path[1]] = new_path_to_point
                heapq.heappush(self.distances_heap, (new_path_to_point, path[1]))

        self.__processed_node.add(processing_node)