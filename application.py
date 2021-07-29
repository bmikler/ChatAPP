import os
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from cs50 import SQL


# Configure application

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True

Session(app)

# Connect do SQL - TODO
db = SQL("sqlite:///messeges.db")


@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/login")

    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route("/send", methods=["GET", "POST"])
def send():
    text = request.form.get("message")
    if text:
        db.execute("INSERT INTO messeges (sender, text) VALUES(?, ?)", session["name"], text)
    return redirect("/")

    
@app.route("/chatbox")
def chatbox():
    messeges = db.execute("SELECT * FROM messeges")
    return render_template("chatbox.html", messeges=messeges)
