#Class for the leaderboard so that we can use OOP
import sqlite3
import os

class Leaderboard:
    def __init__(self, path):
        if not os.path.exists(path):
            f = open(path, "x")
            print("Database created at: " + path)
    
        print("Connecting to Database: " + path)
        self.db = sqlite3.connect(path)

        cursor = self.db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS leaderboard(name, score)")


    def update_leaderboard(self, data):
        """
        Update the leaderboard with new data.
        :param data: List of tuples (name, reps)
        """
        for entry in data:        
            self.insert_new_entry(entry[0], entry[1])

    def get_leaderboard_data(self):
        """
        Get the current leaderboard data.
        :return: List of tuples (name, reps) ordered by reps in descending order
        """
        cursor = self.db.cursor()
        result = cursor.execute("SELECT * FROM leaderboard")

        return result.fetchall()

    def insert_new_entry(self, name, reps):
        """
        Insert a new entry into the leaderboard.
        :param name: Name of the entry
        :param reps: Number of reps for the entry
        """
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO leaderboard VALUES" + "('" + name + "'," + str(reps) + ")")
        self.db.commit()

    def get_min_score(self):
        """
        Get the minimum score in the leaderboard.
        :return: Minimum score
        """
        cursor = self.db.cursor()
        result = cursor.execute("SELECT * FROM leaderboard ORDER BY score ASC LIMIT 1")

        return result.fetchone()[1]
    
    def close(self):
        self.db.commit()
        self.db.close()
        print("Database Connection Closed")