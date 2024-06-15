import tkinter as tk
from tkinter import ttk
from board import open_multiplayer_board  # Import the function from board.py

def select_difficulty(difficulty):
    print(f"Selected difficulty: {difficulty}")
    if difficulty == "Easy":
        # Import and open the GUI from fuzzy_logic.py
        from fuzzy_logic import open_fuzzy_logic_gui
        # Now you can call the function
        open_fuzzy_logic_gui(root, "Human", "AI")
    elif difficulty == "Medium":
    #     Import and open the GUI from genetic_algorithm.py
        from genetic_algorithm import open_genetic_algorithm_gui
        open_genetic_algorithm_gui(root, "Human", "AI")
    # elif difficulty == "Hard":
    #     # Import and open the GUI from a_star.py
    #     from a_star import open_a_star_gui
    #     open_a_star_gui()
    # elif difficulty == "Very Hard":
    #     # Import and open the GUI from minimax_alpha_beta.py
    #     from minimax_alpha_beta import open_minimax_alpha_beta_gui
    #     open_minimax_alpha_beta_gui()

# Function to open the player name input window and hide the main menu
def prompt_player_names():
    player_name_window = tk.Toplevel(root)
    player_name_window.title("Enter Player Names")

    # Set window size
    window_width = 300
    window_height = 200

    # Get the screen dimension
    screen_width = player_name_window.winfo_screenwidth()
    screen_height = player_name_window.winfo_screenheight()

    # Find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Set the position of the window to the center of the screen
    player_name_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    player_name_window.resizable(False, False)

    # Create labels and entry widgets for player names
    tk.Label(player_name_window, text="Player 1 Name:").pack(pady=5)
    player1_entry = ttk.Entry(player_name_window)
    player1_entry.pack(pady=5)

    tk.Label(player_name_window, text="Player 2 Name:").pack(pady=5)
    player2_entry = ttk.Entry(player_name_window)
    player2_entry.pack(pady=5)

    def start_game():
        player1 = player1_entry.get()
        player2 = player2_entry.get()
        player_name_window.destroy()
        root.withdraw()  # Hide the main menu window
        open_multiplayer_board(root, player1, player2)  # Pass player names to the board function

    start_button = ttk.Button(player_name_window, text="Start Game", command=start_game)
    start_button.pack(pady=20)

def start_multiplayer():
    prompt_player_names()  # Open the player name input window

# Create main window
root = tk.Tk()
root.title("Game Mode Selection")

# Set window size
window_width = 400
window_height = 300

# Get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Find the center point
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

# Set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)

# Add label and buttons for the main window
label = ttk.Label(root, text="Select Game Mode", font=("Helvetica", 16))
label.pack(pady=20)

# Create a Menubutton for SOLO
solo_button = ttk.Menubutton(root, text="SOLO", direction="below")
solo_menu = tk.Menu(solo_button, tearoff=0)
solo_button['menu'] = solo_menu

# Add difficulty options to the menu
difficulties = ["Easy", "Medium", "Hard", "Very Hard"]
for difficulty in difficulties:
    solo_menu.add_command(label=difficulty, command=lambda d=difficulty: select_difficulty(d))

solo_button.pack(pady=10)

# Update the multiplayer button to call the start_multiplayer function
multiplayer_button = ttk.Button(root, text="MULTIPLAYER", command=start_multiplayer)
multiplayer_button.pack(pady=10)

# Run the application
root.mainloop()
