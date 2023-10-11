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


def get_dot_array_image(dot_radius, dot_spacing, image_size, object_pixel_size):

    dot_image = np.zeros(shape = (image_size[1], image_size[0]))
    dot_blobs = []

    area_size_x = image_size[0] * object_pixel_size
    area_size_y = image_size[1] * object_pixel_size
    positions_x = np.arange(image_size[0]) * object_pixel_size
    positions_y = np.arange(image_size[1]) * object_pixel_size

    X, Y = np.meshgrid(positions_x, positions_y)

    nr_of_dots_x = int(area_size_x // dot_spacing)
    nr_of_dots_y = int(area_size_y // dot_spacing)
    dot_buffer_x = area_size_x % dot_spacing / 2
    dot_buffer_y = area_size_y % dot_spacing / 2

    for y_dot in range(nr_of_dots_y):
        for x_dot in range(nr_of_dots_x):
            dot_center_x = (x_dot + 1/2) * dot_spacing + dot_buffer_x
            dot_center_y = (y_dot + 1/2) * dot_spacing + dot_buffer_y

            dot_image += (X-dot_center_x)**2 + (Y - dot_center_y)**2 < dot_radius**2
            dot_blobs.append([dot_center_x/object_pixel_size, dot_center_y/object_pixel_size, dot_radius/object_pixel_size])
                
    dot_image = 1-dot_image # invert as the dot array is an absorbtion target

    return dot_image, dot_blobs   
     


    
