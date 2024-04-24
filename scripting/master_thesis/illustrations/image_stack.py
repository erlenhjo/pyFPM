from mpl_toolkits.mplot3d import proj3d
import numpy as np

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def main():
    fig, ax = plt.subplots()

    x = np.linspace(-3.14, 3.14, 100)
    X, Y = np.meshgrid(x, x)

    images = [
        np.sin(1*X),
        np.sin(2*X),
        np.sin(3*X),
        np.sin(4*X),
        np.sin(5*X),
    ]
    
    border_colors = ["red", "orange", "yellow", "green", "blue"]

    images_reverse = images.copy()
    images_reverse.reverse()

    N = len(images)
    for n, (image, border_color) in enumerate(zip(images_reverse, border_colors)):
        x0 = 0.07*(N-n-1)
        y0 = 0.07*(N-n-1)
        width = 0.7
        height = 0.7
        axin = ax.inset_axes(bounds=[x0, y0, width, height])    # create new inset axes in data coordinates
        axin.imshow(image)
        axin.spines['bottom'].set_color(border_color)
        axin.spines['bottom'].set_linewidth(4)
        axin.spines['top'].set_color(border_color) 
        axin.spines['top'].set_linewidth(4) 
        axin.spines['right'].set_color(border_color)
        axin.spines['right'].set_linewidth(4)
        axin.spines['left'].set_color(border_color)
        axin.spines['left'].set_linewidth(4)
        axin.set_xticks([])
        axin.set_yticks([])

    plt.show()








if __name__ == "__main__":
    main()
