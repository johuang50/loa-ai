from game.board import EMPTY, BOARD_SIZE

def count_pieces_in_direction(board, x, y, dx, dy):
    count = 0
    i, j = x + dx, y + dy
    while 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE:
        if board[i][j] != EMPTY:
            count += 1
        i += dx
        j += dy
    i, j = x - dx, y - dy
    while 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE:
        if board[i][j] != EMPTY:
            count += 1
        i -= dx
        j -= dy
    return count + 1

def generate_moves(board, player):
    directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
    moves = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == player:
                for dx, dy in directions:
                    dist = count_pieces_in_direction(board, x, y, dx, dy)
                    nx, ny = x + dx * dist, y + dy * dist
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                        if board[nx][ny] in [EMPTY, -player]:
                            moves.append(((x, y), (nx, ny)))
    return moves

