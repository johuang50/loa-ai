import numpy as np
cimport numpy as np

from game.rules import generate_moves
from game.board import BOARD_SIZE

ctypedef np.int32_t INT_t

cdef void explore_group(np.ndarray[INT_t, ndim=2] board, int x, int y, int player, set visited):
    cdef int dx, dy, nx, ny
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    if board[nx, ny] == player and (nx, ny) not in visited:
                        stack.append((nx, ny))

cpdef int count_groups(np.ndarray[INT_t, ndim=2] board, int player):
    cdef int x, y, groups = 0
    visited = set()
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x, y] == player and (x, y) not in visited:
                groups += 1
                explore_group(board, x, y, player, visited)
    return groups

cpdef int mobility(np.ndarray[INT_t, ndim=2] board, int player):
    return len(generate_moves(board, player))

cpdef float piece_spread(np.ndarray[INT_t, ndim=2] board, int player):
    cdef int i, j, x1, y1, x2, y2, total = 0, count = 0
    cdef int positions[64][2]
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i, j] == player:
                positions[count][0] = i
                positions[count][1] = j
                count += 1
    for i in range(count):
        for j in range(i + 1, count):
            x1, y1 = positions[i][0], positions[i][1]
            x2, y2 = positions[j][0], positions[j][1]
            total += abs(x1 - x2) + abs(y1 - y2)
    return float(total)

cpdef float heuristic(np.ndarray[INT_t, ndim=2] board, int player):
    cdef int opponent = -player
    cdef int player_groups = count_groups(board, player)
    cdef int opponent_groups = count_groups(board, opponent)

    cdef int player_mobility = mobility(board, player)
    cdef int opponent_mobility = mobility(board, opponent)

    cdef float player_spread = piece_spread(board, player)
    cdef float opponent_spread = piece_spread(board, opponent)

    return (
        10.0 * (opponent_groups - player_groups) +
        1.0 * (player_mobility - opponent_mobility) -
        0.1 * (player_spread - opponent_spread)
    )
