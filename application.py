from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

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

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    # obtain user's portfolio
    rows = db.execute("SELECT symbol, name, SUM(shares) as shares FROM portfolio WHERE user_id = :user_id GROUP BY symbol, name", user_id=session["user_id"])

    # append current price of stock to each record in portfolio
    for row in rows:
        curr_quote = lookup(row["symbol"])
        curr_price = usd(curr_quote["price"])
        row["price"] = curr_price
        row["total"] = usd(curr_quote["price"] * row["shares"])

    # obtain user's cash balance
    cash = usd((db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"]))[0]["cash"])

    # obtain user's asset total
    total = usd((db.execute("SELECT total FROM users WHERE id = :id", id=session["user_id"]))[0]["total"])

    # display portfolio information to user
    return render_template("index.html", total=total,rows=rows, cash=cash)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure valid ticker symbol was entered
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("enter a valid ticker symbol")

        symbol = quote["symbol"]
        name = quote["name"]
        price = quote["price"]

        # ensure whole number of shares was entered
        if not request.form.get("shares").isdigit():
            return apology("enter a whole number of shares")

        # ensure positive number of shares was entered
        shares = int(request.form.get("shares"))
        if shares <= 0:
            return apology("enter a positive number of shares")

        # ensure user has enough cash to purchase shares
        cash = (db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"]))[0]["cash"]
        if (price * shares) <= float(cash):

            # add transaction to database
            db.execute("INSERT INTO portfolio (symbol, name, shares, price, transacted, user_id) VALUES (:symbol, :name, :shares, :price, CURRENT_TIMESTAMP, :user_id)", symbol=symbol, name=name, shares=shares, price=usd(price), user_id=session["user_id"])

            # update user's cash balance
            db.execute("UPDATE users SET cash = cash - :buy WHERE id = :id", buy=price * shares, id=session["user_id"])

        else:
            return apology("i'm sorry, you can't afford that")

        # redirect user to home page
        flash("Bought!")
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    # obtain all of user's transactions
    rows = db.execute("SELECT symbol, shares, price, transacted FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])

    # display all transactions to user
    return render_template("history.html", rows=rows)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

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

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure valid ticker symbol was submitted
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("enter a valid ticker symbol")

        # display quote information to user
        return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide a username to register")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide a password to register")

        # ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation of password to register")

        # ensure username doesn't already exist
        result = db.execute("SELECT username FROM users WHERE username = :username", username=request.form.get("username"))
        if len(result) != 0:
            return apology("username already exists")

        # ensure password and confirmation match
        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("both passwords entered do not match")

        # insert username and password into database
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

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure valid ticker symbol was entered
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("enter a valid ticker symbol")

        symbol = quote["symbol"]
        name = quote["name"]
        price = quote["price"]

        # ensure whole number of shares was entered
        if not request.form.get("shares").isdigit():
            return apology("enter a whole number of shares")

        # ensure positive number of shares was entered
        shares = int(request.form.get("shares"))
        if shares <= 0:
            return apology("enter a positive number of shares")

        # ensure user actually owns shares of stock entered
        own = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=symbol)
        if len(own) == 0:
            return apology("you don't own any shares with that ticker symbol")

        # ensure user owns enough shares to sell desired amount
        shares_bal = (db.execute("SELECT SUM(shares) as shares_bal FROM portfolio WHERE user_id = :user_id AND symbol = :symbol GROUP BY symbol = :symbol", user_id=session["user_id"], symbol=symbol))[0]["shares_bal"]
        if shares <= shares_bal:

            # add transaction to database
            db.execute("INSERT INTO portfolio (symbol, name, shares, price, transacted, user_id) VALUES (:symbol, :name, :shares, :price, CURRENT_TIMESTAMP, :user_id)", symbol=symbol, name=name, shares=shares * -1, price=usd(price), user_id=session["user_id"])

            # update user's cash balance
            db.execute("UPDATE users SET cash = cash + :sell WHERE id = :id", sell=price * shares, id=session["user_id"])

        else:
            return apology("i'm sorry, you don't own as many shares as you wish to sell")

        # redirect user to home page
        flash("Sold!")
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add additional cash to account."""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        amount = request.form.get("amount")

        # ensure an amount was submitted
        if not amount:
            return apology("must provide an amount")

        # ensure valid amount was entered
        if not amount.isdigit() or int(amount) <= 0:
            return apology("enter a valid amount")

        # update user's cash balance
        db.execute("UPDATE users SET cash = cash + :amount WHERE id = :id", amount=amount, id=session["user_id"])

        # update user's total balance
        db.execute("UPDATE users SET total = total + :amount WHERE id = :id", amount=amount, id=session["user_id"])

        # redirect user to home page
        flash("Added!")
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("add.html")