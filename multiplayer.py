import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageSequence
import pygame
from sos_game_utils import bind_tooltip

pygame.mixer.init()

# Initialize global variables
tooltip_window = None
board_window = None
buttons = []
player1_score = 0
player2_score = 0
player_turn = [1]
board = []
fire_frames = []
water_frames = []
forest_frames = []
tiger_frames = []
lion_frames = []
player1 = "Player 1"
player2 = "Player 2"


def update_scoreboard():
    global player1_score, player2_score, player_turn, scoreboard_frame

    scoreboard_frame.delete("all")  # Clear the canvas
    scoreboard_frame.create_image(0, 0, image=scoreboard_frame.image, anchor="nw")  # Redraw background image

    # Change player names' color based on the turn
    player1_color = "#FBF6EE" if player_turn[0] == 1 else "black"
    player2_color = "#FBF6EE" if player_turn[0] == 2 else "black"

    scoreboard_frame.create_text(100, 20, text=f"{player1}: {player1_score}", fill=player1_color, font=("PlaywriteNO", 12, "bold"))
    scoreboard_frame.create_text(100, 60, text=f"{player2}: {player2_score}", fill=player2_color, font=("PlaywriteNO", 12, "bold"))

def increment_score(player):
    global player1_score, player2_score
    if player == 1:
        player1_score += 1
    elif player == 2:
        player2_score += 1
    update_scoreboard()

def update_button_image(button, frames, index=0):
    global board_window
    button.config(image=frames[index])
    animation_id = board_window.after(100, update_button_image, button, frames, (index + 1) % len(frames))
    button.animation_id = animation_id  # Store the animation ID

def handle_click(event, row, col):
    global buttons, board, player_turn, player1_score, player2_score, fire_frames, water_frames, tiger_frames, lion_frames

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
        update_button_image(buttons[row][col], frames)

        tooltip_text = "Fire" if char == 'S' else "Water"
        bind_tooltip(buttons[row][col], tooltip_text)

        if not check_winner(row, col, char):
            player_turn[0] = 2 if player_turn[0] == 1 else 1
            update_scoreboard()
        check_game_end()

def check_sos(row, col, char):
    found_sos = False
    sos_positions = []
    board_size = 6

    for i in range(-2, 1):
        if (0 <= row + i < board_size - 2 and
            board[row + i][col] == 'S' and
            board[row + i + 1][col] == 'O' and
            board[row + i + 2][col] == 'S'):
            found_sos = True
            sos_positions.extend([(row + i, col), (row + i + 1, col), (row + i + 2, col)])
        if (0 <= col + i < board_size - 2 and
            board[row][col + i] == 'S' and
            board[row][col + i + 1] == 'O' and
            board[row][col + i + 2] == 'S'):
            found_sos = True
            sos_positions.extend([(row, col + i), (row, col + i + 1), (row, col + i + 2)])

    for i in range(-2, 1):
        if (0 <= row + i < board_size - 2 and 0 <= col + i < board_size - 2 and
            board[row + i][col + i] == 'S' and
            board[row + i + 1][col + i + 1] == 'O' and
            board[row + i + 2][col + i + 2] == 'S'):
            found_sos = True
            sos_positions.extend([(row + i, col + i), (row + i + 1, col + i + 1), (row + i + 2, col + i + 2)])
        if (0 <= row - i < board_size - 2 and 0 <= col + i < board_size - 2 and
            board[row - i][col + i] == 'S' and
            board[row - i - 1][col + i + 1] == 'O' and
            board[row - i - 2][col + i + 2] == 'S'):
            found_sos = True
            sos_positions.extend([(row - i, col + i), (row - i - 1, col + i + 1), (row - i - 2, col + i + 2)])

    return found_sos, sos_positions

def check_winner(row, col, char):
    global buttons, player_turn, player1_score, player2_score, tiger_frames, lion_frames

    found_sos, sos_positions = check_sos(row, col, char)
    if found_sos:
        current_player = player_turn[0]
        frames = tiger_frames if current_player == 1 else lion_frames
        for pos in sos_positions:
            r, c = pos
            if buttons[r][c].animation_id:
                board_window.after_cancel(buttons[r][c].animation_id)
                buttons[r][c].animation_id = None
            update_button_image(buttons[r][c], frames)

        if current_player == 1:
            player1_score += 1
        else:
            player2_score += 1
        update_scoreboard()
        return True
    return False

def check_game_end():
    global board, player1_score, player2_score, player1, player2, board_window, root

    if all(cell != '' for row in board for cell in row):
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
    try:
        messagebox.showinfo("Game Over", f"{emoji} Game Over! The winner is: {winner} {emoji}")
    except:
        pass  # Prevent crash if messagebox fails

def open_multiplayer_board(root_window, p1, p2):
    global board_window, player1, player2, board_size, board, buttons, scoreboard_frame
    global fire_frames, water_frames, forest_frames, tiger_frames, lion_frames, player_turn

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

    update_scoreboard()

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
            button = ttk.Button(board_frame, text='', width=5, command=lambda r=row, c=col: handle_click(None, r, c))
            button.grid(row=row, column=col, padx=5, pady=5)
            button.config(image=forest_frames[0])
            button.animation_id = None
            update_button_image(button, forest_frames)
            button.bind('<Button-1>', lambda event, r=row, c=col: handle_click(event, r, c))
            button.bind('<Button-3>', lambda event, r=row, c=col: handle_click(event, r, c))
            buttons[row][col] = button

            bind_tooltip(button, "")

    board_window.protocol("WM_DELETE_WINDOW", root_window.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    root.option_add("*Font", "Digital-7 12")
    open_multiplayer_board(root, "Player 1", "Player 2")
    root.mainloop()
