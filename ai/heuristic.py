from game.rules import generate_moves, is_win
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


def centralization(board, player):
    center = BOARD_SIZE // 2
    positions = [
        (x, y)
        for x in range(BOARD_SIZE)
        for y in range(BOARD_SIZE)
        if board[x][y] == player
    ]
    return sum(abs(x - center) + abs(y - center) for x, y in positions)


def edge_proximity(board, player):
    positions = [
        (x, y)
        for x in range(BOARD_SIZE)
        for y in range(BOARD_SIZE)
        if board[x][y] == player
    ]
    return sum(
        min(x, BOARD_SIZE - 1 - x, y, BOARD_SIZE - 1 - y) for x, y in positions
    )


def find_winning_move(board, player):
    moves = generate_moves(board, player)
    for move in moves:
        (from_x, from_y), (to_x, to_y) = move  # Correctly unpack the tuple
        temp_board = [row[:] for row in board]
        temp_board[to_x][to_y] = temp_board[from_x][from_y]
        temp_board[from_x][from_y] = 0
        if is_win(temp_board, player):
            return move
    return None


def heuristic(board, player):
    # Check for a winning move
    winning_move = find_winning_move(board, player)
    if winning_move:
        return float("inf"), winning_move

    opponent = -player
    player_groups = count_groups(board, player)
    opponent_groups = count_groups(board, opponent)

    player_mobility = mobility(board, player)
    opponent_mobility = mobility(board, opponent)

    player_spread = piece_spread(board, player)
    opponent_spread = piece_spread(board, opponent)

    player_centralization = centralization(board, player)
    opponent_centralization = centralization(board, opponent)

    player_edge_proximity = edge_proximity(board, player)
    opponent_edge_proximity = edge_proximity(board, opponent)

    score = (
        10 * (opponent_groups - player_groups)  # fewer groups is better
        + 1 * (player_mobility - opponent_mobility)  # more mobility is better
        - 0.1 * (player_spread - opponent_spread)  # tighter piece clustering is better
        + 0.5 * (opponent_centralization - player_centralization)  # closer to center is better
        - 0.2 * (player_edge_proximity - opponent_edge_proximity)  # avoid edges
    )
    return score, None
