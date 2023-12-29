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
    if x.text == "[]":
        return "email not found"
    password_db = json.loads(x.text)[0]["password"]
    return password_db

def get_max_userid():
    url = "http://danick.triantis.nl:8080/users/query/?ordering=&export_json=&sql=SELECT+userid%0D%0AFROM+users%0D%0AWHERE+userid+IN+%28%0D%0A++++SELECT+MAX%28userid%29%0D%0A++++FROM+users%0D%0A%29"
    x = requests.get(url)
    if x.text == "[]":
        return 0
    data = json.loads(x.text)[0]["userid"]
    return data

def insert_user(userid,email,password):
    email.replace("@", "%40")
    email = "%22" + email + "%22"
    url = "http://danick.triantis.nl:8080/users/query/?ordering=&export_ordering=&sql=INSERT+INTO+users+%28email%2Cpassword%2Cuserid%29%0D%0AVALUES+%28%22{}%22%2C+%22{}%22%2C{}%29".format(email,password,userid)
    x = requests.get(url)
    # print(json.loads(x.text))

def insert_personal_form(userid,first_name,last_name,age,gender,experience,location):
    url="http://danick.triantis.nl:8080/Personal_Form/query/?ordering=&export_ordering=&sql=INSERT+INTO+Personal_Form+%28userid%2Cfirst_name%2Clast_name%2Cage%2Cgender%2Cexperience%2Clocation%29%0D%0AVALUES+%28{}%2C%22{}%22%2C%22{}%22%2C{}%2C%22{}%22%2C%22{}%22%2C%22{}%22%29".format(userid,first_name,last_name,age,gender,experience,location)
    x = requests.get(url)
    # print(json.loads(x.text))

def createaccount(email,password,first_name,last_name,age,gender,experience,location):
    userid = get_max_userid() + 1
    insert_user(userid,email,password)
    insert_personal_form(userid,first_name,last_name,age,gender,experience,location)


def get_leaderboard():
    url = "http://danick.triantis.nl:8080/leaderboard/query/?ordering=&export_json=&sql=SELECT+*+FROM+%22leaderboard%22+ORDER+BY+%22score%22+DESC;"
    x = requests.get(url)
    data = json.loads(x.text)
    print(data)
    return data

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
    data = get_leaderboard()
    return render_template('leaderboard.html', results = data)

@app.route('/login_form', methods=['POST'])
def login_form():
    email = request.form['loginemail']
    password = request.form['loginpw']
    print(email, password)
    if password == get_password(email):
        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))

@app.route('/signup_form', methods=['POST'])
def signup_form():
    email = request.form['signupemail']
    password = request.form['signuppw']
    password_confirm = request.form['signuppwconfirm']
    first_name = request.form['signupfirstname']
    last_name = request.form['signuplastname']
    age = request.form['signupage']
    gender = request.form.getlist('signupgender')
    experience = request.form.getlist('signupexperience')
    location = request.form.getlist('signuplocation')
    print(email,password,password_confirm,first_name,last_name,age,gender,experience,location)
    if email=="" or password == "" or password_confirm == "" or first_name == "" or last_name == "" or age == "" or gender == [] or experience == [] or location == []:
        return redirect(url_for('signup'))
    else:
        gender = gender[0]
        experience = experience[0]
        location = location[0]
    if password == password_confirm:
        createaccount(email, password,first_name,last_name,age,gender,experience,location)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('signup'))

if __name__ == '__main__':
    app.run(debug=True)
