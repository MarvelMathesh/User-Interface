import tkinter as tk
import customtkinter as ctk
import threading
import time

class RecipeManager:
    RECIPES = {
        "Tomato Soup": {
            "icon": "🍅",
            "color": "#FF6B6B",
            "time": 0.5,
            "description": "Tangy Tomato Soup with Herbs",
            "ingredients": [
                "4 large ripe tomatoes (or 2 cups canned tomatoes)",
                "1 small onion, chopped",
                "2 cloves garlic, minced",
                "1 cup vegetable or chicken broth",
                "1/2 cup water",
                "1 tbsp butter or olive oil",
                "1/2 tsp sugar (optional, to balance acidity)",
                "1/2 tsp salt (adjust to taste)",
                "1/4 tsp black pepper",
                "1/4 tsp red chili flakes (optional, for spice)",
                "1/2 cup milk or heavy cream (for a creamy version)",
                "Fresh basil leaves (for garnish)",
                "Croutons (optional)"
            ],
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
            "description": "Healthy Spinach Soup",
            "ingredients": [
                "2 bunches fresh spinach leaves, washed and chopped",
                "1 medium onion, chopped",
                "3 cloves garlic, minced",
                "2 cups vegetable broth",
                "400ml water",
                "15ml olive oil",
                "1/2 tsp salt",
                "1/4 tsp black pepper",
                "1/4 tsp nutmeg",
                "1 tbsp lemon juice",
                "1/4 cup cream (optional)"
            ],
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
            "ingredients": [
                "1 cup tur dal (split pigeon peas)",
                "1 medium onion, finely chopped",
                "1 tomato, chopped",
                "2 green chilies, slit",
                "1 tsp ginger-garlic paste",
                "1/2 tsp turmeric powder",
                "1 tsp cumin seeds",
                "1 tsp red chili powder",
                "600ml water",
                "20ml ghee",
                "Salt to taste",
                "Fresh coriander leaves for garnish"
            ],
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

class LuxuryCookingApp:
    def __init__(self):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.geometry("800x480")
        self.root.title("CHEF X")
        self.root.config(bg="#0A0A0A")
        self.root.resizable(False, False)

        self.current_recipe = tk.StringVar(value="")
        self.cooking_thread = None
        self.is_cooking = False
        self.active_module = None
        self.card_widgets = {}

        self.bg_color = "#0A0A0A"
        self.card_color = "#161616"
        self.accent_color = "#FF5500"
        self.success_color = "#00C853"
        self.danger_color = "#FF3B30"
        self.text_color = "#FFFFFF"
        self.secondary_text = "#8E8E93"
        self.gradient_top = "#151515"
        self.gradient_bottom = "#0A0A0A"
        self.card_hover = "#222222"
        self.card_border = "#2A2A2A"

        self.create_ui()

    def create_ui(self):
        self.main_container = ctk.CTkFrame(self.root, fg_color=self.bg_color, corner_radius=0)
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.content_area = ctk.CTkFrame(self.main_container, fg_color=self.bg_color, corner_radius=0)
        self.content_area.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.create_content_area()
        self.create_cooking_view()
        self.show_recipe_cards()

    def create_content_area(self):
        header = ctk.CTkFrame(self.content_area, fg_color=self.gradient_top, height=60)
        header.pack(fill="x", pady=0)
        header.pack_propagate(False)
        
        app_title = ctk.CTkLabel(
            header, 
            text="CHEF X",
            font=("SF Pro Display", 22, "bold"),
            text_color=self.text_color
        )
        app_title.pack(side="left", padx=20)
        
        status_indicator = ctk.CTkLabel(
            header,
            text="● ONLINE",
            font=("SF Pro Display", 12),
            text_color=self.success_color
        )
        status_indicator.pack(side="right", padx=20)
        
        self.recipe_container = ctk.CTkFrame(
            self.content_area,
            fg_color=self.bg_color,
            corner_radius=0
        )
        
        self.recipe_detail_view = ctk.CTkFrame(self.content_area, fg_color=self.bg_color)
        
        self.create_recipe_cards()

    def create_recipe_cards(self):
        scrollable_container = ctk.CTkScrollableFrame(
            self.recipe_container,
            fg_color=self.bg_color,
            corner_radius=0,
            scrollbar_button_color=self.accent_color,
            scrollbar_button_hover_color=self.accent_color
        )
        scrollable_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        title_label = ctk.CTkLabel(
            scrollable_container,
            text="SELECT RECIPE",
            font=("SF Pro Display", 14, "bold"),
            text_color=self.secondary_text
        )
        title_label.pack(anchor="w", padx=20, pady=(15, 10))
        
        recipe_grid = ctk.CTkFrame(scrollable_container, fg_color="transparent")
        recipe_grid.pack(fill="both", expand=True, padx=10)
        
        for i, (recipe_name, recipe_data) in enumerate(RecipeManager.RECIPES.items()):
            card = ctk.CTkFrame(
                recipe_grid,
                fg_color=self.card_color,
                corner_radius=15,
                border_width=1,
                border_color=self.card_border,
                height=180,
                width=365
            )
            
            self.card_widgets[recipe_name] = card
            
            row = i // 2
            col = i % 2
            
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            recipe_grid.grid_columnconfigure(0, weight=1)
            recipe_grid.grid_columnconfigure(1, weight=1)
            
            card.grid_propagate(False)
            
            color_indicator = ctk.CTkFrame(
                card,
                width=8,
                height=140,
                corner_radius=4,
                fg_color=recipe_data["color"]
            )
            color_indicator.place(x=15, y=20)
            
            recipe_icon = ctk.CTkLabel(
                card,
                text=recipe_data["icon"],
                font=("SF Pro", 36)
            )
            recipe_icon.place(x=35, y=20)
            
            name_label = ctk.CTkLabel(
                card,
                text=recipe_name,
                font=("SF Pro Display", 18, "bold"),
                text_color=self.text_color
            )
            name_label.place(x=100, y=20)
            
            desc_label = ctk.CTkLabel(
                card,
                text=recipe_data["description"],
                font=("SF Pro", 12),
                text_color=self.secondary_text,
                wraplength=250,
                justify="left"
            )
            desc_label.place(x=100, y=45)
            
            ingredient_count = len(recipe_data["ingredients"])
            ingredients_label = ctk.CTkLabel(
                card,
                text=f"🧪 {ingredient_count} ingredients",
                font=("SF Pro", 12),
                text_color=self.secondary_text
            )
            ingredients_label.place(x=100, y=70)
            
            time_label = ctk.CTkLabel(
                card,
                text=f"⏱️ {recipe_data['time']} min",
                font=("SF Pro", 12),
                text_color=self.secondary_text
            )
            time_label.place(x=35, y=140)
            
            view_button = ctk.CTkButton(
                card,
                text="PREPARE",
                command=lambda r=recipe_name: self.view_recipe_detail(r),
                font=("SF Pro Display", 13, "bold"),
                fg_color=self.accent_color,
                hover_color="#E64A00",
                corner_radius=20,
                width=100,
                height=30
            )
            view_button.place(x=235, y=135)

    def view_recipe_detail(self, recipe_name):
        self.current_recipe.set(recipe_name)
        recipe = RecipeManager.RECIPES[recipe_name]
        
        self.recipe_container.pack_forget()
        
        for widget in self.recipe_detail_view.winfo_children():
            widget.destroy()
            
        self.recipe_detail_view.pack(fill="both", expand=True, padx=0, pady=0)
        
        top_frame = ctk.CTkFrame(self.recipe_detail_view, fg_color=self.gradient_top, height=60)
        top_frame.pack(fill="x", pady=0)
        top_frame.pack_propagate(False)
        
        back_button = ctk.CTkButton(
            top_frame,
            text="← BACK",
            command=self.show_recipe_cards,
            fg_color="transparent",
            text_color=self.accent_color,
            hover_color="#232323",
            font=("SF Pro Display", 14, "bold"),
            width=80,
            height=30
        )
        back_button.pack(side="left", padx=20)
        
        title_label = ctk.CTkLabel(
            top_frame,
            text=recipe_name,
            font=("SF Pro Display", 18, "bold"),
            text_color=self.text_color
        )
        title_label.pack(side="left", padx=10)
        
        content_frame = ctk.CTkScrollableFrame(
            self.recipe_detail_view,
            fg_color=self.bg_color,
            corner_radius=0,
            scrollbar_button_color=self.accent_color,
            scrollbar_button_hover_color=self.accent_color
        )
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent", height=80)
        header_frame.pack(fill="x", pady=(10, 20), padx=20)
        
        color_indicator = ctk.CTkFrame(
            header_frame,
            width=10,
            height=50,
            corner_radius=5,
            fg_color=recipe["color"]
        )
        color_indicator.place(x=0, y=15)
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text=recipe["icon"],
            font=("SF Pro", 50)
        )
        icon_label.place(x=20, y=0)
        
        desc_label = ctk.CTkLabel(
            header_frame,
            text=recipe["description"],
            font=("SF Pro", 16),
            text_color=self.text_color,
            justify="left"
        )
        desc_label.place(x=100, y=10)
        
        time_label = ctk.CTkLabel(
            header_frame,
            text=f"⏱️ {recipe['time']} min",
            font=("SF Pro", 13),
            text_color=self.accent_color,
            bg_color="transparent"
        )
        time_label.place(x=100, y=35)
        
        details_grid = ctk.CTkFrame(content_frame, fg_color="transparent")
        details_grid.pack(fill="both", expand=True, padx=20, pady=10)
        
        details_grid.grid_columnconfigure(0, weight=1)
        details_grid.grid_columnconfigure(1, weight=1)
        
        ingredients_title = ctk.CTkLabel(
            details_grid,
            text="INGREDIENTS",
            font=("SF Pro Display", 14, "bold"),
            text_color=self.secondary_text
        )
        ingredients_title.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        modules_title = ctk.CTkLabel(
            details_grid,
            text="MODULES",
            font=("SF Pro Display", 14, "bold"),
            text_color=self.secondary_text
        )
        modules_title.grid(row=0, column=1, sticky="w", pady=(0, 10), padx=(20, 0))
        
        ingredients_frame = ctk.CTkFrame(
            details_grid,
            fg_color=self.card_color,
            corner_radius=15,
            border_width=1,
            border_color=self.card_border,
        )
        ingredients_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        
        for i, ingredient in enumerate(recipe["ingredients"]):
            ingredient_item = ctk.CTkLabel(
                ingredients_frame,
                text=f"• {ingredient}",
                font=("SF Pro", 13),
                text_color=self.text_color,
                justify="left",
                anchor="w"
            )
            ingredient_item.pack(anchor="w", pady=(10 if i == 0 else 5, 10 if i == len(recipe["ingredients"])-1 else 0), padx=15)
        
        modules_frame = ctk.CTkFrame(
            details_grid,
            fg_color=self.card_color,
            corner_radius=15,
            border_width=1,
            border_color=self.card_border
        )
        modules_frame.grid(row=1, column=1, sticky="nsew", pady=(0, 20), padx=(20, 0))
        
        for i, module in enumerate(recipe["modules"]):
            module_frame = ctk.CTkFrame(modules_frame, fg_color="transparent")
            module_frame.pack(fill="x", pady=(10 if i == 0 else 5, 10 if i == len(recipe["modules"])-1 else 0), padx=15)
            
            module_emoji = ctk.CTkLabel(
                module_frame,
                text=module["emoji"],
                font=("SF Pro", 16),
                width=30
            )
            module_emoji.pack(side="left")
            
            module_info = ctk.CTkFrame(module_frame, fg_color="transparent")
            module_info.pack(side="left", fill="x", expand=True)
            
            module_name = ctk.CTkLabel(
                module_info,
                text=module["name"],
                font=("SF Pro Display", 13, "bold"),
                text_color=self.text_color,
                anchor="w"
            )
            module_name.pack(anchor="w")
            
            module_action = ctk.CTkLabel(
                module_info,
                text=module["action"],
                font=("SF Pro", 12),
                text_color=self.secondary_text,
                anchor="w"
            )
            module_action.pack(anchor="w")
        
        cook_button = ctk.CTkButton(
            self.recipe_detail_view,
            text="START COOKING",
            command=self.start_cooking,
            font=("SF Pro Display", 16, "bold"),
            fg_color=self.accent_color,
            hover_color="#E64A00",
            height=50,
            corner_radius=25
        )
        cook_button.pack(pady=15, padx=20, fill="x", side="bottom")

    def create_cooking_view(self):
        self.cooking_view = ctk.CTkFrame(self.content_area, fg_color=self.bg_color)

    def show_recipe_cards(self):
        self.recipe_detail_view.pack_forget()
        self.cooking_view.pack_forget()
        
        self.recipe_container.pack(fill="both", expand=True, padx=0, pady=0)

    def start_cooking(self):
        recipe_name = self.current_recipe.get()
        recipe = RecipeManager.RECIPES[recipe_name]
        cooking_time = recipe['time'] * 60
        
        self.recipe_container.pack_forget()
        self.recipe_detail_view.pack_forget()
        
        for widget in self.cooking_view.winfo_children():
            widget.destroy()
            
        self.cooking_view.pack(fill="both", expand=True, padx=0, pady=0)
        
        top_bar = ctk.CTkFrame(self.cooking_view, fg_color=self.gradient_top, height=60)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)
        
        recipe_title = ctk.CTkLabel(
            top_bar,
            text=f"{recipe['icon']} {recipe_name}",
            font=("SF Pro Display", 18, "bold"),
            text_color=self.text_color
        )
        recipe_title.pack(side="left", padx=20)
        
        self.status_label = ctk.CTkLabel(
            top_bar,
            text="INITIALIZING...",
            font=("SF Pro Display", 14),
            text_color=self.accent_color
        )
        self.status_label.pack(side="right", padx=20)
        
        content_area = ctk.CTkFrame(self.cooking_view, fg_color="transparent")
        content_area.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.active_module_frame = ctk.CTkFrame(
            content_area,
            fg_color=self.card_color,
            corner_radius=20,
            border_width=1,
            border_color=self.card_border
        )
        self.active_module_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        progress_ring = ctk.CTkProgressBar(
            self.active_module_frame,
            mode="indeterminate",
            width=100,
            height=10,
            fg_color="#232323",
            progress_color=recipe["color"],
            corner_radius=5
        )
        progress_ring.pack(pady=(40, 0))
        progress_ring.start()
        
        self.active_module_emoji = ctk.CTkLabel(
            self.active_module_frame,
            text="🔄",
            font=("SF Pro", 100)
        )
        self.active_module_emoji.pack(pady=(10, 10))
        
        self.active_module_name = ctk.CTkLabel(
            self.active_module_frame,
            text="INITIALIZING",
            font=("SF Pro Display", 24, "bold"),
            text_color=self.text_color
        )
        self.active_module_name.pack()
        
        self.active_module_action = ctk.CTkLabel(
            self.active_module_frame,
            text="Preparing to cook...",
            font=("SF Pro", 16),
            text_color=self.secondary_text
        )
        self.active_module_action.pack(pady=5)
        
        status_frame = ctk.CTkFrame(self.active_module_frame, fg_color="transparent")
        status_frame.pack(pady=10)
        
        for i, module in enumerate(recipe["modules"]):
            status_dot = ctk.CTkButton(
                status_frame,
                text="",
                width=12,
                height=12,
                corner_radius=6,
                fg_color="#333333",
                hover_color="#333333"
            )
            status_dot.pack(side="left", padx=5)
        
        control_bar = ctk.CTkFrame(self.cooking_view, fg_color=self.gradient_top, height=90)
        control_bar.pack(fill="x", side="bottom")
        control_bar.pack_propagate(False)
        
        self.progress = ctk.CTkProgressBar(
            control_bar, 
            width=700, 
            height=8,
            fg_color="#232323",
            progress_color=recipe["color"],
            corner_radius=4
        )
        self.progress.pack(padx=20, pady=(15, 5), fill="x")
        self.progress.set(0)
        
        time_frame = ctk.CTkFrame(control_bar, fg_color="transparent")
        time_frame.pack(fill="x", padx=20)
        
        self.time_remaining = ctk.CTkLabel(
            time_frame,
            text="0:30",
            font=("SF Pro Display", 16, "bold"),
            text_color=self.text_color
        )
        self.time_remaining.pack(side="left")
        
        self.stop_button = ctk.CTkButton(
            time_frame, 
            text="STOP",
            command=self.stop_cooking,
            font=("SF Pro Display", 14, "bold"),
            fg_color=self.danger_color,
            hover_color="#D32F2F",
            corner_radius=15,
            width=80,
            height=30
        )
        self.stop_button.pack(side="right", pady=5)
        
        self.is_cooking = True
        self.cooking_thread = threading.Thread(
            target=self.cook_process, 
            args=(cooking_time, recipe), 
            daemon=True
        )
        self.cooking_thread.start()

    def cook_process(self, total_time, recipe):
        modules = recipe["modules"]
        module_count = len(modules)
        start_time = time.time()
        
        self.root.after(0, lambda: self.status_label.configure(text="CONNECTING MODULES"))
        time.sleep(1)
        
        while self.is_cooking and time.time() - start_time < total_time:
            elapsed = time.time() - start_time
            progress = elapsed / total_time
            remaining = int(total_time - elapsed)
            
            mins = remaining // 60
            secs = remaining % 60
            time_str = f"{mins}:{secs:02d}"
            
            active_module_index = min(int(progress * module_count * 1.5), module_count - 1)
            active_module = modules[active_module_index]
            
            self.root.after(0, self.update_cooking_ui, 
                          progress, 
                          time_str, 
                          active_module)
            
            time.sleep(0.1)

        if self.is_cooking:
            self.root.after(0, self.finish_cooking)

    def update_cooking_ui(self, progress, time_remaining, active_module):
        self.progress.set(progress)
        self.time_remaining.configure(text=time_remaining)
        
        self.active_module_emoji.configure(text=active_module["emoji"])
        self.active_module_name.configure(text=active_module["name"].upper())
        self.active_module_action.configure(text=active_module["action"])
        
        self.status_label.configure(text="COOKING IN PROGRESS")

    def finish_cooking(self):
        self.is_cooking = False
        self.progress.set(1)
        self.time_remaining.configure(text="0:00")
        self.status_label.configure(text="COOKING COMPLETE")
        
        self.active_module_emoji.configure(text="✅")
        self.active_module_name.configure(text="FINISHED")
        self.active_module_action.configure(text="Your meal is ready to enjoy!")
        
        self.stop_button.configure(
            text="DONE",
            fg_color=self.accent_color,
            hover_color="#E64A00",
            command=self.show_recipe_cards
        )

    def stop_cooking(self):
        self.is_cooking = False
        self.show_recipe_cards()

    def run(self):
        self.root.mainloop()

def main():
    app = LuxuryCookingApp()
    app.run()

if __name__ == "__main__":
    main()
