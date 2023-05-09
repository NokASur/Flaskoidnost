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
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    admin = db.Column(db.Integer)

    def __init__(self, password, email, name, admin=0):
        self.name = name
        self.email = email
        self.password = password
        self.admin = admin

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
    id = db.Column("id", db.Integer, primary_key=True)
    text = db.Column(db.String(1000))

    def __init__(self, text):
        self.text = text

    def repr(self):
        return self.text


class Answers(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    question_id = db.Column(db.Integer)
    value = db.Column(db.Integer)

    def __init__(self, text, question_id, value):
        self.text = text
        self.question_id = question_id
        self.value = value

    def repr(self):
        return self.text


class CurAnswers(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    test_id = db.Column(db.Integer)
    answer = db.Column(db.String(100))

    def __init__(self, user_id, answer, test_id):
        self.user_id = user_id
        self.answer = answer
        self.test_id = test_id


db.create_all()
db.session.commit()
