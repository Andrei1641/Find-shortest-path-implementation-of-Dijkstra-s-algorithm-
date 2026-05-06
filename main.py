import sys

from pygame.time import Clock

from node import Node
from searcher import Searcher
import pygame


pygame.init()

screen = pygame.display.set_mode((500, 500))

clock: Clock = pygame.time.Clock()

nodes_pos: dict[tuple[int, int], Node] = {}
NODE_RADIUS = 25

stop = False
while not stop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                mouse_pos = pygame.mouse.get_pos()
                dist_to_mouse = float('inf')
                collate = False
                for pos in nodes_pos:
                    dist_to_mouse =  ((pos[0] - mouse_pos[0]) ** 2 + (pos[1] - mouse_pos[1]) ** 2) ** 0.5
                    if dist_to_mouse < 2 * NODE_RADIUS + 10:
                        collate = True

                if not collate:
                    nodes_pos[mouse_pos] = Node()
                    pygame.draw.circle(screen, (100, 10, 10), mouse_pos, NODE_RADIUS)


    pygame.display.flip()
    clock.tick(60)


# a = Node()
# b = Node()
# c = Node()
# d = Node()
# e = Node()
# f = Node()
#
# node_ls: list[Node] = [a, b, c, d, e, f]
#
# # a - start point
#
#
# a.add_path(b, 5, 5)
# a.add_path(c, 0, 0)
# c.add_path(d, 30, 30)
# c.add_path(e, 35, 35)
# b.add_path(d, 15, 15)
# b.add_path(e, 20, 20)
# d.add_path(f, 20, 20)
# e.add_path(f, 10, 10)
#
#
# searcher = Searcher(a, node_ls)
#
# searcher.find_shortest_path()
#
# d = searcher.get_distances_dict()
#
# print(d[f])