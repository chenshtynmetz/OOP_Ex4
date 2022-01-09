import unittest
from DiGraph import DiGraph


# tests of all the function on Digraph class
class MyTestCase(unittest.TestCase):
    g1 = DiGraph()
    g1.add_node(1)
    g1.add_node(2)
    g1.add_node(3)
    g1.add_node(4)
    g1.add_node(5)
    g1.add_edge(1, 2, 2.5)
    g1.add_edge(2, 3, 3)
    g1.add_edge(3, 4, 1.5)
    g1.add_edge(4, 5, 3.5)
    # g1.add_edge(5, 1, 1)
    g1.add_edge(1, 4, 7)
    g1.add_edge(2, 5, 6)

    def test_v_size(self):
        size = len(self.g1.nodes)
        self.assertEqual(size, 5)  # add assertion here

    def test_e_size(self):
        size = 0
        for i in self.g1.e_dictOfSrc:
            size = size + len(self.g1.e_dictOfSrc[i])
        self.assertEqual(size, 6)

    def test_get_mc(self):
        self.assertEqual(11, self.g1.mc)

    def test_get_all_v(self):
        nodeDict = {}
        for i in range(1, len(self.g1.nodes) + 1):
            nodeDict[i] = self.g1.nodes[i]
        # {1: self.g1.nodes[1], 2:self.g1.nodes[2], 3:self.g1.nodes[]}
        self.assertEqual(self.g1.nodes, nodeDict)

    def test_add_node(self):
        # self.g1.add_node(8)
        size = len(self.g1.nodes)
        self.assertEqual(5, size)

    def test_add_edge(self):
        size = 0
        for i in self.g1.e_dictOfSrc:
            size = size + len(self.g1.e_dictOfSrc[i])
        self.assertEqual(6, size)


if __name__ == '__main__':
    unittest.main()
