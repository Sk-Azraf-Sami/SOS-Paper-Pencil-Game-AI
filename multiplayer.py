import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import pygame

pygame.mixer.init()

class MultiplayerBoard:
    def __init__(self, root, player1, player2):
        self.root = root
        self.player1 = player1
        self.player2 = player2

        # Pause any background music from root
        pygame.mixer.music.pause()

        # Create a new top-level window
        self.board_window = tk.Toplevel(root)
        self.board_window.title("SOS Multiplayer Board")

        # Set window size and position to match the main menu window
        window_width = 580  # Increased width to accommodate scoreboard
        window_height = 380

        # Get the screen dimension
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Set the position of the window to the center of the screen
        self.board_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.board_window.resizable(False, False)

        # Load background music
        pygame.mixer.music.load("resources/music/forest.mp3")
        pygame.mixer.music.play(-1)

        # Create a frame for the game board and scoreboard
        main_frame = ttk.Frame(self.board_window, style="Custom.TFrame")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Load background image for main_frame
        background_image = Image.open("resources/images/forest.jpg")
        frame_background_photo = ImageTk.PhotoImage(background_image.resize((window_width, window_height), Image.ANTIALIAS))
        frame_background_label = tk.Label(main_frame, image=frame_background_photo)
        frame_background_label.image = frame_background_photo  # Store a reference to the image object
        frame_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a frame for the game board
        board_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        board_frame.grid(row=0, column=0, padx=(20, 10), pady=20)

        # Create a Canvas for the scoreboard
        self.scoreboard_frame = tk.Canvas(main_frame, width=180, height=80)
        self.scoreboard_frame.grid(row=0, column=1, padx=(10, 20), pady=0)

        # Load background image for scoreboard_frame
        scoreboard_image = Image.open("resources/images/score_board.png")
        scoreboard_photo = ImageTk.PhotoImage(scoreboard_image.resize((200, 100), Image.ANTIALIAS))
        self.scoreboard_frame.create_image(0, 0, image=scoreboard_photo, anchor="nw")
        self.scoreboard_frame.image = scoreboard_photo  # Store a reference to the image object

        # Initialize scores
        self.player1_score = 0
        self.player2_score = 0

        # Display initial scoreboard
        self.update_scoreboard()

        self.board_size = 6
        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.player_turn = [1]  # Use list to make it mutable in nested function

        # Load GIF frames
        self.fire_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/fire.gif"))]
        self.water_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/water.gif"))]
        self.forest_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/forest.gif"))]
        self.tiger_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/tiger.gif"))]
        self.lion_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/lion.gif"))]

        # Create game board buttons
        self.buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        for row in range(self.board_size):
            for col in range(self.board_size):
                button = ttk.Button(board_frame, text='', width=5, command=lambda r=row, c=col: self.handle_click(None, r, c))
                button.grid(row=row, column=col, padx=5, pady=5)  # Adjust row index to leave space for labels
                button.config(image=self.forest_frames[0])  # Set the default image
                button.animation_id = None  # Add an attribute to store the animation ID
                self.update_button_image(button, self.forest_frames)  # Start the animation for forest.gif
                button.bind('<Button-1>', lambda event, r=row, c=col: self.handle_click(event, r, c))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.handle_click(event, r, c))
                self.buttons[row][col] = button

        # Ensure the root window is destroyed when the board window is closed
        self.board_window.protocol("WM_DELETE_WINDOW", root.destroy)

    def update_scoreboard(self):
        self.scoreboard_frame.delete("all")  # Clear the canvas
        self.scoreboard_frame.create_image(0, 0, image=self.scoreboard_frame.image, anchor="nw")  # Redraw background image
        self.scoreboard_frame.create_text(100, 20, text=f"{self.player1}: {self.player1_score}", fill="red", font=("PlaywriteNO", 12, "bold"))
        self.scoreboard_frame.create_text(100, 60, text=f"{self.player2}: {self.player2_score}", fill="black", font=("PlaywriteNO", 12, "bold"))

    def increment_score(self, player):
        if player == 1:
            self.player1_score += 1
        elif player == 2:
            self.player2_score += 1
        self.update_scoreboard()

    def update_button_image(self, button, frames, index=0, animation_id=None):
        # Update the button image with the next frame
        button.config(image=frames[index])
        animation_id = self.board_window.after(100, self.update_button_image, button, frames, (index + 1) % len(frames), animation_id)
        button.animation_id = animation_id  # Store the animation ID

    def handle_click(self, event, row, col):
        current_player = self.player_turn[0]
        char = 'S' if current_player == 1 else 'O'
        frames = self.fire_frames if char == 'S' else self.water_frames

        if self.board[row][col] == '':
            # Stop the forest GIF animation
            if self.buttons[row][col].animation_id:
                self.board_window.after_cancel(self.buttons[row][col].animation_id)
                self.buttons[row][col].animation_id = None

            self.board[row][col] = char
            self.update_button_image(self.buttons[row][col], frames)
            if not self.check_winner(row, col, char):
                self.player_turn[0] = 2 if current_player == 1 else 1
            self.check_game_end()

    def check_sos(self, row, col, char):
        found_sos = False
        sos_positions = []
        board_size = self.board_size
        # Check for vertical and horizontal SOS sequence
        for i in range(-2, 1):
            if (0 <= row + i < board_size - 2 and
                self.board[row + i][col] == 'S' and
                self.board[row + i + 1][col] == 'O' and
                self.board[row + i + 2][col] == 'S'):
                found_sos = True
                sos_positions.extend([(row + i, col), (row + i + 1, col), (row + i + 2, col)])
            if (0 <= col + i < board_size - 2 and
                self.board[row][col + i] == 'S' and
                self.board[row][col + i + 1] == 'O' and
                self.board[row][col + i + 2] == 'S'):
                found_sos = True
                sos_positions.extend([(row, col + i), (row, col + i + 1), (row, col + i + 2)])

        # Check for diagonal SOS sequence
        for i in range(-2, 1):
            if (0 <= row + i < board_size - 2 and 0 <= col + i < board_size - 2 and
                self.board[row + i][col + i] == 'S' and
                self.board[row + i + 1][col + i + 1] == 'O' and
                self.board[row + i + 2][col + i + 2] == 'S'):
                found_sos = True
                sos_positions.extend([(row + i, col + i), (row + i + 1, col + i + 1), (row + i + 2, col + i + 2)])
            if (0 <= row - i < board_size - 2 and 0 <= col + i < board_size - 2 and
                self.board[row - i][col + i] == 'S' and
                self.board[row - i - 1][col + i + 1] == 'O' and
                self.board[row - i - 2][col + i + 2] == 'S'):
                found_sos = True
                sos_positions.extend([(row - i, col + i), (row - i - 1, col + i + 1), (row - i - 2, col + i + 2)])

        return found_sos, sos_positions

    def check_winner(self, row, col, char):
        found_sos, sos_positions = self.check_sos(row, col, char)
        if found_sos:
            current_player = self.player_turn[0]

            frames = self.tiger_frames if current_player == 1 else self.lion_frames
            for pos in sos_positions:
                r, c = pos
                if self.buttons[r][c].animation_id:
                    self.board_window.after_cancel(self.buttons[r][c].animation_id)
                    self.buttons[r][c].animation_id = None
                self.update_button_image(self.buttons[r][c], frames)

            if current_player == 1:
                self.player1_score += 1
                print(f"Player 1 scores a point! ({row}, {col}) is part of an SOS sequence. Current Score: {self.player1_score}")
            else:
                self.player2_score += 1
                print(f"Player 2 scores a point! ({row}, {col}) is part of an SOS sequence. Current Score: {self.player2_score}")
            self.update_scoreboard()
            return True
        return False

    def check_game_end(self):
        if all(cell != '' for row in self.board for cell in row):
            if self.player1_score > self.player2_score:
                winner = self.player1
            elif self.player2_score > self.player1_score:
                winner = self.player2
            else:
                winner = "No one, it's a tie!"
            messagebox.showinfo("Game Over", f"Game Over! The winner is: {winner}")
            self.board_window.destroy()
            self.root.destroy()

def open_multiplayer_board(root, player1, player2):
    MultiplayerBoard(root, player1, player2)

if __name__ == "__main__":
    # This part is optional and can be used to test the board independently
    root = tk.Tk()
    # Load custom font for the main window
    root.option_add("*Font", "Digital-7 12")
    open_multiplayer_board(root, "Player 1", "Player 2")
    root.mainloop()
