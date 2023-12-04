import tkinter as tk
from tkinter import ttk
import cv2
from ttkthemes import ThemedStyle
from leaderboard import Leaderboard
from pushupCounter import pushUpCounter
from tkinter import simpledialog
import videoPlayer

class VirtualTrainerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Trainer App")
        self.root.geometry("600x800")  # Adjusted for a tablet-sized screen

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
    
        self.leaderboard = Leaderboard("Application/Assets/database.db")

        self.pushup_counter_frame = None  # Initialize the push-up counter frame reference
        self.create_widgets()


    def create_widgets(self):
        # Create a notebook (tabbed interface)
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
        label = ttk.Label(home_frame, text="Welcome to Virtual Trainer", font=("Helvetica", 16, "bold"))
        label.pack(pady=20)

    def create_leaderboard_page(self):
        leaderboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(leaderboard_frame, text="Leaderboard")

        # Leaderboard Page Widgets
        leaderboard_label = ttk.Label(leaderboard_frame, text="Leaderboard", font=("Helvetica", 16, "bold"))
        leaderboard_label.pack(pady=20)

        # Create a Treeview widget for the leaderboard
        columns = ("Rank", "Name", "# of Reps")
        self.leaderboard_tree = ttk.Treeview(leaderboard_frame, columns=columns, show="headings", height=10)

        # Configure column headings
        for col in columns:
            self.leaderboard_tree.heading(col, text=col)
            self.leaderboard_tree.column(col, anchor="center")


        # data = [("Marom", 23), ("Bilal", 31), ("Danick", 18), ("Thanos", 25), ("Johan", 42), 
        #         ("Marios", 50), ("Nicky", 11), ("Yusef", 5), ("Jan", 10), ("Emma", 8)]
        # self.leaderboard.update_leaderboard(data)

        # TODO: LOAD LEADERBOARD DATA FROM DATABASE OVER HERE
        # self.leaderboard.insert_new_entry("Marom", 100)


        # print(self.leaderboard.get_leaderboard_data())
        # Get leaderboard data
        leaderboard_data = self.leaderboard.get_leaderboard_data()

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
        label = ttk.Label(workout_frame, text="Select a Workout", font=("Helvetica", 16, "bold"))
        label.pack(pady=20)

        # Add Buttons for Each Type of Workout
        button1 = ttk.Button(workout_frame, text="Core Workout", command=lambda: self.start_workout("Core Workout"), takefocus=False)
        button1.pack(pady=10)

        button2 = ttk.Button(workout_frame, text="Cardio Workout", command=lambda: self.start_workout("Back Workout"), takefocus=False)
        button2.pack(pady=10)

        button3 = ttk.Button(workout_frame, text="Chest Workout", command=lambda: self.start_workout("Chest Workout"), takefocus=False)
        button3.pack(pady=10)

        button4 = ttk.Button(workout_frame, text="Legs Workout", command=lambda: self.start_workout("Legs Workout"), takefocus=False)
        button4.pack(pady=10)



    def get_input(self):
        result = simpledialog.askstring("Name", "Enter your name:")
        if result:
            # Do something with the user input (e.g., print it)
            return result

    def start_workout(self, workout_type):
        # Logic for starting workout type 1
        print("Starting Workout of type: " + workout_type)
        videoPlayer.playVideo("Assets\Video\VID-20231204-WA0002.mp4")


        # Add your workout selection widgets here

    def create_pushup_counter_page(self):
         # Hide the tabs during push-up counter
        self.notebook.pack_forget()

        # Create a new frame for push-up counter
        self.pushup_counter_frame = ttk.Frame(self.root)
        self.pushup_counter_frame.pack(expand=True, fill="both")

        # Add a button to go back to the leaderboard
        back_to_leaderboard_button = ttk.Button(self.pushup_counter_frame, text="Back to Leaderboard",  command=self.back_to_leaderboard, takefocus=False)
        back_to_leaderboard_button.pack(pady=20)

    def convert_opencv_to_tkinter(self, opencv_image):
        # Convert the OpenCV image to a PhotoImage
        pil_image = Image.fromarray(opencv_image)
        tk_image = ImageTk.PhotoImage(pil_image)
        return tk_image
    
    def start_pushup_counter(self):
        #TODO: ADD threading 
        self.create_pushup_counter_page()
        reps = pushUpCounter()


        minLeaderBoard = self.leaderboard.get_min_score()

        lengthLeaderboard = len(self.leaderboard.get_leaderboard_data())
    
        try:

            if reps > minLeaderBoard or lengthLeaderboard < 10:
                print("You made it onto the leaderboard") 
                name = self.get_input()
                self.leaderboard.insert_new_entry(reps, name)
            else:
                print("You didnt quite make it onto the leaderboard, better luck next time")

        except:
            print("PushUp Counter failed") #Reps = None
        

    def back_to_leaderboard(self):
        # Destroy the pushup_counter_frame
        if self.pushup_counter_frame:
            self.pushup_counter_frame.destroy()

        # Show the tabs again
        self.notebook.pack(expand=True, fill="both")

    def navigate_to_home(self):
        self.notebook.select(0)  # Switch to the Home page

    def navigate_to_leaderboard(self):
        self.notebook.select(1)  # Switch to the Leaderboard page

    def navigate_to_workout(self):
        self.notebook.select(2)  # Switch to the Workout page

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualTrainerApp(root)
    root.mainloop()

