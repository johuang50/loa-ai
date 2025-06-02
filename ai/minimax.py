import copy
from game.board import make_move
from game.rules import generate_moves

def minimax(board, depth, player, alpha, beta, maximizing, evaluate):
    if depth == 0:
        return evaluate(board, player), None

    moves = generate_moves(board, player if maximizing else -player)
    if not moves:
        return evaluate(board, player), None

    best_move = None

    if maximizing:
        max_eval = float('-inf')
        for move in moves:
            new_board = make_move(copy.deepcopy(board), move)
            eval, _ = minimax(new_board, depth - 1, player, alpha, beta, False, evaluate)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = make_move(copy.deepcopy(board), move)
            eval, _ = minimax(new_board, depth - 1, player, alpha, beta, True, evaluate)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

