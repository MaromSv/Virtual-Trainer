#Class for the leaderboard so that we can use OOP
import sqlite3
import os

class Leaderboard:
    def __init__(self, path):
        self.path = path

        if not os.path.exists(path):
            f = open(path, "x")
            print("Database created at: " + path)
    
        print("Connecting to Database: " + path)
        db = self.open_database()

        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS test(name, score)")
        self.close_database(db)
        print("Database initialisation complete.")

    def open_database(self):
        db = sqlite3.connect(self.path)
        return db
    
    def close_database(self, db):
        db.commit()
        db.close()
        

    def update_leaderboard(self, data):
        """
        Update the leaderboard with new data.
        :param data: List of tuples (name, reps)
        """
        db = self.open_database()

        for entry in data:        
            self.insert_new_entry(db, entry[0], entry[1])

        self.close_database(db)

    def get_leaderboard_data(self):
        """
        Get the current leaderboard data.
        :return: List of tuples (name, reps) ordered by reps in descending order
        """
        db = self.open_database()
        cursor = db.cursor()

        result = cursor.execute("SELECT * FROM test")
        output = result.fetchall()

        self.close_database(db)

        return output

    def insert_new_entry(self, db, name, reps):
        """
        Insert a new entry into the leaderboard.
        :param name: Name of the entry
        :param reps: Number of reps for the entry
        """
        cursor = db.cursor()
        cursor.execute("INSERT INTO test VALUES" + "('" + name + "'," + str(reps) + ")")
        db.commit()

    def get_min_score(self):
        """
        Get the minimum score in the leaderboard.
        :return: Minimum score
        """
        db = self.open_database()
        cursor = db.cursor()

        result = cursor.execute("SELECT * FROM test ORDER BY score ASC LIMIT 1")
        output = result.fetchone()[1]

        self.close_database(db)

        return output
    