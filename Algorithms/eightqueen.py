def print_solution(board):
    for row in board:
        print(' '.join('Q' if col else '.' for col in row))
    print()


def is_safe(board, row, col):
    # Check this row on left side
    for i in range(col):
        if board[row][i]:
            return False

    for i in range(row):
        if board[i][col]:
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j]:
            return False

    for i, j in zip(range(row, len(board), -1), range(col, len(board), -1)):
        if board[i][j]:
            return False

    for i, j in zip(range(row, len(board), 1), range(col, -1, -1)):
        if board[i][j]:
            return False

    for i, j in zip(range(row, -1, -1), range(col, len(board), -1)):
        if board[i][j]:
            return False

    return True


c = 0


def solve_queens_algo(board, col):
    # Base case: If all queens are placed
    global c
    if col >= len(board):
        c += 1
        print_solution(board)
        return True

    res = False
    for i in range(len(board)):
        if is_safe(board, i, col):
            # Place this queen in the current position
            board[i][col] = True

            # Recur to place the rest of the queens (simulation)
            res = solve_queens_algo(board, col + 1) or res

            # If placing queen in this position doesn't lead to a solution
            # then remove the queen (backtrack)
            board[i][col] = False
    return res


def solve_queens(n):
    board = [[False] * n for i in range(n)]
    if not solve_queens_algo(board, 0):
        print("No solution exists")


# Run the solver for 8-Queens problem
if __name__ == '__main__':
    solve_queens(4)
    print("the number of solutions are : ", c)
