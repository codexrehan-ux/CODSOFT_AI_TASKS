"""CodSoft AI Internship - Task 2
Tic-Tac-Toe AI using the Minimax algorithm.
"""

HUMAN = "X"
AI = "O"
EMPTY = " "


def print_board(board):
    print("\n  1   2   3")
    for row in range(3):
        print(f"{row + 1} {board[row][0]} | {board[row][1]} | {board[row][2]}")
        if row < 2:
            print("  --+---+--")
    print()


def available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == EMPTY]


def check_winner(board):
    lines = []
    lines.extend(board)
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line[0] != EMPTY and line.count(line[0]) == 3:
            return line[0]
    return None


def minimax(board, maximizing):
    winner = check_winner(board)
    if winner == AI:
        return 1
    if winner == HUMAN:
        return -1
    if not available_moves(board):
        return 0

    if maximizing:
        best_score = -float("inf")
        for row, col in available_moves(board):
            board[row][col] = AI
            score = minimax(board, False)
            board[row][col] = EMPTY
            best_score = max(best_score, score)
        return best_score

    best_score = float("inf")
    for row, col in available_moves(board):
        board[row][col] = HUMAN
        score = minimax(board, True)
        board[row][col] = EMPTY
        best_score = min(best_score, score)
    return best_score


def best_ai_move(board):
    best_score = -float("inf")
    best_move = None

    for row, col in available_moves(board):
        board[row][col] = AI
        score = minimax(board, False)
        board[row][col] = EMPTY

        if score > best_score:
            best_score = score
            best_move = (row, col)

    return best_move


def get_human_move(board):
    while True:
        try:
            row, col = map(int, input("Enter your move (row column): ").split())
            row -= 1
            col -= 1

            if row not in range(3) or col not in range(3):
                print("Please enter row and column numbers from 1 to 3.")
            elif board[row][col] != EMPTY:
                print("That position is already occupied. Choose another.")
            else:
                return row, col
        except ValueError:
            print("Invalid input. Enter two numbers, for example: 2 3")


def main():
    board = [[EMPTY for _ in range(3)] for _ in range(3)]

    print("=" * 45)
    print("       CODSOFT - TIC-TAC-TOE AI")
    print("=" * 45)
    print("You are X. The AI is O.")
    print("The AI uses the Minimax algorithm.\n")

    while True:
        print_board(board)
        row, col = get_human_move(board)
        board[row][col] = HUMAN

        winner = check_winner(board)
        if winner or not available_moves(board):
            break

        ai_move = best_ai_move(board)
        if ai_move:
            board[ai_move[0]][ai_move[1]] = AI
            print(f"AI chooses: {ai_move[0] + 1} {ai_move[1] + 1}")

        winner = check_winner(board)
        if winner or not available_moves(board):
            break

    print_board(board)
    winner = check_winner(board)

    if winner == HUMAN:
        print("Congratulations! You won!")
    elif winner == AI:
        print("AI wins. Better luck next time!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
