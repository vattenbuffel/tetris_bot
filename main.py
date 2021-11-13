import board as Board
import numpy as np # Delete this. It's only used for debugging
from Actions import Actions
import display as Display
import player as Player
import game as Game
import bot as Bot
import pygame

# bot_playing = False
bot_playing = True
prev_states_n = 10**10


player, player_color = Player.new()
player_score = 0
board = Board.new()

def get_human_actions():
    events = pygame.event.get()
    actions = []
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                actions.append(Actions.LEFT)
            elif event.key == pygame.K_s:
                actions.append(Actions.DOWN)
            elif event.key == pygame.K_d:
                actions.append(Actions.RIGHT)
            elif event.key == pygame.K_w:
                actions.append(Actions.ROTATE)
            elif event.key == pygame.K_ESCAPE:
                exit() 
            
    return actions

import time
prev_t = time.perf_counter()

while True:
    Display.update(player, player_color, board)
    actions = get_human_actions()
    if bot_playing and time.perf_counter() - prev_t > 0.016:
        action_t = time.perf_counter_ns()
        action, states_n = Bot.action_get(player, board)
        prev_states_n = states_n
        actions = [action]
        # print(f"It took: {(time.perf_counter_ns() - action_t)/1000000} ms to calculate bot action. It evaluated: {states_n} possible board states")
        prev_t = time.perf_counter()

    for action in actions:
        new_player = Game.perform_action(player, board, action)
        res = Game.after_action(player, new_player, player_color, player_score, board, action)
        if res is None:
            print("You died")
            exit(0)
        else:
            player, player_score, player_color, board, player_died = res
            if player_died:
                prev_states_n = 10**10






