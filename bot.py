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

# times = {'action':0, "create_child":0, "hit_floor":0, "dict_math":0}

def action_get(player, board) -> Actions:
    base_state = GameState(board, player, Actions.NONE, 0, None)
    # build_start_t = time.perf_counter_ns()
    states_n = build_state_tree(base_state, prev_player_dict={})
    # best_state_t = time.perf_counter_ns()
    goal_state:GameState = base_state.best_child(end_child=False)
    best_state = base_state.best_child(end_child=True)
    eval_board(best_state.board, best_state.player, 0, verbose=True)    
    # print(f"It took: {(best_state_t - build_start_t)/1000000} ms to build tree. It took {(time.perf_counter_ns() - best_state_t)/1000000} ms to find best action" )
    # actions = goal_state.children_actions_get()
    # global times
    # times = {key:0 for key in times}
    return goal_state.action, states_n

def build_state_tree(parent:GameState, states_n=0, depth=0, prev_player_dict={}):
    # Populates parent with all possible children states

    states_n += 1

    for action in Actions:
        start_t = time.perf_counter_ns()
        if action == Actions.NONE:
            continue

        res = Game.perform_action(parent.player, parent.board, action)
        # times["action"] += (time.perf_counter_ns() - start_t)/(1e6)

        # Player got to same state, ie hitting a wall or action was NONE for example
        if res is None and action != Actions.DOWN:
            continue

        start_t = time.perf_counter_ns()
        child:GameState = GameState(parent.board, parent.player, action, depth, parent)        
        # times["create_child"] += (time.perf_counter_ns() - start_t)/(1e6)
        # Player collided with floor
        if res is None and action == Actions.DOWN:
            start_t = time.perf_counter_ns()
            child.end = True
            child.value = eval_board(parent.board, parent.player, depth)
            parent.children.append(child)
            # print(f"Actions: {[action.name for action in child.actions_get()]}, value: {child.value}")
            # times["hit_floor"] += (time.perf_counter_ns() - start_t)/(1e6)
            continue
        
        player = res
        # If player got to a position previously visited and in more steps, continue
        start_t = time.perf_counter_ns()
        player_tuple = tuple(tuple(row) for row in player)
        if player_tuple in prev_player_dict and prev_player_dict[player_tuple] <= depth:
            continue
        prev_player_dict[player_tuple] = depth
        # times["dict_math"] += (time.perf_counter_ns() - start_t)/(1e6)

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


    # well cost
    # well_cost = 0
    # y_player_max = np.max(player[:,1]) 
    # y_board_max = 0 
    # for y in range(Board.height, 0, -1):
    #     if np.any(player_board[y,:]):
    #         y_board_max = y
    #         break
    # well_depth = y_board_max - y_player_max
            




        

    # height = Board.height - np.min(np.where(np.any(player_board, axis=1)))
    # return height - depth

    if verbose:
        print(f"hole_cost: {hole_cost}, adjacent_hole_cost: {adjacent_hole_cost}, bridge_cost: {bridge_cost}")

    cost -= depth
    return cost




