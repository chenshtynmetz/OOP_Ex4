import json
import math
import random

from client_python.GraphAlgo import GraphAlgo
from client_python.client import Client
from client_python.pokemon import Pokemon, Agent
from client_python import DiGraph


class Functions:

    def __init__(self, min_x, min_y, max_x, max_y, screen, graph: DiGraph, pokemons: [], dic_agents: {},
                 algo: GraphAlgo):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.screen = screen
        self.graph = graph
        self.pokemons = pokemons
        #self.client = client
        self.dic_agents = dic_agents
        self.algo = algo

    def scale(self, data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
        return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

    # decorate scale with the correct values
    def my_scale(self, data, x=False, y=False):
        if x:
            return self.scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return self.scale(data, 50, self.screen.get_height() - 50, self.min_y, self.max_y)

    # this function calculate the distance between 2 points on the graph
    def distance(self, pos1: tuple, pos2: tuple) -> float:
        x1 = math.pow(pos1[0] - pos2[0], 2)
        y1 = pos1[1] - pos2[1]
        y2 = y1 * y1
        ans = math.sqrt(x1 + y2)
        return ans

    # this function return the edge that the pokemon stand on
    def pok_on_edge(self, pok: Pokemon):
        esp = 0.0000000001
        for src in self.graph.e_dictOfSrc.keys():
            for dest in self.graph.e_dictOfSrc.get(src).keys():
                len_edge = self.distance(self.graph.nodes.get(src).pos, self.graph.nodes.get(dest).pos)
                len1 = self.distance(self.graph.nodes.get(src).pos, pok.pos)
                len2 = self.distance(pok.pos, self.graph.nodes.get(dest).pos)
                if abs((len2 + len1) - len_edge) <= esp:
                    if pok.type == 1:
                        return self.graph.edges.get((src, dest))
                    if pok.type == -1:
                        return self.graph.edges.get((dest, src))

    # this function clear and update the list of the pokemons.
    def update_pokemons(self, file):
        dict1 = json.loads(file)
        list_pokemons = dict1["Pokemons"]
        if self.pokemons !=None:
            self.pokemons.clear()
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
                self.pokemons.append(Pokemon(val, typ, pos))
            except Exception:
                one_pokemon = pokem["Pokemon"]
                val = one_pokemon['value']
                typ = one_pokemon['type']
                x1 = random.uniform(35.19, 35.22)
                y1 = random.uniform(32.05, 32.22)
                pos = (x1, y1, 0.0)
                self.pokemons.append(Pokemon(val, typ, pos))

    # this function update the dictionary of the agents.
    def updeate_agents(self, file: str):
        dict2 = json.loads(file)
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
                x1 = self.my_scale(float(x1), x=True)
                y1 = self.my_scale(float(y1), y=True)
                pos = (x1, y1, z)
                if id1 in self.dic_agents:
                    self.dic_agents[id1].value = val
                    self.dic_agents[id1].src = src1
                    self.dic_agents[id1].dest = dest1
                    self.dic_agents[id1].speed = speed
                    self.dic_agents[id1].pos = pos
                else:
                    self.dic_agents[id1] = Agent(id1, val, src1, dest1, speed, pos)
            except Exception:
                one_agent = a["Agent"]
                id1 = one_agent['id']
                val = one_agent['value']
                src1 = one_agent['src']
                dest1 = one_agent['dest']
                speed = one_agent['speed']
                x1 = random.uniform(35.19, 35.22)
                y1 = random.uniform(32.05, 32.22)
                x1 = self.my_scale(float(x1), x=True)
                y1 = self.my_scale(float(y1), y=True)
                pos = (x1, y1, 0.0)
                if id1 in self.dic_agents:
                    self.dic_agents[id1].value = val
                    self.dic_agents[id1].src = src1
                    self.dic_agents[id1].dest = dest1
                    self.dic_agents[id1].speed = speed
                    self.dic_agents[id1].pos = pos
                else:
                    self.dic_agents[id1] = Agent(id1, val, src1, dest1, speed, pos)

    # this function update the graph
    def update_graph(self, file):
        self.algo.load_from_json(file)
        graph = self.algo.get_graph()

    # this function get agent and allocate to him a pokemon.
    def allocate_agent_to_pok(self, agent: Agent):
        flag = True
        while flag:
            min_len = math.inf
            min_path = []
            min_pok = None
            for po in self.pokemons:
                if not po.collected:
                    if agent.src == po.edge.src:
                        min_path.append(agent.src)
                        min_pok = po
                        break
                    len1, path1 = self.algo.shortest_path(agent.src, po.edge.src)
                    if min_len > len1:
                        min_len = len1
                        min_path = path1
                        min_pok = po
            for agn in self.dic_agents.values():
                if min_pok == agn.pok:
                    continue
            flag = False
            st = min_path.pop(0)
            agent.pok = min_pok
            min_pok.collected = True
            min_path.append(min_pok.edge.dest)
            agent.path = min_path
            # print(agent.path)
