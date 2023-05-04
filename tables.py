from datetime import timedelta
from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = environ["SECRET_KEY"] or "BASIC_KEY"
app.pemanent_session_lifetime = timedelta(minutes=0)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)


class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, password, email, name):
        self.name = name
        self.email = email
        self.password = password

    def repr(self):
        return "Name: " + self.name + "\nEmail: " + self.email


class TestStats(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    points = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    def __init__(self, user_id, points, date=datetime.now()):
        self.user_id = user_id
        self.points = points
        self.date = date

    def repr(self):
        return "Date and time: " + str(self.date) + ", points: " + str(self.points)


class Tests(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    in_big = db.Column(db.Boolean)
    in_small = db.Column(db.Boolean)

    def __init__(self, text, in_big=True, in_small=False):
        self.text = text
        self.in_big = in_big
        self.in_small = in_small

    def repr(self):
        return self.text


db.create_all()
db.session.commit()
