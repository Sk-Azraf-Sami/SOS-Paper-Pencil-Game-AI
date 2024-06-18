import tkinter as tk

player1_score = 0
player2_score = 0
player_turn = [1]
player1 = "Player 1"
player2 = "Player 2"
scoreboard_frame = None

def initialize_scoreboard(frame, p1, p2, turn):
    global scoreboard_frame, player1, player2, player_turn
    scoreboard_frame = frame
    player1 = p1
    player2 = p2
    player_turn = turn
    update_scoreboard()

def update_scoreboard():
    global player1_score, player2_score, player_turn, scoreboard_frame

    scoreboard_frame.delete("all")
    scoreboard_frame.create_image(0, 0, image=scoreboard_frame.image, anchor="nw")

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
