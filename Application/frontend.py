import tkinter as tk
from tkinter import ttk
import cv2
from ttkthemes import ThemedStyle
from leaderboard import Leaderboard
from pushupCounter import pushUpCounter
from PIL import Image, ImageTk

class VirtualTrainerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Trainer App")
        self.root.geometry("600x820")  # Adjusted for a tablet-sized screen

        # Apply a themed style
        self.style = ThemedStyle(self.root)
        self.style.set_theme("equilux")  # You can choose a different theme

        # Customize the color for some specific elements
        self.style.configure("TLabel", foreground="#FFD700", background="#1E1E1E")  # Yellow text
        self.style.configure("TFrame", background="#1E1E1E")  # Background color for frames
        self.style.map("TButton", background=[('active', '#FF5733')])  # Background color for buttons on mouse hover

        # Customize the color for the notebook and tabs
        self.style.configure("TNotebook", background="#1E1E1E")  # Original gray background color for the notebook
        self.style.configure("TNotebook.Tab", background="#1E1E1E", foreground="#FFD700")  # Tab color

        # Disable focus highlight
        self.style.map("TNotebook.Tab", foreground=[('selected', '#FFD700'), ('active', '#FFD700')])
        self.style.configure("TNotebook.Tab", focuscolor=self.style.configure(".")["background"])

        self.leaderboard = Leaderboard()
        self.pushup_counter_frame = None  # Initialize the push-up counter frame reference
        self.create_widgets()


    def create_widgets(self):
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)

        # Create pages
        self.create_home_page()
        self.create_leaderboard_page()
        self.create_workout_page()

        # Pack the notebook
        self.notebook.pack(expand=True, fill="both")

    def create_home_page(self):
        home_frame = ttk.Frame(self.notebook)
        self.notebook.add(home_frame, text="Home")

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

        # TODO: LOAD LEADERBOARD DATA FROM DATABASE OVER HERE
        self.leaderboard.insert_new_entry("Marom", 100)
        print(self.leaderboard.get_leaderboard_data())
        # Get leaderboard data
        leaderboard_data = self.leaderboard.get_leaderboard_data()

        # Insert data into the Treeview
        for idx, row in enumerate(leaderboard_data, start=1):
            self.leaderboard_tree.insert("", "end", values=(idx,) + row)

        # Pack the Treeview
        self.leaderboard_tree.pack(padx=20, pady=10)

        # Button to start push-up counter
        attempt_record_button = ttk.Button(leaderboard_frame, text="Attempt Record", command=self.start_pushup_counter)
        attempt_record_button.pack(pady=20)

    def create_workout_page(self):
        workout_frame = ttk.Frame(self.notebook)
        self.notebook.add(workout_frame, text="Start workout")

        # Workout Page Widgets
        label = ttk.Label(workout_frame, text="Select a Workout", font=("Helvetica", 16, "bold"))
        label.pack(pady=20)

        # Add your workout selection widgets here

    def create_pushup_counter_page(self):
         # Hide the tabs during push-up counter
        self.notebook.pack_forget()

        # Create a new frame for push-up counter
        self.pushup_counter_frame = ttk.Frame(self.root)
        self.pushup_counter_frame.pack(expand=True, fill="both")

        # Add a button to go back to the leaderboard
        back_to_leaderboard_button = ttk.Button(self.pushup_counter_frame, text="Back to Leaderboard", command=self.back_to_leaderboard)
        back_to_leaderboard_button.pack(pady=20)

    def convert_opencv_to_tkinter(self, opencv_image):
        # Convert the OpenCV image to a PhotoImage
        pil_image = Image.fromarray(opencv_image)
        tk_image = ImageTk.PhotoImage(pil_image)
        return tk_image
    
    def start_pushup_counter(self):
        self.create_pushup_counter_page()

        reps = pushUpCounter()
        minLeaderBoard = self.leaderboard.get_min_score()

        lengthLeaderboard = len(self.leaderboard.get_leaderboard_data())
        if reps > minLeaderBoard or lengthLeaderboard < 10:
            print("You made it onto the leaderboard") #TODO: Replace with code to insert name and add entry to leaderboard
        else:
            print("You didnt quite make it onto the leaderboard, better luck next time")
        

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

