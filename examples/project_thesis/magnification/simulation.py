import numpy as np
import matplotlib.pyplot as plt

from pyFPM.aberrations.dot_array.plot_dot_array import (plot_dot_error,
                                                        plot_example_dots,
                                                        plot_located_dots,
                                                        plot_located_dots_vs_grid,
                                                        plot_dot_error_scatter)
from pyFPM.aberrations.dot_array.locate_dot_array import (locate_dots,
                                                          assemble_dots_in_grid)                                        
from pyFPM.NTNU_specific.components import (HAMAMATSU_C11440_42U30,
                                            EO_DOT_ARRAY)
from pyFPM.aberrations.dot_array.simulate_dot_array import simulate_dot_array


def simulate_blob_detection_small():
    dot_array = EO_DOT_ARRAY
    image_size = [512, 512]
    pixel_size = HAMAMATSU_C11440_42U30.camera_pixel_size
    magnification = 2

    subprecision = 8

    image, _ = simulate_dot_array(dot_array= dot_array, image_size=image_size, 
                                pixel_size=pixel_size, magnification=magnification,
                                rotation = 2)    
    
    object_pixel_size = pixel_size / magnification
    
    fig_0, axes_0 = plt.subplots(nrows=1, ncols=1, figsize=(5,5), constrained_layout=True)
    axes_0.matshow(image)
    axes_0.set_axis_off()

    located_blobs = locate_dots(image, dot_array, object_pixel_size, sub_precision=subprecision)

    fig_2, axes_2 = plt.subplots(nrows=1, ncols=1, figsize=(3,2.5), constrained_layout=True)
    blobs, grid_points, grid_indices, rotation, center_indices = assemble_dots_in_grid(image, located_blobs, dot_array, object_pixel_size)
    print(f"The total rotation was {rotation} degrees")       
    plot_dot_error(ax=axes_2, blobs=blobs, grid_points=grid_points, 
                    grid_indices=grid_indices, object_pixel_size=object_pixel_size)

    fig_1 = plot_located_dots_vs_grid(image=image, detected_blobs=blobs, grid_points=grid_points)
    
    fig_3 = plt.figure(figsize=(5,5), constrained_layout = True)
    plot_example_dots(fig_3, image, blobs, grid_points, grid_indices, dot_array, object_pixel_size)

    fig_4, axes_4 = plt.subplots(nrows=1, ncols=1, figsize=(3,3), constrained_layout = True)
    plot_dot_error_scatter(ax=axes_4, blobs=blobs, grid_points=grid_points, 
                            grid_indices=grid_indices, object_pixel_size=object_pixel_size,
                            center_indices=center_indices)



    # fig_0.savefig(r"C:\Users\erlen\Documents\GitHub\pyFPM\examples\project_thesis\results\blob_demo"+r"\blob_demo_overview.pdf", dpi=1000)
    # fig_2.savefig(r"C:\Users\erlen\Documents\GitHub\pyFPM\examples\project_thesis\results\blob_demo"+r"\blob_demo_error.pdf", dpi=1000)

def simulate_blob_detection():

    dot_array = EO_DOT_ARRAY
    image_size = HAMAMATSU_C11440_42U30.raw_image_size
    pixel_size = HAMAMATSU_C11440_42U30.camera_pixel_size
    magnification = 2

    subprecision = 8

    image, _ = simulate_dot_array(dot_array= dot_array, image_size=image_size, 
                                pixel_size=pixel_size, magnification=magnification*0.99, rotation=0.2)


    fig_0, axes_0 = plt.subplots(nrows=1,ncols=1)
    axes_0.matshow(image)
    axes_0.set_axis_off()
    

    fig_1, axes_1 = plt.subplots(nrows=1,ncols=1)
    object_pixel_size = pixel_size / magnification
    
    located_blobs = locate_dots(image, dot_array, object_pixel_size, sub_precision=subprecision)
    blobs, grid_points, grid_indices, rotation = assemble_dots_in_grid(image, located_blobs, dot_array, object_pixel_size)
    print(f"The total rotation was {rotation} degrees")       
    plot_dot_error(ax=axes_1, blobs=blobs, grid_points=grid_points, 
                    grid_indices=grid_indices, object_pixel_size=object_pixel_size)

    fig_0.tight_layout()
    fig_1.tight_layout()
    fig_2 = plt.figure(figsize=(5,5))
    plot_example_dots(fig_2, image, blobs, grid_points, grid_indices, dot_array, object_pixel_size)



if __name__ == "__main__":
    simulate_blob_detection_small()
    #simulate_blob_detection()
    plt.show()