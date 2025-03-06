import tkinter as tk
import customtkinter as ctk
import threading
import time
import random

class RecipeManager:
    RECIPES = {
        "Tomato Soup": {
            "icon": "🍅",
            "color": "#FF6B6B",
            "time": 0.5,
            "description": "Tangy Tomato Soup with Herbs",
            "modules": [
                {"name": "Hopper", "action": "Dispensing tomatoes", "emoji": "🍅"},
                {"name": "Spice", "action": "Adding basil and pepper", "emoji": "🌿"},
                {"name": "Water", "action": "Adding 500ml water", "emoji": "💧"},
                {"name": "Cooktop", "action": "Heating to 90°C", "emoji": "🔥"},
                {"name": "Motor", "action": "Stirring at medium speed", "emoji": "🔄"}
            ]
        },
        "Spinach Soup": {
            "icon": "🥬",
            "color": "#45B7D1",
            "time": 0.5,
            "description": "Healthy spinach Soup",
            "modules": [
                {"name": "Hopper", "action": "Dispensing spinach leaves", "emoji": "🥬"},
                {"name": "Spice", "action": "Adding garlic and salt", "emoji": "🧄"},
                {"name": "Water", "action": "Adding 400ml water", "emoji": "💧"},
                {"name": "Oil", "action": "Adding 15ml olive oil", "emoji": "🫒"},
                {"name": "Cooktop", "action": "Heating to 85°C", "emoji": "🔥"},
                {"name": "Motor", "action": "Blending at high speed", "emoji": "🌪️"}
            ]
        },
        "Tur Dal": {
            "icon": "🍲",
            "color": "#D35400",
            "time": 0.5,
            "description": "Spicy Lentil Soup",
            "modules": [
                {"name": "Hopper", "action": "Dispensing tur dal", "emoji": "🌱"},
                {"name": "Spice", "action": "Adding turmeric and cumin", "emoji": "🌶️"},
                {"name": "Water", "action": "Adding 600ml water", "emoji": "💧"},
                {"name": "Oil", "action": "Adding 20ml ghee", "emoji": "🧈"},
                {"name": "Cooktop", "action": "Heating to 95°C", "emoji": "🔥"},
                {"name": "Motor", "action": "Stirring at low speed", "emoji": "🔄"}
            ]
        }
    }

class SmartCookingApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.geometry("600x800")
        self.root.title("Smart Cooking System")
        self.root.resizable(False, False)

        self.current_recipe = tk.StringVar(value="Select Recipe")
        self.cooking_thread = None
        self.is_cooking = False
        self.module_status = {}

        self.create_ui()

    def create_ui(self):
        main_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="transparent")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        header = ctk.CTkLabel(
            main_frame, 
            text="🍲 Food Items 🍲", 
            font=("Arial Rounded", 24, "bold")
        )
        header.pack(pady=(0, 20))

        recipe_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        recipe_frame.pack(fill="x", pady=10)

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

        self.details_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.details_container.pack(fill="x", pady=10)

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

        self.module_frame = ctk.CTkFrame(
            main_frame, 
            fg_color="#2C2C2C",
            corner_radius=8
        )
        self.module_frame.pack(fill="x", pady=10)

        self.module_title_label = ctk.CTkLabel(
            self.module_frame,
            text="📡 ESP32 Module Status",
            font=("Arial", 14, "bold")
        )
        self.module_title_label.pack(pady=(10, 5))

        # Module Status Display
        self.module_status_frame = ctk.CTkFrame(
            self.module_frame,
            fg_color="transparent"
        )
        self.module_status_frame.pack(pady=(0, 10), padx=10, fill="x")

        # Cooking Controls
        control_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        control_frame.pack(fill="x", pady=10)

        self.start_button = ctk.CTkButton(
            control_frame, 
            text="▶️ Start", 
            command=self.start_cooking,
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=("Arial", 16)
        )
        self.start_button.pack(side="left", expand=True, padx=5)

        self.stop_button = ctk.CTkButton(
            control_frame, 
            text="⏹️ Stop", 
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
            text="⏱️ Ready to Cook", 
            font=("Arial", 16, "italic")
        )
        self.status_label.pack(pady=10)

        # Network Status
        self.network_status = ctk.CTkLabel(
            main_frame,
            text="🟢 All ESP32 modules connected",
            font=("Arial", 12),
            text_color="#4CAF50"
        )
        self.network_status.pack(pady=5)

    def create_module_indicators(self):
        """Create status indicators for each ESP32 module"""

        for widget in self.module_status_frame.winfo_children():
            widget.destroy()
        
        recipe_name = self.current_recipe.get()
        if recipe_name == "Select Recipe":
            return
            
        recipe = RecipeManager.RECIPES[recipe_name]
        self.module_status = {}
        
        for i, module in enumerate(recipe["modules"]):
            module_name = module["name"]
            module_emoji = module.get("emoji", "📱")
            
            module_frame = ctk.CTkFrame(
                self.module_status_frame,
                fg_color="transparent" 
            )
            module_frame.pack(fill="x", pady=2)
            
            module_label = ctk.CTkLabel(
                module_frame,
                text=f"{module_emoji} {module_name}:",
                font=("Arial", 12),
                width=120,
                anchor="w"
            )
            module_label.pack(side="left")
            
            status_label = ctk.CTkLabel(
                module_frame,
                text="Standby",
                font=("Arial", 12),
                text_color="#888888"
            )
            status_label.pack(side="left", padx=10)
            
            self.module_status[module_name] = {
                "label": status_label,
                "emoji": module_emoji
            }

    def update_recipe_details(self, recipe_name):
        recipe = RecipeManager.RECIPES.get(recipe_name, {})

        self.recipe_icon_label.configure(text=recipe.get('icon', ''))
        self.recipe_desc_label.configure(text=recipe.get('description', ''))
        self.create_module_indicators()

    def start_cooking(self):
        if self.current_recipe.get() == "Select Recipe":
            return

        recipe = RecipeManager.RECIPES[self.current_recipe.get()]
        cooking_time = recipe['time'] * 60  # Convert to seconds

        self.is_cooking = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(text=f"🔄 Initializing modules...")

        self.progress.set(0)

        self.cooking_thread = threading.Thread(
            target=self.cook_process, 
            args=(cooking_time, recipe), 
            daemon=True
        )
        self.cooking_thread.start()

    def cook_process(self, total_time, recipe):
        for module in recipe["modules"]:
            time.sleep(0.5)  # Simulate network communication
            module_name = module["name"]
            
            self.root.after(0, lambda name=module_name: 
                self.module_status[name]["label"].configure(text="Initializing...", text_color="#FFA500"))
        
        modules = recipe["modules"]
        module_count = len(modules)
        start_time = time.time()
        
        while self.is_cooking and time.time() - start_time < total_time:
            elapsed = time.time() - start_time
            progress = elapsed / total_time
            remaining = int(total_time - elapsed)
            
            active_module_index = min(int(progress * module_count * 1.5), module_count - 1)
            
            self.root.after(0, self.update_cooking_ui, progress, remaining, 
                           modules, active_module_index)
            
            time.sleep(0.1)

        if self.is_cooking:
            self.root.after(0, self.finish_cooking)

    def update_cooking_ui(self, progress, remaining, modules, active_index):
        self.progress.set(progress)
        self.status_label.configure(text=f"👨‍🍳 Cooking... {remaining} seconds left")
        
        for i, module in enumerate(modules):
            module_name = module["name"]
            module_action = module["action"]
            module_emoji = module.get("emoji", "📱")
            
            if i < active_index:
                self.module_status[module_name]["label"].configure(
                    text=f"Completed ✅", 
                    text_color="#4CAF50"
                )
            elif i == active_index:
                self.module_status[module_name]["label"].configure(
                    text=f"{module_emoji} {module_action}", 
                    text_color="#FF6B6B"
                )
            else:
                self.module_status[module_name]["label"].configure(
                    text="Waiting...", 
                    text_color="#888888"
                )

    def finish_cooking(self):
        self.is_cooking = False
        self.progress.set(1)
        self.status_label.configure(text="✅ Cooking Complete! Enjoy your meal! 🍽️")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
        for module_name, status_info in self.module_status.items():
            status_info["label"].configure(text="Completed ✅", text_color="#4CAF50")

    def stop_cooking(self):
        self.is_cooking = False
        self.progress.set(0)
        self.status_label.configure(text="⚠️ Cooking Stopped - Modules Reset")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
        for module_name, status_info in self.module_status.items():
            status_info["label"].configure(text="Standby", text_color="#888888")

    def run(self):
        self.root.mainloop()

def main():
    app = SmartCookingApp()
    app.run()

if __name__ == "__main__":
    main()
