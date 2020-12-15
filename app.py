import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import setup_db, Actor, Movie

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  db = SQLAlchemy(app)
  migrate = Migrate(app, db)

  CORS(app)




  return app
  create_app().run(debug=True)

# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=8080, debug=True)