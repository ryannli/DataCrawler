import unittest
from model.graph import Graph, Vertex


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.vertex = Vertex("vertex", {"key": "value"})

    def test_add_vertex_edge(self):
        v1 = self.graph.add_actor_vertex("actor1")
        v2 = self.graph.add_actor_vertex("actor2")
        v3 = self.graph.add_actor_vertex("actor3")
        v4 = self.graph.add_movie_vertex("movie1")
        v5 = self.graph.add_movie_vertex("movie2")

        self.graph.add_edge("actor1", "movie1", 3)
        self.graph.add_edge("actor2", "movie1", 4)
        self.graph.add_edge("actor3", "movie2", 5)
        self.graph.add_edge("actor3", "movie3", 6)
        self.graph.add_actor_siblings()

        v1.set_compare_value(3)
        v3.set_compare_value(5)
        v5.set_compare_value(1)
        vertices =[v1, v3, v5]
        vertices.sort()

        self.assertEqual(len(self.graph.get_actor_vertices()), 3)
        self.assertEqual(len(self.graph.get_movie_vertices()), 2)
        self.assertEqual(len(self.graph.get_all_vertices()), 5)
        self.assertEqual(len(self.graph.get_edges()), 3)
        self.assertEqual(vertices[0], v5)
        self.assertEqual(v1.get_compare_value(), 3)

    def test_vertex(self):
        self.vertex.add_neighbor("vertex", 3)
        self.vertex.add_sibling("vertex")

        self.assertEqual(len(self.vertex.get_siblings()), 1)
        self.assertEqual(len(self.vertex.get_neighbors()), 1)
        self.assertEqual(self.vertex.get_content()['key'], "value")
        self.assertEqual(self.vertex.get_name(), "vertex")

        self.vertex.remove_neighbor("vertex")
        self.vertex.remove_sibling("vertex")
        self.assertEqual(len(self.vertex.get_neighbors()), 0)
        self.assertEqual(len(self.vertex.get_siblings()), 0)

if __name__ == "__main__":
    unittest.main()
