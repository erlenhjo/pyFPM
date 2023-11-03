import numpy as np

from pyFPM.setup.Setup_parameters import Setup_parameters

class Imaging_system(object):
    def __init__(self, setup_parameters: Setup_parameters, pixel_scale_factor,
                  patch_start, patch_size):
        
        spatial_frequency = 1 / setup_parameters.LED_info.wavelength
        spatial_cutoff_frequency = calculate_spatial_cutoff_frequency(spatial_frequency, setup_parameters.lens.NA)

        raw_object_pixel_size = setup_parameters.camera.camera_pixel_size / setup_parameters.lens.magnification
        final_object_pixel_size = raw_object_pixel_size / pixel_scale_factor
        final_image_size = [pixel_scale_factor * size for size in patch_size]

        
        if final_object_pixel_size > calculate_required_pixel_size(spatial_cutoff_frequency = spatial_cutoff_frequency):
            raise "Too low pixel scale factor"

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
            LED_offset = setup_parameters.LED_info.LED_offset
        )
        
        # calculate frequency components for normal frequency shift model
        spatial_LED_frequencies_x, spatial_LED_frequencies_y = calculate_spatial_LED_frequency_components(
            LED_locations_x = LED_locations_x, 
            LED_locations_y = LED_locations_y,
            patch_offset_x = patch_offset_x,
            patch_offset_y = patch_offset_y,
            z_LED = setup_parameters.LED_info.array_to_object_distance, 
            spatial_frequency = spatial_frequency
        )
        # calculate frequency components for alternative frequency shift model (Fresnel propagation based?)
        spatial_LED_frequencies_x_alternative, spatial_LED_frequencies_y_alternative = calculate_spatial_LED_frequency_components_alternative(
            LED_locations_x = LED_locations_x, 
            LED_locations_y = LED_locations_y,
            patch_offset_x = patch_offset_x,
            patch_offset_y = patch_offset_y,
            z_LED = setup_parameters.LED_info.array_to_object_distance, 
            spatial_frequency = spatial_frequency
        )
 
        low_res_CTF = calculate_coherent_transfer_function(
            pixel_size = raw_object_pixel_size,
            image_region_size = patch_size, 
            spatial_cutoff_frequency = spatial_cutoff_frequency
        )


        high_res_object_x_positions, high_res_object_y_positions = calculate_position_mesh_grids(final_object_pixel_size, 
                                                                                                 image_region_size=final_image_size)
        high_res_non_telecentric_object_plane_phase_correction = calculate_object_plane_phase_shift(
                                                                     x_mesh = high_res_object_x_positions, 
                                                                     y_mesh = high_res_object_y_positions, 
                                                                     wavevector = 2*np.pi*spatial_frequency, 
                                                                     distance = setup_parameters.lens.working_distance
                                                                 )
        high_res_spherical_illumination_object_plane_phase_correction = calculate_object_plane_phase_shift(
                                                                            x_mesh = high_res_object_x_positions, 
                                                                            y_mesh = high_res_object_y_positions, 
                                                                            wavevector = 2*np.pi*spatial_frequency, 
                                                                            distance = setup_parameters.LED_info.array_to_object_distance
                                                                        )
                    
        # assign public variables
        self.frequency = spatial_frequency
        self.cutoff_frequency = spatial_cutoff_frequency
        self.LED_frequencies_x = spatial_LED_frequencies_x
        self.LED_frequencies_y = spatial_LED_frequencies_y

        self.patch_start = patch_start
        self.patch_size = patch_size
        self.final_image_size = final_image_size
        self.raw_object_pixel_size = raw_object_pixel_size
        self.final_object_pixel_size = final_object_pixel_size
        self.pixel_scale_factor = pixel_scale_factor
        
        self.low_res_CTF = low_res_CTF
        self.high_res_spherical_illumination_correction = high_res_spherical_illumination_object_plane_phase_correction
        self.high_res_non_telecentric_correction =high_res_non_telecentric_object_plane_phase_correction


    def wavevectors_x(self):
        return 2*np.pi*self.LED_frequencies_x
    def wavevectors_y(self):
        return 2*np.pi*self.LED_frequencies_y
    def differential_wavevectors_x(self):
        return 2*np.pi / (self.final_object_pixel_size * self.final_image_size[0])
    def differential_wavevectors_y(self):
        return 2*np.pi / (self.final_object_pixel_size * self.final_image_size[1])
    



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
    patch_offset_x = (image_center_pixel_x - patch_center_pixel_x) * raw_object_pixel_size
    patch_offset_y = (image_center_pixel_y - patch_center_pixel_y) * raw_object_pixel_size
    
    return patch_offset_x, patch_offset_y


def calculate_LED_locations(LED_array_size, center_indices, LED_pitch, LED_offset):
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
    for x_index in range(x_size):
        for y_index in range(y_size):
            x_locations[y_index, x_index] = (x_index - center_indices[0]) * LED_pitch
            y_locations[y_index, x_index] = (y_index - center_indices[1]) * LED_pitch    

    # apply offset
    x_locations = x_locations + x_offset
    y_locations = y_locations + y_offset

    return x_locations, y_locations


def calculate_spatial_LED_frequency_components(LED_locations_x, LED_locations_y, patch_offset_x, patch_offset_y, z_LED, spatial_frequency):
    # find x_locations relative patch center
    locations_x = patch_offset_x - LED_locations_x
    locations_y = patch_offset_y - LED_locations_y
    
    # find relative frequency values
    freqs_x_relative = locations_x / np.sqrt(locations_x**2 + locations_y**2 + z_LED**2)
    freqs_y_relative = locations_y / np.sqrt(locations_x**2 + locations_y**2 + z_LED**2)

    # multiply by frequency magnitude
    spatial_frequencies_x = spatial_frequency * freqs_x_relative
    spatial_frequencies_y = spatial_frequency * freqs_y_relative

    return spatial_frequencies_x, spatial_frequencies_y


def calculate_spatial_LED_frequency_components_alternative(LED_locations_x, LED_locations_y, patch_offset_x, patch_offset_y, z_LED, spatial_frequency):
    return "Not implemented yet :)", None


def calculate_coherent_transfer_function(pixel_size, image_region_size, spatial_cutoff_frequency):
    fx_mesh, fy_mesh = calculate_frequency_mesh_grids(pixel_size=pixel_size, image_region_size=image_region_size)
    
    coherent_transfer_function = (fx_mesh**2 + fy_mesh**2) < spatial_cutoff_frequency**2

    return coherent_transfer_function 

def calculate_frequency_mesh_grids(pixel_size, image_region_size):
    max_frequency = 1 / (2 * pixel_size)
    spatial_frequencies_x = np.linspace(start = -max_frequency, stop = max_frequency, num = image_region_size[0], endpoint = True)  
    spatial_frequencies_y = np.linspace(start = -max_frequency, stop = max_frequency, num = image_region_size[1], endpoint = True)

    fx_mesh, fy_mesh = np.meshgrid(spatial_frequencies_x, spatial_frequencies_y)
    
    return fx_mesh, fy_mesh

def calculate_position_mesh_grids(pixel_size, image_region_size):

    max_position_x = image_region_size[0] * pixel_size / 2
    max_position_y = image_region_size[1] * pixel_size / 2

    positions_x = np.linspace(start = -max_position_x, stop = max_position_x, num = image_region_size[0], endpoint = True)
    positions_y = np.linspace(start = -max_position_y, stop = max_position_y, num = image_region_size[1], endpoint = True)

    x_mesh, y_mesh = np.meshgrid(positions_x, positions_y)
    
    return x_mesh, y_mesh


def calculate_object_plane_phase_shift(x_mesh, y_mesh, wavevector, distance):
    return np.exp(1j * wavevector * 1/(2*distance) * (x_mesh**2 + y_mesh**2))
