from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_socketio import SocketIO, emit


# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
socketio = SocketIO(app)

Session(app)

db = SQL("sqlite:///messages.db")


@app.route("/")
def index():
    # if user is not loged redirect to login template
    if not session.get("user_id"):
        return redirect("/login")

    messages_db = db.execute("SELECT * FROM messages")
    users_db = db.execute("SELECT * FROM users")
    # if user is loged render chat with all messages from database
    return render_template("index.html", messages_db=messages_db, users_db=users_db)


@app.route("/register", methods=["GET", "POST"])
def register():
    # list of all useres from databes to check is username is already taken
    users = []

    for user in db.execute("SELECT username FROM users"):
        users.append(user["username"])

    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("register.html", error="Please prompot username.")

        if request.form.get("username") in users:
            return render_template("register.html", error="Username already taken.")

        if len(request.form.get("username")) < 5:
            return render_template("register.html", error="Username to short (min 5 characters).")

        if not request.form.get("password"):
            return render_template("register.html", error="Please prompot password.")

        if len(request.form.get("password")) < 5:
            return render_template("register.html", error="Password (min 5 characters).")

        if not request.form.get("confirmation"):
            return render_template("register.html", error="Please confirm password.")

        if request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html", error="Passwords don`t match.")

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))
        return render_template("login.html", error="You are register. Please login.")

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
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", error="Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        socketio.emit('user_join', (session['username']))
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    socketio.emit('user_left', (session['username']))
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# socketio events


@socketio.on('send_message')
def handle_send_message_event(data):

    text = data['message']
    username = session['username']
    userid = session['user_id']
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")

    db.execute(
        "INSERT INTO messages (user_id, text, date) VALUES(?, ?, ?)", userid, text, date)

    socketio.emit('receive_message', (text, username, userid, date))


if __name__ == '__main__':
    socketio.run(app)
