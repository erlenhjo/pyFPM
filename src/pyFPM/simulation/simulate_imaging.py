from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.setup.Data import Simulated_data, Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.simulation.fraunhofer_simulator import simulate_fraunhofer_imaging
from pyFPM.aberrations.pupils.zernike_pupil import get_zernike_pupil

import numpy as np


def simulate_imaging(
    high_res_complex_object,
    zernike_coefficients,
    noise_fraction,
    setup_parameters,
    arraysize,
    pixel_scale_factor
):
      
    # Define simulated data set
    center_LED = setup_parameters.LED_info.center_indices
    x_start = center_LED[0] - arraysize//2
    y_start = center_LED[1] - arraysize//2
    x_stop = x_start + arraysize
    y_stop = y_start + arraysize

    LED_indices = [[x, y] for x in range(x_start, x_stop) for y in range(y_start, y_stop)]

    full_image_imaging_system = Imaging_system(
        setup_parameters = setup_parameters,
        pixel_scale_factor = pixel_scale_factor,
        patch_start = [0,0],
        patch_size = setup_parameters.camera.raw_image_size,
        )
    
    pupil = get_zernike_pupil(full_image_imaging_system, zernike_coefficients)

    low_res_images \
        = simulate_fraunhofer_imaging(
            high_res_complex_object,
            pupil,
            LED_indices,
            full_image_imaging_system)
    
    # will get back to this :)
    # low_res_images = apply_gaussian_noise(low_res_images, noise_fraction)

    simulated_data = Simulated_data(LED_indices=LED_indices, amplitude_images=low_res_images)
    
    return simulated_data, pupil, full_image_imaging_system.low_res_CTF

def finalize_simulation_setup(
    setup_parameters,
    simulated_data,
    patch_start,
    patch_size,
    pixel_scale_factor
):
    # Adapt simulated dataset for further use

    imaging_system = Imaging_system(
        setup_parameters = setup_parameters,
        pixel_scale_factor = pixel_scale_factor,
        patch_start = patch_start,
        patch_size = patch_size
        )

    data_patch = Data_patch(data = simulated_data,
                            patch_start = patch_start,
                            patch_size = patch_size)

    illumination_pattern = Illumination_pattern(
        LED_indices = simulated_data.LED_indices,
        imaging_system = imaging_system,
        setup_parameters = setup_parameters
    )

    return data_patch, imaging_system, illumination_pattern





