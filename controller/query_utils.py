import traceback
import operator
from model.utils import get_readable_string_from_int


def query_movie_gross(graph):
    """
    Query a movie's gross (box office)
    :param graph: the graph class
    :return: the gross value
    """
    query_movie = input("Please input a movie title\n").strip()
    try:
        result = get_readable_string_from_int((graph.get_movie_vertices())[query_movie].get_content()['gross'])
        print("The gross value is " + result + "\n")
        return result
    except:
        print("Sorry the movie is not in database. Please try another one :)\n")


def query_actor_movies(graph):
    """
    Query actor's movies
    :param graph: the graph class
    :return: the string of all movies the actor participates in
    """
    query_actor = input("Please input an actor/actress name\n").strip()
    try:
        result = ", ".join(list((graph.get_actor_vertices())[query_actor].get_neighbors().keys()))
        print("The movies of this actor/actress are " + result + "\n")
        return result
    except:
        print("Sorry the actor is not in database. Please try another one :)\n")


def query_movie_actors(graph):
    """
    Query movie's starring actors
    :param graph: the graph class
    :return: the string of all actors the movie contains
    """
    query_movie = input("Please input an movie title\n").strip()
    try:
        result = ", ".join(list((graph.get_movie_vertices())[query_movie].get_neighbors().keys()))
        print("The actors/actresses of this movie are " + result + "\n")
        return result
    except:
        print("Sorry the movie is not in database. Please try another one :)\n")


def query_actor_top_grossing(graph):
    """
    Query grossing of top actors (box office)
    :param graph: the graph class
    :return: the list of top grossing
    """
    query_number = input("Please input the number of top grossings of actors you expect\n").strip()
    try:
        print("The top %d actor grossings are:" % (int(query_number)))
        actor_vertices = graph.get_actor_vertices()
        result_list = []
        for entry in get_actors_top_k_grossing(graph, int(query_number)):
            result = get_readable_string_from_int(actor_vertices[entry[0]].get_compare_value())
            result_list.append(result)
            print("The grossing for " + entry[0] + " is " + result)
        print()
        return result_list
    except:
        traceback.print_exc()
        print("Please input an legal integer for grossing :)\n")


def query_actor_oldest(graph):
    """
    Query oldest actors
    :param graph: the graph class
    :return: the list of ages
    """
    query_number = input("Please input the number of oldest actors you expect\n").strip()
    try:
        print("The oldest %d actors are:" % (int(query_number)))
        actor_vertices = graph.get_actor_vertices()
        result_list = []
        for entry in get_actors_oldest_k(graph, int(query_number)):
            result = actor_vertices[entry[0]].get_compare_value()
            result_list.append(result)
            print("Age for " + entry[0] + " is " + str(result))
        print()
        return result_list
    except:
        print("Please input an legal integer for oldest actors :)\n")


def query_movies_given_year(graph):
    """
    Query movies in a year
    :param graph: the graph class
    :return: the list of movies
    """
    query_number = input("Please input the year you expect\n").strip()
    try:
        print("The movies for year %d are:" % (int(query_number)))
        ret_list = []
        movie_vertices = graph.get_movie_vertices()
        for movie_name in movie_vertices:
            if (movie_vertices[movie_name].get_content())['year'] == int(query_number):
                ret_list.append(movie_name)
        print(", ".join(ret_list))
        print()
        return ret_list
    except:
        print("Integer is illegal or the year is not in dataset :)\n")


def query_actors_given_year(graph):
    """
    Query actors in a year
    :param graph: the graph class
    :return: the list of actors
    """
    query_number = input("Please input the year you expect\n").strip()
    try:
        print("The actors for year %d are:" % (int(query_number)))
        ret_list = []
        actor_vertices = graph.get_actor_vertices()
        movie_vertices = graph.get_movie_vertices()
        for actor_name in actor_vertices:
            movies = actor_vertices[actor_name].get_neighbors()
            if any((movie_vertices[movie_name].get_content())['year'] == int(query_number) for movie_name in movies):
                ret_list.append(actor_name)
        print(", ".join(ret_list))
        print()
        return ret_list
    except:
        print("Integer is illegal or the year is not in dataset :)\n")


def query_language_movies(graph):
    """
    Query movies in a language
    :param graph: the graph class
    :return: the list of movies
    """
    query_language = input("Please input the language you expect\n").strip()
    ret_list = []
    movie_vertices = graph.get_movie_vertices()
    for movie_name in movie_vertices:
        try:
            # Some movies may not have key "lang"
            if query_language in (movie_vertices[movie_name].get_content()['lang']):
                ret_list.append(movie_name)
        except KeyError:
            pass
    if len(ret_list) == 0:
        print("Sorry we do not have language %s in dataset" % query_language)
    else:
        print("The movies of language %s are" % query_language)
        print(", ".join(ret_list))
        return ret_list


def query_country_movies(graph):
    """
    Query movies produced by a country
    :param graph: the graph class
    :return: the list of movies
    """
    query_country = input("Please input the country you expect\n").strip()
    ret_list = []
    movie_vertices = graph.get_movie_vertices()
    for movie_name in movie_vertices:
        try:
            # Some movies may not have key "country"
            if query_country in (movie_vertices[movie_name].get_content()['country']):
                ret_list.append(movie_name)
        except KeyError:
            pass
    if len(ret_list) == 0:
        print("Sorry we do not have country %s in dataset" % query_country)
    else:
        print("The movies of country %s are" % query_country)
        print(", ".join(ret_list))
        return ret_list


def get_actors_top_k_grossing(graph, k):
    """
    Get actor names of top k grossing
    :param graph: the graph class
    :param k: the integer for length of return list
    :return: the list of actor names with top k grossing
    """
    actor_vertices = graph.get_actor_vertices()
    movie_vertices = graph.get_movie_vertices()
    for actor in actor_vertices:
        total_grossing = sum([(movie_vertices[movie].get_content())['gross'] \
                              for movie in actor_vertices[actor].get_neighbors()])
        actor_vertices[actor].set_compare_value(total_grossing)
    sorted_x = sorted(actor_vertices.items(), key=operator.itemgetter(1))
    if k > len(sorted_x):
        return sorted_x[::-1]
    return sorted_x[:-(k + 1):-1]


def get_actors_oldest_k(graph, k):
    """
    Get actor names of oldest k
    :param graph: the graph class
    :param k: the integer for length of return list
    :return: the list of actor names of k oldest
    """
    actor_vertices = graph.get_actor_vertices()
    for actor in actor_vertices:
        age = (actor_vertices[actor].get_content())['age']
        actor_vertices[actor].set_compare_value(age)
    sorted_x = sorted(actor_vertices.items(), key=operator.itemgetter(1))
    return sorted_x[:-(k + 1):-1]
