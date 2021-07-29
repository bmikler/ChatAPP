from os import name
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


# Configure application

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True

Session(app)

db = SQL("sqlite:///messages.db")

@app.route("/")
def index():
    if not session.get("user_id"):
        return redirect("/login")

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
# list of all useres from databes to check is username is already taken
    users = []

    for user in db.execute("SELECT username FROM users"):
        users.append(user["username"])

    if request.method == "POST":
        
        if not request.form.get("username"):
            return render_template("register.html", error = "Please prompot username.")

        if request.form.get("username") in users:
            return render_template("register.html", error = "Username already taken.")
        
        if len(request.form.get("username")) < 5:
            return render_template("register.html", error = "Username to short (min 5 characters).")

        if not request.form.get("password"):
            return render_template("register.html", error = "Please prompot password.")
            
        if len(request.form.get("password")) < 5:
            return render_template("register.html", error = "Password (min 5 characters).")

        if not request.form.get("confirmation"):
            return render_template("register.html", error = "Please confirm password.")

        if request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html", error = "Passwords don`t match.")

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))
        return render_template("login.html", error = "You are register. Please login.")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", error="Provide username.")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", error="Provide password.")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", error="Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        print(session["user_id"], session["username"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/send", methods=["GET", "POST"])
def send():
    text = request.form.get("message")

    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")

    if text:
        db.execute("INSERT INTO messages (user_id, text, date) VALUES(?, ?, ?)", session["user_id"], text, date)
    return redirect("/")

    
@app.route("/chatbox")
def chatbox():
    messages = db.execute("SELECT * FROM messages")
    users = db.execute("SELECT * FROM users")
    return render_template("chatbox.html", messages=messages, users=users)
