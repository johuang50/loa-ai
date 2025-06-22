from game.board import initial_board, BLACK, WHITE, make_move
from ai.minimax import minimax
from ai.heuristic import heuristic
from game.rules import generate_moves
import copy
import random

def print_board(board):
    symbols = {0: '.', 1: 'B', -1: 'W'}
    for row in board:
        print(" ".join(symbols[cell] for cell in row))
    print()

def get_human_move(board, player):
    moves = generate_moves(board, player)
    move_dict = {str(i): move for i, move in enumerate(moves)}
    print("\nAvailable moves:")
    for i, move in move_dict.items():
        print(f"{i}: {move}")
    choice = str(random.randrange(len(move_dict.items()))) #input("Enter move number: ")
    while choice not in move_dict:
        choice = input("Invalid. Enter move number: ")
    return move_dict[choice]

def is_connected_group(board, player):
    visited = set()
    positions = [(x, y) for x in range(8) for y in range(8) if board[x][y] == player]
    if not positions:
        return False

    def dfs(x, y):
        if (x, y) in visited:
            return
        visited.add((x, y))
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] == player:
                    dfs(nx, ny)

    dfs(*positions[0])
    return len(visited) == len(positions)

def game_over(board):
    return is_connected_group(board, BLACK) or is_connected_group(board, WHITE)

def main():
    board = initial_board()
    print_board(board)

    color = input("Do you want to play as black or white? (b/w): ").strip().lower()
    while color not in ['b', 'w']:
        color = input("Invalid. Choose 'b' or 'w': ").strip().lower()
    human = BLACK if color == 'b' else WHITE
    ai = -human

    current_player = BLACK

    while not game_over(board):
        print_board(board)
        print("Current turn:", "Black" if current_player == BLACK else "White")

        if current_player == human:
            move = get_human_move(board, human)
        else:
            _, move = minimax(copy.deepcopy(board), depth=4, player=ai, alpha=float('-inf'),
                              beta=float('inf'), maximizing=True, evaluate=heuristic)
            print("AI chooses:", move)

        board = make_move(board, move)
        current_player *= -1

    print_board(board)
    print("Game Over!")
    if is_connected_group(board, human):
        print("You win!")
    elif is_connected_group(board, ai):
        print("AI wins!")
    else:
        print("Draw!")

if __name__ == "__main__":
    main()
