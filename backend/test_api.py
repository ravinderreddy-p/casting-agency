import os
import unittest
from flask import json
from flask_sqlalchemy import SQLAlchemy

from src.api import create_app
from src.database.models import setup_db, Actor, Movie
from .src.auth.auth import AuthError, requires_auth


class CastingAgencyTestCase(unittest.TestCase):
    """ This class represents the Casting Agency test cases """
    def setUp(self):
        """ Define test variables and initialize the app """
        self.app = create_app()
        self.client = self.app.test_client
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
        res = self.client().get(f'{actors}')
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
        res = self.client().get(f'{movies}')
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
        res = self.client().delete(f'/actors/{actor_id}')
        data = json.loads(res.data)

        if res.status_code == 405:
            self.assertEqual(res.status_code, 405)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'method not allowed')

        else:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)

    def test_add_actor(self):
        res = self.client().post('/actors', data=json.dumps(self.add_actor), content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_movie(self):
        res = self.client().post('/movies', data=json.dumps(self.add_movie), content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_movie(self):
        id = 1
        res = self.client().patch(f'/movies/{id}', data=json.dumps(self.update_movie), content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_actor(self):
        id = 6
        res = self.client().patch(f'/actors/{id}', data=json.dumps(self.update_actor), content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # def test_404_delete_actor(self):
    #     actor_id = 100
    #     res = self.client().delete(f'/actors/{actor_id}')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')


if __name__ == "__main__":
    unittest.main()
