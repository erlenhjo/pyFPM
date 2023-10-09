import numpy as np

from pyFPM.setup.Setup_parameters import Setup_parameters

class Imaging_system(object):
    def __init__(self, setup_parameters: Setup_parameters, pixel_scale_factor,
                  patch_start, patch_size):
        
        spatial_frequency = 1 / setup_parameters.LED_info.wavelength
        spatial_cutoff_frequency = calculate_spatial_cutoff_frequency(spatial_frequency, setup_parameters.lens.NA)

        raw_image_pixel_size = setup_parameters.camera.camera_pixel_size / setup_parameters.lens.magnification
        final_image_pixel_size = raw_image_pixel_size / pixel_scale_factor
        final_image_size = [pixel_scale_factor * size for size in patch_size]

        
        if final_image_pixel_size > calculate_required_pixel_size(spatial_cutoff_frequency = spatial_cutoff_frequency):
            raise "Too low pixel scale factor"

        # calculate offsets
        x_offset, y_offset = calculate_offset(
            LED_offset = setup_parameters.LED_info.LED_offset,
            image_size = setup_parameters.camera.raw_image_size,
            patch_start = patch_start,
            patch_size = patch_size,
            raw_image_pixel_size = raw_image_pixel_size
        )

        # calculate LED positions
        x_locations, y_locations = calculate_LED_locations(
            LED_array_size = setup_parameters.LED_info.LED_array_size,
            center_indices = setup_parameters.LED_info.center_indices,
            LED_pitch = setup_parameters.LED_info.LED_pitch,
            x_offset = x_offset,
            y_offset = y_offset
        )
        
        # calculate frequency components for thin or thick sample/glass slide
        if setup_parameters.slide is None:
            spatial_LED_frequencies_x, spatial_LED_frequencies_y = calculate_spatial_LED_frequency_components_thin_sample(
                x_locations = x_locations, 
                y_locations = y_locations, 
                z_LED = setup_parameters.LED_info.array_to_object_distance, 
                spatial_frequency = spatial_frequency
            )
        else:
            spatial_LED_frequencies_x, spatial_LED_frequencies_y = calculate_spatial_LED_frequency_components_thick_sample(
                x_locations = x_locations, 
                y_locations = y_locations, 
                z_LED = setup_parameters.LED_info.array_to_object_distance,
                spatial_frequency = spatial_frequency,
                slide = setup_parameters.slide
            )
 
        low_res_CTF = calculate_coherent_transfer_function(
            pixel_size = raw_image_pixel_size,
            image_region_size = patch_size, 
            spatial_cutoff_frequency = spatial_cutoff_frequency
        )

        high_res_CTF = calculate_coherent_transfer_function(
            pixel_size = final_image_pixel_size,
            image_region_size = final_image_size, 
            spatial_cutoff_frequency = spatial_cutoff_frequency
        )

        # assign public variables
        self.frequency = spatial_frequency
        self.cutoff_frequency = spatial_cutoff_frequency
        self.LED_frequencies_x = spatial_LED_frequencies_x
        self.LED_frequencies_y = spatial_LED_frequencies_y

        self.patch_start = patch_start
        self.patch_size = patch_size
        self.final_image_size = final_image_size
        self.raw_image_pixel_size = raw_image_pixel_size
        self.final_image_pixel_size = final_image_pixel_size
        self.pixel_scale_factor = pixel_scale_factor
        
        self.low_res_CTF = low_res_CTF
        self.high_res_CTF = high_res_CTF

    def wavevectors_x(self):
        return 2*np.pi*self.LED_frequencies_x
    def wavevectors_y(self):
        return 2*np.pi*self.LED_frequencies_y
    def differential_wavevectors_x(self):
        return 2*np.pi / (self.final_image_pixel_size * self.final_image_size[0])
    def differential_wavevectors_y(self):
        return 2*np.pi / (self.final_image_pixel_size * self.final_image_size[1])
    def get_pupil(self, defocus):
        pupil = calculate_pupil(
            defocus = defocus,
            pixel_size = self.raw_image_pixel_size,
            frequency = self.frequency,
            image_region_size = self.patch_size
        )
        return pupil


def calculate_spatial_cutoff_frequency(spatial_frequency, NA_sys):
    return spatial_frequency * NA_sys

def calculate_NA_sys(spatial_frequencies_x: np.ndarray, spatial_frequencies_y: np.ndarray, spatial_frequency, NA_lens):
    NA_illumination = max(np.abs(spatial_frequencies_x).max(),np.abs(spatial_frequencies_y).max()) / spatial_frequency   # is mean or max the most correct?
    return NA_lens + NA_illumination
    
def calculate_required_pixel_size(spatial_cutoff_frequency):
    return 1 / (2.1 * spatial_cutoff_frequency)    #technically should be 2 for Nyquist criterion, but 2.1 gives some leeway


def calculate_offset(LED_offset, image_size, patch_start, patch_size, raw_image_pixel_size):
    # misalignment of LEDs with respect to optical axis
    LED_offset_x = LED_offset[0]
    LED_offset_y = LED_offset[1]

    # find center of image and patch
    image_center_pixel_x = image_size[0] / 2
    image_center_pixel_y = image_size[1] / 2
    patch_center_pixel_x = patch_start[0] + patch_size[0]/2
    patch_center_pixel_y = patch_start[1] + patch_size[1]/2

    # calculate offset of selected patch with respect to image centre
    patch_offset_x = (image_center_pixel_x - patch_center_pixel_x) * raw_image_pixel_size
    patch_offset_y = (image_center_pixel_y - patch_center_pixel_y) * raw_image_pixel_size

    # total offset
    x_offset = LED_offset_x + patch_offset_x
    y_offset = LED_offset_y + patch_offset_y
    
    return x_offset, y_offset


def calculate_LED_locations(LED_array_size, center_indices, LED_pitch, x_offset, y_offset):
    # note [y, x] indexing due to how matrix indexing works (row, col) -> (y, x)
    # arraysize + 1 in case LED array is one indexed
    x_size = LED_array_size[0] + 1 
    y_size = LED_array_size[1] + 1

    x_locations = np.zeros(shape = (y_size , x_size))
    y_locations = np.zeros(shape = (y_size , x_size))

    # calculate locations relative center LED
    for x_index in range(x_size):
        for y_index in range(y_size):
            x_locations[y_index, x_index] = (x_index - center_indices[0]) * LED_pitch
            y_locations[y_index, x_index] = (y_index - center_indices[1]) * LED_pitch    

    # apply offset
    x_locations = x_locations + x_offset
    y_locations = y_locations + y_offset

    return x_locations, y_locations


def calculate_spatial_LED_frequency_components_thin_sample(x_locations, y_locations, z_LED, spatial_frequency):
    # find relative values
    freqs_x_relative = -x_locations / np.sqrt(x_locations**2 + y_locations**2 + z_LED**2)
    freqs_y_relative = -y_locations / np.sqrt(x_locations**2 + y_locations**2 + z_LED**2)

    # multiply by frequency magnitude
    spatial_frequencies_x = spatial_frequency * freqs_x_relative
    spatial_frequencies_y = spatial_frequency * freqs_y_relative

    return spatial_frequencies_x, spatial_frequencies_y


def calculate_spatial_LED_frequency_components_thick_sample(x_locations, y_locations, z_LED, f0, slide):
    raise "Thick sample compensation by Zheng not implemented yet."


def calculate_coherent_transfer_function(pixel_size, image_region_size, spatial_cutoff_frequency):
    max_frequency = 1 / (2 * pixel_size)
    spatial_frequencies_x = np.linspace(start = -max_frequency, stop = max_frequency, num = image_region_size[0], endpoint = False)   # is enpoint setting correct?
    spatial_frequencies_y = np.linspace(start = -max_frequency, stop = max_frequency, num = image_region_size[1], endpoint = False)

    fx_mesh, fy_mesh = np.meshgrid(spatial_frequencies_x, spatial_frequencies_y)
    
    coherent_transfer_function = (fx_mesh**2 + fy_mesh**2) < spatial_cutoff_frequency**2

    return coherent_transfer_function 

def calculate_pupil(defocus, pixel_size, frequency, image_region_size):
    max_frequency = 1 / (2 * pixel_size)
    spatial_frequencies_x = np.linspace(start = -max_frequency, stop = max_frequency, num = image_region_size[0], endpoint = False)   # is enpoint setting correct?
    spatial_frequencies_y = np.linspace(start = -max_frequency, stop = max_frequency, num = image_region_size[1], endpoint = False)

    fx_mesh, fy_mesh = np.meshgrid(spatial_frequencies_x, spatial_frequencies_y)
    fz_mesh = np.emath.sqrt(frequency**2 - fx_mesh**2 - fy_mesh**2)

    return np.exp(1j*2*np.pi*defocus*np.real(fz_mesh)) * np.exp(-(abs(defocus)*2*np.pi*abs(np.imag(fz_mesh))))

