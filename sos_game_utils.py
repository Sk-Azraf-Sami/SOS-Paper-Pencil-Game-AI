import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def initialize_window(root, title):
    board_window = tk.Toplevel(root)
    board_window.title(title)

    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    board_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    board_window.resizable(False, False)

    return board_window

def create_labels(frame, player1, player2):
    player1_score = tk.IntVar()
    player2_score = tk.IntVar()

    player1_label = tk.StringVar()
    player2_label = tk.StringVar()
    player1_label.set(f"Player 1: {player1} (S)")
    player2_label.set(f"Player 2: {player2} (O)")

    player1_name_label = tk.Label(frame, textvariable=player1_label, fg="red")
    player1_name_label.grid(row=0, column=0, columnspan=3)
    player2_name_label = tk.Label(frame, textvariable=player2_label, fg="black")
    player2_name_label.grid(row=1, column=0, columnspan=3)

    tk.Label(frame, textvariable=player1_score).grid(row=0, column=3)
    tk.Label(frame, textvariable=player2_score).grid(row=1, column=3)

    return player1_score, player2_score, player1_name_label, player2_name_label

def create_board(frame, board_size, handle_click):
    buttons = [[None for _ in range(board_size)] for _ in range(board_size)]
    for row in range(board_size):
        for col in range(board_size):
            button = ttk.Button(frame, text='', width=5, command=lambda r=row, c=col: handle_click(None, r, c))
            button.grid(row=row+2, column=col, padx=5, pady=5)  # Adjust row index to leave space for labels
            button.bind('<Button-1>', lambda event, r=row, c=col: handle_click(event, r, c))
            button.bind('<Button-3>', lambda event, r=row, c=col: handle_click(event, r, c))
            buttons[row][col] = button
    return buttons

def check_sos(board, row, col, char, board_size):
    found_sos = False
    for i in range(-2, 1):
        if (0 <= row + i < board_size - 2 and
            board[row + i][col] == 'S' and
            board[row + i + 1][col] == 'O' and
            board[row + i + 2][col] == 'S'):
            found_sos = True
        if (0 <= col + i < board_size - 2 and
            board[row][col + i] == 'S' and
            board[row][col + i + 1] == 'O' and
            board[row][col + i + 2] == 'S'):
            found_sos = True

    for i in range(-2, 1):
        if (0 <= row + i < board_size - 2 and 0 <= col + i < board_size - 2 and
            board[row + i][col + i] == 'S' and
            board[row + i + 1][col + i + 1] == 'O' and
            board[row + i + 2][col + i + 2] == 'S'):
            found_sos = True
        if (0 <= row - i < board_size - 2 and 0 <= col + i < board_size - 2 and
            board[row - i][col + i] == 'S' and
            board[row - i - 1][col + i + 1] == 'O' and
            board[row - i - 2][col + i + 2] == 'S'):
            found_sos = True

    return found_sos

def check_winner(board, row, col, char, player_turn, player1_score, player2_score, player1_name_label, player2_name_label):
    if check_sos(board, row, col, char, len(board)):
        current_player = player_turn[0]
        if current_player == 1:
            player1_score.set(player1_score.get() + 1)
            print(f"Player 1 scores a point! ({row}, {col}) is part of an SOS sequence. Current Score: {player1_score.get()}")
        else:
            player2_score.set(player2_score.get() + 1)
            print(f"Player 2 scores a point! ({row}, {col}) is part of an SOS sequence. Current Score: {player2_score.get()}")
        return True
    return False

def check_game_end(board, player1_score, player2_score, player1, player2, board_window, root):
    if all(cell != '' for row in board for cell in row):
        if player1_score.get() > player2_score.get():
            winner = player1
        elif player2_score.get() > player1_score.get():
            winner = player2
        else:
            winner = "No one, it's a tie!"
        messagebox.showinfo("Game Over", f"Game Over! The winner is: {winner}")
        board_window.destroy()
        root.destroy()
