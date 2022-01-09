import unittest
from GraphAlgo import GraphAlgo
from DiGraph import DiGraph


# tests of all the algorithms
class MyTestCase(unittest.TestCase):

    def test_load_from_json(self):
        graphAlgo = GraphAlgo(DiGraph())
        self.assertFalse(graphAlgo.load_from_json("somthing.json"))


    def test_save_from_json(self):
        graphAlgo = GraphAlgo(DiGraph())
        graphAlgo.load_from_json("../data/A0.json")
        self.assertTrue(graphAlgo.save_to_json("temp.json"))

    def test_shortest_path(self):
        graphAlgo = GraphAlgo(DiGraph())
        graphAlgo.graph.add_node(0)
        graphAlgo.graph.add_node(1)
        graphAlgo.graph.add_node(2)
        graphAlgo.graph.add_edge(0, 1, 1)
        graphAlgo.graph.add_edge(1, 2, 4)
        self.assertEqual(graphAlgo.shortest_path(0, 1), (1.0, [0, 1]))
        self.assertEqual(graphAlgo.shortest_path(0, 2), (5.0, [0, 1, 2]))
        graphAlgo.graph.remove_node(1)
        self.assertEqual(graphAlgo.shortest_path(0, 2), (5.0, [0, 1, 2]))

    def test_centerPoint(self):
        graphAlgo1 = GraphAlgo(DiGraph())
        graphAlgo1.load_from_json("../data/A0.json")
        x = graphAlgo1.centerPoint()
        print(x)
        graphAlgo2 = GraphAlgo(DiGraph())
        graphAlgo2.load_from_json("../data/A1.json")
        y = graphAlgo2.centerPoint()
        print(y)
        graphAlgo3 = GraphAlgo(DiGraph())
        graphAlgo3.load_from_json("/data/A2.json")
        graphAlgo4 = GraphAlgo(DiGraph())
        graphAlgo4.load_from_json("/data/A3.json")


    def test_TSP(self):
        g = DiGraph()
        g.add_node(1)
        g.add_node(2)
        g.add_node(3)
        g.add_node(4)
        g.add_node(5)
        g.add_edge(1, 2, 3)
        g.add_edge(1, 3, 5)
        g.add_edge(3, 2, 4)
        g.add_edge(2, 5, 7)
        g.add_edge(4, 1, 3)
        g.add_edge(5, 2, 4)
        g.add_edge(3, 1, 9)
        g.add_edge(3, 4, 2)
        g.add_edge(5, 1, 2)
        alg = GraphAlgo(g)
        cities = [3, 5, 1, 2]
        ans = alg.TSP(cities)
        self.assertEqual(ans, ([3, 2, 5, 1], 13.0))


if __name__ == '__main__':
    unittest.main()
