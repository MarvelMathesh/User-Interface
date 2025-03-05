import tkinter as tk
import customtkinter as ctk
import threading
import time

class RecipeManager:
    RECIPES = {
        "Pasta": {
            "icon": "🍝",
            "color": "#FF6B6B",
            "time": 5,
            "description": "Classic Italian Pasta",
            "steps": [
                "Boil water",
                "Cook pasta",
                "Prepare sauce",
                "Combine & serve"
            ]
        },
        "Salad": {
            "icon": "🥗",
            "color": "#45B7D1",
            "time": 1,
            "description": "Fresh Garden Salad",
            "steps": [
                "Wash vegetables",
                "Chop ingredients",
                "Mix",
                "Toss & garnish"
            ]
        },
        "Soup": {
            "icon": "🍲",
            "color": "#D35400",
            "time": 2,
            "description": "Hot & Tasty Soup",
            "steps": [
                "Boil water",
                "Add ingredients",
                "Stir",
                "Serve hot"
            ]
        }
    }

class CookingApp:
    def __init__(self):
        # App setup
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.geometry("600x800")
        self.root.title("User Interface")
        self.root.resizable(False, False)

        # State variables
        self.current_recipe = tk.StringVar(value="Select Recipe")
        self.cooking_thread = None
        self.is_cooking = False

        # Setup UI
        self.create_ui()

    def create_ui(self):
        # Main container
        main_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="transparent")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Header
        header = ctk.CTkLabel(
            main_frame, 
            text="User Interface", 
            font=("Arial Rounded", 24, "bold")
        )
        header.pack(pady=(0, 20))

        # Recipe Selection Frame
        recipe_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        recipe_frame.pack(fill="x", pady=10)

        # Recipe Dropdown
        self.recipe_dropdown = ctk.CTkOptionMenu(
            recipe_frame, 
            values=list(RecipeManager.RECIPES.keys()),
            variable=self.current_recipe,
            command=self.update_recipe_details,
            width=300,
            dynamic_resizing=False,
            font=("Arial", 16)
        )
        self.recipe_dropdown.pack(expand=True)

        # Recipe Details Container
        self.details_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.details_container.pack(fill="x", pady=10)

        # Recipe Icon and Description
        self.recipe_icon_label = ctk.CTkLabel(
            self.details_container, 
            text="", 
            font=("Arial", 72)
        )
        self.recipe_icon_label.pack(pady=10)

        self.recipe_desc_label = ctk.CTkLabel(
            self.details_container, 
            text="", 
            font=("Arial", 16),
            wraplength=500
        )
        self.recipe_desc_label.pack(pady=5)

        # Steps Frame
        self.steps_frame = ctk.CTkScrollableFrame(
            main_frame, 
            height=150, 
            width=500,
            fg_color="#2C2C2C"
        )
        self.steps_frame.pack(pady=10)

        # Cooking Controls
        control_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        control_frame.pack(fill="x", pady=10)

        self.start_button = ctk.CTkButton(
            control_frame, 
            text="Start Cooking", 
            command=self.start_cooking,
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=("Arial", 16)
        )
        self.start_button.pack(side="left", expand=True, padx=5)

        self.stop_button = ctk.CTkButton(
            control_frame, 
            text="Stop", 
            command=self.stop_cooking,
            fg_color="#F44336",
            hover_color="#D32F2F",
            state="disabled",
            font=("Arial", 16)
        )
        self.stop_button.pack(side="right", expand=True, padx=5)

        # Progress
        self.progress = ctk.CTkProgressBar(
            main_frame, 
            width=500, 
            height=20,
            fg_color="#333333",
            progress_color="#4CAF50"
        )
        self.progress.pack(pady=10)
        self.progress.set(0)

        # Status Label
        self.status_label = ctk.CTkLabel(
            main_frame, 
            text="Ready to Cook", 
            font=("Arial", 16, "italic")
        )
        self.status_label.pack(pady=10)

    def update_recipe_details(self, recipe_name):
        # Clear previous steps
        for widget in self.steps_frame.winfo_children():
            widget.destroy()

        recipe = RecipeManager.RECIPES.get(recipe_name, {})
        
        # Update icon
        self.recipe_icon_label.configure(text=recipe.get('icon', ''))
        
        # Update description
        self.recipe_desc_label.configure(text=recipe.get('description', ''))
        
        # Add cooking steps
        for i, step in enumerate(recipe.get('steps', []), 1):
            step_label = ctk.CTkLabel(
                self.steps_frame, 
                text=f"{i}. {step}", 
                font=("Arial", 14),
                anchor="w",
                wraplength=480
            )
            step_label.pack(pady=5, fill="x")

    def start_cooking(self):
        if self.current_recipe.get() == "Select Recipe":
            return

        recipe = RecipeManager.RECIPES[self.current_recipe.get()]
        cooking_time = recipe['time'] * 60  # Convert to seconds

        self.is_cooking = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(text=f"Cooking {self.current_recipe.get()}...")

        # Reset progress
        self.progress.set(0)

        # Start cooking thread
        self.cooking_thread = threading.Thread(
            target=self.cook_process, 
            args=(cooking_time,), 
            daemon=True
        )
        self.cooking_thread.start()

    def cook_process(self, total_time):
        start_time = time.time()
        while self.is_cooking and time.time() - start_time < total_time:
            elapsed = time.time() - start_time
            progress = elapsed / total_time
            remaining = int(total_time - elapsed)

            # Update UI in main thread
            self.root.after(0, self.update_cooking_ui, progress, remaining)
            time.sleep(0.1)

        # Cooking complete
        if self.is_cooking:
            self.root.after(0, self.finish_cooking)

    def update_cooking_ui(self, progress, remaining):
        self.progress.set(progress)
        self.status_label.configure(text=f"Cooking... {remaining} seconds left")

    def finish_cooking(self):
        self.is_cooking = False
        self.progress.set(1)
        self.status_label.configure(text="Cooking Complete!")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

    def stop_cooking(self):
        self.is_cooking = False
        self.progress.set(0)
        self.status_label.configure(text="Cooking Stopped")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

    def run(self):
        self.root.mainloop()

def main():
    app = CookingApp()
    app.run()

if __name__ == "__main__":
    main()
