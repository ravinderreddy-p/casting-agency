import os
import unittest
from flask import json
from flask_sqlalchemy import SQLAlchemy

from src.api import create_app
from src.database.models import setup_db, Actor, Movie
from src.auth.auth import AuthError, requires_auth


class CastingAgencyTestCase(unittest.TestCase):
    """ This class represents the Casting Agency test cases """
    def setUp(self):
        """ Define test variables and initialize the app """
        self.app = create_app()
        self.client = self.app.test_client

        self.token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik16VTFNMFl3T0RRNE5rUXlOMEV5UWtNNVFrUTRORGxDUkRaR01qWTFSREF6TVRFME0wRXhOdyJ9.eyJpc3MiOiJodHRwczovL3JhdmktZnNuZC5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDA0OTkyNzAyODkxMjE1NjI1NzAiLCJhdWQiOlsiQ29mZmVlIHNob3AiLCJodHRwczovL3JhdmktZnNuZC5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg0MTY5NDc5LCJleHAiOjE1ODQxNzY2NzksImF6cCI6Ikxma3hSZGxlRGllTmpKbXlZRXlEUElSejhYODBKUUd1Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6ZHJpbmtzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDpkcmlua3MiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6ZHJpbmtzIiwicG9zdDptb3ZpZXMiXX0.KxuPTvTpunBMWcX9qLsGWcVVqlactsKoEzKzl2I7j3hIDG3322UkD4qIDclGm9CZuSZCPkKmVLkoHd7-fS3oEKR-uQW5xN2PmNlRq0mvdW4fOqWoHfSYy_Hu1O1Hfw6efVpouM3hhZW5TYeWOe1vWfDKfbyvKXgY4CIDUg5j3KpSFdmTiVHX5qGUogWAg2uRUFEv4BBt2FzUVraCRJBXz1ymHfmJG8V75wY6mgy5-okF6pVtDD3NiucWeglXKaF1gIRs0b-DIiP9oO44W2RfZCz6Qz1kYNk1MKAPgZCgvGhogfq_-dteVNPN9U3tFB-kzDDQSgzl-y5DpC9gMVBLMw'

        self.database_name = 'cast_agency_test'
        self.database_path = 'postgres://{}/{}'.format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.add_actor = {
            'name': 'Kamal',
            'age': 55,
            'gender': 'M'
        }

        self.add_movie = {
            'name': 'Indian2',
            'release_date': '2020-12-12'
        }

        self.update_movie = {
            'name': 'India-2'
        }

        self.update_actor = {
            'name': 'Kamal Hasan'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()


    def tearDown(self):
        """Execute after each test"""
        pass

    def test_get_actors(self):
        actors = "/actors"
        res = self.client().get(f'{actors}',
                                headers={
                                    "Authorization":
                                        "Bearer {}".format(self.token)
                                        }
                                )
        data = json.loads(res.data)

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found')

        else:
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['name'])
            self.assertTrue(data['age'])
            self.assertTrue(data['gender'])

    def test_get_movies(self):
        movies = "/movies"
        res = self.client().get(f'{movies}',
                                headers={
                                    "Authorization":
                                        "Bearer {}".format(self.token)
                                        })
        data = json.loads(res.data)

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found')

        else:
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['name'])
            self.assertTrue(data['release_date'])

    def test_delete_actor(self):
        actor_id = 2
        res = self.client().delete(f'/actors/{actor_id}',
                                headers={
                                    "Authorization":
                                        "Bearer {}".format(self.token)
                                        })
        data = json.loads(res.data)

        if res.status_code == 405:
            self.assertEqual(res.status_code, 405)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'method not allowed')

        else:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)

    def test_delete_movies(self):
        movie_id = 2
        res = self.client().delete(f'/actors/{movie_id}',
                                headers={
                                    "Authorization":
                                        "Bearer {}".format(self.token)
                                        })
        data = json.loads(res.data)

        if res.status_code == 405:
            self.assertEqual(res.status_code, 405)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'method not allowed')

        else:
            actor = Actor.query.filter(Actor.id == movie_id).one_or_none()
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)

    def test_add_actor(self):
        res = self.client().post('/actors', data=json.dumps(self.add_actor), content_type='application/json',
                                headers={
                                    "Authorization":
                                        "Bearer {}".format(self.token)
                                        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_movie(self):
        res = self.client().post('/movies', data=json.dumps(self.add_movie), content_type='application/json',
                                headers={
                                    "Authorization":
                                        "Bearer {}".format(self.token)
                                        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_movie(self):
        id = 1
        res = self.client().patch(f'/movies/{id}', data=json.dumps(self.update_movie), content_type='application/json',
                                headers={
                                    "Authorization":
                                        "Bearer {}".format(self.token)
                                        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_actor(self):
        id = 6
        res = self.client().patch(f'/actors/{id}', data=json.dumps(self.update_actor), content_type='application/json',
                                headers={
                                    "Authorization":
                                        "Bearer {}".format(self.token)
                                        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_delete_actor(self):
        actor_id = 100
        res = self.client().delete(f'/actors/{actor_id}',
                                headers={
                                    "Authorization":
                                        "Bearer {}".format(self.token)
                                        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')


if __name__ == "__main__":
    unittest.main()
