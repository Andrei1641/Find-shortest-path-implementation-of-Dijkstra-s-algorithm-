from node import Node
import heapq


class Searcher:
    def __init__(self, start: Node, node_ls: list[Node]):
        self.__distances_heap = [(0, 0, start)]
        self.__distances_dict = Searcher.__dict_ini(start, node_ls)
        heapq.heapify(self.__distances_heap)
        self.__processed_node: set[Node] = set()
        self.__path_to_point = {}

    @staticmethod
    def __dict_ini(start: Node, node_ls: list[Node]) -> dict[Node, float]:
        d: dict[Node, float] = {}
        for n in node_ls:
            if n != start:
                d.update({n : float('inf')})
            else:
                d.update({n: 0})
        return d


    def get_distances_dict(self):
        return self.__distances_dict

    #search the shortest path to unprocessed node
    def __search_smallest_path(self) -> tuple[float, int, Node] | None:
        if self.__distances_heap:
            for _ in self.__distances_heap:
                distance = heapq.heappop(self.__distances_heap)
                if distance[2] not in self.__processed_node:
                    return distance
        return None


    def __set_new_distances(self, smolest_dist: tuple[float, int, Node], id_count: int):
        dist, _, processing_node = smolest_dist

        if dist > self.__distances_dict[processing_node]:
            return

        for path in processing_node.paths:

            if path[1] in self.__processed_node:
                continue

            new_path_to_point: float = path[0] + dist
            if new_path_to_point < self.__distances_dict[path[1]]:
                self.__distances_dict[path[1]] = new_path_to_point
                heapq.heappush(self.__distances_heap, (new_path_to_point, id_count, path[1]))

        self.__processed_node.add(processing_node)


    def find_shortest_path(self):
        smolest_dist = self.__search_smallest_path()
        counter_id = 1

        while smolest_dist is not None:
            self.__set_new_distances(smolest_dist, counter_id)
            smolest_dist = self.__search_smallest_path()
            counter_id += 1