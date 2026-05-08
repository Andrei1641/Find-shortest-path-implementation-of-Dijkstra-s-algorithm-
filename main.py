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

font = pygame.font.SysFont(None, 36)

clock: Clock = pygame.time.Clock()

pos_nodes: dict[Node, tuple[int, int],] = {}
NODE_RADIUS = 25

shortest_time = 0
shortest_path = 0

first_chosen_node: tuple[Node, tuple[int, int]] | None = None
second_chosen_node: tuple[Node, tuple[int, int]] | None = None

counter: int = 0

path_time_pos: list[tuple[tuple[int, int], int]] = []

typing_mode = 0
towards_time = ""
backwards_time = ""

select_window: str = ''

start_n: tuple[Node, tuple[int, int]] | None = None
finish_n: tuple[Node, tuple[int, int]] | None = None

stop = False
while not stop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #select node
        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    first_chosen_node, second_chosen_node = mouse_node_collate(pos_nodes), first_chosen_node


        if event.type == pygame.KEYDOWN:
            #create node
            if event.key == pygame.K_p:
                mouse_pos = pygame.mouse.get_pos()
                collate = mouse_node_collate(pos_nodes, shift=10)

                if not collate:
                    new_node = Node()
                    pos_nodes[new_node] = mouse_pos


            if event.key == pygame.K_s and (finish_n and start_n):
                searcher = Searcher(start_n[0], list(pos_nodes.keys()))
                counter = searcher.find_shortest_path(counter)
                counter += 1
                d = searcher.get_distances_dict()
                p = searcher.get_path()
                shortest_path = p
                shortest_time = d[finish_n[0]]


            #set mode
            if event.key == pygame.K_RETURN and typing_mode == 0:
                if (first_chosen_node and second_chosen_node) and (first_chosen_node != second_chosen_node):
                    typing_mode = 1
                elif first_chosen_node == second_chosen_node or (bool(first_chosen_node) ^ bool(second_chosen_node)):
                    typing_mode = 4

            elif event.key == pygame.K_RETURN and typing_mode == 1:
                typing_mode = 2
            elif event.key == pygame.K_RETURN and typing_mode == 2:
                typing_mode = 3

            #mode reaktion
            #towards_time_path
            if typing_mode == 1:
                select_window = "Type towards time path"
                if event.unicode.isdigit():
                    towards_time += event.unicode

            #backwarts_time_path
            if typing_mode == 2:
                select_window = "Type backwards time path"
                if event.unicode.isdigit():
                    backwards_time += event.unicode

            #set_paths
            if typing_mode == 3:
                select_window = ''
                if not (towards_time.isdigit() and backwards_time.isdigit()):
                    second_chosen_node[0].add_path(first_chosen_node[0], counter)
                    counter += 2
                else:
                    second_chosen_node[0].add_path(first_chosen_node[0], counter, int(towards_time), int(backwards_time))
                    counter += 2
                towards_time = ''
                backwards_time = ''
                typing_mode = 0

            #start_select
            if typing_mode == 4 and not start_n:
                start_n = first_chosen_node or second_chosen_node
                typing_mode = 0

            #finish_select
            if typing_mode == 4 and start_n:
                finish_n = first_chosen_node or second_chosen_node
                typing_mode = 0


    #rendering
    screen.fill((0, 0, 0))

    for n, n_pos in pos_nodes.items():
        pygame.draw.circle(screen, (100, 10, 10), n_pos, NODE_RADIUS)
        for time, _, next_n in n.paths:
            pygame.draw.line(screen, (100, 10, 10), pos_nodes[n] , pos_nodes[next_n], 20)

            norm = 40

            x1, y1 = pos_nodes[n]
            x2, y2 = pos_nodes[next_n]

            x1, x2 = x1 - 5, x2 - 5
            y1, y2 = y1 - 5, y2 - 5


            dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

            shift_x, shift_y = (int(((x2 - x1) / dist) * norm), int(((y2 - y1) / dist) * norm))

            time_pos: tuple[int, int] = (x1 + shift_x, y1 + shift_y)

            path_time_pos.append((time_pos, time))


    if first_chosen_node:
        pygame.draw.circle(screen, (10, 100, 10), first_chosen_node[1], NODE_RADIUS)
    if second_chosen_node:
        pygame.draw.circle(screen, (10, 100, 10), second_chosen_node[1], NODE_RADIUS)
    if start_n:
        pygame.draw.circle(screen, (100, 10, 100), pos_nodes[start_n[0]], NODE_RADIUS)
    if finish_n:
        pygame.draw.circle(screen, (100, 100, 10), pos_nodes[finish_n[0]], NODE_RADIUS)

    if shortest_time:
        s_t = font.render("Shortest time: " + str(shortest_time), True, (255, 255, 255))
        screen.blit(s_t, (10, 10))
    if shortest_path:
        pygame.draw.circle(screen, (255, 255, 255), pos_nodes[finish_n[0]], NODE_RADIUS)
        tmp_node = shortest_path[finish_n[0]]
        while tmp_node:
            pygame.draw.circle(screen, (255, 255, 255), pos_nodes[tmp_node], NODE_RADIUS)
            tmp_node = shortest_path[tmp_node]
    if path_time_pos:
        for i in path_time_pos:
            p_t_p = font.render(str(i[1]), True, (255, 255, 255))

            screen.blit(p_t_p, i[0])

    # input window
    if select_window:
        width = 350
        height = 100
        x, y = screen.get_size()
        x, y = x // 2 - width // 2, y // 2 - height // 2
        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))

        text = font.render(select_window, True, (255, 255, 255))
        screen.blit(text, (x + 5, y + 5))

        time_input = ''
        if select_window == 'Type towards time path':
            time_input = font.render(towards_time, True, (255, 255, 255))
        else:
            time_input = font.render(backwards_time, True, (255, 255, 255))

        screen.blit(time_input, (x + 5, y + 60))


    pygame.display.flip()