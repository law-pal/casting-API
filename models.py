import os
from sqlalchemy import Column, String, Integer, Boolean, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
import json



DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'lawpal86')
DB_NAME = os.getenv('DB_NAME', 'agency')
database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


''' Actor'''
class Actor(db.Model):
   __tablename__ = 'actors'

   id = Column(db.Integer, primary_key=True)
   name = Column(db.String(120))
   age = Column(db.Integer)
   gender = Column(db.String(120))

   def __repr__(self):
          return f'<actors {self.id} {self.name}>'

   def __init__(self, name, age, gender):
      self.name = name
      self.age = age
      self.gender = gender

   def insert(self):
      db.session.add(self)
      db.session.commit()

   def update(self):
      db.session.commit()

   def delete(self):
      db.session.delete(self)
      db.session.commit()

   def format(self):
      return {
         'id': self.id,
         'name': self.name,
         'age': self.age,
         'gender': self.gender
      }

''' Movie '''

class Movie(db.Model):
   __tablename__ = 'movie'

   id = Column(db.Integer, primary_key=True)
   title = Column(db.String(120))
   release_date = Column(db.String(120))

   def __repr__(self):
          return f'<movie {self.id} {self.title}>'

   def __init__(self, title, release):
      self.title = title
      self.release = release

   def insert(self):
      db.session.add(self)
      db.session.commit()

   def update(self):
      db.session.commit()

   def delete(self):
      db.session.delete(self)
      db.session.commit()

   def format(self):
      return {
         'id': self.id,
         'title': self.title,
         'release': self.release
      }

