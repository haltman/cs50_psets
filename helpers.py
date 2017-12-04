import csv
import urllib.request

from flask import redirect, render_template, request, session, url_for
from functools import wraps
from random import randint, shuffle
from cs50 import SQL

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///flow.db")

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def two_shuffle():
    """Shuffle all questions and years in Round 2."""

    # query database for all questions/years
    rows = db.execute("SELECT question, year_prompt FROM round_two")

    # list of tuples (question, year)
    pre_shuffle = list()
    for i in range(len(rows)):
        pre_shuffle.append((rows[i]["question"], rows[i]["year_prompt"]))

    # shuffle tuples
    post_shuffle = list(pre_shuffle)
    shuffle(post_shuffle)

    return post_shuffle

def three_category():
    """Random category generator for Round 3."""

    # query database for all unique categories
    result = db.execute("SELECT DISTINCT category FROM round_three")

    # list of categories
    cats_pre = list()
    for i in range(len(result)):
        cats_pre.append(result[i]["category"])

    # shuffle categories
    cats_post = list(cats_pre)
    shuffle(cats_post)

    return cats_post

def three_qs(cat):
    """Shuffle questions in provided category for Round 3."""

    # query database for questions in provided category
    rows = db.execute("SELECT question FROM round_three WHERE category = :category", category=cat)

    # list of questions in provided category
    qs_list_pre = list()
    for i in range(len(rows)):
        qs_list_pre.append(rows[i]["question"])

    # shuffle questions in provided category
    qs_list_post = list(qs_list_pre)
    shuffle(qs_list_post)

    return qs_list_post

def three_ans(cat):
    """Shuffle answers in provided category for Round 3."""

    # query database for answers in provided category
    rows = db.execute("SELECT answer FROM round_three WHERE category = :category", category=cat)

    # list of answers in provided category
    ans_list_pre = list()
    for i in range(len(rows)):
        ans_list_pre.append(rows[i]["answer"])

    # shuffle answers in provided category
    ans_list_post = list(ans_list_pre)
    shuffle(ans_list_post)

    return ans_list_post

def anskey(round_num):
    """Create answer key for provided round number."""

    # query database for questions/answers in provided round number
    answer_key = dict()
    rows = db.execute("SELECT question, answer FROM :round_num", round_num=round_num)

    # create answer key for provided round number
    for i in range(len(rows)):
        answer_key[rows[i]["question"]] = rows[i]["answer"]

    return answer_key