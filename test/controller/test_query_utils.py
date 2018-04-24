import unittest
from contextlib import contextmanager
import controller.query_utils as query
import controller.graph_lib as graphlib
from model.graph import Graph
from unittest.mock import patch

class TestGraphLib(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        v1 = self.graph.add_actor_vertex("actor1", {'age':38})
        v2 = self.graph.add_actor_vertex("actor2", {'age':26})
        v3 = self.graph.add_actor_vertex("actor3", {'age':10})
        v4 = self.graph.add_movie_vertex("movie1", {'year':2017, 'gross':17000, 'lang': ["English"]})
        v5 = self.graph.add_movie_vertex("movie2", {'year':2017, 'gross':170000, 'country': ["China"]})

        self.graph.add_edge("actor1", "movie1", 3)
        self.graph.add_edge("actor2", "movie1", 4)
        self.graph.add_edge("actor3", "movie2", 5)
        self.graph.add_edge("actor3", "movie3", 6)

    @patch('builtins.input', lambda x: '2017')
    def test_query_actors_given_year(self):
        self.assertEqual(query.query_actors_given_year(self.graph), ["actor1", "actor2", "actor3"])

    @patch('builtins.input', lambda x: 'illegal')
    def test_query_actors_given_year_illegal(self):
        self.assertEqual(query.query_actors_given_year(self.graph), None)

    @patch('builtins.input', lambda x: 'movie1')
    def test_query_movie_gross(self):
        self.assertEqual(query.query_movie_gross(self.graph), "$17.0 thousand")

    @patch('builtins.input', lambda x: 'illegal')
    def test_query_movie_gross_illegal(self):
        self.assertEqual(query.query_movie_gross(self.graph), None)

    @patch('builtins.input', lambda x: 'actor1')
    def test_query_actor_movies(self):
        self.assertEqual(query.query_actor_movies(self.graph), "movie1")

    @patch('builtins.input', lambda x: 'illegal')
    def test_query_actor_movies_illegal(self):
        self.assertEqual(query.query_actor_movies(self.graph), None)

    @patch('builtins.input', lambda x: 'movie1')
    def test_query_movie_actors(self):
        self.assertEqual(query.query_movie_actors(self.graph), "actor1, actor2")

    @patch('builtins.input', lambda x: 'illegal')
    def test_query_movie_actors_illegal(self):
        self.assertEqual(query.query_movie_actors(self.graph), None)

    @patch('builtins.input', lambda x: '2')
    def test_query_actor_top_grossing(self):
        self.assertEqual(query.query_actor_top_grossing(self.graph), ['$170.0 thousand', '$17.0 thousand'])

    @patch('builtins.input', lambda x: '10')
    def test_query_actor_top_grossing_more(self):
        self.assertEqual(query.query_actor_top_grossing(self.graph), ['$170.0 thousand', '$17.0 thousand', '$17.0 thousand'])

    @patch('builtins.input', lambda x: 'illegal')
    def test_query_actor_top_grossing_illegal(self):
        self.assertEqual(query.query_actor_top_grossing(self.graph), None)

    @patch('builtins.input', lambda x: '2')
    def test_query_actor_oldest(self):
        self.assertEqual(query.query_actor_oldest(self.graph), [38, 26])

    @patch('builtins.input', lambda x: 'illegal')
    def test_query_actor_oldest_illegal(self):
        self.assertEqual(query.query_actor_oldest(self.graph), None)

    @patch('builtins.input', lambda x: '2017')
    def test_query_movies_given_year(self):
        self.assertEqual(query.query_movies_given_year(self.graph), ["movie1", "movie2"])

    @patch('builtins.input', lambda x: 'illegal')
    def test_query_movies_given_year_illegal(self):
        self.assertEqual(query.query_movies_given_year(self.graph), None)

    @patch('builtins.input', lambda x: 'English')
    def test_query_language_movies(self):
        self.assertEqual(query.query_language_movies(self.graph), ["movie1"])

    @patch('builtins.input', lambda x: 'illegal')
    def test_query_language_movies_illegal(self):
        self.assertEqual(query.query_language_movies(self.graph), None)

    @patch('builtins.input', lambda x: 'China')
    def test_query_country_movies(self):
        self.assertEqual(query.query_country_movies(self.graph), ["movie2"])

    @patch('builtins.input', lambda x: 'illegal')
    def test_query_country_movies_illegal(self):
        self.assertEqual(query.query_country_movies(self.graph), None)
