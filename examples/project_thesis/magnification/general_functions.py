import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from pyFPM.aberrations.dot_array.plot_dot_array import (plot_example_dots, plot_dot_error)
from pyFPM.aberrations.dot_array.locate_dot_array import (locate_dots,
                                                          assemble_dots_in_grid)                                          
from pyFPM.NTNU_specific.components import EO_DOT_ARRAY, HAMAMATSU_C11440_42U30



def locate_and_plot_dots(lens, filepath, subprecision):
    
    image = np.array(Image.open(filepath))

    dot_array = EO_DOT_ARRAY
    camera = HAMAMATSU_C11440_42U30


    fig_1, axes_1 = plt.subplots(nrows=1,ncols=1)
    # axes[0].matshow(image)
    # axes[0].set_axis_off()
    
    object_pixel_size = camera.camera_pixel_size / lens.magnification
    
    located_blobs = locate_dots(image, dot_array, object_pixel_size, sub_precision=subprecision)
    blobs, grid_points, grid_indices, rotation = assemble_dots_in_grid(image, located_blobs, dot_array, object_pixel_size)
    print(f"The total rotation was {rotation} degrees")       
    plot_dot_error(ax=axes_1, blobs=blobs, grid_points=grid_points, 
                    grid_indices=grid_indices, object_pixel_size=object_pixel_size)

    fig_1.tight_layout()
    fig_2 = plt.figure()
    plot_example_dots(fig_2, image, blobs, grid_points, grid_indices, dot_array, object_pixel_size)

    