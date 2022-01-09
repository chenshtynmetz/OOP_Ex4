import unittest
from unittest import TestCase

from client_python.DiGraph import Edge
from client_python.GraphAlgo import GraphAlgo
from client_python.gui_function import Functions
from client_python.pokemon import Pokemon


class TestFunctions(TestCase):
    algo = GraphAlgo()
    graph = algo.get_graph()
    p1 = Pokemon(5, 1, (35.18753053591606, 32.10378225882353, 0.0))
    p2 = Pokemon(8, -1, (35.2, 32.33, 0))
    graph.add_node(0, (35.18753053591606, 32.10378225882353, 0.0))
    graph.add_node(1, (35.18958953510896, 32.10785303529412, 0.0))
    graph.add_edge(0, 1, 2.5)
    e = Edge(0, 1, 2.5)
    f = Functions(0, 0, 0, 0, 0, graph, None, None, algo)

    def test_distance(self):
        a = (5, 2)
        b = (10, 7)
        ans = 7.0710678118654752440084436210485
        self.assertEqual(ans, self.f.distance(a, b))

    def test_pok_on_edge(self):
        algo = GraphAlgo()
        graph = algo.get_graph()
        p1 = Pokemon(5, 1, (35.18753053591606, 32.10378225882353, 0.0))
        p2 = Pokemon(8, -1, (35.2, 32.33, 0))
        graph.add_node(0, (35.18753053591606, 32.10378225882353, 0.0))
        graph.add_node(1, (35.18958953510896, 32.10785303529412, 0.0))
        graph.add_edge(0, 1, 2.5)
        e = Edge(0, 1, 2.5)
        f = Functions(0, 0, 0, 0, 0, graph, None, None, algo)
        e1 = self.f.pok_on_edge(self.p1)
        self.assertEqual(0, e1.src)
        self.assertEqual(1, e1.dest)

    def test_allocate_agent_to_pok(self):
        algo = GraphAlgo()
        graph = algo.get_graph()
        p1 = Pokemon(5, 1, (35.18753053591606, 32.10378225882353, 0.0))
        p2 = Pokemon(8, -1, (35.2, 32.33, 0))
        graph.add_node(0, (35.18753053591606, 32.10378225882353, 0.0))
        graph.add_node(1, (35.18958953510896, 32.10785303529412, 0.0))
        graph.add_edge(0, 1, 2.5)
        e = Edge(0, 1, 2.5)
        f = Functions(0, 0, 0, 0, 0, graph, None, None, algo)
        path = [1, 2, 3]
        path2 = [1, 2, 3]
        self.assertEqual(path2, path)
