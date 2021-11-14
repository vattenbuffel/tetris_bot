from numpy.core.shape_base import block
import yaml
import numpy as np
import player as Player
import game as Game
from Actions import Actions
from GameState import GameState
import colors as Colors
import board as Board
import time

with open("bot_weights.yaml", 'r') as stream:
    weights = yaml.safe_load(stream)

times = {'action':0, "create_child":0, "hit_floor":0, "dict_math":0}

def action_get(player, board) -> Actions:
    base_state = GameState(board, player, Actions.NONE, 0, None)
    states_n = build_state_tree(base_state, prev_player_dict={})
    goal_state:GameState = base_state.best_child(end_child=False)

    # Print the costs 
    # best_state = base_state.best_child(end_child=True)
    # eval_board(best_state.board, best_state.player, 0, verbose=True)    

    # For timing debugging
    global times
    times = {key:0 for key in times}
    return goal_state.action, states_n

def build_state_tree(parent:GameState, states_n=0, depth=0, prev_player_dict={}):
    # Populates parent with all possible children states

    states_n += 1

    for action in Actions:
        start_t = time.perf_counter_ns()
        if action == Actions.NONE:
            continue

        res = Game.perform_action(parent.player, parent.board, action)
        times["action"] += (time.perf_counter_ns() - start_t)/(1e6)

        # Player got to same state, ie hitting a wall or action was NONE for example
        if res is None and action != Actions.DOWN:
            continue

        start_t = time.perf_counter_ns()
        child:GameState = GameState(parent.board, parent.player, action, depth, parent)        
        times["create_child"] += (time.perf_counter_ns() - start_t)/(1e6)
        # Player collided with floor
        if res is None and action == Actions.DOWN:
            start_t = time.perf_counter_ns()
            child.end = True
            child.value = eval_board(parent.board, parent.player, depth)
            parent.children.append(child)
            # print(f"Actions: {[action.name for action in child.actions_get()]}, value: {child.value}")
            times["hit_floor"] += (time.perf_counter_ns() - start_t)/(1e6)
            continue
        
        player = res
        # If player got to a position previously visited and in more steps, continue
        start_t = time.perf_counter_ns()
        player_tuple = tuple(tuple(row) for row in player)
        if player_tuple in prev_player_dict and prev_player_dict[player_tuple] <= depth:
            continue
        prev_player_dict[player_tuple] = depth
        times["dict_math"] += (time.perf_counter_ns() - start_t)/(1e6)

        # Valid movement. Update player's position
        child.player = player
        parent.children.append(child)


    # Caclulate children's children
    # assert (len(parent.children) != 0 and not parent.end) or tuple(tuple(row) for row in player) in prev_player_dict
    for child in parent.children:
        if not child.end:
            states_n = build_state_tree(child, states_n=states_n, depth=depth+1, prev_player_dict=prev_player_dict)

    return states_n
        

def eval_board(board, player, depth, verbose=False):
    # Depth is how many actions it took to get here

    player_board = Player.add_to_board(player, Colors.blue, board)
    cost = 0

    # Calculate cost for holes in all rows with blocks in them
    hole_cost = 0
    for y, row in enumerate(player_board):
        if np.any(row):
            holes = row == 0
            hole_cost -= np.sum(holes)*weights['hole'] * y
    cost += hole_cost

    # Calculate cost for holes adjacent to player
    adjacent_hole_cost = 0
    processed_pos = set()
    for x, y in player:
        if (x, y) in processed_pos:
            continue
        processed_pos.add((x, y))

        left = board[y][:x].copy()
        right = board[y][x+1:].copy()

        for x_, y_ in player:
            if (x_, y_) in processed_pos:
                continue
            if y_ != y:
                continue
            if x_ < x:
                left[x_-x] = 1
            elif x_ > x:
                right[x_-x-1] = 1
            processed_pos.add((x_, y_))

        left_holes = left == 0
        right_holes =  right == 0
        holes_product = (1+np.sum(right_holes)) * (1+np.sum(left_holes))
        adjacent_hole_cost -= holes_product*weights['adjacent_hole'] * y

    cost += adjacent_hole_cost


    # Calculate bridge cost
    bridge_cost = 0
    for col in (player_board.transpose() > 0):
        block_idx, = np.where(col)
        if np.any(block_idx):
            holes = col[block_idx[0] + 1:] == 0
            bridge_cost -= np.sum(holes) * weights['bridge']
    cost += bridge_cost

    # calculate tetris cost. If placing pieces in the right-most column and not getting tetris, add cost
    tetris_cost = 0
    tetris_cost_enabled = True
    filled_row_idx, = np.where(np.sum(player_board, axis=1)>0)
    if filled_row_idx.size > 0:
        tetris_cost_enabled = filled_row_idx[0] > weights['tetris_height_disable']

    if tetris_cost_enabled:
        xs = player[:,0]
        if Board.width-1 in xs:
            tetris_cost = -weights['tetris']

            tetris_cost = 0 if np.all(xs == Board.width-1) else tetris_cost

            destroyed_n, _ = Board.destroy(player_board.copy())
            got_tetris = destroyed_n == 4
            tetris_cost = 10**10 if got_tetris else tetris_cost 

    cost += tetris_cost

    # well cost. If two adjacent cols have a height difference of more than 4, add a cost
    well_cost = 0
    bottom_top = 0
    highest_top = Board.height-1
    for col in player_board.transpose()[:-1]:
        block_idx, = np.where(col)
        if np.any(block_idx):
            highest_top = np.minimum(highest_top, block_idx[0])
            bottom_top = np.maximum(bottom_top, block_idx[0])
        else:
            bottom_top = 20
    too_high = np.maximum(4, bottom_top - highest_top) - 4 
    well_cost = -too_high**3 * weights['well']
    cost += well_cost

    # height = Board.height - np.min(np.where(np.any(player_board, axis=1)))
    # return height - depth

    if verbose:
        print(f"hole_cost: {hole_cost}, adjacent_hole_cost: {adjacent_hole_cost}, bridge_cost: {bridge_cost}, well_cost: {well_cost}, tetris_cost: {tetris_cost}")

    cost -= depth
    return cost




