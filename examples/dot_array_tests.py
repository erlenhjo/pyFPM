import numpy as np
from PIL import Image

from aberration_detection.Dot_array import EO_DOT_ARRAY, get_dot_array_image, \
                                           locate_dots, plot_located_dots, \
                                           assemble_dots_in_grid, plot_located_dots_vs_grid
from NTNU_specific.components import HAMAMATSU, INFINITYCORRECTED_2X

def simulate_dots_and_locate():
    dot_radius = EO_DOT_ARRAY.diameter / 2 # m
    dot_spacing = EO_DOT_ARRAY.spacing # m
    pixel_number = 512
    nr_of_dots = 4

    dot_array_image, known_blobs, pixel_size = get_dot_array_image(dot_radius=dot_radius, 
                                                         dot_spacing=dot_spacing, 
                                                         pixel_number=pixel_number,
                                                         nr_of_dots=nr_of_dots
                                                         )
    
    detected_blobs = locate_dots(dot_array_image, dot_radius, pixel_size)

    plot_located_dots(dot_array_image, [detected_blobs, known_blobs])

def locate_and_plot_dots():
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ20230915_dotarray_2x_inf\0_10-16_16.tiff"

    image = np.array(Image.open(filepath))[750:1200, 750:1200]

    dot_radius = EO_DOT_ARRAY.diameter/2
    dot_spacing = EO_DOT_ARRAY.spacing
    pixel_size = HAMAMATSU.camera_pixel_size
    magnification = INFINITYCORRECTED_2X.magnification

    imaged_dot_radius = dot_radius * magnification
    imaged_dot_spacing = dot_spacing * magnification

    detected_blobs = locate_dots(image, imaged_dot_radius, pixel_size)


    #plot_located_dots(image, [detected_blobs])
    blob_grid, grid = assemble_dots_in_grid(image.shape, detected_blobs, imaged_dot_spacing, pixel_size)
    plot_located_dots_vs_grid(image, detected_blobs, grid)



if __name__ == "__main__":
    #simulate_dots_and_locate()
    locate_and_plot_dots()
