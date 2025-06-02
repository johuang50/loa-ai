import numpy as np
from ai.heuristic import heuristic


def evaluate_position(board, player):
    if not isinstance(board, np.ndarray):
        board = np.array(board, dtype=np.int32)
    return heuristic(board, player)
