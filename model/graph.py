# Referenced from http://www.bogotobogo.com/python/python_graph_data_structures.php

class Vertex:
    """
    The vertex class
    """

    def __init__(self, name, content):
        """
        Initialize a new vertex with vertex name and content
        :param name: the vertex name
        :param content: vertex content
        """
        self.name = name
        self.content = content
        self.neighbors = dict()
        self.siblings = set()
        self.value_for_sort = None

    def add_neighbor(self, vertex_name, weight):
        """
        Adds a vertex as neighbor with a weight
        :param vertex_name: the vertex name of the added neighbor
        :param weight: the weight between two vertices
        """
        self.neighbors[vertex_name] = weight

    def remove_neighbor(self, vertex_name):
        """
        Removes a neighbor of the vertex
        :param vertex_name: the vertex name to remove
        """
        if vertex_name in self.neighbors:
            self.neighbors.pop(vertex_name)

    def get_neighbors(self):
        """
        Gets all neighbors of the vertex
        :return: the dict of neighbors
        """
        return self.neighbors

    def add_sibling(self, vertex_name):
        self.siblings.add(vertex_name)

    def remove_sibling(self, vertex_name):
        self.siblings.remove(vertex_name)

    def get_siblings(self):
        return self.siblings

    def get_content(self):
        """
        Gets the content of vertex
        :return: the content of vertex
        """
        return self.content

    def get_name(self):
        """
        Gets the name of vertex
        :return: the name of vertex
        """
        return self.name

    def set_compare_value(self, value):
        """
        Sets comparable value of the vertex
        :param value: the value to set
        """
        self.value_for_sort = value

    def get_compare_value(self):
        """
        Gets the comparable value of the vertex
        :return: the value
        """
        return self.value_for_sort

    def __lt__(self, other):
        """
        The compare function
        :param other: another vertex
        :return: if the comparable value of current vertex is less than another vertex
        """
        return self.value_for_sort < other.value_for_sort


class Graph:
    """
    The graph class to hold vertices
    """

    def __init__(self):
        """
        Initialize a graph
        """
        self.movie_vertices = dict()
        self.actor_vertices = dict()
        self.edges = set()

    def add_movie_vertex(self, name, content=None):
        """
        Adds a movie vertex
        :param name: the name of movie vertex
        :param content: the content of movie vertex
        :return: the added vertex
        """
        vertex = Vertex(name, content)
        self.movie_vertices[name] = vertex
        return vertex

    def add_actor_vertex(self, name, content=None):
        """
        Adds an actor vertex
        :param name: the name of actor vertex
        :param content: the content of actor vertex
        :return: the added vertex
        """
        vertex = Vertex(name, content)
        self.actor_vertices[name] = vertex
        return vertex

    def add_edge(self, actor, movie, weight):
        """
        Adds an edge between actor and movie vertices
        :param actor: the actor vertex
        :param movie: the movie vertex
        :param weight: the weight of edge
        """
        if movie not in self.movie_vertices or actor not in self.actor_vertices:
            return

        self.actor_vertices[actor].add_neighbor(movie, weight)
        self.movie_vertices[movie].add_neighbor(actor, weight)
        self.edges.add((actor, movie, weight))

    def get_actor_vertices(self):
        """
        Gets all actor vertices
        :return: the dict of actor vertices
        """
        return self.actor_vertices

    def get_movie_vertices(self):
        """
        Gets all movie vertices
        :return: the dict of movie vertices
        """
        return self.movie_vertices

    def get_all_vertices(self):
        """
        Gets all vertices in graph
        :return: the dict of all vertices
        """
        ret = {}
        ret.update(self.actor_vertices)
        ret.update(self.movie_vertices)
        return ret

    def get_edges(self):
        """
        Gets all edges in graph
        :return: the set of all edges
        """
        return self.edges

    def add_actor_siblings(self):
        """
        Add actor siblings which has any common neighbor with current vertex
        """
        for actor_1 in self.actor_vertices:
            for actor_2 in self.actor_vertices:
                if actor_1 != actor_2 \
                        and actor_2 not in self.actor_vertices[actor_1].get_siblings() \
                        and len(set(self.actor_vertices[actor_1].get_neighbors())
                                & set(self.actor_vertices[actor_2].get_neighbors())) > 0:
                    self.actor_vertices[actor_1].add_sibling(actor_2)
                    self.actor_vertices[actor_2].add_sibling(actor_1)
