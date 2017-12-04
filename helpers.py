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
    """Shuffle all questions and year prompts in Round 2."""

    rows = db.execute("SELECT question, year_prompt FROM round_two")

    pre_shuffle = list()
    for i in range(len(rows)):
        pre_shuffle.append((rows[i]["question"], rows[i]["year_prompt"]))

    post_shuffle = list(pre_shuffle)
    shuffle(post_shuffle)

    return post_shuffle

def three_category():
    """Random category generator."""

    result = db.execute("SELECT DISTINCT category FROM round_three")
    cats_pre = list()
    for i in range(len(result)):
        cats_pre.append(result[i]["category"])

    cats_post = list(cats_pre)
    shuffle(cats_post)

    #cat_num = randint(0, 3)
    #category = cats_post[cat_num]

    return cats_post

def three_qs(cat):
    """Shuffle all questions in selected category."""

    rows = db.execute("SELECT question FROM round_three WHERE category = :category", category=cat)

    qs_list_pre = list()
    for i in range(len(rows)):
        qs_list_pre.append(rows[i]["question"])

    qs_list_post = list(qs_list_pre)
    shuffle(qs_list_post)

    return qs_list_post

def three_ans(cat):
    """Shuffle all answers in selected category."""

    rows = db.execute("SELECT answer FROM round_three WHERE category = :category", category=cat)

    ans_list_pre = list()
    for i in range(len(rows)):
        ans_list_pre.append(rows[i]["answer"])

    ans_list_post = list(ans_list_pre)
    shuffle(ans_list_post)

    return ans_list_post

def anskey(round_num):
    """Create answer key."""

    answer_key = dict()
    rows = db.execute("SELECT question, answer FROM :round_num", round_num=round_num)

    for i in range(len(rows)):
        answer_key[rows[i]["question"]] = rows[i]["answer"]

    return answer_key