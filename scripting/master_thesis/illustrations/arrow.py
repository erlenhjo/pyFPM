import matplotlib.pyplot as plt
import matplotlib.patches
import numpy as np
from typing import List
from dataclasses import dataclass

def test():
    fig, axes = plt.subplots(2)
    axes: List[plt.Axes] = axes
    # Show the full measurement for comparison on axis 0
    testdata_x = np.arange(1000)
    testdata_y = np.random.normal(0,1,1000)* 1

    axes[0].plot(testdata_x, testdata_y)
    # Place a little rectangle to mark the area of the enlargement
    axes[0].add_patch(matplotlib.patches.Rectangle((200., -3.), 50., 6., transform=axes[0].transData, alpha=0.3, color="g"))
    # Enlarged measurement on axis 1
    axes[1].plot(testdata_x[200:250], testdata_y[200:250])
    axes[0].set_xlim() # needed for some reason?
    axes[0].set_ylim()
    axes[1].set_xlim()
    axes[1].set_ylim()

    arrow_style = Arrow_style(
        face_color = "g",
        edge_color = "k",
        connection_style = "arc3, rad=-0.2",
        arrow_style = "simple",
        alpha = 0.5,
        mutation_scale = 40
    )

    arrow_text = Arrow_text(
        text="Region",
        relative_x = 00,
        relative_y = 0,
        font_size = "large" 
    )

    add_arrow(fig, axes[0], axes[1], 
              coord_from=(225,-2), coord_to=(225,1), 
              arrow_style=arrow_style,
              arrow_text=arrow_text)

    plt.show()

@dataclass
class Arrow_style:
    face_color: str
    edge_color: str
    connection_style: str
    arrow_style: str
    alpha: float
    mutation_scale: float

@dataclass
class Arrow_text:
    text: str
    relative_x: float
    relative_y: float
    font_size: str

# takes in figure and two axes (could be same?), internal coordinates for the start and end of the arrow
# within the two axes and creates an arrow according to arrow_values between the desired points
# needs ylim, xlim to be updated?
def add_arrow(fig: plt.Figure, ax_from: plt.Axes, ax_to: plt.Axes, coord_from, coord_to, 
              arrow_style: Arrow_style, arrow_text: Arrow_text|None, 
              axes_coordinates = False):
    
    if axes_coordinates:
        data_transform_from = ax_from.transAxes
        data_transform_to = ax_to.transAxes
    else: # data coordinates
        data_transform_from = ax_from.transData
        data_transform_to = ax_to.transData
    
    
    figure_transform = fig.transFigure.inverted()

    # add arrow
    point_from = figure_transform.transform(data_transform_from.transform(coord_from))
    point_to = figure_transform.transform(data_transform_to.transform(coord_to))

    arrow = matplotlib.patches.FancyArrowPatch(
        point_from, 
        point_to,
        transform = fig.transFigure,
        fc = arrow_style.face_color,
        ec = arrow_style.edge_color,
        connectionstyle = arrow_style.connection_style, 
        arrowstyle = arrow_style.arrow_style, 
        alpha = arrow_style.alpha,
        mutation_scale = arrow_style.mutation_scale
    )
    fig.add_artist(arrow)

    if arrow_text is not None:
        #add arrow text
        text_xy = (np.array(point_from)+np.array(point_to))/2 + np.array([arrow_text.relative_x, arrow_text.relative_y])
        text = plt.Text(
            text=arrow_text.text,
            x=text_xy[0],
            y=text_xy[1],
            transform = fig.transFigure,
            verticalalignment = "center",
            horizontalalignment = "center",
            fontsize = arrow_text.font_size,
            zorder = 10
        )
        fig.add_artist(text)


if __name__=="__main__":
    test()