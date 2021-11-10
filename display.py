import pygame
import colors
import numpy as np
import board as Board

screen_width, screen_height = 500, 600
screen_grid_line_thickness = 4
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")


screen_grid_cell_width = screen_width / Board.width
screen_grid_cell_height = screen_height / Board.height


def draw_grid():
    color = (100, 100, 100)
    # Draw cols
    for i in range(Board.width+1):
        x = i * (screen_width/Board.width)
        pygame.draw.line(screen, color, (x, 0), (x, screen_height), screen_grid_line_thickness)

    # Draw rows
    for i in range(Board.height+1):
        y = i * (screen_height/Board.height)
        pygame.draw.line(screen, color, (0, y), (screen_width, y), screen_grid_line_thickness)

def draw_board(board):
    for y, row in enumerate(board):
        for x, col in enumerate(row):
            draw_cell(x, y, colors.colors[col])

def draw_player(player, color):
    for x, y in player:
        draw_cell(x, y, color)

def draw_cell(x, y, color):
    x0 = x*screen_grid_cell_width + np.ceil(screen_grid_line_thickness//2) 
    y0 = y*screen_grid_cell_height + np.ceil(screen_grid_line_thickness//2)
    points = [x0, y0, screen_grid_cell_width - np.ceil(screen_grid_line_thickness//2), screen_grid_cell_height - np.ceil(screen_grid_line_thickness//2)]
    pygame.draw.rect(screen, color, points)


def update(player, player_color, board):
    screen.fill(colors.black)
    draw_grid()
    draw_board(board)
    draw_player(player, player_color)
    pygame.display.update()
    pygame.time.wait(10)










