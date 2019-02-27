import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import itertools
import plotly.graph_objs as go
from plotly.offline import plot


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
        # length and hight of a square
        self.d_h = self.x_coords[1] - self.x_coords[0]
        self.d_v = self.y_coords[1] - self.y_coords[0]

    def plot(self):
        """Plot maze using plotly"""
        # Data trace, invisible but needed, also disable hover
        trace0 = go.Scatter(
                x=[0, self.width*10],
                y=[0, self.height*10],
                opacity = 0,
                showlegend = False,
                hoverinfo = "none")
        # Layout, hide axis, fix aspect ration and add walls
        layout = {"shapes" : self.draw_walls(),
                  "yaxis" : {
                      "scaleanchor" : "x",
                      "scaleratio" : 1,
                      "showgrid" : False,
                      "zeroline" : False,
                      "showline" : False,
                      "ticks" : "",
                      "showticklabels" : False},
                  "xaxis" : {
                      "showgrid" : False,
                      "zeroline" : False,
                      "showline" : False,
                      "ticks" : "",
                      "showticklabels" : False}
                  }
        # create figure
        fig = {
                "data" : [trace0],
                "layout" : layout
                }
        # plot figure
        plot(fig)

    def draw_walls(self):
        """plot walls of the maze"""
        shape_list = []
        # Loop over rows in maze dataframe
        # Build walls as indicated
        for i, row in self.maze.iterrows():
            if row.left:
                shape_list.append({
                    'type': 'line',
                    'x0': self.x_coords[row.x],
                    'y0': self.y_coords[row.y],
                    'x1': self.x_coords[row.x],
                    'y1': self.y_coords[row.y] + self.d_v,
                    'line': {
                        'color': 'rgb(0, 0, 0)',
                        'width': 2,
                        },
                    })
            if row.up:
                shape_list.append({
                    'type': 'line',
                    'x0': self.x_coords[row.x],
                    'y0': self.y_coords[row.y+1],
                    'x1': self.x_coords[row.x] + self.d_h,
                    'y1': self.y_coords[row.y+1],
                    'line': {
                        'color': 'rgb(0, 0, 0)',
                        'width': 2,
                        },
                    })
            if row.right:
                shape_list.append({
                    'type': 'line',
                    'x0': self.x_coords[row.x+1],
                    'y0': self.y_coords[row.y],
                    'x1': self.x_coords[row.x+1],
                    'y1': self.y_coords[row.y] + self.d_v,
                    'line': {
                        'color': 'rgb(0, 0, 0)',
                        'width': 2,
                        },
                    })
            if row.down:
                shape_list.append({
                    'type': 'line',
                    'x0': self.x_coords[row.x],
                    'y0': self.y_coords[row.y],
                    'x1': self.x_coords[row.x] + self.d_h,
                    'y1': self.y_coords[row.y],
                    'line': {
                        'color': 'rgb(0, 0, 0)',
                        'width': 2,
                        },
                    })
        return shape_list

if __name__ == "__main__":
    maze = pd.read_csv("maze.csv")
    p = PlotMaze(maze.x.max()+1, maze.y.max()+1, maze)
    p.plot()
