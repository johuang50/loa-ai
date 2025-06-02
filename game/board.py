EMPTY = 0
BLACK = 1
WHITE = -1
BOARD_SIZE = 8

def initial_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for i in range(1, 7):
        board[0][i] = BLACK
        board[7][i] = BLACK
        board[i][0] = WHITE
        board[i][7] = WHITE
    return board

def make_move(board, move):
    (x1, y1), (x2, y2) = move
    board[x2][y2] = board[x1][y1]
    board[x1][y1] = EMPTY
    return board

