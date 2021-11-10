import numpy as np

width = 10
height = 20

def new():
    return np.zeros((height, width), dtype='int')

def cell_set(row, col, val, board):
    board[row, col] = val
    return board

def destroy(board):
    # Detroy all filled rows, drag the rows above down and fill the top with empty rows
    destroyed_n = 0

    for y, row in enumerate(board):
        if np.all(row):
            destroyed_n += 1
            board[1:y+1, :] = board[0:y, :]
            board[0,:] = np.zeros(width)

    return destroyed_n, board

