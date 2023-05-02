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
    password = db.Column(db.String(100))

    def __init__(self, password, email, name):
        self.name = name
        self.email = email
        self.password = password

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
        return redirect(url_for("login"))
    else:
        return render_template("index.html", name=session["name"])


@app.route('/login', methods=["GET", "POST"])
def login(meta_fill="Name/Email", password_fill="Password"):
    if request.method == "POST":
        meta = request.form['meta']
        password = request.form['password']
        bad = 1
        if meta == '' or password == '':
            add = "Please, fill this form too!"
            if password == '':
                password_fill = add + "(PASSWORD)"
            if meta == '':
                meta_fill = add + "(NAME/EMAIL)"

        elif db.session.query(User).filter(User.name == meta).first() is None and \
                db.session.query(User).filter(User.email == meta).first() is None:
            meta_fill = "Incorrect name/email"
        else:
            account = db.session.query(User).filter(User.name == meta).first() or db.session.query(User).filter(User.email == meta).first()
            if account.password != password:
                password_fill = "Incorrect password"
            else:
                session["password"] = account.password
                session["email"] = account.email
                session["name"] = account.name
                bad = 0
        if bad:
            return render_template("login.html", meta_fill=meta_fill, password_fill=password_fill)

        session.permanent = True
        return redirect(url_for("index"))
    else:
        if "name" in session:
            return redirect(url_for("index"))
        else:
            return render_template("login.html", meta_fill=meta_fill, password_fill=password_fill)


@app.route('/sign_up', methods=["GET", "POST"])
def sign_up(email_fill="Email", name_fill="Nickname", password_fill="Password"):
    if request.method == "POST":
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        bad = 1
        if email == '' or password == '' or name == '':
            add = "Please, fill this form too!"
            if password == '':
                password_fill = add + "(PASSWORD)"
            if name == '':
                name_fill = add + "(NAME)"
            if email == '':
                email_fill = add + "(EMAIL)"

        elif db.session.query(User).filter(User.name == name).first() is not None:
            name_fill = "This name is in use"

        elif db.session.query(User).filter(User.email == email).first() is not None:
            email_fill = "This email is in use"
        else:
            bad = 0
        if bad:
            return render_template("sign_up.html", email_fill=email_fill, name_fill=name_fill, password_fill=password_fill)

        session["password"] = request.form["password"]
        session["email"] = request.form["email"]
        session["name"] = request.form["name"]
        session.permanent = True
        db.session.add(User(session["password"], session["email"], session["name"]))
        db.session.commit()
        return redirect(url_for("index"))

    if "name" in session:
        return redirect(url_for("index"))
    else:
        return render_template("sign_up.html", email_fill=email_fill, name_fill=name_fill, password_fill=password_fill)


@app.route('/logout')
def logout():
    if "name" in session:
        session.pop("name")
    return redirect(url_for('login'))
