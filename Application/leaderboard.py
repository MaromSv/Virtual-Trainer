#Class for the leaderboard so that we can use OOP
class Leaderboard:
    def __init__(self):
        self.leaderboard_data = []

    def update_leaderboard(self, data):
        """
        Update the leaderboard with new data.
        :param data: List of tuples (name, reps)
        """
        self.leaderboard_data = data

    def get_leaderboard_data(self):
        """
        Get the current leaderboard data.
        :return: List of tuples (name, reps) ordered by reps in descending order
        """
        return sorted(self.leaderboard_data, key=lambda x: x[1], reverse=True)

    def fill_leaderboard_from_array(self, array_data):
        """
        Fill the leaderboard with data from a 2D array.
        :param array_data: List of tuples (name, reps) from the 2D array
        """
        self.update_leaderboard(array_data)

    def insert_new_entry(self, name, reps):
        """
        Insert a new entry into the leaderboard.
        :param name: Name of the entry
        :param reps: Number of reps for the entry
        """
        self.leaderboard_data.append((name, reps))

    def get_min_score(self):
            """
            Get the minimum score in the leaderboard.
            :return: Minimum score
            """
            if not self.leaderboard_data:
                return None

            return min(entry[1] for entry in self.leaderboard_data)