import tetrominos
import time
import colors
import numpy as np
import board as Board

# times = {'add_to_board': 0,'validate': 0, 'move':0, 'rotate':0}

def new():
    # Returns a tuple (player, color). Player = np.array([[x0, y0], [x1, y1], ..]). Color = (r, g, b)
    idx = np.random.choice(tetrominos.starts.shape[0])
    tetromino_base = tetrominos.starts[idx].copy()
    color = tetrominos.color_get(tetromino_base)

    # Fix if the tetromino base is of screen... This shouldn't happen but happens due to me being dumb when creating tetrominos
    move_into_screen(tetromino_base)

    player = tetromino_base
    # Move player to middle of screen
    d_to_center = Board.width//2 - player[0][0] - 1
    player = player + np.array([d_to_center, 0])
    return player, color

def die(player, board):
    # Checks if the player dies. It can only die after a new piece is spawned so this should only be called when a new piece is spawend.
    return not valid_movement(player, board)

def down(player, board):
    # Returns a new player which has moved one cell down. Or None if the player encountered the floor or another player, ie die.
    return move(player, 0, 1, board)

def right(player, board):
    return move(player, 1, 0, board)

def left(player, board):
    return move(player, -1, 0, board)

def move(player, dx, dy, board):
    # Move player in [dx dy] direction. Returns None if an invalid position was moved into
    start_t = time.perf_counter_ns()
    new_player = player + np.array([dx, dy])
    # times['move'] += (time.perf_counter_ns() - start_t)/1e6
    if not valid_movement(new_player, board):
        return None
    return new_player

def valid_movement(player, board):
    # Check if a movement is valid by checking if there's a crash downward or sidewards, or out of limit
    # I don't understand why return np.any(board[player]) doesn't work
    start_t = time.perf_counter_ns()
    for x, y in player:
        # Check for colliding with floor
        if y > Board.height - 1:
            # times['validate'] += (time.perf_counter_ns() - start_t)/1e6
            return False
        # Check for colliding with sides
        if x < 0:
            # times['validate'] += (time.perf_counter_ns() - start_t)/1e6
            return False
        elif x >= Board.width:
            # times['validate'] += (time.perf_counter_ns() - start_t)/1e6
            return False
        # Check for collision with other blocks
        if board[y, x]:
            # times['validate'] += (time.perf_counter_ns() - start_t)/1e6
            return False
    # times['validate'] += (time.perf_counter_ns() - start_t)/1e6
    return True 

def move_into_screen(player):
    x_min, x_max = player[:, 0].min(), player[:, 0].max()
    if x_min < 0:
        player[:,0] -= x_min
    elif x_max > Board.width-1:
        player[:,0] -= x_max - (Board.width - 1) 

    y_min, y_max = player[:, 1].min(), player[:, 1].max()
    if y_min < 0:
        player[:,1] -= y_min
    elif y_max > Board.height-1:
        player[:,1] -= y_max - (Board.height - 1) 


# rotate_times = {"rotate":0, "move_into_screen":0}
def rotate(player, board):
    start_t = time.perf_counter_ns()
    player = player.copy()
    base = player[0].copy()
    player -= base
    
    start_t_rotate = time.perf_counter_ns()
    player = tetrominos.rotate(player)
    # rotate_times['rotate'] += (time.perf_counter_ns() - start_t_rotate)/1e6
    player += base

    # Move it back into screen if needed
    start_t_move_into_screen = time.perf_counter_ns()
    move_into_screen(player)
    # rotate_times['move_into_screen'] += (time.perf_counter_ns() - start_t_move_into_screen)/1e6

    # times['rotate'] += (time.perf_counter_ns() - start_t)/1e6
    # Make sure no overlap with existing pieces
    if not valid_movement(player, board):
        return None
    return player


def add_to_board(player, color, board):
    start_t = time.perf_counter_ns()
    board = board.copy()
    color_idx = colors.color_idx_map[color]
    for x, y in player:
        board[y, x] = color_idx
    
    # times['add_to_board'] += (time.perf_counter_ns() - start_t)/1e6
    return board

def calc_scores(row_destroyed_n):
    if row_destroyed_n == 1:
        return 40
    elif row_destroyed_n == 2:
        return 100
    elif row_destroyed_n == 3:
        return 300
    elif row_destroyed_n == 4:
        return 1200
    else:
        return 0
