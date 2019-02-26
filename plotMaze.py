import numpy as np
import matplotlib.pyplot as plt
import itertools


class PlotMaze():

    def __init__(self, width, height, maze):
        """Plot the maze"""
        
        self.width = width
        self.height = height
        self.maze = maze

        # Split canvas in tiles
        canvas_width, canvas_height = self.width*10, self.height*10
        self.x_coords = np.linspace(0, canvas_width, self.width + 1) 
        self.y_coords = np.linspace(0, canvas_height, self.height + 1)


    def plot(self):
        """Perform actual plotting"""

        # create figure
        fig, ax = plt.subplots(1, 1)

        self.draw_walls(ax)
        self.layout_maze(ax)

        plt.show()

    def draw_walls(self, ax):
        """draw wals of the maze"""

        # loop over all cells
        for i, row in self.maze.iterrows():
            if row.left:
                ax.vlines(self.x_coords[row.x], 
                            self.y_coords[row.y], 
                            self.y_coords[row.y+1])
            if row.up:
                ax.hlines(self.y_coords[row.y+1], 
                            self.x_coords[row.x],
                            self.x_coords[row.x+1])
            if row.right:
                ax.vlines(self.x_coords[row.x+1], 
                            self.y_coords[row.y], 
                            self.y_coords[row.y+1])
            if row.down:
                ax.hlines(self.y_coords[row.y], 
                            self.x_coords[row.x], 
                            self.x_coords[row.x+1])


    def layout_maze(self, ax):
        """layout the maze plot"""

        ax.set_aspect("equal")
        plt.axis("off")
