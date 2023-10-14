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
     

def get_dot_array_image(dot_radius, dot_spacing, image_size, object_pixel_size):
    # create a mask corresponding to a single dot
    single_dot_mask = create_single_dot_mask(dot_radius, object_pixel_size)
    # place "delta functions" at desired positions
    dot_centers, dot_blobs = determine_dot_centers(dot_radius, dot_spacing, object_pixel_size, image_size)
    # create complete image with correct Center of Mass through convolution
    dot_image = fftconvolve(dot_centers, single_dot_mask, mode="same")
    # invert as the dot array is an absorbtion target
    dot_image = 1-dot_image 

    return dot_image, dot_blobs       

def determine_dot_centers(dot_radius, dot_spacing, object_pixel_size, image_size):
    image_size_x = image_size[0]
    image_size_y = image_size[1]

    area_size_x = image_size_x * object_pixel_size
    area_size_y = image_size_y * object_pixel_size
    nr_of_dots_x = int(area_size_x // dot_spacing)
    nr_of_dots_y = int(area_size_y // dot_spacing)
    dot_buffer_x = area_size_x % dot_spacing / 2
    dot_buffer_y = area_size_y % dot_spacing / 2

    dot_centers = np.zeros(shape = (image_size_y, image_size_x))
    dot_blobs = []

    for y_dot in range(nr_of_dots_y):
        for x_dot in range(nr_of_dots_x):
            # center of dot in fractional pixels
            dot_center_x = ((x_dot + 1/2) * dot_spacing + dot_buffer_x) / object_pixel_size - 1
            dot_center_y = ((y_dot + 1/2) * dot_spacing + dot_buffer_y) / object_pixel_size - 1
            
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

    return dot_centers, dot_blobs

def create_single_dot_mask(dot_radius, object_pixel_size):
    positions = np.arange(2 * dot_radius//object_pixel_size + 2)
    center = positions[len(positions)//2]
    X, Y = np.meshgrid(positions, positions)
    single_dot = (X-center)**2 + (Y-center)**2 < (dot_radius/object_pixel_size)**2
    return single_dot


from pyFPM.NTNU_specific.components import EO_DOT_ARRAY

def simulate_dot_array(image_size):
    pixel_size = 6.5e-6 
    magnification = 2
    dot_radius = EO_DOT_ARRAY.diameter / 2 # m
    dot_spacing = EO_DOT_ARRAY.spacing # m

    pixel_scale_factor = 2
    high_res_image_size = [size * pixel_scale_factor for size in image_size]
    high_res_pixel_size = pixel_size / pixel_scale_factor

    dot_array_image, _ = get_dot_array_image(
                            dot_radius=dot_radius, 
                            dot_spacing=dot_spacing, 
                            image_size=high_res_image_size,
                            object_pixel_size=high_res_pixel_size/magnification
                            )

    return dot_array_image


def main_test():
    image_size = [4096,4096]
    image = simulate_dot_array(image_size)


def profile_main_test():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main_test()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename=r"profiling_data\dot_array_image_generation_convolution.prof")

if __name__ == "__main__":
    profile_main_test()

