from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from random import randint, shuffle
import json

from helpers import *

# global scores
score = 0
score_one = 0
score_two = 0
score_three = 0

# global round number
round_num = 0

# global list of random questions/answers for round one
nums = list()

# global count of questions answered in round three
num_q = 0

# global list of randomly ordered categories for round three
cat_list = list()

# global answer key for round one
answer_key_one = dict()

# global answer map for round three
answer_map_three = dict()

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///flow.db")

@app.route("/")
@login_required
def index():
    """User's home page"""

    # identify user's username
    username = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])

    # identify user's high score
    result = db.execute("SELECT score FROM history WHERE user_id = :user_id AND high_score = 'Y'", user_id=session["user_id"])
    if len(result) == 0:
        high_score = 0
    else:
        high_score = result[0]["score"]

    return render_template("index.html", username=username[0]["username"], score=high_score)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            flash("Invalid username and/or password.")
            return render_template("login.html")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # inform user if username already exists
        result = db.execute("SELECT username FROM users WHERE username = :username", username=request.form.get("username"))
        if len(result) != 0:
            flash("That username already exists. Try another!")
            return render_template("register.html")

        # otherwise insert username and password into database
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")))

            # query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

            # remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # redirect user to home page
            flash("Registered!")
            return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/new")
@login_required
def new():
    """Start a new game."""

    return render_template("new.html")

@app.route("/one", methods=["GET", "POST"])
@login_required
def one():
    """Round 1."""

    # access global variables
    global score
    global score_one
    global round_num
    global nums
    global answer_key_one

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # obtain user's responses
        responses = dict()
        for i in range(5):
            responses[i] = request.form.get("q" + str(i+1))

        # compare user's responses to answer key and update score
        for i in range(5):
            if answer_key_one[i] == responses[i]:
                score_one = score_one + 1

        # redirect user to second round if answered 3 or more questions correctly
        if score_one >= 3:
            flash("Round 1 Complete!")
            score = score + score_one
            round_num = round_num + 1
            return redirect(url_for("two"))

        else:
            return redirect(url_for("loser"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:

        # select 5 questions randomly from database
        for i in range (5):
            while True:
                id = randint(0, 19)
                if id not in nums:
                    nums.append(id)
                    break

        rows = db.execute("SELECT question, answer FROM round_one WHERE id IN (:nums)", nums=nums)

        # numbered questions
        qs_dict = dict()
        for i in range(1, 6):
            qs_dict[i] = rows[i - 1]["question"]

        # lettered answers
        ans_list_pre = list()
        ans_dict_pre = dict()
        for i in range(5):
            ans_dict_pre[i] = rows[i]["answer"]
            ans_list_pre.append(rows[i]["answer"])

        # shuffle answers
        i = 0
        qa_dict = dict()
        ans_list_post = list(ans_list_pre)
        shuffle(ans_list_post)
        ans_dict_post = dict()
        for char in "ABCDE":
            ans_dict_post[char] = ans_list_post[i]
            qa_dict[i + 1] = (rows[i]["question"], char, ans_list_post[i])
            i += 1

        # create answer key
        j = 0
        while True:
            if j < len(ans_list_pre):
                for key in ans_dict_post:
                    if ans_dict_pre[j] == ans_dict_post[key]:
                        answer_key_one[j] = str(key)
                        break
                j += 1
            else:
                break

        return render_template("one.html", parent_dict=qa_dict)

@app.route("/two", methods=["GET", "POST"])
@login_required
def two():
    """Round 2."""

    # access global variables
    global score
    global score_two
    global round_num

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # create answer key
        answer_key_two = anskey("round_two")

        # obtain user's responses
        jstr2 = request.form.get("answer_map_two")
        answer_map_two = json.loads(jstr2)

        # compare user's responses to answer key and update score
        for key in answer_map_two:
            if answer_key_two[key] == answer_map_two[key]:
                score_two = score_two + 1

        # redirect user to third round if answered 3 or more questions correctly
        if score_two >= 3:
            flash("Round 2 Complete!")
            score = score + score_two
            round_num = round_num + 1
            return redirect(url_for("three"))

        else:
            return redirect(url_for("loser"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:

        # shuffle questions/years
        shuffle = two_shuffle()

        # separate questions and years
        qs = list()
        yrs = list()
        for i in range(len(shuffle)):
            qs.append(shuffle[i][0])
            yrs.append(shuffle[i][1])

        return render_template("two.html", questions=qs, years=yrs)

@app.route("/three", methods=["GET", "POST"])
@login_required
def three():
    """Round 3."""

    # access global variables
    global score
    global score_three
    global round_num
    global num_q
    global answer_map_three
    global cat_list

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # udpate answer map with user's answers
        jstr3 = request.form.get("answer_map_three")
        loaded = json.loads(jstr3)
        if not answer_map_three:
            answer_map_three = loaded
        else:
            answer_map_three.update(loaded)

        # check round three score and determine if winner or loser
        if num_q == 4:

            # create answer key
            answer_key_three = anskey("round_three")

            # compare user's responses to answer key and update score
            for key in answer_map_three:
                if answer_key_three[key] == answer_map_three[key]:
                    score_three = score_three + 1

            # reset global variables
            num_q = 0
            answer_map_three = {}
            cat_list = ()

            # redirect user to third round if answered 3 or more questions correctly
            if score_three >= 3:
                flash("Round 3 Complete!")
                score = score + score_three
                round_num = round_num + 1
                return redirect(url_for("winner"))

            else:
                return redirect(url_for("loser"))

        # otherwise continue round three
        else:
            # generate next category
            category = cat_list[num_q]

            # shuffle questions
            questions = three_qs(category)

            # shuffle answers
            answers = three_ans(category)

            # update question number
            num_q = num_q + 1

            return render_template("three.html", category=category, questions=questions, answers=answers)

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        # generate random first category
        cat_list = three_category()
        category = cat_list[num_q]

        # shuffle questions
        questions = three_qs(category)

        # shuffle answers
        answers = three_ans(category)

        # update question number
        num_q = num_q + 1

        return render_template("three.html", category=category, questions=questions, answers=answers)

@app.route("/loser")
@login_required
def loser():
    """User loses the game."""

    # determine if user earned their highest score
    result = db.execute("SELECT MAX(score) as score FROM history WHERE user_id = :user_id GROUP BY user_id", user_id=session["user_id"])
    if len(result) == 0:

        # set high score flag to true if first game played
        high_score = 'Y'

    elif result[0]["score"] < score:

        # set high score flag to true if score of current game higher than previous games played
        high_score = 'Y'

        # reset high score flag to false for previously highest-scoring game record
        db.execute("UPDATE history SET high_score = 'N' WHERE user_id = :user_id AND high_score = 'Y'", user_id=session["user_id"])
    else:

        # otherwise not a high score
        high_score = 'N'

    # insert record of game played into history table
    db.execute("INSERT INTO history (user_id, score, high_score, date, round_num) VALUES (:user_id, :score, :high_score, CURRENT_TIMESTAMP, :round_num)", user_id=session["user_id"], score=score, high_score=high_score, round_num=round_num)

    return render_template("loser.html")

@app.route("/winner")
@login_required
def winner():
    """User wins the game."""

    # determine if user earned their highest score
    result = db.execute("SELECT MAX(score) as score FROM history WHERE user_id = :user_id GROUP BY user_id", user_id=session["user_id"])
    if len(result) == 0:

        # set high score flag to true if first game played
        high_score = 'Y'

    elif result[0]["score"] < score:

        # set high score flag to true if score of current game higher than any previous games played
        high_score = 'Y'

        # reset high score flag to false for previously highest-scoring game record
        db.execute("UPDATE history SET high_score = 'N' WHERE user_id = :user_id AND high_score = 'Y'", user_id=session["user_id"])
    else:

        # otherwise not a high score
        high_score = 'N'

    # insert record of game played into history table
    db.execute("INSERT INTO history (user_id, score, high_score, date, round_num) VALUES (:user_id, :score, :high_score, CURRENT_TIMESTAMP, :round_num)", user_id=session["user_id"], score=score, high_score=high_score, round_num=round_num)

    return render_template("winner.html")

@app.route("/history")
@login_required
def history():
    """History of all games played by user."""

    # query database for all games played by user
    rows = db.execute("SELECT score, high_score, date, round_num FROM history WHERE user_id = :user_id", user_id=session["user_id"])

    return render_template("history.html", rows=rows)

@app.route("/leader")
@login_required
def leader():
    """Flow Leader Board."""

    # query database for top 5 scores of all time
    rows = db.execute("SELECT u.username, MAX(h.score) as score, h.date FROM history h JOIN users u ON h.user_id=u.id GROUP BY u.username ORDER BY MAX(h.score) DESC LIMIT 5")

    return render_template("leader.html", rows=rows)




