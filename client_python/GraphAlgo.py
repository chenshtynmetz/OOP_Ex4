import json
import math
import random

from typing import List
from queue import PriorityQueue
import easygui
import pygame

from Button import Button
from DiGraph import DiGraph, Node
from GraphAlgoInterface import GraphAlgoInterface


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph: DiGraph = None):
        if graph is None:
            self.graph = DiGraph()
        else:
            self.graph = graph
        self.WIDHT = 800
        self.HIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDHT, self.HIGHT), depth=32)
        self.r = 12
        self.clock = pygame.time.Clock()
        self.Font = pygame.font.SysFont('david', 20)
        self.result = []
        self.nodes_screen = []
        self.tsp = []
        self.margin = 50
        self.button_center = Button(pygame.Rect((10, 10), (70, 20)), "center", (255, 255, 0))
        self.button_tsp = Button(pygame.Rect((10, 33), (70, 20)), "tsp", (255, 255, 0))
        self.button_load = Button(pygame.Rect((10, 56), (70, 20)), "load", (255, 255, 0))
        self.button_save = Button(pygame.Rect((10, 79), (70, 20)), "save", (255, 255, 0))
        self.button_short = Button(pygame.Rect((10, 101), (120, 20)), "shortest path", (255, 255, 0))
        self.min_x = math.inf
        self.max_x = math.inf * -1
        self.min_y = math.inf
        self.max_y = math.inf * -1

    # return the graph
    def get_graph(self) ->DiGraph:
        return self.graph

    # load new graph from json file
    def load_from_json(self, file: str) -> bool:
        try:
                self.graph.nodes.clear()
                self.graph.edges.clear()
                self.graph.e_dictOfSrc.clear()
                self.graph.e_dictOfDest.clear()
                dict = json.loads(file)
                list_nodes = dict["Nodes"]
                list_edge = dict["Edges"]
                for n in list_nodes:
                    try:
                        temp = n['pos'].split(",")
                        x = float(temp[0])
                        y = float(temp[1])
                        z = float(temp[2])
                        pos = (x, y, z)
                        self.graph.add_node(n['id'], pos)
                    except Exception:
                        x = random.uniform(35.19, 35.22)
                        y = random.uniform(32.05, 32.22)
                        pos = (x, y, 0.0)
                        self.graph.add_node(n['id'], pos)
                for ed in list_edge:
                    self.graph.add_edge(ed['src'], ed['dest'], ed['w'])
        except:
            return False
        return True

    # save the graph to json file
    def save_to_json(self, file_name: str) -> bool:
        if self.graph is None:
            return False
        dict = {"Edges": [], "Nodes": []}
        for node in self.graph.nodes.values():
            dict_node = {"id": node.id}
            if node.pos is not None:
                dict_node["pos"] = f'{node.pos[0]},{node.pos[1]},{node.pos[2]}'
            dict["Nodes"].append(dict_node)
        for edge in self.graph.edges.values():
            dict_edge = {"src": edge.src, "w": edge.weight, "dest": edge.dest}
            dict["Edges"].append(dict_edge)
        try:
            with open(file_name, "w") as f:
                f.write(json.dumps(dict))
                return True
        except:
            return False
        finally:
            f.close()

    # this function calculate the shortest path between 2 vertexes on the graph with diakstra. return the distance and list of all the vertexes in the path.
    def shortest_path(self, id1: int, id2: int) -> (float, list):
        ans = []
        path = self.diakstra(id1, id2)
        if path == math.inf:
            return math.inf, []
        ans.insert(0, id2)
        node_temp = self.graph.nodes.get(id2).tag
        while node_temp != id1:
            ans.insert(0, node_temp)
            node_temp = self.graph.nodes.get(node_temp).tag
        ans.insert(0, id1)
        distance = self.graph.nodes.get(id2).weight
        return distance, ans

   # def shortest_path2(self ,id1: int, id2:int):

    # diakstra algorithm
    def diakstra(self, id1: int, id2: int):
        if id1 == id2:
            return 0
        queue = PriorityQueue()
        for node in self.graph.nodes.values():
            node.weight = math.inf
        self.clean_tag()
        self.graph.nodes.get(id1).weight = 0.0
        queue.put((self.graph.nodes.get(id1).weight, self.graph.nodes.get(id1)))
        while not queue.empty():
            (tempDis, tempNode) = queue.get()
            for i in self.graph.e_dictOfSrc.get(tempNode.id).keys():
                if tempNode.weight + self.graph.e_dictOfSrc[tempNode.id][i].weight < self.graph.nodes.get(i).weight:
                    new_dis = tempNode.weight + self.graph.e_dictOfSrc[tempNode.id][i].weight
                    self.graph.nodes.get(i).weight = new_dis
                    self.graph.nodes.get(i).tag = tempNode.id
                    queue.put((new_dis, self.graph.nodes.get(i)))

        return self.graph.nodes.get(id2).weight

    # restart the tags of all the vertexes to 0
    def clean_tag(self):
        for i in self.graph.nodes.values():
            i.tag = 0

    # restart the info of all the vertexes to ''
    def clean_info(self):
        for i in self.graph.nodes.values():
            i.info = ''

    # this function calculate the tsp problem
    def TSP(self, node_lst: List[int]) -> (List[int], float):
        path = []
        mini = math.inf
        temp_key = -1
        len_path = 0
        temp_node = node_lst.pop(0)
        path.append(temp_node)
        while len(node_lst) > 0:
            for node in node_lst:
                dis = self.diakstra(temp_node, node)
                if mini > dis:
                    mini = dis
                    temp_key = node_lst.index(node)
            temp_node = node_lst.pop(temp_key)
            path.append(temp_node)
            len_path = len_path + mini
            mini = math.inf
        return path, len_path

    # this function calculate the center vertex of the graph
    def centerPoint(self) -> (int, float):
        mini = math.inf
        ind = -1
        for node in self.graph.nodes.keys():
            self.clean_tag()
            self.clean_info()
            if node == 0:
                self.diakstra(node, 1)
            else:
                self.diakstra(node, 0)
            max_short_path = -1 * math.inf
            for other in self.graph.nodes.keys():
                if other == node:
                    continue
                if self.graph.nodes.get(other).weight > max_short_path:
                    max_short_path = self.graph.nodes.get(other).weight
            if mini > max_short_path:
                mini = max_short_path
                ind = node
        return ind, mini

    # this function present the graph with pygame
    def plot_graph(self) -> None:
        pygame.init()
        pygame.font.init()
        self.display()

    # reverse and regular because the function get a dict
    def BFS(self, src_node: Node, dic: {}) -> bool:
        my_queue = [src_node]
        while len(my_queue) > 0:
            node_temp = my_queue.pop()
            for i in self.graph.e_dictOfSrc.get(node_temp).keys():
                if node_temp.info == "white":
                    edge_temp = dic.get(node_temp).i
                    my_queue.append(self.graph.nodes.get(edge_temp.dest))
            node_temp.info = "black"
        for i in self.graph.nodes.keys():
            if self.graph.nodes.get(i).info == "white":
                return False
        return True

    # this function check if the graph is connected
    def isConnect(self) -> bool:
        head = self.graph.nodes.get(0)
        self.clean_tag()
        self.clean_info()
        path = self.BFS(head, self.graph.e_dictOfSrc)
        if not path:
            return False
        path = self.BFS(head, self.graph.e_dictOfDest)
        return path

    # this function display the graph.
    def display(self):
        while True:
            for eve in pygame.event.get():
                if eve.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if eve.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_center.rect.collidepoint(eve.pos):
                        self.button_center.pressed()
                    if self.button_tsp.rect.collidepoint(eve.pos):
                        self.button_tsp.pressed()
                    if self.button_load.rect.collidepoint(eve.pos):
                        self.button_load.pressed()
                    if self.button_save.rect.collidepoint(eve.pos):
                        self.button_save.pressed()
                    if self.button_short.rect.collidepoint(eve.pos):
                        self.button_short.pressed()
            self.draw()
            pygame.display.update()
            self.screen.fill(pygame.Color(255, 250, 250))
            pygame.display.set_caption("Graph")
            self.clock.tick(60)

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

    # this function draw the gui
    def draw(self):
        self.min_x = float(min(list(self.graph.nodes.values()), key=lambda n: n.pos[0]).pos[0])
        self.max_x = float(max(list(self.graph.nodes.values()), key=lambda n: n.pos[0]).pos[0])
        self.min_y = float(min(list(self.graph.nodes.values()), key=lambda n: n.pos[1]).pos[1])
        self.max_y = float(max(list(self.graph.nodes.values()), key=lambda n: n.pos[1]).pos[1])
        pygame.draw.rect(self.screen, self.button_center.color, self.button_center.rect)
        pygame.draw.rect(self.screen, self.button_tsp.color, self.button_tsp.rect)
        pygame.draw.rect(self.screen, self.button_load.color, self.button_load.rect)
        pygame.draw.rect(self.screen, self.button_save.color, self.button_save.rect)
        pygame.draw.rect(self.screen, self.button_short.color, self.button_short.rect)
        if self.button_load.is_pressed:
            button_load_text = self.Font.render(self.button_load.text, True, (0, 250, 250))
            file = easygui.enterbox('enter path of json file:', 'load')
            self.load_from_json(file)
            self.button_load.pressed()
        else:
            button_load_text = self.Font.render(self.button_load.text, True, (0, 0, 0))
        if self.button_save.is_pressed:
            button_save_text = self.Font.render(self.button_save.text, True, (0, 250, 250))
            file = easygui.enterbox('enter a path of a json file:', 'save')
            self.save_to_json(file)
            self.button_save.pressed()
        else:
            button_save_text = self.Font.render(self.button_save.text, True, (0, 0, 0))
        for edge in self.graph.edges.values():
            src = self.graph.nodes.get(edge.src).pos
            dest = self.graph.nodes.get(edge.dest).pos
            src_x = self.scale(src[0], self.margin, self.screen.get_width() - self.margin, self.min_x, self.max_x)
            src_y = self.scale(src[1], self.margin, self.screen.get_height() - self.margin, self.min_y, self.max_y)
            dest_x = self.scale(dest[0], self.margin, self.screen.get_width() - self.margin, self.min_x, self.max_x)
            dest_y = self.scale(dest[1], self.margin, self.screen.get_height() - self.margin, self.min_y, self.max_y)
            if edge.src and edge.dest in self.result:
                self.draw_arrow((src_x, src_y), (dest_x, dest_y), 15, 5, (0, 0, 150))
            else:
                self.draw_arrow((src_x, src_y), (dest_x, dest_y), 15, 5, (0, 0, 0))
        for node in self.graph.nodes.values():
            x = self.scale(node.pos[0], self.margin, self.screen.get_width() - self.margin, self.min_x, self.max_x)
            y = self.scale(node.pos[1], self.margin, self.screen.get_height() - self.margin, self.min_y, self.max_y)
            pygame.draw.circle(self.screen, pygame.Color(255, 128, 0), (x, y), self.r)
            node_text = self.Font.render(str(node.id), True, pygame.Color((0, 0, 244)))
            self.screen.blit(node_text, (x - 8, y - 8))
        if self.button_center.is_pressed:
            button_center_text = self.Font.render(self.button_center.text, True, (0, 250, 250))
            node = self.centerPoint()
            xn = self.scale(self.graph.nodes.get(node[0]).pos[0], self.margin, self.screen.get_width() - self.margin,
                            self.min_x,
                            self.max_x)
            yn = self.scale(self.graph.nodes.get(node[0]).pos[1], self.margin, self.screen.get_height() - self.margin,
                            self.min_y,
                            self.max_y)
            pygame.draw.circle(self.screen, pygame.Color(128, 0, 64), (xn, yn), self.r)
        else:
            button_center_text = self.Font.render(self.button_center.text, True, (0, 0, 0))
        if self.button_tsp.is_pressed:
            button_tsp_text = self.Font.render(self.button_tsp.text, True, (0, 250, 250))
            tsp_l = easygui.enterbox('enter list of node:', 'tsp')
            temp_list = tsp_l.split(",")
            int_list = []
            for i in temp_list:
                int_list.append(int(i))
            easygui.msgbox("the tsp is:" + f'{self.TSP(int_list)}')
            self.button_tsp.pressed()
        else:
            button_tsp_text = self.Font.render(self.button_tsp.text, True, (0, 0, 0))
        if self.button_short.is_pressed:
            button_short_text = self.Font.render(self.button_short.text, True, (0, 250, 250))
            s = easygui.enterbox('choose source node:', 'source node')
            d = easygui.enterbox('choose destintion node:', 'destination node')
            easygui.msgbox('the shoretest path is:' + f'{self.shortest_path(int(s), int(d))}')
            self.button_short.pressed()
        else:
            button_short_text = self.Font.render(self.button_short.text, True, (0, 0, 0))
        self.screen.blit(button_center_text, (self.button_center.rect.x + 10, self.button_center.rect.y))
        self.screen.blit(button_tsp_text, (self.button_tsp.rect.x + 10, self.button_tsp.rect.y))
        self.screen.blit(button_load_text, (self.button_load.rect.x + 10, self.button_load.rect.y))
        self.screen.blit(button_save_text, (self.button_save.rect.x + 10, self.button_save.rect.y))
        self.screen.blit(button_short_text, (self.button_short.rect.x + 10, self.button_short.rect.y))
