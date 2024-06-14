import random
from tkinter import messagebox

def single_player_move(board, buttons, current_player, score, update_turn_label, update_score, check_for_sos, highlight_sos):
    def make_move(row, col):
        if board[row][col] == "":
            board[row][col] = current_player[0]
            buttons[row][col].config(text=current_player[0])
            sos_positions = check_for_sos(row, col)
            if sos_positions:
                score[current_player[0]] += 1
                update_score()
                highlight_sos(sos_positions)
            current_player[0] = "O" if current_player[0] == "S" else "S"
            update_turn_label()
            if current_player[0] == "O":
                computer_move()
        else:
            messagebox.showwarning("Invalid Move", "This spot is already taken!")

    def computer_move():
        empty_cells = [(r, c) for r in range(5) for c in range(5) if board[r][c] == ""]
        if empty_cells:
            row, col = random.choice(empty_cells)
            board[row][col] = "O"
            buttons[row][col].config(text="O")
            sos_positions = check_for_sos(row, col)
            if sos_positions:
                score["O"] += 1
                update_score()
                highlight_sos(sos_positions)
            current_player[0] = "S"
            update_turn_label()

    return make_move
