import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
# import sqlite_web
import requests
import json
import copy

# test_url = "http://danick.triantis.nl:8080/users/query/?sql=INSERT+INTO+users+(chk_email,+chk_password,+chk_userid)+VALUES+(%27marios%27,+%27m1234%27,+%271%27);"
# x = requests.get(test_url)

import requests

# url = 'http://danick.triantis.nl:8080'
# data = {'query': 'SELECT * FROM leaderboard'}

# response = requests.get(url, json=data)

# print(response.json())

# url = "http://danick.triantis.nl:8080/leaderboard/query/?sql=SELECT+*+FROM+users;"

# current_userid = 0

# For Login page

def get_password(email):
    email.replace("@", "%40")
    email = "%22" + email + "%22"
    url = "http://danick.triantis.nl:8080/users/query/?ordering=&export_json=&sql=SELECT+password+FROM+%22users%22+WHERE+email%3D{}".format(email)
    x = requests.get(url)
    if x.text == "[]":
        return "email not found"
    password_db = json.loads(x.text)[0]["password"]
    return password_db

def get_userid(email):
    email.replace("@", "%40")
    url="http://danick.triantis.nl:8080/users/query/?ordering=&export_json=&sql=SELECT+userid+FROM+%22users%22+WHERE+email+%3D%3D+%22{}%22".format(email)
    x = requests.get(url)
    if x.text == "[]":
        return 0
    data = json.loads(x.text)[0]["userid"]
    session['userid'] = data


# For signup page

def createaccount(email,password,first_name,last_name,age,gender,experience,location):
    userid = get_max_userid() + 1
    insert_user(userid,email,password)
    insert_personal_form(userid,first_name,last_name,age,gender,experience,location)

def get_max_userid():
    url = "http://danick.triantis.nl:8080/users/query/?ordering=&export_json=&sql=SELECT+userid%0D%0AFROM+users%0D%0AWHERE+userid+IN+%28%0D%0A++++SELECT+MAX%28userid%29%0D%0A++++FROM+users%0D%0A%29"
    x = requests.get(url)
    if x.text == "[]":
        return 0
    data = json.loads(x.text)[0]["userid"]
    return data

def insert_personal_form(userid,first_name,last_name,age,gender,experience,location):
    url="http://danick.triantis.nl:8080/Personal_Form/query/?ordering=&export_ordering=&sql=INSERT+INTO+Personal_Form+%28userid%2Cfirst_name%2Clast_name%2Cage%2Cgender%2Cexperience%2Clocation%29%0D%0AVALUES+%28{}%2C%22{}%22%2C%22{}%22%2C{}%2C%22{}%22%2C%22{}%22%2C%22{}%22%29".format(userid,first_name,last_name,age,gender,experience,location)
    requests.get(url)

def insert_user(userid,email,password):
    email.replace("@", "%40")
    print(email)
    url = "http://danick.triantis.nl:8080/users/query/?ordering=&export_ordering=&sql=INSERT+INTO+users+%28userid%2Cemail%2Cpassword%29%0D%0AVALUES+%28{}%2C%22{}%22%2C%22{}%22%29".format(userid,email,password)
    requests.get(url)


# For home page
    
def update_personal_info(userid,first_name,last_name,age,gender,experience,location):
    url="http://danick.triantis.nl:8080/Personal_Form/query/?ordering=&export_ordering=&sql=UPDATE+%22Personal_Form%22%0D%0ASET+first_name%3D%22{}%22%2C+last_name%3D%22{}%22%2C+age%3D{}%2C+gender%3D%22{}%22%2C+experience%3D%22{}%22%2C+location%3D%22{}%22%0D%0AWHERE+userid%3D{}+".format(first_name,last_name,age,gender,experience,location,userid)
    requests.get(url)


# For leaderboard page
    
def get_leaderboard():
    url = "http://danick.triantis.nl:8080/leaderboard/query/?ordering=&export_json=&sql=SELECT+*+FROM+%22leaderboard%22+ORDER+BY+%22score%22+DESC;"
    x = requests.get(url)
    data = json.loads(x.text)
    print(data)
    return data

# For Buddy page
def insert_buddy_form(userid,days_available,gender_preference,age_preference,experience_preference,location_preference):
    days_available.replace(",", "%2C")
    experience_preference.replace(",", "%2C")
    if select_current_buddy_form(userid) == []:
        url="http://danick.triantis.nl:8080/Buddy_Form/query/?ordering=&export_ordering=&sql=INSERT+INTO+Buddy_Form+%28userid%2Cdays_available%2Cgender_preference%2Cage_preference%2Cexperience_preference%2Clocation_preference%29%0D%0AVALUES+%28{}%2C%22{}%22%2C%22{}%22%2C%22{}%22%2C%22{}%22%2C%22{}%22%29".format(userid,days_available,gender_preference,age_preference,experience_preference,location_preference)

    else:
        url="http://danick.triantis.nl:8080/Buddy_Form/query/?ordering=&export_ordering=&sql=UPDATE+Buddy_Form%0D%0ASET+days_available+%3D+%22{}%22%2C+gender_preference+%3D+%22{}%22%2C+age_preference+%3D+%22{}%22%2C+experience_preference+%3D+%22{}%22%2C+location_preference+%3D+%22{}%22%0D%0AWHERE+userid%3D%3D{}".format(days_available,gender_preference,age_preference,experience_preference,location_preference,userid)
    requests.get(url)


def select_current_buddy_form(userid):
    url = "http://danick.triantis.nl:8080/Buddy_Form/query/?ordering=&export_json=&sql=SELECT+userid+FROM+%22Buddy_Form%22%0D%0AWHERE+userid%3D%3D{}".format(userid)
    x = requests.get(url)
    data = json.loads(x.text)
    if data == []:
        return []
    else:
        return data[0]["userid"]
    
def delete_Buddy_Form(userid):
    url="http://danick.triantis.nl:8080/Buddy_Form/query/?ordering=&export_ordering=&sql=DELETE+FROM+%22Buddy_Form%22+WHERE+userid%3D%3D{}".format(userid)    
    requests.get(url)

def insert_Current_Buddy(userid,buddy_userid,common_days):
    url="http://danick.triantis.nl:8080/Current_Buddy/query/?ordering=&export_ordering=&sql=INSERT+INTO+%22Current_Buddy%22+%28userid%2C+buddy_userid%2C+common_days%29%0D%0AVALUES+%28{}%2C{}%2C%22{}%22%29".format(userid,buddy_userid,common_days)
    requests.get(url)
    url="http://danick.triantis.nl:8080/Current_Buddy/query/?ordering=&export_ordering=&sql=INSERT+INTO+%22Current_Buddy%22+%28userid%2C+buddy_userid%2C+common_days%29%0D%0AVALUES+%28{}%2C{}%2C%22{}%22%29".format(buddy_userid,userid,common_days)
    requests.get(url)
    
def days_available_to_bool(days_available):
    days_available = days_available.split(",")
    days_available_bool = [False,False,False,False,False,False,False]
    for i in days_available:
        if i == "Monday":
            days_available_bool[0] = True
        elif i == "Tuesday":
            days_available_bool[1] = True
        elif i == "Wednesday":
            days_available_bool[2] = True
        elif i == "Thursday":
            days_available_bool[3] = True
        elif i == "Friday":
            days_available_bool[4] = True
        elif i == "Saturday":
            days_available_bool[5] = True
        elif i == "Sunday":
            days_available_bool[6] = True
    return days_available_bool

def experience_preference_to_bool(experience_preference):
    experience_preference = experience_preference.split(",")
    experience_preference_bool = [False,False,False]
    for i in experience_preference:
        if i == "Beginner":
            experience_preference_bool[0] = True
        elif i == "Intermediate":
            experience_preference_bool[1] = True
        elif i == "Advanced":
            experience_preference_bool[2] = True
    return experience_preference_bool

def removeBadIndicies(listOfStuff, badIndicies):
    for index in badIndicies:
        listOfStuff.pop(index)
    return listOfStuff

def find_common_days(current_days_available,buddy_days_available):
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    common_days = []
    for i in range(7):
        if current_days_available[i] == True and buddy_days_available[i] == True:
            common_days.append(days[i])
    return common_days

def find_buddy(userid):
    url = 'http://danick.triantis.nl:8080/Personal_Form/query/?ordering=&export_json=&sql=SELECT+first_name%2C+last_name%2C+age%2C+gender%2C+experience%2C+location+FROM+%22Personal_Form%22+where+userid+%3D+{}'.format(session['userid'])
    x = requests.get(url)
    data = json.loads(x.text)
    # current_first_name = data[0]["first_name"]
    # current_last_name = data[0]["last_name"]
    current_age = data[0]["age"]
    # current_location = data[0]["location"]
    current_gender = data[0]["gender"]
    current_experience = data[0]["experience"]
    url = "http://danick.triantis.nl:8080/Buddy_Form/query/?ordering=&export_json=&sql=SELECT+days_available%2C+gender_preference%2C+age_preference%2C+experience_preference+FROM+%22Buddy_Form%22%0D%0AWHERE+userid+%3D%3D+{}".format(userid)
    x = requests.get(url)
    data = json.loads(x.text)
    if data == []:
        return []
    current_days_available = data[0]["days_available"]
    current_days_available = days_available_to_bool(current_days_available)
    current_gender_preference = data[0]["gender_preference"]
    current_experience_preference = data[0]["experience_preference"]
    current_experience_preference = experience_preference_to_bool(current_experience_preference)
    # current_location_preference = "Campus"
    current_age_preference = data[0]["age_preference"]

    buddies = []

    url = "http://danick.triantis.nl:8080/Current_Buddy/query/?ordering=&export_json=&sql=SELECT+Buddy_Form.userid%2C+age%2C+gender%2C+experience%2C+days_available%2C+gender_preference%2C+experience_preference%2C+age_preference%0D%0AFROM+Buddy_Form%2C+Personal_Form%0D%0AWHERE+Personal_Form.userid+%3D%3D+Buddy_Form.userid+AND+Personal_Form.userid+%21%3D+{}".format(userid)
    x = requests.get(url)
    data = json.loads(x.text)
    if data == []:
        return []
    print(data)
    for i in data:
        buddy_userid = i["userid"]
        buddy_age = i["age"]
        buddy_gender = i["gender"]
        buddy_experience = i["experience"]
        buddy_days_available = i["days_available"]
        buddy_days_available = days_available_to_bool(buddy_days_available)
        buddy_gender_preference = i["gender_preference"]
        buddy_experience_preference = i["experience_preference"]
        buddy_experience_preference = experience_preference_to_bool(buddy_experience_preference)
        buddy_age_preference = i["age_preference"]
        buddies.append([buddy_userid,buddy_experience,buddy_age,buddy_gender,buddy_gender_preference,buddy_days_available,buddy_experience_preference,buddy_age_preference])
        # print(buddy_userid,buddy_days_available,buddy_experience_preference)
    print(buddies)
    # ALGORITHM 
    possibleBuddies = copy.deepcopy(buddies)
    badBuddyIndicies = []

    #Remove yourself from possible buddies:
    for index, buddy in enumerate(possibleBuddies):
            if buddy[0] == session['userid']:
                badBuddyIndicies.append(index)

    #Remove all possible buddies that dont abide by gender requirement
    if current_gender_preference == 'Same':
        for index, buddy in enumerate(possibleBuddies):
            if buddy[3] != current_gender:
                badBuddyIndicies.append(index)
    
    #Remove people that dont share days with you
    for index, buddy in enumerate(possibleBuddies):
        sharedDay = False
        for i in range(7):
            if buddy[5][i] == True and current_days_available[i] == True:
                sharedDay = True

        if sharedDay == False:
            badBuddyIndicies.append(index)

    #Remove people that dont share experience with you
    for i in range(len(current_experience_preference)):
        if current_experience_preference[i] == False and i == 0:
            for index, buddy in enumerate(possibleBuddies):
                if buddy[1] == 'Beginner':
                    badBuddyIndicies.append(index)
        elif current_experience_preference[i] == False and i == 1:
            for index, buddy in enumerate(possibleBuddies):
                if buddy[1] == 'Intermediate':
                    badBuddyIndicies.append(index)
        elif current_experience_preference[i] == False and i == 2:
            for index, buddy in enumerate(possibleBuddies):
                if buddy[1] == 'Advanced':
                    badBuddyIndicies.append(index)

    #Remove duplicates from badBuddyIndicies
    badBuddyIndicies = list(dict.fromkeys(badBuddyIndicies))
    badBuddyIndicies.sort(reverse=True)
    #Remove unsuitable buddies
    possibleBuddies = removeBadIndicies(possibleBuddies, badBuddyIndicies)

    buddyAgeDifferences = []
    for index, buddy in enumerate(possibleBuddies):
        buddyAgeDifferences.append((buddy[0], abs(buddy[2] - current_age), index))
    
    sorted (
    buddyAgeDifferences, 
    key=lambda x: x[1]
    )
    if (len(buddyAgeDifferences) == 0):
        return -1
    else: 
        buddy_userid = buddyAgeDifferences[0][0]
        common_days = find_common_days(current_days_available,possibleBuddies[buddyAgeDifferences[0][2]][5])
        insert_Current_Buddy(userid,buddy_userid,common_days) #TODO fix commondays and buddy_userid
        delete_Buddy_Form(userid)
        delete_Buddy_Form(buddy_userid)




    
# Usefull(less) stuff

# def sort_users():
#     url = "http://danick.triantis.nl:8080/users/query/?ordering=&export_ordering=&sql=SELECT+*+FROM+users%0D%0AORDER+BY+userid%3B"
#     requests.get(url)

# def sort_Buddy_Form():
#     url = "http://danick.triantis.nl:8080/Buddy_Form/query/?ordering=&export_ordering=&sql=SELECT+*+FROM+Buddy_Form%0D%0AORDER+BY+userid%3B"
#     requests.get(url)

# def sort_personal_from():
#     url = "http://danick.triantis.nl:8080/Personal_Form/query/?ordering=&export_ordering=&sql=SELECT+*+FROM+Personal_Form%0D%0AORDER+BY+userid%3B"
#     requests.get(url)

# def delete_personal_form(userid):
#     url="http://danick.triantis.nl:8080/Personal_Form/query/?ordering=&export_ordering=&sql=DELETE+FROM+%22Personal_Form%22+WHERE+userid%3D%3D{}".format(userid)    
#     requests.get(url)


app = Flask(__name__,template_folder='templates',static_folder='static')
app.config["SESSION_PERMANENT"] = True
app.secret_key = 'BAD_SECRET_KEY'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
def home():
    url = 'http://danick.triantis.nl:8080/Personal_Form/query/?ordering=&export_json=&sql=SELECT+first_name%2C+last_name%2C+age%2C+gender%2C+experience%2C+location+FROM+%22Personal_Form%22+where+userid+%3D+{}'.format(session['userid'])
    x = requests.get(url)
    data = json.loads(x.text)
    first_name = data[0]["first_name"]
    last_name = data[0]["last_name"]
    age = data[0]["age"]
    location = data[0]["location"]
    gender = data[0]["gender"]
    experience = data[0]["experience"]
    return render_template('home.html', first_name = first_name, last_name = last_name, age = age, gender = gender, experience = experience, location = location)

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/buddy')
def buddy():
    url = 'http://danick.triantis.nl:8080/Current_Buddy/query/?ordering=&export_json=&sql=SELECT+*+FROM+%22Current_Buddy%22+where+userid+%3D+{}+'.format(session['userid'])
    x = requests.get(url)
    data = json.loads(x.text)
    if data == []:
        return  render_template('buddy.html', unga = ': No current buddy', email = '-', first_name = '-', last_name = '-', age = '-', gender = '-', experience = '-', location = '-', common_days = '-')
    else:
        buddy_id = data[0]['buddy_userid']
        common_days = data[0]['common_days']
        buddy_url = 'http://danick.triantis.nl:8080/users/query/?ordering=&export_json=&sql=SELECT+email+FROM+%22users%22+where+userid+%3D+{}'.format(buddy_id)
        x2 = requests.get(buddy_url)
        buddy_info_json = json.loads(x2.text)
        buddy_email = buddy_info_json[0]['email']
        print('buddy email: ' + buddy_email)
        print('buddy common days' + common_days)
        buddy_url_2 = 'http://danick.triantis.nl:8080/Personal_Form/query/?ordering=&export_json=&sql=SELECT+*+FROM+%22Personal_Form%22+where+userid+%3D+{}'.format(buddy_id)
        x3 = requests.get(buddy_url_2)
        buddy_info_json_2 = json.loads(x3.text)
        first_name = buddy_info_json_2[0]["first_name"]
        last_name = buddy_info_json_2[0]["last_name"]
        age = buddy_info_json_2[0]["age"]
        location = buddy_info_json_2[0]["location"]
        gender = buddy_info_json_2[0]["gender"]
        experience = buddy_info_json_2[0]["experience"]

        return render_template('buddy.html', email = buddy_email, first_name = first_name, last_name = last_name, age = age, gender = gender, location = location, experience = experience, common_days = common_days)

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
        get_userid(email)
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
    
@app.route('/personal_form', methods=['POST'])
def personal_form():
    first_name = request.form['first_name_enter']
    last_name = request.form['last_name_enter']
    age = request.form['age_enter']
    gender = request.form.getlist('gender_enter')
    experience = request.form.getlist('experience_enter')
    location = request.form.getlist('location_enter')
    if first_name == "" or last_name == "" or age == "" or gender == [] or experience == [] or location == []:
        return redirect(url_for('home'))
    else:
        gender = gender[0]
        experience = experience[0]
        location = location[0]
        update_personal_info(session['userid'],first_name,last_name,age,gender,experience,location)
        return redirect(url_for('home'))
    
@app.route('/buddy_form', methods=['POST'])
def buddy_form():
    days_available= request.form.getlist('days_available_enter')
    gender_preference = request.form.getlist('gender_preference_enter')
    experience_preference = request.form.getlist('experience_preference_enter')
    location_preference = request.form.getlist('location_preference_enter')
    age_preference = request.form.getlist('age_preference_enter')
    if days_available == [] or gender_preference == [] or experience_preference == [] or location_preference == [] or age_preference == []:
        return redirect(url_for('buddy'))
    else:
        gender_preference = gender_preference[0]
        age_preference = age_preference[0]
        location_preference = location_preference[0]
        experience_preference = ','.join(experience_preference)
        days_available = ','.join(days_available)
        insert_buddy_form(session['userid'],days_available,gender_preference,age_preference,experience_preference,location_preference)
        find_buddy(session['userid'])
        return redirect(url_for('buddy'))


if __name__ == '__main__':
    app.run(debug=True)
