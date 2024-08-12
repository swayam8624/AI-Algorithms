import math

# Define the board
board = [
    ['_', '_', '_'],
    ['_', '_', '_'],
    ['_', '_', '_']
]


# Function to print the board
def print_board(board):
    for row in board:
        print(" ".join(row))
    print()


# Function to check if there are moves left on the board
def is_moves_left(board):
    for row in board:
        if '_' in row:
            return True
    return False


# Function to evaluate the board
def evaluate(board):
    # Check rows for a win
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != '_':
            return 10 if row[0] == 'X' else -10

    # Check columns for a win
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '_':
            return 10 if board[0][col] == 'X' else -10

    # Check diagonals for a win
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '_':
        return 10 if board[0][0] == 'X' else -10
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '_':
        return 10 if board[0][2] == 'X' else -10

    # No winner
    return 0


# Minimax function with alpha-beta pruning
def minimax(board, depth, is_max, alpha, beta):
    score = evaluate(board)

    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if not is_moves_left(board):
        return 0

    if is_max:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'X'
                    best = max(best, minimax(board, depth + 1, not is_max, alpha, beta))
                    board[i][j] = '_'
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'O'
                    best = min(best, minimax(board, depth + 1, not is_max, alpha, beta))
                    board[i][j] = '_'
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best


# Function to find the best move
def find_best_move(board):
    best_val = -math.inf
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = 'X'
                move_val = minimax(board, 0, False, -math.inf, math.inf)
                board[i][j] = '_'
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    return best_move


# Function to check if the game is over
def is_game_over(board):
    score = evaluate(board)
    if score == 10 or score == -10 or not is_moves_left(board):
        return True
    return False


# Main function to play the game
def play_game():
    print("Initial Board:")
    print_board(board)

    while not is_game_over(board):
        # Player's turn
        print("Player's Turn (O)")
        player_move = tuple(map(int, input("Enter your move (row and column): ").split()))
        if board[player_move[0]][player_move[1]] == '_':
            board[player_move[0]][player_move[1]] = 'O'
        else:
            print("Invalid move. Try again.")
            continue

        print_board(board)

        if is_game_over(board):
            break

        # AI's turn
        print("AI's Turn (X)")
        best_move = find_best_move(board)
        board[best_move[0]][best_move[1]] = 'X'

        print_board(board)

    # Game over
    score = evaluate(board)
    if score == 10:
        print("AI wins!")
    elif score == -10:
        print("Player wins!")
    else:
        print("It's a draw!")


play_game()
