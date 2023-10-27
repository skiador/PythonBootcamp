import numpy as np
PLAYER1 = "X"
PLAYER2 = "O"
board_items = [[' ', ' ', ' '] for _ in range(3)]


def display_board():
    board = (
        f"  {board_items[0][0]}  |  {board_items[0][1]}  |  {board_items[0][2]}  \n"
             f"-----------------\n"
             f"  {board_items[1][0]}  |  {board_items[1][1]}  |  {board_items[1][2]}  \n"
             f"-----------------\n"
             f"  {board_items[2][0]}  |  {board_items[2][1]}  |  {board_items[2][2]}  \n"
    )

    print(board)


def add_piece(row, column, piece):
    board_items[row][column] = piece


def prompt_for_move(player):
    while True:
        try:
            print(f"{player} turn:")
            row = int(input("Enter row: ")) - 1
            column = int(input("Enter column:")) - 1

            if 0 <= row <= 2 and 0 <= column <= 2:
                if board_items[row][column] == ' ':
                    add_piece(row, column, player)
                    break
                else:
                    print("This position is already occupied.")
            else:
                print("Enter a valid position.")
        except:
            print("Please enter a valid integer 0-2")




def check_end_game():
    for row in board_items:
        if row[0] == row[1] == row[2] != ' ':
            return True

    for col in range(3):
        if board_items[0][col] == board_items[1][col] == board_items[2][col] != ' ':
            return True
    if board_items[0][0] == board_items[1][1] == board_items[2][2] != ' ':
        return True
    if board_items[0][2] == board_items[1][1] == board_items[2][0] != ' ':
        return True

    return False


enter = input("Welcome to tic tac toe. Please press enter to start the game...")
display_board()

while not check_end_game():
    for player in [PLAYER1, PLAYER2]:
        prompt_for_move(player)
        display_board()
        if check_end_game():
            print(f"Player {player} wins!")
            break



