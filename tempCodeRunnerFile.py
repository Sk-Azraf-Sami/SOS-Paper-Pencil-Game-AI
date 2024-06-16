import tkinter as tk
from tkinter import ttk
from tkinter import font
import pygame
from PIL import Image, ImageTk, ImageSequence
from mutiplayer import open_multiplayer_board

# Initialize pygame for sound and animation
pygame.init()

# Load sound files
background_sound = pygame.mixer.Sound('background_music.mp3')
click_sound = pygame.mixer.Sound('button_click.mp3')

# Play background sound in a loop
background_sound.play(loops=-1)

# Function to play button click sound
def play_click_sound():
    click_sound.play()

# Function to select difficulty and open the corresponding GUI
def select_difficulty(difficulty):
    play_click_sound()
    print(f"Selected difficulty: {difficulty}")
    if difficulty == "Easy":
        from fuzzy_logic import open_fuzzy_logic_gui
        open_fuzzy_logic_gui(root, "Human", "AI")
    elif difficulty == "Medium":
        from genetic_algorithm import open_genetic_algorithm_gui
        open_genetic_algorithm_gui(root, "Human", "AI")
    elif difficulty == "Hard":
        from a_star import open_a_star_gui
        open_a_star_gui(root, "Human", "AI")
    elif difficulty == "Very Hard":
        from mini_max import open_mini_max
        open_mini_max(root, "Human", "AI")

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

# Create main window
root = tk.Tk()
root.title("Game Mode Selection")

window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)

# Set digital clock-like font
try:
    digital_font = font.Font(family="Digital-7", size=26, weight="bold")
except Exception as e:
    print(f"Font loading error: {e}")
    digital_font = font.Font(size=16, weight="bold")

# Create canvas for background animation
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack(fill="both", expand=True)

# Load and prepare animated GIF for background
background_gif = Image.open('background.gif')
frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(background_gif)]

# Start animation
animate_background(canvas, frames, 0)

# Add label and buttons to the canvas
label = ttk.Label(root, text="Select Game Mode", font=digital_font, background='lightblue')
label_window = canvas.create_window(window_width/2, 50, window=label)

# Configure styles for ttk widgets
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TMenubutton", font=("Helvetica", 12), padding=10)

# Create buttons for SOLO and MULTIPLAYER
button_width = 20

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

multiplayer_button = ttk.Button(root, text="MULTIPLAYER", command=start_multiplayer, width=button_width)
multiplayer_button_window = canvas.create_window(window_width/2, 180, window=multiplayer_button)

# Run the application
root.mainloop()

# Quit pygame when the tkinter window is closed
pygame.quit()
