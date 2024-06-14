import tkinter as tk
from tkinter import ttk, messagebox
import mode_selection
import board_gui
import two_player_logic
import single_player_logic
import random

class SOSGame:
    def __init__(self, master):
        self.master = master
        self.master.title("SOS Game")
        self.master.configure(bg="#f0f0f0")
        
        self.mode = None  # Game mode: "single" or "two"
        self.current_player = ["S"]
        self.score = {"S": 0, "O": 0}
        self.board = [["" for _ in range(5)] for _ in range(5)]
        
        mode_selection.mode_selection(master, self.start_game)
        
    def start_game(self, mode):
        self.mode = mode
        for widget in self.master.winfo_children():
            widget.destroy()  # Remove all widgets before creating the game board
        self.buttons = board_gui.create_board(self.master, self.make_move)
        self.score_label, self.turn_label = board_gui.create_labels(self.master, self.current_player[0], self.get_score_text())
        
    def make_move(self, row, col):
        if self.mode == "single":
            move_function = single_player_logic.single_player_move(
                self.board, self.buttons, self.current_player, self.score,
                self.update_turn_label, self.update_score, self.check_for_sos, self.highlight_sos
            )
        else:
            move_function = two_player_logic.two_player_move(
                self.board, self.buttons, self.current_player, self.score,
                self.update_turn_label, self.update_score, self.check_for_sos, self.highlight_sos
            )
        move_function(row, col)

    def check_for_sos(self, row, col):
        sos_positions = (self.check_line(row, col, 1, 0) or  # Horizontal
                         self.check_line(row, col, 0, 1) or  # Vertical
                         self.check_line(row, col, 1, 1) or  # Diagonal down-right
                         self.check_line(row, col, 1, -1))   # Diagonal down-left
        return sos_positions

    def check_line(self, row, col, row_step, col_step):
        positions = [(row + i*row_step, col + i*col_step) for i in range(-2, 3)]
        s_positions = [(r, c) for r, c in positions if 0 <= r < 5 and 0 <= c < 5 and self.board[r][c] == "S"]
        o_position = [(r, c) for r, c in positions if 0 <= r < 5 and 0 <= c < 5 and self.board[r][c] == "O"]
        if len(s_positions) >= 2 and len(o_position) == 1:
            s_start = s_positions[0]
            o_mid = o_position[0]
            s_end = s_positions[-1]
            if abs(s_start[0] - s_end[0]) == 2 * row_step and abs(s_start[1] - s_end[1]) == 2 * col_step:
                return [s_start, o_mid, s_end]
        return []

    def highlight_sos(self, sos_positions):
        for (r, c) in sos_positions:
            self.buttons[r][c].config(style="Highlight.TButton")

    def get_score_text(self):
        return f"Score - S: {self.score['S']} | O: {self.score['O']}"
    
    def update_score(self):
        self.score_label.config(text=self.get_score_text())
        
    def update_turn_label(self):
        self.turn_label.config(text=f"Current Player: {self.current_player[0]}")

if __name__ == "__main__":
    root = tk.Tk()
    game = SOSGame(root)
    root.mainloop()
