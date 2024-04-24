import numpy as np
from scipy.signal import convolve2d, fftconvolve
from scipy.ndimage import convolve
from dataclasses import dataclass
from numba import njit

@dataclass
class Dot_array(object):
    spacing: float
    spacing_tolerance: float
    diameter: float
    diameter_tolerance: float
     

def get_dot_array_image(dot_radius, dot_spacing, image_size, object_pixel_size, rotation=0):
    # create a mask corresponding to a single dot
    single_dot_mask = create_single_dot_mask(dot_radius, object_pixel_size)
    # place "delta functions" at desired positions
    dot_centers, dot_blobs = determine_dot_centers(dot_radius, dot_spacing, object_pixel_size, image_size, rotation)
    # create complete image with correct Center of Mass through convolution
    dot_image = fftconvolve(dot_centers, single_dot_mask, mode="same")
    # invert as the dot array is an absorbtion target
    dot_image = 1-dot_image 

    return dot_image, dot_blobs       

def determine_dot_centers(dot_radius, dot_spacing, object_pixel_size, image_size, rotation):
    image_size_x = image_size[0]
    image_size_y = image_size[1]

    area_size_x = image_size_x * object_pixel_size
    area_size_y = image_size_y * object_pixel_size
    nr_of_dots_x = int(area_size_x // dot_spacing)
    nr_of_dots_y = int(area_size_y // dot_spacing)
    dot_buffer_x = area_size_x % dot_spacing / 2
    dot_buffer_y = area_size_y % dot_spacing / 2
    rotation = np.pi/180 * rotation
    rotation_center_x = (nr_of_dots_x/2 * dot_spacing + dot_buffer_x)/ object_pixel_size - 1
    rotation_center_y = (nr_of_dots_y/2 * dot_spacing + dot_buffer_y) / object_pixel_size - 1

    dot_centers = np.zeros(shape = (image_size_y, image_size_x))
    dot_blobs = []

    for y_dot in range(nr_of_dots_y):
        for x_dot in range(nr_of_dots_x):
            # center of dot in fractional pixels
            ideal_dot_center_x = ((x_dot + 1/2) * dot_spacing + dot_buffer_x) / object_pixel_size - 1
            ideal_dot_center_y = ((y_dot + 1/2) * dot_spacing + dot_buffer_y) / object_pixel_size - 1

            relative_x = ideal_dot_center_x - rotation_center_x
            relative_y = ideal_dot_center_y - rotation_center_y
            dot_center_x = relative_x * np.cos(rotation) - relative_y * np.sin(rotation) + rotation_center_x
            dot_center_y = relative_x * np.sin(rotation) + relative_y * np.cos(rotation) + rotation_center_y
            
            # assign a total value of 1 distributed between the four nearest pixels
            x_minus = np.floor(dot_center_x).astype(int)
            x_plus = x_minus + 1
            y_minus = np.floor(dot_center_y).astype(int)
            y_plus = y_minus + 1
            # use the lever principle
            x_minus_fraction = x_plus - dot_center_x
            x_plus_fraction = dot_center_x - x_minus
            y_minus_fraction = y_plus - dot_center_y
            y_plus_fraction = dot_center_y - y_minus
            # assign values
            dot_centers[x_minus, y_minus] = x_minus_fraction * y_minus_fraction
            dot_centers[x_minus, y_plus] = x_minus_fraction * y_plus_fraction
            dot_centers[x_plus, y_minus] = x_plus_fraction * y_minus_fraction
            dot_centers[x_plus, y_plus] = x_plus_fraction * y_plus_fraction

            dot_blobs.append([dot_center_x, dot_center_y, dot_radius/object_pixel_size])

    return dot_centers, np.array(dot_blobs)

def create_single_dot_mask(dot_radius, object_pixel_size):
    positions = np.arange(2 * dot_radius//object_pixel_size + 2)
    center = positions[len(positions)//2]
    X, Y = np.meshgrid(positions, positions)
    single_dot = (X-center)**2 + (Y-center)**2 < (dot_radius/object_pixel_size)**2
    return single_dot



