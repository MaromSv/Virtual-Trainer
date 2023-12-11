import tkinter as tk
from tkinter import ttk
import cv2
from ttkthemes import ThemedStyle
from leaderboard import Leaderboard
from pushupCounter import pushUpCounter
from tkinter import simpledialog as sd
import videoPlayer
from tkinter import messagebox


class VirtualTrainerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Trainer App")
        self.root.geometry("600x800")  # Adjusted for a tablet-sized screen
        self.root.attributes('-fullscreen', True)
        # Apply a themed style
        self.style = ThemedStyle(self.root)
        self.style.set_theme("equilux")  # You can choose a different theme

        # Customize the color for some specific elements
        self.style.configure("TLabel", foreground="#FFD700", background="#1E1E1E")  # Yellow text
        self.style.configure("TFrame", background="#1E1E1E")  # Background color for frames
        self.style.map("TButton", background=[('active', '#FF5733')])  # Background color for buttons on mouse hover

        # Customize the color for the notebook and tabs
        self.style.configure('lefttab.TNotebook', tabposition='s')
        self.style.configure("TNotebook", background="#1E1E1E")  # Original gray background color for the notebook
        self.style.configure("TNotebook.Tab", background="#1E1E1E", foreground="#FFD700")  # Tab color

        # Disable focus highlight
        self.style.map("TNotebook.Tab", foreground=[('selected', '#FFD700'), ('active', '#FFD700')])
        self.style.configure("TNotebook.Tab", focuscolor=self.style.configure(".")["background"])

        #Size/Shape of tabs:
        self.style.configure("TNotebook.Tab", padding = (52, 20), font=('Helvetica', 15), tabmargins=0)
       

        
        # self.leaderboard = Leaderboard("Assets/database.db")
    
        self.leaderboard = Leaderboard("Application\Assets\db\database.db")

        self.pushup_counter_frame = None  # Initialize the push-up counter frame reference
        self.create_widgets()


    def create_widgets(self):
        # Create a notebook (Dtabbed interface)
        self.notebook = ttk.Notebook(self.root, style = 'lefttab.TNotebook')

        # Create pages
        self.create_home_page()
        self.create_workout_page()
        self.create_leaderboard_page()
      

        # Pack the notebook
        self.notebook.pack(expand=True, fill="both")

    def create_home_page(self):
        home_frame = ttk.Frame(self.notebook)
        self.notebook.add(home_frame, text="Home")

    
        #TODO: add explanations or something to the page
        
        # Home Page Widgets
        label = ttk.Label(home_frame, text="Welcome to Virtual Trainer", font=("Helvetica", 30, "bold"))
        label.pack(pady=20)

    def create_leaderboard_page(self):
        leaderboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(leaderboard_frame, text="Leaderboard")

        # Leaderboard Page Widgets
        leaderboard_label = ttk.Label(leaderboard_frame, text="Leaderboard", font=("Helvetica", 30, "bold"))
        leaderboard_label.pack(pady=20)

        # Create a Treeview widget for the leaderboard
        columns = ("Rank", "Name", "# of Reps")
        self.leaderboard_tree = ttk.Treeview(leaderboard_frame, columns=columns, show="headings", height=10)

        # Configure column headings
        for col in columns:
            self.leaderboard_tree.heading(col, text=col)
            self.leaderboard_tree.column(col, anchor="center")

        # Get leaderboard data
        leaderboard_data = self.leaderboard.get_leaderboard_data()
        leaderboard_data = sorted(leaderboard_data, key=lambda x: int(x[1]), reverse=True)


        # Insert data into the Treeview
        for idx, row in enumerate(leaderboard_data, start=1):
            self.leaderboard_tree.insert("", "end", values=(idx,) + row)

        # Pack the Treeview
        self.leaderboard_tree.pack(padx=20, pady=10)

        # Button to start push-up counter
        attempt_record_button = ttk.Button(leaderboard_frame, text="Attempt Record", command=self.start_pushup_counter, takefocus=False)
        attempt_record_button.pack(pady=20)

    def create_workout_page(self):
        workout_frame = ttk.Frame(self.notebook)
        self.notebook.add(workout_frame, text="Start workout")

        # Workout Page Widgets
        label = ttk.Label(workout_frame, text="Select a Workout", font=("Helvetica", 30, "bold"))
        label.pack(pady=20)

        # Add Buttons for Each Type of Workout
        custom_style = ttk.Style()
        custom_style.configure("TButton", font=("Helvetica", 20))  # Change the font size as needed

        button1 = ttk.Button(workout_frame, text="Chest Workout", command=lambda: self.start_workout("Chest"), takefocus=False, style="TButton")
        button1.pack(pady=20)

        button2 = ttk.Button(workout_frame, text="Cardio Workout", command=lambda: self.start_workout("Cardio"), takefocus=False, style="TButton")
        button2.pack(pady=20)

        button3 = ttk.Button(workout_frame, text="Core Workout", command=lambda: self.start_workout("Core"), takefocus=False, style="TButton")
        button3.pack(pady=20)

        button4 = ttk.Button(workout_frame, text="Legs Workout", command=lambda: self.start_workout("Legs"), takefocus=False, style="TButton")
        button4.pack(pady=20)




    def get_input_name(self):
        result = sd.askstring("Name", "Enter your name:")
        if result:
            # Do something with the user input (e.g., print it)
            return result
        #TODO:HANDLE ERRORS


   
    def get_difficulty(self):
        resultValid = False
        while not resultValid:
            result = sd.askinteger("Difficulty", "Enter the desired difficulty (1-3): ")

            validInputs = [None, 1, 2, 3]

            if result not in validInputs:
                messagebox.showinfo("Error", "Pick one of the following [1, 2, 3]")
            else:
                resultValid = True
        
        return result

    def start_workout(self, workout_type):
        diff = self.get_difficulty()
        print(workout_type)
        if (workout_type == 'Chest'):
            videoPlayer.playVideo("Application\Assets\Video\pushup" + str(diff) + ".mp4")
        elif (workout_type == 'Core'):
            videoPlayer.playVideo("Application\Assets\Video\situp" + str(diff) + ".mp4")
        elif (workout_type == 'Legs'):
            videoPlayer.playVideo("Application\Assets\Video\squat" + str(diff) + ".mp4")
        # else: 
        #     videoPlayer.playVideo("Assets\Video\VID-20231204-WA0008.mp4")

    def refresh_page(self):
        self.notebook.destroy()
        self.create_widgets()

    def start_pushup_counter(self):
        # reps = pushUpCounter()

        reps = 7
        minLeaderBoard = self.leaderboard.get_min_score()

        lengthLeaderboard = len(self.leaderboard.get_leaderboard_data())
        print(minLeaderBoard)
        # try:

        if reps > minLeaderBoard or lengthLeaderboard < 10:
            print("You made it onto the leaderboard") 
            name = self.get_input_name()
            self.leaderboard.insert_new_entry(name, reps)
            print(self.leaderboard.get_leaderboard_data)
            self.refresh_page()
            self.navigate_to_leaderboard()
        else:
            print("You didnt quite make it onto the leaderboard, better luck next time")

        # except:
        #     print("PushUp Counter failed") #Reps = None
        

    def navigate_to_home(self):
        self.notebook.select(0)  # Switch to the Home page

    def navigate_to_leaderboard(self):
        self.notebook.select(2)  # Switch to the Leaderboard page

    def navigate_to_workout(self):
        self.notebook.select(1)  # Switch to the Workout page

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualTrainerApp(root)
    root.mainloop()

