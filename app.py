from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.secret_key = environ["SECRET_KEY"] or "BASIC_KEY"
app.pemanent_session_lifetime = timedelta(minutes=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def repr(self):
        flash("Name: " + self.name + "\nEmail: " + self.email + "\n")


app.app_context().push()
db.create_all()
db.session.commit()
if __name__ == "__main__":
    app.run()


@app.route('/')
def index():
    if "name" not in session:
        return render_template("index.html")
    else:
        return render_template("index.html")


@app.route('/registration', methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        session["name"] = 'basic'
        session["email"] = 'check'
        db.add(User(session['name'], session['email']))
        db.commit()
        return redirect(url_for("index"))
    else:
        if "name" in session:
            return redirect(url_for("index"))
        else:
            return render_template("reginstration.html")
