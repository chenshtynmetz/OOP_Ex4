import unittest
from unittest import TestCase

from client_python.DiGraph import Edge
from client_python.GraphAlgo import GraphAlgo
from client_python.client import Client
from client_python.gui_function import Functions
from client_python.pokemon import Pokemon


class TestFunctions(TestCase):
    c = Client()
    algo = GraphAlgo()
    algo.load_from_json("/data/A0")
    graph = algo.get_graph()
    f = Functions(0, 0, 0, 0, 0, graph, None, c, None, algo)


    def test_distance(self):
        a = (5, 2)
        b = (10, 7)
        ans = 7.0710678118654752440084436210485
        self.assertEqual(ans, self.f.distance(a, b))

    def test_pok_on_edge(self):
        p = Pokemon(5, -1, (35.197656770719604, 32.10191878639921, 0.0))
        e1 = self.f.pok_on_edge(p)
        e = Edge(9, 8, 8.8888)
        self.assertEqual(e.src, e1.src)
        self.assertEqual(e.dest, e1.dest)


    # def test_allocate_agent_to_pok(self):


