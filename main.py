import sys

from pygame.time import Clock

from node import Node
from searcher import Searcher
import pygame


def mouse_node_collate(nodes_pos: dict[Node, tuple[int, int]], *, shift = 0) ->  tuple[Node, tuple[int, int]] | None:
    mouse_pos = pygame.mouse.get_pos()
    for node, pos in nodes_pos.items():
        dist_to_mouse = ((pos[0] - mouse_pos[0]) ** 2 + (pos[1] - mouse_pos[1]) ** 2) ** 0.5
        if dist_to_mouse < 2 * NODE_RADIUS + shift:
            return node, pos
    return None


pygame.init()

screen = pygame.display.set_mode((500, 500))

clock: Clock = pygame.time.Clock()

pos_nodes: dict[Node, tuple[int, int],] = {}
NODE_RADIUS = 25


first_chosen_node: tuple[Node, tuple[int, int]] | None = None
second_chosen_node: tuple[Node, tuple[int, int]] | None = None



typing_mode = 0
towards_time = ""
backwards_time = ""


start_n: tuple[Node, tuple[int, int]] | None = None
finish_n: tuple[Node, tuple[int, int]] | None = None

stop = False
while not stop:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    first_chosen_node, second_chosen_node = mouse_node_collate(pos_nodes), first_chosen_node


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                mouse_pos = pygame.mouse.get_pos()
                collate = mouse_node_collate(pos_nodes, shift=10)

                if not collate:
                    new_node = Node()
                    pos_nodes[new_node] = mouse_pos


            if event.key == pygame.K_RETURN and typing_mode == 0:
                if (first_chosen_node and second_chosen_node) and (first_chosen_node != second_chosen_node):
                    typing_mode = 1
                elif first_chosen_node == second_chosen_node or (bool(first_chosen_node) ^ bool(second_chosen_node)):
                    typing_mode = 4

            elif event.key == pygame.K_RETURN and typing_mode == 1:
                typing_mode = 2
            elif event.key == pygame.K_RETURN and typing_mode == 2:
                typing_mode = 3

            if typing_mode == 1:
                if event.unicode.isdigit():
                    towards_time += event.unicode


            if typing_mode == 2:
                if event.unicode.isdigit():
                    backwards_time += event.unicode

            if typing_mode == 3:
                if not (towards_time.isdigit() and backwards_time.isdigit()):
                    second_chosen_node[0].add_path(first_chosen_node[0])
                else:
                    second_chosen_node[0].add_path(first_chosen_node[0], int(towards_time), int(backwards_time))
                typing_mode = 0


            if typing_mode == 4 and not start_n:
                start_n = first_chosen_node or second_chosen_node
                typing_mode = 0

            if typing_mode == 4 and start_n:
                finish_n = first_chosen_node or second_chosen_node
                typing_mode = 0

            if event.key == pygame.K_s and (finish_n and start_n):
                searcher = Searcher(start_n[0], list(pos_nodes.keys()))
                searcher.find_shortest_path()
                d = searcher.get_distances_dict()
                print(d[finish_n[0]])


    for n, n_pos in pos_nodes.items():
        pygame.draw.circle(screen, (100, 10, 10), n_pos, NODE_RADIUS)
        for _, next_n in n.paths:
            pygame.draw.line(screen, (100, 10, 10), pos_nodes[n] , pos_nodes[next_n], 20)



    if first_chosen_node:
        pygame.draw.circle(screen, (10, 100, 10), first_chosen_node[1], NODE_RADIUS)
    if second_chosen_node:
        pygame.draw.circle(screen, (10, 100, 10), second_chosen_node[1], NODE_RADIUS)
    if start_n:
        pygame.draw.circle(screen, (100, 10, 100), pos_nodes[start_n[0]], NODE_RADIUS)
    if finish_n:
        pygame.draw.circle(screen, (100, 100, 10), pos_nodes[finish_n[0]], NODE_RADIUS)


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