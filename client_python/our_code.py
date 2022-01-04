import random
import math

from client import Client
import json
from pygame import gfxdraw, RESIZABLE
import pygame
# from pygame import *
# init pygame
from client_python.GraphAlgo import GraphAlgo
from client_python.pokemon import Pokemon
from client_python.pokemon import agent

WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

pokemons = []
agents = []
graph_alg = GraphAlgo()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

graph_alg.load_from_json(client.get_graph())
graph = graph_alg.get_graph()

# for n in graph.Nodes:
#     x, y, _ = n.pos.split(',')
#     n.pos = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = float(min(list(graph.nodes.values()), key=lambda n: n.pos[0]).pos[0])
min_y = float(max(list(graph.nodes.values()), key=lambda n: n.pos[0]).pos[0])
max_x = float(min(list(graph.nodes.values()), key=lambda n: n.pos[1]).pos[1])
max_y = float(max(list(graph.nodes.values()), key=lambda n: n.pos[1]).pos[1])


# this function spread the nodes on the screen
def scale(data, min_screen, max_screen, min_data, max_data):
    return ((float(data) - float(min_data)) / (float(max_data) - float(min_data))) * (
            max_screen - min_screen) + min_screen


def draw_arrow(src, dst, d, hi, color):
    dx = float(dst[0]) - float(src[0])
    dy = float(dst[1]) - float(src[1])
    s = float(math.sqrt(dx * dx + dy * dy))
    x1 = float(s - d)
    x2 = float(x1)
    y1 = float(hi)
    y2 = hi * -1
    sin = dy / s
    cos = dx / s
    x_temp = x1 * cos - y1 * sin + float(src[0])
    y1 = x1 * sin + y1 * cos + float(src[1])
    x1 = x_temp
    x_temp = x2 * cos - y2 * sin + float(src[0])
    y2 = x2 * sin + y2 * cos + float(src[1])
    x2 = x_temp
    points = [(dst[0], dst[1]), (int(x1), int(y1)), (int(x2), int(y2))]
    pygame.draw.line(screen, color, src, dst, width=2)
    pygame.draw.polygon(screen, color, points)


# # decorate scale with the correct values
#
# def my_scale(data, x=False, y=False):
#     if x:
#         return scale(data, 50, screen.get_width() - 50, min_x, max_x)
#     if y:
#         return scale(data, 50, screen.get_height()-50, min_y, max_y)


r = 12
margin = 50
client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""

while client.is_running() == 'true':
    dict = json.loads(client.get_pokemons())
    list_pokemons = dict["Pokemons"]
    for p in list_pokemons:
        try:
            one_pokemon = p["Pokemon"]
            val = one_pokemon['value']
            typ = one_pokemon['type']
            temp = one_pokemon['pos'].split(",")
            x = float(temp[0])
            y = float(temp[1])
            z = float(temp[2])
            pos = (x, y, z)
            pokemons.append(Pokemon(val, typ, pos))
        except Exception:
            one_pokemon = p["Pokemon"]
            val = one_pokemon['value']
            typ = one_pokemon['type']
            x = random.uniform(35.19, 35.22)
            y = random.uniform(32.05, 32.22)
            pos = (x, y, 0.0)
            pokemons.append(Pokemon(val, typ, pos))
        dict = json.loads(client.get_agents())
        list_agents = dict["Agents"]
        for a in list_agents:
            try:
                one_agent = a["Agent"]
                id1 = one_agent['id']
                val = one_agent['value']
                src = one_agent['src']
                dest = one_agent['dest']
                speed = one_agent['speed']
                temp = one_agent['pos'].split(",")
                x = float(temp[0])
                y = float(temp[1])
                z = float(temp[2])
                pos = (x, y, z)
                agents.append(agent(id1, val, src, dest, speed, pos))
            except Exception:
                one_agent = a["Agent"]
                id1 = one_agent['id']
                val = one_agent['value']
                src = one_agent['src']
                dest = one_agent['dest']
                speed = one_agent['speed']
                x = random.uniform(35.19, 35.22)
                y = random.uniform(32.05, 32.22)
                pos = (x, y, 0.0)
                agents.append(agent(id1, val, src, dest, speed, pos))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(pygame.Color(0, 0, 0))
    # draw edges
    for edge in graph.edges.values():
        # find the edge nodes

        src = graph.nodes.get(edge.src).pos
        dest = graph.nodes.get(edge.dest).pos
        src_x = scale(src[0], margin, screen.get_width() - margin, min_x, max_x)
        src_y = scale(src[1], margin, screen.get_height() - margin, min_y, max_y)
        dest_x = scale(dest[0], margin, screen.get_width() - margin, min_x, max_x)
        dest_y = scale(dest[1], margin, screen.get_height() - margin, min_y, max_y)
        draw_arrow((src_x, src_y), (dest_x, dest_y), 15, 5, (0, 0, 0))

    # draw nodes
    for n in graph.nodes.values():
        x = scale(n.pos[0], margin, screen.get_width() - margin, min_x, max_x)
        y = scale(n.pos[1], margin, screen.get_height() - margin, min_y, max_y)
        pygame.draw.circle(screen, pygame.Color(255, 128, 0), (x, y), r)
        node_text = FONT.render(str(n.id), True, pygame.Color((0, 0, 244)))
        screen.blit(node_text, (x - 8, y - 8))
        #
        # # draw the node id
        # id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        # rect = id_srf.get_rect(center=(x, y))
        # screen.blit(id_srf, rect)

    # draw agents
    for ag in agents:
        pygame.draw.circle(screen, pygame.Color(122, 61, 23),
                           (int(ag.pos[0]), int(ag.pos[1])), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        pygame.draw.circle(screen, pygame.Color(0, 255, 255), (int(p.pos[0]), int(p.pos[1])), 10)

    # update screen changes
    pygame.display.update()

    # refresh rate
    clock.tick(60)

    # choose next edge
    for agent in agents:
        if agent.dest == -1:
            next_node = (agent.src - 1) % len(graph.nodes)
            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    client.move()
# game over:

# this function draw arrow
