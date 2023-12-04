import sqlite3
import os

path = "Assets/test.db"

# Function: connect_database(path)
# 
# Creates database file if it does not exists.
# Afterwards will connect to database and return 
# the database connection.
#
# Argument: path - the path of the database file
# Return: db - the connection to the specified database
# 
def connect_database(path):
    if not os.path.exists(path):
        f = open(path, "x")
        print("Database created at: " + path)
    else:
        print("Database already exists! Aborting...")
        exit()
    
    print("Connecting to Database: " + path)
    db = sqlite3.connect(path)
    return db

# Function: create_table(database)
# 
# Creates tables inside specified database file if they does not exist.
#
# Argument: database - the database in which to create the tables
# 
def create_tables(database):
    cursor = database.cursor()

    print("Creating 'login' table...")
    query = """CREATE TABLE IF NOT EXISTS login (\n
    id INTEGER PRIMARY KEY UNIQUE,\n
    username TEXT NOT NULL,\n
    password TEXT NOT NULL\n
    ) WITHOUT ROWID;"""
    cursor.execute(query)
    
    print("Creating 'users' table...")
    query = """CREATE TABLE IF NOT EXISTS users (\n
    id INTEGER PRIMARY KEY UNIQUE,\n
    firstName TEXT NOT NULL,\n
    lastName TEXT NOT NULL,\n
    age INTEGER NOT NULL,\n
    gender TEXT NOT NULL,\n
    location TEXT NOT NULL\n
    ) WITHOUT ROWID;"""
    cursor.execute(query)
    
    print("Creating 'buddysystem' table...")
    query = """CREATE TABLE IF NOT EXISTS buddysystem (\n
    id INTEGER PRIMARY KEY UNIQUE,\n
    available TEXT NOT NULL,\n
    gender TEXT NOT NULL,\n
    experience TEXT NOT NULL,\n
    location TEXT NOT NULL\n
    ) WITHOUT ROWID;"""
    cursor.execute(query)

    print("Creating 'leaderboard' table...")
    query = """CREATE TABLE IF NOT EXISTS leaderboard (\n
    id INTEGER PRIMARY KEY UNIQUE,\n
    exercise TEXT NOT NULL,\n
    score INTEGER NOT NULL\n
    ) WITHOUT ROWID;"""
    cursor.execute(query)
    database.commit()

# Function: check_tables(database)
# 
# Checks if all tables are present in the database
#
# Argument: database - the database of which to check the tables
# 
def check_tables(database):
    cursor = database.cursor()

    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='login';")
    print("Table 'login' exists: " + str(result.fetchall()))

    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    print("Table 'users' exists: " + str(result.fetchall()))

    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='buddysystem';")
    print("Table 'buddysystem' exists: " + str(result.fetchall()))
    
    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='leaderboard';")
    print("Table 'leaderboard' exists: " + str(result.fetchall()))


# Function: close_database(database)
# 
# Closes database connection
#
# Argument: database - the database of which to close the connection
# 
def close_database(database):
    database.commit()
    database.close()
    print("Database Connection Closed")

def init_database():
    path = "Assets/test.db"

    db = connect_database(path)
    create_tables(db)
    check_tables(db)
    close_database(db)

def add_entry():
    cmd = input("Choose a table: 1. login, 2. users, 3. buddysystem, 4. leaderboard? ")

    match cmd:
        case 1:
            add_login()
        case 2:
            add_user()
        case 3:
            add_buddysystem()
        case 4:
            add_leaderboard()
        case _:
            print("Unknown input!")
            add_entry()
            

def add_login():
    db = connect_database(path)

    id = input("Enter a 5-digit user ID: ")
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    cursor = db.cursor()
    cursor.execute("INSERT INTO login VALUES" + "(" + str(id) + "," + username + "," + password + ")")
    db.commit()

    close_database(db)

def add_user():
    db = connect_database(path)

    id = input("Enter a 5-digit user ID: ")
    firstname = input("Enter a first name: ")
    lastname = input("Enter a last name: ")
    age = input("Enter an age: ")
    gender = input("Enter a gender: ")
    location = input("Enter a location: ")

    cursor = db.cursor()
    cursor.execute("INSERT INTO users VALUES" + "(" + str(id) + "," + firstname + "," + lastname + "," + age + "," + gender + "," + location + ")")
    db.commit()

    close_database(db)

def add_buddysystem():
    db = connect_database(path)

    id = input("Enter a 5-digit user ID: ")
    available = input("Enter available day: ")
    gender = input("Enter a gender: ")
    experience = input("Enter the experience level: ")
    location = input("Enter a location: ")

    cursor = db.cursor()
    cursor.execute("INSERT INTO buddysystem VALUES" + "(" + str(id) + "," + available + "," + gender + "," + experience + "," + location + ")")
    db.commit()

    close_database(db)

def add_leaderboard():
    db = connect_database(path)

    id = input("Enter a 5-digit user ID: ")
    exercise = input("Enter an exercise: ")
    score = input("Enter a score: ")

    cursor = db.cursor()
    cursor.execute("INSERT INTO leaderboard VALUES" + "(" + str(id) + "," + exercise + "," + score + ")")
    db.commit()

    close_database(db)


if __name__ == "__main__":
    print("Database Initialiser for the Virtual Trainer\n\n")
    cmd = input("Do you want to initialise the database? ").lower()

    if (cmd == "y"):
        print("Initialisation Started!")
        init_database()
    elif (cmd == "yes"):
        print("Initialisation Started!")
        init_database()

    
    cmd = input("Do you want to make an entry in the database? ").lower()
    if (cmd == "y"):
        add_entry()
    elif (cmd == "yes"):
        add_entry()
    else:
        print("Program Exit")
        exit()
