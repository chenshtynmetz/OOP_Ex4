# init pygame
import json
import math
import random

import pygame
from pygame import RESIZABLE

from client_python.DiGraph import DiGraph
from client_python.DiGraph import DiGraph
from client_python.GraphAlgo import GraphAlgo
from client_python.client import Client
from client_python.pokemon import Pokemon, agent


class myGame:
    WIDTH, HEIGHT = 1080, 720

    # # default port
    # PORT = 6666
    # # server host (default localhost 127.0.0.1)
    # HOST = '127.0.0.1'
    pygame.init()
    min_x = math.inf
    max_x = math.inf * -1
    min_y = math.inf
    max_y = math.inf * -1
    margin = 50
    r = 12
    Font = pygame.font.SysFont('david', 20)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
    clock = pygame.time.Clock()
    pygame.font.init()

    # client = Client()
    # client.start_connection(HOST, PORT)

    def __init__(self):
        self.pokemons = []
        self.agents = []
        self.graph_alg = GraphAlgo()
        self.load_pokemons(self.client.get_pokemons())
        self.load_agents(self.client.get_agents())
        self.load_graph(self.client.get_graph())
        self.graph = self.graph_alg.get_graph()

    # load graph from json file
    def load_graph(self, file_name: str):
        self.graph_alg.load_from_json(file_name)

    # load pokemons from json file
    def load_pokemons(self, file: str) -> bool:
        try:
            dict = json.loads(file)
            list_pokemons = dict["Pokemons"]
            for p in list_pokemons:
                try:
                    val = p['value']
                    typ = p['type']
                    temp = p['pos'].split(",")
                    x = float(temp[0])
                    y = float(temp[1])
                    z = float(temp[2])
                    pos = (x, y, z)
                    self.pokemons.append(Pokemon(val, typ, pos))
                except Exception:
                    val = p['value']
                    typ = p['type']
                    x = random.uniform(35.19, 35.22)
                    y = random.uniform(32.05, 32.22)
                    pos = (x, y, 0.0)
                    self.pokemons.append(Pokemon(val, typ, pos))
        except:
            return False
        return True

    # load agents from json file
    def load_agents(self, file: str) -> bool:
        try:
            dict = json.loads(file)
            list_agents = dict["Agents"]
            for a in list_agents:
                try:
                    id1 = a['id']
                    val = a['value']
                    src = a['src']
                    dest = a['dest']
                    speed = a['speed']
                    temp = a['pos'].split(",")
                    x = float(temp[0])
                    y = float(temp[1])
                    z = float(temp[2])
                    pos = (x, y, z)
                    self.agents.append(agent(id1, val, src, dest, speed, pos))
                except Exception:
                    id1 = a['id']
                    val = a['value']
                    src = a['src']
                    dest = a['dest']
                    speed = a['speed']
                    x = random.uniform(35.19, 35.22)
                    y = random.uniform(32.05, 32.22)
                    pos = (x, y, 0.0)
                    self.agents.append(agent(id1, val, src, dest, speed, pos))
        except:
            return False
        return True

    # this function spread the nodes on the screen
    def scale(self, data, min_screen, max_screen, min_data, max_data):
        return ((float(data) - float(min_data)) / (float(max_data) - float(min_data))) * (
                max_screen - min_screen) + min_screen

    # this function draw arrow
    def draw_arrow(self, src, dst, d, hi, color):
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
        pygame.draw.line(self.screen, color, src, dst, width=2)
        pygame.draw.polygon(self.screen, color, points)

    def draw(self):
        self.min_x = float(min(list(self.graph.nodes.values()), key=lambda n: n.pos[0]).pos[0])
        self.max_x = float(max(list(self.graph.nodes.values()), key=lambda n: n.pos[0]).pos[0])
        self.min_y = float(min(list(self.graph.nodes.values()), key=lambda n: n.pos[1]).pos[1])
        self.max_y = float(max(list(self.graph.nodes.values()), key=lambda n: n.pos[1]).pos[1])
        for edge in self.graph.edges.values():
            src = self.graph.nodes.get(edge.src).pos
            dest = self.graph.nodes.get(edge.dest).pos
            src_x = self.scale(src[0], self.margin, self.screen.get_width() - self.margin, self.min_x, self.max_x)
            src_y = self.scale(src[1], self.margin, self.screen.get_height() - self.margin, self.min_y, self.max_y)
            dest_x = self.scale(dest[0], self.margin, self.screen.get_width() - self.margin, self.min_x, self.max_x)
            dest_y = self.scale(dest[1], self.margin, self.screen.get_height() - self.margin, self.min_y, self.max_y)
            self.draw_arrow((src_x, src_y), (dest_x, dest_y), 15, 5, (0, 0, 0))
        for node in self.graph.nodes.values():
            x = self.scale(node.pos[0], self.margin, self.screen.get_width() - self.margin, self.min_x, self.max_x)
            y = self.scale(node.pos[1], self.margin, self.screen.get_height() - self.margin, self.min_y, self.max_y)
            pygame.draw.circle(self.screen, pygame.Color(255, 128, 0), (x, y), self.r)
            node_text = self.Font.render(str(node.id), True, pygame.Color((0, 0, 244)))
            self.screen.blit(node_text, (x - 8, y - 8))

    def display(self):
        # self.client.start()
        # while self.client.is_running() == 'true':
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        self.screen.fill(pygame.Color(255, 250, 250))
        pygame.display.set_caption("game")
        self.draw()
        pygame.display.update()
        # refresh rate
        self.clock.tick(60)

    # def run(self):
    #     while self.client.is_running() == 'true':
    #         self.display()


# while client.is_running() == 'true':
#     game = myGame()
#     game.display()
