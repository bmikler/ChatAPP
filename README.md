
# cs50 Quarrel-app

## Description:

This is my final project for CS50's Introduction to Computer Science.
Simple real-time chat app, where users can register their account, login and chat with each other.

## Overview:

This app contains fallowing features:

* Registration users in sql database - wroks with sqlite3 and CS50 libry.
* To inprove seciurity all passwords are hashes by Werkzeug hash function.
* Real-time messages and information about users who join or leave the chat. Works with websocet (flask-socetio). In first version sending messages was working by refreshing single chatbox div.
* Auto scrolling chat-box - works with simple javascript script, auto-scrolling works only if user don`t scroll up by humself.
* All messages are saveing in sql database - wroks with sqlite3 and CS50 libry.


# Rest-API

Rest-API created with Flask.
[Flask](https://flask.palletsprojects.com/en/2.0.x/)

# Deployment

Deployment via heroku and gunicorn.

[Heroku](https:/www.heroku.com)
[Gunicorn](https://gunicorn.org/)

## Way to improvement in next version:
* Add multiple rooms.
* Add users photos.
* Use sqlalchemy instead of CS50 sql libry.

# Try app by Yourself!
[Quarrel chat-app](http://glacial-lake-99797.herokuapp.com/)

### File list:

app.py - Reast-API created wtih Python/Flask.
messages.db - sql database, contains users and messages table.
Profile - information needed for deplyment app with gunicorn and heroku.

static/styles.css - css stylesheet.
templates/index.html - main app page, contains chatbox.
templates/layout.html - main layout of the app.
templates/login.html - login page.
templates/register - registration page.

# Python Libraries needed:
•	Flask
•	CS50
•	werkzeug.security
•	flask_socketio
•	

Credits:
Messenger style chatbox was inspired by Easy HTML Learner:
[Easy HTML Learner]( https://www.youtube.com/watch?v=qbKJj691FFg&t=442s)




