from tkinter import messagebox
import pygame

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
