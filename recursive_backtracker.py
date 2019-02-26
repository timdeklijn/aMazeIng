"""recursive_backtracker

Wikipedia (https://en.wikipedia.org/wiki/Maze_generation_algorithm):
The depth-first search algorithm of maze generation is frequently implemented 
using backtracking:

1. Make the initial cell the current cell and mark it as visited
2. While there are unvisited cells
    1. If the current cell has any neighbours which have not been visited
        1. Choose randomly one of the unvisited neighbours
        2. Push the current cell to the stack
        3. Remove the wall between the current cell and the chosen cell
        4. Make the chosen cell the current cell and mark it as visited
    2. Else if stack is not empty
        1. Pop a cell from the stack
        2. Make it the current cell
"""

__author__ = "Tim de Klijn"
__vershion__ = "0.0"

import numpy as np
from plotMaze import PlotMaze
from collections import namedtuple
import itertools
import pandas as pd

# maze size (cells)
WIDTH = 30
HEIGHT = 30

def initiate_maze():
    """Create maze by filling list with cells"""

    # Create dataframe
    maze = pd.DataFrame(
            columns = [
                "visited", 
                "left", 
                "up", 
                "right", 
                "down", 
                "x", 
                "y"])

    # Fill dataframe
    for x,y in itertools.product(range(WIDTH), range(HEIGHT)):
        maze = maze.append({
            "visited": False, 
            "left": True, 
            "up": True, 
            "right": True, 
            "down": True, 
            "x": x,
            "y": y}, ignore_index=True)

    # Set entrance and exit
    maze = set_walls(0, 0, 
            np.array([True, True, True, False]), maze)
    maze = set_walls(WIDTH-1, HEIGHT-1, 
            np.array([True, True, False, True]), maze)
    return maze


def set_walls(x, y, walls, maze):
    """Set wall status of a cell"""

    maze.loc[((maze.x == x) & (maze.y == y)),
            ["left", "up", "right", "down"]] *= walls
    return maze

def set_visited(x, y, maze):
    """For a certain x and y set visited to True"""
    maze.loc[((maze.x == x) & (maze.y == y)),
            "visited"] = True
    return maze

def unvisited_left(maze):
    """Count unvisited cells in the maze"""
    if maze.visited.sum() < maze.size:
        return True
    else:
        return False

def find_unvisited_neighbours(maze, current_cell):
    """
    For all possible neighbours of the current cell check if it has
    neighbours
    """
    x, y = current_cell
    return maze[((maze.x == x-1) & (maze.y == y) & (maze.visited == False)) |
                ((maze.x == x+1) & (maze.y == y) & (maze.visited == False)) |
                ((maze.x == x) & (maze.y == y-1) & (maze.visited == False)) |
                ((maze.x == x) & (maze.y == y+1) & (maze.visited == False)) ]


def push_current_to_stack(current, stack, maze): 
    """Find current cell and append to stack"""
    stack = stack.append(
           maze.loc[(maze.x == current[0]) &
                    (maze.y == current[1])],
                    ignore_index = True)
    return stack

def remove_walls(current_cell, new_cell_coords, maze):
    """Remove walls between neighbours"""
    yc, xc = current_cell
    yn, xn = new_cell_coords

    # Find type of neighbour and set wall destruction
    if xc < xn:
        current = np.array([True, True, False, True])
        new = np.array([False, True, True, True])
    if xc > xn:
        current = np.array([False, True, True, True])
        new = np.array([True, True, False, True])
    if yc < yn:
        current = np.array([True, False, True, True])
        new = np.array([True, True, True, False])
    if yc > yn:
        current = np.array([True, True, True, False])
        new = np.array([True, False, True, True])

    maze = set_walls(xc, yc, current, maze)
    maze = set_walls(xn, yn, new, maze)

    return maze


def recursive(maze):
    """Perform recursive backtracker algoirthm"""
    stack = pd.DataFrame(
                columns = [
                    "visited", 
                    "left", 
                    "up", 
                    "right", 
                    "down", 
                    "x", 
                    "y"])
    # start cell
    current_cell = [0, 0]
    while unvisited_left(maze):
        maze = set_visited(current_cell[0], current_cell[1], maze)
        # find neighbours
        neighbours = find_unvisited_neighbours(maze, current_cell)
        if neighbours.size > 0:
            # choose random new cell
            new_cell = neighbours.sample(1, axis=0)
            new_cell_coords = new_cell[["x", "y"]].values[0]
            # push current cell to stack
            stack = push_current_to_stack(current_cell, stack, maze)
            # remove walls
            maze = remove_walls(current_cell, new_cell_coords, maze)
            current_cell = new_cell_coords
        elif stack.size > 0:
            # Get item from stack
            stack, c =stack.drop(stack.tail(1).index), stack.tail(1)
            current_cell = c[["x", "y"]].values[0]
        else:
            break


if __name__ == "__main__":
    # maze with all walls 
    maze = initiate_maze()
    recursive(maze)

    # plot maze
    p = PlotMaze(WIDTH, HEIGHT, maze)
    p.plot()
