import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import db, Actor, Movie
from pathlib import Path
from dotenv import load_dotenv

env_path_test = Path('.', '.env')
load_dotenv(dotenv_path=env_path_test)

# Variables for database testing
DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'lawpal86')
DB_NAME = os.getenv('DB_NAME', 'agency')
database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

''' Sets up database for testing '''


def setup_db_test(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


TOKEN = os.getenv('TOKEN')


class AgencyTest(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json'}
        self.database_name = 'agency'
        self.database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
            DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
        setup_db_test(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_public_add_actor(self):
        new_actor = {
            'name': 'Dwayne Johnson',
            'age': 50,
            'gender': 'male'
        }

        res = self.client().post('/actors', json=new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_add_actor(self):
        new_actor = {
            'name': 'Dwayne Johnson',
            'age': 50,
            'gender': 'male'
        }
        self.headers.update({'Authorization': 'Bearer ' + TOKEN})

        res = self.client().post(
            '/actors', json=new_actor,
            headers=self.headers)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_public_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_get_actors(self):
        self.headers.update({'Authorization': 'Bearer ' + TOKEN})

        res = self.client().get('/actors', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_public_update_actor(self):
        updated_actor = {
            'name': 'Carl'
        }

        res = self.client().patch('/actors/1', json=updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_update_actor(self):

        actor = Actor(name='Dwaine Johnsen', age=50,
                      gender='male')
        actor.insert()
        actor_id = actor.id

        updated_actor = {
            'name': 'Dwayne Johnson'
        }

        self.headers.update({'Authorization': 'Bearer ' + TOKEN})

        res = self.client().patch(
            f'/actors/{actor_id}',
            json=updated_actor,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_public_delete_actor(self):

        res = self.client().delete('/actors/1', )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_delete_actor(self):
        actor = Actor(name='Bruce Willis', age=60,
                      gender='male')
        actor.insert()
        actor_id = actor.id

        self.headers.update({'Authorization': 'Bearer ' + TOKEN})

        res = self.client().delete(f'/actors/{actor_id}', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['delete'], str(actor_id))

    def test_public_add_movie(self):
        new_movie = {
            'title': 'Transformers',
            'release_date': '01.12.2010'
        }

        res = self.client().post('/movies', json=new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_add_movie(self):
        new_movie = {
            'title': 'Transformers',
            'release_date': '01-10-2010'
        }
        self.headers.update({'Authorization': 'Bearer ' + TOKEN})

        res = self.client().post(
            '/movies', json=new_movie,
            headers=self.headers)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_public_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_get_movies(self):
        self.headers.update({'Authorization': 'Bearer ' + TOKEN})

        res = self.client().get('/movies', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_public_update_movie(self):
        updated_movie = {
            'title': 'Avengers'
        }

        res = self.client().patch('/movies/1', json=updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_update_movie(self):
        movie = Movie(
            title='Mission Impossible',
            release_date='January-5-2010')
        movie.insert()
        movie_id = movie.id

        updated_movie = {
            'title': 'Mission Impossible 2'
        }

        self.headers.update({'Authorization': 'Bearer ' + TOKEN})

        res = self.client().patch(
            f'/movies/{movie_id}',
            json=updated_movie,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_public_delete_movie(self):

        res = self.client().delete('/movies/1', )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_delete_movie(self):
        movie = Movie(title='Avengers', release_date='March-25-2010')
        movie.insert()
        movie_id = movie.id

        self.headers.update({'Authorization': 'Bearer ' + TOKEN})

        res = self.client().delete(f'/movies/{movie_id}', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['delete'], str(movie_id))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
