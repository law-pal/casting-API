import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, setup_db, Actor, Movie
#from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  migrate = Migrate(app, db)

  CORS(app, resources={r'/api/*': {'origins': '*'}})


  '''
  after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''MOVIES'''

  @app.route('/movies')
  #@requires_auth('view:movies')
  def get_movies():

    try:
        movies = Movie.query.all()

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }, 200)

    except:
        abort(404)

  @app.route('/movies', methods=['POST'])
  #@requires_auth('post:movies')
  def add_movie():

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

      except:
          abort(422)

  @app.route('/movies/<id>', methods=['PATCH'])
  #@requires_auth('patch:movies')
  def update_movie(id):

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
        except: 
            abort(422)
    else:
        abort(404)  

  @app.route("/movies/<id>", methods=['DELETE'])
  #@requires_auth('delete:movies')
  def delete_movies(id):

    movie = Movie.query.get(id)

    if movie:
          try:
              movie.delete()
              return jsonify({
                  'success': True,
                  'delete': id
              })
          except:
              abort(422)
    else:
          abort(404)


  '''ACTORS'''

  @app.route('/actors')
  #@requires_auth('view:actors')
  def get_actors():
    try:
        actors = Actor.query.all()

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }, 200)

    except:
        abort(404)

  @app.route('/actors', methods=['POST'])
  #@requires_auth('post:actors')
  def add_actor():

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

      except:
          abort(422)

  @app.route('/actors/<id>', methods=['PATCH'])
  #@requires_auth('patch:actors')
  def update_actor(id):

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
        except: 
            abort(422)
    else:
        abort(404)  

  @app.route("/actors/<id>", methods=['DELETE'])
  #@requires_auth('delete:actors')
  def delete_actors(id):

    actor = Actor.query.get(id)

    if actor:
          try:
              actor.delete()
              return jsonify({
                  'success': True,
                  'delete': id
              })
          except:
              abort(422)
    else:
          abort(404)


  return app
  create_app().run(debug=True)

# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=8080, debug=True)