import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date
from flask_migrate import Migrate

database_name = 'casting_agency'
database_path = 'postgres://czupthrakoiebb:40e2294faf1c2b347252e5185180fec345f2b8416daf88081b41bbf1f0f50893@ec2-3-234-109-123.compute-1.amazonaws.com:5432/d3oed7orapo5u8'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] =database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app =app
    db.init_app(app)
    db.create_all()


'''
Actors
'''
class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

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


'''
Movies
'''
class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    release_date = Column(Date)

    def __init__(self, name, release_date):
        self.name = name,
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id': self.id,
            'name': self.name,
            'release_date': self.release_date
        }