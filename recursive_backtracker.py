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
__vershion__ = "0.2"


import numpy as np
from plotMaze import PlotMaze
from collections import namedtuple
import itertools
import pandas as pd
import gc

# maze size (cells)
WIDTH = 80
HEIGHT = 80


def initiate_maze():
    """Create maze by filling list with cells"""
    # Create dataframe
    maze = pd.DataFrame(
            columns = ["visited", "left", "up", "right", 
                       "down", "x", "y"])
    # Fill dataframe
    for x,y in itertools.product(range(WIDTH), range(HEIGHT)):
        maze = maze.append({
            "visited": False, "left": True, "up": True, 
            "right": True, "down": True, "x": x,
            "y": y}, ignore_index=True)
    maze = maze.reset_index(drop=True)
    # Set entrance and exit
    maze = set_walls(0,
            np.array([True, True, True, False]), maze)
    maze = set_walls((HEIGHT*WIDTH)-1,
            np.array([True, True, False, True]), maze)
    return maze


def set_walls(c, walls, maze):
    """Set wall status of a cell"""
    maze.iloc[c][["left", "up", "right", "down"]] *= walls
    return maze


def set_visited(c, maze):
    """For a certain x and y set visited to True"""
    maze.iloc[c].visited = True
    return maze


def unvisited_left(maze):
    """Count unvisited cells in the maze"""
    if maze.visited.sum() < maze.shape[0]:
        return True
    else:
        return False


def find_unvisited_neighbours(maze, c):
    """
    For all possible neighbours of the current cell check if it has
    neighbours
    """
    x, y = maze.iloc[c][["x", "y"]]
    return maze[((maze.x == x-1) & (maze.y == y) & (maze.visited == False)) |
                ((maze.x == x+1) & (maze.y == y) & (maze.visited == False)) |
                ((maze.x == x) & (maze.y == y-1) & (maze.visited == False)) |
                ((maze.x == x) & (maze.y == y+1) & (maze.visited == False)) ]



def push_current_to_stack(c, stack, maze): 
    """Find current cell and append to stack"""
    stack = stack.append(
           maze.iloc[c])
    return stack


def remove_walls(current_index, new_index, maze):
    """Remove walls between neighbours"""
    xc, yc = maze.iloc[current_index][["x", "y"]]
    xn, yn = maze.iloc[new_index][["x", "y"]]
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
    maze = set_walls(current_index, current, maze)
    maze = set_walls(new_index, new, maze)
    return maze


def recursive(maze):
    """Perform recursive backtracker algoirthm"""
    stack = pd.DataFrame(
                columns = [
                    "visited", "left", "up", "right", 
                    "down", "x", "y"])
    # start cell
    current_cell_index = 0
    total_list = []
    while unvisited_left(maze):
        gc.collect()
        maze = set_visited(current_cell_index, maze)
        # find neighbours
        neighbours = find_unvisited_neighbours(maze, current_cell_index)
        if neighbours.shape[0] > 0:
            # choose random new cell
            new_cell_index = neighbours.sample(1, axis=0).index.values[0]
            # push current cell to stack
            stack = push_current_to_stack(current_cell_index, stack, maze)
            # remove walls
            maze = remove_walls(current_cell_index, new_cell_index, maze)
            current_cell_index = new_cell_index
            total_list.append(current_cell_index)
        else:
            # Get item from stack
            stack, current_cell_index = (
                stack.drop(stack.tail(1).index), 
                stack.tail(1).index.values[0])


if __name__ == "__main__":
    # maze with all walls 
    maze = initiate_maze()
    recursive(maze)
    maze.to_csv("maze.csv")

    # plot maze
    p = PlotMaze(WIDTH, HEIGHT, maze)
    p.plot()
