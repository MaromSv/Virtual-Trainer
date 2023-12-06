import tkinter as tk
from tkinter import simpledialog

class DifficultyDialog(simpledialog.Dialog):
    def __init__(self, parent, title="Difficulty"):
        self.difficulty = None
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Choose Difficulty:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("easy")

        difficulties = ["Easy", "Medium", "Hard"]
        for i, difficulty in enumerate(difficulties):
            tk.Radiobutton(master, text=difficulty, variable=self.difficulty_var, value=difficulty.lower(), font=("Helvetica", 10)).grid(row=i+1, column=0, columnspan=3, padx=10, pady=5, sticky="w")

        return None

    def apply(self):
        self.difficulty = self.difficulty_var.get()
