import numpy as np
from dataclasses import dataclass

@dataclass
class Dot_array(object):
    spacing: float
    spacing_tolerance: float
    diameter: float
    diameter_tolerance: float


EO_DOT_ARRAY = Dot_array(
    spacing = 125e-6,
    spacing_tolerance = 2e-6,
    diameter = 62.5e-6,
    diameter_tolerance = 2e-6  
)


def get_dot_array_image(dot_radius, dot_spacing, pixel_number, nr_of_dots):

    dot_image = np.zeros(shape = (pixel_number, pixel_number))
    dot_blobs = []

    image_size = nr_of_dots * dot_spacing
    pixel_size = image_size / pixel_number

    positions = np.arange(pixel_number)*pixel_size

    X, Y = np.meshgrid(positions, positions)

    for y_dot in range(nr_of_dots):
        for x_dot in range(nr_of_dots):
            dot_center_x = (1/2 + x_dot) * dot_spacing
            dot_center_y = (1/2 + y_dot) * dot_spacing

            dot_image += (X-dot_center_x)**2 + (Y - dot_center_y)**2 < dot_radius**2
            dot_blobs.append([dot_center_x/pixel_size, dot_center_y/pixel_size, dot_radius/pixel_size])
                
    dot_image = 1-dot_image # invert as the dot array is an absorbtion target

    return dot_image, dot_blobs, pixel_size       
     


    
