import tkinter as tk
from tkinter import ttk

def mode_selection(master, start_game):
    mode_frame = tk.Frame(master, bg="#f0f0f0")
    mode_frame.pack(pady=20)

    tk.Label(mode_frame, text="Select Mode", font=('Arial', 24, 'bold'), bg="#f0f0f0", fg="#333333").pack(pady=20)
    ttk.Button(mode_frame, text="Single Player", command=lambda: start_game("single")).pack(pady=10)
    ttk.Button(mode_frame, text="Two Players", command=lambda: start_game("two")).pack(pady=10)
