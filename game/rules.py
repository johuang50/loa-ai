from game.board import EMPTY, BOARD_SIZE

def count_pieces_in_direction(board, x, y, dx, dy, player):
    max_piece = float('inf')
    count = 0
    dist_count = 0
    i, j = x + dx, y + dy
    while 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE:
        dist_count += 1
        if board[i][j] != EMPTY:
            count += 1

            if board[i][j] == -player and max_piece == float('inf'):
                max_piece = dist_count

        i += dx
        j += dy
    i, j = x - dx, y - dy
    while 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE:
        if board[i][j] != EMPTY:
            count += 1

        i -= dx
        j -= dy
    
    if count + 1 > max_piece:
        count = 'invalid'


    return count

def generate_moves(board, player):
    directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
    moves = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == player:
                for dx, dy in directions:
                    dist = count_pieces_in_direction(board, x, y, dx, dy, player)

                    if dist == 'invalid':
                        continue

                    dist += 1

                    nx, ny = x + dx * dist, y + dy * dist
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                        if board[nx][ny] in [EMPTY, -player]:
                            moves.append(((x, y), (nx, ny)))
    return moves

def is_win(board, player):
    visited = set()
    group_found = False

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == player and (x, y) not in visited:
                if group_found:
                    # If another group is found, the player hasn't won
                    return False
                explore_group(board, x, y, player, visited)
                group_found = True

    # If exactly one group is found, the player has won
    return group_found

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

