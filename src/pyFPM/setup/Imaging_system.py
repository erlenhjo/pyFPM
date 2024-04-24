import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt #for debug

from pyFPM.setup.Setup_parameters import Setup_parameters

@dataclass
class LED_calibration_parameters:
    LED_distance: float
    LED_x_offset: float
    LED_y_offset: float
    LED_rotation: float


class Imaging_system(object):
    def __init__(self, setup_parameters: Setup_parameters, pixel_scale_factor,
                  patch_offset, patch_size, calibration_parameters: LED_calibration_parameters,
                  binned_image_size):
        
        spatial_frequency = 1 / setup_parameters.LED_info.wavelength
        spatial_cutoff_frequency = calculate_spatial_cutoff_frequency(spatial_frequency, setup_parameters.lens.NA)
        
        binning_factor = setup_parameters.binning_factor
        raw_object_pixel_size = setup_parameters.camera.camera_pixel_size / setup_parameters.lens.magnification * binning_factor
        final_object_pixel_size = raw_object_pixel_size / pixel_scale_factor
        final_image_size = [pixel_scale_factor * size for size in patch_size]

        effective_object_to_aperture_distance = setup_parameters.lens.effective_object_to_aperture_distance
        
        # calculate offsets
        patch_offset_x, patch_offset_y = calculate_patch_offset_distance(
            patch_offset = patch_offset,
            raw_object_pixel_size = raw_object_pixel_size
        )

        patch_start, patch_end = calculate_patch_start_and_end(
            image_size = binned_image_size,
            patch_offset = patch_offset,
            patch_size = patch_size
        )

        # calculate LED positions
        LED_locations_x, LED_locations_y = calculate_LED_locations(
            LED_array_size = setup_parameters.LED_info.LED_array_size,
            center_indices = setup_parameters.LED_info.center_indices,
            LED_pitch = setup_parameters.LED_info.LED_pitch,
            LED_rotation = calibration_parameters.LED_rotation,
            LED_offset = np.array(setup_parameters.LED_info.LED_offset) \
                + np.array([calibration_parameters.LED_x_offset,calibration_parameters.LED_y_offset])
        )
        
        # calculate frequency components for Zheng's frequency shift model
        LED_shifts_x_Zheng, LED_shifts_y_Zheng = calculate_LED_shifts_from_in_plane_frequency_components(
            LED_locations_x = LED_locations_x, 
            LED_locations_y = LED_locations_y,
            patch_offset_x = patch_offset_x,
            patch_offset_y = patch_offset_y,
            z_LED = calibration_parameters.LED_distance, 
            spatial_frequency = spatial_frequency,
            pixel_size = final_object_pixel_size,
            image_size = final_image_size
        )

        # calculate frequency components for alternative frequency shift model (Fresnel propagation based?)
        LED_shifts_x_Fresnel, LED_shifts_y_Fresnel = calculate_LED_shifts_Fresnel(
            LED_locations_x = LED_locations_x, 
            LED_locations_y = LED_locations_y,
            patch_offset_x = patch_offset_x,
            patch_offset_y = patch_offset_y,
            z_LED = calibration_parameters.LED_distance,
            z_q = effective_object_to_aperture_distance, 
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

        # caculate positions relative the center of the Field of View
        high_res_object_x_positions, high_res_object_y_positions = calculate_relative_position_mesh_grids(
                                                                            pixel_size = final_object_pixel_size, 
                                                                            image_region_size = final_image_size
                                                                        ) 
        high_res_Fresnel_object_phase_correction = calculate_object_plane_phase_curvature(
                                                    x_mesh = high_res_object_x_positions, 
                                                    y_mesh = high_res_object_y_positions, 
                                                    wavevector = 2*np.pi*spatial_frequency, 
                                                    distance = effective_object_to_aperture_distance
                                                )
        high_res_spherical_illumination_object_phase_correction = calculate_object_plane_phase_curvature(
                                                                    x_mesh = high_res_object_x_positions, 
                                                                    y_mesh = high_res_object_y_positions, 
                                                                    wavevector = 2*np.pi*spatial_frequency, 
                                                                    distance = calibration_parameters.LED_distance
                                                                )
        
        BF_edge_masks, mask_index_per_LED = get_BF_edge_mask(
                                                LED_locations_x = LED_locations_x, 
                                                LED_locations_y = LED_locations_y, 
                                                patch_offset_x = patch_offset_x, 
                                                patch_offset_y = patch_offset_y,
                                                z_LED = calibration_parameters.LED_distance, 
                                                z_q = effective_object_to_aperture_distance, 
                                                numerical_aperture = setup_parameters.lens.NA,
                                                raw_object_pixel_size = raw_object_pixel_size, 
                                                patch_size = patch_size
                                            )
                            
        # assign public variables
        self.frequency = spatial_frequency
        self.cutoff_frequency = spatial_cutoff_frequency
        self.LED_shifts_x_Zheng = LED_shifts_x_Zheng
        self.LED_shifts_y_Zheng = LED_shifts_y_Zheng
        self.LED_shifts_x_Fresnel = LED_shifts_x_Fresnel
        self.LED_shifts_y_Fresnel = LED_shifts_y_Fresnel
        self.df_x = 1/(final_object_pixel_size * final_image_size[0])
        self.df_y = 1/(final_object_pixel_size * final_image_size[1])

        self.patch_offset = patch_offset
        self.patch_start = patch_start
        self.patch_end = patch_end
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
        self.BF_edge_masks = BF_edge_masks
        self.mask_index_per_LED = mask_index_per_LED

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


def calculate_patch_start_and_end(image_size, patch_offset, patch_size):
    x_start = image_size[0] // 2 + patch_offset[0] - patch_size[0]//2
    y_start = image_size[1] // 2 + patch_offset[1] - patch_size[1]//2
    x_end = x_start + patch_size[0]
    y_end = y_start + patch_size[1]
    patch_start = [x_start, y_start]
    patch_end = [x_end, y_end]
    return patch_start, patch_end


def calculate_patch_offset_distance(patch_offset, raw_object_pixel_size):
    patch_offset_x = patch_offset[0] * raw_object_pixel_size
    patch_offset_y = patch_offset[1] * raw_object_pixel_size
    return patch_offset_x, patch_offset_y


def calculate_LED_locations(LED_array_size, center_indices, LED_pitch, LED_rotation, LED_offset):
    # note [y, x] indexing due to how matrix indexing works (row, col) -> (y, x)
    # arraysize + 1 in case LED array is one indexed
    x_size = LED_array_size[0] + 1 
    y_size = LED_array_size[1] + 1

    # misalignment of LEDs with respect to optical axis
    x_offset = LED_offset[0]
    y_offset = LED_offset[1]

    x_locations = np.zeros(shape=(y_size , x_size))
    y_locations = np.zeros(shape=(y_size , x_size))

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


def calculate_LED_shifts_Fresnel(LED_locations_x, LED_locations_y, 
                                 patch_offset_x, patch_offset_y, 
                                 z_LED, z_q, wavelength,
                                 pixel_size, image_size):
    df_x = 1/(pixel_size * image_size[0])
    df_y = 1/(pixel_size * image_size[1])

    #calculate spatial shift
    frequency_shifts_x = ((LED_locations_x-patch_offset_x)/z_LED - patch_offset_x/z_q)/wavelength
    frequency_shifts_y = ((LED_locations_y-patch_offset_y)/z_LED - patch_offset_y/z_q)/wavelength

    #calculate pixel shift
    pixel_shifts_x = frequency_shifts_x/df_x
    pixel_shifts_y = frequency_shifts_y/df_y
    
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

def calculate_relative_position_mesh_grids(pixel_size, image_region_size):
    FOV_x = image_region_size[0] * pixel_size
    FOV_y = image_region_size[1] * pixel_size
    positions_x = np.linspace(start = -FOV_x/2, stop = FOV_x/2, num = image_region_size[0], endpoint = False)
    positions_y = np.linspace(start = -FOV_y/2, stop = FOV_y/2, num = image_region_size[1], endpoint = False)

    x_mesh, y_mesh = np.meshgrid(positions_x, positions_y)
    
    return x_mesh, y_mesh


def calculate_object_plane_phase_curvature(x_mesh, y_mesh, wavevector, distance):
    return np.exp(1j * wavevector * 1/(2*distance) * (x_mesh**2 + y_mesh**2))


def get_BF_edge_mask(LED_locations_x, LED_locations_y, 
                     patch_offset_x, patch_offset_y,
                     z_LED, z_q, numerical_aperture,
                     raw_object_pixel_size, patch_size):
    

    local_x_coords, local_y_coords = calculate_relative_position_mesh_grids(pixel_size = raw_object_pixel_size, 
                                                                            image_region_size = patch_size)
    
    x_coords = local_x_coords + patch_offset_x
    y_coords = local_y_coords + patch_offset_y

    BF_edge_masks = []
    mask_nr_per_LED = np.full(shape=LED_locations_x.shape, fill_value=-1, dtype=np.int8)
    current_mask_nr = 0

    for Y in range(LED_locations_x.shape[0]):
        for X in range(LED_locations_x.shape[1]):
            relative_frequency_shift_x_per_pixel = ((LED_locations_x[Y,X] - x_coords)/z_LED - x_coords/z_q)
            relative_frequency_shift_y_per_pixel = ((LED_locations_y[Y,X] - y_coords)/z_LED - y_coords/z_q)

            absolute_frequency_per_pixel = np.sqrt(relative_frequency_shift_x_per_pixel**2 + relative_frequency_shift_y_per_pixel**2)
            mask_inner = absolute_frequency_per_pixel > numerical_aperture * 0.9
            mask_outer = absolute_frequency_per_pixel < numerical_aperture * 1.2

            mask: np.ndarray = mask_inner & mask_outer # elementwise and

            
            if mask.sum():
                mask_nr_per_LED[Y,X] = current_mask_nr
                current_mask_nr += 1
                BF_edge_masks.append(mask)

    return np.array(BF_edge_masks), mask_nr_per_LED