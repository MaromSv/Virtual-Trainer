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
    
    print("Connecting to Database: " + path)
    db = sqlite3.connect(path)
    return db

# Function: create_table(database)
# 
# Creates table inside specified database file if it does not exist.
#
# Argument: database - the database in which to create the table
# 
def create_table(database):
    cursor = database.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS trainer(name, score)")
    
# Function: insert_data(database, name, score)
# 
# Inserts data entry to specified database file.
#
# Argument: database - the database in which to insert data
# Argument: name - the name of the new data entry
# Argument: score - the score of the new data entry
# 
def insert_data(database, name, score):
    cursor = database.cursor()

    cursor.execute("INSERT INTO trainer VALUES" + "('" + name + "'," + score + ")")
    database.commit()

# Function: remove_data(database, name)
# 
# Removes data entry from specified database file.
#
# Argument: database - the database from which to remove data
# Argument: name - the name of the to be deleted data entry
# 
def remove_data(database, name):
    cursor = database.cursor()

    cursor.execute("DELETE FROM trainer WHERE name='" + name + "'")
    database.commit()

# Function: print_database(database)
# 
# Prints all entries in the database
#
# Argument: database - the database from which to remove data
# 
def print_database(database):
    cursor = database.cursor()

    result = cursor.execute("SELECT * FROM Trainer")
    print(result.fetchall())

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
