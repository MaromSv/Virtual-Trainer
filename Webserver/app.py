import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///root/Database/database.db'
db = SQLAlchemy(app)

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True, nullable=True)
    email = db.Column(db.text(120), unique=True, nullable=True)
    password = db.Column(db.text(255), nullable=True)

class Personal_Form(db.Model):
    userid = db.Column(db.Integer, primary_key=True, nullable=True)
    first_name = db.Column(db.text(255), nullable=True)
    last_name = db.Column(db.text(255), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.text(255), nullable=True)
    experience = db.Column(db.text(255), nullable=True)
    location = db.Column(db.text(255), nullable=True)

class Buddy_Form(db.Model):
    userid = db.Column(db.Integer, primary_key=True, nullable=True)
    days_preference = db.Column(db.text(255), nullable=True)
    gender_preference = db.Column(db.text(255), nullable=True)
    experience_preference = db.Column(db.text(255), nullable=True)
    location_preference = db.Column(db.text(255), nullable=True)



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
    return render_template('leaderboard.html')

@app.route('/login_form', methods=["get"])
def login_form():
    email = request.form['loginemail']
    password = request.form['loginpw']
    user = User.query.filter_by(email=email).first()
    if user and password == user.password:
        return render_template('home.html')
    else:
        return render_template('login.html')



# def get_user_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect('/root/Database/database.db')
#         cur = db.cursor()
#         cur.execute('SELECT * FROM leaderboard')
#         db = cur.fetchall()
#     return db

# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

if __name__ == '__main__':
    app.run(debug=True)
