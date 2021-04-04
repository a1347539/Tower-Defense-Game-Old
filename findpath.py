from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import numpy as np


def find_path(matrix, start, end):
    matrix = matrix.tolist()
    #print(list(matrix),start[0], start[1],end[0], end[1])

    grid = Grid(matrix=matrix)

    start = grid.node(start[0], start[1])
    end = grid.node(end[0], end[1])

    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path = finder.find_path(start, end, grid)
    
    path_temp = path[0]
        
    path = []
    
    for x, y in path_temp:
        x -= 1
        y -= 1
        path.append((x, y))

    return path
