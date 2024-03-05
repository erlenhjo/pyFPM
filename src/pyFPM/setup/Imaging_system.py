import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt #for debug

from pyFPM.setup.Setup_parameters import Setup_parameters, get_object_to_lens_distance

@dataclass
class LED_calibration_parameters:
    LED_distance: float
    LED_x_offset: float
    LED_y_offset: float
    LED_rotation: float


class Imaging_system(object):
    def __init__(self, setup_parameters: Setup_parameters, pixel_scale_factor,
                  patch_start, patch_size, LED_calibration_parameters):
        
        spatial_frequency = 1 / setup_parameters.LED_info.wavelength
        spatial_cutoff_frequency = calculate_spatial_cutoff_frequency(spatial_frequency, setup_parameters.lens.NA)

        raw_object_pixel_size = setup_parameters.camera.camera_pixel_size / setup_parameters.lens.magnification
        final_object_pixel_size = raw_object_pixel_size / pixel_scale_factor
        final_image_size = [pixel_scale_factor * size for size in patch_size]

        object_to_lens_distance = get_object_to_lens_distance(setup_parameters.lens)
        
        # calculate offsets
        patch_offset_x, patch_offset_y = calculate_patch_offset(
            image_size = setup_parameters.camera.raw_image_size,
            patch_start = patch_start,
            patch_size = patch_size,
            raw_object_pixel_size = raw_object_pixel_size
        )

        # calculate LED positions
        LED_locations_x, LED_locations_y = calculate_LED_locations(
            LED_array_size = setup_parameters.LED_info.LED_array_size,
            center_indices = setup_parameters.LED_info.center_indices,
            LED_pitch = setup_parameters.LED_info.LED_pitch,
            LED_rotation = LED_calibration_parameters.LED_rotation,
            LED_offset = np.array(setup_parameters.LED_info.LED_offset) \
                + np.array([LED_calibration_parameters.LED_x_offset,LED_calibration_parameters.LED_y_offset])
        )
        
        # calculate frequency components for normal frequency shift model
        LED_shifts_x, LED_shifts_y = calculate_LED_shifts_from_in_plane_frequency_components(
            LED_locations_x = LED_locations_x, 
            LED_locations_y = LED_locations_y,
            patch_offset_x = patch_offset_x,
            patch_offset_y = patch_offset_y,
            z_LED = LED_calibration_parameters.LED_distance, 
            spatial_frequency = spatial_frequency,
            pixel_size = final_object_pixel_size,
            image_size = final_image_size
        )
        # calculate frequency components for alternative frequency shift model (Fresnel propagation based?)
        LED_shifts_x_aperture, LED_shifts_y_aperture = calculate_LED_shifts_from_aperture_shift(
            LED_locations_x = LED_locations_x, 
            LED_locations_y = LED_locations_y,
            patch_offset_x = patch_offset_x,
            patch_offset_y = patch_offset_y,
            z_LED = LED_calibration_parameters.LED_distance,
            z_1 = object_to_lens_distance, 
            wavelength = setup_parameters.LED_info.wavelength,
            pixel_size = final_object_pixel_size,
            image_size = final_image_size
        )
 
        low_res_CTF = calculate_coherent_transfer_function(
            pixel_size = raw_object_pixel_size,
            image_region_size = patch_size, 
            spatial_cutoff_frequency = spatial_cutoff_frequency
        )
        high_res_CTF = calculate_coherent_transfer_function(
            pixel_size = final_object_pixel_size,
            image_region_size = final_image_size, 
            spatial_cutoff_frequency = spatial_cutoff_frequency
        )


        high_res_object_x_positions, high_res_object_y_positions = calculate_position_mesh_grids(pixel_size = final_object_pixel_size, 
                                                                                                 image_region_size = final_image_size,
                                                                                                 offset_x = patch_offset_x, 
                                                                                                 offset_y = patch_offset_y
                                                                                                 ) 
        high_res_Fresnel_object_phase_correction = calculate_object_plane_phase_shift(
                                                    x_mesh = high_res_object_x_positions, 
                                                    y_mesh = high_res_object_y_positions, 
                                                    wavevector = 2*np.pi*spatial_frequency, 
                                                    distance = object_to_lens_distance
                                                )
        high_res_spherical_illumination_object_phase_correction = calculate_object_plane_phase_shift(
                                                                    x_mesh = high_res_object_x_positions, 
                                                                    y_mesh = high_res_object_y_positions, 
                                                                    wavevector = 2*np.pi*spatial_frequency, 
                                                                    distance = LED_calibration_parameters.LED_distance
                                                                )
                    
        # assign public variables
        self.frequency = spatial_frequency
        self.cutoff_frequency = spatial_cutoff_frequency
        self.LED_shifts_x = LED_shifts_x
        self.LED_shifts_y = LED_shifts_y
        self.LED_shifts_x_aperture = LED_shifts_x_aperture
        self.LED_shifts_y_aperture = LED_shifts_y_aperture
        self.df_x = 1/(final_object_pixel_size * final_image_size[0])
        self.df_y = 1/(final_object_pixel_size * final_image_size[1])

        self.patch_start = patch_start
        self.patch_size = patch_size
        self.final_image_size = final_image_size
        self.raw_object_pixel_size = raw_object_pixel_size
        self.final_object_pixel_size = final_object_pixel_size
        self.pixel_scale_factor = pixel_scale_factor
        self.patch_offset_x = patch_offset_x
        self.patch_offset_y = patch_offset_y
        
        self.low_res_CTF = low_res_CTF
        self.high_res_CTF = high_res_CTF
        self.high_res_spherical_illumination_correction = high_res_spherical_illumination_object_phase_correction
        self.high_res_Fresnel_correction = high_res_Fresnel_object_phase_correction

        self.float_type = setup_parameters.camera.float_type
        if self.float_type == np.float32:
            self.complex_type = np.complex64
        else:
            self.complex_type = np.complex128 

def calculate_spatial_cutoff_frequency(spatial_frequency, NA_sys):
    return spatial_frequency * NA_sys

def calculate_NA_sys(spatial_frequencies_x: np.ndarray, spatial_frequencies_y: np.ndarray, spatial_frequency, NA_lens):
    NA_illumination = max(np.abs(spatial_frequencies_x).max(),np.abs(spatial_frequencies_y).max()) / spatial_frequency   # is mean or max the most correct?
    return NA_lens + NA_illumination
    
def calculate_required_pixel_size(spatial_cutoff_frequency):
    return 1 / (2.1 * spatial_cutoff_frequency)    #technically should be 2 for Nyquist criterion, but 2.1 gives some leeway


def calculate_patch_offset(image_size, patch_start, patch_size, raw_object_pixel_size):
    # find center of image and patch
    image_center_pixel_x = image_size[0] / 2
    image_center_pixel_y = image_size[1] / 2
    patch_center_pixel_x = patch_start[0] + patch_size[0]/2
    patch_center_pixel_y = patch_start[1] + patch_size[1]/2

    # calculate offset of selected patch with respect to image centre
    patch_offset_x = (patch_center_pixel_x - image_center_pixel_x) * raw_object_pixel_size
    patch_offset_y = (patch_center_pixel_y - image_center_pixel_y) * raw_object_pixel_size
    
    return patch_offset_x, patch_offset_y


def calculate_LED_locations(LED_array_size, center_indices, LED_pitch, LED_rotation, LED_offset):
    # note [y, x] indexing due to how matrix indexing works (row, col) -> (y, x)
    # arraysize + 1 in case LED array is one indexed
    x_size = LED_array_size[0] + 1 
    y_size = LED_array_size[1] + 1

    # misalignment of LEDs with respect to optical axis
    x_offset = LED_offset[0]
    y_offset = LED_offset[1]

    x_locations = np.zeros(shape = (y_size , x_size))
    y_locations = np.zeros(shape = (y_size , x_size))

    # calculate locations relative center LED
    rotation_radians = 3.14/180 * LED_rotation
    for x_index in range(x_size):
        for y_index in range(y_size):
            m = x_index - center_indices[0]
            n = y_index - center_indices[1]
            sin = np.sin(rotation_radians)
            cos = np.cos(rotation_radians)
            x_locations[y_index, x_index] = (cos*m + sin*n) * LED_pitch
            y_locations[y_index, x_index] = (-sin*m + cos*n) * LED_pitch 
    

    # apply offset
    x_locations = x_locations + x_offset
    y_locations = y_locations + y_offset

    return x_locations, y_locations


def calculate_LED_shifts_from_in_plane_frequency_components(LED_locations_x, LED_locations_y, 
                                                            patch_offset_x, patch_offset_y, 
                                                            z_LED, spatial_frequency,
                                                            pixel_size, image_size):
    df_x = 1/(pixel_size * image_size[0])
    df_y = 1/(pixel_size * image_size[1])
    
    # find x_locations relative patch center
    locations_x = LED_locations_x - patch_offset_x
    locations_y = LED_locations_y - patch_offset_y
    
    # find relative frequency values
    freqs_x_relative = locations_x / np.sqrt(locations_x**2 + locations_y**2 + z_LED**2)
    freqs_y_relative = locations_y / np.sqrt(locations_x**2 + locations_y**2 + z_LED**2)

    # multiply by frequency magnitude and divide by discreteization to get value in pixels
    pixel_shifts_x = spatial_frequency/df_x * freqs_x_relative
    pixel_shifts_y = spatial_frequency/df_y * freqs_y_relative

    return pixel_shifts_x, pixel_shifts_y


def calculate_LED_shifts_from_aperture_shift(LED_locations_x, LED_locations_y, 
                                                      patch_offset_x, patch_offset_y, 
                                                      z_LED, z_1, wavelength,
                                                      pixel_size, image_size):
    dx = wavelength*z_1/(pixel_size * image_size[0])
    dy = wavelength*z_1/(pixel_size * image_size[1])

    #calculate spatial shift
    spatial_shifts_x = (LED_locations_x-patch_offset_x)*z_1/z_LED - patch_offset_x
    spatial_shifts_y = (LED_locations_y-patch_offset_y)*z_1/z_LED - patch_offset_y

    #calculate pixel shift
    pixel_shifts_x = spatial_shifts_x/dx
    pixel_shifts_y = spatial_shifts_y/dy
    
    return pixel_shifts_x, pixel_shifts_y


def calculate_coherent_transfer_function(pixel_size, image_region_size, spatial_cutoff_frequency):
    fx_mesh, fy_mesh = calculate_frequency_mesh_grids(pixel_size=pixel_size, image_region_size=image_region_size)
    coherent_transfer_function = (fx_mesh**2 + fy_mesh**2) <= spatial_cutoff_frequency**2

    return coherent_transfer_function 

def calculate_frequency_mesh_grids(pixel_size, image_region_size):
    max_frequency = 1 / (2 * pixel_size)
    spatial_frequencies_x = np.linspace(start = -max_frequency, stop = max_frequency, num = image_region_size[0], endpoint = False)  
    spatial_frequencies_y = np.linspace(start = -max_frequency, stop = max_frequency, num = image_region_size[1], endpoint = False)

    fx_mesh, fy_mesh = np.meshgrid(spatial_frequencies_x, spatial_frequencies_y)

    return fx_mesh, fy_mesh

def calculate_position_mesh_grids(pixel_size, image_region_size, offset_x, offset_y):
    FOV_x = image_region_size[0] * pixel_size
    FOV_y = image_region_size[1] * pixel_size
    positions_x = np.linspace(start = -FOV_x/2, stop = FOV_x/2, num = image_region_size[0], endpoint = False)
    positions_y = np.linspace(start = -FOV_y/2, stop = FOV_y/2, num = image_region_size[1], endpoint = False)

    x_mesh, y_mesh = np.meshgrid(positions_x, positions_y)
    
    return x_mesh, y_mesh


def calculate_object_plane_phase_shift(x_mesh, y_mesh, wavevector, distance):
    return np.exp(1j * wavevector * 1/(2*distance) * (x_mesh**2 + y_mesh**2))
