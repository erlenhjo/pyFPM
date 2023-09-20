import numpy as np

def dot_array(dot_radius, dot_spacing, pixel_number, nr_of_dots):

    dot_image = np.zeros(shape = (pixel_number, pixel_number))

    image_size = nr_of_dots * dot_spacing
    pixel_size = image_size / pixel_number

    positions = np.arange(pixel_number)*pixel_size + pixel_size/2

    X, Y = np.meshgrid(positions, positions)

    for y_dot in range(nr_of_dots):
        for x_dot in range(nr_of_dots):
            dot_center_x = (1/2 + x_dot) * dot_spacing
            dot_center_y = (1/2 + y_dot) * dot_spacing

            dot_image += (X-dot_center_x)**2 + (Y - dot_center_y)**2 < dot_radius**2

                
    return dot_image
