from controller.analysis_utils import *
from controller.graph_lib import construct_graph
import unittest


class TestAnalysisUtils(unittest.TestCase):
    def setUp(self):
        actor_data = {"Morgan Freeman": {
            "url": "https://en.wikipedia.org/wiki/Morgan_Freeman",
            "movies": [
                "Momentum",
                "Ted 2",
                "London Has Fallen",
                "Now You See Me 2",
                "Going In Style"
            ],
            "age": 80,
            "total_gross": 300,
        },
            "John Slattery": {
                "url": "https://en.wikipedia.org/wiki/John_Slattery",
                "movies": [
                    "Ted 2",
                    "Ant-Man",
                    "Spotlight",
                    "Captain America: Civil War",
                    "Going In Style"
                ],
                "age": 55,
                "total_gross": 400,
            }}
        movie_data = {"Going In Style": {
            "country": [
                "United States"
            ],
            "lang": [
                "English"
            ],
            "gross": 84900000.0,
            "actors": [
                "Morgan Freeman",
                "Michael Caine",
                "Alan Arkin",
                "Joey King",
                "John Slattery"
            ],
            "url": "https://en.wikipedia.org/wiki/Going_in_Style_(2017_film)",
            "year": 2017
        },
            "Now You See Me 2": {
                "country": [
                    "United States"
                ],
                "lang": [
                    "English"
                ],
                "gross": 334900000.0,
                "actors": [
                    "Jesse Eisenberg",
                    "Mark Ruffalo",
                    "Woody Harrelson",
                    "Dave Franco",
                    "Daniel Radcliffe"
                ],
                "url": "https://en.wikipedia.org/wiki/Now_You_See_Me_2",
                "year": 2016
            }}
        self.graph = construct_graph(actor_data, movie_data)
        self.graph.add_actor_siblings()

    def test_hub_actors(self):
        self.assertEqual(hub_actors(self.graph, number=2, save_fig=False)[0][1], 1)

    def test_grossing_vs_age(self):
        grossing_vs_age(self.graph, save_fig=False)

    def test_movie_year_percentage(self):
        movie_year_percentage(self.graph, save_fig=False)

if __name__ == "__main__":
    unittest.main()