import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import pygame
from sos_game_utils import update_scoreboard, increment_score, update_button_image, check_sos, check_winner, check_game_end, handle_click_ai, bind_tooltip, player_turn

pygame.mixer.init()

# Initialize global variables
board_window = None
buttons = []
board = []
fire_frames = []
water_frames = []
forest_frames = []
tiger_frames = []
lion_frames = []
player1 = "Player 1"
player2 = "Player 2"
player1_score = 0
player2_score = 0

import random

def evaluate_board(board):
    # This is a simple heuristic that could be improved
    return player2_score - player1_score

def get_possible_moves(board):
    return [(i, j) for i in range(board_size) for j in range(board_size) if board[i][j] == '']

def minimax(board, depth, alpha, beta, is_maximizing, player1_score, player2_score, board_window, root, player1, player2):
    if depth == 0 or check_game_end(board, player1_score, player2_score, board_window, root, player1, player2):
        return evaluate_board(board)

    possible_moves = get_possible_moves(board)

    if is_maximizing:
        max_eval = float('-inf')
        for move in possible_moves:
            board_copy = [row.copy() for row in board]
            board_copy[move[0]][move[1]] = 'O'  # AI always plays 'O'
            if check_sos(board_copy, move[0], move[1], 'O')[0]:
                player2_score += 1
            eval = minimax(board_copy, depth - 1, alpha, beta, False, player1_score, player2_score, board_window, root, player1, player2)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in possible_moves:
            board_copy = [row.copy() for row in board]
            board_copy[move[0]][move[1]] = 'S'  # Human always plays 'S'
            if check_sos(board_copy, move[0], move[1], 'S')[0]:
                player1_score += 1
            eval = minimax(board_copy, depth - 1, alpha, beta, True, player1_score, player2_score, board_window, root, player1, player2)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def ai_make_move(board, buttons, fire_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2):
    global player1_score, player2_score
    if player_turn[0] == 2:  # AI's turn (player 2)
        possible_moves = get_possible_moves(board)
        best_score = float('-inf')
        best_move = None
        for move in possible_moves:
            board_copy = [row.copy() for row in board]
            board_copy[move[0]][move[1]] = 'O'  # AI always plays 'O'
            if check_sos(board_copy, move[0], move[1], 'O')[0]:
                player2_score += 1
            score = minimax(board_copy, 3, float('-inf'), float('inf'), False, player1_score, player2_score, board_window, root, player1, player2)  # Adjust depth as needed
            if score > best_score:
                best_score = score
                best_move = move
        handle_click_ai(None, best_move[0], best_move[1], board, buttons, fire_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2)
        if check_sos(board, best_move[0], best_move[1], 'O')[0]:  # Check if AI made 'SOS'
            ai_make_move(board, buttons, fire_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2)

def open_multiplayer_board(root_window, p1, p2):
    global board_window, player1, player2, board_size, board, buttons, scoreboard_frame
    global fire_frames, water_frames, forest_frames, tiger_frames, lion_frames

    player1 = p1
    player2 = p2

    pygame.mixer.music.pause()

    board_window = tk.Toplevel(root_window)
    board_window.title("SOS Multiplayer Board")

    window_width = 580
    window_height = 380

    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    board_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    board_window.resizable(False, False)

    pygame.mixer.music.load("resources/music/forest.mp3")
    pygame.mixer.music.play(-1)

    main_frame = ttk.Frame(board_window, style="Custom.TFrame")
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    background_image = Image.open("resources/images/forest.jpg")
    frame_background_photo = ImageTk.PhotoImage(background_image.resize((window_width, window_height), Image.ANTIALIAS))
    frame_background_label = tk.Label(main_frame, image=frame_background_photo)
    frame_background_label.image = frame_background_photo
    frame_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    board_frame = ttk.Frame(main_frame, style="Custom.TFrame")
    board_frame.grid(row=0, column=0, padx=(20, 10), pady=20)

    scoreboard_frame = tk.Canvas(main_frame, width=180, height=80)
    scoreboard_frame.grid(row=0, column=1, padx=(10, 20), pady=0)

    scoreboard_image = Image.open("resources/images/score_board.png")
    scoreboard_photo = ImageTk.PhotoImage(scoreboard_image.resize((200, 100), Image.ANTIALIAS))
    scoreboard_frame.create_image(0, 0, image=scoreboard_photo, anchor="nw")
    scoreboard_frame.image = scoreboard_photo

    update_scoreboard(scoreboard_frame, player1, player2)

    board_size = 6
    board = [['' for _ in range(board_size)] for _ in range(board_size)]

    fire_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/fire.gif"))]
    water_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/water.gif"))]
    forest_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/forest.gif"))]
    tiger_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/tiger.gif"))]
    lion_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/lion.gif"))]

    buttons = [[None for _ in range(board_size)] for _ in range(board_size)]
    for row in range(board_size):
        for col in range(board_size):
            button = ttk.Button(board_frame, text='', width=5, command=lambda r=row, c=col: handle_click_ai(None, r, c, board, buttons, fire_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root_window, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2, ai_make_move))
            
            button.grid(row=row, column=col, padx=5, pady=5)
            button.config(image=forest_frames[0])
            button.animation_id = None
            update_button_image(button, forest_frames, board_window)
            button.bind('<Button-1>', lambda event, r=row, c=col: handle_click_ai(event, r, c, board, buttons, fire_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root_window, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2, ai_make_move))

            button.bind('<Button-3>', lambda event, r=row, c=col: handle_click_ai(event, r, c, board, buttons, fire_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root_window, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2, ai_make_move))
            buttons[row][col] = button

            bind_tooltip(button, "")

    board_window.protocol("WM_DELETE_WINDOW", root_window.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    root.option_add("*Font", "Digital-7 12")
    open_multiplayer_board(root, "Player 1", "Player 2")
    root.mainloop()
