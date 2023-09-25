import numpy as np
from PIL import Image

from aberration_detection.Dot_array import EO_DOT_ARRAY, get_dot_array_image, locate_dots, plot_located_dots
from NTNU_specific.components import HAMAMATSU

def simulate_dots_and_locate():
    dot_radius = EO_DOT_ARRAY.diameter / 2 # m
    dot_spacing = EO_DOT_ARRAY.spacing # m
    pixel_number = 512
    nr_of_dots = 4

    dot_array_image, dot_blobs, pixel_size = get_dot_array_image(dot_radius=dot_radius, 
                                                         dot_spacing=dot_spacing, 
                                                         pixel_number=pixel_number,
                                                         nr_of_dots=nr_of_dots
                                                         )
    
    blobs_LoG, blobs_DoG = locate_dots(dot_array_image, dot_radius, pixel_size)

    plot_located_dots(dot_array_image, [blobs_LoG, blobs_DoG, dot_blobs])

def locate_and_plot_dots():
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ20230915_dotarray_2x_inf\0_10-16_16.tiff"

    image = np.array(Image.open(filepath))


    dot_radius = EO_DOT_ARRAY.diameter/2
    pixel_size = HAMAMATSU.camera_pixel_size

    blobs_LoG, blobs_DoG = locate_dots(image, dot_radius, pixel_size)

    plot_located_dots(image, [blobs_LoG, blobs_DoG])


if __name__ == "__main__":
    simulate_dots_and_locate()
    locate_and_plot_dots()