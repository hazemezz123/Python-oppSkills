# Superhero Battle Simulator

A graphical user interface (GUI) application for simulating battles between superheroes and villains.

## Features

- Create custom heroes and villains with different power levels
- View details of all created characters
- Simulate battles between heroes and villains with real-time updates
- Health bar visualization during battles
- Battle log to track the progress of fights
- Battle history tracking and review of past battles
- Persistent storage - all characters and battle history are saved automatically

## Requirements

- Python 3.x
- Tkinter (usually comes with Python installation)
- Pillow (PIL) for image handling
- ttkthemes for improved visual appearance

## Installation

```
pip install -r requirements.txt
```

## How to Run

1. Ensure you have Python installed on your system
2. Install dependencies using the command above
3. Run the application:

```
python superhero_battle_gui.py
```

## Using the Application

### 1. Create Character Tab

- Enter a name for your character
- Select whether it's a hero or villain
- Set the power level (1-30)
- Click "Create Character" to add it to your collection
- All created characters are automatically saved

### 2. Battle Arena Tab

- Select a hero and villain from the dropdown menus
- Click "Start Battle" to begin the simulation
- Watch the health bars update in real-time
- Read the battle log to follow the action
- The battle ends when one character's health reaches zero

### 3. Character List Tab

- View all created heroes and villains
- Click on a character to see its details

### 4. Battle History Tab

- View a record of all battles that have been fought
- See date, participants, winner, and number of rounds for each battle
- Click on any battle to view the detailed battle log
- Revisit exciting moments from past battles
- All battle history is automatically saved

## Data Storage

The application automatically saves all your created characters and battle history to the following files:

- `data/heroes.pickle`: Contains all created heroes
- `data/villains.pickle`: Contains all created villains
- `data/battle_history.json`: Contains the complete battle history

These files are created automatically in a `data` directory when you close the application or when you create characters or complete battles.

## Code Enhancements

- Added health attribute to characters for more realistic battles
- Improved battle mechanics with attack and defense calculations
- Added threading to keep UI responsive during battles
- Special abilities for heroes and evil plans for villains
- Interactive health bars to visualize damage during fights
- Battle history tracking and management
- Improved text padding and visual styling
- Data persistence for characters and battle history
