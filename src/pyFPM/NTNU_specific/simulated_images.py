from pyFPM.NTNU_specific.components import INFINITYCORRECTED_2X, MAIN_LED_ARRAY
from pyFPM.setup.Setup_parameters import Camera
from pyFPM.NTNU_specific.simulate_imaging import simulate_imaging, finalize_simulation_setup

import numpy as np
import skimage


def simulate_cameraman_2x(zernike_coefficients, noise_fraction):
    
    amplitude_image = skimage.data.camera()
    phase_image = np.zeros(shape=amplitude_image.shape)
    high_res_complex_object = amplitude_image * np.exp(1j*phase_image)
    pixel_scale_factor = 4
    arraysize = 9
    low_res_image_size = [amplitude_image.shape[1]//pixel_scale_factor, amplitude_image.shape[0]//pixel_scale_factor]
    
    lens = INFINITYCORRECTED_2X
    LED_array = MAIN_LED_ARRAY
    array_to_object_distance = 0.200 # m

    dummy_camera = Camera(
            camera_pixel_size = 6e-6,
            raw_image_size = low_res_image_size,
            bit_depth = int(2**8-1)
            )

    setup_parameters, simulated_data, pupil = simulate_imaging(
        high_res_complex_object = high_res_complex_object,
        zernike_coefficients = zernike_coefficients,
        noise_fraction = noise_fraction,
        camera = dummy_camera,
        lens = lens,
        LED_array = LED_array,
        array_to_object_distance = array_to_object_distance,
        arraysize = arraysize,
        pixel_scale_factor = pixel_scale_factor
    )

    data_patch, imaging_system, illumination_pattern \
        = finalize_simulation_setup(
            setup_parameters = setup_parameters,
            simulated_data = simulated_data,
            patch_start = [0, 0],
            patch_size = setup_parameters.camera.raw_image_size,
            pixel_scale_factor = pixel_scale_factor
        )
    
    return setup_parameters, data_patch, imaging_system, illumination_pattern, pupil

