import os
from flask import Flask, json
from flask import jsonify
from flask import request
from flask import make_response
from flask import Response
from flask import abort
from urllib.parse import unquote

app = Flask(__name__)

ENCODE_STRING = "****"
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "../data", "data.json")
actor_movie_data = json.load(open(json_url, encoding='utf-8'), encoding="utf-8")
actor_data = actor_movie_data[0]
movie_data = actor_movie_data[1]


@app.route('/api/actors', methods=['GET'])
def get_actors():
    """
    Get dict of actors in json format satisfying query statement
    :return: the json of dictionary of actors
    """
    query = request.query_string.decode("utf-8")
    query = unquote(query)
    query = query.replace('"', "")

    query_result = _query_data(actor_data, query)
    return jsonify(query_result)


@app.route('/api/movies', methods=['GET'])
def get_movies():
    """
    Get dict of movies in json format satisfying query statement
    :return: the json of dictionary of movies
    """
    query = request.query_string.decode("utf-8")
    # replace %xx escapes by their single-character equivalent
    query = unquote(query)
    # remove double quotation marks in query string
    query = query.replace('"', "")

    query_result = _query_data(movie_data, query)
    return jsonify(query_result)


@app.route('/api/actors/<string:actor_name>', methods=['GET'])
def get_actor(actor_name):
    """
    Get the actor information according to actor name end
    :param actor_name: the actor name
    :return: the json of dictionary of actor information or abort 404
    """
    # replace "_" with space in query string
    actor_name = actor_name.replace("_", " ")
    if actor_name in actor_data:
        return jsonify(actor_data[actor_name])
    abort(404)


@app.route('/api/movies/<string:movie_name>', methods=['GET'])
def get_movie(movie_name):
    """
    Get the actor information according to movie name end
    :param movie_name: the movie name
    :return: the json of dictionary of movie information or abort 404
    """
    movie_name = movie_name.replace("_", " ")
    if movie_name in movie_data:
        return jsonify(movie_data[movie_name])
    abort(404)


@app.route('/api/actors/<string:actor_name>', methods=['PUT'])
def put_actor(actor_name):
    """
    Update the actor information according to actor name end
    :param actor_name: the actor name
    :return: the json of success information with code 200 or abort 400
    """
    return _put_data(actor_name, actor_data, request.json)


@app.route('/api/movies/<string:movie_name>', methods=['PUT'])
def put_movie(movie_name):
    """
    Update the actor information according to movie name end
    :param movie_name: the movie name
    :return: the json of success information with code 200 or abort 400
    """
    return _put_data(movie_name, movie_data, request.json)


@app.route('/api/actors', methods=['POST'])
def post_actor():
    """
    Post the new actor information
    :return: the json of success information with code 201 or abort 400
    """
    return _post_data(actor_data, request.json)


@app.route('/api/movies', methods=['POST'])
def post_movie():
    """
    Post the new movie information
    :return: the json of success information with code 201 or abort 400
    """
    return _post_data(movie_data, request.json)


@app.route('/api/actors/<string:actor_name>', methods=['DELETE'])
def delete_actor(actor_name):
    """
    Delete the actor according to actor name end
    :param actor_name: the actor name
    :return: the json of success information with code 200 or abort 400
    """
    return _delete_data(actor_data, actor_name)


@app.route('/api/movies/<string:movie_name>', methods=['DELETE'])
def delete_movie(movie_name):
    """
    Delete the actor according to movie name end
    :param movie_name: the movie name
    :return: the json of success information with code 200 or abort 400
    """
    return _delete_data(movie_data, movie_name)


@app.errorhandler(400)
def bad_request(error):
    """
    Error handler for error 400. Make response in json format.
    :param error: the error
    :return: the json response of error
    """
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(error):
    """
    Error handler for error 404. Make response in json format.
    :param error: the error
    :return: the json response of error
    """
    return make_response(jsonify({'error': 'Not Found'}), 404)


def _put_data(name, data, request_json):
    """
    Updates information from request json to backend data's key name
    :param name: the name of key in dict of data
    :param data: the dict of data
    :param request_json: the json request
    :return: the json of success information with code 200 or abort 400
    """
    name = name.replace("_", " ")
    if not request_json or name not in data:
        abort(400)

    for attr in request_json:
        data[name][attr] = request_json[attr]
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def _post_data(data, request_json):
    """
    Post new data from request json to backend data
    :param data: the dict of data
    :param request_json: the json request
    :return: the json of success information with code 201 or abort 400
    """
    if not request_json or 'name' not in request_json:
        abort(400)

    name = request.json['name']
    if name in data:
        # Should use "PUT" method
        abort(400)
    data[name] = request.json

    return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}


def _delete_data(data, name):
    """
    Delete the data according to given name key
    :param data: the dict of data
    :param name: the name key
    :return: the json of success information with code 200 or abort 400
    """
    name = name.replace("_", " ")
    if name not in data:
        abort(400)

    data.pop(name)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def _query_data(data, query):
    """
    Query data according to input query string and additionally deal with boolean AND and OR logics.
    :param data: the dict of backend data
    :param query: the query string
    :return: dict of query result
    """
    # Encode "&" in query attr_values to remove confusion with operator AND. For example, name="Harry & Son"&year=1984
    query = _encode_and(query)
    if "|" in query and "&" in query:
        abort(400)
    AND = False
    if "|" in query:
        query = query.split("|")
    else:
        query = query.split("&")
        AND = True
    query = _decode_and(query)

    candidate_names_all_query = []

    for q in query:
        q = q.split("=")
        q = [entry for entry in q if entry]
        if len(q) != 2:
            # Should have left hand side and right hand side
            abort(400)
        candidate_names = set()
        attr, attr_value = q[0], q[1]
        try:
            attr_value = int(attr_value)
        except:
            pass
        for name in data:
            if attr not in data[name]:
                abort(400)
            if data[name][attr] == attr_value:
                candidate_names.add(name)
            elif attr == 'name' and attr_value in data[name][attr]:
                candidate_names.add(name)
        candidate_names_all_query.append(candidate_names)

    if AND:
        # Gets the intersections between candidates
        candidate_names_all_query = set.intersection(*candidate_names_all_query)
    else:
        # Gets the union between candidates
        candidate_names_all_query = set.union(*candidate_names_all_query)

    return [data[name] for name in candidate_names_all_query]


def _encode_and(string):
    """
    Encode string with " & " and replace with ENCODE_STRING
    :param query: the input string
    :return: the encoded string
    """
    string = string.split(" & ")
    return ENCODE_STRING.join(string)


def _decode_and(query_list):
    """
    Decode list of query strings by replacing ENCODE_STRING with " & "
    :param query_list: the input list of query strings
    :return: the decoded list of strings
    """
    return [query.replace(ENCODE_STRING, " & ") for query in query_list]


if __name__ == "__main__":
    app.run(debug=True)
