import random
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import threading
import os
from PIL import Image, ImageTk  # For working with images
import datetime  # For timestamping battle records

# The base class for our characters
class Character:
    increment = 0
    SuperPerson = []
    Villain = []
    
    def __new__(cls, name, alignment, power_level):
        if power_level > 30:
            raise ValueError("Your power is very high")
        else:
            return super().__new__(cls)
    
    def __init__(self, name, alignment, power_level):
        Character.increment += 1
        self.name = name
        self.alignment = alignment
        self.power_level = power_level
        self.health = 100  # New health attribute for more realistic battles
        
        if self.alignment == "Evilness":
            Character.Villain.append(self.name)
        else:
            Character.SuperPerson.append(self.name)
    
    # Functions to define our character's actions
    def attacking(self, attackPower):
        return f"{self.name}'s attack power is {attackPower} so I can deal a hit to my enemy."
    
    def defending(self, defensePower):
        return f"{self.name}'s defense power is {defensePower} so I can protect myself from any attacks."
    
    @staticmethod
    def show_all_hero_and_villain():
        hero_list = f"All the Villains in our story: {Character.Villain}"
        villain_list = f"All the SuperPersons in our story: {Character.SuperPerson}"
        return hero_list, villain_list
    
    @staticmethod
    def battle_simulator(hero, villain, update_callback=None):
        """Simulates a battle between a hero and villain with optional GUI updates"""
        battle_log = []
        battle_log.append(f"The Battle Starts: {hero.name} vs {villain.name}")
        
        round_number = 1
        
        # Both characters start with full health
        hero.health = 100
        villain.health = 100
        
        while hero.health > 0 and villain.health > 0:
            battle_log.append(f"\n--- Round {round_number} ---")
            battle_log.append(f"{hero.name} attacks {villain.name}!")
            
            # Calculate attack and defense values with some randomness
            hero_attack_power = random.randint(1, hero.power_level)
            villain_defense = random.randint(0, villain.power_level // 2)
            damage_to_villain = max(0, hero_attack_power - villain_defense)
            
            battle_log.append(f"{hero.name} attacks with power: {hero_attack_power}")
            battle_log.append(f"{villain.name} defends with power: {villain_defense}")
            
            # Apply damage
            villain.health -= damage_to_villain
            villain.health = max(0, villain.health)  # Health can't go below 0
            battle_log.append(f"{villain.name} takes {damage_to_villain} damage! Health: {villain.health}/100")
            
            # Break if villain is defeated
            if villain.health <= 0:
                battle_log.append(f"{villain.name} has been defeated!")
                battle_log.append(f"{hero.name} wins the battle!")
                break
                
            # Villain's turn to attack
            battle_log.append(f"{villain.name} attacks {hero.name}!")
            
            villain_attack_power = random.randint(1, villain.power_level)
            hero_defense = random.randint(0, hero.power_level // 2)
            damage_to_hero = max(0, villain_attack_power - hero_defense)
            
            battle_log.append(f"{villain.name} attacks with power: {villain_attack_power}")
            battle_log.append(f"{hero.name} defends with power: {hero_defense}")
            
            # Apply damage
            hero.health -= damage_to_hero
            hero.health = max(0, hero.health)  # Health can't go below 0
            battle_log.append(f"{hero.name} takes {damage_to_hero} damage! Health: {hero.health}/100")
            
            # Update the GUI if callback provided
            if update_callback:
                update_text = "\n".join(battle_log)
                update_callback(update_text, hero.health, villain.health)
                time.sleep(0.5)  # Slow down the battle for visual effect
            
            round_number += 1
            
            # Check if hero is defeated
            if hero.health <= 0:
                battle_log.append(f"{hero.name} has been defeated!")
                battle_log.append(f"{villain.name} wins the battle!")
                break
        
        battle_result = "\n".join(battle_log)
        return battle_result, hero.health > 0

# A class for the Heroes in our story
class SuperPerson(Character):
    def __init__(self, name, alignment, power_level):
        super().__init__(name, alignment, power_level)
        self.special_ability = random.choice(["Flight", "Super Strength", "Invisibility", "Mind Control"])

# A class for the villains in our story
class Villain(Character):
    def __init__(self, name, alignment, power_level):
        super().__init__(name, alignment, power_level)
        self.evil_plan = random.choice(["World Domination", "Revenge", "Chaos", "Power Stealing"])

# GUI Application
class SuperheroBattleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Superhero Battle Simulator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Set a theme - you can change this to any of the available themes
        style = ttk.Style()
        try:
            style.theme_use("clam")  # Use a modern looking theme
        except:
            pass  # If theme not available, use default
        
        # Configure colors for the theme
        style.configure("TButton", foreground="blue4", background="gray90", font=("Arial", 10, "bold"), padding=5)
        style.configure("TLabel", foreground="black", font=("Arial", 10), padding=2)
        style.configure("Header.TLabel", foreground="navy", font=("Arial", 16, "bold"), padding=5)
        style.configure("Result.TLabel", foreground="green4", font=("Arial", 10, "italic"), padding=3)
        style.configure("TFrame", background="#f0f0f0", padding=5)
        style.configure("TLabelframe", padding=10)
        style.configure("TLabelframe.Label", font=("Arial", 10, "bold"))
        style.configure("TNotebook", background="#f0f0f0", tabposition="n")
        style.configure("TNotebook.Tab", padding=[10, 5], font=("Arial", 9, "bold"))
        style.map("TButton", background=[("active", "lightblue")])
        
        # Create a custom style for the health bars
        style.configure("Hero.Horizontal.TProgressbar", foreground="blue", background="blue")
        style.configure("Villain.Horizontal.TProgressbar", foreground="red", background="red")
        
        self.heroes = []
        self.villains = []
        self.battle_history = []  # To store battle records
        
        # Create main notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create the tabs
        self.create_character_tab = ttk.Frame(self.notebook)
        self.battle_tab = ttk.Frame(self.notebook)
        self.character_list_tab = ttk.Frame(self.notebook)
        self.battle_history_tab = ttk.Frame(self.notebook)  # New tab for battle history
        
        self.notebook.add(self.create_character_tab, text="Create Character")
        self.notebook.add(self.battle_tab, text="Battle Arena")
        self.notebook.add(self.character_list_tab, text="Character List")
        self.notebook.add(self.battle_history_tab, text="Battle History")  # Add the new tab
        
        # Setup each tab
        self.setup_create_character_tab()
        self.setup_battle_tab()
        self.setup_character_list_tab()
        self.setup_battle_history_tab()  # Setup the new tab
        
        # Create predefined characters
        self.create_predefined_characters()
    
    def setup_create_character_tab(self):
        # Character creation form
        ttk.Label(self.create_character_tab, text="Create Your Character", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)
        
        # Main frame for the form
        form_frame = ttk.Frame(self.create_character_tab, padding=20)
        form_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=50, sticky=tk.NSEW)
        
        # Character Name
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        
        # Character Type with better looking radio buttons
        ttk.Label(form_frame, text="Type:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.character_type = tk.StringVar(value="hero")
        
        type_frame = ttk.Frame(form_frame)
        type_frame.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        
        ttk.Radiobutton(type_frame, text="Hero", variable=self.character_type, value="hero").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(type_frame, text="Villain", variable=self.character_type, value="villain").pack(side=tk.LEFT, padx=5)
        
        # Power Level with improved slider
        ttk.Label(form_frame, text="Power Level:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        
        power_frame = ttk.Frame(form_frame)
        power_frame.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        
        self.power_scale = ttk.Scale(power_frame, from_=1, to=30, orient=tk.HORIZONTAL, length=200)
        self.power_scale.set(15)  # Default value
        self.power_scale.pack(side=tk.LEFT)
        
        self.power_label = ttk.Label(power_frame, text="15")
        self.power_label.pack(side=tk.LEFT, padx=10)
        self.power_scale.configure(command=self.update_power_label)
        
        # Create Button
        create_btn = ttk.Button(form_frame, text="Create Character", command=self.create_character)
        create_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Result
        self.result_label = ttk.Label(self.create_character_tab, text="", style="Result.TLabel")
        self.result_label.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Make the tab resizable
        self.create_character_tab.columnconfigure(0, weight=1)
        self.create_character_tab.columnconfigure(1, weight=1)
        self.create_character_tab.rowconfigure(1, weight=1)
    
    def setup_battle_tab(self):
        # Battle arena setup
        ttk.Label(self.battle_tab, text="Battle Arena", style="Header.TLabel").grid(row=0, column=0, columnspan=4, pady=20)
        
        # Selection frame
        selection_frame = ttk.Frame(self.battle_tab, padding=10)
        selection_frame.grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky=tk.EW)
        
        # Hero selection
        ttk.Label(selection_frame, text="Select Hero:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.hero_var = tk.StringVar()
        self.hero_dropdown = ttk.Combobox(selection_frame, textvariable=self.hero_var, state="readonly", width=20)
        self.hero_dropdown.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Villain selection
        ttk.Label(selection_frame, text="Select Villain:").grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
        self.villain_var = tk.StringVar()
        self.villain_dropdown = ttk.Combobox(selection_frame, textvariable=self.villain_var, state="readonly", width=20)
        self.villain_dropdown.grid(row=0, column=3, sticky=tk.W, padx=10, pady=5)
        
        # Battle button
        self.battle_btn = ttk.Button(selection_frame, text="Start Battle", command=self.start_battle)
        self.battle_btn.grid(row=1, column=0, columnspan=4, pady=10)
        
        # Health bars frame
        health_frame = ttk.LabelFrame(self.battle_tab, text="Health Status", padding=15)
        health_frame.grid(row=2, column=0, columnspan=4, padx=20, pady=10, sticky=tk.NSEW)
        
        # Hero health bar
        ttk.Label(health_frame, text="Hero:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.hero_health_var = tk.IntVar(value=100)
        self.hero_health_bar = ttk.Progressbar(health_frame, orient=tk.HORIZONTAL, length=300, mode='determinate', 
                                              variable=self.hero_health_var, style="Hero.Horizontal.TProgressbar")
        self.hero_health_bar.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.hero_health_label = ttk.Label(health_frame, text="100/100")
        self.hero_health_label.grid(row=0, column=2, padx=5, pady=5)
        
        # Villain health bar
        ttk.Label(health_frame, text="Villain:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.villain_health_var = tk.IntVar(value=100)
        self.villain_health_bar = ttk.Progressbar(health_frame, orient=tk.HORIZONTAL, length=300, mode='determinate', 
                                                variable=self.villain_health_var, style="Villain.Horizontal.TProgressbar")
        self.villain_health_bar.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        self.villain_health_label = ttk.Label(health_frame, text="100/100")
        self.villain_health_label.grid(row=1, column=2, padx=5, pady=5)
        
        # Health frame column configuration
        health_frame.columnconfigure(1, weight=1)
        
        # Battle log frame
        log_frame = ttk.LabelFrame(self.battle_tab, text="Battle Log", padding=15)
        log_frame.grid(row=3, column=0, columnspan=4, padx=20, pady=10, sticky=tk.NSEW)
        
        self.battle_log = scrolledtext.ScrolledText(log_frame, width=70, height=15, font=("Courier New", 10),
                                                  padx=10, pady=10, wrap=tk.WORD)
        self.battle_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Make the battle tab resizable
        self.battle_tab.columnconfigure(0, weight=1)
        self.battle_tab.columnconfigure(1, weight=1)
        self.battle_tab.columnconfigure(2, weight=1)
        self.battle_tab.columnconfigure(3, weight=1)
        self.battle_tab.rowconfigure(3, weight=1)
    
    def setup_character_list_tab(self):
        # Main title
        ttk.Label(self.character_list_tab, text="Character List", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)
        
        # Main list frame
        list_frame = ttk.Frame(self.character_list_tab, padding=10)
        list_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky=tk.NSEW)
        
        # Hero frame
        hero_frame = ttk.LabelFrame(list_frame, text="Heroes", padding=10)
        hero_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Hero list with scrollbar
        hero_list_frame = ttk.Frame(hero_frame)
        hero_list_frame.pack(fill=tk.BOTH, expand=True)
        
        hero_scrollbar = ttk.Scrollbar(hero_list_frame)
        hero_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.heroes_list = tk.Listbox(hero_list_frame, yscrollcommand=hero_scrollbar.set, 
                                     font=("Arial", 10), bg="white", selectbackground="lightblue")
        self.heroes_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        hero_scrollbar.config(command=self.heroes_list.yview)
        
        # Villain frame
        villain_frame = ttk.LabelFrame(list_frame, text="Villains", padding=10)
        villain_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Villain list with scrollbar
        villain_list_frame = ttk.Frame(villain_frame)
        villain_list_frame.pack(fill=tk.BOTH, expand=True)
        
        villain_scrollbar = ttk.Scrollbar(villain_list_frame)
        villain_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.villains_list = tk.Listbox(villain_list_frame, yscrollcommand=villain_scrollbar.set, 
                                       font=("Arial", 10), bg="white", selectbackground="lightpink")
        self.villains_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        villain_scrollbar.config(command=self.villains_list.yview)
        
        # Character details
        details_frame = ttk.LabelFrame(self.character_list_tab, text="Character Details", padding=10)
        details_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky=tk.NSEW)
        
        self.character_details = scrolledtext.ScrolledText(details_frame, width=80, height=10, 
                                                         font=("Arial", 10), bg="white",
                                                         padx=10, pady=10, wrap=tk.WORD)
        self.character_details.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Bind selection events
        self.heroes_list.bind('<<ListboxSelect>>', self.show_hero_details)
        self.villains_list.bind('<<ListboxSelect>>', self.show_villain_details)
        
        # Make the character list tab resizable
        self.character_list_tab.columnconfigure(0, weight=1)
        self.character_list_tab.columnconfigure(1, weight=1)
        self.character_list_tab.rowconfigure(1, weight=1)
        self.character_list_tab.rowconfigure(2, weight=1)
    
    def setup_battle_history_tab(self):
        """Setup the battle history tab"""
        # Main title
        ttk.Label(self.battle_history_tab, text="Battle History", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)
        
        # Main frame for the history list
        history_frame = ttk.LabelFrame(self.battle_history_tab, text="Past Battles", padding=15)
        history_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky=tk.NSEW)
        
        # Create a treeview to show battle history
        columns = ("date", "hero", "villain", "winner", "rounds")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", selectmode="browse")
        
        # Define headings
        self.history_tree.heading("date", text="Date & Time")
        self.history_tree.heading("hero", text="Hero")
        self.history_tree.heading("villain", text="Villain")
        self.history_tree.heading("winner", text="Winner")
        self.history_tree.heading("rounds", text="Rounds")
        
        # Define columns
        self.history_tree.column("date", width=150)
        self.history_tree.column("hero", width=120)
        self.history_tree.column("villain", width=120)
        self.history_tree.column("winner", width=120)
        self.history_tree.column("rounds", width=80)
        
        # Add scrollbar
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        # Pack the tree and scrollbar
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Battle details frame
        details_frame = ttk.LabelFrame(self.battle_history_tab, text="Battle Details", padding=15)
        details_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky=tk.NSEW)
        
        self.history_details = scrolledtext.ScrolledText(details_frame, width=80, height=15, 
                                                       font=("Courier New", 10), bg="white", 
                                                       padx=10, pady=10, wrap=tk.WORD)
        self.history_details.pack(fill=tk.BOTH, expand=True)
        
        # Bind event for selected battle
        self.history_tree.bind("<<TreeviewSelect>>", self.show_battle_details)
        
        # Make the battle history tab resizable
        self.battle_history_tab.columnconfigure(0, weight=1)
        self.battle_history_tab.columnconfigure(1, weight=1)
        self.battle_history_tab.rowconfigure(1, weight=1)
        self.battle_history_tab.rowconfigure(2, weight=2)  # Give more space to the details
    
    def update_power_label(self, value):
        """Update the power level label when the scale changes"""
        self.power_label.config(text=str(int(float(value))))
    
    def update_character_lists(self):
        """Update the character lists in all relevant places"""
        # Clear and repopulate hero lists
        self.heroes_list.delete(0, tk.END)
        self.hero_dropdown['values'] = []
        hero_names = []
        
        for hero in self.heroes:
            self.heroes_list.insert(tk.END, hero.name)
            hero_names.append(hero.name)
        
        self.hero_dropdown['values'] = hero_names
        
        # Clear and repopulate villain lists
        self.villains_list.delete(0, tk.END)
        self.villain_dropdown['values'] = []
        villain_names = []
        
        for villain in self.villains:
            self.villains_list.insert(tk.END, villain.name)
            villain_names.append(villain.name)
        
        self.villain_dropdown['values'] = villain_names
    
    def create_character(self):
        """Create a new character based on form input"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a character name")
            return
        
        character_type = self.character_type.get()
        power_level = int(float(self.power_scale.get()))
        
        try:
            if character_type == "hero":
                new_character = SuperPerson(name, "Goodness", power_level)
                self.heroes.append(new_character)
                self.result_label.config(text=f"Created hero: {name} with power level {power_level}")
            else:
                new_character = Villain(name, "Evilness", power_level)
                self.villains.append(new_character)
                self.result_label.config(text=f"Created villain: {name} with power level {power_level}")
            
            # Clear form
            self.name_entry.delete(0, tk.END)
            self.power_scale.set(15)
            self.update_power_label("15")
            
            # Update lists
            self.update_character_lists()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def show_hero_details(self, event):
        """Show details for the selected hero"""
        selection = self.heroes_list.curselection()
        if selection:
            index = selection[0]
            if index < len(self.heroes):
                hero = self.heroes[index]
                details = f"Hero: {hero.name}\n"
                details += f"Alignment: {hero.alignment}\n"
                details += f"Power Level: {hero.power_level}\n"
                details += f"Special Ability: {hero.special_ability}\n"
                self.character_details.delete(1.0, tk.END)
                self.character_details.insert(tk.END, details)
    
    def show_villain_details(self, event):
        """Show details for the selected villain"""
        selection = self.villains_list.curselection()
        if selection:
            index = selection[0]
            if index < len(self.villains):
                villain = self.villains[index]
                details = f"Villain: {villain.name}\n"
                details += f"Alignment: {villain.alignment}\n"
                details += f"Power Level: {villain.power_level}\n"
                details += f"Evil Plan: {villain.evil_plan}\n"
                self.character_details.delete(1.0, tk.END)
                self.character_details.insert(tk.END, details)
    
    def show_battle_details(self, event):
        """Show details of the selected battle from history"""
        selection = self.history_tree.selection()
        if selection:
            item_id = selection[0]
            item_index = self.history_tree.index(item_id)
            if item_index < len(self.battle_history):
                battle_record = self.battle_history[item_index]
                self.history_details.delete(1.0, tk.END)
                self.history_details.insert(tk.END, battle_record["log"])
    
    def start_battle(self):
        """Start a battle between selected hero and villain"""
        hero_name = self.hero_var.get()
        villain_name = self.villain_var.get()
        
        if not hero_name or not villain_name:
            messagebox.showerror("Error", "Please select both a hero and a villain")
            return
        
        # Find the selected characters
        selected_hero = None
        selected_villain = None
        
        for hero in self.heroes:
            if hero.name == hero_name:
                selected_hero = hero
                break
        
        for villain in self.villains:
            if villain.name == villain_name:
                selected_villain = villain
                break
        
        if not selected_hero or not selected_villain:
            messagebox.showerror("Error", "Could not find selected characters")
            return
        
        # Reset health bars
        self.hero_health_var.set(100)
        self.villain_health_var.set(100)
        self.hero_health_label.config(text="100/100")
        self.villain_health_label.config(text="100/100")
        
        # Clear battle log
        self.battle_log.delete(1.0, tk.END)
        
        # Disable battle button during battle
        self.battle_btn.config(state="disabled")
        
        # Start battle in a separate thread to keep UI responsive
        battle_thread = threading.Thread(
            target=self.run_battle, 
            args=(selected_hero, selected_villain)
        )
        battle_thread.daemon = True
        battle_thread.start()
    
    def run_battle(self, hero, villain):
        """Run the battle simulation in a separate thread"""
        # Run the battle with UI updates
        battle_log, hero_won = Character.battle_simulator(hero, villain, self.update_battle_ui)
        
        # Enable battle button after battle
        self.root.after(0, lambda: self.battle_btn.config(state="normal"))
        
        # Record battle in history
        winner = hero.name if hero_won else villain.name
        
        # Count rounds from the battle log
        rounds = battle_log.count("--- Round")
        
        # Add to battle history
        battle_record = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hero": hero.name,
            "villain": villain.name,
            "winner": winner,
            "rounds": rounds,
            "log": battle_log
        }
        
        self.battle_history.append(battle_record)
        
        # Update battle history display
        self.update_battle_history()
        
        # Show final result
        self.root.after(0, lambda: messagebox.showinfo("Battle Result", f"{winner} has won the battle!"))
    
    def update_battle_history(self):
        """Update the battle history treeview with all recorded battles"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add all battles to the treeview
        for battle in self.battle_history:
            self.history_tree.insert("", tk.END, values=(
                battle["date"],
                battle["hero"],
                battle["villain"],
                battle["winner"],
                battle["rounds"]
            ))
    
    def update_battle_ui(self, battle_text, hero_health, villain_health):
        """Update the battle UI with current battle status"""
        def update():
            self.battle_log.delete(1.0, tk.END)
            self.battle_log.insert(tk.END, battle_text)
            self.battle_log.see(tk.END)
            
            # Update health bars with colors
            self.hero_health_var.set(hero_health)
            self.villain_health_var.set(villain_health)
            
            # Change color based on health
            if hero_health < 30:
                self.hero_health_label.config(foreground="red")
            elif hero_health < 70:
                self.hero_health_label.config(foreground="orange")
            else:
                self.hero_health_label.config(foreground="green")
                
            if villain_health < 30:
                self.villain_health_label.config(foreground="red")
            elif villain_health < 70:
                self.villain_health_label.config(foreground="orange")
            else:
                self.villain_health_label.config(foreground="green")
                
            self.hero_health_label.config(text=f"{hero_health}/100")
            self.villain_health_label.config(text=f"{villain_health}/100")
        
        # Schedule update on main thread
        self.root.after(0, update)
    
    def create_predefined_characters(self):
        """Create some predefined characters"""
        # Heroes
        self.heroes.append(SuperPerson("Batman", "Goodness", 20))
        self.heroes.append(SuperPerson("Superman", "Goodness", 28))
        self.heroes.append(SuperPerson("Wonder Woman", "Goodness", 25))
        self.heroes.append(SuperPerson("Spider-Man", "Goodness", 18))
        
        # Villains
        self.villains.append(Villain("Joker", "Evilness", 15))
        self.villains.append(Villain("Lex Luthor", "Evilness", 20))
        self.villains.append(Villain("The Cyborg Superman", "Evilness", 27))
        self.villains.append(Villain("Green Goblin", "Evilness", 19))
        
        # Update the lists
        self.update_character_lists()

# Main application
def main():
    root = tk.Tk()
    
    # Set icon if available
    try:
        root.iconbitmap("superhero.ico")  # You can create a simple icon file
    except:
        pass  # If no icon is available, continue without it
        
    # Apply a better looking theme if available
    try:
        from ttkthemes import ThemedTk
        root = ThemedTk(theme="arc")  # A clean, modern theme
    except:
        pass  # If ttkthemes is not installed, use the default Tk root
    
    app = SuperheroBattleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 