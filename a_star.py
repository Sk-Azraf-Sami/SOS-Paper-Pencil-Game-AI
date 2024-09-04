import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import pygame
from sos_game_utils import update_scoreboard, increment_score, update_button_image, check_sos, check_winner, \
    check_game_end, handle_click_ai, bind_tooltip, player_turn, player1_score, player2_score, enable_all_buttons

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

import random
import heapq


def evaluate_board(board):
    score = 0
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 'S':
                if col + 2 < len(board[0]) and board[row][col + 1] == 'O' and board[row][col + 2] == 'S':
                    score += 1
                if row + 2 < len(board) and board[row + 1][col] == 'O' and board[row + 2][col] == 'S':
                    score += 1
                if row + 2 < len(board) and col + 2 < len(board[0]) and board[row + 1][col + 1] == 'O' and \
                        board[row + 2][col + 2] == 'S':
                    score += 1
                if row + 2 < len(board) and col - 2 >= 0 and board[row + 1][col - 1] == 'O' and board[row + 2][
                    col - 2] == 'S':
                    score += 1
            elif board[row][col] == 'O':
                if col - 1 >= 0 and col + 1 < len(board[0]) and board[row][col - 1] == 'S' and board[row][
                    col + 1] == 'S':
                    score += 1
                if row - 1 >= 0 and row + 1 < len(board) and board[row - 1][col] == 'S' and board[row + 1][col] == 'S':
                    score += 1
                if row - 1 >= 0 and row + 1 < len(board) and col - 1 >= 0 and col + 1 < len(board[0]) and \
                        board[row - 1][col - 1] == 'S' and board[row + 1][col + 1] == 'S':
                    score += 1
                if row - 1 >= 0 and row + 1 < len(board) and col + 1 < len(board[0]) and col - 1 >= 0 and \
                        board[row - 1][col + 1] == 'S' and board[row + 1][col - 1] == 'S':
                    score += 1
    return score


def heuristic(board):
    return evaluate_board(board)


def get_possible_moves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '':
                moves.append((i, j))
    return moves


def a_star(board, max_depth):
    pq = []
    initial_moves = get_possible_moves(board)
    for move in initial_moves:
        i, j = move
        board[i][j] = 'S'
        score = heuristic(board)
        heapq.heappush(pq, (-score, 0, move, 'S'))
        board[i][j] = ''
        board[i][j] = 'O'
        score = heuristic(board)
        heapq.heappush(pq, (-score, 0, move, 'O'))
        board[i][j] = ''

    best_move = (-1, -1)
    best_char = 'S'
    best_score = -1000

    while pq:
        neg_score, depth, (i, j), char = heapq.heappop(pq)
        score = -neg_score
        if score > best_score:
            best_score = score
            best_move = (i, j)
            best_char = char

        if depth < max_depth:
            board[i][j] = char
            next_moves = get_possible_moves(board)
            for next_move in next_moves:
                ni, nj = next_move
                board[ni][nj] = 'S'
                next_score = heuristic(board)
                heapq.heappush(pq, (-next_score, depth + 1, next_move, 'S'))
                board[ni][nj] = ''
                board[ni][nj] = 'O'
                next_score = heuristic(board)
                heapq.heappush(pq, (-next_score, depth + 1, next_move, 'O'))
                board[ni][nj] = ''
            board[i][j] = ''

    return best_move, best_char


def ai_make_move(board, buttons, fire_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root,
                 update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2):
    if player_turn[0] == 2:  # AI's turn (player 2)
        max_depth = 3  # Set a depth limit
        best_move, best_char = a_star(board, max_depth)
        if best_move != (-1, -1):
            row, col = best_move
            handle_click_ai(None, row, col, board, buttons, fire_frames if best_char == 'S' else water_frames,
                            water_frames, tiger_frames, lion_frames, player_turn, board_window, root, update_scoreboard,
                            check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2,
                            ai_make_move, best_char)

            # Check if the AI should make another move
            while player_turn[0] == 2:  # Check if it's still AI's turn
                best_move, best_char = a_star(board, max_depth)
                if best_move != (-1, -1):
                    row, col = best_move
                    handle_click_ai(None, row, col, board, buttons, fire_frames if best_char == 'S' else water_frames,
                                    water_frames, tiger_frames, lion_frames, player_turn, board_window, root,
                                    update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame,
                                    player1, player2, ai_make_move, best_char)
                else:
                    break

    enable_all_buttons(buttons)


def apply_a_star(root_window, p1, p2):
    global board_window, player1, player2, board_size, board, buttons, scoreboard_frame
    global fire_frames, water_frames, forest_frames, tiger_frames, lion_frames

    player1 = p1
    player2 = p2

    pygame.mixer.music.pause()

    board_window = tk.Toplevel(root_window)
    board_window.title("SOS HARD MODE (A*)")

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

    background_image = Image.open("resources/images/background_medium.jpg")
    frame_background_photo = ImageTk.PhotoImage(background_image.resize((window_width, window_height), Image.LANCZOS))
    frame_background_label = tk.Label(main_frame, image=frame_background_photo)
    frame_background_label.image = frame_background_photo
    frame_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    board_frame = ttk.Frame(main_frame, style="Custom.TFrame")
    board_frame.grid(row=0, column=0, padx=(20, 10), pady=20)

    scoreboard_frame = tk.Canvas(main_frame, width=180, height=80)
    scoreboard_frame.grid(row=0, column=1, padx=(10, 20), pady=0)

    scoreboard_image = Image.open("resources/images/score_board.png")
    scoreboard_photo = ImageTk.PhotoImage(scoreboard_image.resize((200, 100), Image.LANCZOS))
    scoreboard_frame.create_image(0, 0, image=scoreboard_photo, anchor="nw")
    scoreboard_frame.image = scoreboard_photo

    update_scoreboard(scoreboard_frame, player1, player2)

    board_size = 6
    board = [['' for _ in range(board_size)] for _ in range(board_size)]

    fire_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.LANCZOS)) for img in
                   ImageSequence.Iterator(Image.open("resources/images/fire.gif"))]
    water_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.LANCZOS)) for img in
                    ImageSequence.Iterator(Image.open("resources/images/water.gif"))]
    forest_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.LANCZOS)) for img in
                     ImageSequence.Iterator(Image.open("resources/images/forest.gif"))]
    tiger_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.LANCZOS)) for img in
                    ImageSequence.Iterator(Image.open("resources/images/human.gif"))]
    lion_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.LANCZOS)) for img in
                   ImageSequence.Iterator(Image.open("resources/images/robot.gif"))]

    buttons = [[None for _ in range(board_size)] for _ in range(board_size)]
    for row in range(board_size):
        for col in range(board_size):
            button = ttk.Button(board_frame, text='', width=5,
                                command=lambda r=row, c=col: handle_click_ai(None, r, c, board, buttons, fire_frames,
                                                                             water_frames, tiger_frames, lion_frames,
                                                                             player_turn, board_window, root_window,
                                                                             update_scoreboard, check_winner,
                                                                             check_game_end, bind_tooltip,
                                                                             scoreboard_frame, player1, player2,
                                                                             ai_make_move))

            button.grid(row=row, column=col, padx=5, pady=5)
            button.config(image=forest_frames[0])
            button.animation_id = None
            update_button_image(button, forest_frames, board_window)
            button.bind('<Button-1>',
                        lambda event, r=row, c=col: handle_click_ai(event, r, c, board, buttons, fire_frames,
                                                                    water_frames, tiger_frames, lion_frames,
                                                                    player_turn, board_window, root_window,
                                                                    update_scoreboard, check_winner, check_game_end,
                                                                    bind_tooltip, scoreboard_frame, player1, player2,
                                                                    ai_make_move))

            button.bind('<Button-3>',
                        lambda event, r=row, c=col: handle_click_ai(event, r, c, board, buttons, fire_frames,
                                                                    water_frames, tiger_frames, lion_frames,
                                                                    player_turn, board_window, root_window,
                                                                    update_scoreboard, check_winner, check_game_end,
                                                                    bind_tooltip, scoreboard_frame, player1, player2,
                                                                    ai_make_move))
            buttons[row][col] = button

            bind_tooltip(button, "")

    board_window.protocol("WM_DELETE_WINDOW", root_window.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    root.option_add("*Font", "Digital-7 12")
    apply_a_star(root, "Player 1", "Player 2")
    root.mainloop()
