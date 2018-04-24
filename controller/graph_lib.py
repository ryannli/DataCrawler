from inspect import getsourcefile
import os.path as path, sys

# enable import from other module directories
current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

import json
from model.graph import *
from controller.query_utils import *
from controller.analysis_utils import *

DATA_ANALYSIS = True
ACTOR_MOVIE_FILE_PATH = '../data/data.json' # The json data path
QUERY_LIST = '\nPlease input the number corresponding to the query you want\n\
			1. Find how much a movie has grossed\n \
			2. List which movies an actor has worked in\n \
			3. List which actors worked in a movie\n \
			4. List the top X actors with the most total grossing value\n \
			5. List the oldest X actors\n \
			6. List all the movies for a given year\n \
			7. List all the actors for a given year\n \
			8. List all movies for a given language\n \
			9. List all movies for a given country\n'

def add_edges(graph):
    actor_vertices = graph.get_actor_vertices()
    for actor_name in actor_vertices:
        content = actor_vertices[actor_name].get_content()
        for movie_name in content['movies']:
            weight = content['age']
            graph.add_edge(actor=actor_name, movie=movie_name, weight=weight)

    # Ensure each actor vertex has movie neighbors
    movie_vertices = graph.get_movie_vertices()
    for movie_name in movie_vertices:
        content = movie_vertices[movie_name].get_content()
        for actor_name in content['actors']:
            if actor_name in actor_vertices:
                weight = (actor_vertices[actor_name].get_content())['age']
                graph.add_edge(actor=actor_name, movie=movie_name, weight=weight)

    return graph

def construct_graph(actor_data, movie_data):
    """
    Construct a graph class from actor data and movie data
    :param actor_data: dict of actor names and actor information
    :param movie_data: dict of movie names and movie information
    :return: constructed graph
    """
    graph = Graph()
    for actor in actor_data:
        graph.add_actor_vertex(actor, actor_data[actor])

    for movie in movie_data:
        graph.add_movie_vertex(movie, movie_data[movie])

    return add_edges(graph)


def construct_graph_single(actor_movie_data):
    """
    Construct a graph class from actor data and movie data from a given format
    :param actor_movie_data: dict of actor information and movie information
    :return: constructed graph
    """
    graph = Graph()
    actor_data, movie_data = actor_movie_data[0], actor_movie_data[1]

    for entry in actor_data:
        content = actor_data[entry]
        content.pop("json_class")
        graph.add_actor_vertex(content["name"], content)

    for entry in movie_data:
        content = movie_data[entry]
        content.pop("json_class")
        content['url'] = content.pop('wiki_page')
        content['gross'] = content.pop('box_office')
        graph.add_movie_vertex(content["name"], content)

    graph = add_edges(graph)
    graph.add_actor_siblings()
    return graph


def start_query(graph):
    """
    Create interaction with user queries
    :param graph: the graph class
    """
    while 1:
        try:
            query = input(QUERY_LIST)
            if query == "quit":
                break
            query_num = int(query)
            if 1 <= query_num <= 9:
                if query_num == 1:
                    query_movie_gross(graph)
                elif query_num == 2:
                    query_actor_movies(graph)
                elif query_num == 3:
                    query_movie_actors(graph)
                elif query_num == 4:
                    query_actor_top_grossing(graph)
                elif query_num == 5:
                    query_actor_oldest(graph)
                elif query_num == 6:
                    query_movies_given_year(graph)
                elif query_num == 7:
                    query_actors_given_year(graph)
                elif query_num == 8:
                    query_language_movies(graph)
                elif query_num == 9:
                    query_country_movies(graph)

        except KeyboardInterrupt:
            exit(0)
        except ValueError:
            print("Please input a legal number!")


def start_data_analysis(graph):
    """
    Create and save different data analysis
    :param graph: the input graph
    """
    hub_actors(graph)
    grossing_vs_age(graph)
    movie_year_percentage(graph)


if __name__ == "__main__":
    with open(ACTOR_MOVIE_FILE_PATH, encoding='utf-8') as data_file:
        actor_movie_data = json.load(data_file)

    graph = construct_graph_single(actor_movie_data)
    if DATA_ANALYSIS:
        start_data_analysis(graph)
    else:
        start_query(graph)
