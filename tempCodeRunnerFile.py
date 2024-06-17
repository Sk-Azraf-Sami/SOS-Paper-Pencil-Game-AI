import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import pygame

pygame.mixer.init()

def open_multiplayer_board(root, player1, player2):
        # Pause any background music from root
    pygame.mixer.music.pause()

    # Create a new top-level window
    board_window = tk.Toplevel(root)
    board_window.title("SOS Multiplayer Board")

    # Set window size and position to match the main menu window
    window_width =  650# Increased width to accommodate scoreboard
    window_height = 400

    # Get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Set the position of the window to the center of the screen
    board_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    board_window.resizable(False, False)

    # Load background music
    pygame.mixer.music.load("forest.mp3")
    pygame.mixer.music.play(-1)

    # Create a frame for the game board and scoreboard
    main_frame = ttk.Frame(board_window, style="Custom.TFrame")
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Load background image for main_frame
    background_image = Image.open("forest.jpg")
    frame_background_photo = ImageTk.PhotoImage(background_image.resize((window_width, window_height), Image.ANTIALIAS))
    frame_background_label = tk.Label(main_frame, image=frame_background_photo)
    frame_background_label.image = frame_background_photo  # Store a reference to the image object
    frame_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a frame for the game board
    board_frame = ttk.Frame(main_frame, style="Custom.TFrame")
    board_frame.grid(row=0, column=0, padx=(20, 10), pady=20)

    # Create a frame for the scoreboard
    scoreboard_frame = ttk.Frame(main_frame, style="Custom.TFrame")
    scoreboard_frame.grid(row=0, column=1, padx=(10, 20), pady=20)

    # Load background image for scoreboard_frame
    scoreboard_image = Image.open("score_board.png")
    scoreboard_photo = ImageTk.PhotoImage(scoreboard_image.resize((window_width // 3, window_height), Image.ANTIALIAS))
    scoreboard_background_label = tk.Label(scoreboard_frame, image=scoreboard_photo)
    scoreboard_background_label.image = scoreboard_photo  # Store a reference to the image object
    scoreboard_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Load custom font
    digital7_font = ("Digital-7", 20)
    modern_font = ("Helvetica", 16, "bold")

    # Score labels
    player1_score = tk.IntVar()
    player2_score = tk.IntVar()

    # Create label variables for player names
    player1_label = tk.StringVar()
    player2_label = tk.StringVar()

    # Update the labels with player names and colors
    player1_label.set(f"Player 1: {player1}")
    player2_label.set(f"Player 2: {player2}")

    # Create labels with label variables and initial color
    player1_name_label = tk.Label(scoreboard_frame, textvariable=player1_label, fg="red", font=modern_font)
    player1_name_label.grid(row=0, column=0, pady=(0, 10))
    player2_name_label = tk.Label(scoreboard_frame, textvariable=player2_label, fg="black", font=modern_font)
    player2_name_label.grid(row=1, column=0, pady=(0, 10))

    # Score displays
    player1_score_label = tk.Label(scoreboard_frame, textvariable=player1_score, font=digital7_font)
    player1_score_label.grid(row=0, column=1, padx=20, pady=(0, 10))
    player2_score_label = tk.Label(scoreboard_frame, textvariable=player2_score, font=digital7_font)
    player2_score_label.grid(row=1, column=1, padx=20, pady=(0, 10))

    board_size = 6
    board = [['' for _ in range(board_size)] for _ in range(board_size)]
    player_turn = [1]  # Use list to make it mutable in nested function

    # Load GIF frames
    fire_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("fire.gif"))]
    water_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("water.gif"))]
    forest_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("forest.gif"))]
    tiger_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("tiger.gif"))]
    lion_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("lion.gif"))]
    def check_sos(row, col, char):
        found_sos = False
        sos_positions = []
        # Check for vertical and horizontal SOS sequence
        for i in range(-2, 1):
            if (0 <= row + i < board_size - 2 and
                board[row + i][col] == 'S' and
                board[row + i + 1][col] == 'O' and
                board[row + i + 2][col] == 'S'):
                found_sos = True
                sos_positions.extend([(row + i, col), (row + i + 1, col), (row + i + 2, col)])
            if (0 <= col + i < board_size - 2 and
                board[row][col + i] == 'S' and
                board[row][col + i + 1] == 'O' and
                board[row][col + i + 2] == 'S'):
                found_sos = True
                sos_positions.extend([(row, col + i), (row, col + i + 1), (row, col + i + 2)])

        # Check for diagonal SOS sequence
        for i in range(-2, 1):
            if (0 <= row + i < board_size - 2 and 0 <= col + i < board_size - 2 and
                board[row + i][col + i] == 'S' and
                board[row + i + 1][col + i + 1] == 'O' and
                board[row + i + 2][col + i + 2] == 'S'):
                found_sos = True
                sos_positions.extend([(row + i, col + i), (row + i + 1, col + i + 1), (row + i + 2, col + i + 2)])
            if (0 <= row - i < board_size - 2 and 0 <= col + i < board_size - 2 and
                board[row - i][col + i] == 'S' and
                board[row - i - 1][col + i + 1] == 'O' and
                board[row - i - 2][col + i + 2] == 'S'):
                found_sos = True
                sos_positions.extend([(row - i, col + i), (row - i - 1, col + i + 1), (row - i - 2, col + i + 2)])

        return found_sos, sos_positions

    def check_winner(row, col, char):
        found_sos, sos_positions = check_sos(row, col, char)
        if found_sos:
            current_player = player_turn[0]
            frames = tiger_frames if current_player == 1 else lion_frames
            for pos in sos_positions:
                r, c = pos
                if buttons[r][c].animation_id:
                    board_window.after_cancel(buttons[r][c].animation_id)
                    buttons[r][c].animation_id = None
                update_button_image(buttons[r][c], frames)

            if current_player == 1:
                player1_score.set(player1_score.get() + 1)
                print(f"Player 1 scores a point! ({row}, {col}) is part of an SOS sequence. Current Score: {player1_score.get()}")
            else:
                player2_score.set(player2_score.get() + 1)
                print(f"Player 2 scores a point! ({row}, {col}) is part of an SOS sequence. Current Score: {player2_score.get()}")
            return True
        return False

    def update_button_image(button, frames, index=0, animation_id=None):
        # Update the button image with the next frame
        button.config(image=frames[index])
        animation_id = board_window.after(100, update_button_image, button, frames, (index + 1) % len(frames), animation_id)
        button.animation_id = animation_id  # Store the animation ID