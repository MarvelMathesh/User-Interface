import tkinter as tk
from tkinter import ttk
import time
import threading

class CookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Interface")
        self.root.geometry("480x320")

        # for dropdown menu
        self.recipe = tk.StringVar(value="Select a Recipe")
        ttk.Label(root, text="Choose a Recipe:", font=("Arial", 14)).pack(pady=10)
        recipes = ["Pasta", "Soup", "Salad"] 
        self.menu = ttk.Combobox(root, values=recipes, textvariable=self.recipe, state="readonly", font=("Arial", 12))
        self.menu.pack(pady=5)

        self.start = ttk.Button(root, text="Start", command=self.start_cooking)
        self.start.pack(pady=10)
        self.stop = ttk.Button(root, text="Stop", command=self.stop_cooking, state=tk.DISABLED)
        self.stop.pack(pady=5)
        self.label = ttk.Label(root, text="", font=("Arial", 14))
        self.label.pack(pady=10)

        self.running = False

    def start_cooking(self):
        if self.recipe.get() == "Select a Recipe":
            self.label.config(text="Select a recipe!")
            return
        
        self.running = True
        self.start.config(state=tk.DISABLED)
        self.stop.config(state=tk.NORMAL)
        self.label.config(text=f"Cooking {self.recipe.get()}...")

        threading.Thread(target=self.cook_recipe, daemon=True).start()

    def cook_recipe(self):
        time.sleep(3)
        if self.running:
            self.label.config(text="Cooking Done!")
            self.start.config(state=tk.NORMAL)
            self.stop.config(state=tk.DISABLED)

    def stop_cooking(self):
        self.running = False
        self.label.config(text="Cooking Stopped!")
        self.start.config(state=tk.NORMAL)
        self.stop.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CookingApp(root)
    root.mainloop()
