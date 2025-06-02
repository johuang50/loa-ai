from game.rules import generate_moves, apply_move
from ai.eval import evaluate_position


def minimax(board, depth, player, maximizing, alpha, beta):
    if depth == 0:
        return evaluate_position(board, player), None

    best_move = None
    if maximizing:
        max_eval = float("-inf")
        for move in generate_moves(board, player):
            new_board = apply_move(board, move)
            eval_score, _ = minimax(new_board, depth - 1, player, False, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for move in generate_moves(board, -player):
            new_board = apply_move(board, move)
            eval_score, _ = minimax(new_board, depth - 1, player, True, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move
