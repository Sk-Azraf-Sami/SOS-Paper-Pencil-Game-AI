import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pygame

# Initialize global variables
tooltip_window = None
board_window = None
buttons = []
player_turn = [1]
board = []
fire_frames = []
water_frames = []
forest_frames = []
tiger_frames = []
lion_frames = []
player1 = "Player 1"
player2 = "Player 2"

global player1_score, player2_score
player1_score = 0
player2_score = 0

def show_tooltip(event, text):
    global tooltip_window
    if tooltip_window or not text:
        return

    x, y, _, _ = event.widget.bbox("insert")
    x += event.widget.winfo_rootx() + 25
    y += event.widget.winfo_rooty() + 25

    tooltip_window = tw = tk.Toplevel(event.widget)
    tw.wm_overrideredirect(True)
    tw.wm_geometry(f"+{x}+{y}")

    label = tk.Label(tw, text=text, justify='left',
                     background="#ffffe0", relief='solid', borderwidth=1,
                     font=("tahoma", "8", "normal"))
    label.pack(ipadx=1)

def hide_tooltip(event):
    global tooltip_window
    if tooltip_window:
        tooltip_window.destroy()
        tooltip_window = None

def bind_tooltip(widget, text):
    widget.bind("<Enter>", lambda event: show_tooltip(event, text))
    widget.bind("<Leave>", hide_tooltip)

def update_scoreboard(scoreboard_frame, player1, player2):
    global player1_score, player2_score, player_turn

    if isinstance(scoreboard_frame, tk.Canvas):
        scoreboard_frame.delete("all")  # Clear the canvas
        scoreboard_frame.create_image(0, 0, image=scoreboard_frame.image, anchor="nw")  # Redraw background image

        # Change player names' color based on the turn
        player1_color = "#FBF6EE" if player_turn[0] == 1 else "black"
        player2_color = "#FBF6EE" if player_turn[0] == 2 else "black"

        scoreboard_frame.create_text(100, 20, text=f"{player1}: {player1_score}", fill=player1_color, font=("PlaywriteNO", 12, "bold"))
        scoreboard_frame.create_text(100, 60, text=f"{player2}: {player2_score}", fill=player2_color, font=("PlaywriteNO", 12, "bold"))

def increment_score(player, scoreboard_frame, player1, player2):
    global player1_score, player2_score
    if player == 1:
        player1_score += 1
    elif player == 2:
        player2_score += 1
    update_scoreboard(scoreboard_frame, player1, player2)

def update_button_image(button, frames, board_window, index=0):
    if board_window.winfo_exists():  # Check if the application is still running
        if frames and button.winfo_exists():  # Ensure frames is not empty and button exists
            button.config(image=frames[index])
            animation_id = board_window.after(100, update_button_image, button, frames, board_window, (index + 1) % len(frames))
            button.animation_id = animation_id  # Store the animation ID

def check_sos(board, row, col, char):
    sos_positions = []
    board_size = 6

    for i in range(-2, 1):
        if (0 <= row + i < board_size - 2 and
            board[row + i][col] == 'S' and
            board[row + i + 1][col] == 'O' and
            board[row + i + 2][col] == 'S'):
            sos_positions.extend([(row + i, col), (row + i + 1, col), (row + i + 2, col)])
        if (0 <= col + i < board_size - 2 and
            board[row][col + i] == 'S' and
            board[row][col + i + 1] == 'O' and
            board[row][col + i + 2] == 'S'):
            sos_positions.extend([(row, col + i), (row, col + i + 1), (row, col + i + 2)])

    for i in range(-2, 1):
        if (0 <= row + i < board_size - 2 and 0 <= col + i < board_size - 2 and
            board[row + i][col + i] == 'S' and
            board[row + i + 1][col + i + 1] == 'O' and
            board[row + i + 2][col + i + 2] == 'S'):
            sos_positions.extend([(row + i, col + i), (row + i + 1, col + i + 1), (row + i + 2, col + i + 2)])
        if (0 <= row - i < board_size - 2 and 0 <= col + i < board_size - 2 and
            board[row - i][col + i] == 'S' and
            board[row - i - 1][col + i + 1] == 'O' and
            board[row - i - 2][col + i + 2] == 'S'):
            sos_positions.extend([(row - i, col + i), (row - i - 1, col + i + 1), (row - i - 2, col + i + 2)])

    return len(sos_positions) > 0, sos_positions

def handle_click(event, row, col, board, buttons, fire_frames, water_frames,tiger_frames, lion_frames, player_turn, board_window, root, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2):
    if event is None or event.num == 1:
        char = 'S'
        frames = fire_frames
    elif event.num == 3:
        char = 'O'
        frames = water_frames
    else:
        return

    if board[row][col] == '':
        if buttons[row][col].animation_id:
            board_window.after_cancel(buttons[row][col].animation_id)
            buttons[row][col].animation_id = None

        board[row][col] = char
        update_button_image(buttons[row][col], frames, board_window)

        tooltip_text = "Fire" if char == 'S' else "Water"
        bind_tooltip(buttons[row][col], tooltip_text)

        if not check_winner(row, col, char, board, buttons, player_turn, board_window, update_button_image, tiger_frames, lion_frames, update_scoreboard, root):
            player_turn[0] = 2 if player_turn[0] == 1 else 1
            update_scoreboard(scoreboard_frame, player1, player2)
        check_game_end(board, scoreboard_frame, player1_score, player2_score, board_window, root, player1, player2)

def check_winner(row, col, char, board, buttons, player_turn, board_window, update_button_image, tiger_frames, lion_frames, update_scoreboard, root):
    global player1_score, player2_score

    found_sos, sos_positions = check_sos(board, row, col, char)
    if found_sos:
        current_player = player_turn[0]
        frames = tiger_frames if current_player == 1 else lion_frames
        for pos in sos_positions:
            r, c = pos
            if buttons[r][c].animation_id:
                board_window.after_cancel(buttons[r][c].animation_id)
                buttons[r][c].animation_id = None
            update_button_image(buttons[r][c], frames, board_window)

        if current_player == 1:
            player1_score += len(sos_positions) // 3
        else:
            player2_score += len(sos_positions) // 3
        update_scoreboard(root, player1, player2)
        return True
    return False

def check_game_end(board, scoreboard_frame, player1_score, player2_score, board_window, root, player1, player2):
    update_scoreboard(scoreboard_frame, player1, player2)
    if all(cell != '' for row in board for cell in row):
        print(player1_score)
        print(player2_score)
        if player1_score > player2_score:
            winner = player1
            emoji = "🎉🎊"
        elif player2_score > player1_score:
            winner = player2
            emoji = "🏆🥳"
        else:
            winner = "No one, it's a tie!"
            emoji = "😮😅"

        pygame.mixer.music.stop()
        pygame.mixer.music.load("resources/music/winner.mp3")
        pygame.mixer.music.play()

        show_winner_message(winner, emoji)
        
        board_window.destroy()
        root.destroy()

def show_winner_message(winner, emoji):
    messagebox.showinfo("Game Over", f"{winner} wins the game! {emoji}")
    

def handle_click_ai(event, row, col, board, buttons, fire_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2, ai_make_move=None):
    if event is None or event.num == 1:
        char = 'S'
        frames = fire_frames
    elif event.num == 3:
        char = 'O'
        frames = water_frames
    else:
        return

    if board[row][col] == '':
        if buttons[row][col].animation_id:
            board_window.after_cancel(buttons[row][col].animation_id)
            buttons[row][col].animation_id = None

        board[row][col] = char
        update_button_image(buttons[row][col], frames, board_window)

        tooltip_text = "Fire" if char == 'S' else "Water"
        bind_tooltip(buttons[row][col], tooltip_text)

        # Check for "SOS" and update the score
        if not check_winner(row, col, char, board, buttons, player_turn, board_window, update_button_image, tiger_frames, lion_frames, update_scoreboard, root):
            player_turn[0] = 2 if player_turn[0] == 1 else 1
            update_scoreboard(scoreboard_frame, player1, player2)
            
            # AI move
            if ai_make_move and player_turn[0] == 2:
                board_window.after(500, lambda: ai_make_move(board, buttons, fire_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2))
        else:
            # Allow AI to make another move if it created "SOS"
            if player_turn[0] == 2 and ai_make_move:
                board_window.after(500, lambda: ai_make_move(board, buttons, fire_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2))

        check_game_end(board, scoreboard_frame, player1_score, player2_score, board_window, root, player1, player2)
