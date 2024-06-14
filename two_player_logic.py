from tkinter import ttk, messagebox
def two_player_move(board, buttons, current_player, score, update_turn_label, update_score, check_for_sos, highlight_sos):
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
        else:
            messagebox.showwarning("Invalid Move", "This spot is already taken!")
    return make_move
