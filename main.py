from node import Node
from searcher import Searcher

a = Node()
b = Node()
c = Node()
d = Node()
e = Node()
f = Node()

node_ls: list[Node] = [a, b, c, d, e, f]

# a - start point


a.add_path(b, 5, 5)
a.add_path(c, 0, 0)
c.add_path(d, 30, 30)
c.add_path(e, 35, 35)
b.add_path(d, 15, 15)
b.add_path(e, 20, 20)
d.add_path(f, 20, 20)
e.add_path(f, 10, 10)


searcher = Searcher(a, node_ls)

searcher.find_shortest_path()

d = searcher.get_distances_dict()

print(d[f])