import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

from pyFPM.aberrations.dot_array.plot_dot_array import (plot_example_dots, plot_dot_error)
from pyFPM.aberrations.dot_array.locate_dot_array import (locate_dots,
                                                          assemble_dots_in_grid)                                          
from pyFPM.NTNU_specific.components import EO_DOT_ARRAY, HAMAMATSU_C11440_42U30, INFINITYCORRECTED_2X, TELECENTRIC_3X



def locate_and_plot_dots():
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification_per_defocus_telecentric"
    outputdirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\generated_plots\magnification"
    for filename in os.listdir(datadirpath):
        filepath = os.path.join(datadirpath,filename)
        fig_1, fig_2 = locate_and_plot(filepath)
    plt.show()



def locate_and_plot(filepath):
    image = np.array(Image.open(filepath))#[1300:,1300:]

    dot_array = EO_DOT_ARRAY
    camera = HAMAMATSU_C11440_42U30
    lens = TELECENTRIC_3X
    #lens = INFINITYCORRECTED_2X

    fig_1, axes = plt.subplots(nrows=1,ncols=2)
    axes[0].matshow(image)
    axes[0].set_axis_off()
    
    object_pixel_size = camera.camera_pixel_size / lens.magnification
    
    located_blobs = locate_dots(image, dot_array, object_pixel_size, sub_precision=8)
    blobs, grid_points, grid_indices, rotation = assemble_dots_in_grid(image, located_blobs, dot_array, object_pixel_size)
    print(f"The total rotation was {rotation} degrees")       
    plot_dot_error(ax=axes[1], blobs=blobs, grid_points=grid_points, 
                    grid_indices=grid_indices, object_pixel_size=object_pixel_size)

    fig_1.tight_layout()

    fig_2 = plt.figure()
    plot_example_dots(fig_2, image, blobs, grid_points, grid_indices, dot_array, object_pixel_size)

    return fig_1, fig_2



def main():
    locate_and_plot_dots()

if __name__ == "__main__":
    main()
