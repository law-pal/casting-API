import os
from jose import jwt
from os import environ as env
from werkzeug.exceptions import HTTPException
from flask import Flask, request, abort, jsonify, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, setup_db, Actor, Movie
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
import auth_config
from functools import wraps
from auth import AuthError, requires_auth, requires_signed_in

AUTH0_CALLBACK_URL = auth_config.AUTH0_CALLBACK_URL
AUTH0_CLIENT_ID = auth_config.AUTH0_CLIENT_ID
AUTH0_CLIENT_SECRET = auth_config.AUTH0_CLIENT_SECRET
AUTH0_DOMAIN = auth_config.AUTH0_DOMAIN
AUTH0_BASE_URL = 'https://' + auth_config.AUTH0_DOMAIN
AUTH0_AUDIENCE = auth_config.AUTH0_AUDIENCE


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = 'super secret key'
    setup_db(app)
    migrate = Migrate(app, db)

    CORS(app, resources={r'/api/*': {'origins': '*'}})

    oauth = OAuth()
    oauth.init_app(app)

    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=AUTH0_BASE_URL,
        access_token_url=AUTH0_BASE_URL + '/oauth/token',
        authorize_url=AUTH0_BASE_URL + '/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    '''
    after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/login')
    def login():
        return auth0.authorize_redirect(
            redirect_uri=AUTH0_CALLBACK_URL,
            audience=AUTH0_AUDIENCE)

    @app.route('/callback')
    def callback_handling():
        # Handles response from token endpoint
        res = auth0.authorize_access_token()
        token = res.get('access_token')

        # Store the user information in flask session.
        session['jwt_token'] = token
        return redirect('/dashboard')

    @app.route('/logout')
    def logout():
        # Clear session stored data
        session.clear()
        params = {
            'returnTo': url_for('home', _external=True),
            'client_id': AUTH0_CLIENT_ID
        }
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

    @app.route('/dashboard')
    @requires_signed_in
    def dashboard():
        return render_template('dashboard.html', token=session['jwt_token'])

# MOVIES
    @app.route('/movies')
    def get_movies():

        try:
            movies = Movie.query.all()

            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movies]
            }, 200)

        except BaseException:
            abort(404)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(jwt):

        body = request.get_json()

        if not ('title' in body and 'release_date' in body):
            abort(404)

        title = body.get('title')
        release_date = body.get('release_date')

        try:
            movie = Movie(title=title, release_date=release_date)
            movie.insert()

            return jsonify({
                'success': True
            })

        except BaseException:
            abort(422)

    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):

        movie = Movie.query.get(id)

        if movie:
            try:
                body = request.get_json()

                title = body.get('title')
                release_date = body.get('release_date')

                if title:
                    movie.title = title
                if release_date:
                    movie.release_date = release_date

                movie.update()

                return jsonify({
                    'success': True
                })
            except BaseException:
                abort(422)
        else:
            abort(404)

    @app.route("/movies/<id>", methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(jwt, id):

        movie = Movie.query.get(id)

        if movie:
            try:
                movie.delete()
                return jsonify({
                    'success': True,
                    'delete': id
                })
            except BaseException:
                abort(422)
        else:
            abort(404)

# ACTORS
    @app.route('/actors')
    def get_actors():
        try:
            actors = Actor.query.all()

            return jsonify({
                'success': True,
                'actors': [actor.format() for actor in actors]
            }, 200)

        except BaseException:
            abort(404)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(jwt):

        body = request.get_json()

        if not ('name' in body and 'age' in body and 'gender' in body):
            abort(404)

        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()

            return jsonify({
                'success': True
            })

        except BaseException:
            abort(422)

    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):

        actor = Actor.query.get(id)

        if actor:
            try:
                body = request.get_json()

                name = body.get('name')
                age = body.get('age')
                gender = body.get('gender')

                if name:
                    actor.name = name
                if age:
                    actor.age = age
                if gender:
                    actor.gender = gender

                actor.update()

                return jsonify({
                    'success': True
                })
            except BaseException:
                abort(422)
        else:
            abort(404)

    @app.route("/actors/<id>", methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(jwt, id):

        actor = Actor.query.get(id)

        if actor:
            try:
                actor.delete()
                return jsonify({
                    'success': True,
                    'delete': id
                })
            except BaseException:
                abort(422)
        else:
            abort(404)

# Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': str(error)
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': str(error)
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        return jsonify({
            'success': False,
            'error': ex.status_code,
            'message': ex.error
        }), 401

    return app


app = create_app()


if __name__ == '__main__':
    app.run()
