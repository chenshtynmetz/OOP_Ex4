import json
import math
import random
import time
from types import SimpleNamespace
import networkx as nx
import pygame

from client_python.Button import Button
from client_python.GraphAlgo import GraphAlgo
from client_python.client import Client
from client_python.pokemon import Pokemon

WIDTH, HEIGHT = 1080, 720
PORT = 6666
HOST = '127.0.0.1'
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), depth=32, flags=pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
client = Client()
client.start_connection(HOST, PORT)
algo = GraphAlgo()
# dict_info = json.loads(client.get_info())
# path = dict_info["GameServer"]["graph"]
algo.load_from_json(client.get_graph())
graph = algo.get_graph()
FONT = pygame.font.SysFont('Arial', 20, bold=True)
min_x = float(min(list(graph.nodes.values()), key=lambda n: n.pos[0]).pos[0])
min_y = float(min(list(graph.nodes.values()), key=lambda n: n.pos[1]).pos[1])
max_x = float(max(list(graph.nodes.values()), key=lambda n: n.pos[0]).pos[0])
max_y = float(max(list(graph.nodes.values()), key=lambda n: n.pos[1]).pos[1])
radius = 15


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


def distance(pos1: tuple, pos2: tuple) -> float:
    x = pos1[0] - pos2[0]
    y = pos1[1] - pos2[1]
    x = x * x
    y = y * y
    ans = math.sqrt(x + y)
    return ans


def pok_on_edge(pok: Pokemon):
    esp = 0.0000000001
    for src in graph.e_dictOfSrc.keys():
        for dest in graph.e_dictOfSrc.get(src).keys():
            len_edge = distance(graph.nodes.get(src).pos, graph.nodes.get(dest).pos)
            len1 = distance(graph.nodes.get(src).pos, pok.pos)
            len2 = distance(pok.pos, graph.nodes.get(dest).pos)
            if abs((len2 + len1) - len_edge) <= esp:
                return graph.edges.get((src, dest))


def next_edge(agent, dest):
    client.choose_next_edge(
        '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(dest) + '}')
    ttl = client.time_to_end()
    print(ttl, client.get_info())

str_info = json.loads(client.get_info())
sum_of_agents = str_info['GameServer']['agents']
for ag in range(sum_of_agents):
    name = "{\"id\":+"+str(ag)+"}"
    client.add_agent(name)
client.start()
pokemons = []
button_stop = Button(pygame.Rect((700, 10), (70, 20)), "Stop", (255, 0, 0))
button_stop.func = client.stop
while client.is_running() == 'true':
    pokemons.clear()
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
    # pokemons = json.loads(client.get_pokemons(),
    #                       object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    # pokemons = [p.Pokemon for p in pokemons]
    # for p in pokemons:
    #     x, y, _ = p.pos.split(',')
    #     p.pos = SimpleNamespace(x=my_scale(
    #         float(x), x=True), y=my_scale(float(y), y=True))
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    if button_stop.is_pressed:
        button_stop.func()
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_stop.rect.collidepoint(event.pos):
                button_stop.pressed()
    screen.fill(pygame.Color(0, 0, 0))
    for e in graph.edges.values():
        # find the edge nodes
        src = next(n for n in graph.nodes.values() if n.id == e.src)
        dest = next(n for n in graph.nodes.values() if n.id == e.dest)
        # scaled positions
        src_x = my_scale(src.pos[0], x=True)
        src_y = my_scale(src.pos[1], y=True)
        dest_x = my_scale(dest.pos[0], x=True)
        dest_y = my_scale(dest.pos[1], y=True)
        # draw the line
        pygame.draw.line(screen, pygame.Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y), width=2)
    for n in graph.nodes.values():
        x = my_scale(n.pos[0], x=True)
        y = my_scale(n.pos[1], y=True)
        pygame.draw.circle(screen, pygame.Color(255, 128, 0), (x, y), radius)
        id_srf = FONT.render(str(n.id), True, pygame.Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)
    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, pygame.Color(122, 61, 23),
                           (int(agent.pos.x), int(agent.pos.y)), 10)
        # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        p_x = my_scale(p.pos[0], x=True)
        p_y = my_scale(p.pos[1], y=True)
        pygame.draw.circle(screen, pygame.Color(0, 255, 255), (int(p_x), int(p_y)), 10)
    for p in pokemons:
        p.edge = pok_on_edge(p)
    for agent in agents:
        if agent.dest == -1:
            len, path = algo.shortest_path(agent.src, pokemons[0].edge.src)
            for ver in path:
                next_edge(agent, ver)
            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(pokemons[0].edge.dest) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())
    button_stop_text = FONT.render(button_stop.text, True, (0, 0, 0))
    pygame.draw.rect(screen, button_stop.color, button_stop.rect)
    screen.blit(button_stop_text, (button_stop.rect.x + 10, button_stop.rect.y))
    pygame.draw.rect(screen, (0, 0, 0), [20, 15, 100, 70])
    time_text = FONT.render("Time: " + str(int(pygame.time.get_ticks() / 1000)), True, pygame.Color(255, 255, 255))
    rect = time_text.get_rect(center=(70, 50))
    screen.blit(time_text, rect)
    pygame.display.update()
    clock.tick(60)
    client.move()

# todo check why the program stop in line 74-75