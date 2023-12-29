import requests
import json

class Leaderboard:
    def __init__(self, url):
        self.url = url
        print("Opening Database with URL: " + url)

        req = requests.get(self.url)

        if not req.ok:
            print("Error! Could not load database!")
            return
        
        print("Database initialisation complete.")
    
    def execute_query(self, query):
        query = self.url + "/query/?ordering=&export_json=&sql=" + query

        req = requests.get(query)
        if not req.ok:
            print("Could not execute query!")
            return 0

        data = json.loads(req.text)

        return data
    
    def execute_update(self, name, reps):
        query = self.url + "/insert/"

        form = {
            "chk_name": "on",
            "name": name,
            "chk_score": "on",
            "score": reps
        }

        req = requests.post(query, form)
        if not req.ok:
            print("Could not execute update!")

        return

    def update_leaderboard(self, data):
        """
        Update the leaderboard with new data.
        :param data: List of tuples (name, reps)
        """
        for entry in data:
            self.execute_update(entry[0], entry[1])

        return

    def get_leaderboard_data(self):
        """
        Get the current leaderboard data.
        :return: List of tuples (name, reps) ordered by reps in descending order
        """
        result = self.execute_query("SELECT+*+FROM+leaderboard+ORDER+BY+score+DESC")
        data = []

        for i in result:
            entry = [i["name"], i["score"]]
            data.append(entry)

        return list(tuple(d) for d in data)

    def insert_new_entry(self, name, reps):
        """
        Insert a new entry into the leaderboard.
        :param name: Name of the entry
        :param reps: Number of reps for the entry
        """
        query = self.url + "/insert/"
        form = {
            "chk_name": "on",
            "name": name,
            "chk_score": "on",
            "score": reps
        }

        req = requests.post(query, form)
        if not req.ok:
            print("Could not insert entry in leaderboard!")

        return

    def get_min_score(self):
        """
        Get the minimum score in the leaderboard.
        :return: Minimum score
        """
        result = self.execute_query("SELECT+score+FROM+leaderboard+ORDER+BY+score+DESC+LIMIT+1+OFFSET+9")

        return result[0]["score"]
    
# leaderboard = Leaderboard("http://danick.triantis.nl:8080/leaderboard")
# print(leaderboard.get_min_score())

# leaderboard.insert_new_entry("Senno", 71)
# print(leaderboard.get_min_score())
