import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import pygame
from sos_game_utils import update_scoreboard, increment_score, update_button_image, check_sos, check_winner, check_game_end, handle_click_ai, bind_tooltip, player_turn, player1_score, player2_score

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

def evaluate_board(board):
    score = 0
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 'S':
                if col + 2 < len(board[0]) and board[row][col + 1] == 'O' and board[row][col + 2] == 'S':
                    score += 1
                if row + 2 < len(board) and board[row + 1][col] == 'O' and board[row + 2][col] == 'S':
                    score += 1
                if row + 2 < len(board) and col + 2 < len(board[0]) and board[row + 1][col + 1] == 'O' and board[row + 2][col + 2] == 'S':
                    score += 1
                if row + 2 < len(board) and col - 2 >= 0 and board[row + 1][col - 1] == 'O' and board[row + 2][col - 2] == 'S':
                    score += 1
            elif board[row][col] == 'O':
                if col - 1 >= 0 and col + 1 < len(board[0]) and board[row][col - 1] == 'S' and board[row][col + 1] == 'S':
                    score += 1
                if row - 1 >= 0 and row + 1 < len(board) and board[row - 1][col] == 'S' and board[row + 1][col] == 'S':
                    score += 1
                if row - 1 >= 0 and row + 1 < len(board) and col - 1 >= 0 and col + 1 < len(board[0]) and board[row - 1][col - 1] == 'S' and board[row + 1][col + 1] == 'S':
                    score += 1
                if row - 1 >= 0 and row + 1 < len(board) and col + 1 < len(board[0]) and col - 1 >= 0 and board[row - 1][col + 1] == 'S' and board[row + 1][col - 1] == 'S':
                    score += 1
    return score

import random

def initialize_population(board, population_size=10):
    population = []
    for _ in range(population_size):
        individual = {'move': (random.randint(0, len(board) - 1), random.randint(0, len(board[0]) - 1)), 'char': random.choice(['S', 'O'])}
        population.append(individual)
    return population

def evaluate_fitness(board, individual):
    row, col = individual['move']
    char = individual['char']
    if board[row][col] != '':
        return -1000  # Invalid move, very low fitness

    temp_board = [row[:] for row in board]
    temp_board[row][col] = char
    fitness_score = evaluate_board(temp_board)
    
    # Adding a base fitness score to avoid zero fitnesses
    return fitness_score if fitness_score > 0 else 1

def select_parents(population, fitnesses):
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        return random.sample(population, 2)  # fallback to random selection if all fitnesses are zero
    probabilities = [fitness / total_fitness for fitness in fitnesses]
    parents = random.choices(population, probabilities, k=2)
    return parents

def crossover(parent1, parent2):
    return {'move': parent1['move'], 'char': parent2['char']}

def mutate(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        individual['move'] = (random.randint(0, len(board) - 1), random.randint(0, len(board[0]) - 1))
    if random.random() < mutation_rate:
        individual['char'] = random.choice(['S', 'O'])
    return individual

def genetic_algorithm(board, generations=10, population_size=10, mutation_rate=0.1):
    population = initialize_population(board, population_size)
    for _ in range(generations):
        fitnesses = [evaluate_fitness(board, individual) for individual in population]
        new_population = []
        for _ in range(population_size):
            parent1, parent2 = select_parents(population, fitnesses)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        population = new_population

    fitnesses = [evaluate_fitness(board, individual) for individual in population]
    best_individual = population[fitnesses.index(max(fitnesses))]
    return best_individual['move'], best_individual['char']

def ai_make_move(board, buttons, fire_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2):
    if player_turn[0] == 2:  # AI's turn (player 2)
        best_move, best_char = genetic_algorithm(board)
        if best_move != (-1, -1):
            row, col = best_move
            handle_click_ai(None, row, col, board, buttons, fire_frames if best_char == 'S' else water_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2)
            
            # Check if the AI should make another move
            while player_turn[0] == 2:  # Check if it's still AI's turn
                best_move, best_char = genetic_algorithm(board)
                if best_move != (-1, -1):
                    row, col = best_move
                    handle_click_ai(None, row, col, board, buttons, fire_frames if best_char == 'S' else water_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2)
                else:
                    break


def apply_genetic_algorithm(root_window, p1, p2):
    global board_window, player1, player2, board_size, board, buttons, scoreboard_frame
    global fire_frames, water_frames, forest_frames, tiger_frames, lion_frames

    player1 = p1
    player2 = p2

    pygame.mixer.music.stop()  # Stop the background music of the root window

    board_window = tk.Toplevel(root_window)
    board_window.title("SOS-HARD MODE")

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

    background_image = Image.open("resources/images/background_hard.jpg")
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

    update_scoreboard(scoreboard_frame, player1, player2)

    board_size = 6
    board = [['' for _ in range(board_size)] for _ in range(board_size)]

    fire_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/fire.gif"))]
    water_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/water.gif"))]
    forest_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/forest.gif"))]
    tiger_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/human.gif"))]
    lion_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/robot.gif"))]

    buttons = [[None for _ in range(board_size)] for _ in range(board_size)]
    for row in range(board_size):
        for col in range(board_size):
            button = ttk.Button(board_frame, text='', width=5, command=lambda r=row, c=col: handle_click_ai(None, r, c, board, buttons, fire_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root_window, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2, ai_make_move))
            
            button.grid(row=row, column=col, padx=5, pady=5)
            button.config(image=forest_frames[0])
            button.animation_id = None
            update_button_image(button, forest_frames, board_window)
            button.bind('<Button-1>', lambda event, r=row, c=col: handle_click_ai(event, r, c, board, buttons, fire_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root_window, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2, ai_make_move))

            button.bind('<Button-3>', lambda event, r=row, c=col: handle_click_ai(event, r, c, board, buttons, fire_frames, water_frames, tiger_frames, lion_frames, player_turn, board_window, root_window, update_scoreboard, check_winner, check_game_end, bind_tooltip, scoreboard_frame, player1, player2, ai_make_move))
            buttons[row][col] = button

            bind_tooltip(button, "")

    board_window.protocol("WM_DELETE_WINDOW", root_window.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    root.option_add("*Font", "Digital-7 12")
    apply_genetic_algorithm(root, "Player 1", "Player 2")
    root.mainloop()
