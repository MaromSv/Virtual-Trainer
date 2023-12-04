import sqlite3
import os

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
# Creates table inside specified database file if it does not exist.
#
# Argument: database - the database in which to create the table
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


if __name__ == "__main__":
    print("Database Initialiser for the Virtual Trainer\n\n")
    cmd = input("Are you sure you want to initialise the database? ").lower()

    if (cmd == "y"):
        print("Initialisation Started!")
        init_database()
    elif (cmd == "yes"):
        print("Initialisation Started!")
        init_database()
    else:
        print("Initialisation Aborted!")
        exit()
