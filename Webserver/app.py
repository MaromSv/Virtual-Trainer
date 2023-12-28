import sqlite3
from flask import Flask, render_template, request, redirect, url_for
# import sqlite_web
import requests
import json

# test_url = "http://danick.triantis.nl:8080/users/query/?sql=INSERT+INTO+users+(chk_email,+chk_password,+chk_userid)+VALUES+(%27marios%27,+%27m1234%27,+%271%27);"
# x = requests.get(test_url)

import requests

# url = 'http://danick.triantis.nl:8080'
# data = {'query': 'SELECT * FROM leaderboard'}

# response = requests.get(url, json=data)

# print(response.json())

# url = "http://danick.triantis.nl:8080/leaderboard/query/?sql=SELECT+*+FROM+users;"


def get_password(email):
    email.replace("@", "%40")
    email = "%22" + email + "%22"
    url = "http://danick.triantis.nl:8080/users/query/?ordering=&export_json=&sql=SELECT+password+FROM+%22users%22+WHERE+email%3D{}".format(email)
    x = requests.get(url)
    password_db = json.loads(x.text)[0]["password"]
    print(password_db)

def get_leaderboard():
    url = "http://danick.triantis.nl:8080/leaderboard/query/?ordering=&export_json=&sql=SELECT+*+FROM+%22leaderboard%22;"
    x = requests.get(url)
    data = json.loads(x.text)
    print(data)

# get_leaderboard()
# get_password("marios@gmail.com")

app = Flask(__name__,template_folder='templates',static_folder='static')

# class User(db.Model):
#     userid = db.Column(db.Integer, primary_key=True, nullable=True)
#     email = db.Column(db.text(120), unique=True, nullable=True)
#     password = db.Column(db.text(255), nullable=True)

# class Personal_Form(db.Model):
#     userid = db.Column(db.Integer, primary_key=True, nullable=True)
#     first_name = db.Column(db.text(255), nullable=True)
#     last_name = db.Column(db.text(255), nullable=True)
#     age = db.Column(db.Integer, nullable=True)
#     gender = db.Column(db.text(255), nullable=True)
#     experience = db.Column(db.text(255), nullable=True)
#     location = db.Column(db.text(255), nullable=True)

# class Buddy_Form(db.Model):
#     userid = db.Column(db.Integer, primary_key=True, nullable=True)
#     days_preference = db.Column(db.text(255), nullable=True)
#     gender_preference = db.Column(db.text(255), nullable=True)
#     experience_preference = db.Column(db.text(255), nullable=True)
#     location_preference = db.Column(db.text(255), nullable=True)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/buddy')
def buddy():
    return render_template('buddy.html')

@app.route('/leaderboard')
def leaderboard():
    get_leaderboard()
    return render_template('leaderboard.html')

@app.route('/login_form', methods=["get"])
def login_form():
    email = request.form['loginemail']
    password = request.form['loginpw']
    # user = User.query.filter_by(email=email).first()
    if password == get_password(email):
        return render_template('home.html')
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
