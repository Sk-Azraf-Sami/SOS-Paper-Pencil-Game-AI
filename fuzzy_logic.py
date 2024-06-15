import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

def open_fuzzy_logic_gui(root, player1, player2="AI"):
    # Create a new top-level window
    board_window = tk.Toplevel(root)
    board_window.title("SOS Multiplayer Board")

    # Set window size and position to match the main menu window
    window_width = 400
    window_height = 300

    # Get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Set the position of the window to the center of the screen
    board_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    board_window.resizable(False, False)

    # Create a frame for the labels and the board
    frame = ttk.Frame(board_window)
    frame.grid(row=0, column=0, padx=10, pady=10)

    # Score labels
    player1_score = tk.IntVar()
    player2_score = tk.IntVar()

    # Create label variables for player names
    player1_label = tk.StringVar()
    player2_label = tk.StringVar()

    # Update the labels with player names and colors
    player1_label.set(f"Player 1: {player1} (S)")
    player2_label.set(f"Player 2: {player2} (O)")

    # Create labels with label variables and initial color
    player1_name_label = tk.Label(frame, textvariable=player1_label, fg="red")
    player1_name_label.grid(row=0, column=0, columnspan=3)
    player2_name_label = tk.Label(frame, textvariable=player2_label, fg="black")
    player2_name_label.grid(row=1, column=0, columnspan=3)

    tk.Label(frame, textvariable=player1_score).grid(row=0, column=3)
    tk.Label(frame, textvariable=player2_score).grid(row=1, column=3)

    board_size = 6
    board = [['' for _ in range(board_size)] for _ in range(board_size)]
    player_turn = [1]  # Use list to make it mutable in nested function

    def check_sos(row, col, char):
        found_sos = False
        # Check for vertical and horizontal SOS sequence
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

        # Check for diagonal SOS sequence
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

    def check_winner(row, col, char):
        if check_sos(row, col, char):
            current_player = player_turn[0]
            if current_player == 1:
                player1_score.set(player1_score.get() + 1)
                print(f"Player 1 scores a point! ({row}, {col}) is part of an SOS sequence. Current Score: {player1_score.get()}")
            else:
                player2_score.set(player2_score.get() + 1)
                print(f"Player 2 scores a point! ({row}, {col}) is part of an SOS sequence. Current Score: {player2_score.get()}")
            return True
        return False

    def handle_click(event, row, col):
        current_player = player_turn[0]
        char = 'S' if event.num == 1 else 'O'
        if board[row][col] == '':
            board[row][col] = char
            buttons[row][col].config(text=char, state='disabled')
            print(f"Cell clicked: ({row}, {col}), contains: '{char}'")  # Print cell location and content
            if not check_winner(row, col, char):
                player_turn[0] = 2 if current_player == 1 else 1
                # Update label colors
                if player_turn[0] == 1:
                    player1_name_label.config(fg="red")
                    player2_name_label.config(fg="black")
                else:
                    player1_name_label.config(fg="black")
                    player2_name_label.config(fg="red")
            check_game_end()
            if player_turn[0] == 2:
                ai_move()

    def ai_move():
        best_move = None
        best_score = float('-inf')

        # AI makes decisions based on a simple heuristic
        for row in range(board_size):
            for col in range(board_size):
                if board[row][col] == '':
                    for char in ['S', 'O']:
                        board[row][col] = char
                        score = evaluate_board()
                        board[row][col] = ''
                        if score > best_score:
                            best_score = score
                            best_move = (row, col, char)

        if best_move:
            row, col, char = best_move
            board[row][col] = char
            buttons[row][col].config(text=char, state='disabled')
            if not check_winner(row, col, char):
                player_turn[0] = 1
                player1_name_label.config(fg="red")
                player2_name_label.config(fg="black")
            check_game_end()

    def evaluate_board():
        score = 0
        for row in range(board_size):
            for col in range(board_size):
                if board[row][col] != '':
                    if check_sos(row, col, board[row][col]):
                        score += 1
        return score

    def check_game_end():
        if all(cell != '' for row in board for cell in row):
            if player1_score.get() > player2_score.get():
                winner = player1
            elif player2_score.get() > player1_score.get():
                winner = player2
            else:
                winner = "No one, it's a tie!"
            # Show the game over message before destroying the root
            messagebox.showinfo("Game Over", f"Game Over! The winner is: {winner}")
            board_window.destroy()
            root.destroy()

    buttons = [[None for _ in range(board_size)] for _ in range(board_size)]
    for row in range(board_size):
        for col in range(board_size):
            button = ttk.Button(frame, text='', width=5, command=lambda r=row, c=col: handle_click(None, r, c))
            button.grid(row=row+2, column=col, padx=5, pady=5)  # Adjust row index to leave space for labels
            button.bind('<Button-1>', lambda event, r=row, c=col: handle_click(event, r, c))
            button.bind('<Button-3>', lambda event, r=row, c=col: handle_click(event, r, c))
            buttons[row][col] = button

    # Ensure the root window is destroyed when the board window is closed
    board_window.protocol("WM_DELETE_WINDOW", root.destroy)

if __name__ == "__main__":
    # This part is optional and can be used to test the board independently
    root = tk.Tk()
    open_fuzzy_logic_gui(root, "Player 1", "Player 2")
    root.mainloop()
