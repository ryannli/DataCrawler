from controller.api import *
from controller.graph_lib import construct_graph
from flask_testing import TestCase
import unittest
from flask import Flask
import json


class TestAPI(TestCase):
    def create_app(self):
        return app

    def test_get_actor_query(self):
        response = self.client.get('/api/actors?name="Bruce"&age=10')
        self.assertEqual(response.status_code, 200)

    def test_get_actor_query_illegal(self):
        response = self.client.get('/api/actors?name="Bruce"&age=10|age=20')
        self.assertEqual(response.status_code, 400)

    def test_get_movie_query(self):
        response = self.client.get('/api/movies?name="The Kid"|year=2011')
        self.assertEqual(response.status_code, 200)

    def test_get_movie_query_illegal(self):
        response = self.client.get('/api/movies?name="The Kid"|year=')
        self.assertEqual(response.status_code, 400)

    def test_get_movie_query_illegal_2(self):
        response = self.client.get('/api/movies?name="The Kid"|years=2011')
        self.assertEqual(response.status_code, 400)

    def test_get_actor(self):
        response = self.client.get('/api/actors/Peter_Gallagher')
        self.assertEqual(response.status_code, 200)

    def test_get_actor_illegal(self):
        response = self.client.get('/api/actors/Billy_Bathgates')
        self.assertEqual(response.status_code, 404)

    def test_get_movie(self):
        response = self.client.get('/api/movies/The_Kid')
        self.assertEqual(response.status_code, 200)

    def test_get_movie_illegal(self):
        response = self.client.get('/api/movies/The_Kids')
        self.assertEqual(response.status_code, 404)

    def test_post_actors_invalid(self):
        response = self.client.post('/api/actors',
                                    data="invalid string!")
        self.assertEqual(response.status_code, 400)

    def test_post_actors(self):
        response = self.client.post('/api/actors',
                                    data=json.dumps({"name": "New Name"}), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_post_movies_invalid(self):
        response = self.client.post('/api/movies',
                                    data="invalid string")
        self.assertEqual(response.status_code, 400)

    def test_post_movies_invalid_2(self):
        response = self.client.post('/api/movies',
                                   data=json.dumps({"name": "Chairman of the Board"}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_movies(self):
        response = self.client.post('/api/movies',
                                    data=json.dumps({"name": "New Movie"}), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_put_movies(self):
        response = self.client.put('/api/movies/Passed_Away',
                                   data=json.dumps({"box_office": 4000}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_movies_illegal(self):
        response = self.client.put('/api/movies/Passed_Away_illegal',
                                   data=json.dumps({"box_office": 4000}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_actors(self):
        response = self.client.put('/api/actors/Whoopi_Goldberg',
                                   data=json.dumps({"age": 81}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_actors_illegal(self):
        response = self.client.put('/api/actors/Whoopi_Goldberg_illegal',
                                   data=json.dumps({"age": 81}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_actors(self):
        response = self.client.delete('/api/actors/Cynthia_Stevenson')
        self.assertEqual(response.status_code, 200)

    def test_delete_actors_illegal(self):
        response = self.client.delete('/api/actors/Cynthia_Stevenson2')
        self.assertEqual(response.status_code, 400)

    def test_delete_movies(self):
        response = self.client.delete('/api/movies/Ed')
        self.assertEqual(response.status_code, 200)

    def test_delete_movies_illegal(self):
        response = self.client.delete('/api/movies/Ed2')
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
