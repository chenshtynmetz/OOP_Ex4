import json
import math
import random
import sys
import time

import pygame
from pygame import RESIZABLE, HWSURFACE, DOUBLEBUF

from client_python.Button import Button
from client_python.GraphAlgo import GraphAlgo
from client_python.client import Client
from client_python.gui_function import Functions
from client_python.pokemon import Pokemon, Agent

WIDTH, HEIGHT = 1080, 720
PORT = 6666
HOST = '127.0.0.1'
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), depth=32,  flags= RESIZABLE)
# screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE | )
# background = pygame.Surface((WIDTH, HEIGHT), depth=32, flags= pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
client = Client()
client.start_connection(HOST, PORT)
algo = GraphAlgo()
algo.load_from_json(client.get_graph())
graph = algo.get_graph()
FONT = pygame.font.SysFont('comicsansms', 18, bold=True)
min_x = float(min(list(graph.nodes.values()), key=lambda n: n.pos[0]).pos[0])
min_y = float(min(list(graph.nodes.values()), key=lambda n: n.pos[1]).pos[1])
max_x = float(max(list(graph.nodes.values()), key=lambda n: n.pos[0]).pos[0])
max_y = float(max(list(graph.nodes.values()), key=lambda n: n.pos[1]).pos[1])
back = pygame.image.load('../imag/back.jpeg')

radius = 15
dic_agents = {}
pokemons = []
t_count = time.time()
m_count = 0
button_stop = Button(pygame.Rect((695, 10), (100, 30)), "Stop", (251, 201, 14))
button_stop.func = client.stop
str_info = json.loads(client.get_info())
sum_of_agents = str_info['GameServer']['agents']
for ag in range(sum_of_agents):
    name = "{\"id\":+" + str(ag) + "}"
    client.add_agent(name)
client.start()

while client.is_running() == 'true':
    back = pygame.transform.scale(back, (screen.get_width(), screen.get_width()))
    screen.blit(back, (0, 0))
    func = Functions(min_x, min_y, max_x, max_y, screen, graph, pokemons, dic_agents, algo)
    # update the pokemons list
    func.update_pokemons(client.get_pokemons())
    # update the graph
    func.update_graph(client.get_graph())
    str_info = json.loads(client.get_info())["GameServer"]
    # update the agents dictionary
    func.updeate_agents(client.get_agents())
    # if the stop button is pressed, stop the connection to the server gracefully.
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
    for e in graph.edges.values():
        # find the edge nodes
        src = next(n for n in graph.nodes.values() if n.id == e.src)
        dest = next(n for n in graph.nodes.values() if n.id == e.dest)
        # scaled positions
        src_x = func.my_scale(src.pos[0], x=True)
        src_y = func.my_scale(src.pos[1], y=True)
        dest_x = func.my_scale(dest.pos[0], x=True)
        dest_y = func.my_scale(dest.pos[1], y=True)
        # draw the line
        pygame.draw.line(screen, pygame.Color(69, 69, 69),
                         (src_x, src_y), (dest_x, dest_y), width=2)
    for n in graph.nodes.values():
        x = func.my_scale(n.pos[0], x=True)
        y = func.my_scale(n.pos[1], y=True)
        # draw the vertex
        pygame.draw.circle(screen, pygame.Color(128, 0, 64), (x, y), radius)
        id_srf = FONT.render(str(n.id), True, pygame.Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)
    # draw agents
    for agent in dic_agents.values():
        pygame.draw.circle(screen, pygame.Color(251, 201, 14),
                           (int(agent.pos[0]), int(agent.pos[1])), 10)
    # draw pokemon
    for p in pokemons:
        p.edge = func.pok_on_edge(p)
        p_x = func.my_scale(p.pos[0], x=True)
        p_y = func.my_scale(p.pos[1], y=True)
        if p.type == -1:
            pygame.draw.circle(screen, pygame.Color(0, 196, 196), (int(p_x), int(p_y)), 10)
        else:
            pygame.draw.circle(screen, pygame.Color(255, 0, 128), (int(p_x), int(p_y)), 10)
    sign = True
    for a in dic_agents.values():
        if a.dest == -1:
            sign = False
            if len(a.path) == 0:
                # if the agent dont have path to do, allocate pokemon to him
                func.allocate_agent_to_pok(a)
            else:
                # go to the next node
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
    # moves counter
    pygame.draw.rect(screen, button_stop.color, pygame.Rect((589, 10), (102, 30)))
    m_count = str_info['moves']
    moves_text = FONT.render("Moves:" + str(m_count), True, pygame.Color(0, 0, 0))
    screen.blit(moves_text, (590, 10))
    # stop button
    button_stop_text = FONT.render(button_stop.text, True, (0, 0, 0))
    pygame.draw.rect(screen, button_stop.color, button_stop.rect)
    screen.blit(button_stop_text, (button_stop.rect.x + 10, button_stop.rect.y))
    # time counter
    pygame.draw.rect(screen, button_stop.color, pygame.Rect((485, 10), (100, 30)))
    time_text = FONT.render("Time: " + str(int(pygame.time.get_ticks() / 1000)), True, pygame.Color(0, 0, 0))
    screen.blit(time_text, (490, 10))
    pygame.display.update()
    clock.tick(60)
    t_to_end = int(client.time_to_end()) / 1000
    if int(str_info['moves']) / (time.time() - t_count) < 9.8 and sign:
        client.move()
