import tkinter as tk
from tkinter import ttk

def create_board(master, make_move):
    style = ttk.Style()
    style.configure("TButton", font=('Arial', 20), padding=10, relief="solid", borderwidth=1)
    style.map("TButton", foreground=[('active', 'blue')], background=[('active', 'lightgray')])
    style.configure("Highlight.TButton", background="lightblue", foreground="red", relief="solid", borderwidth=2)

    buttons = [[None for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            buttons[i][j] = ttk.Button(master, text="", command=lambda i=i, j=j: make_move(i, j))
            buttons[i][j].grid(row=i+2, column=j)  # Removed padding

    return buttons

def create_labels(master, current_player, score):
    score_label = ttk.Label(master, text=score, font=('Arial', 16), background="#f0f0f0")
    score_label.grid(row=0, column=0, columnspan=5, pady=(10, 0))

    turn_label = ttk.Label(master, text=f"Current Player: {current_player}", font=('Arial', 16), background="#f0f0f0")
    turn_label.grid(row=1, column=0, columnspan=5, pady=(0, 10))

    return score_label, turn_label
