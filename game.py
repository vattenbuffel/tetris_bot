import board as Board
from Actions import Actions
import player as Player
import time

# times = {"left":0, "down":0, "right":0, "rotate":0}

def perform_action(player, board, action:Actions):
    if action == Actions.NONE:
        return None
    elif action == Actions.LEFT:
        start_t = time.perf_counter_ns()
        res = Player.left(player, board)
        # times["left"] += (time.perf_counter_ns() - start_t) / 1e6
        return res
    elif action == Actions.DOWN:
        start_t = time.perf_counter_ns()
        res = Player.down(player, board)
        # times["down"] += (time.perf_counter_ns() - start_t) / 1e6
        return res
    elif action == Actions.RIGHT:
        start_t = time.perf_counter_ns()
        res = Player.right(player, board)
        # times["right"] += (time.perf_counter_ns() - start_t) / 1e6
        return res
    elif action == Actions.ROTATE:
        start_t = time.perf_counter_ns()
        res = Player.rotate(player, board)
        # times["rotate"] += (time.perf_counter_ns() - start_t) / 1e6
        return res
    else:
        raise ValueError(f"Not supported action performed: {action}")

def after_action(old_player, new_player, player_color, player_score, board, action):
    # Call this after an action is performed

    # If player died
    if new_player is None and action == Actions.DOWN:
        board = Player.add_to_board(old_player, player_color, board)
        rows_destroyed_n, board = Board.destroy(board)
        player_score += Player.calc_scores(rows_destroyed_n)
        print(f"Player_score: {player_score}")
        new_player, player_color = Player.new()
        if Player.die(new_player, board):
            return None
        return new_player, player_score, player_color, board, True

    # If an invalid action was tried to be performed
    if new_player is None:
        return old_player, player_score, player_color, board, False

    return new_player, player_score, player_color, board, False

