import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from pyFPM.aberrations.dot_array.Dot_array import (EO_DOT_ARRAY, 
                                                   get_dot_array_image)
from pyFPM.aberrations.dot_array.plot_dot_array import (plot_located_dots,
                                                        plot_located_dots_vs_grid,
                                                        plot_located_dot_error)
from pyFPM.aberrations.dot_array.locate_dot_array import (locate_dots,
                                                          assemble_dots_in_grid)                                           
from pyFPM.NTNU_specific.components import (HAMAMATSU_C11440_42U30, 
                                            INFINITYCORRECTED_2X)

def simulate_dots():
    dot_radius = EO_DOT_ARRAY.diameter / 2 # m
    dot_spacing = EO_DOT_ARRAY.spacing # m
    image_size = HAMAMATSU_C11440_42U30.raw_image_size
    pixel_size = HAMAMATSU_C11440_42U30.camera_pixel_size

    magnification = INFINITYCORRECTED_2X.magnification
    object_pixel_size = pixel_size / magnification

    dot_array_image, known_blobs = get_dot_array_image(dot_radius=dot_radius, 
                                                         dot_spacing=dot_spacing, 
                                                         image_size=image_size, 
                                                         object_pixel_size=object_pixel_size
                                                         )
    
    plt.matshow(dot_array_image)
    plt.show()

def locate_and_plot_dots():
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ20230915_dotarray_2x_inf\0_10-16_16.tiff"

    image = np.array(Image.open(filepath))#[750:1200, 750:1200]

    dot_radius = EO_DOT_ARRAY.diameter/2
    dot_spacing = EO_DOT_ARRAY.spacing
    pixel_size = HAMAMATSU_C11440_42U30.camera_pixel_size
    magnification = INFINITYCORRECTED_2X.magnification

    object_pixel_size = pixel_size / magnification

    filtered_blobs, blobs_LoG, blobs_DoG = locate_dots(image, dot_radius, object_pixel_size)

    plot_located_dots(image, [filtered_blobs, blobs_LoG, blobs_DoG])
    blobs, grid_points, grid_indices, rotation = assemble_dots_in_grid(image.shape, filtered_blobs, dot_spacing, object_pixel_size)
    print(f"The total rotation was {rotation} degrees")
    plot_located_dots_vs_grid(image, blobs, grid_points)
    plot_located_dot_error(blobs, grid_points, grid_indices, object_pixel_size)
    plt.show()


if __name__ == "__main__":
    simulate_dots()
    #locate_and_plot_dots()
