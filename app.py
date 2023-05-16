from flask import redirect, url_for, render_template, request, session, flash
from tables import *
from levels import *
from tasks import *

for task in all_tasks:  # task_name/Day/Times/Level
    data = db.session.query(PhysTask).filter(PhysTask.task_name == task[0], PhysTask.day == task[1], PhysTask.times == task[2], PhysTask.level == task[3]).first()
    if data:
        pass
        # print(data.day)
        # print(data.times)
        # print(data.level)
        # print(data.task_name)
    else:
        db.session.add(PhysTask(task[0], task[1], task[2], task[3]))
db.session.commit()

question_text = "What is your Weight?"
# print(db.session.query(Tests).filter(Tests.text == question_text))
if not db.session.query(Tests).filter(Tests.text == question_text).all():
    db.session.add(Tests(question_text))
    question_id = db.session.query(Tests).filter(Tests.text == question_text).first().id
    db.session.add(Answers("<50kg", question_id, 0))
    db.session.add(Answers("50-70kg", question_id, 1))
    db.session.add(Answers(">70kg", question_id, 1))

question_text = "What is your Height?"
if not db.session.query(Tests).filter(Tests.text == question_text).all():
    db.session.add(Tests(question_text))
    question_id = db.session.query(Tests).filter(Tests.text == question_text).first().id
    db.session.add(Answers("<170sm", question_id, 0))
    db.session.add(Answers("170-180sm", question_id, 1))
    db.session.add(Answers(">180sm", question_id, 0))

db.session.commit()

t = db.session.query(Tests).first()


# print(t.text, t.in_big, t.in_small)


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
                session["id"] = db.session.query(User).filter(User.name == session["name"]).first().id
                session["last_test"] = 1
                session["cur_level"] = db.session.query(User).filter(User.name == session["name"]).first().level
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
        # print(request.form)
        session["password"] = request.form["password"]
        session["email"] = request.form["email"]
        session["name"] = request.form["name"]
        session["last_test"] = 1
        session["cur_level"] = 0
        session.permanent = True
        db.session.add(User(session["password"], session["email"], session["name"]))
        db.session.commit()
        session["id"] = db.session.query(User).filter(User.name == session["name"]).first().id
        return redirect(url_for("index"))

    if "name" in session:
        return redirect(url_for("index"))
    else:
        return render_template("sign_up.html", email_fill=email_fill, name_fill=name_fill, password_fill=password_fill)


@app.route('/logout')
def logout():
    if "name" in session:
        arr = []
        for entry in session:
            arr.append(entry)
        for entry in arr:
            session.pop(entry)
    return redirect(url_for('login'))


@app.route('/test/<index>', methods=["POST", "GET"])
def test(index):
    index = int(index)
    print(index)
    if index < 1:
        return redirect("/test/1")
    next_btn_text = "Next question"
    prev_btn_text = "Previous question"
    questions = db.session.query(Tests).all()

    if index == len(questions):
        next_btn_text = "Finish"

    if index > len(questions):
        return redirect("/done")

    question = questions[index - 1]
    pos_answers = db.session.query(Answers).filter(Answers.question_id == question.id).all()
    print(request)
    print(session["id"])
    if request.method == "POST":
        for i in request.form:
            answered = db.session.query(CurAnswers).filter(CurAnswers.test_id == session["last_test"]).first()
            if not answered:
                db.session.add(CurAnswers(session["id"], request.form[i], session["last_test"]))
            else:
                answered.answer = request.form[i]
                answered.user_id = session["id"]
                answered.test_id = session["last_test"]
            db.session.commit()
        session["last_test"] = index
        return redirect("/test/" + str(index))

    if "name" in session:
        session["last_test"] = index
        return render_template("test.html", index=index, n_index=index + 1, p_index=index - 1,
                               question=question.text, pos_answers=pos_answers,
                               next_btn_text=next_btn_text, prev_btn_text=prev_btn_text)
    else:
        return redirect(url_for("login"))


@app.route('/done')
def done():
    session["last_test"] = 1
    points = 0
    cur_ans = db.session.query(CurAnswers).filter(CurAnswers.user_id == session["id"]).all()
    for answer in cur_ans:
        ans = db.session.query(Answers).filter(Answers.text == answer.answer).first()
        points += ans.value
        db.session.delete(answer)
    cur_level = db.session.query(User).filter(User.id == session["id"]).first().level
    cur_level = max(cur_level, get_level(points))
    session["cur_level"] = cur_level
    db.session.add(TestStats(session["id"], points, len(db.session.query(TestStats).filter(TestStats.user_id == session["id"]).all()) + 1))
    db.session.commit()
    return render_template("done.html")


@app.route('/profile')
def profile():
    if request.method == "POST":
        pass
    if "name" in session:
        stats = db.session.query(TestStats).filter(TestStats.user_id == session["id"]).all()
        if stats:
            return render_template("profile.html", stats=stats, name=session["name"], email=session["email"], password=session["password"])
        else:
            return render_template("profile.html", stats='', name=session["name"], email=session["email"], password=session["password"])
    else:
        return redirect(url_for("login"))


@app.route('/recommendations')
def recommendations():
    if request.method == "POST":
        pass
    if "name" in session:
        rec_tasks = db.session.query(PhysTask).filter(PhysTask.level == session["cur_level"]).all()
        return render_template("recommendations.html", cur_level=session["cur_level"], rec_tasks=rec_tasks)
    else:
        return redirect(url_for("login"))
