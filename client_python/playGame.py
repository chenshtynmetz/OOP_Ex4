import json
import math
import random
import sys
import time

import pygame

from client_python.Button import Button
from client_python.GraphAlgo import GraphAlgo
from client_python.client import Client
from client_python.pokemon import Pokemon, Agent

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
algo.load_from_json(client.get_graph())
graph = algo.get_graph()
FONT = pygame.font.SysFont('Arial', 20, bold=True)
min_x = float(min(list(graph.nodes.values()), key=lambda n: n.pos[0]).pos[0])
min_y = float(min(list(graph.nodes.values()), key=lambda n: n.pos[1]).pos[1])
max_x = float(max(list(graph.nodes.values()), key=lambda n: n.pos[0]).pos[0])
max_y = float(max(list(graph.nodes.values()), key=lambda n: n.pos[1]).pos[1])
up_pok = pygame.image.load('../imag/up_pok.jpg')
back = pygame.image.load('../imag/back.jpeg')
pok_w = 40
pok_h = 15
up_pok = pygame.transform.scale(up_pok, (pok_w, pok_h))
radius = 15
dic_agents = {}
pokemons = []
t_count = time.time()
m_count = 0
button_stop = Button(pygame.Rect((700, 10), (90, 30)), "Stop", (255, 0, 0))
button_stop.func = client.stop
str_info = json.loads(client.get_info())
sum_of_agents = str_info['GameServer']['agents']
for ag in range(sum_of_agents):
    name = "{\"id\":+" + str(ag) + "}"
    client.add_agent(name)
client.start()


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
    x1 = math.pow(pos1[0] - pos2[0], 2)
    y1 = pos1[1] - pos2[1]
    y2 = y1 * y1
    ans = math.sqrt(x1 + y2)
    return ans


def pok_on_edge(pok: Pokemon):
    esp = 0.0000000001
    for src in graph.e_dictOfSrc.keys():
        for dest in graph.e_dictOfSrc.get(src).keys():
            len_edge = distance(graph.nodes.get(src).pos, graph.nodes.get(dest).pos)
            len1 = distance(graph.nodes.get(src).pos, pok.pos)
            len2 = distance(pok.pos, graph.nodes.get(dest).pos)
            if abs((len2 + len1) - len_edge) <= esp:
                if pok.type == 1:
                    return graph.edges.get((src, dest))
                if pok.type == -1:
                    return graph.edges.get((dest, src))


def update_pokemons(file):
    dict1 = json.loads(file)
    list_pokemons = dict1["Pokemons"]
    pokemons.clear()
    for pokem in list_pokemons:
        try:
            one_pokemon = pokem["Pokemon"]
            val = one_pokemon['value']
            typ = one_pokemon['type']
            temp = one_pokemon['pos'].split(",")
            x1 = float(temp[0])
            y1 = float(temp[1])
            z = float(temp[2])
            pos = (x1, y1, z)
            pokemons.append(Pokemon(val, typ, pos))
        except Exception:
            one_pokemon = p["Pokemon"]
            val = one_pokemon['value']
            typ = one_pokemon['type']
            x1 = random.uniform(35.19, 35.22)
            y1 = random.uniform(32.05, 32.22)
            pos = (x1, y1, 0.0)
            pokemons.append(Pokemon(val, typ, pos))


def updeate_agents():
    dict2 = json.loads(client.get_agents())
    list_agents = dict2["Agents"]
    for a in list_agents:
        try:
            one_agent = a["Agent"]
            id1 = one_agent['id']
            val = one_agent['value']
            src1 = one_agent['src']
            dest1 = one_agent['dest']
            speed = one_agent['speed']
            temp = one_agent['pos'].split(",")
            x1 = float(temp[0])
            y1 = float(temp[1])
            z = float(temp[2])
            x1 = my_scale(float(x1), x=True)
            y1 = my_scale(float(y1), y=True)
            pos = (x1, y1, z)
            if id1 in dic_agents:
                dic_agents[id1].value = val
                dic_agents[id1].src = src1
                dic_agents[id1].dest = dest1
                dic_agents[id1].speed = speed
                dic_agents[id1].pos = pos
            else:
                dic_agents[id1] = Agent(id1, val, src1, dest1, speed, pos)
        except Exception:
            one_agent = a["Agent"]
            id1 = one_agent['id']
            val = one_agent['value']
            src1 = one_agent['src']
            dest1 = one_agent['dest']
            speed = one_agent['speed']
            x1 = random.uniform(35.19, 35.22)
            y1 = random.uniform(32.05, 32.22)
            x1 = my_scale(float(x1), x=True)
            y1 = my_scale(float(y1), y=True)
            pos = (x1, y1, 0.0)
            if dic_agents.get(id1) == True:
                dic_agents[id1].value = val
                dic_agents[id1].src = src1
                dic_agents[id1].dest = dest1
                dic_agents[id1].speed = speed
                dic_agents[id1].pos = pos
            else:
                dic_agents[id1] = Agent(id1, val, src1, dest1, speed, pos)


def update_graph(file):
    algo.load_from_json(file)
    graph = algo.get_graph()


def allocate_agent_to_pok(agent: Agent):
    flag = True
    while flag:
        min_len = math.inf
        min_path = []
        min_pok = None
        for po in pokemons:
            if not po.collected:
                if agent.src == po.edge.src:
                    min_path.append(agent.src)
                    min_pok = po
                    break
                len1, path1 = algo.shortest_path(agent.src, po.edge.src)
                if min_len > len1:
                    min_len = len1
                    min_path = path1
                    min_pok = po
        for agn in dic_agents.values():
            if min_pok == agn.pok:
                continue
        flag = False
        st = min_path.pop(0)
        agent.pok = min_pok
        min_pok.collected = True
        min_path.append(min_pok.edge.dest)
        agent.path = min_path
        print(agent.path)


while client.is_running() == 'true':
    update_pokemons(client.get_pokemons())
    update_graph(client.get_graph())
    str_info = json.loads(client.get_info())["GameServer"]
    updeate_agents()
    if button_stop.is_pressed:
        button_stop.func()
        sys.exit()
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_stop.rect.collidepoint(event.pos):
                button_stop.pressed()
    screen.blit(back, (0, 0))
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
    for agent in dic_agents.values():
        pygame.draw.circle(screen, pygame.Color(122, 61, 23),
                           (int(agent.pos[0]), int(agent.pos[1])), 10)
    # draw pokemon
    for p in pokemons:
        p.edge = pok_on_edge(p)
        p_x = my_scale(p.pos[0], x=True)
        p_y = my_scale(p.pos[1], y=True)
        if p.type == -1:
            pygame.draw.circle(screen, pygame.Color(0, 255, 255), (int(p_x), int(p_y)), 10)
        else:
            pygame.draw.circle(screen, pygame.Color(250, 0, 2), (int(p_x), int(p_y)), 10)
    sign = True
    for a in dic_agents.values():
        if a.dest == -1:
            sign = False
            if len(a.path) == 0:
                allocate_agent_to_pok(a)
            else:
                next_node = a.path.pop(0)
                if a.src == a.pok.edge.src:
                    client.choose_next_edge(
                        '{"agent_id":' + str(a.id) + ', "next_node_id":' + str(next_node) + '}')
                    ttl = client.time_to_end()
                    print(ttl, client.get_info())
                else:
                    client.choose_next_edge(
                        '{"agent_id":' + str(a.id) + ', "next_node_id":' + str(next_node) + '}')
                    ttl = client.time_to_end()
                    print(ttl, client.get_info())
    # Moves counter window
    pygame.draw.rect(screen, button_stop.color, pygame.Rect((590, 10), (90, 30)))
    m_count = str_info['moves']
    moves_text = FONT.render("Moves: " + str(m_count), True, pygame.Color(0, 0, 0))
    screen.blit(moves_text, (590, 10))
    button_stop_text = FONT.render(button_stop.text, True, (0, 0, 0))
    pygame.draw.rect(screen, button_stop.color, button_stop.rect)
    screen.blit(button_stop_text, (button_stop.rect.x + 10, button_stop.rect.y))
    pygame.draw.rect(screen, (0, 0, 0), [20, 15, 100, 70])
    time_text = FONT.render("Time: " + str(int(pygame.time.get_ticks() / 1000)), True, pygame.Color(255, 255, 255))
    rect = time_text.get_rect(center=(70, 50))
    screen.blit(time_text, rect)
    pygame.display.update()
    clock.tick(60)
    t_to_end = int(client.time_to_end()) / 1000
    if int(str_info['moves']) / (time.time() - t_count) < 10 and sign:
        client.move()
