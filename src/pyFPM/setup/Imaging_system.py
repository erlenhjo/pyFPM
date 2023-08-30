import numpy as np

from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.components.slides import THIN_SLIDE

class Imaging_system(object):
    def __init__(self, setup_parameters: Setup_parameters, pixel_scale_factor,
                  patch_start, patch_size, rotation):
        
        spatial_frequency = 1 / setup_parameters.wavelength

        raw_image_pixel_size = setup_parameters.camera.ccd_pixel_size / setup_parameters.lens.magnification
        final_image_pixel_size = raw_image_pixel_size / pixel_scale_factor
        final_image_size = pixel_scale_factor * patch_size

        # calculate offsets
        x_offset, y_offset = calculate_offset(
            LED_offset = setup_parameters.LED_offset,
            image_size = setup_parameters.camera.raw_image_size,
            patch_start = patch_start,
            patch_size = patch_size,
            raw_image_pixel_size = raw_image_pixel_size
        )

        # calculate LED positions
        x_locations, y_locations = calculate_LED_locations(
            arraysize = setup_parameters.arraysize, 
            LED_pitch = setup_parameters.LED_pitch,
            x_offset = x_offset,
            y_offset = y_offset,
            rotation = rotation
        )
        
        # calculate frequency components for thin or thick sample/glass slide
        if setup_parameters.slide == THIN_SLIDE:
            spatial_frequencies_x, spatial_frequencies_y = calculate_LED_frequencies_thin(
                x_locations = x_locations, 
                y_locations = y_locations, 
                z_LED = setup_parameters.z_LED, 
                spatial_frequency = spatial_frequency

            )
        else:
            spatial_frequencies_x, spatial_frequencies_y = calculate_LED_frequencies_thick(
                x_locations = x_locations, 
                y_locations = y_locations, 
                z_LED = setup_parameters.z_LED,
                spatial_frequency = spatial_frequency,
                slide = setup_parameters.slide
            )
 
        low_res_CTF = calculate_coherent_transfer_function(

        )

        high_res_CTF = calculate_coherent_transfer_function(

        )

        # assign public variables
        self.setup = setup_parameters

        self.spatial_frequency = spatial_frequency
        self.spatial_frequencies_x = spatial_frequencies_x
        self.spatial_frequencies_y = spatial_frequencies_y

        self.patch_size = patch_size
        self.final_image_size = final_image_size
        self.raw_image_pixel_size = raw_image_pixel_size
        self.final_image_pixel_size = final_image_pixel_size
        








def calculate_offset(LED_offset, image_size, patch_start, patch_size, raw_image_pixel_size):
    # misalignment of LEDs with respect to optical axis
    LED_offset_x = LED_offset[0]
    LED_offset_y = LED_offset[1]

    # find center of image and patch
    image_center_pixel_x = image_size[0] / 2
    image_center_pixel_y = image_size[1] / 2
    patch_center_pixel_x = patch_start[0] + patch_size/2
    patch_center_pixel_y = patch_start[1] + patch_size/2

    # calculate offset of selected patch with respect to image centre
    patch_offset_x = (image_center_pixel_x - patch_center_pixel_x) * raw_image_pixel_size
    patch_offset_y = (image_center_pixel_y - patch_center_pixel_y) * raw_image_pixel_size

    # total offset
    x_offset = LED_offset_x + patch_offset_x
    y_offset = LED_offset_y + patch_offset_y
    
    return x_offset, y_offset


def calculate_LED_locations(arraysize, LED_pitch, x_offset, y_offset, rotation):
    # note [y, x] indexing due to how matrix indexing works (row, col) -> (y, x)

    x_locations = np.zeros(shape = (arraysize,arraysize))
    y_locations = np.zeros(shape = (arraysize,arraysize))

    # calculate locations relative center LED
    center_index = (arraysize-1)/2
    for x_index in range(arraysize):
        for y_index in range(arraysize):
            x_locations[y_index, x_index] = (x_index - center_index) * LED_pitch
            y_locations[y_index, x_index] = (center_index - y_index) * LED_pitch    
    
    if rotation != 0:
        raise "Rotation not implemented yet"

    # apply offset
    x_locations = x_locations + x_offset
    y_locations = y_locations + y_offset

    return x_locations, y_locations


def calculate_LED_frequencies_thin(x_locations, y_locations, z_LED, spatial_frequency):
    # find relative values
    freqs_x_relative = -x_locations / np.sqrt(x_locations**2 + y_locations**2 + z_LED**2)
    freqs_y_relative = -y_locations / np.sqrt(x_locations**2 + y_locations**2 + z_LED**2)

    # multiply by frequency magnitude
    spatial_frequencies_x = spatial_frequency * freqs_x_relative
    spatial_frequencies_y = spatial_frequency * freqs_y_relative

    return spatial_frequencies_x, spatial_frequencies_y


def calculate_LED_frequencies_thick(x_locations, y_locations, z_LED, f0, slide):
    raise "Thick sample compensation by Zheng not implemented yet."


def calculate_coherent_transfer_function(pixel_size, image_region_size):
    df_x
    df_y

    f_max