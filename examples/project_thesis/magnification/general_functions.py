import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from pyFPM.aberrations.dot_array.plot_dot_array import (plot_example_dots, plot_dot_error, plot_dot_error_scatter)
from pyFPM.aberrations.dot_array.locate_dot_array import (locate_dots,
                                                          assemble_dots_in_grid)                                          
from pyFPM.NTNU_specific.components import EO_DOT_ARRAY, HAMAMATSU_C11440_42U30



def locate_and_plot_dots(lens, filepath, subprecision):
    
    image = np.array(Image.open(filepath))

    dot_array = EO_DOT_ARRAY
    camera = HAMAMATSU_C11440_42U30

    fig_0, axes_0 = plt.subplots(nrows=1, ncols=1, figsize=(2.5,2.5), constrained_layout = True)
    axes_0.matshow(image)
    axes_0.set_axis_off()

    fig_1, axes_1 = plt.subplots(nrows=1, ncols=1, figsize=(3,2.5), constrained_layout = True)
    
    object_pixel_size = camera.camera_pixel_size / lens.magnification
    
    located_blobs = locate_dots(image, dot_array, object_pixel_size, sub_precision=subprecision)
    blobs, grid_points, grid_indices, rotation, center_indices = assemble_dots_in_grid(image, located_blobs, dot_array, object_pixel_size)
    print(f"The total rotation was {rotation} degrees")       
    plot_dot_error(ax=axes_1, blobs=blobs, grid_points=grid_points, 
                    grid_indices=grid_indices, object_pixel_size=object_pixel_size)

    fig_2 = plt.figure()
    plot_example_dots(fig_2, image, blobs, grid_points, grid_indices, dot_array, object_pixel_size)

    fig_3, axes_3 = plt.subplots(nrows=1, ncols=1, figsize=(3,3), constrained_layout = True)
    plot_dot_error_scatter(ax=axes_3, blobs=blobs, grid_points=grid_points, 
                            grid_indices=grid_indices, object_pixel_size=object_pixel_size,
                            center_indices=center_indices)
    
    return fig_0, fig_1, fig_2, fig_3
    

def locate_and_scatter_plot(lens, filepath, subprecision):
    image = np.array(Image.open(filepath))

    dot_array = EO_DOT_ARRAY
    camera = HAMAMATSU_C11440_42U30
    
    object_pixel_size = camera.camera_pixel_size / lens.magnification
    
    located_blobs = locate_dots(image, dot_array, object_pixel_size, sub_precision=subprecision)
    blobs, grid_points, grid_indices, rotation, center_indices = assemble_dots_in_grid(image, located_blobs, dot_array, object_pixel_size)

    fig_3, axes_3 = plt.subplots(nrows=1, ncols=1, figsize=(3,3), constrained_layout = True)
    plot_dot_error_scatter(ax=axes_3, blobs=blobs, grid_points=grid_points, 
                            grid_indices=grid_indices, object_pixel_size=object_pixel_size,
                            center_indices=center_indices)
    fig_3.suptitle(filepath.split("_")[-1])