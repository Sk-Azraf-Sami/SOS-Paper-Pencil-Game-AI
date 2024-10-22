#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from tkinter import font
import pygame
from PIL import Image, ImageTk, ImageSequence
from multiplayer import open_multiplayer_board
import os

# Initialize pygame for sound and animation
pygame.init()

# Load sound files
background_sound = pygame.mixer.Sound('resources/music/background_music.mp3')
click_sound = pygame.mixer.Sound('resources/music/button_click.mp3')

# Play background sound in a loop
background_sound.play(loops=-1)

# Function to play button click sound
def play_click_sound():
    click_sound.play()

# Function to stop background sound
def stop_background_sound():
    background_sound.stop()

# Function to select difficulty and open the corresponding GUI
def select_difficulty(difficulty):
    play_click_sound()
    stop_background_sound()  # Stop background sound before opening the next GUI
    print(f"Selected difficulty: {difficulty}")
    if difficulty == "Easy":
        root.withdraw()
        from fuzzy_logic import apply_fuzzy_logic
        apply_fuzzy_logic(root, "HUMAN", "ROBOT")
    elif difficulty == "Medium":
        root.withdraw()
        from genetic_algorithm import apply_genetic_algorithm
        apply_genetic_algorithm(root, "HUMAN", "ROBOT")
    elif difficulty == "Hard":
        root.withdraw()
        from a_star import apply_a_star
        apply_a_star(root, "HUMAN", "ROBOT")
    elif difficulty == "Very Hard":
        root.withdraw()
        from mini_max import apply_mini_max_algorithm
        apply_mini_max_algorithm(root, "HUMAN", "ROBOT")

# Function to prompt player names for multiplayer mode
def prompt_player_names():
    play_click_sound()
    player_name_window = tk.Toplevel(root)
    player_name_window.title("Enter Player Names")

    window_width = 300
    window_height = 200
    screen_width = player_name_window.winfo_screenwidth()
    screen_height = player_name_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    player_name_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    player_name_window.resizable(False, False)

    tk.Label(player_name_window, text="Player 1 Name:").pack(pady=5)
    player1_entry = ttk.Entry(player_name_window)
    player1_entry.pack(pady=5)

    tk.Label(player_name_window, text="Player 2 Name:").pack(pady=5)

    player2_entry = ttk.Entry(player_name_window)
    player2_entry.pack(pady=5)

    def start_game():
        play_click_sound()
        player1 = player1_entry.get()
        player2 = player2_entry.get()
        player_name_window.destroy()
        # Stop background music and withdraw root window before opening multiplayer board
        stop_background_sound()
        root.withdraw()
        open_multiplayer_board(root, player1, player2)

    start_button = ttk.Button(player_name_window, text="Start Game", command=start_game)
    start_button.pack(pady=20)

def start_multiplayer():
    prompt_player_names()

# Function to animate the background
def animate_background(canvas, image_sequence, image_index):
    canvas.image = image_sequence[image_index]
    canvas.create_image(0, 0, image=canvas.image, anchor=tk.NW)
    root.after(100, animate_background, canvas, image_sequence, (image_index + 1) % len(image_sequence))

# Function to show the story of the game
def show_story():
    play_click_sound()
    story_window = tk.Toplevel(root)
    story_window.title("Game Story")

    window_width = 400
    window_height = 300
    screen_width = story_window.winfo_screenwidth()
    screen_height = story_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    story_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    story_window.resizable(False, False)

    story_text = (
        "Origin:\n"
        "The game 'SOS' was discovered and popularized in Turkey. It is a paper-and-pencil game typically "
        "played by two players. Each player takes turns writing either an 'S' or an 'O' on a grid, with the "
        "objective of forming the sequence 'SOS' either horizontally, vertically, or diagonally. The game "
        "gained popularity in Turkish schools and has been enjoyed by children and adults alike. While its "
        "exact origins are not well-documented, Turkey is widely recognized as the country where SOS became a well-known pastime."
    )

    tk.Label(story_window, text=story_text, wraplength=380).pack(pady=10)

# Function to show the game rules
def show_rules():
    play_click_sound()
    rules_window = tk.Toplevel(root)
    rules_window.title("Game Rules")

    window_width = 400
    window_height = 200
    screen_width = rules_window.winfo_screenwidth()
    screen_height = rules_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    rules_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    rules_window.resizable(False, False)

    rules_text = (
        "SOS is a two-player game.\n"
        "1. Players can place either fire or water in an empty square on their turn.\n"
        "2. To place fire, left-click the mouse.\n"
        "3. To place water, right-click the mouse.\n"
        "4. Each player takes one turn at a time.\n"
        "5. If a player forms an fire-water-fire sequence, they get another turn.\n"
        "6. The game ends when all squares are filled.\n"
        "7. The player with the most fire-water-fire sequences wins."
    )

    tk.Label(rules_window, text=rules_text, wraplength=380).pack(pady=10)

# Create main window
root = tk.Tk()
root.title("Game Mode Selection")


# Set the game icon
icon_path = os.path.abspath('resources/images/icon.ico')
if os.path.exists(icon_path):
    try:
        img = ImageTk.PhotoImage(Image.open(icon_path))
        root.tk.call('wm', 'iconphoto', root._w, img)
    except Exception as e:
        print(f"Failed to set icon: {e}")
else:
    print(f"Icon file not found at {icon_path}")

window_width = 400
window_height = 320
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)

# Set digital clock-like font
try:
    digital_font = font.Font(family="Digital-7", size=16, weight="bold")  # Smaller font size
except Exception as e:
    print(f"Font loading error: {e}")
    digital_font = font.Font(size=12, weight="bold")  # Fallback font size

# Create canvas for background animation
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack(fill="both", expand=True)

# Load and prepare animated GIF for background
background_gif = Image.open('resources/images/background.gif')
frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(background_gif)]

# Start animation
animate_background(canvas, frames, 0)

# Add label and buttons to the canvas
label = ttk.Label(root, text="SOS (Paper-Pencil Game)", font=digital_font, background='lightblue')
label_window = canvas.create_window(window_width/2, 50, window=label)

# Configure styles for ttk widgets
style = ttk.Style()
style.configure("TButton", font=digital_font, padding=1)  # Reduced padding
style.configure("TMenubutton", font=digital_font, padding=1)  # Reduced padding

# Create buttons for SOLO, MULTIPLAYER, STORY, and RULES
button_width = 10  # Reduced button width

solo_button = ttk.Button(root, text="SOLO", width=button_width)
solo_button_window = canvas.create_window(window_width/2, 120, window=solo_button)

# Create menu for SOLO button
solo_menu = tk.Menu(root, tearoff=0)
for difficulty in ["Easy", "Medium", "Hard", "Very Hard"]:
    solo_menu.add_command(label=difficulty, command=lambda d=difficulty: select_difficulty(d))

def show_solo_menu(event):
    play_click_sound()
    solo_menu.post(event.x_root, event.y_root)

solo_button.bind("<Button-1>", show_solo_menu)

# Hide menu when clicking outside
def hide_solo_menu(event):
    if not solo_menu.winfo_ismapped():
        return
    if event.widget is not solo_button:
        solo_menu.unpost()

root.bind("<Button-1>", hide_solo_menu)

multiplayer_button = ttk.Button(root, text="MULTIPLAYER", width=button_width, command=start_multiplayer)
multiplayer_button_window = canvas.create_window(window_width/2, 170, window=multiplayer_button)

story_button = ttk.Button(root, text="STORY", width=button_width, command=show_story)
story_button_window = canvas.create_window(window_width/2, 220, window=story_button)

rules_button = ttk.Button(root, text="RULES", width=button_width, command=show_rules)
rules_button_window = canvas.create_window(window_width/2, 270, window=rules_button)

# Start the Tkinter main loop
root.mainloop()
