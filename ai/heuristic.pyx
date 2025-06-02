from game.rules import generate_moves
from game.board import BOARD_SIZE


def count_groups(board, player):
    visited = set()
    groups = 0

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == player and (x, y) not in visited:
                groups += 1
                explore_group(board, x, y, player, visited)
    return groups


def explore_group(board, x, y, player, visited):
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
                    if board[nx][ny] == player and (nx, ny) not in visited:
                        stack.append((nx, ny))


def mobility(board, player):
    return len(generate_moves(board, player))


def piece_spread(board, player):
    positions = [
        (x, y)
        for x in range(BOARD_SIZE)
        for y in range(BOARD_SIZE)
        if board[x][y] == player
    ]
    if not positions:
        return 0
    total_dist = 0
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            (x1, y1), (x2, y2) = positions[i], positions[j]
            total_dist += abs(x1 - x2) + abs(y1 - y2)
    return total_dist


def heuristic(board, player):
    opponent = -player
    player_groups = count_groups(board, player)
    opponent_groups = count_groups(board, opponent)

    player_mobility = mobility(board, player)
    opponent_mobility = mobility(board, opponent)

    player_spread = piece_spread(board, player)
    opponent_spread = piece_spread(board, opponent)

    score = (
        10 * (opponent_groups - player_groups)  # fewer groups is better
        + 1 * (player_mobility - opponent_mobility)  # more mobility is better
        - 0.1 * (player_spread - opponent_spread)  # tighter piece clustering is better
    )
    return score
